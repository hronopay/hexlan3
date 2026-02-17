#!/bin/bash
set -e

# Настройка путей
export MXE_PATH=/mnt/mxe
export PATH=$MXE_PATH/usr/bin:$PATH
export HOST=x86_64-w64-mingw32.static

# Компиляторы
CROSS_CC=$HOST-gcc
CROSS_CXX=$HOST-g++
CROSS_AR=$HOST-ar

echo "--- STARTING COMPILATION (FIXED BOOST COMMAND) ---"

# 1. OpenSSL 1.0.1u
if [ -f "openssl-1.0.1u/libssl.a" ]; then
    echo ">>> OpenSSL already built. Skipping..."
else
    echo ">>> Building OpenSSL 1.0.1u..."
    cd openssl-1.0.1u
    make clean || true
    CC=gcc ./Configure --cross-compile-prefix=$HOST- mingw64 no-shared no-dso
    make
    cd ..
fi

# 2. Berkeley DB 4.8.30
if [ -f "db-4.8.30.NC/build_unix/libdb_cxx.a" ]; then
    echo ">>> Berkeley DB already built. Skipping..."
else
    echo ">>> Building Berkeley DB 4.8.30..."
    cd db-4.8.30.NC
    sed -i 's/__atomic_compare_exchange/__atomic_compare_exchange_db/g' dbinc/atomic.h
    cd build_unix
    make clean || true
    ../dist/configure --host=$HOST --enable-cxx --disable-shared --enable-static \
        --disable-replication \
        CC=$CROSS_CC CXX=$CROSS_CXX \
        CPPFLAGS="-DWIN32 -D_MINGW_ -D_WIN32" \
        LIBS="-lws2_32"
    
    # ПАТЧИ (на случай пересборки)
    sed -i 's/#include <netdb.h>/#include <winsock2.h>\n#include <ws2tcpip.h>/' db_int.h
    sed -i 's/#include <netinet\/in.h>/#include <winsock2.h>\n#include <ws2tcpip.h>/' db_int.h
    sed -i 's/#include <sys\/socket.h>/#include <winsock2.h>/' db_int.h
    sed -i 's/#include <arpa\/inet.h>/#include <winsock2.h>/' db_int.h
    sed -i 's/#include <sys\/select.h>/\/\/ sys\/select.h replaced/' db_int.h
    sed -i 's/^#define socklen_t int/\/* #undef socklen_t *\//' db_config.h
    sed -i 's/^#define HAVE_SYS_UIO_H.*$/\/* #undef HAVE_SYS_UIO_H *\//' db_config.h
    sed -i 's/#include <sys\/uio.h>/struct iovec { void *iov_base; size_t iov_len; };/' db_int.h
    find ../repmgr ../os ../clib -name "*.c" -print0 | xargs -0 sed -i 's/\bADDRINFO\b/DB_ADDRINFO/g'
    sed -i 's/\bADDRINFO\b/DB_ADDRINFO/g' ../dbinc/repmgr.h
    sed -i 's/\bADDRINFO\b/DB_ADDRINFO/g' ../dbinc_auto/repmgr_ext.h
    sed -i 's/\bADDRINFO\b/DB_ADDRINFO/g' ../dbinc_auto/os_ext.h
    sed -i 's/mkdir(name, DB_MODE_700)/mkdir(name)/g' ../os/os_mkdir.c
    sed -i 's/mkdir(name, mode)/mkdir(name)/g' ../os/os_mkdir.c
    sed -i 's/fsync(fhp->fd)/_commit(fhp->fd)/g' ../os/os_fsync.c
    sed -i '/#include "db_int.h"/a #include <io.h>' ../os/os_fsync.c
    
    make
    cd ../..
fi

# 3. Boost 1.76.0
echo ">>> Building Boost 1.76.0..."
cd boost_1_76_0
./bootstrap.sh
echo "using gcc : mxe : $CROSS_CXX ;" > user-config.jam

# ИСПРАВЛЕНИЕ: linking=static -> link=static
./b2 toolset=gcc-mxe target-os=windows threadapi=win32 link=static variant=release --layout=tagged --user-config=user-config.jam -j2
cd ..

# 4. MiniUPnPc 1.9
echo ">>> Building MiniUPnPc 1.9..."
cd miniupnpc-1.9
make -f Makefile.mingw CC=$CROSS_CC AR=$CROSS_AR libminiupnpc.a
cd ..

# 5. LibQrencode 4.1.1
echo ">>> Building LibQrencode 4.1.1..."
cd qrencode-4.1.1
./configure --host=$HOST --enable-static --disable-shared --without-tools --without-libiconv-prefix CC=$CROSS_CC
make
cd ..

echo "--- ALL 5 LIBRARIES BUILT SUCCESSFULLY! ---"
