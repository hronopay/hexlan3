import os
import re

fpath = "src/qt/forms/overviewpage.ui"
if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Ищем все виджеты типа QFrame
    frames = re.findall(r'<widget class="QFrame" name="([^"]+)">', content)
    print("Found QFrames in overviewpage.ui:")
    for frame in frames:
        print(" - " + frame)
else:
    print("Error: " + fpath + " not found. Check the path.")
