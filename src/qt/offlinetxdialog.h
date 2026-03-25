
#ifndef OFFLINETXDIALOG_H
#define OFFLINETXDIALOG_H

#include <QDialog>

namespace Ui { class OfflineTxDialog; }

class OfflineTxDialog : public QDialog
{
    Q_OBJECT
public:
    explicit OfflineTxDialog(const QString &jsonPacket, QWidget *parent = 0);
    ~OfflineTxDialog();

private slots:
    void on_copyButton_clicked();
    void on_saveButton_clicked();

private:
    Ui::OfflineTxDialog *ui;
    QString packet;
};
#endif
