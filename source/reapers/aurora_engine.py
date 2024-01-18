import os
import zlib
from icecream import ic

from source.reaper import Reaper
from source.ui import localize


class ERFUnpacker(Reaper):

    def run(self):

        with open(self.file_name, 'rb') as f:
            f.seek(4, 0)
            iVer = f.read(4)

            if iVer == b'\x56\x31\x2E\x30':  # Version 1
                f.seek(16)
                iFileCount = int.from_bytes(f.read(4), byteorder='little')
                f.seek(24)
                iOff2Lst = int.from_bytes(f.read(4), byteorder='little')
                f.seek(28)
                iERFLst = int.from_bytes(f.read(4), byteorder='little')
                f.seek(iOff2Lst)

                FileNameArray = []
                FileExtArray = []

                for _ in range(iFileCount):
                    rName = f.read(16).rstrip(b'\x00')
                    FileNameArray.append(rName)
                    f.seek(4, 1)
                    fEXT = int.from_bytes(f.read(4), byteorder='little')

                    if fEXT == b'\xBF\x0B\x00\x00':
                        fEXT = '.dds'
                    else:
                        fEXT = '.dat'

                    FileExtArray.append(fEXT)

                f.seek(iERFLst, 0)

                for j in range(1, iFileCount + 1):
                    data1 = int.from_bytes(f.read(4), byteorder='little')
                    data2 = int.from_bytes(f.read(4), byteorder='little')
                    c = f.tell()
                    f.seek(data1)
                    Data = f.read(data2)
                    rName = FileNameArray[j].decode('utf-8')
                    fName = rName + FileExtArray[j]

                    with open(os.path.join(self.output_folder, fName), 'wb') as newFile:
                        newFile.write(Data)

                    f.seek(c, 0)
                    print(f"{j}/{iFileCount} {fName}")
                    ic(fName)
                    self.update_signal.emit(int(100 / iFileCount * (j + 1)), f'{j + 1}/{iFileCount}',
                                            f'{localize.saving} - {rName}...', False)

            else:
                f.seek(8, 0)
                iVer = f.read(4)

                if iVer == b'\x56\x00\x32\x00':  # Version 2
                    f.seek(16, 0)
                    iFileCount = int.from_bytes(f.read(4), byteorder='little')
                    f.seek(32, 0)

                    for i in range(iFileCount):
                        rName = f.read(64).rstrip(b'\x00')
                        iOffs = int.from_bytes(f.read(4), byteorder='little')
                        iLong = int.from_bytes(f.read(4), byteorder='little')
                        c = f.tell()
                        f.seek(iOffs)
                        Data = f.read(iLong)
                        rName = rName.decode('unicode_escape').replace('\x00', '')
                        iNewFile = open(os.path.join(self.output_folder, rName), 'wb')
                        iNewFile.write(Data)
                        iNewFile.close()
                        f.seek(c)
                        print(f"{i + 1}/{iFileCount} {rName}")
                        ic(rName)
                        self.update_signal.emit(int(100 / iFileCount * (i + 1)), f'{i + 1}/{iFileCount}',
                                                f'{localize.saving} - {rName}...', False)

                elif iVer == b'\x56\x00\x33\x00':  # Version 3, Version 5
                    # TODO: Need Tests!!!
                    f.seek(48, 0)

                    iFileCount = int.from_bytes(f.read(4), byteorder='little')

                    for i in range(iFileCount):
                        f.seek(16, 1)

                        offset = int.from_bytes(f.read(4), byteorder='little') + 1
                        zSize = int.from_bytes(f.read(4), byteorder='little') - 1
                        size = int.from_bytes(f.read(4), byteorder='little')

                        f.seek(offset, 0)
                        compressed_data = f.read(zSize)

                        decompressed_data = zlib.decompress(compressed_data)

                        with open(f'{self.output_folder}\\{i}', 'wb') as file_out:
                            file_out.write(decompressed_data)

                        print(f"{i + 1}/{iFileCount} {i}")
                        self.update_signal.emit(int(100 / iFileCount * (i + 1)), f'{i + 1}/{iFileCount}',
                                                f'{localize.saving} - {i}...', False)

                else:
                    print(localize.not_correct_file)

            self.update_signal.emit(100, f'{iFileCount}/{iFileCount}', localize.done, True)
