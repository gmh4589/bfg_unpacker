
from random import randint
from time import sleep
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
                 real_pb=True
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
        # else = random

        self.percent_del = percent_del
        self.name_index = name_index
        self.first_arg = first_arg
        self.second_arg = second_arg
        self.splitter = splitter
        self.real_pb = real_pb

    @file_reaper
    def run(self):
        arguments = (f'"data\\{self.program_name}" {self.first_arg} '
                     f'"{self.file_name}" {self.second_arg}').replace('/', '\\')
        ic(self.program_name)
        ic(self.first_arg)
        ic(self.file_name)
        ic(self.second_arg)
        ic(arguments)

        try:
            prg = Popen(arguments, stdout=PIPE, stderr=PIPE, encoding='utf-8', errors='ignore')
        except FileNotFoundError:
            self.update_signal.emit(100, '', localize.done, True)
            print(f"File {self.program_name} don't exists in data folder!")
            return

        if self.real_pb:

            if self.percent_type == '50':
                self.update_signal.emit(50, '', f'{localize.saving} - {self.file_name}...', False)

            while True:

                out = prg.stdout.readline().strip()
                o = out.split(self.splitter)
                percent = 0
                print(out)
                ic(prg.stderr.readline().strip())

                if not out:
                    prg.kill()
                    break

                try:

                    if self.percent_type == 'int':
                        percent = int(o[self.percent_index])
                    elif self.percent_type == 'l_first':
                        first, second = o[self.percent_index].split(self.percent_del)
                        percent = int(100 / int(second) * int(first))
                    elif self.percent_type == 'b_first':
                        first, second = o[self.percent_index].split(self.percent_del)
                        percent = int(100 / int(first) * int(second))
                    else:
                        percent += randint(1, 5) if percent <= 99 else 99

                    self.update_signal.emit(percent, '', f'{localize.saving} - {o[self.name_index]}...', False)

                except (ValueError, IndexError):
                    pass

        elif self.real_pb is None:
            pass

        else:
            a = 0

            while prg.poll() is None:
                a += randint(1, 5) if a <= 99 else 99
                self.update_signal.emit(a, '', f'{localize.unpacking} - {self.file_name}...', False)
                sleep(randint(1, 5))

        self.update_signal.emit(100, '', localize.done, True)
