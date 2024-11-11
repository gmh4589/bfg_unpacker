import os
from random import randint
from icecream import ic
from subprocess import Popen, PIPE

from source.reaper import Reaper, file_reaper
from source.ui import localize


class OtherProg(Reaper):

    def __init__(self,
                 program_name='test.exe',
                 percent_index=0,
                 percent_type='int',
                 percent_del='\\',
                 name_index=1,
                 first_arg='',
                 second_arg='',
                 splitter=' ',
                 run_type='popen'
                 ):
        super().__init__()
        self.program_name = program_name
        self.percent_index = percent_index
        self.percent_type = percent_type

        # Percent type:
        # int = real int digit
        # l_first = left digit current, right digit all
        # r_first = right digit current, left digit all
        # 50 = all time 50 percent
        # not = without progress bar
        # else = random

        self.percent_del = percent_del
        self.name_index = name_index
        self.first_arg = first_arg
        self.second_arg = second_arg
        self.splitter = splitter
        self.run_type = run_type

    @file_reaper
    def run(self):
        self.first_arg = (self.first_arg
                          .replace('%out_dir%', self.output_folder)
                          .replace('%full_file_name%', self.file_name)
                          .replace('%file_name%', os.path.basename(self.file_name)))
        self.second_arg = (self.second_arg
                           .replace('%out_dir%', self.output_folder)
                           .replace('%full_file_name%', self.file_name)
                           .replace('%file_name%', os.path.basename(self.file_name)))

        arguments = (f'"data\\{self.program_name}" {self.first_arg} '
                     f'"{self.file_name}" {self.second_arg}').replace('/', '\\')
        ic(self.program_name)
        ic(self.first_arg)
        ic(self.file_name)
        ic(self.second_arg)
        ic(arguments)
        percent = 0
        pipe = None
        prg = None

        try:

            if self.run_type == 'popen':
                prg = Popen(arguments, stdout=PIPE, stderr=PIPE, encoding='utf-8', errors='ignore')
            elif self.run_type == 'os.system':
                os.system(arguments)
            elif self.run_type == 'command_line':

                with open('temp.bat', 'w') as tb:
                    tb.write(arguments)

                os.system('temp.bat')

        except Exception as error:
            self.update_signal.emit(100, '', localize.done, True)
            print(error)
            return

        if self.percent_type == '50':
            self.update_signal.emit(50, '', f'{localize.saving} - {self.file_name}...', False)

        elif self.percent_type == 'not':
            self.update_signal.emit(100, '', f'{localize.saving} - {self.file_name}...', True)

        while True:

            if pipe is not None:
                print(pipe)
            else:

                try:
                    out = prg.stdout.readline().strip()
                    o = out.split(self.splitter)
                    print(out)
                    ic(prg.stderr.readline().strip(), out)

                    if not out:
                        prg.kill()
                        break

                    if self.percent_type == 'int':
                        percent = int(o[self.percent_index])
                    elif self.percent_type == 'l_first':
                        first, second = o[self.percent_index].split(self.percent_del)
                        percent = int(100 / int(second) * int(first))
                    elif self.percent_type == 'b_first':
                        first, second = o[self.percent_index].split(self.percent_del)
                        percent = int(100 / int(first) * int(second))
                    else:
                        percent += randint(5, 20) if percent <= 90 else 90

                    self.update_signal.emit(percent, '', f'{localize.saving} - {o[self.name_index]}...', False)

                except Exception as e:
                    ic(e)
                    percent += 1

                    if percent >= 100:
                        self.update_signal.emit(100, '', '', True)
                    else:
                        self.update_signal.emit(percent, '', f'{localize.saving} - ...', False)
