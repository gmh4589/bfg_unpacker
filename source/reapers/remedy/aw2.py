import os
import io
from tkinter.messagebox import showinfo

import icecream
import lz4.block as lz4
from collections import namedtuple
from source.reaper import Reaper, file_reaper


class AlanWake2(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as toc:
            magic = toc.read(4)
            version = int.from_bytes(toc.read(4), byteorder="little")

            if not self.magic([b'COTR', ], magic, 'Alan Wake 2'):
                return

            if not self.magic([2, ], version, 'Alan Wake 2'):
                return

            in_dir = os.path.dirname(self.file_name)

            comp_info_offset = int.from_bytes(toc.read(4), byteorder="little")
            comp_info_size = int.from_bytes(toc.read(4), byteorder="little")
            blob_offset = int.from_bytes(toc.read(4), byteorder="little")
            blob_count = int.from_bytes(toc.read(4), byteorder="little")
            folder_list_offset = int.from_bytes(toc.read(4), byteorder="little")
            folder_count = int.from_bytes(toc.read(4), byteorder="little")
            file_list_offset = int.from_bytes(toc.read(4), byteorder="little")
            file_count = int.from_bytes(toc.read(4), byteorder="little")
            file_list_start = int.from_bytes(toc.read(4), byteorder="little")
            file_list_len = int.from_bytes(toc.read(4), byteorder="little")
            unk_offset = int.from_bytes(toc.read(4), byteorder="little")
            unk_size = int.from_bytes(toc.read(4), byteorder="little")
            unk_offset2 = int.from_bytes(toc.read(4), byteorder="little")
            unk_size2 = int.from_bytes(toc.read(4), byteorder="little")

            toc.seek(0x10, 1)
            file_data_start = int.from_bytes(toc.read(4), byteorder="little")
            file_data_size = int.from_bytes(toc.read(4), byteorder="little")

            toc.seek(0x1000)
            file_datas = toc.read()
            unzip_list = lz4.decompress(file_datas, file_list_len * 20)

            data_stream = io.BytesIO(unzip_list.replace(b'\0' * 928, b''))

            with open(self.output_folder + '\\file_list.temp', 'wb') as tf:
                tf.write(data_stream.read())

            data_stream.seek(file_list_start)
            file_list_stream = io.BytesIO(data_stream.read())

            # BLOB data block reading
            data_stream.seek(blob_offset)
            blob_list = []

            for i in range(blob_count):
                b_name_offset = int.from_bytes(data_stream.read(4), byteorder="little")
                b_name_size = int.from_bytes(data_stream.read(4), byteorder="little")
                b_hash = data_stream.read(8)
                file_list_stream.seek(b_name_offset)
                blob_list.append(file_list_stream.read(b_name_size)
                                 .decode('utf-8', errors='ignore')
                                 .replace('../pc', in_dir))

            # Folder data block reading
            data_stream.seek(folder_list_offset)
            folder_list = []

            for j in range(folder_count):
                data_stream.seek(0x14, 1)
                fol_name_offset = int.from_bytes(data_stream.read(4), byteorder="little")
                fol_name_size = int.from_bytes(data_stream.read(4), byteorder="little")
                file_list_stream.seek(fol_name_offset)
                fol_name = file_list_stream.read(fol_name_size).decode('utf-8', errors='ignore')
                folder_list.append(fol_name)

            data_stream.seek(file_list_offset)
            file_list = []

            for k in range(file_count):
                data_stream.seek(0xC, 1)
                name_offset = int.from_bytes(data_stream.read(4), byteorder="little")
                name_long = int.from_bytes(data_stream.read(4), byteorder="little")
                data_stream.seek(0xC, 1)
                file_list_stream.seek(name_offset)
                file_name = file_list_stream.read(name_long).decode('utf-8', errors='ignore')
                file_list.append(file_name)

            Offsets = namedtuple('Offsets',
                                 ['vol', 'offset', 'size'])
            offsets = []

            # data_stream.seek(file_data_start + 0x174)
            data_stream.seek(file_list_start + file_list_len + (file_count + 1) * 72)
            icecream.ic(hex(data_stream.tell()))

            for _ in range(file_count):

                offsets.append(
                    Offsets(
                        int.from_bytes(data_stream.read(2), byteorder="little"),  # vol
                        int.from_bytes(data_stream.read(5), byteorder="little"),  # offset
                        int.from_bytes(data_stream.read(4), byteorder="little")   # size
                    )
                )

                data_stream.seek(5, 1)

            blobs = [open(b, 'rb') for b in blob_list]

            for i, name in enumerate(file_list):
                path = os.path.join(self.output_folder, name)
                # path = os.path.join(self.output_folder, str(i) + '.wem')
                ol = offsets[i]
                blobs[ol.vol - 1].seek(ol.offset)

                try:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    file_data = blobs[ol.vol - 1].read(ol.size)
                    icecream.ic(path)

                    with open(path, 'wb') as nf:
                        nf.write(file_data.strip(b'\0'))

                except Exception as e:
                    icecream.ic(e)

                self.update_pb(file_count, i + 1, name)

            for b in blobs:
                b.close()
