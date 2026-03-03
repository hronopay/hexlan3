import os
import re

file_path = "src/qt/bitcoingui.cpp"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Ищем добавление в меню Settings. Используем регулярное выражение для гибкости.
pattern_menu = r'(settingsMenu\s*->\s*addAction\s*\(\s*optionsAction\s*\)\s*;)'
if re.search(pattern_menu, content):
    content = re.sub(pattern_menu, r'settingsMenu->addAction(showMnemonicAction);\n    \1', content)
    print("Вставка в меню Settings выполнена.")
else:
    print("ОШИБКА: Не удалось найти settingsMenu->addAction(optionsAction)")

# 2. Реализация функции (слота)
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

# Проверяем, не добавили ли мы её уже случайно
if "void BitcoinGUI::showMnemonicClicked()" not in content:
    content += mnemonic_slot_impl
    print("Реализация слота добавлена в конец файла.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
