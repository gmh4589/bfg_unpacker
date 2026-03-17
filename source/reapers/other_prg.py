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

        if '%set_dir%' in self.script_name:
            self.script_name = self.script_name.replace('%set_dir%', '')
            self.change_dir = self.output_folder

        if self.change_dir is not None:
            os.chdir(self.change_dir)

        if self.script_name == 'sau':
            sau_path = os.path.abspath(f"{self.path_to_root}\\data\\tools\\sau.exe")
            os.chdir(os.path.dirname(self.file_name))
            self.script_name = f'{sau_path} ./{os.path.basename(self.file_name)} dir="{self.output_folder}"'
            
        elif self.script_name == 'wit':
            ext = self.file_name.split('.')[-1]

            with open(self.file_name, 'rb') as fff:
                fff.seek(0x20 if ext in ('iso', 'gcm') else 0x220)
                name = fff.read(0x40).strip(b'\0').decode('utf-8')

            # data\wit\wit.exe X "%full_file_name%" -d "%out_dir%\nintendo_iso"
            ic(name)
            print(name)
            self.script_name = f'data\\wit\\wit.exe X "{self.file_name}" -d "{self.output_folder}\\{name}"'

        else:
            self.script_name = f"{self.path_to_root}\\{self.script_name}"
            ic(self.script_name)
            self.script_name = (self.script_name
                              .replace(r'%out_dir%', self.output_folder)
                              .replace(r'%full_file_name%', self.file_name)
                              .replace(r'%name_wxt%', os.path.splitext(os.path.basename(self.file_name))[0])
                              .replace(r'%ext%', os.path.splitext(os.path.basename(self.file_name))[1])
                              .replace(r'%file_name%', os.path.basename(self.file_name)))

        ic(self.script_name)

        try:
            prg = Popen(self.script_name, stdout=PIPE, stderr=PIPE, stdin=PIPE, encoding='utf-8', errors='ignore', shell=False)

        except Exception as error:
            self.update_signal.emit(100, '', localize.done, True)
            print(error)
            return

        self.pipe_reader(prg, chang_dir=bool(self.change_dir))
