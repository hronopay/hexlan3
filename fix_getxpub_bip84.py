import os

fpath = "src/rpcwallet.cpp"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

idx_start = code.find("json_spirit::Value getxpub")
if idx_start != -1:
    idx_end = code.find("return result;\n}", idx_start)
    if idx_end != -1:
        idx_end += len("return result;\n}")
        new_func = """json_spirit::Value getxpub(const json_spirit::Array& params, bool fHelp)
{
    if (fHelp || params.size() != 0)
        throw std::runtime_error("getxpub\\n\\nReturns the extended public key (xpub) for Watch-Only HD wallets.");
    
    EnsureWalletIsUnlocked();

    if (pwalletMain->strMnemonic.empty())
        throw JSONRPCError(RPC_WALLET_ERROR, "Mnemonic is empty. Wallet must be initialized with BIP39 first.");

    // Генерируем seed из мнемоники на лету
    std::vector<uint8_t> vchSeed;
    BIP39::MnemonicToSeed(pwalletMain->strMnemonic, pwalletMain->strMnemonicPassphrase, vchSeed);
    
    // Создаем мастер-ключ (Корень 'm')
    CExtKey masterKey;
    masterKey.SetMaster(&vchSeed[0], vchSeed.size());

    // HEXLAN: BIP84 Derivation Path (Спускаемся на уровень m/84'/0'/0')
    CExtKey purposeKey, coinTypeKey, accountKey;
    masterKey.Derive(purposeKey, 84 | 0x80000000);
    purposeKey.Derive(coinTypeKey, 0 | 0x80000000);
    coinTypeKey.Derive(accountKey, 0 | 0x80000000);

    // Кастрируем account-ключ, получая публичный (Account xpub)
    CExtPubKey xpub = accountKey.Neuter();
    
    // Оборачиваем в Base58 формат сети Hexlan
    CHexlanExtPubKey hexlanXpub;
    hexlanXpub.SetKey(xpub);

    json_spirit::Object result;
    result.push_back(json_spirit::Pair("xpub", hexlanXpub.ToString()));
    return result;
}"""
        code = code[:idx_start] + new_func + code[idx_end:]
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(code)
        print("Success! getxpub now correctly exports the m/84'/0'/0' account key.")
else:
    print("Error: Could not find getxpub function.")
