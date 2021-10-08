import os
f = open ("install.txt", "r")
for line in f.read().split("\n"):
    print(line)
    os.system(line)