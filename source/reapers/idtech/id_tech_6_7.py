import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from collections import namedtuple
from source.ui  import localize
from source.codecs.oodle import OodleDecompress
from source.reapers.idtech.bimage import Bimage2DDS

# TODO: oodle DLL crashes in randomly places with randomly files

class IdReaper(Reaper):

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
                    fc_start = 0x28
                    b1_start = 0x48
                    b2_start = 0x68
                    dt_start = 0x80

                # Indiana Jones and the Grand Circle
                case 0x74:          
                    fc_start = 0x24
                    b1_start = 0x44
                    b2_start = 0x64
                    dt_start = 0x90

                case 0xFFFFFFFF: 
                    # DOOM Eternal
                    if version0 == 0xC:
                        fc_start = 0x24
                        b1_start = 0x34
                        b2_start = 0x64
                        dt_start = 0x84
                    # DOOM: The Dark Ages
                    elif version0 == 0xD:
                        fc_start = 0x24
                        b1_start = 0x34
                        b2_start = 0x54
                        dt_start = 0x78
                    
                case _:
                    print(f"{localize.error_in_file}: {self.file_name}")
                    return

            res_file.seek(fc_start)
            file_count = int.from_bytes(res_file.read(4), byteorder="little")
            res_file.seek(b1_start)
            block_1_offset = int.from_bytes(res_file.read(8), byteorder="little")
            res_file.seek(b2_start)
            block_2_offset = int.from_bytes(res_file.read(8), byteorder="little")
            
            res_file.seek(dt_start)
            FileData = namedtuple('FileData',
                                  ['offset', 'zip_size', 'unzip_size'])
            file_data = []

            for _ in range(file_count):
                res_file.seek(0x30, 1)
                file_data.append(
                    FileData(
                        int.from_bytes(res_file.read(8), byteorder="little"), # Offset
                        int.from_bytes(res_file.read(8), byteorder="little"), # Zip Size
                        int.from_bytes(res_file.read(8), byteorder="little")  # Unzip Size
                    )
                )
                res_file.seek(0x48, 1)

            for i, file in enumerate(file_data):

                res_file.seek(file.offset)
                data = res_file.read(file.zip_size)
                name = f"{self.output_folder}\\{i}.{self.get_ext(data[:4])}"
                
                if file.zip_size != file.unzip_size:
                    unzip_data = oodle.decompress(data, file.unzip_size)
                
                    if type(unzip_data) != bool:
                        data = unzip_data

                self.file_save(name, data)

                if self.setting['Main']['save_original_images'] in ['1', '2']:

                    if 'bimage' in name:
                        bimage2dds = Bimage2DDS()
                        bimage2dds.file_name = name
                        bimage2dds.output_folder = os.path.dirname(name)
                        bimage2dds.run()

                        if self.setting['Main']['save_original_images'] == '1':
                            os.remove(name)
                
                self.update_pb(file_count, i, name)



