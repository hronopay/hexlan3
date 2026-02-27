// Copyright (c) 2026 Hexlan Developers
// Distributed under the MIT software license

#ifndef HEXLAN_QT_BIP39DIALOG_H
#define HEXLAN_QT_BIP39DIALOG_H

#include <QDialog>
#include <QString>

class QTextEdit;
class QLineEdit;
class QPushButton;
class QLabel;

class Bip39Dialog : public QDialog
{
    Q_OBJECT

public:
    enum Mode { GENERATE, RECOVER };
    explicit Bip39Dialog(Mode mode, QWidget *parent = 0);
    ~Bip39Dialog();

    QString getMnemonic() const;
    QString getPassphrase() const;

private slots:
    void onOkClicked();
    void onCancelClicked();

private:
    Mode dialogMode;
    QTextEdit* textEditMnemonic;
    QLineEdit* lineEditPassphrase;
    QPushButton* btnOk;
    QPushButton* btnCancel;
    QString mnemonicStr;
};

#endif // HEXLAN_QT_BIP39DIALOG_H
