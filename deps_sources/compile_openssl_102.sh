#!/bin/bash
set -e
export MXE_PATH=/mnt/mxe
export PATH=$MXE_PATH/usr/bin:$PATH
export HOST=x86_64-w64-mingw32.static

echo ">>> Downloading OpenSSL 1.0.2u..."
# Скачиваем прямо в текущую папку
wget -c https://www.openssl.org/source/openssl-1.0.2u.tar.gz
tar xzf openssl-1.0.2u.tar.gz
cd openssl-1.0.2u

echo ">>> Compiling OpenSSL 1.0.2u for Windows..."
./Configure --cross-compile-prefix=$HOST- mingw64 no-shared no-dso
make

echo "--- OPENSSL 1.0.2u READY ---"
