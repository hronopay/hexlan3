import os

def find_struct(fpath, struct_name):
    if not os.path.exists(fpath): return
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "class " + struct_name in line or "struct " + struct_name in line:
                print("=== Found " + struct_name + " in " + fpath + " ===")
                for j in range(i, min(len(lines), i + 20)):
                    print(str(j+1) + ": " + lines[j].rstrip())
                break

find_struct("src/main.h", "CTxIn")
find_struct("src/primitives/transaction.h", "CTxIn")
