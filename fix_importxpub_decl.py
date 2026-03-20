import os

f_cpp = "src/qt/bitcoingui.cpp"
with open(f_cpp, "r", encoding="utf-8") as f:
    code = f.read()

old_code = '#include "rpcserver.h"'
new_code = '#include "rpcserver.h"\n\nextern json_spirit::Value importxpub(const json_spirit::Array& params, bool fHelp);'

if "extern json_spirit::Value importxpub" not in code:
    code = code.replace(old_code, new_code)
    with open(f_cpp, "w", encoding="utf-8") as f:
        f.write(code)
    print("Success! importxpub is now declared in bitcoingui.cpp.")
else:
    print("Already declared.")
