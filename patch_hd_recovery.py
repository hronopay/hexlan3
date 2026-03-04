import re

with open("src/wallet.cpp", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Обновляем GenerateNewKey
pattern_newkey = r'CPubKey CWallet::GenerateNewKey\(\).*?(?=static CPubKey g_cachedChangePubKey;)'
repl_newkey = """CPubKey CWallet::GenerateNewKey()
{
    AssertLockHeld(cs_wallet);
    bool fCompressed = CanSupportFeature(FEATURE_COMPRPUBKEY);

    if (strMnemonic.empty())
        throw std::runtime_error("CWallet::GenerateNewKey() : Wallet is not initialized with BIP39 seed phrase");

    if (!fMasterKeyCached) {
        std::vector<uint8_t> vchSeed;
        SecureString secureMnemonic(strMnemonic.begin(), strMnemonic.end());
        SecureString securePassphrase(strMnemonicPassphrase.begin(), strMnemonicPassphrase.end());
        BIP39::MnemonicToSeed(secureMnemonic, securePassphrase, vchSeed);
        cachedMasterKey.SetMaster(&vchSeed[0], vchSeed.size());
        fMasterKeyCached = true;
    }

    CExtKey purposeKey, coinTypeKey, accountKey, changeKey;
    cachedMasterKey.Derive(purposeKey, 84 | 0x80000000);
    purposeKey.Derive(coinTypeKey, 0 | 0x80000000);
    coinTypeKey.Derive(accountKey, 0 | 0x80000000);
    accountKey.Derive(changeKey, 0); // Внешние адреса

    CKey secret;
    CPubKey pubkey;

    // Самовосстанавливающийся цикл поиска свободного адреса
    while (true) {
        CExtKey childKey;
        changeKey.Derive(childKey, nBip39Counter);
        secret = childKey.key;
        pubkey = secret.GetPubKey();
        assert(secret.VerifyPubKey(pubkey));

        if (HaveKey(pubkey.GetID())) {
            LogPrintf("TRACE: [GenerateNewKey] Key index %d already exists, advancing...\\n", nBip39Counter);
            nBip39Counter++;
            continue;
        }

        if (AddKeyPubKey(secret, pubkey)) {
            nBip39Counter++;
            CWalletDB(strWalletFile).WriteBip39Counter(nBip39Counter);
            break;
        } else {
            LogPrintf("ERROR: [GenerateNewKey] AddKey failed for %d, trying next...\\n", nBip39Counter);
            nBip39Counter++;
            if (nBip39Counter > 10000) throw std::runtime_error("CWallet::GenerateNewKey() : Database locked or broken");
        }
    }

    if (fCompressed) SetMinVersion(FEATURE_COMPRPUBKEY);

    int64_t nCreationTime = GetTime();
    mapKeyMetadata[pubkey.GetID()] = CKeyMetadata(nCreationTime);
    if (!nTimeFirstKey || nCreationTime < nTimeFirstKey)
        nTimeFirstKey = nCreationTime;

    return pubkey;
}

"""

# 2. Обновляем GenerateNewChangeKey (сохраняя кэш из прошлого шага)
pattern_changekey = r'CPubKey CWallet::GenerateNewChangeKey\(\).*?return pubkey;\n\}'
repl_changekey = """CPubKey CWallet::GenerateNewChangeKey()
{
    if (g_fHasCachedChangeKey) return g_cachedChangePubKey;

    AssertLockHeld(cs_wallet);
    bool fCompressed = CanSupportFeature(FEATURE_COMPRPUBKEY);

    if (strMnemonic.empty())
        throw std::runtime_error("CWallet::GenerateNewChangeKey() : Wallet is not initialized with BIP39 seed phrase");

    if (!fMasterKeyCached) {
        std::vector<uint8_t> vchSeed;
        SecureString secureMnemonic(strMnemonic.begin(), strMnemonic.end());
        SecureString securePassphrase(strMnemonicPassphrase.begin(), strMnemonicPassphrase.end());
        BIP39::MnemonicToSeed(secureMnemonic, securePassphrase, vchSeed);
        cachedMasterKey.SetMaster(&vchSeed[0], vchSeed.size());
        fMasterKeyCached = true;
    }

    CExtKey purposeKey, coinTypeKey, accountKey, changeKey;
    cachedMasterKey.Derive(purposeKey, 84 | 0x80000000);
    purposeKey.Derive(coinTypeKey, 0 | 0x80000000);
    coinTypeKey.Derive(accountKey, 0 | 0x80000000);
    accountKey.Derive(changeKey, 1); // Внутренние адреса (сдача)

    CKey secret;
    CPubKey pubkey;

    // Самовосстанавливающийся цикл поиска свободной сдачи
    while (true) {
        CExtKey childKey;
        changeKey.Derive(childKey, nBip39ChangeCounter);
        secret = childKey.key;
        pubkey = secret.GetPubKey();
        assert(secret.VerifyPubKey(pubkey));

        if (HaveKey(pubkey.GetID())) {
            LogPrintf("TRACE: [GenerateNewChangeKey] Change key %d already exists, advancing...\\n", nBip39ChangeCounter);
            nBip39ChangeCounter++;
            continue;
        }

        if (AddKeyPubKey(secret, pubkey)) {
            nBip39ChangeCounter++;
            CWalletDB(strWalletFile).WriteBip39ChangeCounter(nBip39ChangeCounter);
            break;
        } else {
            LogPrintf("ERROR: [GenerateNewChangeKey] AddKey failed for %d, trying next...\\n", nBip39ChangeCounter);
            nBip39ChangeCounter++;
            if (nBip39ChangeCounter > 10000) throw std::runtime_error("CWallet::GenerateNewChangeKey() : Database locked or broken");
        }
    }

    if (fCompressed) SetMinVersion(FEATURE_COMPRPUBKEY);

    int64_t nCreationTime = GetTime();
    mapKeyMetadata[pubkey.GetID()] = CKeyMetadata(nCreationTime);
    if (!nTimeFirstKey || nCreationTime < nTimeFirstKey)
        nTimeFirstKey = nCreationTime;

    g_cachedChangePubKey = pubkey;
    g_fHasCachedChangeKey = true;

    return pubkey;
}"""

content = re.sub(pattern_newkey, repl_newkey, content, flags=re.DOTALL)
content = re.sub(pattern_changekey, repl_changekey, content, flags=re.DOTALL)

with open("src/wallet.cpp", "w", encoding="utf-8") as f:
    f.write(content)
print("Успешно: Установлена самовосстанавливающаяся HD-архитектура!")
