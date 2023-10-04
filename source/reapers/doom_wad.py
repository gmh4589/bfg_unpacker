
import os
from source.reaper import Reaper, file_reaper


class WadExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as wad_file:
            magic = wad_file.read(4)

            if magic not in (b'IWAD', b'PWAD'):
                print("Ошибка: Неверный формат WAD-файла!")
                self.update_signal.emit(100, '', "Ошибка: Неверный формат WAD-файла!", True)  # TODO: text!!!
                return

            num_entries = int.from_bytes(wad_file.read(4), byteorder="little")
            data_offset = int.from_bytes(wad_file.read(4), byteorder="little")
            wad_file.seek(data_offset)

            for i in range(num_entries):
                entry_offset = int.from_bytes(wad_file.read(4), byteorder="little")
                entry_size = int.from_bytes(wad_file.read(4), byteorder="little")
                entry_name = wad_file.read(8).decode("ascii").rstrip("\0")

                for sym in '\\?':
                    entry_name = entry_name.replace(sym, '_')

                this_offset = wad_file.tell()

                wad_file.seek(entry_offset)
                entry_data = wad_file.read(entry_size)
                output_file_path = os.path.join(self.output_folder, entry_name)

                with open(output_file_path, "wb") as output_file:
                    output_file.write(entry_data)

                wad_file.seek(this_offset)

                print(f"{i + 1}/{num_entries} {entry_name}")
                self.update_signal.emit(int(100 / num_entries * (i + 1)), f'{i + 1}/{num_entries}',
                                        f'Saving - {entry_name}...', False)

            self.update_signal.emit(100, f'{num_entries}/{num_entries}', 'Done!', True)
