import sys
import zlib

with open(sys.argv[1], 'rb') as zf:
    data = zf.read()


for i in range(-16384, 16384):

    with open(r'F:\out\temp.dat', 'wb') as nf:
        try:
            nf.write(zlib.decompress(data, i))
            print(f"Проканало: {i}!")
            break
        except zlib.error:
            print(f"Не канает: {i}")


