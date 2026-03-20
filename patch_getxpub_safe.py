import os

fpath = "src/rpcwallet.cpp"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

old_code = """    // Кастрируем приватный ключ, получая публичный (Neuter)
    CExtPubKey xpub = pwalletMain->cachedMasterKey.Neuter();"""

new_code = """    // Защита от Core Dump: проверяем, что ключ реально загружен в память
    if (!pwalletMain->cachedMasterKey.key.IsValid())
        throw JSONRPCError(RPC_WALLET_ERROR, "Master Key is empty in memory. We need to derive it from the mnemonic.");

    // Кастрируем приватный ключ, получая публичный (Neuter)
    CExtPubKey xpub = pwalletMain->cachedMasterKey.Neuter();"""

if old_code in code:
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code.replace(old_code, new_code))
    print("Safeguard added! The wallet will no longer crash.")
else:
    print("Error: Could not find the code to replace.")
