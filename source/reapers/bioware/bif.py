from collections import namedtuple

from source.reaper import Reaper, file_reaper
from source.reapers.bioware.ext import get_ext


class BifKey(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bif:
            magic = bif.read(4)

            if not self.magic([b'BIFF', ], magic, 'Infinity Engine'):
                return

            version = bif.read(4).decode('utf-8', errors='ignore')
            file_count = int.from_bytes(bif.read(4), 'little')
            unk = int.from_bytes(bif.read(4), 'little')
            start_data = int.from_bytes(bif.read(4), 'little')
            bif.seek(start_data)

            FileData = namedtuple('FileData',
                                  ['index', 'unk', 'offset', 'file_size', 'file_type'])
            file_data = []

            for _ in range(file_count):
                file_data.append(
                    FileData(
                        int.from_bytes(bif.read(4), 'little'),  # Index of file
                        int.from_bytes(bif.read(4), 'little') if version == 'V1.1' else None,  # Unknown data (always zeros)
                        int.from_bytes(bif.read(4), 'little'),  # Start data offset
                        int.from_bytes(bif.read(4), 'little'),  # File Size
                        int.from_bytes(bif.read(4), 'little')   # File Type Index
                    )
                )
            
            for i, f in enumerate(file_data):
                bif.seek(f.offset)
                data = bif.read(f.file_size)
                ext = get_ext.get(f.file_type, 'dat')
                fn = f"{str(hex(f.file_type)) + '_' if ext == 'dat' else ''}{str(i).rjust(8, '0')}.{ext}"
                self.file_save(f"{self.output_folder}\\{fn}", data)
                self.update_pb(file_count, i + 1, fn)

