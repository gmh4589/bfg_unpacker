
from collections import namedtuple
import io

from source.reaper import Reaper, file_reaper

Folder = namedtuple('Folder', ['folder_name', 'files'])
File = namedtuple('File', ['file_name', 'file_offset', 'zip_size', 'unzip_size', 'zipped'])


class Fallout1(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as dat_file:
            folder_count = int.from_bytes(dat_file.read(4), byteorder="big")
            dat_file.seek(0x10 if folder_count == 1 else 0x12)
            folder_list = []
            all_files = 0
            current = 0
            folder_count = folder_count - 1 if folder_count > 1 else 1

            for _ in range(folder_count):
                fol_name_long = int.from_bytes(dat_file.read(1))
                folder_name = dat_file.read(fol_name_long).decode('utf-8')
                folder_name = Folder(folder_name, [])
                folder_list.append(folder_name)
            
            for folder in folder_list:
                files_in_folder = int.from_bytes(dat_file.read(4), byteorder="big")
                dat_file.seek(0xC, 1)
                all_files += files_in_folder

                for _ in range(files_in_folder):
                    name_len = int.from_bytes(dat_file.read(1))
                    name = dat_file.read(name_len).decode('utf-8')
                    zipped = True if int.from_bytes(dat_file.read(4), byteorder="big") == 0x40 else False
                    offset = int.from_bytes(dat_file.read(4), byteorder="big")
                    size = int.from_bytes(dat_file.read(4), byteorder="big")
                    zip_size = int.from_bytes(dat_file.read(4), byteorder="big")
                    file_data = File(name, offset, zip_size, size, zipped)
                    folder.files.append(file_data)

            for folder in folder_list:

                for file in folder.files:
                    current += 1
                    dat_file.seek(file.file_offset)
                    data = dat_file.read(file.zip_size)
                    path = f"{self.output_folder}\\{folder.folder_name}\\{file.file_name}"

                    if file.zipped:
                        data = self.lzss_decompress_fallout(data)

                    self.file_save(path, data)

                    self.update_pb(all_files, current, file.file_name)
    
    @staticmethod
    def lzss_decompress_fallout(data: bytes) -> bytes:

        DICT_SIZE = 4096
        MIN_MATCH = 3
        MAX_MATCH = 18

        output = bytearray()
        dictionary = bytearray([0x20] * DICT_SIZE)
        di = DICT_SIZE - MAX_MATCH  
        stream = io.BytesIO(data)

        while True:
            n_bytes = stream.read(2)
            if len(n_bytes) < 2:
                break
            n = int.from_bytes(n_bytes, byteorder='little', signed=True)
            if n == 0:
                break

            if n < 0:
                n = -n
                raw = stream.read(n)
                output.extend(raw)
                continue

            dictionary[:] = [0x20] * DICT_SIZE
            di = DICT_SIZE - MAX_MATCH

            bytes_read = 0

            while bytes_read < n:
                fl_byte = stream.read(1)

                if not fl_byte:
                    break

                fl = fl_byte[0]
                flag_mask = 1

                for _ in range(8):

                    if bytes_read >= n:
                        break

                    if fl & flag_mask:
                        literal = stream.read(1)

                        if not literal:
                            continue
                        
                        b = literal[0]
                        output.append(b)
                        dictionary[di] = b
                        di = (di + 1) % DICT_SIZE
                        bytes_read += 1
                    else:
                        pair = bytearray(stream.read(2))

                        if len(pair) < 2:
                            continue

                        do = pair[0]
                        l = pair[1]

                        do |= (l & 0xF0) << 4
                        l = (l & 0x0F) + MIN_MATCH

                        for _ in range(l):
                            byte = dictionary[do % DICT_SIZE]
                            output.append(byte)
                            dictionary[di] = byte
                            di = (di + 1) % DICT_SIZE
                            do += 1

                        bytes_read += 2

                    flag_mask <<= 1 

        return bytes(output)

