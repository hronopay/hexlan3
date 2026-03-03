import os

def patch_file(path, replacements):
    if not os.path.exists(path):
        print("Ошибка: файл не найден -> " + path)
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print("Внимание: блок не найден в " + path)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Файл " + path + " успешно обновлен.")

# 1. Правка окна пароля (askpassphrasedialog.cpp)
patch_file("src/qt/askpassphrasedialog.cpp", [
    ('ui->stakingCheckBox->setText(tr("For staking only"));', 
     'ui->stakingCheckBox->setText(tr("<b>For staking only</b><br/><small>(Снимите галочку, если хотите разблокировать кошелек полностью для любых операций)</small>"));')
])

# 2. Правка заголовка (bitcoingui.h)
patch_file("src/qt/bitcoingui.h", [
    ('QAction *optionsAction;', 'QAction *optionsAction;\n    QAction *showMnemonicAction;'),
    ('void optionsClicked();', 'void optionsClicked();\n    void showMnemonicClicked();')
])

# 3. Правка реализации (bitcoingui.cpp)
mnemonic_slot_code = """
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

patch_file("src/qt/bitcoingui.cpp", [
    ('optionsAction = new QAction(QIcon(":/icons/options"), tr("&Options..."), this);',
     'optionsAction = new QAction(QIcon(":/icons/options"), tr("&Options..."), this);\n    showMnemonicAction = new QAction(QIcon(":/icons/key"), tr("&Show Mnemonic..."), this);'),
    
    ('settingsMenu->addAction(optionsAction);',
     'settingsMenu->addAction(optionsAction);\n    settingsMenu->addAction(showMnemonicAction);'),
    
    ('connect(optionsAction, SIGNAL(triggered()), this, SLOT(optionsClicked()));',
     'connect(optionsAction, SIGNAL(triggered()), this, SLOT(optionsClicked()));\n    connect(showMnemonicAction, SIGNAL(triggered()), this, SLOT(showMnemonicClicked()));'),
    
    ('void BitcoinGUI::optionsClicked()', mnemonic_slot_code + '\nvoid BitcoinGUI::optionsClicked()')
])
