import os
from PIL import Image
from source.reaper import Reaper, file_reaper


class KTXConvert(Reaper):

    @file_reaper
    def run(self) -> None:

        with open(self.file_name, 'rb') as ktx_stream:
            ktx_stream.seek(0x24)
            width = int.from_bytes(ktx_stream.read(4), byteorder="little")
            height = int.from_bytes(ktx_stream.read(4), byteorder="little")
            ktx_stream.seek(0x60)
            image_data = ktx_stream.read()

        os.makedirs(os.path.dirname(self.output_folder), exist_ok=True)
        new_image = Image.frombytes('RGBA', (width, height), image_data)
        new_image.save(self.output_folder)
        self.update_pb(1, 1, self.file_name)
