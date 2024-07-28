import os
from icecream import ic
from collections import namedtuple

from source.reaper import Reaper, file_reaper
from source.ui import localize


class BethesdaArchive(Reaper):

    @file_reaper
    def run(self):
        # TODO: Add support Morrowind and older games
        # TODO: Trouble with unpack some Oblivion, Skyrim LE, F3 and FNV archives

        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if magic != b'BSA\0':
                print(localize.not_correct_file.replace('%%', 'Bethesda Softworks Archive'))
                self.update_signal.emit(100, '',
                                        localize.not_correct_file.replace('%%', 'Bethesda Softworks Archive'), True)
                return

            version = int.from_bytes(file.read(4), byteorder="little")
            step = 4 if version == 105 else 0
            folder_list_start = int.from_bytes(file.read(4), byteorder="little")
            flags = int.from_bytes(file.read(4), byteorder="little")

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

            folder_count = int.from_bytes(file.read(4), byteorder=byteorder)
            file_count = int.from_bytes(file.read(4), byteorder=byteorder)
            all_folders_len = int.from_bytes(file.read(4), byteorder=byteorder)
            all_files_len = int.from_bytes(file.read(4), byteorder=byteorder)

            ic(folder_count, file_count, all_folders_len, all_files_len)
            file_type_flags = int.from_bytes(file.read(4), byteorder=byteorder)

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

            for i in range(folder_count):
                name_hash = file.read(8)
                files_in_folder = int.from_bytes(file.read(4), byteorder=byteorder)
                file.seek(step, 1)
                offset_to_files = int.from_bytes(file.read(4), byteorder=byteorder)
                file.seek(step, 1)
                folder_data.append(FolderData(name_hash, files_in_folder, offset_to_files))
                ic(name_hash, files_in_folder)

            FileData = namedtuple('FileData',
                                  ['folder_name', 'name_hash', 'file_size', 'file_offset'])
            file_data = []

            for data in folder_data:

                folder_name_len = int.from_bytes(file.read(1), byteorder=byteorder)
                folder_name = file.read(folder_name_len).rstrip(b'\x00').decode('utf-8', errors='ignore')
                os.makedirs(os.path.join(self.output_folder, folder_name), exist_ok=True)

                for j in range(data.files_in_folder):
                    name_hash = file.read(8)
                    file_size = int.from_bytes(file.read(4), byteorder=byteorder)
                    file_offset = int.from_bytes(file.read(4), byteorder=byteorder)
                    file_data.append(FileData(folder_name, name_hash, file_size, file_offset))

            files_list = [file_name.decode('utf-8') for file_name in
                          file.read(all_files_len).split(b'\0') if file_name]

            for k, file_name in enumerate(files_list):

                comp = 0
                path = os.path.join(self.output_folder, file_data[k].folder_name, file_name)
                file.seek(file_data[k].file_offset)

                if compressed:
                    unzip_size = int.from_bytes(file.read(4), byteorder=byteorder)

                    if file_data[k].file_size - unzip_size == 0x13:
                        comp = 0xf
                        file.seek(0xb, 1)
                    else:
                        file.seek(file_data[k].file_offset)

                with open(path, 'wb') as new_file:
                    new_file.write(file.read(file_data[k].file_size - comp))

                if compressed and comp == 0:
                    self.unzip(path, 171)
                elif compressed and comp and version == 105:
                    # TODO: Research compress algorythm into Skyrim SE
                    self.unzip(path, 170)

                ic(file_name)
                print(f'{k}/{file_count}: {localize.saving} - {file_name}...')
                self.update_signal.emit(int(100 / file_count * k), f'{k + 1}/{file_count}',
                                        f'{localize.saving} - {file_name}...', False)

        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
