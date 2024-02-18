
import os
from subprocess import Popen, PIPE
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class Unity(Reaper):

    @file_reaper
    def run(self):
        path = os.path.dirname(self.file_name)

        unity = Popen(f'{self.path_to_root}/data/AssetStudio/AssetStudioCLI.exe '
                      f'"{path}" "{self.output_folder}" --game Normal',
                       stdout=PIPE, stderr=PIPE, encoding='utf-8')

        while True:
            out1 = unity.stdout.readline().strip()
            out = out1.split(' ')

            print(out1)
            ic(out1)

            try:
                i = int(out[1].split('/')[0])
                a = int(out[1].split('/')[1])
                percent = (100 / a) * i
                self.update_signal.emit(percent, '', f'{localize.saving} - {out[-1]}...', False)
            except (IndexError, ValueError):
                pass

            if not out1:
                break

        unity.kill()
        self.update_signal.emit(100, '', localize.done, True)
