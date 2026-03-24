import os
import re

# 1. Откатываем сломанный код
fpath = "src/qt/overviewpage.cpp"
if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        code = f.read()
    
    # Регулярка аккуратно находит все кривые вставки и заменяет их обратно
    fixed_code = re.sub(r'[ \t]*// HEXLAN: Скрываем обычный баланс.*?updateDarksendProgress\(\);', '    updateDarksendProgress();', code, flags=re.DOTALL)
    
    if code != fixed_code:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(fixed_code)
        print("Success: Bad patch removed from overviewpage.cpp.")
    else:
        print("Info: Bad patch not found (already removed?).")
else:
    print("Error: " + fpath + " not found.")

# 2. Вытаскиваем точные имена из UI
ui_path = "src/qt/forms/overviewpage.ui"
if os.path.exists(ui_path):
    with open(ui_path, "r", encoding="utf-8") as f:
        ui_code = f.read()
    
    widgets = re.findall(r'<widget class="([^"]+)" name="([^"]+)">', ui_code)
    print("\n--- UI Widgets List ---")
    for cls, name in widgets:
        if cls in ["QLabel", "QFrame"] or "Line" in cls:
            print(cls + " : " + name)
else:
    print("Error: " + ui_path + " not found.")
