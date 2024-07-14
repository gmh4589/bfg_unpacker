import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class BethesdaArchive(Reaper):

    @file_reaper
    def run(self):
        file_count = 0

        with (open(self.file_name, "rb") as file):
            magic = file.read(4)

            if magic == b'BSA\0':
                version = int.from_bytes(file.read(4), byteorder="little")

                match version:
                    case 103:
                        ic('TES IV: Oblivion')

                    case 104 | 105:
                        print('TES V: Skyrim')

                        folder_list_start = int.from_bytes(file.read(4), byteorder="little")
                        flags = int.from_bytes(file.read(4), byteorder="little")
                        x_mem = bool(flags & 0x200)
                        file_indicate = bool(flags & 0x100)
                        retain_strings = bool(flags & 0x80)
                        xbox = bool(flags & 0x40)
                        file_name_offsets = bool(flags & 0x20)
                        file_names = bool(flags & 0x10)
                        directory_names = bool(flags & 0x8)
                        compressed = bool(flags & 0x4)
                        # ic(x_mem, file_indicate, retain_strings, xbox, file_name_offsets,
                        #    file_names, directory_names, compressed)
                        byteorder = 'big' if xbox else 'little'

                        folder_count = int.from_bytes(file.read(4), byteorder=byteorder)
                        file_count = int.from_bytes(file.read(4), byteorder=byteorder)
                        all_folders_len = int.from_bytes(file.read(4), byteorder=byteorder)
                        all_files_len = int.from_bytes(file.read(4), byteorder=byteorder)
                        file.seek(4, 1)

                        for i in range(folder_count):
                            name_hash = file.read(8)
                            files_in_folder = int.from_bytes(file.read(4), byteorder=byteorder)
                            file.seek(4, 1) if version == 105 else file.seek(0, 1)
                            offset_to_files = int.from_bytes(file.read(4), byteorder=byteorder)
                            file.seek(4, 1) if version == 105 else file.seek(0, 1)
                            ic(file.tell())
                            folder_name_len = int.from_bytes(file.read(1), byteorder=byteorder)
                            folder_name = file.read(folder_name_len).rstrip(b'\x00').decode('utf-8', errors='ignore')
                            ic(folder_name)
                            os.makedirs(os.path.join(self.output_folder, folder_name), exist_ok=True)
                            files_sizes = []
                            files_offsets = []

                            for j in range(files_in_folder):
                                file_name_hash = file.read(8)
                                files_sizes.append(int.from_bytes(file.read(4), byteorder=byteorder))
                                files_offsets.append(int.from_bytes(file.read(4), byteorder=byteorder))

                            files_list = [file_name.decode('utf-8') for file_name in file.read(all_files_len).split(b'\0')]
                            here = file.tell()

                            for k in range(files_in_folder):
                                file.seek(files_offsets[k] + 0xf)
                                path = os.path.join(self.output_folder, folder_name, files_list[k])
                                ext = files_list[k].split('.')[-1]

                                with open(path, 'wb') as new_file:
                                    new_file.write(file.read(files_sizes[k]))

                                if compressed and ext not in ('png', 'mp3', 'ogg', 'jpeg', 'jpg', 'jpe'):
                                    self.unzip(path, 2)

                                print(f'{i}/{file_count}: {localize.saving} - {files_list[k]}...')
                                self.update_signal.emit(int(100 / file_count * i), f'{i}/{file_count}',
                                                        f'{localize.saving} - {files_list[k]}...', False)

                            file.seek(here)
                    case _:
                        ic('Unknown version')
                        return

            elif magic == b'BTDX':

                version = int.from_bytes(file.read(4), byteorder="little")

                match version:
                    case 1:
                        ic('Fallout 4')
                    case 2:
                        ic('Starfield')

            else:

                print(localize.not_correct_file.replace('%%', 'Bethesda Softworks Archive'))
                self.update_signal.emit(100, '',
                                        localize.not_correct_file.replace('%%', 'Bethesda Softworks Archive'), True)
                return

        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
