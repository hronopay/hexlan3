import os

def extract_func(filepath, func_name):
    if not os.path.exists(filepath):
        print(filepath + " not found.")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    idx = code.find(func_name)
    if idx == -1:
        print(func_name + " not found in " + filepath)
        return
    start = code.rfind("\n", 0, idx)
    brace = code.find("{", idx)
    if brace == -1: return
    braces = 1
    curr = brace + 1
    while curr < len(code) and braces > 0:
        if code[curr] == '{': braces += 1
        elif code[curr] == '}': braces -= 1
        curr += 1
    print("=== " + filepath + " : " + func_name + " ===")
    print(code[start:curr].strip())
    print("\n")

extract_func("src/qt/overviewpage.cpp", "OverviewPage::setBalance")
extract_func("src/qt/walletmodel.cpp", "WalletModel::pollBalanceChanged")
