// Copyright (c) 2017 Pieter Wuille
// Distributed under the MIT software license

#include "bech32.h"

namespace bech32
{

namespace
{

typedef std::vector<uint8_t> data;

/** The Bech32 character set for encoding. */
const char* CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l";

/** The Bech32 character set for decoding. */
const int8_t CHARSET_REV[128] = {
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    15, -1, 10, 17, 21, 20, 26, 30,  7,  5, -1, -1, -1, -1, -1, -1,
    -1, 29, -1, 24, 13, 25,  9,  8, 23, -1, 18, 22, 31, 27, 19, -1,
     1,  0,  3, 16, 11, 28, 12, 14,  6,  4,  2, -1, -1, -1, -1, -1,
    -1, 29, -1, 24, 13, 25,  9,  8, 23, -1, 18, 22, 31, 27, 19, -1,
     1,  0,  3, 16, 11, 28, 12, 14,  6,  4,  2, -1, -1, -1, -1, -1
};

uint32_t Polymod(const data& values)
{
    uint32_t chk = 1;
    for (size_t i = 0; i < values.size(); ++i) {
        uint8_t v = values[i];
        uint8_t b = chk >> 25;
        chk = ((chk & 0x1ffffff) << 5) ^ v;
        if (b & 1) chk ^= 0x3b6a57b2;
        if (b & 2) chk ^= 0x26508e6d;
        if (b & 4) chk ^= 0x1ea119fa;
        if (b & 8) chk ^= 0x3d4233dd;
        if (b & 16) chk ^= 0x2a1462b3;
    }
    return chk;
}

data ExpandHRP(const std::string& hrp)
{
    data ret;
    ret.reserve(hrp.size() + 90);
    ret.resize(hrp.size() * 2 + 1);
    for (size_t i = 0; i < hrp.size(); ++i) {
        unsigned char c = hrp[i];
        ret[i] = c >> 5;
        ret[i + hrp.size() + 1] = c & 0x1f;
    }
    ret[hrp.size()] = 0;
    return ret;
}

bool VerifyChecksum(const std::string& hrp, const data& values)
{
    data enc = ExpandHRP(hrp);
    enc.insert(enc.end(), values.begin(), values.end());
    return Polymod(enc) == 1;
}

data CreateChecksum(const std::string& hrp, const data& values)
{
    data enc = ExpandHRP(hrp);
    enc.insert(enc.end(), values.begin(), values.end());
    enc.resize(enc.size() + 6);
    uint32_t mod = Polymod(enc) ^ 1;
    data ret;
    ret.resize(6);
    for (size_t i = 0; i < 6; ++i) {
        ret[i] = (mod >> (5 * (5 - i))) & 31;
    }
    return ret;
}

} // namespace

std::string Encode(const std::string& hrp, const data& values)
{
    data checksum = CreateChecksum(hrp, values);
    data combined = values;
    combined.insert(combined.end(), checksum.begin(), checksum.end());
    std::string ret = hrp + "1";
    ret.reserve(ret.size() + combined.size());
    for (size_t i = 0; i < combined.size(); ++i) {
        ret += CHARSET[combined[i]];
    }
    return ret;
}

std::pair<std::string, data> Decode(const std::string& str)
{
    bool lower = false, upper = false;
    for (size_t i = 0; i < str.size(); ++i) {
        unsigned char c = str[i];
        if (c < 33 || c > 126) return std::make_pair(std::string(), data());
        if (c >= 'a' && c <= 'z') lower = true;
        if (c >= 'A' && c <= 'Z') upper = true;
    }
    if (lower && upper) return std::make_pair(std::string(), data());
    size_t pos = str.rfind('1');
    if (pos == str.npos || pos == 0 || pos + 7 > str.size() || str.size() > 90) {
        return std::make_pair(std::string(), data());
    }
    data values;
    values.resize(str.size() - 1 - pos);
    for (size_t i = 0; i < str.size() - 1 - pos; ++i) {
        unsigned char c = str[i + pos + 1];
        int8_t rev = CHARSET_REV[c];
        if (rev == -1) {
            return std::make_pair(std::string(), data());
        }
        values[i] = rev;
    }
    std::string hrp;
    for (size_t i = 0; i < pos; ++i) {
        hrp += str[i];
    }
    for (size_t i = 0; i < hrp.size(); ++i) {
        if (hrp[i] >= 'A' && hrp[i] <= 'Z') hrp[i] = (hrp[i] - 'A') + 'a';
    }
    if (!VerifyChecksum(hrp, values)) {
        return std::make_pair(std::string(), data());
    }
    return std::make_pair(hrp, data(values.begin(), values.end() - 6));
}

} // namespace bech32
