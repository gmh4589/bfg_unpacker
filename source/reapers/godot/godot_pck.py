
import os
from icecream import ic
from source.reaper import Reaper, file_reaper
from source.reapers.godot.godot_ctex import GodotCTEX
from collections import namedtuple


class GodotPCK(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as pck_file:
            magic = pck_file.read(4)

            if not self.magic([b'GDPC',], magic, 'Godot Engine Archive'):
                return

            version_1 = int.from_bytes(pck_file.read(4), byteorder="little")
            version_2 = int.from_bytes(pck_file.read(4), byteorder="little")
            version_3 = int.from_bytes(pck_file.read(4), byteorder="little")
            version_4 = int.from_bytes(pck_file.read(8), byteorder="little")
            start_data = int.from_bytes(pck_file.read(4), byteorder="little")

            version = f"{version_2}.{version_3}.{version_4}"
            ic(f'Godot version is {version}')

            jump_pos = 0x54 if version_1 == 1 else 0x60

            pck_file.seek(jump_pos)
            file_count = int.from_bytes(pck_file.read(4), byteorder="little")
            file_data = namedtuple("FileData",
                                   ['name', 'offset', 'size', 'hash'])
            file_list = []

            for _ in range(file_count):
                name_long = int.from_bytes(pck_file.read(4), byteorder="little")
                file_list.append(
                    file_data(
                        pck_file.read(name_long).strip(b'\0').decode('utf-8'),  # Name
                        int.from_bytes(pck_file.read(8), byteorder="little"),   # Offset
                        int.from_bytes(pck_file.read(8), byteorder="little"),   # Size
                        pck_file.read(0x10 if version_1 == 1 else 0x14)         # Hash
                    )
                )

            for i, file in enumerate(file_list):
                pck_file.seek(file.offset + start_data)
                name = file.name if version_1 == 2 else file.name.replace('res://', '')
                path = f"{self.output_folder}\\{name}"
                self.file_save(path, pck_file.read(file.size))
                
                if self.setting['Main']['save_original_images'] in ['1', '2']:

                    if 'ctex' in path:
                        ctex2webp = GodotCTEX()
                        ctex2webp.file_name = path
                        ctex2webp.output_folder = os.path.dirname(path)
                        ctex2webp.run()

                        if self.setting['Main']['save_original_images'] == '1':
                            os.remove(path)

                self.update_pb(len(file_list), i + 1, file.name)

