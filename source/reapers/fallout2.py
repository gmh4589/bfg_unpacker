import zlib
from collections import namedtuple
from icecream import ic
from source.reaper import Reaper, file_reaper

FileData = namedtuple('FileData', ['file_name', 'zipped', 'unzip_size', 'zip_size', 'file_offset'])


class Fallout2(Reaper):

    @file_reaper
    def run(self):

        file_data_list = []

        with open(self.file_name, "rb") as dat_file:
            dat_file.seek(-8, 2)
            data_len = int.from_bytes(dat_file.read(4), byteorder="little")
            dat_file.seek(-data_len - 8, 2)
            file_count = int.from_bytes(dat_file.read(4), byteorder="little")
            ic(file_count, hex(dat_file.tell()))

            for _ in range(file_count):
                file_name_len = int.from_bytes(dat_file.read(4), byteorder="little")
                file_name = dat_file.read(file_name_len).decode('utf-8')
                zipped = int.from_bytes(dat_file.read(1))
                unzip_size = int.from_bytes(dat_file.read(4), byteorder="little")
                zip_size = int.from_bytes(dat_file.read(4), byteorder="little")
                file_offset = int.from_bytes(dat_file.read(4), byteorder="little")
                file_data_list.append(
                    FileData(file_name, zipped, unzip_size, zip_size, file_offset)
                )
            
            for file_data in file_data_list:
                dat_file.seek(file_data.file_offset)
                data = dat_file.read(file_data.zip_size)
                path = f"{self.output_folder}\\{file_data.file_name}"

                if file_data.zipped:
                    data = zlib.decompress(data)
                
                self.file_save(path, data)
                self.update_pb(file_count, file_data_list.index(file_data) + 1, file_data.file_name)
        
