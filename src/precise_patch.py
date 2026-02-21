import os

filename = "rpcwallet.cpp"

with open(filename, "r") as f:
    content = f.read()

# Ищем ровно тот блок кода, где нарушен порядок
bad_code = "    walletdb.WriteBip39Counter(0);\n    CWalletDB walletdb(pwalletMain->strWalletFile);"
good_code = "    CWalletDB walletdb(pwalletMain->strWalletFile);\n    walletdb.WriteBip39Counter(0);"

if bad_code in content:
    content = content.replace(bad_code, good_code)
    with open(filename, "w") as f:
        f.write(content)
    print("Perfect patch applied.")
else:
    print("Error: Target code not found.")
