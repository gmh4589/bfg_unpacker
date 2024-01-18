
import os
from icecream import ic

from source.reaper import Reaper
from source.ui import localize


class AFSExtractor(Reaper):

    def run(self):

        with open(self.file_name, "rb") as afs_file:
            magic = afs_file.read(4)

            if magic != b'AFS\x00':
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'AFS'), True)
                return

            file_count = int.from_bytes(afs_file.read(4), byteorder="little")

            for i in range(file_count):
                name = '00000000'[:(len(str(i)))] + str(i) + '.dat'
                offset = int.from_bytes(afs_file.read(4), byteorder="little")
                size = int.from_bytes(afs_file.read(4), byteorder="little")
                ic(name)

                path = os.path.join(self.output_folder, name)
                ic(path)
                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as new_file:
                    here = afs_file.tell()
                    afs_file.seek(offset)
                    new_file.write(afs_file.read(size))
                    afs_file.seek(here)

                print(f'{i}/{file_count}: {localize.saving} - {name}...')
                self.update_signal.emit(int(100 / file_count * (i + 1)), f'{i}/{file_count}',
                                        f'{localize.saving} - {name}...', False)

        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
