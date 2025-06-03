import os
from source.reaper import Reaper, file_reaper
from source.ui import localize


class W2Cache(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if not self.magic([b'RDHS', ], magic, 'RED Engine'):
                return

            file_count = int.from_bytes(file.read(4), byteorder="little")
            file.seek(0x10)

            for i in range(file_count):
                file.seek(4, 1)
                size = int.from_bytes(file.read(4), byteorder="little")
                ext = self.get_ext(magic)
                path = os.path.join(self.output_folder, f"{i}.{ext}")
                file.seek(8, 1)
                self.file_save(path, file.read(size))
                self.update_pb(file_count, i + 1, f"{i}.{ext}")

        self.update_signal.emit(100, '', localize.done, True)
