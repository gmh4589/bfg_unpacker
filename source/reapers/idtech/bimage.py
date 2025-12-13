import os
from source.reaper import Reaper, file_reaper
from source.ui import localize
from source.codecs.dds_tools import DDSCreator


class Bimage2DDS(Reaper, DDSCreator):
    # TODO: Add support other games
    # The Evil Within 2
    # Doom: The Dark Ages
    # Indiana Jones and the Great Circle
    # Wolfenstein: The New Order
    # Wolfenstein: The Old Blood
    # Dishonored 2
    # Dishonored: Death of the Outsider
    # Deathloop
    # Wolfenstein II: The New Colossus
    # DOOM VFR
    # Wolfenstein: Youngblood
    # Wolfenstein: Cyberpylot


    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as bimage:
            magic = bimage.read(4)

            codecs = {
                2:      'R9G9B9E5_SHAREDEXP',
                3:      'B8G8R8A8_UNORM',
                5:      'R8_UNORM',
                6:      'R8G8_UNORM',
                7:      'BC1_UNORM',
                8:      'BC3_UNORM',
                9:      'BC4_UNORM',
                0xA:    'BC1_UNORM',
                0xB:    'BC3_UNORM',
                0xC:    'R16_UNORM',
                0x17:   'BC7_UNORM'
            }

            # DOOM 3 BFG Edition
            if magic == b'\0' * 4:
                codec_start = 0x13
                x_start = 0x18
                y_start = 0x1C
                data_start = 0x38
                order = 'big'

            # DOOM: Eternal
            elif magic == b'BIM\x15':
                codec_start = 0x2D
                x_start = 0x47
                y_start = 0x4B
                data_start = 0xF3
                order = 'little'

            else:
                magic2 = bimage.read(4)

                # DOOM (2016)
                if magic2 == b'\x07MIB':
                    codec_start = 0x20
                    x_start = 0x32
                    y_start = 0x36
                    data_start = 0x3e
                    order = 'big'

                # The Evil Within
                elif magic2 == b'\x09MIB':
                    codec_start = 0x24
                    x_start = 0x10
                    y_start = 0x14
                    data_start = 0x42
                    order = 'big'

                # The Evil Within 2
                # elif magic2 == b'BIM\x08':
                #     codec_start = 0x18
                #     xy_start = 0xB
                #     data_start = 0x3e

                else:
                    print(localize.not_correct_file.replace('%%', f"{int.from_bytes(magic, 'big')}"))
                    self.update_signal.emit(100, '', '', True)
                    return

            bimage.seek(codec_start)
            codec = int.from_bytes(bimage.read(1))
            bimage.seek(x_start)
            image_width = int.from_bytes(bimage.read(4), byteorder=order)
            bimage.seek(y_start)
            image_height = int.from_bytes(bimage.read(4), byteorder=order)
            bimage.seek(data_start)
            image_data = bimage.read()

            dds_name = str(os.path.basename(self.file_name).replace('bimage', 'dds'))

            self.dds_save(image_width,
                          image_height,
                          codecs.get(codec, codec),
                          f"{self.output_folder}\\{dds_name}",
                          image_data)

            self.update_pb(1, 1, dds_name)
