import os

file_path = "src/script.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """bool IsStandard(const CScript& scriptPubKey, txnouttype& whichType)
{
    vector<valtype> vSolutions;"""

replacement = """bool IsStandard(const CScript& scriptPubKey, txnouttype& whichType)
{
    // Hexlan: Зеленый коридор для Native SegWit V0 (P2WPKH и P2WSH)
    if (scriptPubKey.size() == 22 && scriptPubKey[0] == OP_0 && scriptPubKey[1] == 0x14) {
        whichType = TX_PUBKEYHASH; // Маскируем под стандартный для Мемпула
        return true;
    }
    if (scriptPubKey.size() == 34 && scriptPubKey[0] == OP_0 && scriptPubKey[1] == 0x20) {
        whichType = TX_SCRIPTHASH; // Маскируем под стандартный для Мемпула
        return true;
    }

    vector<valtype> vSolutions;"""

if "Native SegWit V0" not in content and target in content:
    content = content.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Успешно: Мемпул (IsStandard) научился пропускать SegWit транзакции!")
elif "Native SegWit V0" in content:
    print("Патч уже применен.")
else:
    print("Ошибка: Целевой блок не найден.")
