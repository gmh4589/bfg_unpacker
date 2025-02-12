import os
import shutil
from subprocess import Popen, PIPE
from threading import Thread
from random import randint
from time import sleep

from icecream import ic

from source.reaper import Reaper, file_reaper, OutReader
from source.ui import localize


class Unreal(Reaper, OutReader):
    # TODO: Need testing:
    #  Unreal Engine 1 - need to test;
    #  Unreal Engine 2 - need to test;
    #  Unreal Engine 3 - is working (tested on Dishonored);
    #  Unreal Engine 4 - is working;
    #  Unreal Engine 5 - need to test;

    key = ''
    output = []
    out = ''
    err = ''
    end = False

    @file_reaper
    def run(self):
        size = 0
        ext = self.file_name.split('.')[-1]
        percent = 0

        match ext:
            case 'umod':
                size = os.path.getsize(self.file_name)
                version = 0
                unreal = Popen(f'{self.path_to_root}data/QuickBMS/quickbms.exe -K '
                               f"{self.path_to_root}data/scripts/unreal_umod.bms "
                               f'"{self.file_name}" "{self.output_folder}"',
                               stdout=PIPE, stderr=PIPE, encoding='utf-8', shell=False)
            case 'pak':
                version = 4
                unreal = Popen(f'"{self.path_to_root}/data/unreal_tools/ue4/repak.exe" '
                               f'{f"--aes-key {self.key} " if self.key else ""}'
                               f'unpack "{self.file_name}"',
                               stdout=PIPE, stderr=PIPE, encoding='utf-8', shell=False)

            case _:
                version = 3
                unreal = Popen(f'{self.path_to_root}/data/unreal_tools/ue3/extract.exe '
                               f'-extract -out="{self.output_folder}" "{self.file_name}" ',
                               stdout=PIPE, stderr=PIPE, encoding='utf-8', shell=False)

        Thread(target=self.out_reader, args=[unreal,], daemon=True).start()
        Thread(target=self.err_reader, args=[unreal,], daemon=True).start()

        while unreal.poll() is None:

            if version == 0:

                try:
                    percent = int((100 / size) * int(self.output[0], 16))
                    print(f"{percent}% {self.output[-1]}")
                    self.update_signal.emit(percent, '', f'{localize.saving} - {self.output[-1]}...', False)
                except (ValueError, IndexError, ZeroDivisionError):
                    pass

            elif version == 3:

                if len(self.output) == 3:
                    current_f, all_f = self.output[1].split('/')
                    percent = int((100 / int(all_f)) * int(current_f))
                    self.update_signal.emit(percent, f'{self.output[1]}', f'{localize.saving} - {self.output[1]}...', False)

            elif version == 4:
                sleep(randint(1, 3))

                percent += randint(0, 2)
                percent = 95 if percent > 95 else percent

                self.update_signal.emit(percent, f'{percent} %',
                                        'Wait, unpacked in process...', False)

        self.end = True

        if version == 4:
            self.update_signal.emit(99, "99 %, almost done...", f'{localize.wait}, files is moving...', False)

            try:
                shutil.move(''.join(self.file_name.split('.')[:-1]), self.output_folder)
            except FileNotFoundError:
                ic('Version of Unreal Engine 4 is not supported or wrong AES key')
                print('Version of Unreal Engine 4 is not supported or wrong AES key')

        self.update_signal.emit(100, '', localize.done, True)
