
import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class RDR2Audio(Reaper):

    @file_reaper
    def run(self):
        name = os.path.basename(self.file_name).split('.')[-2]

        with open(self.file_name, 'rb') as archive:
            data = archive.read()
            files = data.split(b'ADAT')
            files.pop(0)

        file_count = len(files)

        for i, file in enumerate(files):

            with open(f'{self.output_folder}/{name}_{i}.awc', 'wb') as new_track:
                new_track.write(b'ADAT' + file)

            print(f'{i + 1}/{file_count} - {name}_{i}')
            ic(name, i)
            self.update_signal.emit(int(100 / file_count * (i + 1)), f'{i + 1}/{file_count}',
                                    f'{localize.saving} - {name}_{i}...', False)

        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
