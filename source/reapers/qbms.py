
import os
from subprocess import Popen, PIPE

from source.reaper import Reaper, file_reaper
from source.ui import localize


class Q_BMS(Reaper):

    def __init__(self):
        super().__init__()
        self.script_name = ''

    @file_reaper
    def run(self):

        size = os.path.getsize(self.file_name)
        bms = Popen(f'{self.path_to_root}data/QuickBMS/quickbms.exe -K '
                    f'"{os.path.join(self.path_to_root, self.script_name)}" '
                    f'"{self.file_name}" "{self.output_folder}"',
                    stdout=PIPE, stderr=PIPE, encoding='utf-8')

        while True:
            out = bms.stdout.readline().strip()
            o = out.split(' ')

            try:
                percent = int(100 / size * int(o[0], 16))
                print(f"{percent}% {o[-1]}")

                self.update_signal.emit(percent, '', f'{localize.saving} - {o[-1]}...', False)
            except (ValueError, IndexError):
                pass

            if not out:
                break

        self.update_signal.emit(100, '', localize.done, True)