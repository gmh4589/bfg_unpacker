import os
import zlib
import lz4.frame

from icecream import ic
from collections import namedtuple

from source.reaper import Reaper, file_reaper
from source.ui import localize


class BethesdaArchive(Reaper):
    #  TODO:
    #   retry OBJ files,
    #   add x_mem support

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bsa_file:
            magic = bsa_file.read(4)

            if magic != b'BSA\0':
                print(localize.not_correct_file.replace('%%', 'Bethesda Softworks Archive'))
                self.update_signal.emit(100, '',
                                        localize.not_correct_file.replace('%%', 'Bethesda Softworks Archive'), True)
                return

            version = int.from_bytes(bsa_file.read(4), byteorder="little")
            step = 4 if version == 105 else 0
            folder_list_start = int.from_bytes(bsa_file.read(4), byteorder="little")
            flags = int.from_bytes(bsa_file.read(4), byteorder="little")
            directory_names = bool(flags & 0x1)
            file_names = bool(flags & 0x2)
            compressed = bool(flags & 0x4)
            retain_directory = bool(flags & 0x8)
            retain_names = bool(flags & 0x10)
            retain_offsets = bool(flags & 0x20)
            xbox = bool(flags & 0x40)
            startup_strings = bool(flags & 0x80)
            embed_names = bool(flags & 0x100)
            x_mem = bool(flags & 0x200)

            byteorder = 'big' if xbox else 'little'

            folder_count = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
            file_count = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
            all_folders_len = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
            all_files_len = int.from_bytes(bsa_file.read(4), byteorder=byteorder)

            ic(compressed, folder_count, file_count, all_folders_len, all_files_len)
            file_type_flags = int.from_bytes(bsa_file.read(4), byteorder=byteorder)

            nif = bool(file_type_flags & 0x1)
            dds = bool(file_type_flags & 0x2)
            xml = bool(file_type_flags & 0x4)
            wav = bool(file_type_flags & 0x8)
            mp3 = bool(file_type_flags & 0x10)
            txt = bool(file_type_flags & 0x20)
            spt = bool(file_type_flags & 0x40)
            fnt = bool(file_type_flags & 0x80)
            misc = bool(file_type_flags & 0x100)
            x_mem = bool(file_type_flags & 0x200)

            FolderData = namedtuple('FolderData',
                                    ['name_hash', 'files_in_folder', 'offset_to_files'])
            folder_data = []

            self.update_signal.emit(0, '', f'{localize.wait}...', False)

            for i in range(folder_count):
                name_hash = bsa_file.read(8)
                files_in_folder = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                bsa_file.seek(step, 1)
                offset_to_files = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                bsa_file.seek(step, 1)
                folder_data.append(FolderData(name_hash, files_in_folder, offset_to_files))

            FileData = namedtuple('FileData',
                                  ['folder_name', 'name_hash', 'file_size', 'file_offset'])
            file_data = []

            for data in folder_data:

                folder_name_len = int.from_bytes(bsa_file.read(1), byteorder=byteorder)
                folder_name = bsa_file.read(folder_name_len).rstrip(b'\x00').decode('utf-8', errors='ignore')
                # os.makedirs(os.path.join(self.output_folder, folder_name), exist_ok=True)

                for j in range(data.files_in_folder):
                    name_hash = bsa_file.read(8)
                    file_size = int.from_bytes(bsa_file.read(3), byteorder=byteorder)
                    something = int.from_bytes(bsa_file.read(1))
                    file_offset = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                    file_data.append(FileData(folder_name, name_hash, file_size, file_offset))

            files_list = [file_name.decode('utf-8', errors='ignore')
                          for file_name in bsa_file.read(all_files_len).split(b'\0') if file_name]

            for k, file_name in enumerate(files_list):

                path = os.path.join(self.output_folder, file_data[k].folder_name, file_name)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                bsa_file.seek(file_data[k].file_offset + 4)
                error = False
                ext = file_name.split('.')[-1]
                self.update_pb(file_count, k, file_name)

                if version == 103:

                    if b'\x78\x9C' in bsa_file.read(8):
                        compressed = True

                    if ext in ('mp3', 'ogg', 'png'):
                        compressed = False

                bsa_file.seek(file_data[k].file_offset)

                if compressed:

                    if version in (103, 104):  # 103 - Oblivion, 104 - Skyrim LE, Fallout 3, Fallout NV
                        codec = 170
                        here = bsa_file.tell()

                        if embed_names:
                            name_l = int.from_bytes(bsa_file.read(1))
                            file_name = bsa_file.read(name_l)

                        unzip_size = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                        unzip_data = bsa_file.read(file_data[k].file_size)

                        try:
                            unzip_data = zlib.decompress(unzip_data)
                        except zlib.error:
                            bsa_file.seek(here)
                            unzip_size = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                            unzip_data = bsa_file.read(file_data[k].file_size)

                            try:
                                unzip_data = zlib.decompress(unzip_data)
                            except zlib.error:
                                error = True

                    elif version == 105:
                        codec = 249
                        here = bsa_file.tell()

                        if ext in ('dds', 'png'):
                            name_l = int.from_bytes(bsa_file.read(1))
                            file_name = bsa_file.read(name_l)

                        unzip_size = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                        unzip_data = bsa_file.read(file_data[k].file_size)

                        try:
                            unzip_data = lz4.frame.decompress(unzip_data)
                        except RuntimeError:
                            bsa_file.seek(here)
                            unzip_size = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                            unzip_data = bsa_file.read(file_data[k].file_size)

                            try:
                                unzip_data = lz4.frame.decompress(unzip_data)
                            except RuntimeError:
                                error = True

                else:
                    unzip_data = bsa_file.read(file_data[k].file_size)

                with open(path, 'wb') as new_file:
                    # new_file.write(bsa_file.read(file_data[k].file_size))
                    new_file.write(unzip_data)

                if compressed and error:
                    self.unzip(path, codec)

        # self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)


class OldBSA(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bsa_file:
            file_len = os.path.getsize(self.file_name)
            file_count = int.from_bytes(bsa_file.read(2), byteorder="little")
            key = int.from_bytes(bsa_file.read(2), byteorder="big")
            pos = 4 if key < 3 else 2

            file_list_start = (file_len - file_count * 0x12) if "ARCH3D" not in self.file_name else 0x19CED14
            bsa_file.seek(file_list_start)

            for i in range(file_count):
                name = (bsa_file.read(14)[:13].rstrip(b'\x00').decode('utf-8', errors='ignore')
                        if "ARCH3D" not in self.file_name else str(int.from_bytes(bsa_file.read(4), byteorder="little")))
                size = int.from_bytes(bsa_file.read(4), byteorder="little")
                here = bsa_file.tell()
                bsa_file.seek(pos)
                data = bsa_file.read(size)
                pos += size
                bsa_file.seek(here)

                if "ARCH3D" in self.file_name:
                    name += '.3D'

                self.update_pb(file_count, i, name)

                with open(os.path.join(self.output_folder, f"{name}"), 'wb') as nf:
                    nf.write(data)


class DaggerSND(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name,  'rb') as snd_file:
            file_count = int.from_bytes(snd_file.read(2), byteorder="little")
            file_long = os.path.getsize(self.file_name)
            pos = file_long - file_count * 8
            start = 4

            for i in range(file_count):
                snd_file.seek(pos)
                name = f'{int.from_bytes(snd_file.read(4), byteorder="little")}.wav'
                size = int.from_bytes(snd_file.read(4), byteorder="little")
                pos = snd_file.tell()
                snd_file.seek(start)
                start += size
                data = snd_file.read(size)
                self.update_pb(file_count, i, name)

                with open(os.path.join(self.output_folder, name), 'wb') as nf:

                    if data[:4] == b'RIFF':
                        nf.write(data)
                    else:
                        nf.write((b'\x52\x49\x46\x46\xE7\x99\x00\x00\x57\x41\x56\x45\x66\x6D\x74\x20\x10\x00'
                                  b'\x00\x00\x01\x00\x01\x00\x11\x2B\x00\x00\x11\x2B\x00\x00\x01\x00\x08\x00'
                                  b'\x64\x61\x74\x61\xC3\x99') + data)


class MorrowindBSA(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as bsa_file:
            magic = bsa_file.read(4)

            if magic != b'\0\x01\0\0':
                print(localize.not_correct_file.replace('%%', 'Bethesda Softworks Archive'))
                self.update_signal.emit(100, '',
                                        localize.not_correct_file.replace('%%', 'Bethesda Softworks Archive'), True)
                return

            long_data = int.from_bytes(bsa_file.read(4), byteorder="little")
            file_count = int.from_bytes(bsa_file.read(4), byteorder="little")
            offsets = []
            longs = []

            for i in range(file_count):
                long = int.from_bytes(bsa_file.read(4), byteorder="little")
                offset = int.from_bytes(bsa_file.read(4), byteorder="little")
                longs.append(long)
                offsets.append(offset)

            for _ in range(file_count):
                bsa_file.read(4)

            here = bsa_file.tell()

            pos = long_data - here + 12
            files_list = [file_name.decode('utf-8') for file_name in
                          bsa_file.read(pos).split(b'\0') if file_name]

            for _ in range(file_count):
                bsa_file.read(8)

            here = bsa_file.tell()

            for i, name in enumerate(files_list):
                bsa_file.seek(offsets[i] + here)
                data = bsa_file.read(longs[i])
                os.makedirs(os.path.join(self.output_folder, os.path.dirname(name)), exist_ok=True)

                with open(os.path.join(self.output_folder, name), 'wb') as new_file:
                    new_file.write(data)

                self.update_pb(file_count, i, name)

