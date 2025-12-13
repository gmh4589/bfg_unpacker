import zlib
import io
import os
from collections import namedtuple
from source.reaper import Reaper, file_reaper

class WolfSPK(Reaper):

    @staticmethod
    def get_coef(d):
        coef = 4 - (d % 4)
        return coef if coef != 4 else 0

    @file_reaper
    def run(self):
        
        FileData = namedtuple('FileData',
                            ['file_name', 'zip_size', 'unzip_size', 'vol'])
        file_list = []
        streams = []
        current_vol = 0

        with open(self.file_name, "rb") as spk_file:
            magic = spk_file.read(4)
            file_size = os.path.getsize(spk_file.name)

            if not self.magic([b'\x2C\1\0\0', ], magic, 'Wolfenstein 2009 SPK File'):
                return

            while spk_file.tell() < file_size:    
                file_type = spk_file.read(4)
                unzip_size = int.from_bytes(spk_file.read(4), byteorder="little")
                zip_size = int.from_bytes(spk_file.read(4), byteorder="little")
                data = spk_file.read(zip_size)

                if zip_size != unzip_size:
                    data = zlib.decompress(data)

                # self.file_save(f"{self.output_folder}\\{os.path.basename(spk_file.name)}.{current_vol}", data)

                data_stream = io.BytesIO(data)
                fc = int.from_bytes(data_stream.read(4), byteorder="little")

                for _ in range(fc):
                    name = self.get_name(data_stream)
                    zip_size = int.from_bytes(data_stream.read(4), byteorder="little")
                    unzip_size = int.from_bytes(data_stream.read(4), byteorder="little")
                    coef = self.get_coef(zip_size)

                    file_list.append(FileData(name, 
                                              zip_size + coef, 
                                              unzip_size + coef, 
                                              current_vol))

                data_stream.seek(self.get_coef(data_stream.tell()), 1)
                streams.append(io.BytesIO(data_stream.read()))
                current_vol += 1
                
            file_count = len(file_list)
            
            for i, file in enumerate(file_list):
                data = streams[file.vol].read(file.zip_size)

                if file.zip_size != file.unzip_size:
                    data = zlib.decompress(data)

                ext = self.get_ext(data[:4])
                self.file_save(f"{self.output_folder}\\{file.file_name}.{ext}", data)
                self.update_pb(file_count, i, file.file_name)
            
