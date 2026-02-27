import os
import re

def patch_file(filepath, pattern, replacement):
    if not os.path.exists(filepath):
        print("File not found:", filepath)
        return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
    if count > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Patched: {} ({} replacements)".format(filepath, count))
    else:
        print("Warning: Pattern not found in", filepath)

gui_file = "src/qt/bitcoingui.cpp"
wallet_file = "src/wallet.cpp"

patch_file(gui_file, r"uiInterface\.NotifyAddressBookChanged", r"NotifyAddressBookChanged")

pattern_deadlock = r"(\s*pwalletMain->TopUpKeyPool\(\);)\s*// Создаем новый правильный дефолтный адрес Native SegWit\s*CPubKey newDefaultKey;\s*if\s*\(pwalletMain->GetKeyFromPool\(newDefaultKey\)\)\s*\{\s*pwalletMain->SetAddressBookName\(newDefaultKey\.GetID\(\),\s*\"\"\);\s*\}"
patch_file(gui_file, pattern_deadlock, r"\1")

pat_set = r"NotifyAddressBookChanged\(this,\s*address,\s*strName,\s*::IsMine\(\*this,\s*address\)\s*!=\s*ISMINE_NO,\s*\(\s*fUpdated\s*\?\s*CT_UPDATED\s*:\s*CT_NEW\s*\)\s*\);"
rep_set = r"NotifyAddressBookChanged(this, dest, strName, ::IsMine(*this, dest) != ISMINE_NO, (fUpdated ? CT_UPDATED : CT_NEW) );"
patch_file(wallet_file, pat_set, rep_set)

pat_del = r"NotifyAddressBookChanged\(this,\s*address,\s*\"\",\s*::IsMine\(\*this,\s*address\)\s*!=\s*ISMINE_NO,\s*CT_DELETED\);"
rep_del = r"NotifyAddressBookChanged(this, dest, \"\", ::IsMine(*this, dest) != ISMINE_NO, CT_DELETED);"
patch_file(wallet_file, pat_del, rep_del)

print("Script execution completed.")
