
from source.reaper import Reaper, file_reaper
from source.ui import localize


class Rockstar(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if magic == b'RPF0':
                print('Rockstar Games Presents Table Tennis')
                version = 0
            elif magic == b'RPF2':
                print('Grand Theft Auto IV')
                version = 2
            elif magic == b'RPF3':
                print('Grand Theft Auto IV Audio & Midnight Club: Los Angeles')
                version = 3
            elif magic == b'RPF4':
                print('Max Payne 3')
                version = 4
            elif magic == b'RPF6':
                print('Red Dead Redemption')
                version = 6
            elif magic == b'RPF7':
                print('Grand Theft Auto V')
                version = 7
            elif magic == b'RPF8':
                print('Red Dead Redemption 2')
                version = 8
            else:
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Rockstar'), True)
                return

            if version == 0:
                table_size = int.from_bytes(file.read(4), byteorder='big')
                file_count = int.from_bytes(file.read(4), byteorder='big')

            elif version == 2:
                table_size = int.from_bytes(file.read(4), byteorder='big')
                file_count = int.from_bytes(file.read(4), byteorder='big')
                file.seek(4)
                encrypt = int.from_bytes(file.read(4), byteorder='big')

