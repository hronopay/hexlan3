with open("rpcmisc.cpp", "r") as f:
    lines = f.readlines()

out = []
in_visitor = False
patched = False

for line in lines:
    if "DescribeAddressVisitor" in line and ("class" in line or "struct" in line):
        in_visitor = True
    
    if in_visitor and line.strip().startswith("};"):
        out.append("""
    Object operator()(const WitnessV0KeyHash& id) const {
        Object obj;
        obj.push_back(Pair("isscript", false));
        obj.push_back(Pair("iswitness", true));
        obj.push_back(Pair("witness_version", 0));
        obj.push_back(Pair("witness_program", HexStr(id.begin(), id.end())));
        return obj;
    }

    Object operator()(const WitnessV0ScriptHash& id) const {
        Object obj;
        obj.push_back(Pair("isscript", true));
        obj.push_back(Pair("iswitness", true));
        obj.push_back(Pair("witness_version", 0));
        obj.push_back(Pair("witness_program", HexStr(id.begin(), id.end())));
        return obj;
    }
""")
        in_visitor = False
        patched = True
    out.append(line)

if patched:
    with open("rpcmisc.cpp", "w") as f:
        f.writelines(out)
    print("Success: rpcmisc.cpp patched with SegWit visitors.")
else:
    print("Notice: Could not find DescribeAddressVisitor or already patched.")
