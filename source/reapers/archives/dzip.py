
import zlib
from source.reaper import Reaper, file_reaper


class DZIPExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as dzip_file:
            magic = dzip_file.read(4)

            if not self.magic([b'DZ\x03\x00', ], magic, 'DZIP Archive'):
                return

            file_list_offset = int.from_bytes(dzip_file.read(4), byteorder="little")
            file_count = int.from_bytes(dzip_file.read(4), byteorder="little")
            dzip_file.seek(file_list_offset)

            for i in range(file_count):
                offset = int.from_bytes(dzip_file.read(4), byteorder="little")
                zip_size = int.from_bytes(dzip_file.read(4), byteorder="little")
                unzip_size = int.from_bytes(dzip_file.read(4), byteorder="little")
                name_long = int.from_bytes(dzip_file.read(4), byteorder="little")
                dzip_file.seek(0x10, 1)
                name = dzip_file.read(name_long).decode("utf-8").rstrip("\0").split(':')[-1]
                path = self.output_folder + name

                if zip_size > 0:

                    here = dzip_file.tell()
                    dzip_file.seek(offset)
                    decompress_data = zlib.decompress(dzip_file.read(zip_size))
                    self.file_save(path, decompress_data)
                    dzip_file.seek(here)

                self.update_pb(file_count, i + 1, path)
