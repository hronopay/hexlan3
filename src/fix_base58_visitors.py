with open("base58.cpp", "r") as f:
    lines = f.readlines()

out = []
patched = False
for line in lines:
    out.append(line)
    if "bool operator()(const CStealthAddress" in line and "return false;" in line:
        out.append("        bool operator()(const WitnessV0KeyHash &id) const { return false; }\n")
        out.append("        bool operator()(const WitnessV0ScriptHash &id) const { return false; }\n")
        patched = True

if patched:
    with open("base58.cpp", "w") as f:
        f.writelines(out)
    print("Success: base58.cpp visitors patched to correctly reject SegWit as Base58.")
else:
    print("Notice: Could not find visitor signatures, or already patched.")
