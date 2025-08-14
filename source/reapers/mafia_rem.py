from  collections import namedtuple
from source.reaper import Reaper, file_reaper


class PCKGUnpacker(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if not self.magic([b'PCKG', ], magic, 'Mafia Remake File'):
                return

            # version = int.from_bytes(file.read(4), byteorder="little")
            file.seek(4, 1)
            file_count = int.from_bytes(file.read(4), byteorder="little")
            file.seek(4, 1)
            FileData = namedtuple('FilaData',
                                  ['hash_summ', 'offset', 'size', 'zip_size'])
            file_data = []

            for i in range(file_count):
                file_data.append(FileData(
                    hash_summ = int.from_bytes(file.read(8), byteorder="little"),
                    offset = int.from_bytes(file.read(8), byteorder="little"),
                    size = int.from_bytes(file.read(4), byteorder="little"),
                    zip_size = int.from_bytes(file.read(4), byteorder="little")
                ))
                file.seek(8, 1)

            for j, f in enumerate(file_data):
                file.seek(f.offset)
                data = file.read(f.zip_size)
                ext = self.get_ext(data[:4])

                with open(f"{self.output_folder}\\{f.hash_summ}.{ext}", 'wb') as nf:
                    nf.write(data)

                self.update_pb(file_count, j + 1, f"{f.hash_summ}.{ext}")
