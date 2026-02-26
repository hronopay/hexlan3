import os

with open("wallet.cpp", "r") as f:
    content = f.read()

old_path = "masterKey.Derive(purposeKey, 44 | 0x80000000);"
new_path = "masterKey.Derive(purposeKey, 84 | 0x80000000); // BIP84 Native SegWit"

if old_path in content:
    content = content.replace(old_path, new_path)
    with open("wallet.cpp", "w") as f:
        f.write(content)
    print("Success: Derivation path updated to BIP84 in wallet.cpp")
else:
    print("Notice: Path already updated or not found.")
