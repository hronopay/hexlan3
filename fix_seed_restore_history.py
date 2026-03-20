import os

f_rpc = "src/rpcwallet.cpp"
with open(f_rpc, "r", encoding="utf-8") as f:
    code = f.read()

# Ищем функцию bip39recover
old_line = '    pwalletMain->nBip39Counter = 0;'
new_line = '    pwalletMain->nBip39Counter = 0;\n    pwalletMain->nTimeFirstKey = 1; // HEXLAN: Заставляем сканировать всю историю с Genesis'

if old_line in code and 'nTimeFirstKey = 1' not in code:
    code = code.replace(old_line, new_line)
    with open(f_rpc, "w", encoding="utf-8") as f:
        f.write(code)
    print("Success! Seed recovery will now track full history.")
else:
    print("Already patched or line not found.")
