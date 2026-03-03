import re

file_path = "src/wallet.h"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем объявление функции игнорируя точное количество пробелов
pattern = r'(bool\s+AddKeyPubKey\s*\([^)]+\)\s*;)'

if re.search(pattern, content) and "AddKeyPubKeyWithDB" not in content:
    content = re.sub(pattern, r'\1\n    bool AddKeyPubKeyWithDB(const CKey& secret, const CPubKey &pubkey, CWalletDB* pwalletdb);', content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Успешно: AddKeyPubKeyWithDB добавлена в wallet.h!")
elif "AddKeyPubKeyWithDB" in content:
    print("Функция уже была добавлена ранее.")
else:
    print("ОШИБКА: Не удалось найти AddKeyPubKey в wallet.h")
