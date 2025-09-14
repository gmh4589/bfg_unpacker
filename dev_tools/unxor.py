
import sys

with open(sys.argv[1], "rb") as f:
    data = f.read(2)
    print(data)

for key in range(1, 256):
    test = bytes(b ^ key for b in data)
    print(f"Key: {key}, Data: {test}")