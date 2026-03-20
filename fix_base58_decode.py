import os

fpath = "src/base58.h"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

old_code = "ret.Decode(&vchData[0], &vchData[Size]);"
new_code = "ret.Decode(&vchData[0]);"

if old_code in code:
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code.replace(old_code, new_code))
    print("Success! Fixed the latent Decode bug in base58.h.")
else:
    print("Error: Could not find the buggy Decode call.")
