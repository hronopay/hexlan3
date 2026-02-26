// Copyright (c) 2026 Hexlan Developers
// Distributed under the MIT software license

#include "segwit_addr.h"
#include "base58.h"
#include "bech32.h"
#include <boost/variant/apply_visitor.hpp>
#include <boost/variant/get.hpp>

// Задаем префикс адресов для SegWit в нашей сети (например, hx)
const std::string SEGWIT_HRP = "hx";

namespace {
    // Конвертер 8-битных байтов в 5-битные слова для Bech32
    bool ConvertBits(const std::vector<uint8_t>& in, std::vector<uint8_t>& out, int frombits, int tobits, bool pad) {
        int acc = 0;
        int bits = 0;
        const int maxv = (1 << tobits) - 1;
        const int max_acc = (1 << (frombits + tobits - 1)) - 1;
        for (size_t i = 0; i < in.size(); ++i) {
            int value = in[i];
            if (value < 0 || value >> frombits) return false;
            acc = ((acc << frombits) | value) & max_acc;
            bits += frombits;
            while (bits >= tobits) {
                bits -= tobits;
                out.push_back((acc >> bits) & maxv);
            }
        }
        if (pad) {
            if (bits) out.push_back((acc << (tobits - bits)) & maxv);
        } else if (bits >= frombits || ((acc << (tobits - bits)) & maxv)) {
            return false;
        }
        return true;
    }

    class DestinationEncoder : public boost::static_visitor<std::string> {
    public:
        std::string operator()(const CKeyID& id) const { return CBitcoinAddress(id).ToString(); }
        std::string operator()(const CScriptID& id) const { return CBitcoinAddress(id).ToString(); }
        std::string operator()(const CStealthAddress& id) const { return CBitcoinAddress(id).ToString(); }
        std::string operator()(const CNoDestination& no) const { return ""; }
        
        std::string operator()(const WitnessV0KeyHash& id) const {
            std::vector<uint8_t> data;
            data.push_back(0); // версия witness
            std::vector<uint8_t> prog(id.begin(), id.end());
            std::vector<uint8_t> conv;
            ConvertBits(prog, conv, 8, 5, true);
            data.insert(data.end(), conv.begin(), conv.end());
            return bech32::Encode(SEGWIT_HRP, data);
        }
        
        std::string operator()(const WitnessV0ScriptHash& id) const {
            std::vector<uint8_t> data;
            data.push_back(0); // версия witness
            std::vector<uint8_t> prog(id.begin(), id.end());
            std::vector<uint8_t> conv;
            ConvertBits(prog, conv, 8, 5, true);
            data.insert(data.end(), conv.begin(), conv.end());
            return bech32::Encode(SEGWIT_HRP, data);
        }
    };
}

std::string EncodeDestination(const CTxDestination& dest) {
    return boost::apply_visitor(DestinationEncoder(), dest);
}

CTxDestination DecodeDestination(const std::string& str) {
    CBitcoinAddress addr(str);
    if (addr.IsValid()) {
        return addr.Get();
    }
    
    std::pair<std::string, std::vector<uint8_t> > dec = bech32::Decode(str);
    if (dec.first == SEGWIT_HRP && dec.second.size() > 0) {
        int version = dec.second[0];
        if (version == 0) {
            std::vector<uint8_t> prog;
            if (ConvertBits(std::vector<uint8_t>(dec.second.begin() + 1, dec.second.end()), prog, 5, 8, false)) {
                if (prog.size() == 20) {
                    uint160 keyid;
                    memcpy(keyid.begin(), &prog[0], 20);
                    return WitnessV0KeyHash(keyid);
                } else if (prog.size() == 32) {
                    uint256 scriptid;
                    memcpy(scriptid.begin(), &prog[0], 32);
                    return WitnessV0ScriptHash(scriptid);
                }
            }
        }
    }
    return CNoDestination();
}

bool IsValidDestinationString(const std::string& str) {
    CTxDestination dest = DecodeDestination(str);
    return boost::get<CNoDestination>(&dest) == NULL;
}
