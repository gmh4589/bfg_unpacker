import os
import zlib
from collections import namedtuple
from icecream import ic
from source.codecs.dds_tools import DDSCreator
from source.reaper import Reaper, file_reaper


class SacredPAK(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if not self.magic([b'TEX\x03', b'MDL\x03', b'SND\x01'], magic, 'Sacred Gold PAK'):
                return

            file_count = int.from_bytes(file.read(4), byteorder="little") if magic != b'SND\x01' else 3195
            seek_dict = {b'TEX\x03': 0x10C, b'MDL\x03': 0x100, b'SND\x01': 0x5B0}
            file.seek(seek_dict[magic])
            FileData = namedtuple('FileData',
                                  ['offset', 'size'])
            file_data = []
            j = 0

            while True:
                have_file = int.from_bytes(file.read(4), byteorder="little")

                if have_file:
                    offset = int.from_bytes(file.read(4), byteorder="little")
                    size = int.from_bytes(file.read(4), byteorder="little")
                    file_data.append(FileData(offset, size))
                    j += 1

                if j == file_count:
                    break

            for i, data in enumerate(file_data):
                file.seek(data.offset)
                f_pos = file.tell()

                if f_pos:

                    if magic == b'TEX\x03':
                        file_name = file.read(0x20).decode('utf-8', errors='ignore').rstrip('\0')
                        width = int.from_bytes(file.read(2), byteorder="little")
                        height = int.from_bytes(file.read(2), byteorder="little")
                        file.seek(0x2c, 1)
                        image_data = file.read(data.size)
                        output_path = os.path.join(self.output_folder, file_name)
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)

                        try:
                            image_data = zlib.decompress(image_data)
                        except zlib.error:
                            pass

                        if file_name:

                            try:
                                dds = DDSCreator()
                                dds.dds_save(width, height,
                                             'B4G4R4A4_UNORM',
                                             name=output_path,
                                             data=image_data)
                            except ValueError:
                                ic(file_name)

                    elif magic == b'MDL\x03':
                        file_name = file.read(0x20).decode('utf-8', errors='ignore').rstrip('\0')
                        model_data = file.read(data.size)
                        output_path = os.path.join(self.output_folder, file_name)
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)

                        with open(output_path, 'wb') as model:
                            model.write(model_data)

                    elif magic == b'SND\x01':
                        file_name = f"{i}.wav"
                        sound_data = file.read(data.size)
                        output_path = os.path.join(self.output_folder, file_name)
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)

                        with open(output_path, 'wb') as sound:
                            sound.write(sound_data)

                self.update_pb(file_count, i + 1, output_path)

