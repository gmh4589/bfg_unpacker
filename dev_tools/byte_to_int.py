
bin_list = [b'MES2', b'PES2']

for b in bin_list:
    print(int.from_bytes(b, byteorder="little"))

#locres = 1970541582