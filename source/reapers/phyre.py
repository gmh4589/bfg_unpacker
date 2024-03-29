
import os
from PIL import Image
from icecream import ic

from source.reapers import image_tools
from source.reaper import Reaper, file_reaper
from source.ui import localize


class PhyreSave(Reaper):

    def phyre_save(self):
        ext = self.file_name.split('.')[-1]

        with open(self.file_name, 'rb') as image_file:

            image_file.seek(84)
            dds_codec = image_file.read(4)

            if ext == 'dds':
                start = 128
                codec = b'ARGB8' if dds_codec == b'\x00' * 4 else dds_codec
                image_file.seek(12)
                x = int.from_bytes(image_file.read(4), byteorder='little')
                y = int.from_bytes(image_file.read(4), byteorder='little')
            elif ext == 'bmp':
                start = 150
                codec = b'ARGB8'
                x, y = Image.open(self.file_name).size
            elif ext == 'png':
                start = 0
                codec = b'ARGB8'
                x, y = Image.open(self.file_name).size
            elif ext == 'gxt':
                start = 0
                codec = b'DXT5'
                x, y = 0, 0

            image_file.seek(start)
            image_data = Image.open(self.file_name).tobytes() if ext == 'png' else image_file.read()

        bin_file = self.file_name.replace(ext, 'bin') if ' (Texture ' not in self.file_name \
            else f"{self.file_name.split(' (Texture ')[0]}.bin"

        with open(bin_file, 'rb') as head_file:
            head_file.seek(12)
            platform = head_file.read(4)
            head_file.seek(0)
            head_data = head_file.read()

            if platform == b'11XD':  # PC
                pref = b'\x00' * 75
                postfix = b'\x48\x02\x08\x31\x00'
                codec = head_data[-5:]
                ext = head_data[-200:]
                ext = 'dds' if b'dds' in ext else 'png'
                head_data = head_data[:-76]

                if 'png' in self.file_name and ext == 'dds':
                    os.system(f'./data/dds_tools/texconv.exe '
                              f'-f {"B8G8R8A8_UNORM" if codec == b"ARGB8" else "R8G8B8A8_UNORM"} '
                              f'"{self.file_name}"')
                    self.file_name = self.file_name.replace('png', 'dds')
                    return self.phyre_save()

            elif platform == b'\x01MXG':  # PS Vita
                pref = b'\x00' * 4
                postfix = b'\x4C\x02\x08\x31\x00'
                ext = 'dds'
            elif platform == b'1XNG':  # Nintendo Switch
                pref = b'\x01\x00\x00\x00'
                postfix = b'\x4E\x02\x08\x01\x00'
                ext = 'dds' if 'dds' in self.file_name else 'png'

        new_file = f"{self.file_name.split('.')[0]}.{ext}_new.phyre" if ' (Texture ' not in self.file_name \
            else f"{self.file_name.split(' (Texture ')[0]}.{ext}_new.phyre"

        if platform == b'\x01MXG':

            if ext == 'png':
                print(os.path.dirname(self.file_name))
                gxt_name = bin_file.replace("bin", "gxt")
                os.system(f'./data/dds_tools/texconv.exe '
                          f'-f {"BC3_UNORM" if codec == b"DXT5" else "BC1_UNORM"} '
                          f'"{self.file_name}"')
                os.system(f'./data/ps_tools/vita/psp2gxt.exe '
                          f'-i "{self.file_name.replace("png", "dds")}" '
                          f'-o "{gxt_name}"')

                with open(gxt_name, 'rb') as gxt_data:
                    new_image_data = gxt_data.read()

                with open(new_file, 'wb') as new_phyre:
                    new_phyre.write(head_data + new_image_data)

            elif ext == 'gxt':
                with open(new_file, 'wb') as new_phyre:
                    new_phyre.write(head_data + image_data)

        else:
            with open(new_file, 'wb') as new_phyre:
                new_phyre.write(head_data + x.to_bytes(4, byteorder='little') +
                                y.to_bytes(4, byteorder='little') + pref + b'\x00PTexture2D\x00' + codec +
                                b'\x00\x08\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00' +
                                (b'\x06' if codec in (b'ARGB8', b'RGBA8') else b'\x05') +
                                b'\x00\x00\x00\x0B\x00\x00\x00\x58\x02\x00\x01\x48\x04\x01\x48' + postfix + image_data)

    @file_reaper
    def run(self):

        if self.file_name.split('.')[-1] != 'phyre':
            self.phyre_save()

        else:
            dir_path = os.path.dirname(self.file_name)
            name = os.path.basename(self.file_name).split('.')[0]

            if 'dds' in self.file_name:
                ft = b'dds\x00'
                file_type = 'dds'
                head_size = 42
            elif 'png' in self.file_name:
                ft = b'png\x00'
                file_type = 'png'
                head_size = 43
            else:
                print(localize.not_correct_file.replace('%%', 'Phyre'))
                return

            with open(self.file_name, 'rb') as phyre:

                phyre.seek(4)
                size = int.from_bytes(phyre.read(4), byteorder='little')
                metaSize = int.from_bytes(phyre.read(4), byteorder='little')
                platform = phyre.read(4)
                supported = [b'1XNG', b'\x01MXG', b'11XD']

                if platform == b'\x01MXG':
                    ft = b'GXT\x00'
                    file_type = 'gxt' if 'dds' in self.file_name else 'gxt_png'
                    head_size = 42 if 'dds' in self.file_name else 107

                if platform not in supported:
                    print(localize.unsupported_platform)
                    return

                phyre.seek(72, 1)
                baseHeaderSize = int.from_bytes(phyre.read(4), byteorder='little')
                varsCount = int.from_bytes(phyre.read(4), byteorder='little')
                dirsCount = int.from_bytes(phyre.read(4), byteorder='little')
                paramsCount = int.from_bytes(phyre.read(4), byteorder='little')
                tableSize = int.from_bytes(phyre.read(4), byteorder='little')
                stringTableOffset = size + metaSize - tableSize
                phyre.seek(8, 1)
                startTableDataStart = phyre.tell()

                phyre.seek(stringTableOffset)
                table = phyre.read(tableSize)
                stringTable = [t.decode('utf-8') for t in table.split(b'\x00')][:-1]

                with open('temp.dat', 'wb') as temp_file:
                    temp_file.write(table)

                phyre.seek(startTableDataStart)

                paramsList = {}

                def getName(o):

                    with open('temp.dat', 'rb') as temp2:
                        temp2.seek(o)
                        return temp2.read().split(b'\x00')[0].decode('utf-8')

                for c in range(varsCount):
                    offset = int.from_bytes(phyre.read(4), byteorder='little')
                    paramsList[getName(offset)] = {'offset': offset}

                for d in range(varsCount, varsCount + dirsCount):
                    parentDirId = int.from_bytes(phyre.read(4), byteorder='little')
                    data = phyre.read(4)
                    offset = int.from_bytes(phyre.read(4), byteorder='little')
                    magic = [phyre.read(4) for _ in range(6)]
                    paramsList[getName(offset)] = {'parentDirId': parentDirId,
                                                   'data': data,
                                                   'offset': offset,
                                                   'magic': magic}

                for e in range(dirsCount + varsCount, len(stringTable) + 6):
                    offset = int.from_bytes(phyre.read(4), byteorder='little')
                    tp = int.from_bytes(phyre.read(4), byteorder='little')
                    magic = [phyre.read(4) for _ in range(4)]
                    paramsList[getName(offset)] = {'offset': offset,
                                                   'type': tp,
                                                   'magic': magic}

                phyre.seek(0)
                data = phyre.read().split(b'\x00PTexture2D\x00')
                image = data[-1]

            size = data[-2].split(ft)[-1]
            p = image[:5]
            image_data = image[head_size:]

            if platform == b'11XD':
                x = int.from_bytes(size[-79:-75], byteorder='little')
                y = int.from_bytes(size[-83:-79], byteorder='little')
            elif platform == b'\x01MXG':
                sizes = image[:head_size]
                p = sizes[:5]
                x = int.from_bytes(sizes[99:101], byteorder='little')
                y = int.from_bytes(sizes[101:103], byteorder='little')
            else:
                x = int.from_bytes(size[-8:-4], byteorder='little')
                y = int.from_bytes(size[-12:-8], byteorder='little')

            # Сохраняет заголовок файла, без размеров текстуры и кодека
            with open(f'{dir_path}\\{name}.bin', 'wb') as head_file:

                head_data = b''

                for d in range(len(data) - 1):
                    head_data += data[d] + b'\x00PTexture2D\x00'

                head_data = head_data[:-24]

                if platform == b'11XD':
                    head_file.write(head_data)
                elif platform == b'1XNG':
                    head_file.write(head_data + p)
                elif platform == b'\x01MXG':
                    head_file.write(head_data + b'\x00' * 13 + b'PTexture2D\x00' + image[:head_size])

            if file_type == 'dds':
                image_tools.dds_save(x, y, p, name, image_data)
            elif file_type == 'png' or file_type == 'gxt_png':
                image_tools.png_save(x, y, p, name, image_data)
            elif file_type == 'gxt':
                image_tools.gxt_save(name, image_data)

            print(f'{localize.saving} - {name}.{file_type}')
            ic(name, file_type)
            self.update_signal.emit(100, '', localize.done, True)
