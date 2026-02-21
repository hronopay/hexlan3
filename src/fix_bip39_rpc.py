import sys

filename = "rpcwallet.cpp"

with open(filename, "r") as f:
    lines = f.readlines()

patched = 0
in_target = False

for i in range(len(lines)):
    if "bip39generate(" in lines[i] or "bip39recover(" in lines[i]:
        in_target = True
    
    if in_target and "walletdb.WriteBip39Counter(0);" in lines[i]:
        indent = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
        lines[i] = indent + "CWalletDB walletdb(pwalletMain->strWalletFile);\n" + lines[i]
        patched += 1
        in_target = False

if patched == 2:
    with open(filename, "w") as f:
        f.writelines(lines)
    print("Success: rpcwallet.cpp patched perfectly.")
else:
    print("Error: Patched {} instead of 2 targets.".format(patched))
