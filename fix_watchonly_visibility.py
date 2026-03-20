import os

f_wallet = "src/wallet.cpp"
with open(f_wallet, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Позволяем GetBalance возвращать общую сумму (Spendable + WatchOnly)
# или хотя бы гарантируем, что функции доступны. 
# В вашем OverviewPage.cpp уже есть вызовы GetWatchOnlyBalance, 
# нам нужно убедиться, что монеты помечаются правильно.

# 2. Исправляем AvailableCoins, чтобы Watch-Only монеты попадали в список (для Coin Control)
old_avail = 'vCoins.push_back(COutput(pcoin, i, nDepth, mine & ISMINE_SPENDABLE));'
new_avail = 'vCoins.push_back(COutput(pcoin, i, nDepth, (mine & ISMINE_SPENDABLE) || (mine & ISMINE_WATCH_ONLY)));'

if old_avail in code:
    code = code.replace(old_avail, new_avail)
    with open(f_wallet, "w", encoding="utf-8") as f:
        f.write(code)
    print("Success! Watch-only coins will now appear in Coin Control.")
else:
    print("Error: Could not find AvailableCoins logic.")
