
import os
from subprocess import Popen, PIPE
from icecream import ic

from source.reaper import Reaper
from source.ui import localize


class Unity(Reaper):

    def run(self):
        path = os.path.dirname(self.file_name)

        unity = Popen(f'{self.path_to_root}/data/AssetStudio/AssetStudioCLI.exe '
                      f'"{path}" "{self.output_folder}" --game Normal',
                       stdout=PIPE, stderr=PIPE, encoding='utf-8')

        while True:
            out1 = unity.stdout.readline().strip()

            print(out1)
            ic(out1)
            self.update_signal.emit(50, '', f'{localize.saving} - ...', False)

            if not out1:
                break

        unity.kill()
        self.update_signal.emit(100, '', localize.done, True)

