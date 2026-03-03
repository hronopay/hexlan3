import os

file_path = "src/qt/bitcoingui.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Исправляем createMenuBar: вставляем Show Mnemonic перед Options в меню Settings
# В вашем файле это строка 469
old_menu_line = 'settingsMenu->addAction(optionsAction);'
new_menu_line = 'settingsMenu->addAction(showMnemonicAction);\n    settingsMenu->addAction(optionsAction);'

# 2. Исправляем создание слота: вставляем реализацию функции в конец файла перед последней скобкой или после существующего слота
mnemonic_slot_impl = """
void BitcoinGUI::showMnemonicClicked()
{
    if(!walletModel)
        return;

    if(walletModel->getEncryptionStatus() == WalletModel::Locked)
    {
        AskPassphraseDialog dlg(AskPassphraseDialog::Unlock, this);
        dlg.setModel(walletModel);
        if(dlg.exec() != QDialog::Accepted)
            return;
    }

    QString mnemonic = QString::fromStdString(pwalletMain->strMnemonic.c_str());
    QString passphrase = QString::fromStdString(pwalletMain->strMnemonicPassphrase.c_str());

    if(mnemonic.isEmpty())
    {
        QMessageBox::critical(this, tr("Error"), tr("Mnemonic not found in this wallet."));
        return;
    }

    QString message = tr("<b>Mnemonic Phrase:</b><br/><p>%1</p><br/><b>Passphrase:</b><br/>%2")
                        .arg(mnemonic).arg(passphrase.isEmpty() ? "<i>none</i>" : passphrase);

    QMessageBox::information(this, tr("BIP39 Seed Backup"), message);
}
"""

if old_menu_line in content:
    content = content.replace(old_menu_line, new_menu_line)
    # Добавляем реализацию слота в конец файла (перед закрывающим namespace или просто в конец)
    content += mnemonic_slot_impl
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Интерфейс bitcoingui.cpp успешно исправлен.")
else:
    print("ОШИБКА: Не удалось найти точку входа в bitcoingui.cpp")
