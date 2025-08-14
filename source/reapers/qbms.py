
import os
from subprocess import Popen, PIPE
from threading import Thread
from icecream import ic
from source.reaper import Reaper, file_reaper, OutReader
from source.ui import localize


class Q_BMS(Reaper):

    def __init__(self):
        super().__init__()
        self.script_name = ''
        self.add = '-K'

    @file_reaper
    def run(self):
        out_reader = OutReader()

        size = os.path.getsize(self.file_name)
        self.file_name = self.file_name.replace("/", "\\")
        script = (f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" {self.add} '
                  f'"{self.path_to_root}\\{self.script_name}" '
                  f'"{self.file_name}" "{self.output_folder}"').replace('/', '\\')
        ic(self.script_name)
        ic(script)
        bms = Popen(script, stdout=PIPE, stderr=PIPE, encoding='utf-8')

        Thread(target=out_reader.out_reader, args=[bms,], daemon=True).start()
        Thread(target=out_reader.err_reader, args=[bms,], daemon=True).start()

        while bms.poll() is None:

            try:
                percent = int(100 / size * int(out_reader.output[0], 16))
                # print(f"{percent}% {out_reader.output[-1]}")
                # ic(self.output[-1])
                self.update_signal.emit(percent, '', f'{localize.saving} - {out_reader.output[-1]}...', False)
            except (ValueError, IndexError):
                print(out_reader.out)

        out_reader.end = True
        self.update_signal.emit(100, '', localize.done, True)
