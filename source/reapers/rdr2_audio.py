
import os
from source.reaper import Reaper


class RDR2Audio(Reaper):

    def run(self):
        output_path = os.path.join(self.output_folder, self.file_name)
        name = os.path.dirname(output_path)

        with open(self.file_name, 'rb') as archive:
            data = archive.read()
            files = data.split(b'ADAT')
            files.pop(0)

        file_count = len(files)

        for i, file in enumerate(files):

            with open(f'{name}_{i}.awc', 'wb') as new_track:
                new_track.write(b'ADAT' + file)

            print(f'{i + 1}/{file_count} - {name}_{i}')
            self.update_signal.emit(int(100 / file_count * (i + 1)), f'{i + 1}/{file_count}',
                                    f'Saving - {name}_{i}...', False)

        self.update_signal.emit(100, f'{file_count}/{file_count}', 'Done!', True)
        print('Done!')