#!/bin/bash
set -e

# 1. Восстановление файла ресурсов (на случай, если был применен sed)
# Если файл был изменен (строки удалены), вернем его через git
# Если изменений не было, команда просто ничего не сделает
if git checkout src/qt/bitcoin.qrc 2>/dev/null; then
    echo ">>> Restored src/qt/bitcoin.qrc to original state."
else
    echo ">>> src/qt/bitcoin.qrc is clean or not tracked."
fi

# 2. Поиск утилиты lrelease
LRELEASE="lrelease"

if ! command -v lrelease &> /dev/null; then
    echo "System 'lrelease' not found. Checking MXE..."
    # Пробуем найти в MXE (имя может отличаться)
    MXE_LRELEASE=$(find /mnt/mxe/usr/bin -name "*-lrelease" | head -n 1)
    
    if [ ! -z "$MXE_LRELEASE" ]; then
        LRELEASE=$MXE_LRELEASE
        echo "Found MXE lrelease: $LRELEASE"
    else
        echo ">>> ERROR: 'lrelease' tool not found!"
        echo ">>> Please install it: sudo apt-get install qttools5-dev-tools"
        exit 1
    fi
fi

# 3. Компиляция переводов
echo ">>> Compiling translations..."
cd src/qt/locale
count=0
for tsfile in *.ts; do
    [ -f "$tsfile" ] || break
    $LRELEASE "$tsfile" -silent
    count=$((count+1))
done
cd ../../..

echo ">>> SUCCESS: Compiled $count translation files (.qm)."
echo ">>> Ready for final build."
