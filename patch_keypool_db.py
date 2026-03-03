import re
import os

file_path = "src/wallet.cpp"

if not os.path.exists(file_path):
    print("Ошибка: файл " + file_path + " не найден.")
    exit()

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Открытие транзакции перед началом цикла
pattern_while = r'(while\s*\(\s*setKeyPool\.size\(\)\s*<\s*\(nTargetSize\s*\+\s*1\)\s*\)\s*\{)'
if re.search(pattern_while, content) and "walletdb.TxnBegin();" not in content:
    content = re.sub(pattern_while, r'walletdb.TxnBegin();\n        \1', content)

# 2. Обработка ошибки: отмена транзакции
pattern_error = r'(if\s*\(\!walletdb\.WritePool\(nEnd,\s*CKeyPool\(GenerateNewKey\(\)\)\)\)\s*)(throw\s+runtime_error\("TopUpKeyPool\(\)\s*:\s*writing\s+generated\s+key\s+failed"\);)'
if re.search(pattern_error, content):
    content = re.sub(pattern_error, r'\1 {\n                walletdb.TxnAbort();\n                \2\n            }', content)

# 3. Закрытие и запись транзакции после цикла
pattern_end = r'(uiInterface\.InitMessage\(strMsg\);\s*\n\s*\})'
if re.search(pattern_end, content) and "walletdb.TxnCommit();" not in content:
    content = re.sub(pattern_end, r'\1\n        walletdb.TxnCommit();', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Групповая транзакция БД успешно внедрена в CWallet::TopUpKeyPool.")
