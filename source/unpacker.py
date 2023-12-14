import os
import configparser

from source.reaper import file_reaper

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class Unpacker:

    def __init__(self):
        self.out_dir = setting['Main']['out_path']
        self.path_to_root = os.path.abspath(__file__).split('source')[0]

    @staticmethod
    def string_replace(file_path, new_string, string_num):

        with open(file_path, 'r', encoding='utf-8') as script:
            lines = script.readlines()

        lines[int(string_num)] = new_string

        with open(file_path, 'w') as new:
            new.writelines(lines)

    @file_reaper
    def seven_zip(self, file_name):
        os.system(f'{self.path_to_root}data\\7zip\\7z.exe x -o"{self.out_dir}" "{file_name}"')

    @file_reaper
    def unity(self, folder_name):

        if folder_name:
            os.chdir(f'{self.path_to_root}data/AssetStudio/')
            os.system('AssetStudioCLI.exe '
                      f'"{folder_name}" "{self.out_dir}" --game Normal')
            os.chdir(f'{self.path_to_root}')

    @file_reaper
    def unreal(self, file_names, key=''):

        for file_name in file_names:
            if file_name:
                exp = file_name.split('.')[-1]

                match exp:
                    case 'umod':
                        self.quick_bms2(file_name, "/data/scripts/unreal_umod.bms")
                    case 'pak':
                        self.string_replace(self.path_to_root + "/data/scripts/unreal_tournament_4.bms",
                                            f'set AES_KEY binary "{key}"', 11)
                        self.quick_bms2(file_name, "/data/scripts/unreal_tournament_4.bms")
                    case _:
                        os.system(f'{self.path_to_root}/data/unreal_tools/extract.exe '
                                  f'-extract -out="{self.out_dir}" "{file_name}"')
