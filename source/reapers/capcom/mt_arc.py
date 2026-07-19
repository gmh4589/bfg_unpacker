import os
import zlib
from collections import namedtuple

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

            if not self.magic([b'ARC\0', b'\0CRA', b'\0SFH'], magic, 'MT Framework'):
                return

            if magic == b'\0SFH':
                arc_file.seek(0x10)
                magic = arc_file.read(4)
                platform = 'consoles'

            order = 'little' if magic == b'ARC\0' else 'big'
            version = int.from_bytes(arc_file.read(2), byteorder=order)
            file_count = int.from_bytes(arc_file.read(2), byteorder=order)

            FileData = namedtuple('FileData',
                                  ['name', 'type_hash', 'file_size', 'flags', 'offset'])
            file_data = []
            
            for _ in range(file_count):
                file_data.append(
                    FileData(
                        name = arc_file.read(64).decode("ascii").rstrip("\0"),
                        type_hash = int.from_bytes(arc_file.read(4), byteorder=order),
                        file_size = int.from_bytes(arc_file.read(4), byteorder=order),
                        flags = arc_file.read(4),
                        offset = int.from_bytes(arc_file.read(4), byteorder=order)
                    )
                )

            for i, f in enumerate(file_data):
                arc_file.seek(f.offset if platform == 'pc' else f.offset + 0x10)
                data = arc_file.read(f.file_size)

                if version in (4, 8):

                    try:
                        obj = zlib.decompressobj(-15)
                        data = obj.decompress(data)
                    except zlib.error:
                        data = self.smart_deflate(data)

                elif version == 17:
                    pass
                else:
                    data = zlib.decompress(data)

                ext = self.get_ext(data[:4])
                path = f"{os.path.join(self.output_folder, f.name)}.{ext}"

                self.file_save(path, data)

                if ext == 'tex' and self.setting['Main']['save_original_images'] in ['1', '2']:
                    tex2dds = TEX2DDS()
                    tex2dds.file_name = path
                    tex2dds.output_folder = os.path.dirname(path)
                    tex2dds.run()

                    if self.setting['Main']['save_original_images'] == '1':
                        os.remove(path.replace('dat', 'tex'))

                self.update_pb(file_count, i + 1, f.name)
