
import os
from subprocess import Popen, PIPE
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class Q_BMS(Reaper):

    def __init__(self):
        super().__init__()
        self.script_name = ''
        self.add = '-K'

    @file_reaper
    def run(self):

        size = os.path.getsize(self.file_name)
        self.file_name = self.file_name.replace("/", "\\")
        script = (f'"{self.path_to_root}data/QuickBMS/quickbms.exe" {self.add} '
                  f'"{os.path.join(self.path_to_root, self.script_name)}" '
                  f'"{self.file_name}" "{self.output_folder}"')
        ic(self.script_name)
        ic(script)
        bms = Popen(script, stdout=PIPE, stderr=PIPE, encoding='utf-8')

        while True:

            try:
                out = bms.stdout.readline().strip()
            except UnicodeDecodeError:
                continue

            o = out.split(' ')

            try:
                percent = int(100 / size * int(o[0], 16))
                print(f"{percent}% {o[-1]}")
                ic(o[-1])
                self.update_signal.emit(percent, '', f'{localize.saving} - {o[-1]}...', False)
            except (ValueError, IndexError):
                print(out)

            if not out:
                bms.kill()
                break

        self.update_signal.emit(100, '', localize.done, True)
