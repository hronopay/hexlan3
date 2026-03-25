import os

fpath = "src/wallet.h"
if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        found = False
        for i, line in enumerate(lines):
            if "class CWalletTx" in line:
                print("=== CWalletTx structure in " + fpath + " ===")
                for j in range(i, min(len(lines), i + 40)):
                    print(str(j+1) + ": " + lines[j].rstrip())
                found = True
                break
        if not found: print("CWalletTx not found in wallet.h")
