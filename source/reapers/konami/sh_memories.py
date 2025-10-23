
import zlib
from icecream import ic
from collections import namedtuple
from source.reaper import Reaper, file_reaper
from source.codecs.zip_methods import ZipMethods


class ARCExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as arc_file:
            magic = arc_file.read(4)

            if not self.magic([b'\x10\xFA\x00\x00'], magic, 'Silent Hill: Shattered Memories ARC'):
                return

            file_count = int.from_bytes(arc_file.read(4), byteorder="little")
            satrt_data = int.from_bytes(arc_file.read(4), byteorder="little")
            zeroes = int.from_bytes(arc_file.read(4), byteorder="little")
            archive_hash = int.from_bytes(arc_file.read(4), byteorder="little")
            FileData = namedtuple('FileData',
                                  ['offset', 'zip_size', 'unzip_size', 'hash_summ'])
            file_data = []

            for i in range(file_count):
                
                file_data.append(
                    FileData(
                        int.from_bytes(arc_file.read(4), byteorder="little"), # Offset
                        int.from_bytes(arc_file.read(4), byteorder="little"), # Zip Size
                        int.from_bytes(arc_file.read(4), byteorder="little"), # Unzip Size
                        int.from_bytes(arc_file.read(4), byteorder="little")  # Hash Summ 
                    )
                )

            for i, file in enumerate(file_data):
                name = f'{str(i).rjust(8, '0')}.dat'
                arc_file.seek(file.offset)
                data = arc_file.read(file.zip_size)

                if data[:2] == b'\x10\xFA':
                    # self.file_save(f"{self.output_folder}\\raw_{name}", data)
                    data = data[0x40:]

                if file.unzip_size != file.zip_size:

                    try:
                        data = zlib.decompress(data)
                    except zlib.error:
                        self.file_save(f"{self.output_folder}\\{name}", data)
                        self.unzip(f"{self.output_folder}\\{name}", ZipMethods.ZLIB_NOERROR)

                ic(data[:4])
                self.file_save(f"{self.output_folder}\\{name}", data)

                self.update_pb(file_count, i + 1, name)
