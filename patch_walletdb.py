import os

file_path = "src/walletdb.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Внедряем функцию WriteBip39ChangeCounter
target_write = """bool CWalletDB::WriteBip39Counter(int nCounter)
{
    nWalletDBUpdated++;
    return Write(std::string("bip39counter"), nCounter);
}"""

replacement_write = target_write + """

bool CWalletDB::WriteBip39ChangeCounter(int nCounter)
{
    nWalletDBUpdated++;
    return Write(std::string("bip39changecounter"), nCounter);
}"""

if target_write in content and "WriteBip39ChangeCounter" not in content:
    content = content.replace(target_write, replacement_write)
    print("Успешно: Добавлена функция WriteBip39ChangeCounter.")

# 2. Добавляем чтение в ReadKeyValue
target_read = """        else if (strType == "bip39counter")
        {
            ssValue >> pwallet->nBip39Counter;
        }"""

replacement_read = target_read + """
        else if (strType == "bip39changecounter")
        {
            ssValue >> pwallet->nBip39ChangeCounter;
        }"""

if target_read in content and "bip39changecounter" not in content:
    content = content.replace(target_read, replacement_read)
    print("Успешно: Добавлено чтение bip39changecounter.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

