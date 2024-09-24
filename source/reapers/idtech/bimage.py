import os
from source.reaper import Reaper, file_reaper
from source.ui import localize
from source.codecs.dds_tools import DDSCreator


class Bimage2DDS(Reaper, DDSCreator):

    def run(self):

        with open(self.file_name, 'rb') as bimage:
            magic = bimage.read(4)

            codecs = {
                2: 'R9G9B9E5_SHAREDEXP',
                3: 'B8G8R8A8_UNORM',
                5: 'R8_UNORM',
                6: 'R8G8_UNORM',
                7: 'BC1_UNORM',
                8: 'BC3_UNORM',
                12: 'R16_UNORM',
                0xA: 'BC1_UNORM',
                0xB: 'BC3_UNORM',
                0x17: 'BC7_UNORM'
            }

            # DOOM 3 BFG Edition
            if magic == b'\0' * 4:
                codec_start = 0x13
                xy_start = 0x2c
                data_start = 0x38

            else:
                magic2 = bimage.read(4)

                # DOOM (2016)
                if magic2 == b'\x07MIB':
                    codec_start = 0x20
                    xy_start = 0x32
                    data_start = 0x3e

                # The Evil Within
                elif magic2 == b'\x09MIB':
                    codec_start = 0x24
                    xy_start = 0x10
                    data_start = 0x42

                else:
                    print(localize.not_correct_file.replace('%%', f"{int.from_bytes(magic, 'big')}"))
                    self.update_signal.emit(100, '', '', True)
                    return

            bimage.seek(codec_start)
            codec = int.from_bytes(bimage.read(4), byteorder='little')
            bimage.seek(xy_start)
            image_width = int.from_bytes(bimage.read(4), byteorder='big')
            image_height = int.from_bytes(bimage.read(4), byteorder='big')
            bimage.seek(data_start)
            image_data = bimage.read()

            dds_name = str(os.path.basename(self.file_name).replace('bimage', 'dds'))

            self.dds_save(image_width,
                          image_height,
                          codecs.get(codec, codec),
                          f"{self.output_folder}\\{dds_name}",
                          image_data)

            self.update_pb(1, 1, dds_name)
