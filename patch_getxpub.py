import os

# 1. Патчим rpcserver.cpp
f_rpcserver = "src/rpcserver.cpp"
with open(f_rpcserver, "r", encoding="utf-8") as f:
    code_server = f.read()

code_server = code_server.replace(
    "extern json_spirit::Value bip39dump(const json_spirit::Array& params, bool fHelp);",
    "extern json_spirit::Value bip39dump(const json_spirit::Array& params, bool fHelp);\nextern json_spirit::Value getxpub(const json_spirit::Array& params, bool fHelp);"
)

code_server = code_server.replace(
    '{ "bip39dump",              &bip39dump,              false,     false,     true },',
    '{ "bip39dump",              &bip39dump,              false,     false,     true },\n    { "getxpub",                &getxpub,                false,     false,     true },'
)

with open(f_rpcserver, "w", encoding="utf-8") as f:
    f.write(code_server)


# 2. Патчим rpcwallet.cpp
f_rpcwallet = "src/rpcwallet.cpp"
with open(f_rpcwallet, "r", encoding="utf-8") as f:
    code_wallet = f.read()

# Ищем конец функции bip39dump
s3 = '        result.push_back(json_spirit::Pair("passphrase", std::string(pwalletMain->strMnemonicPassphrase.c_str())));\n    return result;\n}'

r3 = s3 + """

json_spirit::Value getxpub(const json_spirit::Array& params, bool fHelp)
{
    if (fHelp || params.size() != 0)
        throw std::runtime_error("getxpub\\n\\nReturns the extended public key (xpub) for Watch-Only HD wallets.");
    
    EnsureWalletIsUnlocked();

    if (!pwalletMain->cachedMasterKey.IsValid())
        throw JSONRPCError(RPC_WALLET_ERROR, "HD Master Key is not valid. Wallet must be initialized with BIP39 first.");

    // Кастрируем приватный ключ, получая публичный (Neuter)
    CExtPubKey xpub = pwalletMain->cachedMasterKey.Neuter();
    
    // Оборачиваем в Base58 формат сети Hexlan
    CHexlanExtPubKey hexlanXpub;
    hexlanXpub.SetKey(xpub);

    json_spirit::Object result;
    result.push_back(json_spirit::Pair("xpub", hexlanXpub.ToString()));
    return result;
}"""

code_wallet = code_wallet.replace(s3, r3)

with open(f_rpcwallet, "w", encoding="utf-8") as f:
    f.write(code_wallet)

print("RPC commands patched successfully! 'getxpub' is now available.")
