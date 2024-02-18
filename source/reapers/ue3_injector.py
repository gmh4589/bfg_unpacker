import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class U3Injector(Reaper):
    # TODO: Need testing

    def __init__(self):
        super().__init__()
        self.source_folder = ''
        self.new_folder = ''

    @file_reaper
    def run(self):

        if not self.source_folder or self.new_folder:
            self.update_signal.emit(100, '', localize.done, True)
            return

        source_fl = os.listdir(self.source_folder)
        new_fl = os.listdir(self.new_folder)
        all_files = len(source_fl)

        if len(source_fl) != len(new_fl):
            print('Количество файлов в исходной и новой папках не равно!\n'
                  'Для выхода из программы нажмите ENTER')
            return

        with open(self.file_name, 'rb') as sa:
            source_data = bytearray(sa.read())

        for i in range(all_files):

            source_file = os.path.join(self.source_folder, source_fl[i])
            new_file = os.path.join(self.new_folder, new_fl[i])

            with open(source_file, 'rb') as sf:
                source_df = bytearray(sf.read())

            with open(new_file, 'rb') as sf:
                nf_data = bytearray(sf.read())

            index = source_data.find(source_df)

            if index > -1:
                size_old = os.path.getsize(source_file)
                size_new = os.path.getsize(new_file)
                arc_size = os.path.getsize(self.file_name)

                with open(new_file, 'rb') as nf:
                    n_data = bytearray(nf.read())

                if size_new <= size_old:
                    d1 = source_data.split(source_df)
                    zeros = bytearray(b'\x00' * (size_old - size_new))
                    source_data = d1[0] + n_data + zeros + d1[1]
                    ic('Новые данные были добавлены в середину файла')

                else:
                    new_offset = bytearray(arc_size.to_bytes(4, 'little'))
                    source_data[index-4] = new_offset[0]
                    source_data[index-3] = new_offset[1]
                    source_data[index-2] = new_offset[2]
                    source_data[index-1] = new_offset[3]

                    source_data += nf_data
                    ic('Новые данные были добавлены в конец файла')

            else:
                ic(f'Файл {source_fl[i]} не был найден в исходном архиве и будет пропущен...')

            percent = int((100 / all_files) * i)
            self.update_signal.emit(percent, f'{i}/{all_files}', f'{localize.saving} - {source_fl[i]}...', False)

        arch_name = self.file_name.split('/').pop(-1)

        with open(os.path.join(self.output_folder, arch_name), 'wb') as new_dat:
            new_dat.write(bytes(source_data))

        self.update_signal.emit(100, '', localize.done, True)
