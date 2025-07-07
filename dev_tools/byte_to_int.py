
bin_list = [b'\xFF\xFF\xFF\xFF', b'\xFF\xFF\xFF\x00']

for b in bin_list:
    print(int.from_bytes(b, byteorder="little"))

#locres = 1970541582