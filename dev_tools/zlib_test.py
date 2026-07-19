
import zlib

HEADERS = (
    0x081D, 0x085B, 0x0899, 0x08D7,
    0x1819, 0x1857, 0x1895, 0x18D3,
    0x2815, 0x2853, 0x2891, 0x28CF,
    0x3811, 0x384F, 0x388D, 0x38CB,
    0x480D, 0x484B, 0x4889, 0x48C7,
    0x5809, 0x5847, 0x5885, 0x58C3,
    0x6805, 0x6843, 0x6881, 0x68DE,
    0x7801, 0x785E, 0x789C, 0x78DA, None
)

with open(r"D:\unpack\gameresources_patch\generated\image\env\classic_sky1_px.bimage", 'rb') as zf:
    data = zf.read()

def try_param(data, hd=b'', j=0, k=0, i=-1):
    unzip = zlib.decompress(hd + data[j:-k], i)

    with open('test.dat', 'wb') as tf:
        tf.write(unzip)

def try_deflate(data):
    for i in range(-48, 48):
        print(f"Проверяется аргумент {i}...")

        for j in range(16):
            for k in range(16):
                for h in HEADERS:
                    hd = h.to_bytes(2, 'big') if h is not None else b''

                    try:
                        zlib.decompress(hd + data[j:-k], i)
                        print(f"Проканал аргумент: {i}, заголовок {h} и срез {j}:{k}!")
                        break
                    except zlib.error:
                        pass

    try:
        obj = zlib.decompressobj(-15)
        out = obj.decompress(data)
        print(out[:32])
        print(obj.eof)
        print(len(obj.unused_data))
        print("Это Deflate\\ZLIB, но с обрезанным заголовком и EOF!")
    except zlib.error:
        print("Похоже, что это не Deflate\\ZLIB...")

if __name__ == '__main__':
    try_param(data, i=-8)
    