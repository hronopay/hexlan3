import os

f_rpc = "src/rpcwallet.cpp"
with open(f_rpc, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Находим место в bip39recover, где записываются данные
# Мы добавим сброс времени и команду на сканирование блоков

old_logic = """    pwalletMain->setKeyPool.clear(); // Сброс случайных ключей
    pwalletMain->TopUpKeyPool();     // Генерация HD-пула"""

new_logic = """    pwalletMain->setKeyPool.clear(); // Сброс случайных ключей
    
    // HEXLAN: Устанавливаем дату рождения кошелька в 1 (Genesis), 
    // чтобы при рескане кошелек не игнорировал старые блоки.
    pwalletMain->nTimeFirstKey = 1; 

    pwalletMain->TopUpKeyPool();     // Генерация HD-пула

    // HEXLAN: Автоматический запуск сканирования блокчейна
    pwalletMain->ScanForWalletTransactions(pindexGenesisBlock, true);
    pwalletMain->ReacceptWalletTransactions();"""

if old_logic in code:
    code = code.replace(old_logic, new_logic)
    with open(f_rpc, "w", encoding="utf-8") as f:
        f.write(code)
    print("Success! bip39recover now performs auto-rescan from Genesis.")
else:
    print("Error: Could not find the logic in rpcwallet.cpp. Check the file content.")
