import os
from source.reaper import Reaper, file_reaper


class GodotCTEX(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as ctex_file:
            magic = ctex_file.read(4)

            if not self.magic([b'GST2',], magic, 'Godot Engine Texture'):
                return

            name = f"{self.output_folder}\\{os.path.basename(ctex_file.name).split('.')[0]}.webp"
            ctex_file.seek(0x34)
            data_long = int.from_bytes(ctex_file.read(4), byteorder="little")
            self.file_save(name, ctex_file.read(data_long))

            self.update_pb(1, 1, name)

