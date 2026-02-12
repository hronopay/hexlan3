#!/bin/bash
set -e
export MXE_PATH=/mnt/mxe
export PATH=$MXE_PATH/usr/bin:$PATH
export HOST=x86_64-w64-mingw32.static

cd src/leveldb

echo ">>> Compiling LevelDB (Manual Mode)..."

# Флаги компиляции
# Важно: 
# -DLEVELDB_PLATFORM_WINDOWS - говорим, что мы на Windows
# -DLEVELDB_PLATFORM_NO_SNAPPY - у нас нет библиотеки сжатия Snappy (она и не нужна для кошелька)
CFLAGS="-I. -I./include -DLEVELDB_PLATFORM_WINDOWS -DLEVELDB_PLATFORM_NO_SNAPPY -DWIN32 -D_WIN32 -DOS_WINDOWS -D_REENTRANT -O2 -fno-builtin-memcmp"
CXX="$HOST-g++"
AR="$HOST-ar"

# 1. Собираем список файлов
# Берем все .cc из папок db, table, util
# ИСКЛЮЧАЕМ: тесты (*_test.cc), бенчмарки (*_bench.cc) и файлы окружения (env_*.cc - их выберем вручную)
SOURCES=$(find db table util -name "*.cc" ! -name "*_test.cc" ! -name "*_bench.cc" ! -name "env_*.cc" ! -name "testutil.cc")

# 2. Добавляем системно-зависимые файлы для Windows
# Если есть env_win.cc - берем его, иначе fallback на posix (для MinGW posix тоже часто работает)
if [ -f "util/env_win.cc" ]; then
    echo "  Using Windows environment (env_win.cc)"
    SOURCES="$SOURCES util/env_win.cc"
else
    echo "  Using Posix environment (env_posix.cc)"
    SOURCES="$SOURCES util/env_posix.cc"
fi

# Порт (системные вызовы)
if [ -f "port/port_win.cc" ]; then
    echo "  Using Windows port (port_win.cc)"
    SOURCES="$SOURCES port/port_win.cc"
else
    echo "  Using Posix port (port_posix.cc)"
    SOURCES="$SOURCES port/port_posix.cc"
fi

# 3. Компиляция libleveldb.a
OBJECTS=""
for src in $SOURCES; do
    obj="${src%.cc}.o"
    # echo "  CXX $src" # Раскомментируй, если нужен подробный лог
    $CXX $CFLAGS -c $src -o $obj
    OBJECTS="$OBJECTS $obj"
done

rm -f libleveldb.a
$AR cr libleveldb.a $OBJECTS
echo ">>> Created libleveldb.a"

# 4. Компиляция libmemenv.a
echo ">>> Compiling Memenv..."
MEMENV_SRC=$(find helpers/memenv -name "*.cc" ! -name "*_test.cc")
MEMENV_OBJ=""
for src in $MEMENV_SRC; do
    obj="${src%.cc}.o"
    $CXX $CFLAGS -c $src -o $obj
    MEMENV_OBJ="$MEMENV_OBJ $obj"
done

rm -f libmemenv.a
$AR cr libmemenv.a $MEMENV_OBJ
echo ">>> Created libmemenv.a"

cd ../..
echo "--- LEVELDB BUILD COMPLETE ---"
