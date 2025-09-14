import sys
from source.codecs.oodle import OodleDecompress

oodle = OodleDecompress('oo2core_8_win64.dll')
size = 0x38

with open(sys.argv[1], 'rb') as oodled:
    data = oodled.read()

data = oodle.decompress(data, size)

with open(r"D:\out\unoodled.dat", 'wb') as uno:
    uno.write(data)