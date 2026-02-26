with open("rpcwallet.cpp", "r") as f:
    lines = f.readlines()
start = -1
for i, line in enumerate(lines):
    if "Value getnewaddress(" in line:
        start = i
        break
if start != -1:
    braces = 0
    started = False
    for i in range(start, len(lines)):
        print(lines[i].rstrip())
        braces += lines[i].count('{')
        braces -= lines[i].count('}')
        if '{' in lines[i]: started = True
        if started and braces == 0: break
else:
    print("Function getnewaddress not found.")
