import os
import zlib
from collections import namedtuple

from source.reaper import Reaper, file_reaper
from source.ui import localize


class BundleUnpack(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bundle:
            magic = bundle.read(8)

            if magic != b'POTATO70':
                print(localize.not_correct_file.replace('%%', 'Red Engine'))
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Red Engine'), True)
                return

            bundle.seek(0x13c)
            first_file_offset = int.from_bytes(bundle.read(4), byteorder="little")
            file_count = int((first_file_offset - 32) / 320)
            bundle.seek(0x20)

            FileList = namedtuple('FileList',
                                  ['name', 'hash', 'unzip_size', 'zip_size', 'offset', 'data'])
            file_list = []

            for i in range(file_count):
                file_list.append(
                    FileList(
                        bundle.read(0x100).strip(b'\0').decode('utf-8', errors='ignore'),
                        bundle.read(0x14),
                        int.from_bytes(bundle.read(4), byteorder='little'),
                        int.from_bytes(bundle.read(4), byteorder='little'),
                        int.from_bytes(bundle.read(4), byteorder='little'),
                        bundle.read(0x20)
                    )
                )

            for j, file in enumerate(file_list):
                bundle.seek(file.offset)
                os.makedirs(os.path.join(self.output_folder, os.path.dirname(file.name)), exist_ok=True)

                if file.zip_size == file.unzip_size:
                    data = bundle.read(file.unzip_size)
                else:
                    data = zlib.decompress(bundle.read(file.zip_size))

                with open(os.path.join(self.output_folder, file.name), 'wb') as nf:
                    nf.write(data)

                self.update_pb(file_count, j + 1, file.name)
