import os

file_path = "src/qt/bitcoingui.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Метод 1: Ищем создание меню Settings
target_anchor = 'settingsMenu = menuBar()->addMenu(tr("&Settings"));'
if target_anchor in content:
    # Вставляем нашу кнопку сразу после создания меню
    insertion = '\n    settingsMenu->addAction(showMnemonicAction);'
    content = content.replace(target_anchor, target_anchor + insertion)
    print("Вставка в меню Settings выполнена успешно.")
else:
    # Метод 2 (запасной): Ищем по контексту Options
    print("Якорь меню не найден, пробую запасной метод...")
    target_backup = 'settingsMenu->addAction(optionsAction);'
    if target_backup in content:
        content = content.replace(target_backup, 'settingsMenu->addAction(showMnemonicAction);\n    ' + target_backup)
        print("Вставка через запасной метод выполнена.")
    else:
        print("КРИТИЧЕСКАЯ ОШИБКА: Не удалось найти место для вставки в bitcoingui.cpp")

# Реализация функции (слота) в самый конец файла
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

if "void BitcoinGUI::showMnemonicClicked()" not in content:
    content += mnemonic_slot_impl
    print("Реализация слота добавлена.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
