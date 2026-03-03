import re

file_path = "src/wallet.cpp"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

traces = [
    (r'(walletdb\.TxnBegin\(\);)', r'\1\n        LogPrintf("TRACE: 1. TxnBegin\\n");'),
    (r'(if\s*\(!walletdb\.WritePool\(nEnd,\s*CKeyPool\(GenerateNewKeyWithDB\(&walletdb\)\)\)\))', r'LogPrintf("TRACE: 2. Before WritePool and Generate\\n");\n            \1'),
    (r'(LogPrintf\("BIP39: Master key cached in %d ms\\n", GetTimeMillis\(\) - nStart\);\s*\n\s*\})', r'\1\n    LogPrintf("TRACE: 3. Master key cache block passed\\n");'),
    (r'(nBip39Counter\+\+;)', r'LogPrintf("TRACE: 4. Before WriteBip39Counter\\n");\n    \1'),
    (r'(if\s*\(!AddKeyPubKeyWithDB\(secret,\s*pubkey,\s*pwalletdb\)\))', r'LogPrintf("TRACE: 5. Before AddKeyPubKeyWithDB\\n");\n    \1'),
    (r'(bool\s+CWallet::AddKeyPubKeyWithDB[^{]*\{)', r'\1\n    LogPrintf("TRACE: 6. Entered AddKeyPubKeyWithDB\\n");'),
    (r'(if\s*\(pwalletdb\)\s*return\s*pwalletdb->WriteKey)', r'LogPrintf("TRACE: 7. Before WriteKey\\n");\n        \1')
]

for i, (pattern, repl) in enumerate(traces):
    new_content = re.sub(pattern, repl, content)
    if new_content == content:
        print("Внимание: Не удалось внедрить лог TRACE: " + str(i+1))
    content = new_content

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Трассировочные логи успешно внедрены.")
