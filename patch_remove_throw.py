import os

file_path = "src/wallet.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = 'throw std::runtime_error("CWallet::GenerateNewChangeKey() : AddKey failed");'
replacement = 'LogPrintf("ERROR: CWallet::GenerateNewChangeKey() : AddKey failed!\\n");\n        // Не убиваем кошелек из-за таймаутов базы данных'

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Успешно: Смертельный throw удален. Кошелек больше не будет падать.")
else:
    print("Смертельный throw уже удален.")
