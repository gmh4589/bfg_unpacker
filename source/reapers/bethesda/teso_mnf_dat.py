import zlib
import io
from tkinter.messagebox import showinfo
from collections import namedtuple

from icecream import ic
from source.reaper import Reaper, file_reaper
from source.codecs.oodle import OodleDecompress
from source.ui import localize


#TODO: Working only with single volume archives. Add multivol archive support
class TesOnline(Reaper):
    
    @file_reaper
    def run(self):
        self.oodle_dec = OodleDecompress()

        with open(self.file_name, "rb") as mnf_file:
            magic = mnf_file.read(4)
            only_name = self.file_name.replace('.mnf', '')
            vols = []
            ic(magic, b'MES2', magic == b'MES2')

            if not self.magic([b'MES2', ], magic, 'Hero Engine MNF\\DAT'):
                return
            
            if magic == b'PES2':
                showinfo(title=localize.error, message="Select a MNF file!")
                print("Select a MNF file!")
                return

            version = int.from_bytes(mnf_file.read(2), byteorder="little")
            vol_count = int.from_bytes(mnf_file.read(2), byteorder="little")
            
            for _ in range(vol_count):
                vols.append(int.from_bytes(mnf_file.read(2), byteorder="little"))

            unk1 = int.from_bytes(mnf_file.read(4), byteorder="little")
            data_size = int.from_bytes(mnf_file.read(4), byteorder="little")
            data_blocks_count = int.from_bytes(mnf_file.read(2), byteorder="big")
            unk3 = int.from_bytes(mnf_file.read(4), byteorder="big")
            unk4 = int.from_bytes(mnf_file.read(4), byteorder="big")
            file_count = int.from_bytes(mnf_file.read(4), byteorder="big")
            VolData = namedtuple('VolData', ['file_count', 'file_io'])
            vol_data = []

            for _ in range(vol_count):
                vol_fc = int.from_bytes(mnf_file.read(4), byteorder="big")
                vol_data.append(VolData(vol_fc, None))

            file_data = []

            for _ in range(data_blocks_count):
                ic(hex(mnf_file.tell()))
                unzip_size = int.from_bytes(mnf_file.read(4), byteorder="big")
                zip_size = int.from_bytes(mnf_file.read(4), byteorder="big")
                data = mnf_file.read(zip_size)

                if zip_size != unzip_size:
                    data = zlib.decompress(data)
                
                file_data.append(data)
                self.file_save(f"{self.output_folder}\\{_}.dat", data)
            
            if data_blocks_count == 0:

                with open(f"{only_name}0000.dat", 'wb') as dat_file:
                    dat_file.seek(0x12)
                    file_data.append(dat_file.read())
            
            # Get files data
            file_data_io = io.BytesIO(file_data[-1])
            FileData = namedtuple("FileData",
                                  ['unzip_size', 'zip_size', 'hash', 'offset', 'vol_num', 'zip_method'])
            file_data = []

            for _ in range(file_count):
                file_data.append(
                    FileData(
                        unzip_size= int.from_bytes(file_data_io.read(4), byteorder="little"),
                        zip_size=   int.from_bytes(file_data_io.read(4), byteorder="little"),
                        hash=       int.from_bytes(file_data_io.read(4), byteorder="little"),
                        offset=     int.from_bytes(file_data_io.read(4), byteorder="little"),
                        vol_num=    int.from_bytes(file_data_io.read(2), byteorder="little"),
                        zip_method= int.from_bytes(file_data_io.read(2), byteorder="little"),
                    )
                )

            cur_file = 0

            for i in range(vol_count):
                vol_name = f"{only_name}{str(i).ljust(4, '0')}.dat"
                file_io = open(vol_name, 'rb')
                    
                for file in file_data:
                    vn = file.vol_num

                    if vn == i:
                        file_io.seek(file.offset)
                        data = file_io.read(file.zip_size)
                        cur_file += 1

                        if file.zip_size != file.unzip_size:
                            data = self.oodle_dec.decompress(data, file.unzip_size)

                        fname = f"{str(cur_file).rjust(8, '0')}.{self.get_ext(data[0x1EF:0x1EF+4])}"
                        self.file_save(f"{self.output_folder}\\{fname}", data[0x1EF:])
                        self.update_pb(file_count, cur_file, fname)
                
                file_io.close()

