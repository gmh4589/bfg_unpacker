
import os
from source.reaper import Reaper, file_reaper
from source.ui import localize


class MorUnpacker(Reaper):

    @file_reaper
    def run(self):
        file_name = self.file_name

        with open(file_name, 'rb') as f:

            magic = f.read(4)

            if magic != b'LP1C':
                print(localize.not_correct_file.replace('%%', 'Pathologic Classic'))
                self.update_signal.emit(100, '', localize.done, True)
                return

            f.seek(8)
            file_count = int.from_bytes(f.read(4), byteorder='little')

            for i in range(file_count):
                name_length = int.from_bytes(f.read(1), byteorder='little')
                name = f.read(name_length).decode('unicode_escape')
                file_position = f.tell()
                file_size = int.from_bytes(f.read(4), byteorder='little')
                file_offset = int.from_bytes(f.read(4), byteorder='little')
                f.seek(file_offset)
                file_data = f.read(file_size)
                output_path = os.path.join(self.output_folder, name)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'wb') as new_file:
                    new_file.write(file_data)

                f.seek(file_position + 16)
                print(f'{i + 1}/{file_count} - {name}')
                self.update_signal.emit(int(100 / file_count * (i + 1)), f'{i + 1}/{file_count}',
                                        f'{localize.saving} - {name}...', False)

            self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
