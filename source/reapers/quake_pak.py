
import os
from source.reaper import Reaper, file_reaper
from source.ui import localize


class QPAKExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as pak_file:
            magic = pak_file.read(4)

            if magic != b'PACK':
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'PAK'), True)
                return

            entry_offset = int.from_bytes(pak_file.read(4), byteorder="little")
            pak_file.seek(entry_offset)
            file_list = {}
            file_size = os.path.getsize(self.file_name)

            while True:
                name = pak_file.read(56).decode("ascii").rstrip("\0")
                offset = int.from_bytes(pak_file.read(4), byteorder="little")
                size = int.from_bytes(pak_file.read(4), byteorder="little")
                file_list[name] = [offset, size]

                if pak_file.tell() >= file_size: break

            i = 0
            
            for name, value in file_list.items():
                i += 1
                offset, size = value
                path = os.path.join(self.output_folder, name)
                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as new_file:
                    pak_file.seek(offset)
                    new_file.write(pak_file.read(size))

                print(f"{i}/{len(file_list)} {name}")
                self.update_signal.emit(int(100 / len(file_list) * i), f'{i}/{len(file_list)}',
                                        f'{localize.saving} - {name}...', False)

        self.update_signal.emit(100, f'{len(file_list)}/{len(file_list)}', localize.done, True)
