TEMPLATE = app
TARGET = Hexlan-qt
VERSION = 2.1.0.3

INCLUDEPATH += src src/json src/qt src/qt/plugins/mrichtexteditor build

QT += network printsupport
DEFINES += ENABLE_WALLET
DEFINES += BOOST_THREAD_USE_LIB BOOST_SPIRIT_THREADSAFE
CONFIG += no_include_pwd
CONFIG += thread
CONFIG += static
CONFIG += openssl

greaterThan(QT_MAJOR_VERSION, 4) {
    QT += widgets
    DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0
}

macx {
    QMAKE_APPLE_DEVICE_ARCHS = x86_64
    QMAKE_MACOSX_DEPLOYMENT_TARGET = 10.13

    # Библиотеки в домашней папке (абсолютные пути)
    BOOST_INCLUDE_PATH = /Users/dns/boost_1_58_0
    BOOST_LIB_PATH = /Users/dns/boost_1_58_0/stage/lib

    OPENSSL_INCLUDE_PATH = /Users/dns/openssl-1.0.2l/include
    OPENSSL_LIB_PATH = /Users/dns/openssl-1.0.2l

    BDB_INCLUDE_PATH = /opt/local/include/db48
    BDB_LIB_PATH = /opt/local/lib/db48

    MINIUPNPC_INCLUDE_PATH = /opt/local/include
    MINIUPNPC_LIB_PATH = /opt/local/lib

    INCLUDEPATH += $$BOOST_INCLUDE_PATH $$OPENSSL_INCLUDE_PATH $$BDB_INCLUDE_PATH $$MINIUPNPC_INCLUDE_PATH

    DEFINES += MAC_OSX MSG_NOSIGNAL=0
    LIBS += -framework Foundation -framework ApplicationServices -framework AppKit -framework CoreServices

    LIBS += $$BOOST_LIB_PATH/libboost_thread.a \
            $$BOOST_LIB_PATH/libboost_filesystem.a \
            $$BOOST_LIB_PATH/libboost_program_options.a \
            $$BOOST_LIB_PATH/libboost_chrono.a \
            $$BOOST_LIB_PATH/libboost_system.a \
            /Users/dns/openssl-1.0.2l/libssl.a \
            /Users/dns/openssl-1.0.2l/libcrypto.a \
            -L$$BDB_LIB_PATH -ldb_cxx-4.8 \
            -L/opt/local/lib -lz -lminiupnpc -lgmp

    # Божья коровка и паспорт приложения
    ICON = src/qt/res/icons/Hexlan.icns
    QMAKE_INFO_PLIST = share/qt/Info.plist
}

OBJECTS_DIR = build
MOC_DIR = build
UI_DIR = build

INCLUDEPATH += src/leveldb/include src/leveldb/helpers
LIBS += $$PWD/src/leveldb/libleveldb.a $$PWD/src/leveldb/libmemenv.a
SOURCES += src/txdb-leveldb.cpp
!win32 {
    genleveldb.commands = cd $$PWD/src/leveldb && CC=$$QMAKE_CC CXX=$$QMAKE_CXX $(MAKE) OPT=\"$$QMAKE_CXXFLAGS $$QMAKE_CXXFLAGS_RELEASE\" libleveldb.a libmemenv.a
}
genleveldb.target = $$PWD/src/leveldb/libleveldb.a
genleveldb.depends = FORCE
PRE_TARGETDEPS += $$PWD/src/leveldb/libleveldb.a
QMAKE_EXTRA_TARGETS += genleveldb

!win32 {
    INCLUDEPATH += src/secp256k1/include
    LIBS += $$PWD/src/secp256k1/src/libsecp256k1_la-secp256k1.o
}

QMAKE_CXXFLAGS_WARN_ON = -fdiagnostics-show-option -Wall -Wextra -Wno-ignored-qualifiers -Wformat -Wformat-security -Wno-unused-parameter -Wstack-protector
QMAKE_CXXFLAGS_WARN_ON += -Wno-unused-variable -fpermissive
macx:QMAKE_CXXFLAGS_WARN_ON += -Wno-deprecated-declarations

DEPENDPATH += src src/json src/qt
HEADERS += src/qt/bitcoingui.h src/qt/transactiontablemodel.h src/qt/addresstablemodel.h \
    src/qt/bantablemodel.h src/qt/optionsdialog.h src/qt/coincontroldialog.h \
    src/qt/coincontroltreewidget.h src/qt/sendcoinsdialog.h src/qt/addressbookpage.h \
    src/qt/signverifymessagedialog.h src/qt/aboutdialog.h src/qt/editaddressdialog.h \
    src/qt/bitcoinaddressvalidator.h src/alert.h src/allocators.h src/addrman.h \
    src/base58.h src/bignum.h src/chainparams.h src/checkpoints.h src/sync.h \
    src/util.h src/hash.h src/uint256.h src/kernel.h src/pbkdf2.h src/serialize.h \
    src/support/cleanse.h src/core.h src/main.h src/miner.h src/net.h src/ecwrapper.h \
    src/key.h src/pubkey.h src/db.h src/txdb.h src/txmempool.h src/walletdb.h \
    src/script.h src/scrypt.h src/init.h src/json/json_spirit.h src/qt/clientmodel.h \
    src/qt/guiutil.h src/qt/transactionrecord.h src/qt/guiconstants.h src/qt/optionsmodel.h \
    src/qt/peertablemodel.h src/qt/trafficgraphwidget.h src/qt/transactiondesc.h \
    src/qt/transactiondescdialog.h src/qt/bitcoinamountfield.h src/wallet.h src/keystore.h \
    src/qt/transactionfilterproxy.h src/qt/transactionview.h src/qt/walletmodel.h \
    src/qt/walletmodeltransaction.h src/rpcclient.h src/rpcprotocol.h src/rpcserver.h \
    src/qt/overviewpage.h src/qt/csvmodelwriter.h src/crypter.h src/qt/sendcoinsentry.h \
    src/qt/qvalidatedlineedit.h src/qt/bitcoinunits.h src/qt/qvaluecombobox.h \
    src/qt/askpassphrasedialog.h src/protocol.h src/qt/notificator.h src/qt/paymentserver.h \
    src/qt/rpcconsole.h src/version.h src/netbase.h src/clientversion.h src/threadsafety.h \
    src/tinyformat.h src/stealth.h src/masternode.h src/darksend.h src/instantx.h \
    src/activemasternode.h src/masternodeconfig.h src/masternodeman.h src/spork.h \
    src/smessage.h src/qt/messagemodel.h src/qt/messagepage.h src/qt/tradingdialog.h \
    src/crypto/sha256.h src/crypto/sha1.h src/crypto/ripemd160.h src/masternode-payments.h \
    src/qt/blockbrowser.h src/qt/darksendconfig.h src/qt/masternodemanager.h \
    src/qt/sendmessagesdialog.h src/qt/monitoreddatamapper.h \
    src/qt/sendmessagesentry.h src/qt/addeditadrenalinenode.h \
    src/qt/macdockiconhandler.h src/qt/macnotificationhandler.h \
    src/qt/qvalidatedtextedit.h src/qt/plugins/mrichtexteditor/mrichtextedit.h

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
    src/qt/optionsmodel.cpp src/qt/peertablemodel.cpp src/qt/trafficgraphwidget.cpp \
    src/qt/transactiondesc.cpp src/qt/transactiondescdialog.cpp src/qt/bitcoinstrings.cpp \
    src/qt/bitcoinamountfield.cpp src/wallet.cpp src/keystore.cpp src/qt/transactionfilterproxy.cpp \
    src/qt/transactionview.cpp src/qt/walletmodel.cpp src/qt/walletmodeltransaction.cpp \
    src/rpcclient.cpp src/rpcprotocol.cpp src/rpcserver.cpp src/rpcdump.cpp src/rpcmisc.cpp \
    src/rpcnet.cpp src/rpcmining.cpp src/rpcwallet.cpp src/rpcblockchain.cpp \
    src/rpcrawtransaction.cpp src/qt/overviewpage.cpp src/qt/csvmodelwriter.cpp src/crypter.cpp \
    src/qt/sendcoinsentry.cpp src/qt/qvalidatedlineedit.cpp src/qt/bitcoinunits.cpp \
    src/qt/qvaluecombobox.cpp src/qt/askpassphrasedialog.cpp src/protocol.cpp \
    src/qt/notificator.cpp src/qt/paymentserver.cpp src/qt/rpcconsole.cpp src/noui.cpp \
    src/kernel.cpp src/pbkdf2.cpp src/support/cleanse.cpp src/stealth.cpp src/masternode.cpp \
    src/darksend.cpp src/instantx.cpp src/activemasternode.cpp src/masternodeman.cpp \
    src/spork.cpp src/masternodeconfig.cpp src/smessage.cpp src/qt/messagemodel.cpp \
    src/qt/messagepage.cpp src/qt/tradingdialog.cpp src/rpcsmessage.cpp \
    src/crypto/sha256.cpp src/crypto/sha1.cpp src/crypto/ripemd160.cpp \
    src/masternode-payments.cpp src/rpcdarksend.cpp \
    src/qt/blockbrowser.cpp src/qt/darksendconfig.cpp src/qt/masternodemanager.cpp \
    src/qt/sendmessagesdialog.cpp src/qt/monitoreddatamapper.cpp \
    src/qt/sendmessagesentry.cpp src/qt/addeditadrenalinenode.cpp \
    src/qt/qvalidatedtextedit.cpp src/qt/plugins/mrichtexteditor/mrichtextedit.cpp

RESOURCES += src/qt/bitcoin.qrc

FORMS += src/qt/forms/coincontroldialog.ui src/qt/forms/sendcoinsdialog.ui \
    src/qt/forms/addressbookpage.ui src/qt/forms/signverifymessagedialog.ui \
    src/qt/forms/aboutdialog.ui src/qt/forms/editaddressdialog.ui \
    src/qt/forms/transactiondescdialog.ui src/qt/forms/overviewpage.ui \
    src/qt/forms/sendcoinsentry.ui src/qt/forms/askpassphrasedialog.ui \
    src/qt/forms/rpcconsole.ui src/qt/forms/optionsdialog.ui \
    src/qt/forms/messagepage.ui src/qt/forms/tradingdialog.ui \
    src/qt/forms/blockbrowser.ui src/qt/forms/darksendconfig.ui \
    src/qt/forms/masternodemanager.ui src/qt/forms/sendmessagesdialog.ui \
    src/qt/forms/sendmessagesentry.ui src/qt/forms/addeditadrenalinenode.ui \
    src/qt/plugins/mrichtexteditor/mrichtextedit.ui

CODECFORTR = UTF-8

macx:OBJECTIVE_SOURCES += src/qt/macdockiconhandler.mm src/qt/macnotificationhandler.mm