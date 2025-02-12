
import os
import zlib
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.reapers.capcom.tex import TEX2DDS
from source.codecs.zip_methods import ZipMethods


class ARCExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as arc_file:
            magic = arc_file.read(4)

            if not self.magic([b'ARC\x00', b'\x00CRA'], magic, 'ARC'):
                return

            version = int.from_bytes(arc_file.read(2), byteorder="little")
            file_count = int.from_bytes(arc_file.read(2), byteorder="little")

            if version in (4, 8):
                # 'unzip_dynamic'
                c_num = ZipMethods.UNZIP_DYNAMIC
            elif version == 17:
                # TODO: Add support XMem
                ic('XMemDecompress 0x8000')
                c_num = 0
            else:
                # 'zlib_noerror'
                c_num = 1

            for i in range(file_count):
                name = arc_file.read(64).decode("ascii").rstrip("\0")
                type_hash = int.from_bytes(arc_file.read(4), byteorder="little")
                file_size = int.from_bytes(arc_file.read(4), byteorder="little")
                flags = arc_file.read(4)
                offset = int.from_bytes(arc_file.read(4), byteorder="little")
                here = arc_file.tell()
                path = os.path.join(self.output_folder, name + '.dat')
                os.makedirs(os.path.dirname(path), exist_ok=True)
                arc_file.seek(offset)
                data = arc_file.read(file_size)

                if c_num == 1:
                    data = zlib.decompress(data)
                    self.new_ext = self.get_ext(data[:4])
                    path = path.replace('.dat', f'.{self.new_ext}')

                with open(path, 'wb') as new_file:
                    new_file.write(data)

                if c_num > 1:
                    self.unzip(path, c_num, get_ext=True)

                if self.new_ext == 'tex' and self.setting['Main']['save_original_images'] in ['1', '2']:

                    tex2dds = TEX2DDS()
                    tex2dds.file_name = path.replace('.dat', '.tex')
                    tex2dds.output_folder = os.path.dirname(path)
                    tex2dds.run()

                    if self.setting['Main']['save_original_images'] == '1':
                        os.remove(path.replace('dat', 'tex'))

                arc_file.seek(here)
                self.update_pb(file_count, i, name)
