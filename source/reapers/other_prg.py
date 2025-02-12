import os
from icecream import ic
from subprocess import Popen, PIPE
from threading import Thread

from source.reaper import Reaper, file_reaper, OutReader
from source.ui import localize


class OtherProg(Reaper, OutReader):

    def __init__(self):
        super().__init__()
        self.script_name = ''

    @file_reaper
    def run(self):

        if self.script_name == 'sau':
            sau_path = os.path.abspath(f"{self.path_to_root}\\data\\tools\\sau.exe")
            os.chdir(os.path.dirname(self.file_name))
            self.script_name = f'{sau_path} ./{os.path.basename(self.file_name)} dir="{self.output_folder}"'

        else:
            self.script_name = f"{self.path_to_root}\\{self.script_name}"
            ic(self.script_name)
            self.script_name = (self.script_name
                              .replace('%out_dir%', self.output_folder)
                              .replace('%full_file_name%', self.file_name)
                              .replace('%file_name%', os.path.basename(self.file_name)))

        ic(self.script_name)

        try:
            prg = Popen(self.script_name, stdout=PIPE, stderr=PIPE, encoding='utf-8', errors='ignore', shell=False)

        except Exception as error:
            self.update_signal.emit(100, '', localize.done, True)
            print(error)
            return

        Thread(target=self.out_reader, args=[prg,], daemon=True).start()
        Thread(target=self.err_reader, args=[prg,], daemon=True).start()

        while prg.poll() is None:

            try:
                self.update_signal.emit(0, '', f'{self.output[-1]}...', False)

            except Exception as e:
                ic(e)
                self.update_signal.emit(0, '', '', False)

        self.end = True
        self.update_signal.emit(0, '', '', True)
        os.chdir(self.path_to_root)
