import os

# 1. ЧИНИМ СБОРКУ И КРАШ В RPCWALLET.CPP
f_rpc = "src/rpcwallet.cpp"
with open(f_rpc, "r", encoding="utf-8") as f:
    code_rpc = f.read()

idx_start = code_rpc.find("json_spirit::Value importxpub")
if idx_start != -1:
    idx_end = code_rpc.find("return result;\n}", idx_start)
    if idx_end != -1:
        idx_end += len("return result;\n}")
        
        new_importxpub = """json_spirit::Value importxpub(const json_spirit::Array& params, bool fHelp)
{
    if (fHelp || params.size() < 1 || params.size() > 3)
        throw std::runtime_error("importxpub \\"xpub\\" ...");
    
    EnsureWalletIsUnlocked();

    std::string strXpub = params[0].get_str();
    int nLookahead = params.size() > 1 ? params[1].get_int() : 100;
    bool fRescan = params.size() > 2 ? params[2].get_bool() : true;

    // HEXLAN: Возвращаем родной парсер (исправляет ошибку линковщика)
    CHexlanExtPubKey hexlanXpub;
    if (!hexlanXpub.SetString(strXpub))
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Invalid xpub string format (Base58 failed)");

    CExtPubKey masterPubKey = hexlanXpub.GetKey();

    // HEXLAN: Защита от Core Dump! Если xpub расшифрован с ошибкой - прерываем мягко
    if (!masterPubKey.pubkey.IsValid())
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Decoded xpub is corrupted or invalid. Cannot derive addresses.");

    int nAdded = 0;

    for (int chain = 0; chain <= 1; chain++) {
        CExtPubKey chainPubKey;
        if (!masterPubKey.Derive(chainPubKey, chain)) continue;

        for (int i = 0; i < nLookahead; i++) {
            CExtPubKey childPubKey;
            if (!chainPubKey.Derive(childPubKey, i)) continue;

            CKeyID keyID = childPubKey.pubkey.GetID();
            
            CScript scriptBech32;
            std::vector<unsigned char> vch(keyID.begin(), keyID.end());
            scriptBech32 << OP_0 << vch;
            
            if (!pwalletMain->HaveWatchOnly(scriptBech32)) {
                pwalletMain->AddWatchOnly(scriptBech32);
                nAdded++;
            }
            
            CScript scriptP2PKH;
            scriptP2PKH.SetDestination(keyID);
            
            if (!pwalletMain->HaveWatchOnly(scriptP2PKH)) {
                pwalletMain->AddWatchOnly(scriptP2PKH);
                nAdded++;
            }
        }
    }

    if (fRescan && nAdded > 0) {
        pwalletMain->ScanForWalletTransactions(pindexGenesisBlock, true);
        pwalletMain->ReacceptWalletTransactions();
    }

    json_spirit::Object result;
    result.push_back(json_spirit::Pair("addresses_added", nAdded));
    result.push_back(json_spirit::Pair("rescanned", fRescan));
    return result;
}"""
        code_rpc = code_rpc[:idx_start] + new_importxpub + code_rpc[idx_end:]

with open(f_rpc, "w", encoding="utf-8") as f:
    f.write(code_rpc)


# 2. ЧИНИМ ПАДЕНИЕ ПРИ ЗАПУСКЕ ПУСТОГО КОШЕЛЬКА В WALLET.CPP
f_wallet = "src/wallet.cpp"
with open(f_wallet, "r", encoding="utf-8") as f:
    code_wallet = f.read()

idx_topup = code_wallet.find("bool CWallet::TopUpKeyPool(unsigned int kpSize)")
if idx_topup != -1:
    idx_brace = code_wallet.find("{", idx_topup)
    if idx_brace != -1:
        # Ставим предохранитель в самое начало функции
        injection = "\n    // HEXLAN: Предотвращаем падение при старте Watch-Only кошелька\n    if (strMnemonic.empty()) return false;\n"
        if "strMnemonic.empty()" not in code_wallet[idx_brace:idx_brace+100]:
            code_wallet = code_wallet[:idx_brace+1] + injection + code_wallet[idx_brace+1:]
            with open(f_wallet, "w", encoding="utf-8") as f:
                f.write(code_wallet)

print("Master fixes applied: Linker error bypassed, Startup crash fixed, Importxpub crash fixed!")
