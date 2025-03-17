
bin_list = [b'RIFF']

for b in bin_list:
    print(int.from_bytes(b, byteorder="little"))
