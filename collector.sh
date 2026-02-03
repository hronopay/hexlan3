#!/bin/bash

# Создаем папки
BASE_DIR="$(pwd)/bundled_deps"
echo "Создаю папку для зависимостей: $BASE_DIR"

mkdir -p "$BASE_DIR/openssl/include"
mkdir -p "$BASE_DIR/openssl/lib"
mkdir -p "$BASE_DIR/db48/include"
mkdir -p "$BASE_DIR/db48/lib"
mkdir -p "$BASE_DIR/qrencode/include"
mkdir -p "$BASE_DIR/qrencode/lib"

echo "--- 1. Boost пропускаем (он уже в папке libs) ---"

echo "--- 2. Копируем OpenSSL ---"
if [ -d "/usr/include/openssl" ]; then
    cp -r /usr/include/openssl "$BASE_DIR/openssl/include/"
fi
find /usr/lib /usr/local/lib -name "libssl.a" -exec cp {} "$BASE_DIR/openssl/lib/" \; -quit
find /usr/lib /usr/local/lib -name "libcrypto.a" -exec cp {} "$BASE_DIR/openssl/lib/" \; -quit

echo "--- 3. Копируем Berkeley DB 4.8 ---"
find /usr/include -name "db_cxx.h" -exec dirname {} \; | head -n 1 | xargs -I {} cp -r {}/. "$BASE_DIR/db48/include/"
find /usr/lib /usr/local/lib -name "libdb_cxx-4.8.a" -exec cp {} "$BASE_DIR/db48/lib/" \; -quit

echo "--- 4. Копируем QREncode (Полная автономность!) ---"
# Ищем заголовок
find /usr/include /usr/local/include -name "qrencode.h" -exec cp {} "$BASE_DIR/qrencode/include/" \; -quit
# Ищем статическую либу (.a), чтобы не зависеть от .so
find /usr/lib /usr/local/lib -name "libqrencode.a" -exec cp {} "$BASE_DIR/qrencode/lib/" \; -quit

echo "ГОТОВО! Все библиотеки (SSL, DB, QR) теперь лежат локально в bundled_deps."
