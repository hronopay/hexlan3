import os

with open("script.h", "r") as f:
    content = f.read()

old_dest = "typedef boost::variant<CNoDestination, CKeyID, CScriptID, CStealthAddress> CTxDestination;"

new_dest = """// Hexlan SegWit Data Structures
struct WitnessV0KeyHash : public uint160 {
    WitnessV0KeyHash() : uint160() {}
    explicit WitnessV0KeyHash(const uint160& hash) : uint160(hash) {}
    WitnessV0KeyHash(const CKeyID& id) : uint160(id) {}
};

struct WitnessV0ScriptHash : public uint256 {
    WitnessV0ScriptHash() : uint256() {}
    explicit WitnessV0ScriptHash(const uint256& hash) : uint256(hash) {}
};

typedef boost::variant<CNoDestination, CKeyID, CScriptID, CStealthAddress, WitnessV0KeyHash, WitnessV0ScriptHash> CTxDestination;"""

if old_dest in content:
    content = content.replace(old_dest, new_dest)
    with open("script.h", "w") as f:
        f.write(content)
    print("Success: script.h patched with WitnessV0KeyHash and WitnessV0ScriptHash.")
else:
    print("Notice: CTxDestination string not found exactly as expected. Checking if already patched...")
    if "WitnessV0KeyHash" in content:
        print("Already patched.")
