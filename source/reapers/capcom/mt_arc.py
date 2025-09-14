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
            platform = 'pc'

            if not self.magic([b'ARC\0', b'\0CRA', b'\0SFH'], magic, 'ARC'):
                return

            if magic == b'\0SFH':
                arc_file.seek(0x10)
                magic = arc_file.read(4)
                platform = 'consoles'

            order = 'little' if magic == b'ARC\0' else 'big'
            version = int.from_bytes(arc_file.read(2), byteorder=order)
            file_count = int.from_bytes(arc_file.read(2), byteorder=order)

            if version in (4, 8):
                # 'unzip_dynamic'
                c_num = ZipMethods.ZLIB_NOERROR
            elif version == 17:
                # TODO: Add support XMem
                ic('XMemDecompress 0x8000')
                c_num = 0
            else:
                # 'zlib_noerror'
                c_num = 1
            
            for i in range(file_count):
                name = arc_file.read(64).decode("ascii").rstrip("\0")
                type_hash = int.from_bytes(arc_file.read(4), byteorder=order)
                file_size = int.from_bytes(arc_file.read(4), byteorder=order)
                flags = arc_file.read(4)
                offset = int.from_bytes(arc_file.read(4), byteorder=order)
                here = arc_file.tell()
                path = os.path.join(self.output_folder, name + '.dat')
                arc_file.seek(offset if platform == 'pc' else offset + 0x10)
                data = arc_file.read(file_size)
                ic(offset, file_size)

                if c_num == 1:
                    data = zlib.decompress(data)
                    self.new_ext = self.get_ext(data[:4])
                    path = path.replace('.dat', f'.{self.new_ext}')

                self.file_save(path, data)

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
                self.update_pb(file_count, i + 1, name)
