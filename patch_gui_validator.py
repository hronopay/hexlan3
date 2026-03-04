import os

file_path = "src/qt/bitcoinaddressvalidator.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """        if(((ch >= '0' && ch<='9') ||
           (ch >= 'a' && ch<='z') ||
           (ch >= 'A' && ch<='Z')) &&
           ch != 'l' && ch != 'I' && ch != '0' && ch != 'O')"""

replacement = """        // Hexlan: разрешаем все алфавитно-цифровые символы, 
        // так как Bech32 использует '0', а Base58 не использует.
        // Окончательная проверка валидности адреса произойдет позже.
        if ((ch >= '0' && ch <= '9') ||
            (ch >= 'a' && ch <= 'z') ||
            (ch >= 'A' && ch <= 'Z'))"""

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Успешно: GUI Валидатор ввода обновлен для поддержки Bech32.")
else:
    print("Ошибка: Целевой блок не найден.")
