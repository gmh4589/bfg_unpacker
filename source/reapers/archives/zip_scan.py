import os
from subprocess import Popen
from threading import Timer

from icecream import ic
from source.reaper import Reaper, file_reaper
from source.codecs.zip_methods import ZipMethods
from source.ui import localize


class ZipScanner(Reaper):

    @file_reaper
    def run(self):

        size = os.path.getsize(self.file_name)
        method_dict = ZipMethods.codec_list()
        method_count = len(method_dict)

        for name, i in method_dict.items():
            script = (f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" '
                      f'-o -a "{i}" '
                      f'"{self.path_to_root}\\data\\QuickBMS\\comtype_scan2.bms" '
                      f'"{self.file_name}" "{self.output_folder}"').replace("/", "\\")

            proc = Popen(script)
            Timer(10, proc.terminate).start()
            proc.wait()

            print(f'{localize.test_algorythm}: {name}')
            ic(f'{localize.test_algorythm}: {name}')
            test_file = os.path.join(self.output_folder, name + '.dmp')
            sus = True

            if os.path.exists(test_file):
                test_file_size = os.path.getsize(test_file)

                if size > test_file_size or test_file_size == 0:
                    os.remove(test_file)
                    sus = False

            else:
                sus = False

            print(f'{localize.dump_create}: {name}.dmp') if sus else print(f'{localize.filed_to_unzip} {name}')
            ic(f'{localize.dump_create}: {name}.dmp') if sus else ic(f'{localize.filed_to_unzip} {name}')

            self.update_signal.emit(int(100 / method_count * i), f'{i}/{method_count}',
                                    f'{localize.testing} - {name}...', False)

        self.update_signal.emit(100, f'{method_count}/{method_count}', localize.done, True)
