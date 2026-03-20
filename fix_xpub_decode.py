import os

f_rpc = "src/rpcwallet.cpp"
with open(f_rpc, "r", encoding="utf-8") as f:
    code = f.read()

s_find = """    // HEXLAN: Возвращаем родной парсер (исправляет ошибку линковщика)
    CHexlanExtPubKey hexlanXpub;
    if (!hexlanXpub.SetString(strXpub))
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Invalid xpub string format (Base58 failed)");

    CExtPubKey masterPubKey = hexlanXpub.GetKey();

    // HEXLAN: Защита от Core Dump! Если xpub расшифрован с ошибкой - прерываем мягко
    if (!masterPubKey.pubkey.IsValid())
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Decoded xpub is corrupted or invalid. Cannot derive addresses.");"""

s_replace = """    // HEXLAN: Пуленепробиваемое ручное декодирование (в обход бага сдвига байтов)
    std::vector<unsigned char> vchRet;
    if (!DecodeBase58(strXpub, vchRet))
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Invalid xpub string format (Base58 decode failed)");

    if (vchRet.size() != 82)
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, strprintf("Invalid xpub length. Expected 82 bytes, got %d", vchRet.size()));

    // Проверка контрольной суммы (Double SHA256)
    uint256 hash = Hash(vchRet.begin(), vchRet.end() - 4);
    if (memcmp(&hash, &vchRet[vchRet.size() - 4], 4) != 0)
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Invalid xpub checksum");

    CExtPubKey masterPubKey;
    masterPubKey.Decode(&vchRet[4]); // Точный сдвиг на 4 байта версии

    if (!masterPubKey.pubkey.IsValid())
        throw JSONRPCError(RPC_INVALID_ADDRESS_OR_KEY, "Decoded xpub contains invalid public key. Payload shifted?");"""

if s_find in code:
    code = code.replace(s_find, s_replace)
    with open(f_rpc, "w", encoding="utf-8") as f:
        f.write(code)
    print("Success! Manual Base58Check decoder injected.")
else:
    print("Error: Could not find the parsing block.")
