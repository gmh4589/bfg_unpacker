import os
from source.reaper import Reaper, file_reaper


class ERFUnpacker(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as f:
            f.seek(4, 0)
            iVer = f.read(4)

            if iVer == b'\x56\x31\x2E\x30':
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

            else:
                f.seek(8, 0)
                iVer = f.read(4)

                if iVer == b'\x56\x00\x32\x00':
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
                        self.update_signal.emit(int(100 / iFileCount * (i + 1)), f'{i + 1}/{iFileCount}',
                                                f'Saving - {rName}...', False)

                    self.update_signal.emit(100, f'{iFileCount}/{iFileCount}', f'Done!', True)

                elif iVer == b'\x56\x00\x33\x00':
                    self.update_signal.emit(100, f'0/0', f'TODO!', True)
                    print('TODO!')

                else:
                    self.update_signal.emit(100, f'0/0', f'This file not Aurora Engine Archive!', True)
                    print('This file not Aurora Engine Archive!')

