
bin_list = [b'\x01\0\0\0']

for b in bin_list:
    print(int.from_bytes(b, byteorder="little"))
