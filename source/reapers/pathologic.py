
import os
from PyQt5.QtCore import QThread, pyqtSignal
from source.unpacker import file_reaper


class mor_unpacker(QThread):
    update_signal = pyqtSignal(int, str, str, bool)

    def __init__(self, file_name, output_folder):
        super().__init__()
        self.file_name = file_name
        self.output_folder = output_folder

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as f:
            f.seek(8, 0)
            file_count = int.from_bytes(f.read(4), byteorder='little')

            for i in range(file_count):
                name_length = int.from_bytes(f.read(1), byteorder='little')
                name = f.read(name_length).decode('unicode_escape')
                file_position = f.tell()
                file_size = int.from_bytes(f.read(4), byteorder='little')
                file_offset = int.from_bytes(f.read(4), byteorder='little')
                f.seek(file_offset, 0)
                file_data = f.read(file_size)
                output_path = os.path.join(self.output_folder, name)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'wb') as new_file:
                    new_file.write(file_data)

                f.seek(file_position + 16, 0)
                print(f'{i + 1}/{file_count} - {name}')
                self.update_signal.emit(int(100 / file_count * (i + 1)), f'{i + 1}/{file_count}',
                                        f'Saving - {name}...', False)

            self.update_signal.emit(100, f'{file_count}/{file_count}', f'Done!', True)
            print('Done!')
