import os
from datetime import datetime


def file_reaper(func_name):

    def wrapper(*args, **kwargs):
        start = datetime.now()
        func_name(*args, **kwargs)
        end = datetime.now()
        print(func_name, end-start)

    return wrapper


class Unpacker:

    def __init__(self):
        self.out_dir = 'E:/unpack'
        self.path_to_root = os.path.abspath(__file__).split('source')[0]

    @file_reaper
    def quick_bms(self, file_name, script_name):
        os.system(f'{self.path_to_root}\\data\\QuickBMS\\quickbms.exe '
                  f'"{self.path_to_root}\\{script_name}" '
                  f'"{file_name}" "{self.out_dir}"')

    @file_reaper
    def unity(self, folder_name):
        print(f'{self.path_to_root}\\data\\AssetStudio\\AssetStudioCLI.exe '
              f'"{folder_name}" "{self.out_dir}" --game Normal')
        os.chdir(f'{self.path_to_root}\\data\\AssetStudio\\')
        os.system('AssetStudioCLI.exe '
                  f'"{folder_name}" "{self.out_dir}" --game Normal')
        os.chdir(f'{self.path_to_root}')

    @file_reaper
    def unreal(self):
        pass
