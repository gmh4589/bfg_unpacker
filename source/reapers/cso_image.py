import os
import struct
import zlib
from source.reaper import Reaper, file_reaper


class CSO(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as f:
            magic = f.read(8)
            header_size = int.from_bytes(f.read(8), byteorder="little")
            data_size = int.from_bytes(f.read(64), byteorder="little")
            block_size = int.from_bytes(f.read(8), byteorder="little")
            ver = int.from_bytes(f.read(1), byteorder="little")
            offsetShift = int.from_bytes(f.read(1), byteorder="little")

            if magic != b'\x43\x49\x53\x4f' or data_size <= 0 or block_size <= 0 or ver != 1:
                return 0
    
            f.seek(header_size if header_size > 0 else 24, 0)
    
            blockCount = data_size // block_size
            tableEntryCount = blockCount + 1
            blockTable = struct.unpack("<" + "I" * tableEntryCount, f.read(tableEntryCount * 4))

            file_name = os.path.basename(self.file_name)
            absPath = os.path.join(self.output_folder, f'{file_name}.iso')

            with open(absPath, "wb") as fw:

                for blockIndex in range(blockCount):
                    tableEntry = blockTable[blockIndex]
                    blockOffset = tableEntry & 0x7FFFFFFF
                    f.seek(blockOffset << offsetShift, 0)
                    isCompressed = (tableEntry & 0x80000000) == 0

                    if isCompressed:
                        nextOffset = blockTable[blockIndex + 1] & 0x7FFFFFFF
                        compBlock = f.read((nextOffset - blockOffset) << offsetShift)
                        # fw.write(rapi.decompInflate(compBlock, block_size, -15))
                        fw.write(zlib.decompress(compBlock, block_size, -15))
                    else:
                        fw.write(f.read(block_size))
