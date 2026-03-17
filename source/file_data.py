import json
import os


class FileData:
    path: str
    ext: str
    file_name: str
    magic1: int
    magic2: int
    magic3: int
    json_type: str

    def __init__(self, fn):
        base_name = os.path.basename(fn)
        name_split = base_name.lower().split('.')

        if '.' in base_name:
            self.ext = name_split.pop(-1)
            self.file_name = '.'.join(name_split)
        else:
            self.ext = '*'
            self.file_name = base_name
        
        if self.ext == 'json':
                
            with open(fn, 'r') as js:

                try:
                    json_data = json.load(js)
                except (PermissionError, FileNotFoundError, FileExistsError, UnicodeDecodeError):
                    json_data = {}
            
            self.json_type = json_data.get('type', 'unknown')

        try:

            with open(fn, 'rb') as fff:
                self.magic1 = int.from_bytes(fff.read(4), byteorder="little")
                self.magic2 = int.from_bytes(fff.read(4), byteorder="little")
                self.magic3 = int.from_bytes(fff.read(4), byteorder="little")

        except (PermissionError, FileNotFoundError, FileExistsError):
            self.magic1 = self.magic2 = self.magic3 = None

