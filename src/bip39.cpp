// Copyright (c) 2026 Hexlan Developers
// Distributed under the MIT software license

#include "bip39.h"
#include "bip39_english.h"
#include "util.h"
#include <openssl/evp.h>
#include <openssl/sha.h>
#include <openssl/crypto.h>
#include <stdexcept>
#include <algorithm>

namespace BIP39 {

const std::vector<std::string>& GetWordList() {
    static std::vector<std::string> words;
    if (words.empty()) {
        words.reserve(2048);
        for (int i = 0; i < 2048; i++) {
            words.push_back(std::string(wordlist_english[i]));
        }
    }
    return words;
}

SecureString GenerateMnemonic(int nEntropyBytes) {
    if (nEntropyBytes < 16 || nEntropyBytes > 32 || nEntropyBytes % 4 != 0) {
        throw std::runtime_error("Invalid BIP39 entropy length");
    }

    std::vector<uint8_t> vchEntropy(nEntropyBytes);
    if (!GetRandBytes(&vchEntropy[0], nEntropyBytes)) {
        throw std::runtime_error("Failed to generate random entropy");
    }

    uint8_t hash[SHA256_DIGEST_LENGTH];
    SHA256(&vchEntropy[0], nEntropyBytes, hash);

    int nBits = nEntropyBytes * 8;
    int nChecksumBits = nBits / 32;

    std::vector<bool> vecBits;
    vecBits.reserve(nBits + nChecksumBits);

    for (int i = 0; i < nEntropyBytes; ++i) {
        for (int j = 7; j >= 0; --j) {
            vecBits.push_back((vchEntropy[i] & (1 << j)) != 0);
        }
    }

    for (int i = 0; i < nChecksumBits; ++i) {
        vecBits.push_back((hash[0] & (1 << (7 - i))) != 0);
    }

    const std::vector<std::string>& words = GetWordList();
    SecureString mnemonic;

    for (size_t i = 0; i < vecBits.size() / 11; ++i) {
        int index = 0;
        for (int j = 0; j < 11; ++j) {
            index <<= 1;
            if (vecBits[i * 11 + j]) {
                index |= 1;
            }
        }
        if (i > 0) {
            mnemonic.push_back(' ');
        }
        for (size_t c = 0; c < words[index].size(); ++c) {
            mnemonic.push_back(words[index][c]);
        }
    }

    OPENSSL_cleanse(&vchEntropy[0], vchEntropy.size());
    return mnemonic;
}

bool CheckMnemonic(const SecureString& mnemonic) {
    std::vector<std::string> mnemonicWords;
    std::string currentWord;
    for (size_t i = 0; i < mnemonic.size(); ++i) {
        if (mnemonic[i] == ' ') {
            if (!currentWord.empty()) {
                mnemonicWords.push_back(currentWord);
                currentWord.clear();
            }
        } else {
            currentWord += mnemonic[i];
        }
    }
    if (!currentWord.empty()) {
        mnemonicWords.push_back(currentWord);
    }

    if (mnemonicWords.size() < 12 || mnemonicWords.size() > 24 || mnemonicWords.size() % 3 != 0) {
        return false;
    }

    const std::vector<std::string>& words = GetWordList();
    std::vector<int> wordIndices;
    wordIndices.reserve(mnemonicWords.size());

    for (size_t i = 0; i < mnemonicWords.size(); ++i) {
        auto it = std::find(words.begin(), words.end(), mnemonicWords[i]);
        if (it == words.end()) {
            return false;
        }
        wordIndices.push_back(std::distance(words.begin(), it));
    }

    std::vector<bool> vecBits;
    vecBits.reserve(wordIndices.size() * 11);
    for (size_t i = 0; i < wordIndices.size(); ++i) {
        for (int j = 10; j >= 0; --j) {
            vecBits.push_back((wordIndices[i] & (1 << j)) != 0);
        }
    }

    int nChecksumBits = vecBits.size() / 33;
    int nEntropyBits = vecBits.size() - nChecksumBits;
    int nEntropyBytes = nEntropyBits / 8;

    std::vector<uint8_t> vchEntropy(nEntropyBytes, 0);
    for (int i = 0; i < nEntropyBytes; ++i) {
        for (int j = 0; j < 8; ++j) {
            if (vecBits[i * 8 + j]) {
                vchEntropy[i] |= (1 << (7 - j));
            }
        }
    }

    uint8_t hash[SHA256_DIGEST_LENGTH];
    SHA256(&vchEntropy[0], nEntropyBytes, hash);

    for (int i = 0; i < nChecksumBits; ++i) {
        bool expectedBit = (hash[0] & (1 << (7 - i))) != 0;
        if (vecBits[nEntropyBits + i] != expectedBit) {
            OPENSSL_cleanse(&vchEntropy[0], vchEntropy.size());
            return false;
        }
    }

    OPENSSL_cleanse(&vchEntropy[0], vchEntropy.size());
    return true;
}

void MnemonicToSeed(const SecureString& mnemonic, const SecureString& passphrase, std::vector<uint8_t>& vchSeedRet) {
    SecureString salt;
    const char* prefix = "mnemonic";
    for (int i = 0; prefix[i] != '\0'; ++i) {
        salt.push_back(prefix[i]);
    }
    for (size_t i = 0; i < passphrase.size(); ++i) {
        salt.push_back(passphrase[i]);
    }

    vchSeedRet.resize(64);
    
    PKCS5_PBKDF2_HMAC(mnemonic.c_str(), mnemonic.size(),
                      (const unsigned char*)salt.c_str(), salt.size(),
                      2048, EVP_sha512(),
                      64, &vchSeedRet[0]);
}

} // namespace BIP39
