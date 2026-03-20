import os

# 1. Патчим rpcserver.cpp
f_rpcserver = "src/rpcserver.cpp"
with open(f_rpcserver, "r", encoding="utf-8") as f:
    code_server = f.read()

s_decl_find = "extern json_spirit::Value getxpub(const json_spirit::Array& params, bool fHelp);"
s_decl_repl = s_decl_find + "\nextern json_spirit::Value importxpub(const json_spirit::Array& params, bool fHelp);"
if s_decl_find in code_server:
    code_server = code_server.replace(s_decl_find, s_decl_repl)

s_cmd_find = '{ "getxpub",                &getxpub,                false,     false,     true },'
s_cmd_repl = s_cmd_find + '\n    { "importxpub",             &importxpub,             false,     false,     true },'
if s_cmd_find in code_server:
    code_server = code_server.replace(s_cmd_find, s_cmd_repl)

with open(f_rpcserver, "w", encoding="utf-8") as f:
    f.write(code_server)


# 2. Патчим rpcwallet.cpp
f_rpcwallet = "src/rpcwallet.cpp"
with open(f_rpcwallet, "r", encoding="utf-8") as f:
    code_wallet = f.read()

s_find = """    result.push_back(json_spirit::Pair("xpub", hexlanXpub.ToString()));
    return result;
}"""

s_replace = s_find + """

json_spirit::Value importxpub(const json_spirit::Array& params, bool fHelp)
{
    if (fHelp || params.size() < 1 || params.size() > 3)
        throw std::runtime_error(
            "importxpub \\"xpub\\" ( lookahead rescan )\\n\\n"
            "Imports a BIP32 Extended Public Key (xpub) to watch its addresses.\\n"
            "\\nArguments:\\n"
            "1. \\"xpub\\"       (string, required) The extended public key\\n"
            "2. lookahead   (numeric, optional, default=100) How many addresses to derive (receive and change)\\n"
            "3. rescan      (boolean, optional, default=true) Rescan the blockchain for transactions\\n"
        );
    
    EnsureWalletIsUnlocked();

    std::string strXpub = params[0].get_str();
    int nLookahead = params.size() > 1 ? params[1].get_int() : 100;
    bool fRescan = params.size() > 2 ? params[2].get_bool() : true;

    CHexlanExtPubKey hexlanXpub;
    if (!hexlanXpub.SetString(strXpub))
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Invalid xpub string");

    CExtPubKey masterPubKey = hexlanXpub.GetKey();
    int nAdded = 0;

    // Генерируем ветки: m/0/i (Receive) и m/1/i (Change)
    for (int chain = 0; chain <= 1; chain++) {
        CExtPubKey chainPubKey;
        if (!masterPubKey.Derive(chainPubKey, chain)) continue;

        for (int i = 0; i < nLookahead; i++) {
            CExtPubKey childPubKey;
            if (!chainPubKey.Derive(childPubKey, i)) continue;

            CKeyID keyID = childPubKey.pubkey.GetID();
            
            // 1. Формат Bech32 (Native SegWit: OP_0 <20-byte hash>)
            CScript scriptBech32;
            std::vector<unsigned char> vch(keyID.begin(), keyID.end());
            scriptBech32 << OP_0 << vch;
            
            if (!pwalletMain->HaveWatchOnly(scriptBech32)) {
                pwalletMain->AddWatchOnly(scriptBech32);
                nAdded++;
            }
            
            // 2. Стандартный Base58 (P2PKH) для совместимости
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

if s_find in code_wallet:
    code_wallet = code_wallet.replace(s_find, s_replace)
    with open(f_rpcwallet, "w", encoding="utf-8") as f:
        f.write(code_wallet)
    print("Success! importxpub added to RPC commands.")
else:
    print("Error: Could not find insertion point in rpcwallet.cpp")
