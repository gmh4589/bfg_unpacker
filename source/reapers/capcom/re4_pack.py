import os
from subprocess import Popen

from icecream import ic

from source.reaper import Reaper, file_reaper


class Re4Pack(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if magic == b'RDLX':
                yz2_path = (self.output_folder + "\\" + os.path.basename(self.file_name)).replace(".lfs", "").replace('/', '\\')

                if not os.path.exists(yz2_path):
                    run = f'"{self.path_to_root}\\data\\tools\\re4lfs.exe" "{self.file_name}" "{yz2_path}"'
                    ic(run)
                    Popen(run, shell=True).wait()

                self.file_name = yz2_path
                self.run()
                return None

            file_count = int.from_bytes(file.read(4), byteorder="little")
            offsets = []
            ic(file.name, file_count)

            for j in range(file_count):
                offsets.append(int.from_bytes(file.read(4), byteorder="little"))

            for i, offset in enumerate(offsets):
                file.seek(offset)
                size = int.from_bytes(file.read(4), byteorder="little")
                file.seek(0xC, 1)
                magic = file.read(4)
                name = f"{i:04}.{self.get_ext(magic)}"

                path = os.path.join(self.output_folder, name)
                ic(path)

                with open(path, 'wb') as new_file:
                    new_file.write(magic + file.read(size))

                self.update_pb(file_count, i + 1, name)

