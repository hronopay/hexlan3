import os

f_gui = "src/qt/bitcoingui.cpp"
with open(f_gui, "r", encoding="utf-8") as f:
    code = f.read()

# Добавляем рескан в блок обработки Bip39Dialog
old_gui_logic = """                    pwalletMain->setKeyPool.clear();
                    pwalletMain->TopUpKeyPool();"""

new_gui_logic = """                    pwalletMain->setKeyPool.clear();
                    pwalletMain->nTimeFirstKey = 1; // HEXLAN: Сброс даты для поиска истории
                    pwalletMain->TopUpKeyPool();
                    
                    // HEXLAN: Запуск рескана из GUI
                    pwalletMain->ScanForWalletTransactions(pindexGenesisBlock, true);
                    pwalletMain->ReacceptWalletTransactions();"""

if old_gui_logic in code:
    code = code.replace(old_gui_logic, new_gui_logic)
    with open(f_gui, "w", encoding="utf-8") as f:
        f.write(code)
    print("Success! GUI seed recovery now performs auto-rescan.")
else:
    print("Error: Could not find the GUI logic in bitcoingui.cpp.")
