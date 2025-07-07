import os
from icecream import ic
from subprocess import Popen, PIPE
from threading import Thread

from source.reaper import Reaper, file_reaper, OutReader
from source.ui import localize


class OtherProg(Reaper):

    def __init__(self):
        super().__init__()
        self.script_name = ''
        self.change_dir = None
        self.pr_err = ''
        self.pr_out = ''

    @file_reaper
    def run(self):
        out_reader = OutReader()

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
                fff.seek(0x20 if ext == 'iso' else 0x220)
                name = fff.read(0x40).strip(b'\0').decode('utf-8')

            self.script_name = f'data\\wit\\wit.exe X "%full_file_name%" -d "%out_dir%\\{name}"'

        else:
            self.script_name = f"{self.path_to_root}\\{self.script_name}"
            ic(self.script_name)
            self.script_name = (self.script_name
                              .replace('%out_dir%', self.output_folder)
                              .replace('%full_file_name%', self.file_name)
                              .replace('%file_name%', os.path.basename(self.file_name)))

        ic(self.script_name)

        try:
            prg = Popen(self.script_name, stdout=PIPE, stderr=PIPE, stdin=PIPE, encoding='utf-8', errors='ignore', shell=False)

        except Exception as error:
            self.update_signal.emit(100, '', localize.done, True)
            print(error)
            return

        Thread(target=out_reader.out_reader, args=[prg,], daemon=True).start()
        Thread(target=out_reader.err_reader, args=[prg,], daemon=True).start()

        while prg.poll() is None:

            try:
                self.update_signal.emit(0, '', f'{".".join(out_reader.output)}...', False)

                if out_reader.err and out_reader.err != self.pr_err:
                    print(out_reader.err)
                    self.pr_err = out_reader.err

                if out_reader.out and out_reader.out != self.pr_out:
                    print(out_reader.out)
                    self.pr_out = out_reader.out

                # if '(y/n)' in self.out:
                #     prg.stdin.write('y\n')
                #     prg.stdin.flush()

            except Exception as e:
                ic(e)
                self.update_signal.emit(0, '', '', False)

        out_reader.end = True
        self.update_signal.emit(0, '', '', True)
        os.chdir(self.path_to_root)
