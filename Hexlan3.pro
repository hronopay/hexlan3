TEMPLATE = app
TARGET = Hexlan-qt
VERSION = 2.1.0.3

# --- ПОРЯДОК В ФАЙЛАХ ---
# Весь мусор (.o, .moc) полетит в папку build
OBJECTS_DIR = build
MOC_DIR = build
RCC_DIR = build
UI_DIR = build

# --- ОСНОВНЫЕ НАСТРОЙКИ ---
INCLUDEPATH += src src/json src/qt src/qt/plugins/mrichtexteditor build
QT += network printsupport widgets
DEFINES += ENABLE_WALLET BOOST_THREAD_USE_LIB BOOST_SPIRIT_THREADSAFE
CONFIG += no_include_pwd thread static

# --- ФУНКЦИОНАЛ ---
DEFINES += USE_QRCODE
DEFINES += USE_UPNP=0
DEFINES -= USE_UPNP

# --- ЗАВИСИМОСТИ (LINUX STATIC) ---
MY_BOOST_DIR = $$PWD/libs
DEPS_DIR = $$PWD/bundled_deps

INCLUDEPATH += $$MY_BOOST_DIR
INCLUDEPATH += $$MY_BOOST_DIR/include
INCLUDEPATH += $$MY_BOOST_DIR/boost

INCLUDEPATH += $$DEPS_DIR/openssl/include
INCLUDEPATH += $$DEPS_DIR/db48/include
INCLUDEPATH += $$DEPS_DIR/qrencode/include

INCLUDEPATH += src/leveldb/include src/leveldb/helpers
INCLUDEPATH += src/secp256k1/include

# --- ИСХОДНИКИ ---
# (Убраны bitcoinrpc.h и другие фантомы)
HEADERS += src/qt/bitcoingui.h src/qt/transactiontablemodel.h \
    src/qt/addresstablemodel.h src/qt/optionsdialog.h src/qt/coincontroldialog.h \
    src/qt/coincontroltreewidget.h src/qt/sendcoinsdialog.h src/qt/addressbookpage.h \
    src/qt/signverifymessagedialog.h src/qt/aboutdialog.h src/qt/editaddressdialog.h \
    src/qt/bitcoinaddressvalidator.h src/qt/clientmodel.h src/qt/guiutil.h \
    src/qt/transactionrecord.h src/qt/guiconstants.h src/qt/optionsmodel.h \
    src/qt/monitoreddatamapper.h src/qt/transactiondesc.h src/qt/transactiondescdialog.h \
    src/qt/bitcoinamountfield.h src/wallet.h src/walletdb.h src/db.h src/base58.h \
    src/json/json_spirit.h src/json/json_spirit_value.h \
    src/json/json_spirit_writer.h src/init.h src/util.h src/ui_interface.h \
    src/qt/qvalidatedlineedit.h src/qt/walletmodel.h src/qt/walletmodeltransaction.h \
    src/qt/csvmodelwriter.h src/net.h src/main.h src/qt/transactionview.h \
    src/qt/transactionfilterproxy.h src/qt/qvaluecombobox.h src/qt/askpassphrasedialog.h \
    src/protocol.h src/addrman.h src/qt/notificator.h src/qt/paymentserver.h \
    src/qt/rpcconsole.h src/qt/peertablemodel.h \
    src/qt/trafficgraphwidget.h src/qt/adrenalinenodeconfigdialog.h \
    src/qt/addeditadrenalinenode.h src/qt/masternodemanager.h \
    src/qt/messagemodel.h src/qt/messagepage.h src/qt/tradingdialog.h \
    src/qt/blockbrowser.h src/qt/sendmessagesdialog.h \
    src/qt/sendmessagesentry.h src/qt/sendcoinsentry.h \
    src/qt/qvalidatedtextedit.h src/qt/plugins/mrichtexteditor/mrichtextedit.h \
    src/qt/darksendconfig.h src/qt/qcustomplot.h src/qt/macdockiconhandler.h \
    src/qt/macnotificationhandler.h src/qt/qrcodedialog.h

SOURCES += src/qt/bitcoin.cpp src/qt/bitcoingui.cpp src/qt/transactiontablemodel.cpp \
    src/qt/addresstablemodel.cpp src/qt/optionsdialog.cpp src/qt/sendcoinsdialog.cpp \
    src/qt/coincontroldialog.cpp src/qt/coincontroltreewidget.cpp \
    src/qt/addressbookpage.cpp src/qt/signverifymessagedialog.cpp \
    src/qt/aboutdialog.cpp src/qt/editaddressdialog.cpp src/qt/bitcoinaddressvalidator.cpp \
    src/qt/clientmodel.cpp src/qt/guiutil.cpp src/qt/transactionrecord.cpp \
    src/qt/optionsmodel.cpp src/qt/monitoreddatamapper.cpp src/qt/transactiondesc.cpp \
    src/qt/transactiondescdialog.cpp src/qt/bitcoinstrings.cpp src/qt/bitcoinamountfield.cpp \
    src/wallet.cpp src/walletdb.cpp src/db.cpp src/init.cpp src/util.cpp \
    src/qt/qvalidatedlineedit.cpp src/qt/walletmodel.cpp src/qt/walletmodeltransaction.cpp \
    src/qt/csvmodelwriter.cpp src/net.cpp src/main.cpp src/qt/transactionview.cpp \
    src/qt/transactionfilterproxy.cpp src/qt/qvaluecombobox.cpp src/qt/askpassphrasedialog.cpp \
    src/protocol.cpp src/addrman.cpp src/qt/notificator.cpp src/qt/rpcconsole.cpp \
    src/qt/peertablemodel.cpp src/qt/paymentserver.cpp src/qt/trafficgraphwidget.cpp \
    src/qt/adrenalinenodeconfigdialog.cpp src/qt/addeditadrenalinenode.cpp \
    src/qt/masternodemanager.cpp src/qt/sendcoinsentry.cpp \
    src/rpcclient.cpp src/rpcprotocol.cpp src/rpcserver.cpp src/rpcmisc.cpp \
    src/rpcnet.cpp src/rpcblockchain.cpp src/rpcrawtransaction.cpp \
    src/script.cpp src/sync.cpp src/txmempool.cpp src/hash.cpp src/noui.cpp \
    src/kernel.cpp src/pbkdf2.cpp src/scrypt.cpp src/chainparams.cpp \
    src/stealth.cpp src/activemasternode.cpp src/darksend.cpp src/darksend-relay.cpp \
    src/instantx.cpp src/masternodeman.cpp src/masternode.cpp src/utilstrencodings.cpp \
    src/spork.cpp src/masternodeconfig.cpp src/smessage.cpp src/qt/messagemodel.cpp \
    src/qt/messagepage.cpp src/qt/tradingdialog.cpp src/rpcsmessage.cpp \
    src/crypto/sha256.cpp src/crypto/sha1.cpp src/crypto/ripemd160.cpp \
    src/masternode-payments.cpp src/rpcdarksend.cpp \
    src/qt/blockbrowser.cpp src/qt/darksendconfig.cpp src/qt/masternodemanager.cpp \
    src/qt/sendmessagesdialog.cpp src/qt/monitoreddatamapper.cpp \
    src/qt/sendmessagesentry.cpp src/qt/addeditadrenalinenode.cpp \
    src/qt/qvalidatedtextedit.cpp src/qt/plugins/mrichtexteditor/mrichtextedit.cpp \
    src/qt/qrcodedialog.cpp

RESOURCES += src/qt/bitcoin.qrc

FORMS += src/qt/forms/coincontroldialog.ui src/qt/forms/sendcoinsdialog.ui \
    src/qt/forms/addressbookpage.ui src/qt/forms/signverifymessagedialog.ui \
    src/qt/forms/aboutdialog.ui src/qt/forms/editaddressdialog.ui \
    src/qt/forms/transactiondescdialog.ui src/qt/forms/overviewpage.ui \
    src/qt/forms/sendcoinsentry.ui src/qt/forms/askpassphrasedialog.ui \
    src/qt/forms/rpcconsole.ui src/qt/forms/optionsdialog.ui \
    src/qt/forms/adrenalinenodeconfigdialog.ui src/qt/forms/masternodemanager.ui \
    src/qt/forms/messagepage.ui src/qt/forms/tradingdialog.ui \
    src/qt/forms/sendmessagesdialog.ui src/qt/forms/sendmessagesentry.ui \
    src/qt/forms/blockbrowser.ui src/qt/forms/darksendconfig.ui \
    src/qt/forms/addeditadrenalinenode.ui src/qt/forms/qrcodedialog.ui

# --- ЛИНКОВКА (UNIX) ---
unix {
    QMAKE_CXXFLAGS += -fpermissive -w

    # Boost
    LIBS += -L$$MY_BOOST_DIR/lib -L$$MY_BOOST_DIR/stage/lib -L$$MY_BOOST_DIR

    # OpenSSL, DB, QR
    LIBS += -L$$DEPS_DIR/openssl/lib
    LIBS += -L$$DEPS_DIR/db48/lib
    LIBS += $$DEPS_DIR/qrencode/lib/libqrencode.a

    # Статические либы
    LIBS += -lboost_system -lboost_filesystem -lboost_program_options -lboost_thread -lboost_chrono
    LIBS += -ldb_cxx
    LIBS += -lssl -lcrypto

    # Системные
    LIBS += -lrt -lpthread -ldl

    # Внутренние
    LIBS += src/leveldb/libleveldb.a src/leveldb/libmemenv.a
    LIBS += src/secp256k1/.libs/libsecp256k1.a
}
