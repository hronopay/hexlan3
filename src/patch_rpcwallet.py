import os
import sys

filename = "rpcwallet.cpp"

if not os.path.exists(filename):
    print("Error: {} not found.".format(filename))
    sys.exit(1)

with open(filename, "r") as f:
    lines = f.readlines()

patched = False
for i in range(len(lines)):
    if "walletdb.WriteBip39Counter(0);" in lines[i]:
        if i > 0 and "CWalletDB walletdb" not in lines[i-1] and "CWalletDB walletdb" not in lines[i-2]:
            indent = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
            lines[i] = indent + "CWalletDB walletdb(pwalletMain->strWalletFile);\n" + lines[i]
            patched = True

if patched:
    with open(filename, "w") as f:
        f.writelines(lines)
    print("Success: {} was patched!".format(filename))
else:
    print("Notice: No changes were needed or target strings not found.")
