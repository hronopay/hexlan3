import os

file_h = "src/wallet.h"
file_cpp = "src/wallet.cpp"

# --- Патчим wallet.h ---
with open(file_h, 'r', encoding='utf-8') as f:
    content_h = f.read()

old_h1 = """    bool fWalletUnlockAnonymizeOnly;
    SecureString strMnemonic;
    SecureString strMnemonicPassphrase;
    int nBip39Counter;
    std::string strWalletFile;"""

new_h1 = """    bool fWalletUnlockAnonymizeOnly;
    SecureString strMnemonic;
    SecureString strMnemonicPassphrase;
    int nBip39Counter;
    CExtKey cachedMasterKey;
    bool fMasterKeyCached;
    std::string strWalletFile;"""

old_h2 = """        nLastFilteredHeight = 0;
        fWalletUnlockAnonymizeOnly = false;
    }"""

new_h2 = """        nLastFilteredHeight = 0;
        fWalletUnlockAnonymizeOnly = false;
        fMasterKeyCached = false;
    }"""

if old_h1 in content_h and old_h2 in content_h:
    content_h = content_h.replace(old_h1, new_h1).replace(old_h2, new_h2)
    with open(file_h, 'w', encoding='utf-8') as f:
        f.write(content_h)
    print("wallet.h успешно пропатчен (добавлен кэш)!")
else:
    print("Ошибка: Блоки в wallet.h не найдены!")

# --- Патчим wallet.cpp ---
with open(file_cpp, 'r', encoding='utf-8') as f:
    content_cpp = f.read()

old_c1 = """    if (strMnemonic.empty()) {
        throw std::runtime_error("CWallet::GenerateNewKey() : Wallet is not initialized with BIP39 seed phrase");
    }

    std::vector<uint8_t> vchSeed;
    SecureString secureMnemonic(strMnemonic.begin(), strMnemonic.end());
    SecureString securePassphrase(strMnemonicPassphrase.begin(), strMnemonicPassphrase.end());
    BIP39::MnemonicToSeed(secureMnemonic, securePassphrase, vchSeed);
    
    CExtKey masterKey;
    masterKey.SetMaster(&vchSeed[0], vchSeed.size());

    // Стандарт деривации BIP44: m / 44' / 0' / 0' / 0 / nBip39Counter
    // 0x80000000 означает hardened (усиленную) деривацию
    CExtKey purposeKey, coinTypeKey, accountKey, changeKey, childKey;
    masterKey.Derive(purposeKey, 84 | 0x80000000); // BIP84 Native SegWit"""

new_c1 = """    if (strMnemonic.empty()) {
        throw std::runtime_error("CWallet::GenerateNewKey() : Wallet is not initialized with BIP39 seed phrase");
    }

    if (!fMasterKeyCached) {
        std::vector<uint8_t> vchSeed;
        SecureString secureMnemonic(strMnemonic.begin(), strMnemonic.end());
        SecureString securePassphrase(strMnemonicPassphrase.begin(), strMnemonicPassphrase.end());
        BIP39::MnemonicToSeed(secureMnemonic, securePassphrase, vchSeed);
        
        cachedMasterKey.SetMaster(&vchSeed[0], vchSeed.size());
        fMasterKeyCached = true;
    }

    // Стандарт деривации BIP44: m / 44' / 0' / 0' / 0 / nBip39Counter
    // 0x80000000 означает hardened (усиленную) деривацию
    CExtKey purposeKey, coinTypeKey, accountKey, changeKey, childKey;
    cachedMasterKey.Derive(purposeKey, 84 | 0x80000000); // BIP84 Native SegWit"""

if old_c1 in content_cpp:
    content_cpp = content_cpp.replace(old_c1, new_c1)
    with open(file_cpp, 'w', encoding='utf-8') as f:
        f.write(content_cpp)
    print("wallet.cpp успешно пропатчен (логика кэширования внедрена)!")
else:
    print("Ошибка: Блок в wallet.cpp не найден!")

