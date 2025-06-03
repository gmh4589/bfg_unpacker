import os
import zlib

from source.reaper import Reaper, file_reaper
from collections import namedtuple

class Brink(Reaper):
    # TODO: Unpacking without names.
    #  Найден блок с именами файлов, но не вышло сопоставить имена и файлы

    @file_reaper
    def run(self):

        ext = self.file_name.split('.')[-1]
        sdmd2 = self.file_name.replace(ext, 'sdmd2')
        sdpk2 = self.file_name.replace(ext, 'sdpk2')

        with open(sdmd2, "rb") as sdmd_file:
            magic = sdmd_file.read(4)

            if not self.magic([b'\0\0\x04\0', ], magic, 'Brink'):
                return

            search_start = 0x2010

            while True:
                sdmd_file.seek(search_start)

                if sdmd_file.read(2) == b'\x03\xFF':
                    break

                search_start += 0x2000

            file_count = int.from_bytes(sdmd_file.read(4), byteorder="big")
            sdmd_file.seek(file_count * 4, 1)
            file_list_size = int.from_bytes(sdmd_file.read(4), byteorder="big")
            file_list = [n.decode("ascii") for n in sdmd_file.read(file_list_size).split(b'\0') if n]

        with open(sdpk2, 'rb') as sdpk_file:
            magic = sdpk_file.read(4)

            if not self.magic([b'PSAR', ], magic, 'Brink'):
                return

            sdpk_file.seek(8)
            compression_method = sdpk_file.read(4).decode('ascii')
            header_size = int.from_bytes(sdpk_file.read(4), byteorder="big") - 32
            entry_size = int.from_bytes(sdpk_file.read(4), byteorder="big")
            entry_count = int.from_bytes(sdpk_file.read(4), byteorder="big")
            data_block_size = int.from_bytes(sdpk_file.read(4), byteorder="big")
            sizes_long = int.from_bytes(sdpk_file.read(4), byteorder="big")
            sizes = []

            here = sdpk_file.tell()

            extra_off = here + (entry_count * entry_size)
            extra_count = (header_size - (entry_count * entry_size)) / 2
            sdpk_file.seek(extra_off)

            for i in range(int(extra_count)):
                sizes.append(int.from_bytes(sdpk_file.read(sizes_long), byteorder="big"))

            sdpk_file.seek(here)
            FileNames = namedtuple('FileNames',
                                   ['hash_val', 'compressed_block_index', 'uncompressed_size', 'offset'])
            file_names = []

            for i in range(entry_count):
                sdpk_file.seek(here + i * entry_size)
                hash_val = int.from_bytes(sdpk_file.read(16), byteorder="big")
                compressed_block_index = int.from_bytes(sdpk_file.read(4), byteorder="big")
                tmp = int.from_bytes(sdpk_file.read(1), byteorder="big")
                uncompressed_size = int.from_bytes(sdpk_file.read(4), byteorder="big")
                uncompressed_size |= (tmp << 32)
                tmp = int.from_bytes(sdpk_file.read(1), byteorder="big")
                offset = int.from_bytes(sdpk_file.read(4), byteorder="big")
                offset |= (tmp << 32)
                file_names.append(FileNames(hash_val, compressed_block_index, uncompressed_size, offset))

            file_paths = {}
            folder_name = ''

            for f in file_list:

                if f[-1] == '/':
                    folder_name = f
                    continue

                file_paths[hash(f'{folder_name}{f}')] = f'{folder_name}{f}'

            for i in range(len(file_names)):
                sdpk_file.seek(file_names[i].offset)
                data = sdpk_file.read(file_names[i].uncompressed_size)

                try:
                    data = zlib.decompress(data, 0)
                except Exception as e:
                    print(e)

                full_path = f"{self.output_folder}\\{file_names[i].hash_val}.{self.get_ext(data[:4])}"
                self.file_save(full_path, data)
                self.update_pb(len(file_names), i, full_path)
