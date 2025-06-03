
import json
import os
from collections import namedtuple

from source.reaper import Reaper, file_reaper
from source.ui import localize


class Strings2TXT(Reaper):

    @file_reaper
    def run(self):
        ext = os.path.splitext(self.file_name)[1].lower()

        with open(self.file_name, 'rb') as string:
            file_size = os.path.getsize(self.file_name)
            count = int.from_bytes(string.read(4), byteorder="little")
            text_size = int.from_bytes(string.read(4), byteorder="little")
            text_offset = file_size - text_size
            TextData = namedtuple('TextData', ["index", "offset"])
            text_data = []
            text_dict = {'type': ext.replace('.', '')}

            for i in range(count):
                text_data.append(
                    TextData(
                        index=int.from_bytes(string.read(4), byteorder="little"),
                        offset=int.from_bytes(string.read(4), byteorder="little")
                    ))

            for j, text in enumerate(text_data):
                str_offset = text_offset + text.offset
                string.seek(str_offset)

                if ext == '.strings':
                    t_data = string.read().split(b'\0')[0]

                    try:
                        str_data = t_data.decode('utf-8')
                    except UnicodeDecodeError:
                        str_data = t_data.decode('cp1251')
                        
                else:
                    str_length = int.from_bytes(string.read(4), byteorder="little")
                    t_data = string.read(str_length).strip(b'\0')

                    try:
                        str_data = t_data.decode('utf-8')
                    except UnicodeDecodeError:
                        str_data = t_data.decode('cp1251')

                text_dict[text.index] = {'original': str_data, 'translate': str_data}

                if j % 1000 == 0:
                    self.update_pb(count, j, str_data)

        output = f"{self.output_folder}\\{os.path.basename(self.file_name).lower().replace(ext, '.json')}"

        with open(output, 'w') as output:
            try:
                json.dump(text_dict, output, indent=4, ensure_ascii=False)
            except UnicodeEncodeError:
                json.dump(text_dict, output, indent=4)

        self.update_pb(count, count, localize.done)


class TXT2Strings(Reaper):

    @file_reaper
    def run(self):
        magic = b''
        header = b''
        text = b''
        
        with open(self.file_name, 'r') as file:
            strings = json.load(file)

        count = len(strings) - 1
        json_type = strings['type']
        magic += count.to_bytes(4, byteorder='little')
        
        for i, key in enumerate(strings):

            if key != 'type':
                text_data = strings[key]['translate'].encode('utf-8') + b'\0'
                header += int(key).to_bytes(4, byteorder='little')
                header += len(text).to_bytes(4, byteorder='little')

                if json_type in ('ilstrings', 'dlstrings'):
                    text += len(text_data).to_bytes(4, byteorder='little')

                text += text_data
                
                if i % 1000 == 0:
                    self.update_pb(count, i, text_data)
 
        ext = os.path.splitext(self.file_name)[1].lower()
        out_path = f"{self.output_folder}\\{os.path.basename(self.file_name).replace(ext, f".{json_type}")}"
        magic += len(text).to_bytes(4, byteorder='little')
        
        with open(out_path, 'wb') as nf:
            nf.write(magic + header + text)
        
        self.update_pb(count, count, localize.done)
