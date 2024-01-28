
import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class ARCExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as arc_file:
            magic = arc_file.read(4)

            if magic not in (b'ARC\x00', b'\x00CRA'):
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'ARC'), True)
                return

            version = int.from_bytes(arc_file.read(2), byteorder="little")
            file_count = int.from_bytes(arc_file.read(2), byteorder="little")

            if version in (4, 8):
                # 'unzip_dynamic'
                c_num = 167
            elif version == 17:
                ic('XMemDecompress 0x8000')  # TODO: WTF?
                c_num = 0
            else:
                # 'zlib_noerror'
                c_num = 1

            for i in range(file_count):
                name = arc_file.read(64).decode("ascii").rstrip("\0")
                type_hash = int.from_bytes(arc_file.read(4), byteorder="little")
                file_size = int.from_bytes(arc_file.read(4), byteorder="little")
                flags = arc_file.read(4)
                offset = int.from_bytes(arc_file.read(4), byteorder="little")
                here = arc_file.tell()
                path = os.path.join(self.output_folder, name + '.dat')
                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as new_file:
                    arc_file.seek(offset)
                    new_file.write(arc_file.read(file_size))

                if c_num:
                    self.unzip(path, c_num, get_ext=True)

                arc_file.seek(here)
                ic(name)

                print(f"{i + 1}/{file_count} {name}")
                self.update_signal.emit(int(100 / file_count * (i + 1)), f'{i}/{file_count}',
                                        f'{localize.saving} - {name}...', False)

        # os.remove(f"{self.output_folder}/ZLIB.dmp")
        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
