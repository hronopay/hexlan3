import os

def patch_file(path, replacements):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print("Успешно пропатчен: " + path)
        else:
            print("ОШИБКА: Не найден блок в " + path + " -> " + old[:30])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# Исправляем окно пароля - ищем по переменной чекбокса
patch_file("src/qt/askpassphrasedialog.cpp", [
    ('ui->stakingCheckBox->setChecked(fWalletUnlockStakingOnly);', 
     'ui->stakingCheckBox->setChecked(fWalletUnlockStakingOnly);\n    ui->stakingCheckBox->setText(tr("<b>For staking only</b><br/><small>(Снимите галочку, если хотите разблокировать кошелек полностью)</small>"));')
])

# Исправляем реализацию меню - ищем по началу метода createActions
patch_file("src/qt/bitcoingui.cpp", [
    ('void BitcoinGUI::createActions()', 
     'void BitcoinGUI::createActions()\n{\n    showMnemonicAction = new QAction(QIcon(":/icons/key"), tr("&Show Mnemonic..."), this);'),
    ('settingsMenu->addSeparator();', 
     'settingsMenu->addAction(showMnemonicAction);\n    settingsMenu->addSeparator();'),
    ('connect(quitAction, SIGNAL(triggered()), qApp, SLOT(quit()));',
     'connect(quitAction, SIGNAL(triggered()), qApp, SLOT(quit()));\n    connect(showMnemonicAction, SIGNAL(triggered()), this, SLOT(showMnemonicClicked()));')
])
