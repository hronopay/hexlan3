import os

file_path = "src/script.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """isminetype IsMine(const CKeyStore &keystore, const CScript& scriptPubKey)
{
    vector<valtype> vSolutions;"""

replacement = """isminetype IsMine(const CKeyStore &keystore, const CScript& scriptPubKey)
{
    // Hexlan: SegWit BIP84 recognition for balance
    if (scriptPubKey.size() == 22 && scriptPubKey[0] == OP_0 && scriptPubKey[1] == 0x14) {
        std::vector<unsigned char> hashBytes(scriptPubKey.begin() + 2, scriptPubKey.end());
        if (keystore.HaveKey(CKeyID(uint160(hashBytes)))) {
            return ISMINE_SPENDABLE;
        }
    }

    vector<valtype> vSolutions;"""

if "SegWit BIP84 recognition for balance" not in content and target in content:
    content = content.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Успешно: IsMine обновлен для распознавания балансов SegWit!")
elif "SegWit BIP84 recognition for balance" in content:
    print("Патч уже применен.")
else:
    print("Ошибка: Целевой блок IsMine не найден.")
