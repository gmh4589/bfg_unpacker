
bin_list = [b'FORM']

for b in bin_list:
    print(int.from_bytes(b, byteorder="little"))
