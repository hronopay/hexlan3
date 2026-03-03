import re
import os

def patch_wallet_h():
    path = "src/wallet.h"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "GenerateNewKeyWithDB" not in content:
        content = re.sub(r'(CPubKey\s+GenerateNewKey\(\)\s*;)', r'\1\n    CPubKey GenerateNewKeyWithDB(CWalletDB* pwalletdb);', content)
        content = re.sub(r'(bool\s+AddKeyPubKey\(const\s+CKey&\s+secret,\s+const\s+CPubKey\s+&pubkey\)\s*;)', r'\1\n    bool AddKeyPubKeyWithDB(const CKey& secret, const CPubKey &pubkey, CWalletDB* pwalletdb);', content)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Успешно: wallet.h обновлен (добавлены перегруженные функции).")

def patch_wallet_cpp():
    path = "src/wallet.cpp"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "GenerateNewKeyWithDB" not in content:
        # 1. Меняем сигнатуры основных функций
        content = content.replace("CPubKey CWallet::GenerateNewKey()\n{", "CPubKey CWallet::GenerateNewKeyWithDB(CWalletDB* pwalletdb)\n{")
        content = content.replace("bool CWallet::AddKeyPubKey(const CKey& secret, const CPubKey &pubkey)\n{", "bool CWallet::AddKeyPubKeyWithDB(const CKey& secret, const CPubKey &pubkey, CWalletDB* pwalletdb)\n{")

        # 2. Прокидываем pwalletdb вместо создания новых подключений к БД
        content = content.replace("CWalletDB(strWalletFile).WriteBip39Counter(nBip39Counter);", "if (pwalletdb) pwalletdb->WriteBip39Counter(nBip39Counter);\n    else CWalletDB(strWalletFile).WriteBip39Counter(nBip39Counter);")
        content = content.replace("if (!AddKeyPubKey(secret, pubkey))", "if (!AddKeyPubKeyWithDB(secret, pubkey, pwalletdb))")

        # 3. Безопасная замена WriteKey
        pattern_writekey = r'return\s+CWalletDB\(strWalletFile\)\.WriteKey\(([^)]+)\);'
        replacement_writekey = r'if (pwalletdb) return pwalletdb->WriteKey(\1);\n        else return CWalletDB(strWalletFile).WriteKey(\1);'
        content = re.sub(pattern_writekey, replacement_writekey, content)

        # 4. Внедряем единую транзакцию в TopUpKeyPool
        content = content.replace("CKeyPool(GenerateNewKey())", "CKeyPool(GenerateNewKeyWithDB(&walletdb))")

        # 5. Добавляем обертки для обратной совместимости в конец файла
        wrappers = """
CPubKey CWallet::GenerateNewKey()
{
    return GenerateNewKeyWithDB(NULL);
}

bool CWallet::AddKeyPubKey(const CKey& secret, const CPubKey &pubkey)
{
    return AddKeyPubKeyWithDB(secret, pubkey, NULL);
}
"""
        content += wrappers

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Успешно: wallet.cpp обновлен (устранено дублирование дисковых операций).")

patch_wallet_h()
patch_wallet_cpp()
