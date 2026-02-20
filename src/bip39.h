// Copyright (c) 2026 Hexlan Developers
// Distributed under the MIT software license

#ifndef HEXLAN_BIP39_H
#define HEXLAN_BIP39_H

#include "allocators.h"
#include <string>
#include <vector>

namespace BIP39 {
    /**
     * Генерация мнемонической фразы на основе криптографически стойкой энтропии.
     * @param nEntropyBytes Размер энтропии в байтах (от 16 до 32, кратно 4).
     * @return SecureString, содержащая мнемоническую фразу.
     */
    SecureString GenerateMnemonic(int nEntropyBytes = 32);

    /**
     * Валидация мнемонической фразы (наличие слов в словаре и проверка SHA256 контрольной суммы).
     * @param mnemonic Фраза для проверки.
     * @return true, если фраза корректна.
     */
    bool CheckMnemonic(const SecureString& mnemonic);

    /**
     * Преобразование мнемонической фразы и пароля (соли) в 512-битный seed (PBKDF2 HMAC-SHA512).
     * @param mnemonic Мнемоническая фраза.
     * @param passphrase Пользовательский пароль (может быть пустым).
     * @param vchSeedRet Вектор, куда будет записан 64-байтовый seed.
     */
    void MnemonicToSeed(const SecureString& mnemonic, const SecureString& passphrase, std::vector<uint8_t>& vchSeedRet);
    
    /**
     * Получение стандартного английского словаря BIP39.
     */
    const std::vector<std::string>& GetWordList();
}

#endif // HEXLAN_BIP39_H
