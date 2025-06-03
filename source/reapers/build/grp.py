import os
from icecream import ic
from collections import namedtuple
from source.reaper import Reaper, file_reaper
from source.ui import localize
# TODO: Add to archive creation support


class GRPExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as grp_file:
            magic = grp_file.read(4)

            if magic != b'KenS':
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Build Engine'), True)
                return

            grp_file.seek(0xC)
            file_count = int.from_bytes(grp_file.read(4), byteorder="little")
            FileList = namedtuple('FileList',
                                  ['name', 'size'])
            file_list = []

            for i in range(file_count):
                name = grp_file.read(0xC).decode("ascii").split("\0")[0]
                size = int.from_bytes(grp_file.read(4), byteorder="little")
                file_list.append(FileList(name, size))

            ic(file_list)

            for j, file in enumerate(file_list):
                self.file_save(os.path.join(self.output_folder, file.name), grp_file.read(file.size))
                self.update_pb(file_count, j + 1, file.name)
