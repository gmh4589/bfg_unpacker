
import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class PakExtractor(Reaper):

    def __init__(self):
        super().__init__()
        self.raw_fat = None
        self.no_caps = True
        self.dirs = []

    @file_reaper
    def run(self):
        self.dirs = []

        with open(self.file_name, 'rb') as f:
            fat_offset = int.from_bytes(f.read(4), byteorder='little')
            f.seek(fat_offset)
            fat_size = int.from_bytes(f.read(4), byteorder='little')
            self.raw_fat = bytearray(f.read(fat_size))
            key = self.select_key(int.from_bytes(self.raw_fat[:4], byteorder='little'))

            if key:
                self.decrypt_fat(key)
                f.seek(4)

                if self.dirs:
                    all_files = 0
                    current = 0

                    for d_ in self.dirs:
                        all_files += len(d_['files'])

                    for d in self.dirs:
                        os.makedirs(os.path.join(self.output_folder, d['name']), exist_ok=True)

                        for file in d['files']:
                            current += 1
                            new_file = f.read(file['size'])
                            ext = file['name'].split('.')[-1]
                            path = os.path.join(self.output_folder, d['name'], file['name'])

                            with open(path, 'wb') as nf:
                                nf.write(new_file)

                            if ext == 'bmp':
                                self.unzip(path, 618)

                            print(f"{current}/{all_files} {file['name']}")
                            ic(file["name"])
                            self.update_signal.emit(int(100 / all_files * current), f'{current}/{all_files}',
                                                    f'{localize.saving} - {file["name"]}...', False)

                    self.update_signal.emit(100, '', localize.done, True)

            else:
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Arx Fatalis'), True)

    def decrypt_fat(self, key):
        dec = FATDecryptor(key, self.raw_fat)

        while dec.fat_size > 0:
            dir_name = dec.decrypt_string(self.no_caps)

            if dir_name:
                dir_name = dir_name.replace('\\', '/')  # fix slashes
                d = {'name': dir_name, 'files': []}
                files_count = dec.decrypt_dword()

                for _ in range(files_count):
                    f = {'name': dec.decrypt_string(self.no_caps), 'offset': dec.decrypt_dword(),
                         'flags': dec.decrypt_dword(), 'p3': dec.decrypt_dword(), 'size': dec.decrypt_dword()}
                    d['files'].append(f)

                self.dirs.append(d)

    @staticmethod
    def select_key(first_bytes):
        full_key = b"AVQF3FCKE50GRIAYXJP2AMEYO5QGA0JGIIH2NHBTVOA1VOGGU5H3GSSIARKPRQPQKKYEOIAQG1XRX0J4F5OEAEFI4DD3LL45VJTVOA1VOGGUKE50GRIAYX"
        demo_key = b"NSIARKPRQPHBTE50GRIH3AYXJP2AMF3FCEYAVQO5QGA0JGIIH2AYXKVOA1VOGGU5GSQKKYEOIAQG1XRX0J4F5OEAEFI4DD3LL45VJTVOA1VOGGUKE50GRIAYX"

        if first_bytes == 0x46515641:
            return full_key
        elif first_bytes == 0x4149534E:
            return demo_key
        else:
            return 0


class FATDecryptor:
    def __init__(self, key, raw_fat):
        self.key_str = key
        self.key_pos = 0
        self.raw_fat = bytearray(raw_fat)
        self.fat_size = len(raw_fat)

    def decrypt_char(self):
        c = self.raw_fat[0] ^ self.key_str[self.key_pos]
        self.key_pos = (self.key_pos + 1) % len(self.key_str)
        self.raw_fat.pop(0)
        self.fat_size -= 1

        return c

    def decrypt_dword(self):
        rval = 0

        for j in range(4):
            rval |= self.decrypt_char() << (8 * j)

        return rval

    def decrypt_string(self, no_caps):
        str_bytes = bytearray()

        while True:
            char = self.decrypt_char()

            if char == 0:
                break

            str_bytes.append(char)

        return str_bytes.decode('utf-8',
                                errors='ignore').lower() if no_caps else str_bytes.decode('utf-8',
                                                                                          errors='ignore')
