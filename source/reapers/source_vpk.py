import os
import vpk
from icecream import ic

from source.reaper import Reaper
from source.ui import localize


class VPKExtractor(Reaper):

    def run(self):

        vpk_file = self.file_name if '_dir.vpk' in self.file_name else self.file_name[:-7] + 'dir.vpk'
        ic(vpk_file)
        dir_pak = vpk.open(vpk_file)
        i = 0
        file_count = len(dir_pak)

        for name in dir_pak:
            i += 1
            pak_file = dir_pak.get_file(name)
            path = os.path.join(self.output_folder, name)
            ic(path)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pak_file.save(path)

            print(f'{i}/{file_count}: {localize.saving} - {name}...')
            self.update_signal.emit(int(100 / file_count * i), f'{i}/{file_count}',
                                    f'{localize.saving} - {name}...', False)

        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
