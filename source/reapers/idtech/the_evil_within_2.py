import os
from icecream import ic
from collections import namedtuple

from source.reaper import Reaper, file_reaper
from source.codecs.zip_methods import ZipMethods


class Within(Reaper):

    @file_reaper
    def run(self):
        base_name = os.path.basename(self.file_name)
        ext = base_name.split('.')[-1]
        dir_name = os.path.dirname(self.file_name)
        index_file = f"{dir_name}\\ptr\\{base_name.replace(ext, 'ptr')}" if 'ptr' not in self.file_name else self.file_name
        resources_file = self.file_name.replace('ptr', '') + 'pkr' if 'pkr' not in self.file_name else self.file_name

        temp_file = f"{self.output_folder}\\{base_name}.tmp"
        ic(index_file)

        if not os.path.exists(index_file):
            self.update_pb(0, 0, '')
            return

        with open(index_file, 'rb') as ix:
            ix.seek(0x10)
            zip_list = ix.read()

        with open(temp_file, 'wb') as tf:
            tf.write(zip_list)

        self.unzip(temp_file, ZipMethods.DEFLATE_NOERROR)
        FileList = namedtuple('FileList',
                              ['file_name', 'offset', 'zip_size', 'unzip_size'])
        file_list = []

        with open(temp_file, 'rb') as nix:
            file_count = int.from_bytes(nix.read(4), byteorder="little")
            nix.seek(12)
            step_count1 = int.from_bytes(nix.read(4), byteorder="little")
            step_count2 = int.from_bytes(nix.read(4), byteorder="little")
            nix.seek(step_count1 * 4 + step_count2 * 4, 1)
            file_list_size = int.from_bytes(nix.read(4), byteorder="little")
            nix.seek(4, 1)
            fl = [name.decode('utf-8') for name in nix.read(file_list_size).split(b'\0')]

            for i in range(file_count):
                file_list.append(
                    FileList(
                        fl[int.from_bytes(nix.read(4), byteorder="little")],
                        int.from_bytes(nix.read(4), byteorder="little"),
                        int.from_bytes(nix.read(4), byteorder="little"),
                        int.from_bytes(nix.read(4), byteorder="little"))
                )

            ic(file_list)

        with open(resources_file, "rb") as res_file:
            magic = res_file.read(4)

            if not self.magic([b'\x83\x11\xBA\xFC', ], magic, 'The Evil Within 2'):
                self.update_pb(0, 0, '')
                return

            for i, f in enumerate(file_list):
                path = f"{self.output_folder}\\{f.file_name}"
                res_file.seek(f.offset)
                self.file_save(path, res_file.read(f.zip_size))
                self.unzip(path, ZipMethods.DEFLATE_NOERROR)
                self.update_pb(file_count, i + 1, f.file_name)
