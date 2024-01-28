import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize

resource_type = {1: 'bmp', 3: 'tga', 4: 'wav', 6: 'plt', 7: 'ini', 10: 'txt', 2002: 'mdl', 2009: 'nss',
                 2010: 'ncs', 2012: 'are', 2013: 'set', 2014: 'ifo', 2015: 'bic', 2016: 'wok', 2017: '2da',
                 2022: 'txi', 2023: 'git', 2025: 'uti', 2027: 'utc', 2029: 'dlg', 2030: 'itp', 2032: 'utt',
                 2033: 'dds', 2035: 'uts', 2036: 'ltr', 2037: 'gff', 2038: 'fac', 2040: 'ute', 2042: 'utd',
                 2044: 'utp', 2045: 'dft', 2046: 'gff', 2047: 'gui', 2051: 'utm', 2052: 'dwk', 2053: 'pwk',
                 2056: 'jrl', 2058: 'utw', 2060: 'ssf', 2064: 'ndb', 2065: 'ptm', 2066: 'ptt', 3007: 'tex'}


class ERFUnpacker(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as f:
            magic = f.read(4)

            if magic not in (b'RIM ', b'ERF ', b'E\x00R\x00', b'R\x00I\x00'):
                print(localize.not_correct_file.replace('%%', 'BioWare Engines'))
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'BioWare Engines'), True)
                return

            if magic in (b'RIM ', b'ERF '):
                ver = f.read(4)
            else:
                f.seek(8)
                ver = f.read(8).replace(b'\x00', b'')

            ic(ver)

            if ver == b'V1.0':  # Version 1
                f.seek(16) if magic == b'ERF ' else f.seek(12)
                file_count = int.from_bytes(f.read(4), byteorder='little')
                f.seek(24) if magic == b'ERF ' else f.seek(16)
                off_list = int.from_bytes(f.read(4), byteorder='little')
                erf_list = int.from_bytes(f.read(4), byteorder='little')
                f.seek(off_list)

                file_name_array = []

                if magic == b'ERF ':

                    for _ in range(file_count):
                        rName = f.read(16).rstrip(b'\x00').decode('utf-8', errors='ignore')
                        f.seek(4, 1)
                        ext = resource_type[int.from_bytes(f.read(4), byteorder='little')]
                        file_name_array.append(f'{rName}.{ext}')

                    if erf_list != f.tell():
                        print(localize.not_correct_file.replace('%%', 'BioWare Engines'))
                        self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'BioWare Engines'), True)
                        return

                    for j in range(file_count):
                        offset = int.from_bytes(f.read(4), byteorder='little')
                        long = int.from_bytes(f.read(4), byteorder='little')
                        c = f.tell()
                        f.seek(offset)
                        data = f.read(long)
                        fName = file_name_array[j]
                        ic(fName, offset, long)

                        with open(os.path.join(self.output_folder, fName), 'wb') as newFile:
                            newFile.write(data)

                        f.seek(c, 0)
                        print(f"{j}/{file_count} {fName}")
                        self.update_signal.emit(int(100 / file_count * (j + 1)), f'{j + 1}/{file_count}',
                                                f'{localize.saving} - {fName}...', False)

                elif magic == b'RIM ':

                    for i in range(file_count):
                        oName = f.read(16).rstrip(b'\x00').decode('utf-8', errors='ignore')
                        ext = resource_type[int.from_bytes(f.read(4), byteorder='little')]
                        rName = f'{oName}.{ext}'
                        f.seek(4, 1)
                        offset = int.from_bytes(f.read(4), byteorder='little')
                        long = int.from_bytes(f.read(4), byteorder='little')
                        c = f.tell()
                        f.seek(offset)
                        data = f.read(long)

                        with open(os.path.join(self.output_folder, rName), 'wb') as iNewFile:
                            iNewFile.write(data)

                        f.seek(c)
                        print(f"{i + 1}/{file_count} {rName}")
                        ic(rName)
                        self.update_signal.emit(int(100 / file_count * (i + 1)), f'{i + 1}/{file_count}',
                                                f'{localize.saving} - {rName}...', False)

            elif ver == b'V2.0':  # Version 2
                f.seek(16, 0)
                file_count = int.from_bytes(f.read(4), byteorder='little')
                f.seek(32, 0)

                for i in range(file_count):
                    rName = f.read(64).rstrip(b'\x00').replace(b'\x00', b'').decode('utf-8', errors='ignore')
                    offset = int.from_bytes(f.read(4), byteorder='little')
                    long = int.from_bytes(f.read(4), byteorder='little')
                    c = f.tell()
                    f.seek(offset)
                    data = f.read(long)

                    with open(os.path.join(self.output_folder, rName), 'wb') as iNewFile:
                        iNewFile.write(data)

                    f.seek(c)
                    print(f"{i + 1}/{file_count} {rName}")
                    ic(rName)
                    self.update_signal.emit(int(100 / file_count * (i + 1)), f'{i + 1}/{file_count}',
                                            f'{localize.saving} - {rName}...', False)

            elif ver == b'V3.0':  # Version 3
                # TODO: Need Tests!!!
                f.seek(16)
                names_long = int.from_bytes(f.read(4), byteorder='little')
                file_count = int.from_bytes(f.read(4), byteorder='little')
                f.seek(48)
                names_list = []

                if names_long:
                    names = f.read(names_long)
                    names_list = names.split(b'\x00')

                for i in range(file_count):
                    f.seek(16, 1)

                    offset = int.from_bytes(f.read(4), byteorder='little')
                    zSize = int.from_bytes(f.read(4), byteorder='little')
                    size = int.from_bytes(f.read(4), byteorder='little')
                    this = f.tell()

                    if zSize == size:
                        f.seek(offset, 0)
                        write_data = f.read(zSize)
                    else:
                        # TODO:
                        """
                        Не понятно, каким алгоритмом сжаты данные, в мануале написано, что это Deflate,
                        но Deflate не подходит. Все другие алгоритмы тоже выдают не понятно что.
                        Проверялось на PS3 версии Dragon Age 2, возможно, в ПК версии используется Deflate,
                        а в PS3 какой-то другой алгоритм. Нужно проверить на ПК версии
                        """

                        f.seek(offset + 1, 0)
                        write_data = f.read(zSize - 1)
                        # write_data = zlib.decompress(write_data, -zlib.DEFLATED)

                    ext = self.get_ext(write_data[:4])

                    try:
                        name = f'{names_list[i].decode("utf-8")}' if names_list[i] else f'unknown_{i}.{ext}'
                    except (IndexError, UnicodeDecodeError):
                        name = f'unknown_{i}.{ext}'

                    with open(f'{self.output_folder}\\{name}', 'wb') as file_out:
                        file_out.write(write_data)

                    f.seek(this)
                    print(f"{i + 1}/{file_count} {name}")
                    self.update_signal.emit(int(100 / file_count * (i + 1)), f'{i + 1}/{file_count}',
                                            f'{localize.saving} - {name}...', False)

            else:
                print(localize.not_correct_file.replace('%%', 'BioWare Engines'))

            self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
