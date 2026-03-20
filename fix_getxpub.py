import os

fpath = "src/rpcwallet.cpp"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

old_code = "if (!pwalletMain->cachedMasterKey.IsValid())"
new_code = "if (pwalletMain->strMnemonic.empty())"

if old_code in code:
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code.replace(old_code, new_code))
    print("Success! Fixed the validation check in getxpub.")
else:
    print("Error: Could not find the target code to replace.")
