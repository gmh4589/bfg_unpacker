import os
from source.codecs.zip_methods import ZipMethods
from source.reaper import Reaper, file_reaper


class Witcher2DZIP(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as dzip:
            magic = dzip.read(4)

            if not self.magic([b'DZIP', ], magic, 'DZIP'):
                return

            version = int.from_bytes(dzip.read(4), byteorder="little")
            file_count = int.from_bytes(dzip.read(4), byteorder="little")
            dzip.seek(0x10)
            dzip.seek(int.from_bytes(dzip.read(4), byteorder="little"))

            for i in range(file_count):
                name_len = int.from_bytes(dzip.read(2), byteorder="little")
                name = dzip.read(name_len).decode("utf-8", errors="ignore").rstrip("\0")
                hash_sum = int.from_bytes(dzip.read(16), byteorder="little")
                offset = int.from_bytes(dzip.read(8), byteorder="little")
                size = int.from_bytes(dzip.read(8), byteorder="little")

                path = os.path.join(self.output_folder, name)
                here = dzip.tell()
                dzip.seek(offset)
                zip_data = dzip.read(size)
                self.file_save(path, zip_data[4:])
                self.unzip(path, ZipMethods.LZF)
                dzip.seek(here)
                self.update_pb(file_count, i + 1, name)
