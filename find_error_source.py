import os

fpath = "src/wallet.cpp"
if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "Signing transaction failed" in line:
                print("=== Found error string in " + fpath + " ===")
                # Выводим 10 строк до и 5 после, чтобы понять логику
                for j in range(max(0, i - 10), min(len(lines), i + 5)):
                    print(str(j+1) + ": " + lines[j].rstrip())
                print("---------------------")
else:
    print("File src/wallet.cpp not found.")
