import os
# import io
# import lz4.frame as lz4
from collections import namedtuple
from source.reaper import Reaper, file_reaper
from source.codecs.zip_methods import zip_methods


class AlanWake2(Reaper):

    @file_reaper
    def run(self):

        only_name = self.file_name.split('.')[0]
        toc_file = f'{only_name}.rmdtoc'

        with open(toc_file, "rb") as toc:
            magic = toc.read(4)
            version = int.from_bytes(toc.read(4), byteorder="little")

            if not self.magic([b'COTR', ], magic, 'Alan Wake 2'):
                return

            if not self.magic([2, ], version, 'Alan Wake 2'):
                return

            toc.seek(0x14)
            blob_count = int.from_bytes(toc.read(4), byteorder="little")
            blob_list = [f'{only_name}-{str(i).rjust(3, "0")}.rmdblob' for i in range(blob_count)]
            toc.seek(0x24)
            file_count = int.from_bytes(toc.read(4), byteorder="little")
            file_list_start = int.from_bytes(toc.read(4), byteorder="little")
            file_list_len = int.from_bytes(toc.read(4), byteorder="little")
            toc.seek(0x50)
            file_data_start = int.from_bytes(toc.read(4), byteorder="little")

            print(blob_list)

            toc.seek(0x1000)
            file_datas = toc.read()

            # data_stream = io.BytesIO(lz4.decompress(file_datas))
            temp_file = self.output_folder + '\\file_list.dat'

            with open(temp_file, 'wb') as fl:
                fl.write(file_datas)

            self.unzip(temp_file, zip_methods.LZ4)

            with open(temp_file, 'rb') as fd:
                fd.seek(file_list_start - 0x10)
                a = hex(fd.tell())
                vols_len = int.from_bytes(fd.read(4), byteorder="little")
                fd.seek(8, 1)
                folders_len = int.from_bytes(fd.read(4), byteorder="little")
                fd.seek(file_list_start + vols_len + folders_len)
                b = hex(fd.tell())
                file_list = fd.read(file_list_len)

                file_list = file_list.split(b'\x2ewem')
                file_list.append(b'')
                Offsets = namedtuple('Offsets',
                                     ['vol', 'offset', 'size'])
                offsets = []

                with open(temp_file, 'rb') as tf:
                    tf.seek(file_data_start + 0x174)

                    for _ in range(file_count):
                        tfa = hex(tf.tell())

                        offsets.append(
                            Offsets(
                                int.from_bytes(tf.read(2), byteorder="little"),  # vol
                                int.from_bytes(tf.read(5), byteorder="little"),  # offset
                                int.from_bytes(tf.read(4), byteorder="little")   # size
                            )
                        )

                        tf.seek(5, 1)

                blobs = [open(b, 'rb') for b in blob_list]

                for i, name in enumerate(file_list):
                    name = (name + b'.wem').decode('utf-8', 'ignore')
                    name = name.split('_')

                    name = '\\'.join(name)
                    path = os.path.join(self.output_folder, name)
                    ol = offsets[i]
                    blobs[ol.vol - 1].seek(ol.offset)

                    try:
                        os.makedirs(os.path.dirname(path), exist_ok=True)
                        file_data = blobs[ol.vol - 1].read(ol.size)

                        with open(path, 'wb') as nf:
                            nf.write(file_data.strip(b'\0'))

                        self.update_pb(file_count, i + 1, name)

                    # TODO: УБРАТЬ КОСТЫЛИ!!!
                    except (OSError, ValueError):
                        pass

                for b in blobs:
                    b.close()
