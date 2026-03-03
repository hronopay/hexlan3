import os

file_path = "src/qt/bitcoingui.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем добавление Options в меню Settings и вставляем Show Mnemonic ПЕРЕД ним
old_line = 'settingsMenu->addAction(optionsAction);'
new_line = 'settingsMenu->addAction(showMnemonicAction);\n    settingsMenu->addAction(optionsAction);'

if old_line in content:
    content = content.replace(old_line, new_line)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Меню Show Mnemonic успешно интегрировано в bitcoingui.cpp")
else:
    print("ОШИБКА: Не удалось найти строку с optionsAction")
