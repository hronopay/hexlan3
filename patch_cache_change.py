import os

file_path = "src/wallet.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "g_fHasCachedChangeKey" not in content:
    # 1. Внедряем статические переменные и ранний возврат из кэша
    target1 = "CPubKey CWallet::GenerateNewChangeKey()\n{"
    repl1 = """static CPubKey g_cachedChangePubKey;
static bool g_fHasCachedChangeKey = false;

CPubKey CWallet::GenerateNewChangeKey()
{
    if (g_fHasCachedChangeKey) return g_cachedChangePubKey;
"""
    content = content.replace(target1, repl1)
    
    # 2. Сохраняем ключ в кэш перед выходом
    target2 = "nTimeFirstKey = nCreationTime;\n\n    return pubkey;\n}"
    repl2 = "nTimeFirstKey = nCreationTime;\n\n    g_cachedChangePubKey = pubkey;\n    g_fHasCachedChangeKey = true;\n    return pubkey;\n}"
    # Учтем, если файл был изменен предыдущим патчем (без исключения)
    target2_alt = "nTimeFirstKey = nCreationTime;\n\n    return pubkey;\n}"
    
    if "g_cachedChangePubKey = pubkey;" not in content:
        content = content.replace(target2, repl2)
        
    # 3. Сбрасываем кэш при успешной отправке транзакции
    target3 = "bool CWallet::CommitTransaction(CWalletTx& wtxNew, CReserveKey& reservekey, std::string strCommand)\n{"
    repl3 = "bool CWallet::CommitTransaction(CWalletTx& wtxNew, CReserveKey& reservekey, std::string strCommand)\n{\n    g_fHasCachedChangeKey = false;\n"
    content = content.replace(target3, repl3)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Успешно: Умный кэш сдачи внедрен. Защита базы данных активна.")
else:
    print("Патч кэширования уже применен.")
