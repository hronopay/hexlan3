import re
import os

# 1. Лечим segwit_addr.cpp (привязываем к chainparams)
file_segwit = "src/segwit_addr.cpp"
with open(file_segwit, "r", encoding="utf-8") as f:
    content = f.read()

if '#include "chainparams.h"' not in content:
    content = content.replace('#include "bech32.h"', '#include "bech32.h"\n#include "chainparams.h"')

# Удаляем жесткую константу и заменяем вызовы
content = re.sub(r'const std::string SEGWIT_HRP = "[^"]+";\n?', '', content)
content = content.replace('SEGWIT_HRP', 'Params().Bech32HRP()')

with open(file_segwit, "w", encoding="utf-8") as f:
    f.write(content)
print("Успешно: segwit_addr.cpp теперь использует Params().Bech32HRP()")

# 2. Лечим GUI валидатор в walletmodel.cpp
file_walletmodel = "src/qt/walletmodel.cpp"
if os.path.exists(file_walletmodel):
    with open(file_walletmodel, "r", encoding="utf-8") as f:
        content = f.read()

    if '#include "segwit_addr.h"' not in content:
        content = content.replace('#include "wallet.h"', '#include "wallet.h"\n#include "segwit_addr.h"')

    # Находим функцию validateAddress и заменяем ее тело на универсальную проверку
    pattern = r'(bool\s+WalletModel::validateAddress\(\s*const\s+QString\s*&\s*address\s*\)\s*\{)(.*?)(\n\})'
    
    def replacer(match):
        return match.group(1) + "\n    return IsValidDestinationString(address.toStdString());" + match.group(3)
        
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)

    with open(file_walletmodel, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Успешно: WalletModel::validateAddress обновлен для поддержки Bech32")
else:
    print("Внимание: Файл walletmodel.cpp не найден.")

