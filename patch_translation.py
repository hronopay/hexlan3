import os

ts_path = "src/qt/locale/bitcoin_ru.ts"
if not os.path.exists(ts_path):
    print("Файл перевода не найден")
    exit()

with open(ts_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    # Добавляем перевод для главного окна
    if '<name>BitcoinGUI</name>' in line:
        new_lines.append('    <message>\n        <source>&amp;Show Mnemonic...</source>\n        <translation>&amp;Показать сид-фразу...</translation>\n    </message>\n')
        new_lines.append('    <message>\n        <source>BIP39 Seed Backup</source>\n        <translation>Бэкап BIP39 Seed</translation>\n    </message>\n')
    
    # Добавляем перевод для окна пароля
    if '<name>AskPassphraseDialog</name>' in line:
        new_lines.append('    <message>\n        <source><b>For staking only</b><br/><small>(Снимите галочку, если хотите разблокировать кошелек полностью)</small></source>\n        <translation><b>Только для стейкинга</b><br/><small>(Снимите галочку, если хотите разблокировать кошелек полностью)</small></translation>\n    </message>\n')

with open(ts_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Файл bitcoin_ru.ts успешно обновлен новыми строками перевода")
