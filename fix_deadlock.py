import os

file_path = "src/wallet.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Комментируем вызов интерфейса внутри цикла TopUpKeyPool
target = "uiInterface.InitMessage(strMsg);"
replacement = "// uiInterface.InitMessage(strMsg); // Отключено для предотвращения Deadlock"

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Успешно: Источник Deadlock обезврежен.")
else:
    print("Ошибка: Строка uiInterface.InitMessage(strMsg); не найдена.")
