
import os
from source.reaper import Reaper, file_reaper
from source.ui import localize


class SenBook(Reaper):

    @file_reaper
    def run(self):

        file_path = self.file_name
        book = open(file_path, 'rb')
        book.seek(8, 0)
        start = int.from_bytes(book.read(4), byteorder='little')
        book.seek(20, 0)
        count = int.from_bytes(book.read(4), byteorder='little')
        startData = int.from_bytes(book.read(4), byteorder='little')
        book.seek(start, 0)

        offsetArray = []
        nameOffsetArray = []

        for i in range(count):
            offsetArray.append(int.from_bytes(book.read(4), byteorder='little'))

        for i in range(count):
            nameOffsetArray.append(int.from_bytes(book.read(2), byteorder='little'))

        a = book.tell()
        size = os.path.getsize(file_path)
        data = book.read(startData - a)
        nameArray = data.split(b'\x00')

        offsetArray.append(size)

        path = file_path[:-4] + '\\'
        os.makedirs(path)
        file_count = len(offsetArray) - 1

        for j in range(file_count):
            book.seek(offsetArray[j])
            data = book.read(offsetArray[j + 1] - offsetArray[j])
            coefficient = '0' * (5 - len(str(j))) + str(j)
            newFile = path + coefficient + '.' + str(nameArray[j])[2:-1] + '.dat'

            with open(newFile, 'wb') as file:
                file.write(data)

            print(f'{j + 1}/{file_count} - {newFile}_{j}')
            self.update_signal.emit(int(100 / file_count * (j + 1)), f'{j + 1}/{file_count}',
                                    f'{localize.saving} - {newFile}_{j}...', False)

        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)


class SenBookSave(Reaper):

    @file_reaper
    def run(self):
        file_path = self.file_name
        name = file_path.split('/')[-1]
        fileList = os.listdir(file_path)
        list1 = b''

        for n in fileList:
            list1 += n.split('.')[1].encode('utf-8') + b'\x00'

        blockOff = 33 + len(name)
        contOff = len(fileList)
        size = contOff * 4
        endBlock = blockOff + size
        block2Start = blockOff + (contOff * 6)
        startData = block2Start + len(list1)

        with open(file_path + '_new.dat', 'wb') as f:
            f.write(b'\x20\x00\x00\x00\x20\x00\x00\x00')
            f.write(blockOff.to_bytes(4, byteorder='little'))
            f.write(size.to_bytes(4, byteorder='little'))
            f.write(endBlock.to_bytes(4, byteorder='little'))
            f.write(contOff.to_bytes(4, byteorder='little'))
            f.write(startData.to_bytes(4, byteorder='little'))
            f.write(b'\x00\xef\xcd\xab')
            f.write(name.encode('utf-8') + b'\x00')
            startData += 1
            f.write(startData.to_bytes(4, byteorder='little'))
            for i in range(contOff - 1):
                startData += os.path.getsize(file_path + '/' + fileList[i])
                f.write(startData.to_bytes(4, byteorder='little'))

            f.write(block2Start.to_bytes(2, byteorder='little'))
            for j in range(contOff - 1):
                block2Start += len(fileList[j]) - 9
                f.write(block2Start.to_bytes(2, byteorder='little'))

            f.write(list1 + b'\x00')

            for file in fileList:
                with open(file_path + '/' + file, 'rb') as readF:
                    readData = readF.read()
                f.write(readData)

            print(f'{localize.saving} - {j + 1}/{contOff}')
            self.update_signal.emit(int(100 / contOff * (j + 1)), f'{j + 1}/{contOff}',
                                    f'{localize.saving} - {j + 1}/{contOff}...', False)

        self.update_signal.emit(100, f'{contOff}/{contOff}', localize.done, True)
