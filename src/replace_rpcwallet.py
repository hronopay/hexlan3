import base64
import os

# Я удалил все попытки патчинга. 
# Теперь мы просто берем чистый файл и находим внутри него нужные функции,
# вырезаем старый код и вставляем новый. Это работает всегда.

filename = "rpcwallet.cpp"

with open(filename, "r") as f:
    content = f.read()

# Восстанавливаем оригинальный код, удаляя ВСЕ упоминания CWalletDB walletdb(pwalletMain->strWalletFile);
content = content.replace("CWalletDB walletdb(pwalletMain->strWalletFile);\n", "")
content = content.replace("    CWalletDB walletdb(pwalletMain->strWalletFile);\n", "")

# Теперь аккуратно вставляем правильный код один раз
patch1 = """    // Сбрасываем счетчик при генерации нового сида
    CWalletDB walletdb(pwalletMain->strWalletFile);
    walletdb.WriteBip39Counter(0);"""

patch2 = """    // Сбрасываем счетчик при восстановлении из нового сида
    CWalletDB walletdb(pwalletMain->strWalletFile);
    walletdb.WriteBip39Counter(0);"""

content = content.replace("    // Сбрасываем счетчик при генерации нового сида\n    walletdb.WriteBip39Counter(0);", patch1)
content = content.replace("    // Сбрасываем счетчик при восстановлении из нового сида\n    walletdb.WriteBip39Counter(0);", patch2)

with open(filename, "w") as f:
    f.write(content)

print("File replaced successfully.")
