
from source.reaper import Reaper, file_reaper


class Rockstar(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(3)

            if not self.magic([b'RPF'], magic, 'Rockstar'):
                return

            version = int.from_bytes(file.read(1))
            games = {
                0: 'Rockstar Games Presents Table Tennis',
                2: 'Grand Theft Auto IV',
                3: 'Grand Theft Auto IV Audio or Midnight Club: Los Angeles',
                4: 'Max Payne 3',
                6: 'Red Dead Redemption',
                7: 'Grand Theft Auto V',
                8: 'Red Dead Redemption 2'
            }

            if version not in games.keys():
                print(f'Unknown version - {version}')
                return

            print(f'Detected game - {games.get(version)}')

            if version == 0:
                table_size = int.from_bytes(file.read(4), byteorder='big')
                file_count = int.from_bytes(file.read(4), byteorder='big')

            elif version == 2:
                table_size = int.from_bytes(file.read(4), byteorder='big')
                file_count = int.from_bytes(file.read(4), byteorder='big')
                file.seek(4)
                encrypt = int.from_bytes(file.read(4), byteorder='big')

