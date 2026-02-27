import os

filepath = "src/qt/bitcoingui.cpp"
if os.path.exists(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    old_line = "NotifyAddressBookChanged(pwalletMain, it->first, it->second, ::IsMine(*pwalletMain, it->first) != ISMINE_NO, CT_DELETED);"
    new_line = "pwalletMain->NotifyAddressBookChanged(pwalletMain, it->first, it->second, ::IsMine(*pwalletMain, it->first) != ISMINE_NO, CT_DELETED);"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print("Successfully patched: {}".format(filepath))
    else:
        print("Warning: Line not found in {}".format(filepath))
else:
    print("File not found: {}".format(filepath))
