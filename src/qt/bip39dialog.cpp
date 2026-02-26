// Copyright (c) 2026 Hexlan Developers
// Distributed under the MIT software license

#include "bip39dialog.h"
#include "../bip39.h"

#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QTextEdit>
#include <QPushButton>
#include <QMessageBox>

Bip39Dialog::Bip39Dialog(Mode mode, QWidget *parent) :
    QDialog(parent), dialogMode(mode)
{
    setWindowTitle(mode == GENERATE ? tr("Create HD Wallet") : tr("Recover HD Wallet"));
    setMinimumSize(450, 250);

    QVBoxLayout* mainLayout = new QVBoxLayout(this);

    QLabel* labelExplanation = new QLabel(this);
    labelExplanation->setWordWrap(true);
    
    QFont fontExplanation = labelExplanation->font();
    fontExplanation.setPointSize(10);
    labelExplanation->setFont(fontExplanation);
    mainLayout->addWidget(labelExplanation);

    textEditMnemonic = new QTextEdit(this);
    textEditMnemonic->setAcceptRichText(false);
    QFont font = textEditMnemonic->font();
    font.setPointSize(12);
    font.setBold(true);
    textEditMnemonic->setFont(font);
    mainLayout->addWidget(textEditMnemonic);

    QHBoxLayout* buttonLayout = new QHBoxLayout();
    btnOk = new QPushButton(tr("OK"), this);
    btnCancel = new QPushButton(tr("Cancel"), this);
    buttonLayout->addStretch();
    buttonLayout->addWidget(btnOk);
    buttonLayout->addWidget(btnCancel);
    mainLayout->addLayout(buttonLayout);

    connect(btnOk, SIGNAL(clicked()), this, SLOT(onOkClicked()));
    connect(btnCancel, SIGNAL(clicked()), this, SLOT(onCancelClicked()));

    if (mode == GENERATE) {
        labelExplanation->setText(tr("Please write down your 12-word mnemonic phrase securely.\n\nThis is the ONLY way to recover your funds if you lose your wallet or password. Do not share it with anyone!"));
        
        // Генерируем 16 байт энтропии (12 слов)
        SecureString mnemonicSec = BIP39::GenerateMnemonic(16);
        mnemonicStr = QString::fromStdString(std::string(mnemonicSec.begin(), mnemonicSec.end()));
        
        textEditMnemonic->setPlainText(mnemonicStr);
        textEditMnemonic->setReadOnly(true);
    } else {
        labelExplanation->setText(tr("Enter your 12-word mnemonic phrase to recover your wallet.\n\nWords should be separated by a single space."));
        textEditMnemonic->setReadOnly(false);
    }
}

Bip39Dialog::~Bip39Dialog()
{
}

QString Bip39Dialog::getMnemonic() const
{
    return mnemonicStr;
}

void Bip39Dialog::onOkClicked()
{
    if (dialogMode == RECOVER) {
        mnemonicStr = textEditMnemonic->toPlainText().trimmed();
        
        // Заменяем множественные пробелы и переносы строк на один пробел
        mnemonicStr.replace(QRegExp("\\s+"), " ");
        
        if (mnemonicStr.isEmpty()) {
            QMessageBox::warning(this, tr("Error"), tr("Mnemonic phrase cannot be empty."));
            return;
        }
        
        SecureString secureMnem(mnemonicStr.toStdString().c_str());
        if (!BIP39::CheckMnemonic(secureMnem)) {
            QMessageBox::warning(this, tr("Error"), tr("Invalid mnemonic phrase. Please check your spelling and ensure you have 12 words."));
            return;
        }
    } else {
        QMessageBox::StandardButton reply;
        reply = QMessageBox::question(this, tr("Confirm"), tr("Have you securely written down your mnemonic phrase? If you lose it, your funds will be lost forever."), QMessageBox::Yes|QMessageBox::No);
        if (reply == QMessageBox::No) {
            return;
        }
    }
    accept();
}

void Bip39Dialog::onCancelClicked()
{
    reject();
}
