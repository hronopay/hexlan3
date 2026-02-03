#!/bin/bash

# Создаем папку ТОЛЬКО для OpenSSL и DB
BASE_DIR="$(pwd)/bundled_deps"
echo "Создаю папку для зависимостей: $BASE_DIR"

mkdir -p "$BASE_DIR/openssl/include"
mkdir -p "$BASE_DIR/openssl/lib"
mkdir -p "$BASE_DIR/db48/include"
mkdir -p "$BASE_DIR/db48/lib"

echo "--- 1. Boost пропускаем (он уже в папке libs) ---"

echo "--- 2. Копируем OpenSSL ---"
# Заголовки
if [ -d "/usr/include/openssl" ]; then
    cp -r /usr/include/openssl "$BASE_DIR/openssl/include/"
fi
# Либы (ищем статические .a)
find /usr/lib /usr/local/lib -name "libssl.a" -exec cp {} "$BASE_DIR/openssl/lib/" \; -quit
find /usr/lib /usr/local/lib -name "libcrypto.a" -exec cp {} "$BASE_DIR/openssl/lib/" \; -quit

echo "--- 3. Копируем Berkeley DB 4.8 ---"
# Ищем db_cxx.h и копируем его
find /usr/include -name "db_cxx.h" -exec dirname {} \; | head -n 1 | xargs -I {} cp -r {}/. "$BASE_DIR/db48/include/"
# Ищем библиотеку libdb_cxx-4.8.a
find /usr/lib /usr/local/lib -name "libdb_cxx-4.8.a" -exec cp {} "$BASE_DIR/db48/lib/" \; -quit

echo "ГОТОВО! OpenSSL и DB скопированы в bundled_deps."
