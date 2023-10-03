
import os
from source.reaper import Reaper


class Seven(Reaper):

    def run(self):
        self.update_signal.emit(0, '', f'Wait...', False)

        with open(self.file_name, 'rb') as file:
            idstring = file.read(4)

            if idstring != b'\x37\xBD\x37\x4D':
                print("Неверный формат файла 7Ѕ7M")
                return

            data = bytearray((byte ^ 0xf7) for byte in file.read())

            with open('./temp.dat', 'wb') as new_file:
                new_file.write(idstring+data)

        with open('./temp.dat', 'rb') as f:
            f.seek(9)
            file_list = {}

            while True:
                nameSize = int.from_bytes(f.read(1), byteorder='little')
                fName = f.read(nameSize).decode('utf-8')
                fSize = int.from_bytes(f.read(4), byteorder='little')
                file_list[fName] = fSize
                f.seek(8, 1)
                lastFile = f.read(1)

                if lastFile != b'\x00':
                    break

            file_count = len(file_list)
            i = 0

            for name, size in file_list.items():
                Data = f.read(size)
                path = os.path.join(self.output_folder, name)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                i += 1

                with open(path, 'wb') as newFile:
                    newFile.write(Data)
                    print(f'{i}/{file_count} - {name}')
                    self.update_signal.emit(int(100 / file_count * i), f'{i}/{file_count}',
                                            f'Saving - {name}...', False)

        os.remove('./temp.dat')
        self.update_signal.emit(100, f'{file_count}/{file_count}', f'Done!', True)
        print('DONE!')