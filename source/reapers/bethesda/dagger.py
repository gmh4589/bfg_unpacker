import os
from source.reaper import Reaper, file_reaper


class DaggerSND(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name,  'rb') as snd_file:
            file_count = int.from_bytes(snd_file.read(2), byteorder="little")
            file_long = os.path.getsize(self.file_name)
            pos = file_long - file_count * 8
            start = 4

            for i in range(file_count):
                snd_file.seek(pos)
                name = f'{int.from_bytes(snd_file.read(4), byteorder="little")}.wav'
                size = int.from_bytes(snd_file.read(4), byteorder="little")
                pos = snd_file.tell()
                snd_file.seek(start)
                start += size
                data = snd_file.read(size)
                self.update_pb(file_count, i, name)

                with open(os.path.join(self.output_folder, name), 'wb') as nf:

                    if data[:4] == b'RIFF':
                        nf.write(data)
                    else:
                        nf.write((b'\x52\x49\x46\x46\xE7\x99\x00\x00\x57\x41\x56\x45\x66\x6D\x74\x20\x10\x00'
                                  b'\x00\x00\x01\x00\x01\x00\x11\x2B\x00\x00\x11\x2B\x00\x00\x01\x00\x08\x00'
                                  b'\x64\x61\x74\x61\xC3\x99') + data)


