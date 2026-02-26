with open("script.cpp", "r") as f:
    content = f.read()

# Патчим сборщик ключей
if "void operator()(const WitnessV0KeyHash" not in content:
    content = content.replace(
        "void operator()(const CStealthAddress &stxAddr) {",
        "void operator()(const WitnessV0KeyHash& keyid) { vKeys.push_back(CKeyID(keyid)); }\n    void operator()(const WitnessV0ScriptHash& scriptid) {}\n    void operator()(const CStealthAddress &stxAddr) {"
    )

# Патчим генератор скриптов
if "bool operator()(const WitnessV0KeyHash" not in content:
    content = content.replace(
        "bool operator()(const CStealthAddress &stxAddr) const {",
        "bool operator()(const WitnessV0KeyHash& id) const {\n        script->clear();\n        *script << OP_0 << std::vector<unsigned char>(id.begin(), id.end());\n        return true;\n    }\n    bool operator()(const WitnessV0ScriptHash& id) const {\n        script->clear();\n        *script << OP_0 << std::vector<unsigned char>(id.begin(), id.end());\n        return true;\n    }\n    bool operator()(const CStealthAddress &stxAddr) const {"
    )

with open("script.cpp", "w") as f:
    f.write(content)

print("Success: script.cpp patched with SegWit OP_0 script generation.")
