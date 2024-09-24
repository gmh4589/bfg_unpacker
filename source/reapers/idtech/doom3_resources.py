import os
from source.reaper import Reaper, file_reaper
from source.reapers.idtech.bimage import Bimage2DDS


class Doom3BFG(Reaper):
    # For unpack *.resources files from Doom 3 BFG Edition

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bfg:
            magic = bfg.read(4)

            if not self.magic([b'\xD0\x00\x00\x0D', ], magic, 'idTech streamed'):
                return

            offset = int.from_bytes(bfg.read(4), byteorder="big")
            bfg.seek(offset)
            file_count = int.from_bytes(bfg.read(4), byteorder="big")

            for i in range(file_count):
                name_len = int.from_bytes(bfg.read(4), byteorder="little")
                name = bfg.read(name_len).decode("utf-8", errors='ignore')
                offset = int.from_bytes(bfg.read(4), byteorder="big")
                size = int.from_bytes(bfg.read(4), byteorder="big")

                path = os.path.join(self.output_folder, name)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                here = bfg.tell()
                bfg.seek(offset)

                with open(path, 'wb') as new_file:
                    new_file.write(bfg.read(size))

                if self.setting['Main']['save_original_images'] in ['1', '2']:

                    if 'bimage' in path:
                        bimage2dds = Bimage2DDS()
                        bimage2dds.file_name = path
                        bimage2dds.output_folder = os.path.dirname(path)
                        bimage2dds.run()

                if self.setting['Main']['save_original_images'] == '1':
                    os.remove(path)

                bfg.seek(here)
                self.update_pb(file_count, i + 1, name)
