import os
from icecream import ic
from subprocess import Popen, PIPE

from source.reaper import Reaper, file_reaper
from source.ui import localize


class OtherProg(Reaper):

    def __init__(self, script_name=''):
        super().__init__()
        self.script_name = script_name
        self.change_dir = None

    @file_reaper
    def run(self):
        ic(self.script_name)

        if self.script_name == 'sau':
            sau_path = os.path.abspath(f"{self.path_to_root}\\data\\tools\\sau.exe")
            os.chdir(os.path.dirname(self.file_name))
            self.script_name = f'{sau_path} ./{os.path.basename(self.file_name)} dir="{self.output_folder}"'
            
        else:
            self.script_name = f"{self.path_to_root}\\{self.script_name}"
            self.script_name = (self.script_name
                              .replace(r'%out_dir%', self.output_folder)
                              .replace(r'%full_file_name%', self.file_name)
                              .replace(r'%name_wxt%', os.path.splitext(os.path.basename(self.file_name))[0])
                              .replace(r'%ext%', os.path.splitext(os.path.basename(self.file_name))[1])
                              .replace(r'%root_path%', self.path_to_root)
                              .replace(r'%new_line%', "\n")
                              .replace(r'%file_name%', os.path.basename(self.file_name)))

        ic(self.script_name)

        try:
            prg = Popen(self.script_name, stdout=PIPE, stderr=PIPE, stdin=PIPE, encoding='utf-8', errors='ignore', shell=False)

        except Exception as error:
            self.update_signal.emit(100, '', localize.done, True)
            print(error)
            return

        self.pipe_reader(prg, chang_dir=bool(self.change_dir))
