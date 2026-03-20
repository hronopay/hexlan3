import os

# 1. ИСПРАВЛЕНИЕ ОШИБКИ ЛИНКОВЩИКА В RPCWALLET.CPP
f_rpc = "src/rpcwallet.cpp"
with open(f_rpc, "r", encoding="utf-8") as f:
    code_rpc = f.read()

old_base58 = "if (!DecodeBase58Check(strXpub, vchTemp) || vchTemp.size() != 78)"
new_base58 = "if (!DecodeBase58Check(strXpub.c_str(), vchTemp) || vchTemp.size() != 78)"
code_rpc = code_rpc.replace(old_base58, new_base58)

with open(f_rpc, "w", encoding="utf-8") as f:
    f.write(code_rpc)

# 2. ОБНОВЛЕНИЕ ЗАГОЛОВОЧНОГО ФАЙЛА GUI
f_h = "src/qt/bitcoingui.h"
with open(f_h, "r", encoding="utf-8") as f:
    code_h = f.read()

if "QAction *importXpubAction;" not in code_h:
    code_h = code_h.replace("QAction *showBackupsAction;", "QAction *showBackupsAction;\n    QAction *importXpubAction;")
    code_h = code_h.replace("void optionsClicked();", "void optionsClicked();\n    void importXpubClicked();")
    with open(f_h, "w", encoding="utf-8") as f:
        f.write(code_h)

# 3. ВНЕДРЕНИЕ 3-КНОПОЧНОГО МЕНЮ И ДИАЛОГА ИМПОРТА
f_cpp = "src/qt/bitcoingui.cpp"
with open(f_cpp, "r", encoding="utf-8") as f:
    code_cpp = f.read()

# Добавляем нужные инклуды
if "#include <QInputDialog>" not in code_cpp:
    code_cpp = code_cpp.replace(
        '#include <QMessageBox>',
        '#include <QMessageBox>\n#include <QInputDialog>\n#include "rpcserver.h"'
    )

# Создаем действие (Action)
if "importXpubAction = new QAction" not in code_cpp:
    code_cpp = code_cpp.replace(
        'verifyMessageAction = new QAction(QIcon(":/icons/transaction_0"), tr("&Verify message..."), this);',
        'verifyMessageAction = new QAction(QIcon(":/icons/transaction_0"), tr("&Verify message..."), this);\n    importXpubAction = new QAction(QIcon(":/icons/add"), tr("Import Watch-Only &xpub..."), this);\n    importXpubAction->setToolTip(tr("Import a BIP32 Extended Public Key for cold storage"));'
    )
    code_cpp = code_cpp.replace(
        'connect(verifyMessageAction, SIGNAL(triggered()), this, SLOT(gotoVerifyMessageTab()));',
        'connect(verifyMessageAction, SIGNAL(triggered()), this, SLOT(gotoVerifyMessageTab()));\n    connect(importXpubAction, SIGNAL(triggered()), this, SLOT(importXpubClicked()));'
    )

# Добавляем в меню File
if "file->addAction(importXpubAction);" not in code_cpp:
    code_cpp = code_cpp.replace(
        'file->addAction(quitAction);',
        'file->addAction(importXpubAction);\n    file->addSeparator();\n    file->addAction(quitAction);'
    )

# Заменяем блок инициализации (Стартовое меню)
idx_start = code_cpp.find("// --- HEXLAN BIP39 GUI INTERCEPT ---")
idx_end = code_cpp.find("// ----------------------------------", idx_start)
if idx_start != -1 and idx_end != -1:
    new_intercept = """// --- HEXLAN BIP39 GUI INTERCEPT ---
        if (pwalletMain && pwalletMain->strMnemonic.empty() && !pwalletMain->HaveWatchOnly()) {
            QMessageBox msgBox(this);
            msgBox.setWindowTitle(tr("Wallet Initialization"));
            msgBox.setText(tr("No HD seed found. Please choose how to initialize your wallet:"));
            
            QPushButton *genBtn = msgBox.addButton(tr("Generate Seed"), QMessageBox::ActionRole);
            QPushButton *resBtn = msgBox.addButton(tr("Restore from Seed"), QMessageBox::ActionRole);
            QPushButton *watchBtn = msgBox.addButton(tr("Watch-Only Wallet (Empty)"), QMessageBox::ActionRole);
            
            msgBox.exec();

            if (msgBox.clickedButton() == genBtn || msgBox.clickedButton() == resBtn) {
                Bip39Dialog::Mode mode = (msgBox.clickedButton() == genBtn) ? Bip39Dialog::GENERATE : Bip39Dialog::RECOVER;
                Bip39Dialog bip39Dlg(mode, this);

                if (bip39Dlg.exec() == QDialog::Accepted) {
                    std::string mnemonic = bip39Dlg.getMnemonic().toStdString();
                    std::string passphrase = bip39Dlg.getPassphrase().toStdString();

                    pwalletMain->strMnemonic = mnemonic.c_str();
                    pwalletMain->strMnemonicPassphrase = passphrase.c_str();
                    pwalletMain->nBip39Counter = 0;

                    {
                        CWalletDB walletdb(pwalletMain->strWalletFile);
                        walletdb.WriteMnemonic(mnemonic);
                        walletdb.WriteMnemonicPassphrase(passphrase);
                        walletdb.WriteBip39Counter(0);
                        
                        for (std::map<CTxDestination, std::string>::iterator it = pwalletMain->mapAddressBook.begin(); it != pwalletMain->mapAddressBook.end(); ++it) {
                            walletdb.EraseName(CHexlanAddress(it->first).ToString());
                            pwalletMain->NotifyAddressBookChanged(pwalletMain, it->first, it->second, ::IsMine(*pwalletMain, it->first) != ISMINE_NO, CT_DELETED);
                        }
                    } 
                    
                    pwalletMain->mapAddressBook.clear();
                    pwalletMain->setKeyPool.clear();
                    pwalletMain->TopUpKeyPool();
                } else {
                    QMessageBox::critical(this, tr("Initialization Failed"), tr("Initialization cancelled. The application will now exit."));
                    exit(0);
                }
            } else if (msgBox.clickedButton() == watchBtn) {
                QMessageBox::information(this, tr("Watch-Only Mode"), tr("Wallet started in Watch-Only mode.\\nUse 'File -> Import Watch-Only xpub...' to add your extended public key."));
            } else {
                exit(0);
            }
        }
        // ----------------------------------"""
    code_cpp = code_cpp[:idx_start] + new_intercept + code_cpp[idx_end + len("// ----------------------------------"):]

# Добавляем функцию импорта в конец файла
if "void BitcoinGUI::importXpubClicked()" not in code_cpp:
    code_cpp += """\n
void BitcoinGUI::importXpubClicked()
{
    bool ok;
    QString xpub = QInputDialog::getText(this, tr("Import Watch-Only xpub"),
                                         tr("Enter your BIP32 Extended Public Key (xpub...):"), QLineEdit::Normal,
                                         "", &ok);
    if (ok && !xpub.isEmpty()) {
        QProgressDialog progress(tr("Importing addresses and scanning blockchain...\\nThis may take a few minutes."), tr("Cancel"), 0, 0, this);
        progress.setWindowModality(Qt::WindowModal);
        progress.show();
        QApplication::processEvents();

        try {
            json_spirit::Array params;
            params.push_back(xpub.toStdString());
            params.push_back(100); 
            params.push_back(true); 
            
            json_spirit::Value result = importxpub(params, false);
            progress.close();
            QMessageBox::information(this, tr("Success"), tr("xpub imported successfully! Check your Dashboard for balances."));
        } catch (std::exception& e) {
            progress.close();
            QMessageBox::critical(this, tr("Error"), tr("Failed to import xpub:\\n") + QString::fromStdString(e.what()));
        }
    }
}
"""

with open(f_cpp, "w", encoding="utf-8") as f:
    f.write(code_cpp)

print("Master patch applied: GUI and Linker fixes are ready!")
