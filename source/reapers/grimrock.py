from collections import namedtuple
import struct
import zlib
from icecream import ic
from source.reaper import Reaper, file_reaper


class Grimrock(Reaper):
    #TODO: Add decompression for zlib(?) files

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as dat_file:
            magic = dat_file.read(4)

            if not self.magic([b'GRA2', ], magic, '"Legend of Grimrock" grimrock.dat File'):
                return
            
            file_count = int.from_bytes(dat_file.read(4), byteorder="little")
            FileData = namedtuple('FileData',
                                  ['hash', 'offset', 'unzip_size', 'zip_size', 'unk1', 'unk2'])
            file_data = []

            for _ in range(file_count):
                file_data.append(
                    FileData(
                        int.from_bytes(dat_file.read(4), byteorder="little"),
                        int.from_bytes(dat_file.read(4), byteorder="little"),
                        int.from_bytes(dat_file.read(4), byteorder="little"),
                        int.from_bytes(dat_file.read(4), byteorder="little"),
                        int.from_bytes(dat_file.read(2), byteorder="little"),
                        int.from_bytes(dat_file.read(2), byteorder="little")
                    )
                )
            
            for i, file in enumerate(file_data):
                dat_file.seek(file.offset)

                if file.zip_size > 0:
                    data = dat_file.read(file.zip_size)
                    # data = zlib.decompress(data)
                else:
                    data = dat_file.read(file.zip_size)

                file_name = f"{self.output_folder}\\{str(i).rjust(8, '0')}.dat"
                self.file_save(file_name, data)
                self.update_pb(file_count, i, file_name)
