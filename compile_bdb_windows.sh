#!/bin/bash
set -e
export MXE_PATH=/mnt/mxe
export PATH=$MXE_PATH/usr/bin:$PATH
export HOST=x86_64-w64-mingw32.static

echo ">>> Cleaning old BDB build..."
cd deps_sources/db-4.8.30.NC/build_unix
make clean || true

echo ">>> Re-configuring BDB for Windows (MinGW)..."
# ВАЖНО: --enable-mingw включает Windows-специфичный код
../dist/configure \
    --disable-replication \
    --enable-cxx \
    --enable-mingw \
    --disable-shared \
    --enable-static \
    --host=$HOST

echo ">>> Compiling BDB..."
# Исправляем известную ошибку BDB 4.8 с современным GCC (atomic_init)
# Если сборка упадет, мы добавим патч, но пока попробуем так
make libdb_cxx.a

echo "--- BDB WINDOWS BUILD SUCCESSFUL ---"
