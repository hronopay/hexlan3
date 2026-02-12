#!/bin/bash
set -e
export MXE_PATH=/mnt/mxe
export PATH=$MXE_PATH/usr/bin:$PATH
export HOST=x86_64-w64-mingw32.static

echo "--- STARTING FINAL WINDOWS COMPILATION ---"

# Очистка от старых сборок (на всякий случай)
# make clean || true

# Запуск qmake с нашим спец-файлом
echo ">>> Running qmake..."
$HOST-qmake-qt5 Hexlan-win64.pro \
    "CONFIG+=release" \
    "CONFIG+=static" \
    "DEFINES+=NO_INCLUDE_PWD"

# Сборка
echo ">>> Compiling EXE..."
make -j4

echo "--- BUILD SUCCESSFUL! ---"
echo "Check the 'release' folder for Hexlan-qt.exe"
