import os
import io
from icecream import ic
from source.reaper import Reaper, file_reaper
from source.codecs.dds_tools import DDSCreator
from source.ui import localize


class TEX2DDS(Reaper, DDSCreator):
    # TODO: Brocken unzipping some textures from Code Veronica X

    @file_reaper
    def run(self):

        def codec_list(cdc):

            match cdc:
                case 0x14 | 0x19 | b'DXT1':
                    return 'BC1_UNORM'
                case b'DXT3':
                    return 'BC2_UNORM'
                case 0x17 | 0x18 | 0x1F | 0x23 | b'DXT5':
                    return 'BC3_UNORM'
                case b'\x15\0\0\0':
                    return 'B8G8R8A8_UNORM'
                case _:
                    return cdc

        def break_convert():

            print(localize.not_correct_file.replace('%%', 'MT Framework texture'))
            self.update_signal.emit(100, '', '', True)

        with open(self.file_name, 'rb') as tex:

            magic = tex.read(4)
            mips_count = 0
            is_cubemap = 0

            if not self.magic([b'TEX\x00', b'\0XET', b'\0SFH', b'HFS\0'], magic, 'Capcom TEX Texture File'):
                return

            if magic in (b'\0SFH', b'HFS\0'):
                tex.seek(0x10)
                tex = io.BytesIO(tex.read())
                magic = tex.read(4)
            
            version = int.from_bytes(tex.read(1))
            order = 'little' if magic == b'TEX\x00' else 'big'

            if version in (0x9A, 0x9D, 0x20, 0x60):  # RE6, RE0, RE1R, RER, RER2
                tex.seek(3, 1)
                f2 = int.from_bytes(tex.read(4), byteorder=order)
                mips_count = f2 & 0x3f
                width = (f2 >> 6) & 0x1fff
                height = (f2 >> 19) & 0x1fff

                is_cubemap = int.from_bytes(tex.read(1)) == 6

                tex.seek(1 if version in (0x20, 0x60) else 0, 1)

                codec_n = int.from_bytes(tex.read(1))
                codec = codec_list(codec_n)

                tex.seek(0x10) if not is_cubemap else None
                start_data = int.from_bytes(tex.read(4), byteorder=order) if not is_cubemap else 0x10C
                ic(start_data)
                tex.seek(start_data)

            elif version == 0x70:  # RE5
                tex.seek(0xC)
                width = int.from_bytes(tex.read(2), byteorder=order)
                height = int.from_bytes(tex.read(2), byteorder=order)
                tex.seek(0x14)
                codec_n = tex.read(4)
                codec = codec_list(codec_n)
                tex.seek(0x28)
                start_data = int.from_bytes(tex.read(4), byteorder=order)
                tex.seek(start_data)

            elif version == 0xB2:
                tex.seek(8)
                width = int.from_bytes(tex.read(2), byteorder=order)
                height = int.from_bytes(tex.read(2), byteorder=order)
                codec = 'BC7_UNORM'
                tex.seek(0x30)
            
            elif version == 0x20:
                pass

            else:
                break_convert()
                return
            
            ic(version, width, height, codec, mips_count)

            self.dds_save(
                width=width,
                height=height,
                codec=codec,
                mips=mips_count,
                name=f"{self.output_folder}\\{os.path.basename(self.file_name).replace('tex', 'dds')}",
                cubemap = 254 if is_cubemap else 0,
                data=tex.read()
                )
            
        self.update_pb(1, 1, self.file_name)
