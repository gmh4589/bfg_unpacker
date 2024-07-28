import os
from icecream import ic
from collections import namedtuple
from tkinter.messagebox import showinfo

from source.reaper import Reaper, file_reaper
from source.ui import localize
from source.codecs.image_tools import dds_save


class BethesdaArchive(Reaper):
    # TODO: Troubles with custom archives
    # TODO: Add all DDS codec support

    @file_reaper
    def run(self):

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
                    offset_block_size = 12
                case b'DX10':
                    offset_block_size = 8
                case b'GNMF':
                    offset_block_size = 12

            match version:
                case 2:
                    zeros = 8
                case _:
                    zeros = 0

            file_count = int.from_bytes(ba2.read(4), byteorder="little")
            file_names_list_offset = int.from_bytes(ba2.read(4), byteorder="little")
            here = ba2.tell()

            ba2.seek(file_names_list_offset)
            file_names = []

            for i in range(file_count):
                name_len = int.from_bytes(ba2.read(2), byteorder="little")
                name = ba2.read(name_len).decode('utf-8')
                print(name)
                file_names.append(name)

            ba2.seek(here)
            FilesData = namedtuple('FilesData',
                                   ['name', 'offset', 'size'])
            files_data = []
            DDSData = namedtuple('DDSData',
                                 ['x_size', 'y_size', 'mip_count', 'dds_format', 'flags', 'tiled'])
            dds_data = []
            ba2.seek(zeros, 1)

            for j in range(file_count):
                ba2.seek(0x10, 1)
                mips = int.from_bytes(ba2.read(2), byteorder="big") - 1
                dummy = int.from_bytes(ba2.read(2), byteorder="little")

                if data_type == b'DX10':
                    x_size = int.from_bytes(ba2.read(2), byteorder="little")
                    y_size = int.from_bytes(ba2.read(2), byteorder="little")
                    mip_count = int.from_bytes(ba2.read(1), byteorder="little")
                    dds_format = int.from_bytes(ba2.read(1), byteorder="little")
                    flags = int.from_bytes(ba2.read(1), byteorder="little")
                    tiled = int.from_bytes(ba2.read(1), byteorder="little")
                    dds_data.append(DDSData(x_size, y_size, mip_count, dds_format, flags, tiled))

                offset = int.from_bytes(ba2.read(offset_block_size), byteorder="little")
                size = int.from_bytes(ba2.read(4), byteorder="little")

                if data_type == b'DX10':

                    for z in range(mips):
                        ba2.seek(0x14, 1)
                        size += int.from_bytes(ba2.read(4), byteorder="little")

                    ba2.seek(8, 1)
                    ic(hex(ba2.tell()), file_names[j], x_size, y_size, mip_count,
                       dds_format, flags, tiled, size, offset)

                files_data.append(FilesData(file_names[j], offset, size))

            for k, file in enumerate(files_data):
                ic(file.offset)
                ba2.seek(file.offset)
                data = ba2.read(file.size)
                folder_path = os.path.dirname(file.name)
                full_path = f"{self.output_folder}\\{file.name}"
                os.makedirs(f'{self.output_folder}\\{folder_path}', exist_ok=True)

                with open(full_path, 'wb') as new_file:
                    new_file.write(data)

                if data_type == b'DX10':
                    self.unzip(full_path, 170)

                    match dds_data[k].dds_format:
                        case 71 | 72:
                            codec = 'BC1_UNORM'
                        case 77 | 78:
                            codec = 'BC3_UNORM'
                        case 80:
                            codec = 'BC4_UNORM'
                        case 83:
                            codec = 'BC5_UNORM'
                        case 84:
                            codec = 'BC5_SNORM'
                        case 87 | 88:
                            codec = 'B8G8R8A8_UNORM'
                        case _:
                            # TODO: None localized text
                            showinfo('INFO',
                                     f'Unknown DDS type {dds_data[k].dds_format}\n'
                                     f'In file {file.name}\n'
                                     f'{localize.archives[:-1]}: {self.file_name}\n'
                                     f'File was save as B8G8R8A8_UNORM')
                            codec = 'B8G8R8A8_UNORM'

                    with open(full_path, 'rb') as temp_dds:
                        image_data = temp_dds.read()

                    dds_save(dds_data[k].y_size,
                             dds_data[k].x_size,
                             codec,
                             full_path.lower().replace('.dds', ''),
                             image_data)

                ic(file.name)
                print(f'{k}/{file_count}: {localize.saving} - {file.name}...')
                self.update_signal.emit(int(100 / file_count * k), f'{k + 1}/{file_count}',
                                        f'{localize.saving} - {file.name}...', False)

        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
