import os
import io
import lz4.block as lz4
from collections import namedtuple

from source.reaper import Reaper, file_reaper
from source.ui import localize


class AlanWake2(Reaper):

    @file_reaper
    def run(self):
        only_name = self.file_name.split('.')[0].split('-0')[0]
        toc_file = f'{only_name}.rmdtoc'
        toc_base_name = os.path.basename(toc_file)
        print(toc_file)

        if not os.path.exists(toc_file):
            self.update_pb(100, 100, f"{localize.file} {toc_base_name} {localize.do_not_exist}!")
            return

        with (open(toc_file, "rb") as toc):
            magic = toc.read(4)
            version = int.from_bytes(toc.read(4), byteorder="little")

            if (not self.magic([b'COTR', ], magic, 'Alan Wake 2') or
                    not self.magic([2, ], version, 'Alan Wake 2')):
                return

            in_dir = os.path.dirname(self.file_name)
            list_data_offset = int.from_bytes(toc.read(4), byteorder="little")
            list_blocks = int.from_bytes(toc.read(4), byteorder="little") / 0x10
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

            ZipBlocks = namedtuple('ZipBlocks',
                                   ['dummy', 'offset', 'dummy3', 'size', 'zip_size'])
            lz4_blocks = []
            toc.seek(list_data_offset)

            for _ in range(int(list_blocks)):
                lz4_blocks.append(
                    ZipBlocks(
                        int.from_bytes(toc.read(3), byteorder="little"),
                        int.from_bytes(toc.read(4), byteorder="little"),
                        int.from_bytes(toc.read(1), byteorder="little"),
                        int.from_bytes(toc.read(4), byteorder="little"),
                        int.from_bytes(toc.read(4), byteorder="little"),
                    )
                )

            blocks = b''

            for i, block in enumerate(lz4_blocks):
                toc.seek(block.offset)
                data = toc.read(block.zip_size)
                decompress_data = lz4.decompress(data, block.size)
                blocks += decompress_data

            data_stream = io.BytesIO(blocks)

            BlobList = namedtuple('BlobList',
                                  ['offset', 'size', 'hash'])
            blob_list = []
            data_stream.seek(blob_offset)

            for _ in range(blob_count):
                blob_list.append(
                    BlobList(
                        int.from_bytes(data_stream.read(4), byteorder="little") + file_list_start,  # Offset
                        int.from_bytes(data_stream.read(4), byteorder="little"),                    # Size
                        int.from_bytes(data_stream.read(8), byteorder="little")                     # Hash
                    )
                )

            data_stream.seek(folder_list_offset)
            FolderList = namedtuple('FolderList',
                                    ['tree_level', 'folder_index', 'folders_in_folder', 'file_index',
                                     'files_in_folder', 'fol_name_offset', 'fol_name_size'])
            folder_list = []

            for _ in range(folder_count):
                folder_list.append(
                    FolderList(
                        tree_level=int.from_bytes(data_stream.read(4), byteorder="little"),
                        folder_index=int.from_bytes(data_stream.read(4), byteorder="little"),
                        folders_in_folder=int.from_bytes(data_stream.read(4), byteorder="little"),
                        file_index=int.from_bytes(data_stream.read(4), byteorder="little"),
                        files_in_folder=int.from_bytes(data_stream.read(4), byteorder="little"),
                        fol_name_offset=int.from_bytes(data_stream.read(4), byteorder="little") + file_list_start,
                        fol_name_size=int.from_bytes(data_stream.read(4), byteorder="little")
                    )
                )

            data_stream.seek(file_list_offset)
            FileList = namedtuple('FileList',
                                    ['unk1', 'unk2', 'unk3', 'name_offset', 'name_long', 'unk4', 'unk5', 'unk6'])
            file_list = []

            for _ in range(file_count):
                file_list.append(
                    FileList(
                        int.from_bytes(data_stream.read(4), byteorder="little"),
                        int.from_bytes(data_stream.read(4), byteorder="little"),
                        int.from_bytes(data_stream.read(4), byteorder="little"),
                        int.from_bytes(data_stream.read(4), byteorder="little") + file_list_start,  # name_offset
                        int.from_bytes(data_stream.read(4), byteorder="little"),                    # name_long
                        int.from_bytes(data_stream.read(4), byteorder="little"),
                        int.from_bytes(data_stream.read(4), byteorder="little"),
                        int.from_bytes(data_stream.read(4), byteorder="little")
                    )
                )

            blob_name_list = []
            folder_name_list = []
            file_name_list = []

            for blob in blob_list:
                o = blob.offset
                s = blob.size
                data_stream.seek(o)
                n = data_stream.read(s)
                blob_name_list.append(n.decode('utf-8').replace('../pc', in_dir))

            for fol in folder_list:
                fo = fol.fol_name_offset
                fs = fol.fol_name_size
                data_stream.seek(fo)
                fn = data_stream.read(fs)
                folder_name_list.append(fn)

            for _, file in enumerate(file_list):
                so = file.name_offset
                sn = file.name_long
                data_stream.seek(so)
                name = data_stream.read(sn)
                file_name_list.append(name.decode('utf-8'))

            Offsets = namedtuple('Offsets',
                                 ['unk', 'vol', 'offset', 'unk2', 'size', 'zip_size'])
            offsets = []

            data_stream.seek(file_data_start)

            for _ in range(file_count):
                offsets.append(
                    Offsets(
                        int.from_bytes(data_stream.read(1), byteorder="little"),  # unk
                        int.from_bytes(data_stream.read(2), byteorder="little"),  # vol
                        int.from_bytes(data_stream.read(4), byteorder="little"),  # offset
                        int.from_bytes(data_stream.read(1), byteorder="little"),  # unk2
                        int.from_bytes(data_stream.read(4), byteorder="little"),  # size
                        int.from_bytes(data_stream.read(4), byteorder="little")   # zip_size
                    )
                )

            try:
                blobs = [open(b, 'rb') for b in blob_name_list]
            except (FileNotFoundError, FileExistsError, PermissionError):
                self.update_pb(100, 100, f"Files {blob_name_list} do not exist or unavailable!")
                return

            for i in range(file_count):
                path = f"{self.output_folder}\\{file_name_list[i]}"

                ol = offsets[i]
                vol = ol.vol
                blobs[vol].seek(ol.offset)

                if ol.zip_size == 0:
                    file_data = blobs[vol].read(ol.size)
                else:
                    file_data = blobs[vol].read(ol.zip_size)

                    try:
                        file_data = lz4.decompress(file_data, ol.size)
                    except lz4.LZ4BlockError:
                        pass

                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as nf:
                    nf.write(file_data)

                self.update_pb(file_count, i + 1, path)

            for b in blobs:
                b.close()
