import os
from subprocess import Popen, PIPE
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class Unreal(Reaper):
    # TODO: Need testing

    def __init__(self):
        super().__init__()
        self.key = ''

    @file_reaper
    def run(self):
        size = 0
        exp = self.file_name.split('.')[-1]

        match exp:
            case 'umod':
                size = os.path.getsize(self.file_name)
                version = 0
                unreal = Popen(f'{self.path_to_root}data/QuickBMS/quickbms.exe -K '
                               f"{self.path_to_root}data/scripts/unreal_umod.bms "
                               f'"{self.file_name}" "{self.output_folder}"',
                               stdout=PIPE, stderr=PIPE, encoding='utf-8')
            case 'pak':
                version = 4

                with open(f'{self.path_to_root}\\data\\scripts\\unreal_tournament_4.bms', 'r') as bms:
                    script_data = bms.read()

                    if self.key:
                        script_data = script_data.replace('set AES_KEY binary ""', f'set AES_KEY binary "{self.key}"')

                with open(f'{self.path_to_root}\\data\\scripts\\unreal_tournament_4_temp.bms', 'w') as temp_bms:
                    temp_bms.write(script_data)

                size = os.path.getsize(self.file_name)
                unreal = Popen(f'{self.path_to_root}data/QuickBMS/quickbms.exe -K '
                               f"{self.path_to_root}data/scripts/unreal_tournament_4_temp.bms "
                               f'"{self.file_name}" "{self.output_folder}"',
                               stdout=PIPE, stderr=PIPE, encoding='utf-8')
            case _:
                version = 3
                unreal = Popen(f'{self.path_to_root}/data/unreal_tools/extract.exe '
                               f'-extract -out="{self.output_folder}" "{self.file_name}" ',
                               stdout=PIPE, stderr=PIPE, encoding='utf-8')

        while unreal.poll() is None:
            out = unreal.stdout.readline().split(' ')

            if version in (0, 4):

                try:
                    percent = int((100 / size) * int(out[0], 16))
                    print(f"{percent}% {out[-1]}")
                    self.update_signal.emit(percent, '', f'{localize.saving} - {out[-1]}...', False)
                except (ValueError, IndexError):
                    pass

            elif version == 3:
                ic(out)

                if len(out) == 3:
                    current_f, all_f = out[1].split('/')
                    ic(current_f, all_f)
                    percent = int((100 / int(all_f)) * int(current_f))
                    self.update_signal.emit(percent, f'{out[1]}', f'{localize.saving} - {out[1]}...', False)

        self.update_signal.emit(100, '', localize.done, True)

