TEMPLATE = app
TARGET = Hexlan-qt
VERSION = 2.1.0.3

# --- ОБЩИЕ НАСТРОЙКИ ---
QT += network printsupport widgets
CONFIG += static thread release no_include_pwd
# Отключаем предупреждения глобально
QMAKE_CXXFLAGS += -w

# --- ОБЩИЕ ОПРЕДЕЛЕНИЯ ---
DEFINES += ENABLE_WALLET BOOST_THREAD_USE_LIB BOOST_SPIRIT_THREADSAFE
DEFINES += USE_UPNP MINIUPNP_STATICLIB STATICLIB

# --- ВНУТРЕННИЕ ПУТИ (ОБЩИЕ) ---
INCLUDEPATH += src src/json src/qt src/qt/plugins/mrichtexteditor
INCLUDEPATH += src/secp256k1/include
INCLUDEPATH += src/leveldb/include src/leveldb/helpers
DEPENDPATH += src src/json src/qt

# ==============================================================================
#                                WINDOWS (WIN32)
# ==============================================================================
win32 {
    message(Building for Windows...)

    # --- ПАПКИ СБОРКИ ---
    OBJECTS_DIR = build_win
    MOC_DIR = build_win
    RCC_DIR = build_win
    UI_DIR = build_win

    # --- СПЕЦИФИЧНЫЕ ОПРЕДЕЛЕНИЯ ---
    DEFINES += WIN32 _WIN32 _MINGW WIN32_LEAN_AND_MEAN

    # --- ПУТИ К БИБЛИОТЕКАМ (deps_sources) ---
    DEPS_BASE = $$PWD/deps_sources

    # Boost 1.76.0
    INCLUDEPATH += $$DEPS_BASE/boost_1_76_0
    LIBS += -L$$DEPS_BASE/boost_1_76_0/stage/lib \
            -lboost_system-mt-x64 \
            -lboost_filesystem-mt-x64 \
            -lboost_program_options-mt-x64 \
            -lboost_thread-mt-x64 \
            -lboost_chrono-mt-x64

    # Berkeley DB 4.8.30
    INCLUDEPATH += $$DEPS_BASE/db-4.8.30.NC/build_unix
    LIBS += -L$$DEPS_BASE/db-4.8.30.NC/build_unix -ldb_cxx

    # OpenSSL 1.0.2u
    INCLUDEPATH += $$DEPS_BASE/openssl-1.0.2u/include
    LIBS += -L$$DEPS_BASE/openssl-1.0.2u -lssl -lcrypto

    # MiniUPnPc 1.9
    INCLUDEPATH += $$DEPS_BASE/miniupnpc-1.9
    LIBS += -L$$DEPS_BASE/miniupnpc-1.9 -lminiupnpc

    # Qrencode 4.1.1
    INCLUDEPATH += $$DEPS_BASE/qrencode-4.1.1
    LIBS += -L$$DEPS_BASE/qrencode-4.1.1/.libs -lqrencode

    # Системные библиотеки Windows
    LIBS += -lws2_32 -lshlwapi -lmswsock -liphlpapi -lgdi32 -lcrypt32 -lrpcrt4 -luuid -lole32
}

# ==============================================================================
#                                LINUX (UNIX)
# ==============================================================================
unix:!macx {
    message(Building for Linux...)

    # --- ПАПКИ СБОРКИ ---
    OBJECTS_DIR = build_linux
    MOC_DIR = build_linux
    RCC_DIR = build_linux
    UI_DIR = build_linux

    # --- ФЛАГИ КОМПИЛЯТОРА ---
    QMAKE_CXXFLAGS += -fpermissive

    # --- ПУТИ К БИБЛИОТЕКАМ (libs / bundled_deps) ---
    MY_BOOST_DIR = $$PWD/libs
    DEPS_DIR = $$PWD/bundled_deps

    INCLUDEPATH += $$MY_BOOST_DIR/include
    INCLUDEPATH += $$MY_BOOST_DIR/boost
    INCLUDEPATH += $$DEPS_DIR/openssl/include
    INCLUDEPATH += $$DEPS_DIR/db48/include
    INCLUDEPATH += $$DEPS_DIR/qrencode/include
    INCLUDEPATH += $$DEPS_DIR/miniupnpc-1.9

    # Boost (линковка)
    LIBS += -L$$MY_BOOST_DIR/lib -L$$MY_BOOST_DIR/stage/lib -L$$MY_BOOST_DIR
    LIBS += -lboost_system -lboost_filesystem -lboost_program_options -lboost_thread -lboost_chrono

    # OpenSSL
    LIBS += -L$$DEPS_DIR/openssl/lib -lssl -lcrypto

    # Berkeley DB
    LIBS += -L$$DEPS_DIR/db48/lib -ldb_cxx

    # MiniUPnPc
    LIBS += $$DEPS_DIR/miniupnpc-1.9/libminiupnpc.a

    # Qrencode
    LIBS += $$DEPS_DIR/qrencode/lib/libqrencode.a

    # Системные библиотеки Linux
    LIBS += -lrt -lpthread -ldl
}

# ==============================================================================
#                        ОБЩИЕ ИСХОДНИКИ И РЕСУРСЫ
# ==============================================================================

HEADERS += src/qt/bitcoingui.h src/qt/transactiontablemodel.h src/qt/addresstablemodel.h \
    src/qt/bantablemodel.h src/qt/optionsdialog.h src/qt/coincontroldialog.h \
    src/qt/coincontroltreewidget.h src/qt/sendcoinsdialog.h src/qt/addressbookpage.h \
    src/qt/signverifymessagedialog.h src/qt/aboutdialog.h src/qt/editaddressdialog.h \
    src/qt/bitcoinaddressvalidator.h src/alert.h src/allocators.h src/addrman.h \
    src/base58.h src/bignum.h src/chainparams.h src/chainparamsseeds.h src/checkpoints.h \
    src/compat.h src/coincontrol.h src/sync.h src/util.h src/hash.h src/uint256.h \
    src/kernel.h src/pbkdf2.h src/serialize.h src/support/cleanse.h src/core.h \
    src/main.h src/miner.h src/net.h src/ecwrapper.h src/key.h src/pubkey.h \
    src/db.h src/txdb.h src/txmempool.h src/walletdb.h src/script.h src/scrypt.h \
    src/init.h src/mruset.h src/json/json_spirit_writer_template.h \
    src/json/json_spirit_writer.h src/json/json_spirit_value.h src/json/json_spirit_utils.h \
    src/json/json_spirit_stream_reader.h src/json/json_spirit_reader_template.h \
    src/json/json_spirit_reader.h src/json/json_spirit_error_position.h src/json/json_spirit.h \
    src/qt/clientmodel.h src/qt/guiutil.h src/qt/transactionrecord.h src/qt/guiconstants.h \
    src/qt/optionsmodel.h src/qt/monitoreddatamapper.h src/qt/peertablemodel.h \
    src/qt/trafficgraphwidget.h src/qt/transactiondesc.h src/qt/transactiondescdialog.h \
    src/qt/bitcoinamountfield.h src/wallet.h src/keystore.h src/qt/transactionfilterproxy.h \
    src/qt/transactionview.h src/qt/walletmodel.h src/qt/walletmodeltransaction.h \
    src/rpcclient.h src/rpcprotocol.h src/rpcserver.h src/limitedmap.h \
    src/qt/overviewpage.h src/qt/csvmodelwriter.h src/crypter.h src/qt/sendcoinsentry.h \
    src/qt/qvalidatedlineedit.h src/qt/bitcoinunits.h src/qt/qvaluecombobox.h \
    src/qt/askpassphrasedialog.h src/protocol.h src/qt/notificator.h src/qt/paymentserver.h \
    src/ui_interface.h src/qt/rpcconsole.h src/version.h src/netbase.h src/clientversion.h \
    src/threadsafety.h src/tinyformat.h src/stealth.h src/qt/flowlayout.h \
    src/qt/darksendconfig.h src/masternode.h src/darksend.h src/darksend-relay.h \
    src/instantx.h src/activemasternode.h src/masternodeconfig.h src/masternodeman.h \
    src/masternode-payments.h src/spork.h src/crypto/common.h src/crypto/hmac_sha256.h \
    src/crypto/hmac_sha512.h src/crypto/ripemd160.h src/crypto/sha1.h src/crypto/sha256.h \
    src/crypto/sha512.h src/qt/masternodemanager.h src/qt/addeditadrenalinenode.h \
    src/qt/adrenalinenodeconfigdialog.h src/qt/qcustomplot.h src/smessage.h \
    src/qt/messagepage.h src/qt/messagemodel.h src/qt/sendmessagesdialog.h \
    src/qt/sendmessagesentry.h src/qt/blockbrowser.h \
    src/qt/plugins/mrichtexteditor/mrichtextedit.h src/qt/qvalidatedtextedit.h \
    src/qt/tradingdialog.h src/qt/qrcodedialog.h

SOURCES += src/qt/bitcoin.cpp src/qt/bitcoingui.cpp src/qt/transactiontablemodel.cpp \
    src/qt/addresstablemodel.cpp src/qt/bantablemodel.cpp src/qt/optionsdialog.cpp \
    src/qt/sendcoinsdialog.cpp src/qt/coincontroldialog.cpp src/qt/coincontroltreewidget.cpp \
    src/qt/addressbookpage.cpp src/qt/signverifymessagedialog.cpp src/qt/aboutdialog.cpp \
    src/qt/editaddressdialog.cpp src/qt/bitcoinaddressvalidator.cpp src/alert.cpp \
    src/allocators.cpp src/base58.cpp src/chainparams.cpp src/version.cpp src/sync.cpp \
    src/txmempool.cpp src/util.cpp src/hash.cpp src/netbase.cpp src/ecwrapper.cpp \
    src/key.cpp src/pubkey.cpp src/script.cpp src/scrypt.cpp src/core.cpp src/main.cpp \
    src/miner.cpp src/init.cpp src/net.cpp src/checkpoints.cpp src/addrman.cpp src/db.cpp \
    src/walletdb.cpp src/qt/clientmodel.cpp src/qt/guiutil.cpp src/qt/transactionrecord.cpp \
    src/qt/optionsmodel.cpp src/qt/monitoreddatamapper.cpp src/qt/peertablemodel.cpp \
    src/qt/trafficgraphwidget.cpp src/qt/transactiondesc.cpp src/qt/transactiondescdialog.cpp \
    src/qt/bitcoinstrings.cpp src/qt/bitcoinamountfield.cpp src/wallet.cpp src/keystore.cpp \
    src/qt/transactionfilterproxy.cpp src/qt/transactionview.cpp src/qt/walletmodel.cpp \
    src/qt/walletmodeltransaction.cpp src/rpcclient.cpp src/rpcprotocol.cpp src/rpcserver.cpp \
    src/rpcdump.cpp src/rpcmisc.cpp src/rpcnet.cpp src/rpcmining.cpp src/rpcwallet.cpp \
    src/rpcblockchain.cpp src/rpcrawtransaction.cpp src/qt/overviewpage.cpp \
    src/qt/csvmodelwriter.cpp src/crypter.cpp src/qt/sendcoinsentry.cpp \
    src/qt/qvalidatedlineedit.cpp src/qt/bitcoinunits.cpp src/qt/qvaluecombobox.cpp \
    src/qt/askpassphrasedialog.cpp src/protocol.cpp src/qt/notificator.cpp \
    src/qt/paymentserver.cpp src/qt/rpcconsole.cpp src/noui.cpp src/kernel.cpp src/pbkdf2.cpp \
    src/support/cleanse.cpp src/stealth.cpp src/qt/flowlayout.cpp src/qt/darksendconfig.cpp \
    src/masternode.cpp src/darksend.cpp src/darksend-relay.cpp src/rpcdarksend.cpp \
    src/instantx.cpp src/activemasternode.cpp src/masternodeman.cpp \
    src/masternode-payments.cpp src/spork.cpp src/masternodeconfig.cpp \
    src/crypto/hmac_sha256.cpp src/crypto/hmac_sha512.cpp src/crypto/ripemd160.cpp \
    src/crypto/sha1.cpp src/crypto/sha256.cpp src/crypto/sha512.cpp \
    src/qt/masternodemanager.cpp src/qt/addeditadrenalinenode.cpp \
    src/qt/adrenalinenodeconfigdialog.cpp src/qt/qcustomplot.cpp src/smessage.cpp \
    src/qt/messagepage.cpp src/qt/messagemodel.cpp src/qt/sendmessagesdialog.cpp \
    src/qt/sendmessagesentry.cpp src/qt/blockbrowser.cpp src/qt/qvalidatedtextedit.cpp \
    src/qt/plugins/mrichtexteditor/mrichtextedit.cpp src/qt/tradingdialog.cpp \
    src/rpcsmessage.cpp src/qt/qrcodedialog.cpp src/txdb-leveldb.cpp

RESOURCES += src/qt/bitcoin.qrc

FORMS += src/qt/forms/coincontroldialog.ui src/qt/forms/sendcoinsdialog.ui \
    src/qt/forms/addressbookpage.ui src/qt/forms/signverifymessagedialog.ui \
    src/qt/forms/aboutdialog.ui src/qt/forms/editaddressdialog.ui \
    src/qt/forms/transactiondescdialog.ui src/qt/forms/overviewpage.ui \
    src/qt/forms/sendcoinsentry.ui src/qt/forms/askpassphrasedialog.ui \
    src/qt/forms/rpcconsole.ui src/qt/forms/optionsdialog.ui src/qt/forms/darksendconfig.ui \
    src/qt/forms/masternodemanager.ui src/qt/forms/addeditadrenalinenode.ui \
    src/qt/forms/adrenalinenodeconfigdialog.ui src/qt/forms/messagepage.ui \
    src/qt/forms/sendmessagesentry.ui src/qt/forms/sendmessagesdialog.ui \
    src/qt/forms/blockbrowser.ui src/qt/forms/tradingdialog.ui \
    src/qt/plugins/mrichtexteditor/mrichtextedit.ui src/qt/forms/qrcodedialog.ui

# --- ВНУТРЕННИЕ СТАТИЧЕСКИЕ БИБЛИОТЕКИ (ОБЩИЕ) ---
# Используем $$PWD, чтобы путь всегда был абсолютным и верным
LIBS += $$PWD/src/leveldb/libleveldb.a $$PWD/src/leveldb/libmemenv.a
LIBS += $$PWD/src/secp256k1/.libs/libsecp256k1.a
LIBS += -lpthread
