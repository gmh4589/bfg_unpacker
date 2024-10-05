import os.path
from source.reaper import Reaper, file_reaper
from source.codecs.dds_tools import DDSCreator
from source.ui import localize


class TEX2DDS(Reaper, DDSCreator):

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

            if not self.magic([b'TEX\x00', ], magic, 'ARC'):
                return

            version = int.from_bytes(tex.read(1))

            if version in (0x9A, 0x9D):  # RE6, RE0, RE1R, RER, RER2
                tex.seek(8)
                f2 = int.from_bytes(tex.read(4), byteorder="little")
                mips_count = f2 & 0x3f
                width = (f2 >> 6) & 0x1fff
                height = (f2 >> 19) & 0x1fff

                # tex.seek(0xC)
                t_count = int.from_bytes(tex.read(1))

                if t_count > 1:
                    break_convert()
                    return

                codec_n = int.from_bytes(tex.read(1))
                codec = codec_list(codec_n)

                tex.seek(0x10)
                start_data = int.from_bytes(tex.read(4), byteorder="little")
                tex.seek(start_data)

            elif version == 0x70:  # RE5
                tex.seek(0xC)
                width = int.from_bytes(tex.read(2), byteorder="little")
                height = int.from_bytes(tex.read(2), byteorder="little")
                tex.seek(0x14)
                codec_n = tex.read(4)
                codec = codec_list(codec_n)
                tex.seek(0x28)
                start_data = int.from_bytes(tex.read(4), byteorder="little")
                tex.seek(start_data)

            elif version == 0xB2:
                tex.seek(8)
                width = int.from_bytes(tex.read(2), byteorder="little")
                height = int.from_bytes(tex.read(2), byteorder="little")
                codec = 'BC7_UNORM'
                tex.seek(0x30)

            else:
                break_convert()
                return

            tex_data = tex.read()

            self.dds_save(
                width=width,
                height=height,
                codec=codec,
                mips=mips_count,
                name=os.path.join(self.output_folder, os.path.basename(tex.name).replace('tex', 'dds')),
                data=tex_data
            )

        self.update_pb(1, 1, self.file_name)
