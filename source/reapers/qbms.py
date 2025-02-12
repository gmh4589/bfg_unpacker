
import os
from subprocess import Popen, PIPE
from threading import Thread

from icecream import ic

from source.reaper import Reaper, file_reaper, OutReader
from source.ui import localize


class Q_BMS(Reaper, OutReader):

    def __init__(self):
        super().__init__()
        self.script_name = ''
        self.add = '-K'

    @file_reaper
    def run(self):

        size = os.path.getsize(self.file_name)
        self.file_name = self.file_name.replace("/", "\\")
        script = (f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" {self.add} '
                  f'"{self.path_to_root}\\{self.script_name}" '
                  f'"{self.file_name}" "{self.output_folder}"').replace('/', '\\')
        ic(self.script_name)
        ic(script)
        bms = Popen(script, stdout=PIPE, stderr=PIPE, encoding='utf-8')

        Thread(target=self.out_reader, args=[bms,], daemon=True).start()
        Thread(target=self.err_reader, args=[bms,], daemon=True).start()

        while bms.poll() is None:

            try:
                percent = int(100 / size * int(self.output[0], 16))
                # print(f"{percent}% {self.output[-1]}")
                # ic(self.output[-1])
                self.update_signal.emit(percent, '', f'{localize.saving} - {self.output[-1]}...', False)
            except (ValueError, IndexError):
                print(self.out)

        self.end = True
        self.update_signal.emit(100, '', localize.done, True)
