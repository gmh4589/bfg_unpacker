import os
from icecream import ic
from source.reaper import Reaper, file_reaper


class Splitter(Reaper):
    start_data: int = 0
    header: bytes = b'\0\0\0\0'
    splitter: bytes = b'\0\0\0\0'
    file_type: str = 'Random Game'
    ext: str = 'dat'

    @file_reaper
    def run(self):
        
        param = self.script_name.split(', ')
        self.start_data = int(param[0])
        self.header = int(param[1]).to_bytes(4, byteorder='little')
        self.splitter = int(param[2]).to_bytes(4, byteorder='little')
        self.file_type = param[3]
        self.ext = param[4]

        ic(
            self.start_data,
            self.header,
            self.splitter,
            self.file_type,
            self.ext)

        b_name = os.path.basename(self.file_name).split('.')[-2]

        with open(self.file_name, 'rb') as nf:

            if not self.magic([self.header,], nf.read(4), self.file_type):
                return

            nf.seek(self.start_data)
            files_data = nf.read().split(self.splitter)
            files_data.pop(0)
            file_count = len(files_data)

        for i, f in enumerate(files_data):
            name = f"{b_name}_{i:08}.{self.ext}"
            full_name = os.path.join(self.output_folder, name)

            with open(full_name, 'wb') as nf:
                nf.write(self.splitter + f)

            self.update_pb(file_count, i + 1, name)
