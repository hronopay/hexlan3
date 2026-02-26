import os

with open("rpcwallet.cpp", "r") as f:
    content = f.read()

# Подключаем наш новый заголовочный файл для SegWit-адресации
if '#include "segwit_addr.h"' not in content:
    content = content.replace('#include "wallet.h"', '#include "wallet.h"\n#include "segwit_addr.h"')

old_return = "return CHexlanAddress(keyID).ToString();"

new_return = """if (!pwalletMain->strMnemonic.empty()) {
        // Заворачиваем ключ в SegWit-структуру и кодируем в Bech32
        WitnessV0KeyHash witKeyId(keyID);
        return EncodeDestination(witKeyId);
    }
    return CHexlanAddress(keyID).ToString();"""

if old_return in content:
    content = content.replace(old_return, new_return)
    with open("rpcwallet.cpp", "w") as f:
        f.write(content)
    print("Success: getnewaddress now issues Bech32 (hx1) addresses for HD wallets!")
else:
    # Запасной вариант на случай, если там CBitcoinAddress
    old_return2 = "return CBitcoinAddress(keyID).ToString();"
    new_return2 = new_return.replace("CHexlanAddress", "CBitcoinAddress")
    if old_return2 in content:
        content = content.replace(old_return2, new_return2)
        with open("rpcwallet.cpp", "w") as f:
            f.write(content)
        print("Success: getnewaddress now issues Bech32 (hx1) addresses for HD wallets!")
    else:
        print("Error: Could not find the return statement in getnewaddress.")
