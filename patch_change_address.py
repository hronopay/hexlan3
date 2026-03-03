import os

file_path = "src/wallet.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Внедряем функцию GenerateNewChangeKey после GenerateNewKey
func_change_key = """
CPubKey CWallet::GenerateNewChangeKey()
{
    LogPrintf("TRACE: [GenerateNewChangeKey] Start\\n");
    AssertLockHeld(cs_wallet); // mapKeyMetadata
    bool fCompressed = CanSupportFeature(FEATURE_COMPRPUBKEY);

    CKey secret;

    if (strMnemonic.empty()) {
        throw std::runtime_error("CWallet::GenerateNewChangeKey() : Wallet is not initialized with BIP39 seed phrase");
    }

    if (!fMasterKeyCached) {
        int64_t nStart = GetTimeMillis();
        std::vector<uint8_t> vchSeed;
        SecureString secureMnemonic(strMnemonic.begin(), strMnemonic.end());
        SecureString securePassphrase(strMnemonicPassphrase.begin(), strMnemonicPassphrase.end());
        BIP39::MnemonicToSeed(secureMnemonic, securePassphrase, vchSeed);
        
        cachedMasterKey.SetMaster(&vchSeed[0], vchSeed.size());
        fMasterKeyCached = true;
    }

    int64_t nStartDerive = GetTimeMillis();
    CExtKey purposeKey, coinTypeKey, accountKey, changeKey, childKey;
    cachedMasterKey.Derive(purposeKey, 84 | 0x80000000); // BIP84 Native SegWit
    purposeKey.Derive(coinTypeKey, 0 | 0x80000000);
    coinTypeKey.Derive(accountKey, 0 | 0x80000000);
    accountKey.Derive(changeKey, 1); // Внутренние адреса (сдача = 1)
    changeKey.Derive(childKey, nBip39ChangeCounter);

    secret = childKey.key;
    LogPrint("wallet", "BIP39: Change key derivation took %d ms\\n", GetTimeMillis() - nStartDerive);
    
    nBip39ChangeCounter++;
    CWalletDB(strWalletFile).WriteBip39ChangeCounter(nBip39ChangeCounter);

    if (fCompressed)
        SetMinVersion(FEATURE_COMPRPUBKEY);

    CPubKey pubkey = secret.GetPubKey();
    assert(secret.VerifyPubKey(pubkey));

    int64_t nCreationTime = GetTime();
    mapKeyMetadata[pubkey.GetID()] = CKeyMetadata(nCreationTime);
    if (!nTimeFirstKey || nCreationTime < nTimeFirstKey)
        nTimeFirstKey = nCreationTime;

    if (!AddKeyPubKey(secret, pubkey))
        throw std::runtime_error("CWallet::GenerateNewChangeKey() : AddKey failed");
    return pubkey;
}
"""

target_end = 'throw std::runtime_error("CWallet::GenerateNewKey() : AddKey failed");\n    return pubkey;\n}'

if "GenerateNewChangeKey" not in content:
    if target_end in content:
        content = content.replace(target_end, target_end + "\n\n" + func_change_key)
        print("Метод GenerateNewChangeKey успешно добавлен.")
    else:
        print("Ошибка: Не удалось найти конец метода GenerateNewKey.")

# 2. Меняем логику получения сдачи в CreateTransaction
target_change = """                        // Reserve a new key pair from key pool
                        CPubKey vchPubKey;
                        bool ret;
                        ret = reservekey.GetReservedKey(vchPubKey);
                        assert(ret); // should never fail, as we just unlocked"""

replacement_change = """                        // Reserve a new key pair from key pool
                        CPubKey vchPubKey;
                        if (!strMnemonic.empty()) {
                            // HD-кошелек: генерируем специальный адрес для сдачи на лету (BIP44 Internal 1)
                            vchPubKey = GenerateNewChangeKey();
                        } else {
                            bool ret;
                            ret = reservekey.GetReservedKey(vchPubKey);
                            assert(ret); // should never fail, as we just unlocked
                        }"""

if target_change in content:
    content = content.replace(target_change, replacement_change)
    print("Логика сдачи в CreateTransaction обновлена.")
else:
    print("Ошибка: Целевой блок в CreateTransaction не найден.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Патч для сдачи применен.")
