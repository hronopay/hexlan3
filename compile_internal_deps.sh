#!/bin/bash
set -e
export MXE_PATH=/mnt/mxe
export PATH=$MXE_PATH/usr/bin:$PATH
export HOST=x86_64-w64-mingw32.static

echo ">>> Compiling Internal Dependencies for Windows..."

# 1. Secp256k1
echo ">>> Building Secp256k1..."
cd src/secp256k1
make clean || true
chmod +x autogen.sh
./autogen.sh
./configure --host=$HOST --enable-module-recovery --with-bignum=no --enable-endomorphism
make
cd ../..

# 2. LevelDB
echo ">>> Building LevelDB..."
cd src/leveldb
make clean || true
# LevelDB обычно использует свой Makefile, нам нужно передать ему кросс-компилятор
TARGET_OS=OS_WINDOWS_CROSSCOMPILE make CC=$HOST-gcc CXX=$HOST-g++ AR=$HOST-ar libleveldb.a libmemenv.a
cd ../..

echo "--- INTERNAL DEPS READY ---"
