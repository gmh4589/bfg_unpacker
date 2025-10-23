
import io
from source.reaper import Reaper, file_reaper


class IMG_BDExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bin_file:
            magic = bin_file.read(4)

            if not self.magic([b'\x14\0\0\0', ], magic, 'Fatal Frame IMG_BD.BIN File'):
                return

            bin_file.seek(0x1FCC30)
            bin_data = bin_file.read().split(b'TIM2')
            file_count = len(bin_data)

            for i, data in enumerate(bin_data):

                if data:
                    data_stream = io.BytesIO(data)
                    img_head = b'TIM2' + data_stream.read(0x3C)
                    data_stream.seek(0x20)
                    x = int.from_bytes(data_stream.read(2), byteorder='little')
                    y = int.from_bytes(data_stream.read(2), byteorder='little')
                    img_size = (x * y) + 0x400
                    data_stream.seek(0x3C)
                    img_data = data_stream.read(img_size)
                    path = f'{self.output_folder}\\textures\\{str(i).rjust(6, '0')}.tm2'
                    self.file_save(path, img_head + img_data)
                    self.update_pb(file_count, i + 1, path)
