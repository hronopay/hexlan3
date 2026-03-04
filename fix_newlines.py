import os

file_path = "src/wallet.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Чиним разорванные кавычки в логах
content = content.replace('advancing...\n",', 'advancing...\\n",')
content = content.replace('trying next...\n",', 'trying next...\\n",')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Успешно: Кавычки зашиты, синтаксис С++ восстановлен!")
