import os
import configparser
from source.reapers import locres

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

    def quick_bms(self, file_name, script_name):
        self.quick_bms2(file_name, script_name)

    def quick_bms2(self, file_name, script_name):

        if file_name:
            # bms = Popen(f'{self.path_to_root}data/QuickBMS/quickbms.exe '
            #             f'"{self.path_to_root}{script_name}" '
            #             f'"{file_name}" '
            #             f'"{self.out_dir}"',
            #             stdout=PIPE, stderr=PIPE, encoding='utf-8')
            #
            # out_data, err_data = bms.communicate()
            #
            # print(out_data)
            # print(err_data)
            print(script_name)

            os.system(f'{self.path_to_root}data/QuickBMS/quickbms.exe '
                      f'"{self.path_to_root}{script_name}" '
                      f'"{file_name}" "{self.out_dir}"')

    def unity(self, folder_name):

        if folder_name:
            os.chdir(f'{self.path_to_root}data/AssetStudio/')
            os.system('AssetStudioCLI.exe '
                      f'"{folder_name}" "{self.out_dir}" --game Normal')
            os.chdir(f'{self.path_to_root}')

    def unreal(self, file_name, key=''):
        if file_name:
            exp = file_name.split('.')[-1]

            match exp:
                case 'locress':
                    locres.locressImport(file_name)
                case 'txt':
                    locres.locressExport(file_name)
                case 'umod':
                    self.quick_bms2(file_name, "/data/scripts/unreal_umod.bms")
                case 'pak':
                    self.string_replace(self.path_to_root + "/data/scripts/unreal_tournament_4.bms",
                                        f'set AES_KEY binary "{key}"', 11)
                    self.quick_bms2(file_name, "/data/scripts/unreal_tournament_4.bms")
                case _:
                    os.system(f'{self.path_to_root}/data/unreal_tools/extract.exe '
                              f'-extract -out="{self.out_dir}" "{file_name}"')
