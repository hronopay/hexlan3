import os

fpath = "src/qt/overviewpage.cpp"
try:
    with open(fpath, "r", encoding="utf-8") as f:
        code = f.read()

    s_find = "BitcoinUnits::floorWithUnit"
    s_replace = "BitcoinUnits::formatWithUnit"

    if s_find in code:
        code = code.replace(s_find, s_replace)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(code)
        print("Success: floorWithUnit replaced with formatWithUnit in overviewpage.cpp")
    else:
        print("Already patched or target string not found in overviewpage.cpp")
except Exception as e:
    print("Error: " + str(e))
