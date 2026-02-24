import re

with open("wallet.cpp", "r") as f:
    content = f.read()

# Ищем стандартную логику установки размера пула
match = re.search(r'(nTargetSize\s*=\s*max\(GetArg\("-keypool",\s*\d+\),\s*\(int64_t\)\s*0\);)', content)

if match:
    original_line = match.group(1)
    # Добавляем наше условие
    new_line = original_line + "\n\n    // Hexlan: Если кошелек еще не инициализирован HD-фразой, генерируем только 1 резервный ключ\n    if (strMnemonic.empty())\n        nTargetSize = 1;"
    
    content = content.replace(original_line, new_line)
    
    with open("wallet.cpp", "w") as f:
        f.write(content)
    print("Success: TopUpKeyPool patched to generate only 1 random key before initialization.")
else:
    print("Error: Could not find TopUpKeyPool size logic.")
