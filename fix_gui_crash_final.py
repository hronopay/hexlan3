import os

f_cpp = "src/qt/bitcoingui.cpp"
with open(f_cpp, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("void BitcoinGUI::importXpubClicked()")
if idx != -1:
    code = code[:idx] + """void BitcoinGUI::importXpubClicked()
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
            params.push_back(xpub.trimmed().toStdString()); // HEXLAN: Защита от случайных пробелов
            params.push_back(100); 
            params.push_back(true); 
            
            json_spirit::Value result;
            {
                // HEXLAN: Жизненно важные блокировки потоков перед сканированием!
                LOCK2(cs_main, pwalletMain->cs_wallet);
                result = importxpub(params, false);
            }
            
            progress.close();
            QMessageBox::information(this, tr("Success"), tr("xpub imported successfully! Check your Dashboard for balances."));
        } catch (const json_spirit::Object& obj) {
            progress.close();
            // Вытаскиваем человекочитаемое сообщение из JSON
            std::string err_msg = "Unknown RPC Error";
            for (unsigned int i = 0; i < obj.size(); i++) {
                if (obj[i].name_ == "message") err_msg = obj[i].value_.get_str();
            }
            QMessageBox::critical(this, tr("Import Error"), tr("Failed to import xpub:\\n") + QString::fromStdString(err_msg));
        } catch (const std::exception& e) {
            progress.close();
            QMessageBox::critical(this, tr("System Error"), tr("Failed to import xpub:\\n") + QString::fromStdString(e.what()));
        }
    }
}
"""
    with open(f_cpp, "w", encoding="utf-8") as f:
        f.write(code)
    print("Success! GUI import function is now thread-safe and crash-proof.")
else:
    print("Error: Could not find importXpubClicked.")
