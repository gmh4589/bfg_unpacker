import os
from icecream import ic

from source.reaper import Reaper, file_reaper, zip_methods
from source.ui import localize


class ZipScanner(Reaper):

    @file_reaper
    def run(self):

        size = os.path.getsize(self.file_name)
        method_count = len(zip_methods)

        for i in zip_methods.keys():
            self.unzip(f_name=self.file_name, c_num=i, test=True)
            name = zip_methods[i]
            print(f'Tested algorithm: {name}')
            ic(f'Tested algorithm: {name}')
            test_file = os.path.join(self.output_folder, name + '.dmp')
            sus = True

            if os.path.exists(test_file):
                test_file_size = os.path.getsize(test_file)

                if size > test_file_size:
                    os.remove(test_file)
                    sus = False

            else:
                sus = False

            print(f'Dump create: {name}.dmp') if sus else print(f'Filed to unzip {name}')
            ic(f'Dump create: {name}.dmp') if sus else ic(f'Filed to unzip {name}')

            self.update_signal.emit(int(100 / method_count * i), f'{i}/{method_count}',
                                    f'Testing - {name}...', False)

        self.update_signal.emit(100, f'{method_count}/{method_count}', localize.done, True)
