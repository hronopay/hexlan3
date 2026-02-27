import os

filepath = "src/wallet.cpp"
if os.path.exists(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if r'\"\"' in content:
        content = content.replace(r'\"\"', '""')
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print("Successfully fixed quotes in {}".format(filepath))
    else:
        print("Warning: Escaped quotes not found in {}".format(filepath))
else:
    print("File not found: {}".format(filepath))
