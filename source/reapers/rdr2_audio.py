import os
from source.reapers.reaper import Reaper


class ERFUnpacker(Reaper):

    def run(self):
        output_path = os.path.join(self.output_folder, self.file_name)
        name = os.path.dirname(output_path)
        os.makedirs(name, exist_ok=True)

        with open(self.file_name, 'rb') as archive:
            data = archive.read()
            files = data.split(b'ADAT')
            files.pop(0)
            i = 1

        file_count = len(files)

        for file in files:

            with open(f'{name}_{i}.awc', 'wb') as new_track:
                new_track.write(b'ADAT' + file)

            i += 1

            print(f'{i + 1}/{file_count} - {name}')
            self.update_signal.emit(int(100 / file_count * (i + 1)), f'{i + 1}/{file_count}',
                                    f'Saving - {name}...', False)

        self.update_signal.emit(100, f'{file_count}/{file_count}', f'Done!', True)
        print('Done!')
