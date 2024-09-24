import os
import zlib
from icecream import ic
from collections import namedtuple
from source.ui.custom_ui import CustomDialog

from source.reaper import Reaper, file_reaper
from source.ui import localize
from source.codecs.dds_tools import DDSCreator


class BethesdaArchive(Reaper):
    # TODO:
    #  Add all DDS codec support
    #  Add cubemap DDS support
    #  Add GNMF support
    #  Fallout 4, Fallout 76 -> Don't work tiny TXT files from zipped animation archives
    #  Starfield -> maybe use other compression method

    @file_reaper
    def run(self):

        codec_dict = {10: 'B8G8R8A8_UNORM_SRGB',
                      11: 'B8G8R8A8_UNORM_SRGB',
                      28: 'B8G8R8A8_UNORM_SRGB',
                      29: 'B8G8R8A8_UNORM_SRGB',
                      61: 'R8_UNORM',
                      62: 'R8_UINT',
                      63: 'R8_SNORM',
                      64: 'R8_SINT',
                      65: 'A8_UNORM',
                      71: 'BC1_UNORM',
                      72: 'BC1_UNORM',
                      74: 'BC2_UNORM',
                      75: 'BC2_UNORM_SRGB',
                      77: 'BC3_UNORM',
                      78: 'BC3_UNORM',
                      80: 'BC4_UNORM',
                      81: 'BC4_SNORM',
                      83: 'BC5_UNORM',
                      84: 'BC5_SNORM',
                      87: 'B8G8R8A8_UNORM',
                      88: 'B8G8R8A8_UNORM',
                      95: 'BC6H_UF16',
                      96: 'BC6H_SF16',
                      98: 'BC7_UNORM',
                      99: 'BC7_UNORM',
                      100: 'AYUV',
                      101: 'Y410',
                      102: 'Y416',
                      108: 'Y210',
                      109: 'Y216',
                      }

        with open(self.file_name, "rb") as ba2:
            magic = ba2.read(4)
            version = int.from_bytes(ba2.read(4), byteorder="little")
            data_type = ba2.read(4)

            if (version not in (1, 2, 3, 7, 8) or
                    data_type not in (b'GNRL', b'DX10', b'GNMF') or
                    magic != b'BTDX'):
                print('Unsupported file!')
                return

            match data_type:
                case b'GNRL':
                    offset_block_size = 8
                case b'DX10':
                    offset_block_size = 4
                case b'GNMF':
                    CustomDialog(title='INFO',
                                 text=f'Work in progress!').exec()
                    return

            file_count = int.from_bytes(ba2.read(4), byteorder="little")
            file_names_list_offset = int.from_bytes(ba2.read(4), byteorder="little")
            here = ba2.tell()

            self.update_signal.emit(0, '', f'{localize.wait}...', False)

            ba2.seek(file_names_list_offset)
            file_names = []

            for i in range(file_count):
                name_len = int.from_bytes(ba2.read(2), byteorder="little")
                file_names.append(ba2.read(name_len).decode('utf-8', errors='ignore'))

            ba2.seek(here)
            FilesData = namedtuple('FilesData',
                                   ['name', 'offset', 'size'])
            files_data = []
            DDSData = namedtuple('DDSData',
                                 ['x_size', 'y_size', 'mip_count', 'dds_format', 'flags', 'tiled'])
            dds_data = []
            ba2.seek(8 if version == 2 else 0, 1)

            for j in range(file_count):
                ba2.seek(0x10, 1)
                mips = int.from_bytes(ba2.read(2), byteorder="big") - 1
                dummy = int.from_bytes(ba2.read(2), byteorder="little")

                if data_type == b'DX10':
                    dds_data.append(
                        DDSData(
                            int.from_bytes(ba2.read(2), byteorder="little"),  # Image Width
                            int.from_bytes(ba2.read(2), byteorder="little"),  # Image Height
                            int.from_bytes(ba2.read(1), byteorder="little"),  # Mip count
                            int.from_bytes(ba2.read(1), byteorder="little"),  # Image codec
                            int.from_bytes(ba2.read(1), byteorder="little"),  # Flags
                            int.from_bytes(ba2.read(1), byteorder="little")   # Is tiled
                        )
                    )

                offset = int.from_bytes(ba2.read(4), byteorder="little")
                ba2.seek(offset_block_size, 1)
                size = int.from_bytes(ba2.read(4), byteorder="little")

                if data_type == b'DX10':

                    for z in range(mips):
                        ba2.seek(0x14, 1)
                        size += int.from_bytes(ba2.read(4), byteorder="little")

                    ba2.seek(8, 1)

                files_data.append(
                    FilesData(
                        file_names[j],
                        offset,
                        size
                    )
                )

            for k, file in enumerate(files_data):
                ic(file.offset)
                ba2.seek(file.offset)
                data = ba2.read(file.size)
                folder_path = os.path.dirname(file.name)
                full_path = f"{self.output_folder}\\{dds_data[k].dds_format}_{file.name}"
                os.makedirs(f'{self.output_folder}\\{folder_path}', exist_ok=True)

                if data_type == b'DX10':
                    # self.unzip(full_path, 170)
                    data = zlib.decompress(data)

                    codec = codec_dict.get(dds_data[k].dds_format, f'Unknown codec - {dds_data[k].dds_format}')
                    dds = DDSCreator()
                    dds.dds_save(dds_data[k].y_size,
                                 dds_data[k].x_size,
                                 codec,
                                 full_path.lower(),
                                 data,
                                 mips=dds_data[k].mip_count
                                 )

                else:

                    if data[:2] in (b'\x78\x9C', b'\x48\xC7'):

                        try:
                            data = zlib.decompress(data)
                        except zlib.error:
                            # showinfo(title='INFO', message=f'Error in file {full_path}\n{data[:2]}')
                            pass

                    with open(full_path, 'wb') as new_file:
                        new_file.write(data)

                self.update_pb(file_count, k, file.name)
