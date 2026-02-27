import re

with open("qt/walletmodel.cpp", "r") as f:
    content = f.read()

if '#include "segwit_addr.h"' not in content:
    content = '#include "segwit_addr.h"\n' + content

pattern = r'(addressTableModel = new AddressTableModel\(wallet, this\);)'
upgrade_code = r'''// --- HEXLAN EARLY RAM UPGRADE ---
    if (wallet && !wallet->strMnemonic.empty()) {
        std::map<CTxDestination, std::string> upgradedBook;
        for (std::map<CTxDestination, std::string>::iterator it = wallet->mapAddressBook.begin(); it != wallet->mapAddressBook.end(); ++it) {
            CTxDestination dest = it->first;
            if (const CKeyID* kid = boost::get<CKeyID>(&dest)) {
                upgradedBook[WitnessV0KeyHash(*kid)] = it->second;
            } else {
                upgradedBook[dest] = it->second;
            }
        }
        wallet->mapAddressBook = upgradedBook;
    }
    \1'''

if "HEXLAN EARLY RAM UPGRADE" not in content:
    content = re.sub(pattern, upgrade_code, content)
    with open("qt/walletmodel.cpp", "w") as f:
        f.write(content)
    print("Success: RAM Upgrade moved to the exact moment before GUI table creation.")
else:
    print("Notice: WalletModel already patched.")
