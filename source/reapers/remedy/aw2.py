import os
import io
import lz4.block as lz4
from collections import namedtuple
from source.reaper import Reaper, file_reaper


class AlanWake2(Reaper):

    @file_reaper
    def run(self):
        only_name = self.file_name.split('.')[0]
        toc_file = f'{only_name}.rmdtoc'

        with (open(toc_file, "rb") as toc):
            magic = toc.read(4)
            version = int.from_bytes(toc.read(4), byteorder="little")

            if (not self.magic([b'COTR', ], magic, 'Alan Wake 2') or
                    not self.magic([2, ], version, 'Alan Wake 2')):
                return

            in_dir = os.path.dirname(self.file_name)

            toc.seek(0x10)
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
            dmkp_block_offset = int.from_bytes(toc.read(4), byteorder="little")
            dmkp_block_size = int.from_bytes(toc.read(4), byteorder="little")

            toc.seek(0x10, 1)
            file_data_start = int.from_bytes(toc.read(4), byteorder="little")
            file_data_size = int.from_bytes(toc.read(4), byteorder="little")

            toc.seek(0x1000)
            file_datas = toc.read()
            data_stream = io.BytesIO(lz4.decompress(file_datas, file_list_len * 20))

            temp_file = self.output_folder + '\\file_list.dat'

            with open(temp_file, 'wb') as fl:
                fl.write(data_stream.read())

            data_stream.seek(file_list_start)
            file_list_stream = io.BytesIO(data_stream.read(file_list_len))

            # BLOB data block reading
            data_stream.seek(blob_offset)
            blob_list = []

            for _ in range(blob_count):
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

            for _ in range(folder_count):
                tree_level = int.from_bytes(data_stream.read(4), byteorder="little")
                folder_index = int.from_bytes(data_stream.read(4), byteorder="little")
                folders_in_folder = int.from_bytes(data_stream.read(4), byteorder="little")
                file_index = int.from_bytes(data_stream.read(4), byteorder="little")
                files_in_folder = int.from_bytes(data_stream.read(4), byteorder="little")
                fol_name_offset = int.from_bytes(data_stream.read(4), byteorder="little")
                fol_name_size = int.from_bytes(data_stream.read(4), byteorder="little")
                file_list_stream.seek(fol_name_offset)
                fol_name = file_list_stream.read(fol_name_size).decode('utf-8', errors='ignore')
                folder_list.append(fol_name)

            data_stream.seek(file_list_offset)
            dmkp_size = 0
            file_list = []

            for _ in range(file_count):
                compression_data_offset = int.from_bytes(data_stream.read(4), byteorder="little")
                compression_data_size = int.from_bytes(data_stream.read(4), byteorder="little")
                file_hash = int.from_bytes(data_stream.read(4), byteorder="little")
                name_offset = int.from_bytes(data_stream.read(4), byteorder="little")
                name_long = int.from_bytes(data_stream.read(4), byteorder="little")
                unzip_size = int.from_bytes(data_stream.read(4), byteorder="little")
                pak_data_offset = int.from_bytes(data_stream.read(4), byteorder="little")
                pak_data_size = int.from_bytes(data_stream.read(4), byteorder="little")
                file_list_stream.seek(name_offset)
                file_name = file_list_stream.read(name_long).decode('utf-8', errors='ignore')
                file_list.append(file_name)
                dmkp_size += pak_data_size

            Offsets = namedtuple('Offsets',
                                 ['unk', 'vol', 'offset', 'size', 'zip_size'])
            offsets = []

            # data_stream.seek(file_data_start + 0x174)
            data_stream.seek(file_data_start)

            for _ in range(file_count):
                tfa = hex(data_stream.tell())
                offsets.append(
                    Offsets(
                        int.from_bytes(data_stream.read(1), byteorder="little"),  # unk
                        int.from_bytes(data_stream.read(2), byteorder="little"),  # vol
                        int.from_bytes(data_stream.read(5), byteorder="little"),  # offset
                        int.from_bytes(data_stream.read(4), byteorder="little"),  # size
                        int.from_bytes(data_stream.read(4), byteorder="little")   # zip_size
                    )
                )

            # blob_list = [f'{only_name}-{str(i).rjust(3, "0")}.rmdblob' for i in range(blob_count)]
            blob_list = sorted(blob_list)
            print(blob_list)

            blobs = [open(b, 'rb') for b in blob_list]

            for i in range(file_count):
                path = f"{self.output_folder}\\{file_list[i]}"

                ol = offsets[i]
                blobs[ol.vol - 1].seek(ol.offset)
                file_data = blobs[ol.vol - 1].read(ol.size)
                # os.makedirs(os.path.dirname(path), exist_ok=True)

                try:

                    with open(path, 'wb') as nf:
                        # nf.write(file_data.strip(b'\0'))
                        nf.write(file_data)

                # TODO: УБРАТЬ КОСТЫЛИ!!!
                except (OSError, ValueError):
                    dat = self.get_ext(file_data[:4])
                    path = f"{self.output_folder}\\{i}.{dat}"

                    with open(path, 'wb') as nf:
                        # nf.write(file_data.strip(b'\0'))
                        nf.write(file_data)

                self.update_pb(file_count, i + 1, path)

            for b in blobs:
                b.close()
