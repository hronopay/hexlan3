import os

fpath = "src/rpcwallet.cpp"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("json_spirit::Value getxpub")
if idx != -1:
    code = code[:idx] + """json_spirit::Value getxpub(const json_spirit::Array& params, bool fHelp)
{
    if (fHelp || params.size() != 0)
        throw std::runtime_error("getxpub\\n\\nReturns the extended public key (xpub) for Watch-Only HD wallets.");
    
    EnsureWalletIsUnlocked();

    if (pwalletMain->strMnemonic.empty())
        throw JSONRPCError(RPC_WALLET_ERROR, "Mnemonic is empty. Wallet must be initialized with BIP39 first.");

    // Генерируем seed из мнемоники на лету
    std::vector<uint8_t> vchSeed;
    BIP39::MnemonicToSeed(pwalletMain->strMnemonic, pwalletMain->strMnemonicPassphrase, vchSeed);
    
    // Создаем мастер-ключ
    CExtKey masterKey;
    masterKey.SetMaster(&vchSeed[0], vchSeed.size());

    // Кастрируем приватный ключ, получая публичный (Neuter)
    CExtPubKey xpub = masterKey.Neuter();
    
    // Оборачиваем в Base58 формат сети Hexlan
    CHexlanExtPubKey hexlanXpub;
    hexlanXpub.SetKey(xpub);

    json_spirit::Object result;
    result.push_back(json_spirit::Pair("xpub", hexlanXpub.ToString()));
    return result;
}
"""
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code)
    print("Success! getxpub now properly derives the key from BIP39 seed.")
else:
    print("Error: Could not find getxpub function in file.")
