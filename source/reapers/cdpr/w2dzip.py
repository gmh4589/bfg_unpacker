from icecream import ic
from collections import namedtuple
from source.codecs.zip_methods import ZipMethods
from source.reaper import Reaper, file_reaper


class Witcher2DZIP(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as dzip:
            magic = dzip.read(4)

            if not self.magic([b'DZIP', ], magic, 'DZIP'):
                return

            ver = int.from_bytes(dzip.read(4), byteorder="little")
            file_count = int.from_bytes(dzip.read(4), byteorder="little")
            dummy = int.from_bytes(dzip.read(4), byteorder="little")
            file_list_start = int.from_bytes(dzip.read(8), byteorder="little")
            dzip.seek(file_list_start)

            FileData = namedtuple('FileData', 
                                  ['file_name', 'hash_sum', 'file_offset', 'file_size'])
            file_data = []

            for _ in range(file_count):
                long = int.from_bytes(dzip.read(2), byteorder="little")

                file_data.append(
                    FileData(
                        dzip.read(long).strip().decode('utf-8', errors='ignore')[:-1],
                        int.from_bytes(dzip.read(16), byteorder="little"),
                        int.from_bytes(dzip.read(8), byteorder="little"),
                        int.from_bytes(dzip.read(8), byteorder="little"),
                    )
                )

            ic(file_data)

            for i, file in enumerate(file_data):
                dzip.seek(file.file_offset)
                self.file_save(f"{self.output_folder}\\{file.file_name}", dzip.read(file.file_size))
                self.update_pb(file_count, i + 1, file.file_name)
