
bin_list = [b'MOEG']

for b in bin_list:
    print(int.from_bytes(b, byteorder="little"))
