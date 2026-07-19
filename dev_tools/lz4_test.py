
import lz4.frame as lz4_frame
import lz4.block as lz4_block

lz4_data = b'paste_bytes_here'.split(b'\0')

for data in lz4_data:

    try:
        lz4_block.decompress(data, len(data) * 30)
    except Exception as e:
        print("LZ4 Block error: ", e)

    try:
        lz4_frame.decompress(data, len(data) * 30)
    except Exception as e:
        print("LZ4 Frame error: ", e)
