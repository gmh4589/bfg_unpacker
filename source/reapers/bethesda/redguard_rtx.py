import os
from source.reaper import Reaper, file_reaper
from source.ui import localize


class RedguardRTX(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as rtx_file:
            magic = rtx_file.read(4)

            if not self.magic([b'#bon', ], magic, 'TES Aventure: Redguard RTX File'):
                return

            file_size = os.path.getsize(self.file_name)
            rtx_file.seek(0)

            with open(f'{self.output_folder}\\{os.path.basename(self.file_name)}.txt', 'w') as text_file:

                while True:
                    rtx_file.seek(4, 1)
                    file_long = int.from_bytes(rtx_file.read(4), byteorder="big")
                    dummy = int.from_bytes(rtx_file.read(2), byteorder="big")
                    name_long = int.from_bytes(rtx_file.read(4), byteorder="little")
                    name = rtx_file.read(name_long).decode('utf-8', errors='ignore')
                    long = file_long - name_long - 6

                    if long < 0: 
                        break
                    
                    data = rtx_file.read(file_long - name_long - 6)
                    text_file.write(name + '\n')
                    short_text = ''

                    for n in name[:20].lower():

                        if n in 'abcdefghijklmnopqrstuvwxyz1234567890':
                            short_text += n

                    if file_long > 0:
                        self.file_save(f"{self.output_folder}\\audio\\{short_text}.dat", data)

                    pos = rtx_file.tell()
                    self.update_pb(file_size, pos, name)

                self.update_pb(file_size, file_size, localize.done)
