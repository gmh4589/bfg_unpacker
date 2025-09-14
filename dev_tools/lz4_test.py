import sys
import lz4.frame as lz4_frame
import lz4.block as lz4_block

with open(sys.argv[1], 'rb') as tf:
    # tf.seek(0x80)
    data = tf.read()

try:
    with open('temp_block.dat', 'wb') as nf:
        nf.write(lz4_block.decompress(data, 1_048_576))
except lz4_block.LZ4BlockError:
    print('Not LZ4 Block')

with open('temp_frame.dat', 'wb') as nf:
    nf.write(lz4_frame.decompress(data, 1_048_576))
