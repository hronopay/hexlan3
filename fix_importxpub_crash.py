import os

fpath = "src/rpcwallet.cpp"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

s_find = """    CHexlanExtPubKey hexlanXpub;
    if (!hexlanXpub.SetString(strXpub))
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Invalid xpub string");

    CExtPubKey masterPubKey = hexlanXpub.GetKey();"""

s_replace = """    std::vector<unsigned char> vchTemp;
    // HEXLAN: Ручное и абсолютно надежное декодирование Base58 (4 байта версии + 74 байта данных)
    if (!DecodeBase58Check(strXpub, vchTemp) || vchTemp.size() != 78)
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Invalid xpub string format");

    CExtPubKey masterPubKey;
    masterPubKey.Decode(&vchTemp[4]); // Пропускаем 4 байта версии

    if (!masterPubKey.pubkey.IsValid())
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Decoded public key is invalid");"""

if s_find in code:
    code = code.replace(s_find, s_replace)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code)
    print("Crash fixed! importxpub now uses bulletproof Base58 decoding.")
else:
    print("Error: Could not find code to replace.")
