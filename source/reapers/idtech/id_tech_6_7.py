import os
from icecream import ic
from dataclasses import dataclass

import lz4.block as lz4

from source.reaper import Reaper, file_reaper
from collections import namedtuple
from source.ui  import localize
from source.codecs.oodle import OodleDecompress
from source.reapers.idtech.bimage import Bimage2DDS


class ResourcesStruct:

    def __init__(self,
        file_data: object,

        fco: int,   # 0x20
        fll: int,   # 0x38
        fls: int,   # 0x40
        nix: int,   # 0x48
        ffo: int,   # 0x68
        offsets_table: int       # 0x78
                ):

        def get_data(d, offset, long):
            d.seek(offset)
            return int.from_bytes(d.read(long), byteorder="little")

        self.file_count = get_data(file_data, fco, 4)
        self.file_list_size = get_data(file_data, fll, 8)
        self.start_file_list = get_data(file_data, fls, 8)
        self.name_indexes = get_data(file_data, nix, 8)
        self.data_start = get_data(file_data, ffo, 8)
        self.offsets_start = get_data(file_data, offsets_table, 8)


class IdReaper(Reaper):
# TODO: oodle DLL crashes in randomly places with randomly files

    @file_reaper
    def run(self):
        oodle = OodleDecompress()

        with open(self.file_name, "rb") as res_file:
            magic = res_file.read(4)

            if not self.magic([b'IDCL', ], magic, 'idTech 6'):
                return

            version0 = int.from_bytes(res_file.read(4), byteorder="little")
            res_file.seek(0x10)
            version = int.from_bytes(res_file.read(4), byteorder="little")

            match version:

                # Wolfenstein Series
                case 0:
                    res_struct = ResourcesStruct(0x28, 0x48, 0x68, 0x80)

                # Indiana Jones and the Grand Circle
                case 0x74:          
                    res_struct = ResourcesStruct(0x24, 0x44, 0x64, 0x90)
                    # res_struct = ResourcesStruct(res_file, 0x20, 0x38, 0x40, 0x48, 0x68, 0x50)

                # DOOM Eternal and DOOM: The Dark Ages
                case 0xFFFFFFFF: 
                    res_struct = ResourcesStruct(res_file, 0x20, 0x38, 0x40, 0x48, 0x68, 0x50)
                    
                case _:
                    print(f"{localize.error_in_file}: {self.file_name}")
                    return

            res_file.seek(4)
            names_indexes_end = len(res_file.read(res_struct.data_start).split(b'IDCL')[0]) + 4
            names_indexes_offset = names_indexes_end - res_struct.file_count * 16

            # Get file offsets and sizes
            res_file.seek(res_struct.offsets_start)
            FileData = namedtuple('FileData',
                                  ['offset', 'zip_size', 'unzip_size'])
            file_data = []

            for _ in range(res_struct.file_count):
                res_file.seek(0x38, 1)
                file_data.append(
                    FileData(
                        int.from_bytes(res_file.read(8), byteorder="little"), # Offset
                        int.from_bytes(res_file.read(8), byteorder="little"), # Zip Size
                        int.from_bytes(res_file.read(8), byteorder="little")  # Unzip Size
                    )
                )
                res_file.seek(0x40, 1)

            # Get file names
            res_file.seek(res_struct.start_file_list)
            c = int.from_bytes(res_file.read(8), byteorder="little")
            res_file.seek(c * 8, 1)
            names = res_file.read(res_struct.file_list_size - c).split(b'\0')

            res_file.seek(names_indexes_offset)

            NamesData = namedtuple('NamesData',
                                   ['type', 'name'])
            names_data = []

            for _ in range(res_struct.file_count):
                tix = int.from_bytes(res_file.read(8), byteorder="little")
                nix = int.from_bytes(res_file.read(8), byteorder="little")
                # n = {int(k): v for k, v in re.findall(r"\$(\d+)=([^$]+)", names[nix])}

                names_data.append(NamesData(names[tix], names[nix].split(b'$')[0]))

            for i, file in enumerate(file_data):

                res_file.seek(file.offset)
                data = res_file.read(file.zip_size)

                name = f"{names_data[i].name.decode('utf-8')}"
                nm = os.path.basename(name)
                name = name.replace(nm, f"{i}_{nm}")
                file_path = f"{self.output_folder}\\{name}"

                # try:
                #     # Add file index to the end, because this is not real file name, and it can reapet
                #     name = f"{names_data[i].name.decode('utf-8')}_{i}".replace(':', '_')
                # except IndexError:
                #     name = f"{i}.{self.get_ext(data[:4])}"
                
                if file.zip_size != file.unzip_size:
                    unzip_data = oodle.decompress(data, file.unzip_size)
                
                    if type(unzip_data) != bool:
                        data = unzip_data

                self.file_save(file_path, data)

                if self.setting['Main']['save_original_images'] in ['1', '2']:

                    if '.bimage' in name or '.tga' in name:
                        bimage2dds = Bimage2DDS()
                        bimage2dds.file_name = file_path
                        bimage2dds.output_folder = os.path.dirname(file_path)
                        bimage2dds.run()

                        if self.setting['Main']['save_original_images'] == '1':
                            os.remove(file_path)
                
                self.update_pb(res_struct.file_count, i + 1, name)



