
import os

from source.reaper import Reaper, file_reaper


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

            self.update_pb(file_count, i, f'{name}_{i}.awc')
