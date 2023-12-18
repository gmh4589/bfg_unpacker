
import os
from subprocess import Popen, PIPE

from source.reaper import Reaper, file_reaper
from source.ui import localize


class Unity(Reaper):

    @file_reaper
    def run(self):

        # os.chdir(f'{self.path_to_root}data/AssetStudio/')
        unity = Popen(f'{self.path_to_root}/data/AssetStudio/AssetStudioCLI.exe '
                      f'"{self.file_name}" "{self.output_folder}" --game Normal',
                       stdout=PIPE, stderr=PIPE, encoding='utf-8')

        while True:
            out1 = unity.stdout.readline().strip()
            out2 = unity.stderr.readline().strip()

            print(out1, out2)
            self.update_signal.emit(50, '', f'{localize.saving} - ...', False)

            if not out1 and not out2:
                break

        self.update_signal.emit(100, '', localize.done, True)
        # os.chdir(f'{self.path_to_root}')
