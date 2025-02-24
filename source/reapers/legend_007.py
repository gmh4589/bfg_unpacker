import os

from icecream import ic

from source.reaper import Reaper, file_reaper


class Legend007(Reaper):
    # TODO Don't work with filelist.000, filelist.001, filelist.002, filelist.003, filelist.bin (b'MOEG' header)

    @file_reaper
    def run(self):
        ext = self.file_name.split('.')[-1].lower()

        if ext == 'bin':
            bin_file = self.file_name
            num_file = self.file_name.lower().replace('bin', '000')
        else:
            bin_file = self.file_name.lower().replace(ext, 'bin')
            num_file = self.file_name

        if not os.path.exists(bin_file) or not os.path.exists(num_file):
            print(f'{bin_file} or {num_file} files not exists...')
            return

        file_size = os.path.getsize(num_file)

        with open(num_file, 'rb') as nf:

            if not self.magic([b'MUSX',], nf.read(4), '007 Legend'):
                return

            start_read = 0
            n = 0

            size_dict = {
                362692690: 370688,
                29569164: 800,

            }

            while start_read != file_size:
                nf.seek(start_read + 12)
                new_size = int.from_bytes(nf.read(4), byteorder="little")
                ext = 'mus'

                if new_size > file_size:
                    ic(hex(start_read))
                    new_size = size_dict[new_size]
                    ext = 'dat'

                nf.seek(start_read)
                new_data = nf.read(new_size)

                name = f"{n:08}.{ext}"
                path = os.path.join(self.output_folder, name)
                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as new_file:
                    new_file.write(new_data)

                start_read += new_size
                n += 1
                self.update_pb(file_size, start_read, name)


        # bin_data = open(bin_file, "rb")
        # num_data = open(num_file, 'rb')
        #
        # bin_magic = bin_data.read(4)
        # num_magic = num_data.read(4)
        #
        # if (not self.magic([b'MUSX', b'816\x0d'], num_magic, '007 Legend')
        #         or not self.magic([b'\x0b\0\0\0', b'\0\0\0\x0b'], bin_magic, '007 Legend')):
        #     return
        #
        # num_data.seek(0x10)
        # platform = num_data.read(4).decode('utf-8').replace('_', '')
        #
        # byte_order = 'little' if platform == 'PC' else 'big'
        #
        # bin_len = int.from_bytes(bin_data.read(4), byteorder=byte_order) - 1
        # file_count = int.from_bytes(bin_data.read(4), byteorder=byte_order)
        # dummy = int.from_bytes(bin_data.read(4), byteorder=byte_order)
        # data_block_len = int.from_bytes(bin_data.read(4), byteorder=byte_order) - 8
        #
        # num_data.seek(0)
        # files_data = num_data.read().split(b'\xAB\xAB\xAB\xAB')
        # files_data = [file for file in files_data if file]
        # file_count = len(files_data)
        #
        # for i, data in enumerate(files_data):
        #     name = f"{i:08}.{self.get_ext(data[:4])}"
        #     path = os.path.join(self.output_folder, name)
        #     os.makedirs(os.path.dirname(path), exist_ok=True)
        #
        #     with open(path, 'wb') as new_file:
        #         new_file.write(data)
        #
        #     self.update_pb(file_count, i + 1, name)
        #
        # bin_data.close()
        # num_data.close()
