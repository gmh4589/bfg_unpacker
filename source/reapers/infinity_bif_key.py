import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize
# TODO: Add The Witcher 1 support, try all games


class BifKey(Reaper):

    @file_reaper
    def run(self):
        only_name = self.file_name.split('.')[0]
        bif_file = f'{only_name}.bif'

        with open(bif_file, "rb") as file:
            magic = file.read(4)

            if magic != b'BIFF':
                print(localize.not_correct_file.replace('%%', 'Aurora Engine'))
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Aurora Engine'), True)
                return

            file.seek(8, 0)
            file_count = int.from_bytes(file.read(4), byteorder="little")
            file.seek(0x10, 0)

            for i in range(file_count):
                size = int.from_bytes(file.read(4), byteorder="little")
                file.seek(4, 1)
                offset = int.from_bytes(file.read(4), byteorder="little")
                here = file.tell()
                file.seek(offset)
                dat = file.read(size)
                ext = self.get_ext(dat[:4]).strip()

                path = os.path.join(self.output_folder, f"{i}.{ext}")
                ic(path)
                os.makedirs(os.path.dirname(path), exist_ok=True)

                try:

                    with open(path, 'wb') as new_file:
                        new_file.write(dat)

                except ValueError:

                    with open(path.replace(ext, 'dat'), 'wb') as new_file:
                        new_file.write(dat)

                file.seek(here + 4)
                print(f'{i}/{file_count}: {localize.saving} - {i}.{ext}...')
                self.update_signal.emit(int(100 / file_count * i), f'{i}/{file_count}',
                                        f'{localize.saving} - {i}.{ext}...', False)

        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
