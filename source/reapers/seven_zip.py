
from subprocess import Popen, PIPE
from time import sleep
from random import randint

from source.reaper import Reaper
from source.ui import localize


class SevenZIP(Reaper):

    def run(self):
        a = 0

        zip7 = Popen(f'{self.path_to_root}data\\7zip\\7z.exe x '
                    f'-o"{self.output_folder}" "{self.file_name}"',
                    stdout=PIPE, stderr=PIPE, encoding='utf-8')

        while zip7.poll() is None:
            a += randint(1, 5) if a <= 99 else 99
            self.update_signal.emit(a, '', f'{localize.unpacking} - {self.file_name}...', False)
            sleep(randint(1, 5))

            # TODO: WTF? Why don't read output from 7zip?
            # out1 = zip7.stdout.readline().strip()
            # out2 = zip7.stderr.readline().strip()
            # print(out1, out2)
            # self.update_signal.emit(50, '', f'{localize.saving} - ...', False)

        zip7.kill()
        self.update_signal.emit(100, '', localize.done, True)
