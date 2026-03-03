import os

file_path = "src/wallet.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Лог перед генерацией каждого ключа в цикле
content = content.replace(
    "if (!walletdb.WritePool(nEnd, CKeyPool(GenerateNewKey())))",
    "LogPrintf(\"TRACE: [TopUpKeyPool] Generating key %d\\n\", nEnd);\n            if (!walletdb.WritePool(nEnd, CKeyPool(GenerateNewKey())))"
)

# 2. Логи внутри GenerateNewKey
content = content.replace(
    "CPubKey CWallet::GenerateNewKey()\n{",
    "CPubKey CWallet::GenerateNewKey()\n{\n    LogPrintf(\"TRACE: [GenerateNewKey] Start\\n\");"
)
content = content.replace(
    "CWalletDB(strWalletFile).WriteBip39Counter(nBip39Counter);",
    "LogPrintf(\"TRACE: [GenerateNewKey] Before WriteBip39Counter\\n\");\n    CWalletDB(strWalletFile).WriteBip39Counter(nBip39Counter);\n    LogPrintf(\"TRACE: [GenerateNewKey] After WriteBip39Counter\\n\");"
)
content = content.replace(
    "if (!AddKeyPubKey(secret, pubkey))",
    "LogPrintf(\"TRACE: [GenerateNewKey] Before AddKeyPubKey\\n\");\n    if (!AddKeyPubKey(secret, pubkey))"
)

# 3. Логи внутри AddKeyPubKey
content = content.replace(
    "bool CWallet::AddKeyPubKey(const CKey& secret, const CPubKey &pubkey)\n{",
    "bool CWallet::AddKeyPubKey(const CKey& secret, const CPubKey &pubkey)\n{\n    LogPrintf(\"TRACE: [AddKeyPubKey] Start\\n\");"
)
content = content.replace(
    "if (!CCryptoKeyStore::AddKeyPubKey(secret, pubkey))",
    "LogPrintf(\"TRACE: [AddKeyPubKey] Before CCryptoKeyStore::AddKeyPubKey\\n\");\n    if (!CCryptoKeyStore::AddKeyPubKey(secret, pubkey))"
)
content = content.replace(
    "return CWalletDB(strWalletFile).WriteKey(secret, pubkey, mapKeyMetadata[pubkey.GetID()]);",
    "LogPrintf(\"TRACE: [AddKeyPubKey] Before WriteKey\\n\");\n        bool res = CWalletDB(strWalletFile).WriteKey(secret, pubkey, mapKeyMetadata[pubkey.GetID()]);\n        LogPrintf(\"TRACE: [AddKeyPubKey] After WriteKey\\n\");\n        return res;"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Ковровая бомбардировка логами успешно завершена.")
