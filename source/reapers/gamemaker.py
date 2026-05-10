import os
from source.reaper import Reaper, file_reaper


class GMUnpack(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if not self.magic([b'FORM', ], magic, 'Game Maker File'):
                return

            file_size = int.from_bytes(file.read(4), byteorder="little") + 8
            used_chunks = ()
            counter = {}

            while file.tell() < file_size:
                chunk_name = file.read(4).decode('utf-8', errors='ignore')
                chunk_size = int.from_bytes(file.read(4), byteorder="little")

                if chunk_name in used_chunks:
                    chunks = int.from_bytes(file.read(4), byteorder="little")
                    sizes = [int.from_bytes(file.read(4), byteorder="little") for _ in range(chunks)]
                    file.seek((chunks * 16) + 12, 1)

                    for size in sizes:
                        that_chunk = counter.get(chunk_name, 0)
                        counter[chunk_name] = that_chunk + 1
                        os.makedirs(f"{self.output_folder}/{chunk_name}", exist_ok=True)
                        data = file.read(size)

                        with open(f"{self.output_folder}/{chunk_name}/{that_chunk}.png", 'wb') as nf:
                            nf.write(data)

                else:
                    that_chunk = counter.get(chunk_name, 0)
                    counter[chunk_name] = that_chunk + 1
                    os.makedirs(f"{self.output_folder}/{chunk_name}", exist_ok=True)

                    with open(f"{self.output_folder}/{chunk_name}/{that_chunk}.{chunk_name}", 'wb') as nf:
                        nf.write(file.read(chunk_size))

                self.update_pb(file_size, file.tell(), chunk_name)
