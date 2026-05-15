from source.reaper import Reaper, file_reaper
from collections import namedtuple


class ClockTower3(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            file_count = int.from_bytes(file.read(4), byteorder='little')
            # file_data_start = int.from_bytes(file.read(4), byteorder='little')
            file.seek(0x800)
            FileEntry = namedtuple('FileEntry', ['name', 'size', 'offset'])
            entries = []

            for _ in range(file_count):
                name = file.read(0x10).decode("ascii").rstrip("\0")
                unk1 = file.read(0x4)  
                size = int.from_bytes(file.read(4), byteorder='little')
                offset = int.from_bytes(file.read(4), byteorder='little') * 0x800
                entries.append(FileEntry(name, size, offset))
                unk2 = file.read(0x4)  

            file.seek(0xE800)
            
            for i, entry in enumerate(entries):
                file.seek(entry.offset)
                data = file.read(entry.size)
                path = f"{self.output_folder}\\{entry.name}"
                self.file_save(path, data)
            
                self.update_pb(file_count, i, entry.name)

