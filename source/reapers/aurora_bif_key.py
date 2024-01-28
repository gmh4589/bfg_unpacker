import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize

resource_type = {
    1: 'bmp', 3: 'tga', 4: 'wav', 6: 'plt', 7: 'ini', 10: 'txt', 2002: 'mdl', 2009: 'nss', 2010: 'ncs',
    2012: 'are', 2013: 'set', 2014: 'ifo', 2015: 'bic', 2016: 'wok', 2017: '2da', 2022: 'txi', 2023: 'git',
    2025: 'uti', 2027: 'utc', 2029: 'dlg', 2030: 'itp', 2032: 'utt', 2033: 'dds', 2035: 'uts', 2036: 'ltr',
    2037: 'gff', 2038: 'fac', 2040: 'ute', 2042: 'utd', 2044: 'utp', 2045: 'dft', 2046: 'gff', 2047: 'gui',
    2051: 'utm', 2052: 'dwk', 2053: 'pwk', 2056: 'jrl', 2058: 'utw', 2060: 'ssf', 2064: 'ndb', 2065: 'ptm',
    2066: 'ptt'}


class FileExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if magic != b'FILE':
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Aurora Engine'), True)
                return

            file_count = int.from_bytes(file.read(4), byteorder="little")

            for i in range(file_count):
                name = file.read(64).decode("ascii").rstrip("\0")
                offset = int.from_bytes(file.read(4), byteorder="little")
                size = int.from_bytes(file.read(4), byteorder="little")
                ic(name)

                path = os.path.join(self.output_folder, name)
                ic(path)
                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as new_file:
                    here = file.tell()
                    file.seek(offset)
                    new_file.write(file.read(size))
                    file.seek(here)

                print(f'{i}/{file_count}: {localize.saving} - {name}...')
                self.update_signal.emit(int(100 / file_count * i), f'{i}/{file_count}',
                                        f'{localize.saving} - {name}...', False)

        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
