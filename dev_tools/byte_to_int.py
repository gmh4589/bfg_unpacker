
bin_list = [b'\x0E\x14\x74\x75']

for b in bin_list:
    print(int.from_bytes(b, byteorder="little"))

#locres = 1970541582