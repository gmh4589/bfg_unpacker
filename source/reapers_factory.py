import os
from icecream import ic

from source.ui import localize
from source import reapers
from source.reapers import zip_archive, locres, strings
from source.file_data import FileData


class ReapersFactory:

    def __init__(self, reapers_table, func_name='', script_name=''):
        self.reapers_table = reapers_table
        self.proc = {}
        self.func_name = func_name
        self.script_name = script_name

    @staticmethod
    def get_class(path: str):

        try:
            parts = path.split('.')
            obj = reapers
            ic(parts)

            for part in parts:
                ic(part)
                obj = getattr(obj, part)

            return obj()
        
        except AttributeError:
            return None

    def calculate_weights(self, file_info, candidates):

        if len(candidates) == 1:
            return candidates
        
        weights = {}

        for idx in candidates:
            weight = 0

            for attr in ['ext', 'file_name', 'magic1', 'magic2', 'magic3']:
                val = getattr(file_info, attr)
                db_val = self.reapers_table[attr][idx]

                if db_val == '*':
                    continue
                elif isinstance(db_val, str):
                    weight += 1 if val == db_val else -10
                else:
                    db_val = db_val.item()

                    if db_val > -1:
                        weight += 1 if db_val == val else -1

            ic(self.reapers_table['ext'][idx], idx, weight)
            weights[idx] = weight

        max_value = max(weights.values())
        weights = [key for key, val in weights.items() if val == max_value]
        ic(weights, max_value)

        return weights
    
    def show_file_type(self, idx):
                
        if self.reapers_table['file_type'][idx] is not None:
            print(f"{localize.file_type} {self.reapers_table['file_type'][idx]}")
            ic(f"{localize.file_type} {self.reapers_table['file_type'][idx]}")
        else:
            print(f"{localize.file_type} {self.reapers_table['class_path'][idx]}")
            ic(f"{localize.file_type} {self.reapers_table['class_path'][idx]}")

    def get_list(self, col_name, for_equal):
        lst = list(self.reapers_table[col_name])
        result = [e for e in range(len(lst)) if lst[e] == for_equal]
        return result

    def get_reaper(self):

        keys = list(set(self.get_list('ext', self.file_data.ext)
                        # + self.get_list('file_name', self.file_data.file_name)
                        # + self.get_list('magic1', self.file_data.magic1)
                        # + self.get_list('magic2', self.file_data.magic2)
                        # + self.get_list('magic3', self.file_data.magic3)

                        + self.get_list('ext', '*')
                        # + self.get_list('file_name', '*')
                        # + self.get_list('magic1', -1)
                        # + self.get_list('magic2', -1)
                        # + self.get_list('magic3', -1)
                   ))

        ic(len(keys))

        if keys:
            weights = self.calculate_weights(self.file_data, keys)
            ic(weights)

            for k in weights:
                self.proc[self.reapers_table['file_type'][k]] = [
                    self.get_class(self.reapers_table['class_path'][k]),
                    self.reapers_table['script'][k],
                    self.reapers_table['progress'][k]
                ]

    def find_reaper(self, fn, fp=''):

        if os.path.exists(fn):
            self.proc = {}
            self.file_data = FileData(fn)
            ic(self.file_data)

            # Check on ZIP signature
            if self.file_data.magic1 == int.from_bytes(b'PK\x03\x04', 'little'):
                self.proc = zip_archive.Zip()
            else:
                self.get_reaper()

        return self.proc
            