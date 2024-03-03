import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class UE3(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as upk:

            if upk.read(4) != b'\xC1\x83\x2A\x9E':
                return

            upk.seek(0)
            # all_data = upk.read()
            default_name = self.file_name.split('/')[-1].split('.')[0]

            # if b'OggS' in all_data:
            #     splitter = b'OggS'
            #     ext_list = [b'.wav', b'.WAV', b'.ogg', b'.OGG']
            #     ext = '.ogg'
            # elif b'RIFF' in all_data or b'RIFX' in all_data:
            #     splitter = b'RIFF'
            #     ext_list = [b'.wav', b'.WAV']
            #     ext = '.wav'
            # elif b'DDS\x20' in all_data:
            #     splitter = b'DDS\x20'
            #     ext_list = [b'.dds', b'.DDS']
            #     ext = '.dds'

            upk.seek(0x21)
            count = int.from_bytes(upk.read(4), byteorder="little")
            start = int.from_bytes(upk.read(4), byteorder="little")
            upk.seek(start)
            datas = {}

            for a in range(count):
                upk.seek(0x20, 1)
                long = int.from_bytes(upk.read(4), byteorder="little")
                offset = int.from_bytes(upk.read(4), byteorder="little")
                datas[a] = {'long': long, 'offset': offset}
                upk.seek(0x1c, 1)

            for key, value in datas.items():
                upk.seek(value['offset'])
                raw_data = upk.read(value['long'])
                name = f'{default_name}_{key}.dat'
                ic(name)

                with open(os.path.join(self.output_folder, name), 'wb') as out_file:
                    out_file.write(raw_data)

                # meta_list = raw_data.split(splitter)
                # meta_data = meta_list[0]
                #
                # if len(meta_list) > 1:
                #
                #     for ext in ext_list:
                #
                #         if ext in meta_data:
                #             name = meta_data.split(ext)[0].split(b'\x5c')[-1].decode('utf-8')
                #             break
                #
                #     write_data = raw_data.replace(meta_data, b'')
                #     head_data = raw_data.replace(write_data, b'')
                #     ic(name)
                #
                #     if len(write_data) > 0:
                #
                #         with open(f'out\\{name}{ext}', 'wb') as out:
                #             out.write(write_data)
                #
                #         with open(f'out\\{name}_head.dat', 'wb') as out:
                #             out.write(head_data)
                #
                # else:
                #     name = f'{default_name}_{key}.dat'
                #
                #     with open(f'out\\{name}', 'wb') as out:
                #         out.write(write_data)


                print(f'{key}/{count}: {localize.saving} - {name}...')
                self.update_signal.emit(int(100 / count * key), f'{key}/{count}',
                                        f'{localize.saving} - {name}...', False)

        self.update_signal.emit(100, f'{count}/{count}', localize.done, True)
