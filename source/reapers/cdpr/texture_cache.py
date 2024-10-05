import os
import zlib
from collections import namedtuple

from source.reaper import Reaper, file_reaper
from source.codecs.dds_tools import DDSCreator
from source.codecs.image_tools import BGR2RGB
from source.ui import localize


class TextureCache(Reaper, DDSCreator):
    # TODO: Add cubemap support - вроде добавлено, нужно тестить

    @file_reaper
    def run(self):
        TextureData = namedtuple('TextureData',
                                 ['hash', 'name_offset', 'chunks_offset', 'zip_size', 'unzip_size', 'bpp',
                                  'width', 'height', 'mips', 'sca', 'chunks_block_offset', 'chunks_count', 'dummy1',
                                  'dummy2', 'codec', 'is_cubemap', 'dummy3', 'name'], )
        texture_data = []
        codecs_dict = {0: 'B8G8R8A8_UNORM',
                       7: 'BC1_UNORM',
                       8: 'BC3_UNORM',
                       10: 'BC7_UNORM',
                       13: 'BC2_UNORM',
                       14: 'ATI1',
                       253: 'B8G8R8A8_UNORM',
                       }

        with open(self.file_name, "rb") as w3cache:
            size = os.path.getsize(self.file_name)
            w3cache.seek(size - 20)
            file_count = int.from_bytes(w3cache.read(4), byteorder="little")
            names_len = int.from_bytes(w3cache.read(4), byteorder="little")
            chunk_count = int.from_bytes(w3cache.read(4), byteorder="little")
            start_pos = (file_count * 52) + 32 + names_len + (chunk_count * 4)
            w3cache.seek(size - start_pos)
            chunks = [int.from_bytes(w3cache.read(4), byteorder='little') for _ in range(chunk_count)]
            names = [name.decode('utf-8') for name in w3cache.read(names_len).split(b'\0')]

            for i in range(file_count):
                texture_data.append(
                    TextureData(
                        w3cache.read(4),  # Hash sum
                        w3cache.read(4),  # Offset to file name
                        int.from_bytes(w3cache.read(4), byteorder='little') * 4096,  # Offset to file start
                        int.from_bytes(w3cache.read(4), byteorder='little'),  # Zipped size
                        int.from_bytes(w3cache.read(4), byteorder='little'),  # Unzipped size
                        int.from_bytes(w3cache.read(4), byteorder='little'),  # Bit per pixel
                        int.from_bytes(w3cache.read(2), byteorder='little'),  # Image width
                        int.from_bytes(w3cache.read(2), byteorder='little'),  # Image height
                        int.from_bytes(w3cache.read(2), byteorder='little'),  # Mips count
                        int.from_bytes(w3cache.read(2), byteorder='little'),  # Is cubemap, texture or array
                        int.from_bytes(w3cache.read(4), byteorder='little'),  # Offset in chunks block
                        int.from_bytes(w3cache.read(4), byteorder='little'),  # Chunks count
                        w3cache.read(4),  # Dummy
                        w3cache.read(4),  # Dummy
                        int.from_bytes(w3cache.read(1)),  # Texture codec
                        True if int.from_bytes(w3cache.read(1)) == 3 else False,  # Is cubemap
                        w3cache.read(2),  # Dummy
                        names[i]  # File name
                    )
                )

            for i, t_data in enumerate(texture_data):
                chunk_data = b''
                w3cache.seek(t_data.chunks_offset)
                chunks_count = 1 if t_data.chunks_count == 0 else t_data.chunks_count
                full_name = os.path.join(self.output_folder, t_data.name)
                name, ext = os.path.basename(full_name).lower().split('.')
                codec = codecs_dict.get(t_data.codec, f'Unknown codec - {t_data.codec}')
                # ic(t_data)
                os.makedirs(os.path.dirname(full_name), exist_ok=True)

                # for _ in range(chunks_count):
                w3cache.seek(t_data.chunks_offset)
                zip_size = int.from_bytes(w3cache.read(4), byteorder='little')
                unzip_size = int.from_bytes(w3cache.read(4), byteorder='little')
                x = int.from_bytes(w3cache.read(1))
                # chunk_zip = w3cache.read(t_data.zip_size)
                chunk_zip = w3cache.read(zip_size)
                chunk_data = zlib.decompress(chunk_zip)
                # chunk_data += chunk_zip

                with open(full_name, 'wb') as nf:
                    nf.write(chunk_data)

                if ext in ('xbm', 'png', 'texarray') and self.setting['Main']['save_original_images'] in ['1', '2']:
                    cubemap = 254 if t_data.is_cubemap else 0
                    dds_name = full_name.replace(ext, 'dds')

                    if ext == 'png' and codec != 'BC3_UNORM':
                        chunk_data = BGR2RGB(chunk_data, 'BGRA')
                        codec = 'B8G8R8A8_UNORM'
                        cubemap = 0

                    self.dds_save(t_data.width,
                                  t_data.height,
                                  codec,
                                  dds_name,
                                  chunk_data,
                                  cubemap=cubemap,
                                  # mips=t_data.mips
                                  )

                    if self.setting['Main']['save_original_images'] == '1':
                        os.remove(full_name)

                self.update_pb(file_count, i + 1, t_data.name)
