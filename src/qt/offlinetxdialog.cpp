
#include "offlinetxdialog.h"
#include <QVBoxLayout>
#include <QTextEdit>
#include <QPushButton>
#include <QApplication>
#include <QClipboard>
#include <QFileDialog>
#include <QMessageBox>

OfflineTxDialog::OfflineTxDialog(const QString &jsonPacket, QWidget *parent) :
    QDialog(parent), packet(jsonPacket)
{
    setWindowTitle("Offline Transaction Preparation");
    resize(600, 400);
    QVBoxLayout *layout = new QVBoxLayout(this);

    QTextEdit *textEdit = new QTextEdit(this);
    textEdit->setReadOnly(true);
    textEdit->setPlainText(packet);
    layout->addWidget(textEdit);

    QHBoxLayout *hLayout = new QHBoxLayout();
    QPushButton *copyBtn = new QPushButton("Copy to Clipboard", this);
    QPushButton *saveBtn = new QPushButton("Save to File", this);
    hLayout->addWidget(copyBtn);
    hLayout->addWidget(saveBtn);
    layout->addLayout(hLayout);

    connect(copyBtn, SIGNAL(clicked()), this, SLOT(on_copyButton_clicked()));
    connect(saveBtn, SIGNAL(clicked()), this, SLOT(on_saveButton_clicked()));
}

void OfflineTxDialog::on_copyButton_clicked() {
    QApplication::clipboard()->setText(packet);
    QMessageBox::information(this, "Success", "Copied to clipboard!");
}

void OfflineTxDialog::on_saveButton_clicked() {
    QString fileName = QFileDialog::getSaveFileName(this, "Save Transaction", "", "Hexlan Offline (*.hexlan);;All Files (*)");
    if (!fileName.isEmpty()) {
        QFile file(fileName);
        if (file.open(QIODevice::WriteOnly)) {
            file.write(packet.toUtf8());
            file.close();
        }
    }
}

OfflineTxDialog::~OfflineTxDialog() {}
