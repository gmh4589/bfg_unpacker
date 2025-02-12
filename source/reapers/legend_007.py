import os
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

        bin_data = open(bin_file, "rb")
        num_data = open(num_file, 'rb')

        bin_magic = bin_data.read(4)
        num_magic = num_data.read(4)

        if (not self.magic([b'MUSX', b'816\x0d'], num_magic, '007 Legend')
                or not self.magic([b'\x0b\0\0\0', b'\0\0\0\x0b'], bin_magic, '007 Legend')):
            return

        # num_data.seek(0x10)
        # platform = num_data.read(4).decode('utf-8').replace('_', '')
        #
        # byte_order = 'little' if platform == 'PC' else 'big'

        num_data.seek(0)
        files_data = num_data.read().split(b'\xAB\xAB\xAB\xAB')
        files_data = [file for file in files_data if file]
        file_count = len(files_data)

        for i, data in enumerate(files_data):
            name = f"{i:08}.{self.get_ext(data[:4])}"
            path = os.path.join(self.output_folder, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, 'wb') as new_file:
                new_file.write(data)

            self.update_pb(file_count, i + 1, name)

        bin_data.close()
        num_data.close()
