
# import os
# from subprocess import Popen, PIPE
# from threading import Thread
#
# from source.reaper import Reaper, file_reaper, OutReader
# from source.ui import localize
#
#
# class SevenZIP(Reaper, OutReader):
#
#     @file_reaper
#     def run(self):
#         _, was_files, _ = self.folderSize(self.output_folder)
#         os.system(f'{self.path_to_root}\\data\\7zip\\7z.exe l "{self.file_name}" >> 7z.examples.log')
#
#         with open('7z.examples.log', 'r', encoding='utf-8') as f:
#             self.out = f.read()
#
#         os.remove('7z.examples.log')
#         current_file = 1
#         files_count = int(self.out.split(' ')[-4])
#
#         zip7 = Popen(f'{self.path_to_root}\\data\\7zip\\7z.exe x '
#                      f'-o"{self.output_folder}" "{self.file_name}"',
#                      stdout=PIPE, stderr=PIPE, encoding='utf-8', errors='ignore', shell=False)
#
#         Thread(target=self.out_reader, args=[zip7,], daemon=True).start()
#         Thread(target=self.err_reader, args=[zip7,], daemon=True).start()
#
#         while current_file < files_count:
#             _, current_file, _ = self.folderSize(self.output_folder, was_files)
#             percent = int(100 / files_count * current_file)
#             self.update_signal.emit(percent, f'{current_file}\\{files_count}', f'{localize.saving} ...', False)
#
#         self.end = True
#         self.update_signal.emit(100, '', localize.done, True)

from subprocess import Popen, PIPE
from threading import Thread
from source.reaper import Reaper, file_reaper, OutReader
from source.ui import localize


class SevenZIP(Reaper, OutReader):

    def __init__(self):
        super().__init__()
        self.end = False

    @file_reaper
    def run(self):
        self.file_name = self.file_name.replace('/', '\\')
        _, was_files, _ = self.folderSize(self.output_folder)

        zip7 = Popen(f'{self.path_to_root}\\data\\7zip\\7z.exe x '
                     f'-o"{self.output_folder}" "{self.file_name}"',
                     stdout=PIPE, stderr=PIPE, encoding='utf-8', errors='ignore', shell=False)

        Thread(target=self.out_reader, args=[zip7,], daemon=True).start()
        Thread(target=self.err_reader, args=[zip7,], daemon=True).start()

        while zip7.poll() is None:
            _, current_file, _ = self.folderSize(self.output_folder, was_files)
            self.update_signal.emit(0, '', f'{localize.saving}: {current_file} {localize.file}', False)

        self.end = True
        self.update_signal.emit(100, '', localize.done, True)
