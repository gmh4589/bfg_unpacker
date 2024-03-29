
from random import randint
from time import sleep
from icecream import ic
from subprocess import Popen, PIPE

from source.reaper import Reaper, file_reaper
from source.ui import localize


class OtherProg(Reaper):

    def __init__(self):
        super().__init__()
        self.program_name = 'test.exe'
        self.percent_index = 0
        self.percent_type = 'int'

        # Percent type:
        # int = real int digit
        # l_first = left digit current, right digit all
        # r_first = right digit current, left digit all
        # 50 = all time 50 percent
        # else = random

        self.percent_del = '\\'
        self.name_index = 1
        self.first_arg = ''
        self.second_arg = ''
        self.splitter = ' '
        self.real_pb = True

    @file_reaper
    def run(self):
        arguments = (f'"{self.path_to_root}data\\{self.program_name}" {self.first_arg} '
                     f'"{self.file_name}" {self.second_arg}').replace('/', '\\')

        prg = Popen(arguments, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        ic(self.program_name)
        ic(self.first_arg)
        ic(self.file_name)
        ic(self.second_arg)
        ic(arguments)

        if self.real_pb:

            if self.percent_type == '50':
                self.update_signal.emit(50, '', f'{localize.saving} - {self.file_name}...', False)

            while True:
                out = prg.stdout.readline().strip()
                o = out.split(self.splitter)
                percent = 0
                ic(out)
                ic(prg.stderr.readline().strip())

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

                if not out:
                    prg.kill()
                    break

        elif self.real_pb is None:
            pass

        else:
            a = 0

            while prg.poll() is None:
                a += randint(1, 5) if a <= 99 else 99
                self.update_signal.emit(a, '', f'{localize.unpacking} - {self.file_name}...', False)
                sleep(randint(1, 5))

        self.update_signal.emit(100, '', localize.done, True)
