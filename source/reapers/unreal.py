import os
from subprocess import Popen, PIPE
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class Unreal(Reaper):

    def __init__(self):
        super().__init__()
        self.key = ''

    @staticmethod
    def string_replace(file_path, new_string, string_num):

        with open(file_path, 'r', encoding='utf-8') as script:
            lines = script.readlines()

        lines[int(string_num)] = new_string

        with open(file_path, 'w') as new:
            new.writelines(lines)

    @file_reaper
    def run(self):
        size = 0
        exp = self.file_name.split('.')[-1]

        match exp:
            case 'umod':
                size = os.path.getsize(self.file_name)
                unreal = Popen(f'{self.path_to_root}data/QuickBMS/quickbms.exe -K '
                               f"{self.path_to_root}data/scripts/unreal_umod.bms "
                               f'"{self.file_name}" "{self.output_folder}"',
                               stdout=PIPE, stderr=PIPE, encoding='utf-8')
            case 'pak':
                self.string_replace(f"{self.path_to_root}data/scripts/unreal_tournament_4.bms",
                                    f'set AES_KEY binary "{self.key}"', 11)
                size = os.path.getsize(self.file_name)
                unreal = Popen(f'{self.path_to_root}data/QuickBMS/quickbms.exe -K '
                               f"{self.path_to_root}data/scripts/unreal_tournament_4.bms "
                               f'"{self.file_name}" "{self.output_folder}"',
                               stdout=PIPE, stderr=PIPE, encoding='utf-8')
            case _:
                unreal = Popen(f'{self.path_to_root}/data/unreal_tools/extract.exe '
                               f'-extract -out="{self.output_folder}" "{self.file_name}"',
                               stdout=PIPE, stderr=PIPE, encoding='utf-8')

        while True:
            out1 = unreal.stdout.readline().strip()
            o = out1.split(' ')

            if size:
                try:
                    percent = int(100 / size * int(o[0], 16))
                    print(f"{percent}% {o[-1]}")
                    self.update_signal.emit(percent, '', f'{localize.saving} - {o[-1]}...', False)
                except (ValueError, IndexError):
                    pass
            else:
                print(out1)
                ic(out1)
                self.update_signal.emit(50, '', f'{localize.saving} - ...', False)

            if not out1:
                if not size: unreal.kill()
                break

        self.update_signal.emit(100, '', localize.done, True)
