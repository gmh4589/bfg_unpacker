import os
from dataclasses import dataclass

from source.reaper import Reaper, file_reaper
from source.ui import localize
from source.codecs.dds_tools import DDSCreator

@dataclass
class BimageStructure:
    codec_start: int
    x_start: int
    y_start: int
    data_start: int


class Bimage2DDS(Reaper, DDSCreator):
    # TODO: Add support other games
    # ❌ DeathLoop
    # ❌ Dishonored 2
    # ❌ Dishonored: Death of the Outsider
    # ✔️ DOOM 3: BFG Edition
    # ✔️ DOOM (2016) 
    # ❌ DOOM: Eternal
    # ❌ Doom: The Dark Ages
    # ❌ DOOM VFR
    # ❌ Indiana Jones and the Great Circle
    # ✔️ Rage 
    # ✔️ The Evil Within
    # ❌ The Evil Within 2
    # ❌ Wolfenstein II: The New Colossus
    # ❌ Wolfenstein: Cyberpylot
    # ❌ Wolfenstein: The New Order
    # ❌ Wolfenstein: The Old Blood
    # ❌ Wolfenstein: Youngblood


    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as bimage:
            magics = [bimage.read(4) for _ in range(4)]

            for i, magic in enumerate(magics):

                if b'BIM' in magic or b'MIB' in magic:
                    version = bytearray(magic)
                    offset = (i + 1) * 4
                    break
            
            else:
                print('Unsupported BIMAGE type...')
                return

            order = 'little' if version[0] == b'B' else 'big'
            ver = version[-1] if order == 'little' else version[0]

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

            match ver:
                case 0x7: # DOOM (2016), Rage
                    bim_struct = BimageStructure(0x18, 0x2A, 0x2E, 0x36)
                # case 0x8: # The Evil Within 2
                #     bim_struct = BimageStructure(0x18, 0xB, 0xF)
                case 0x9: # The Evil Within
                    bim_struct = BimageStructure(0x1C, 0x8, 0xC, 0x3A)
                case 0xA: # DOOM 3 BFG Edition
                    bim_struct = BimageStructure(0x7, 0xC, 0x20, 0x2C)
                # case 0x16: # DOOM: Eternal
                #     bim_struct = BimageStructure(0x2d, 0x47, 0x4b, 0xf3)
                # case 0x1A: # DOOM: The Dark Ages
                #     bim_struct = BimageStructure(0x2d, 0x47, 0x4b, 0x214)

                case _:
                    print('Unsupported BIMAGE type...')
                    return


            bimage.seek(bim_struct.codec_start + offset)
            codec = int.from_bytes(bimage.read(1))
            bimage.seek(bim_struct.x_start + offset)
            image_width = int.from_bytes(bimage.read(4), byteorder=order)
            bimage.seek(bim_struct.y_start + offset)
            image_height = int.from_bytes(bimage.read(4), byteorder=order)
            bimage.seek(bim_struct.data_start + offset)
            image_data = bimage.read()

            dds_name = str(os.path.basename(self.file_name).replace('bimage', 'dds'))

            self.dds_save(image_width,
                          image_height,
                          codecs.get(codec, codec),
                          f"{self.output_folder}\\{dds_name}",
                          image_data)

            self.update_pb(1, 1, dds_name)
