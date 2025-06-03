import struct
import json
import zlib
import os

from icecream import ic
from source.reaper import Reaper, file_reaper
from source.ui import localize


class Locres2TXT(Reaper):

    @file_reaper
    def run(self):
        
        with open(self.file_name, 'rb') as locres:
            magic = locres.read(4)
            strings = []
            strings_json = {'type': 'locres'}

            if not self.magic([b'\x0E\x14\x74\x75', ], magic, 'Unreal Engine LOCRES File'):         
                return

            locres.seek(16, 0)
            byte_step = int.from_bytes(locres.read(1), 'little')
            data_size = int.from_bytes(locres.read(8), 'little')
            all_value = int.from_bytes(locres.read(4), 'little')
            block_count = int.from_bytes(locres.read(4), 'little')
            value_names_start = locres.tell()

            locres.seek(data_size, 0)
            string_count = int.from_bytes(locres.read(4), 'little')

            for i in range(string_count):

                long = struct.unpack('<i', locres.read(4))[0]

                if long < 0:
                    long = -long * 2
                    string_data = locres.read(long).decode('utf-16', errors='ignore').strip('\0')
                else:
                    string_data = locres.read(long).decode('utf-8', errors='ignore').strip('\0')
                
                strings.append(string_data)
                locres.seek(4 if byte_step > 1 else 0, 1)

            locres.seek(value_names_start, 0)
            a = 0
            
            for i in range(block_count):
                block_hash = int.from_bytes(locres.read(4), 'little')
                block_name_len = int.from_bytes(locres.read(4), 'little')
                block_name = locres.read(block_name_len).decode('utf-8', errors='ignore').strip('\0')
                block_strings = int.from_bytes(locres.read(4), 'little')
                sss = []

                for j in range(block_strings):

                    try:
                        string_hash = int.from_bytes(locres.read(4), 'little')
                        string_len = int.from_bytes(locres.read(4), 'little')
                        string_data = locres.read(string_len).decode('utf-8', errors='ignore').strip('\0')
                        string_hash_2 = int.from_bytes(locres.read(4), 'little')
                        string_num = int.from_bytes(locres.read(4), 'little')
                        sss.append({string_data: {'original': strings[a], 'translate': strings[a]}})

                        if (a + 1) % 1000 == 0:
                            self.update_pb(string_count, a + 1, string_data)

                    except IndexError:
                        sss.append({string_data: {'original': '', 'translate': ''}})

                    a += 1

                strings_json[block_name] = sss
                ic(len(sss))

            ext = os.path.splitext(self.file_name)[1].lower()
            
            with open(self.output_folder + f'\\{os.path.basename(self.file_name).replace(ext, '.json')}', 'w') as json_file:
                json.dump(strings_json, json_file, indent=4)
        
            self.update_pb(string_count, string_count, localize.done)


class TXT2Locres(Reaper):

    @file_reaper
    def run(self):
        string_count = 0
        magic = b'\x0E\x14\x74\x75'
        header = b''
        strings = b''
        a = 0
        b = 0
        
        with open(self.file_name, 'r') as file:
            locres = json.load(file)

        for key in locres.keys():
            string_count += len(locres[key])
        
        header += string_count.to_bytes(4, byteorder='little')
        header += len(locres).to_bytes(4, byteorder='little')
        
        for key, val in locres.items():

            if key == 'type':
                continue

            header += (zlib.crc32(key.encode('utf-8')) & 0xFFFFFFFF).to_bytes(4, 'big')
            header += (len(key) + 1).to_bytes(4, byteorder='little')
            header += key.encode('utf-8') + b'\0'
            header += len(locres[key]).to_bytes(4, byteorder='little')

            for i in range(len(val)):
                
                for k, v in val[i].items():
                    header += (zlib.crc32(k.encode('utf-8')) & 0xFFFFFFFF).to_bytes(4, 'big')
                    header += (len(k) + 1).to_bytes(4, byteorder='little')
                    header += k.encode('utf-8') + b'\0'
                    header += (zlib.crc32(k.encode('utf-8')) ^ 0xFFFFFFFF).to_bytes(4, 'big')
                    header += a.to_bytes(4, byteorder='little')
                    a += 1

                    t_len = len(v['translate'])

                    if t_len > 0:
                        data_len = struct.pack('<i', -(t_len + 1))
                        strings += data_len
                        strings += v['translate'].encode('utf-16')[2:] + b'\0\0'
                        strings += (1).to_bytes(4, byteorder='little')
                        b += 1

                        if a % 1000 == 0:
                            self.update_pb(string_count, a, v['translate'])

        magic += (zlib.crc32(k.encode('utf-8')) & 0xFFFFFFFF).to_bytes(12, 'big')
        magic += (3).to_bytes(1, byteorder='little')
        magic += (len(header) + len(magic) + 8).to_bytes(8, byteorder='little')
        header += b.to_bytes(4, byteorder='little')
        base_name = os.path.basename(self.file_name).replace('.json', '.locres')

        with open(f'{self.output_folder}\\{base_name}', 'wb') as nf:
            nf.write(magic + header + strings)
        
        self.update_pb(string_count, string_count, localize.done)

