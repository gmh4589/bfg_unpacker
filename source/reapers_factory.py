import os

from icecream import ic
import numpy as np

from source.ui import localize
from source import reapers
from source.reapers import other_prg, re_engine, unreal, qbms, unity, cel_top, zip_archive, locres, strings
from source.file_data import FileData


class ReapersFactory:

    def __init__(self, reapers_table, func_name='', script_name=''):
        self.reapers_table = reapers_table
        self.proc = None
        self.func_name = func_name
        self.script_name = script_name

    @staticmethod
    def get_class(path):
        parts = path.split('.')
        obj = reapers
        ic(parts)

        for part in parts:
            ic(part)
            obj = getattr(obj, part)

        return obj()

    @staticmethod
    def get_by_func(func_name):
        
        func_reapers = {
                '_REEngine': re_engine.ReEngine(),
                '_Unreal': unreal.Unreal(),
                '_Unreal4': unreal.Unreal(),
                '_QuickBMS': qbms.Q_BMS(),
                '_Unity': unity.Unity(),
                '_CelTop': cel_top.CelTop(),
                '_XISO': other_prg.OtherProg(),
                '_OtherPRG': other_prg.OtherProg(),
                }
        
        return func_reapers.get(func_name, 'not_found')

    def calculate_weights(self, file_info, candidates):
        weights = {}

        for idx in candidates:
            weight = 0
            func = self.reapers_table['class_path'][idx]

            for attr in ['ext', 'file_name', 'magic1', 'magic2', 'magic3']:
                val = getattr(file_info, attr)
                db_val = self.reapers_table[attr][idx]

                if isinstance(db_val, np.int64):
                    db_val = db_val.item()

                if db_val == '*' or db_val == -1:
                    continue
                elif (isinstance(val, str) and db_val in val) or db_val == val:
                    weight += 1
                else:
                    weight -= 1

            ic(func, idx, weight)
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

    def get_list(self, col_name, for_eqal):
        lst = list(self.reapers_table[col_name])
        result = [e for e in range(len(lst)) if lst[e] == for_eqal]
        return result

    def get_reaper(self):

        keys = list(set(self.get_list('ext', self.file_data.ext)
                        + self.get_list('file_name', self.file_data.file_name)
                        + self.get_list('magic1', self.file_data.magic1)
                        + self.get_list('magic2', self.file_data.magic2)
                        + self.get_list('magic3', self.file_data.magic3)
                   ))

        ic(len(keys))

        if len(keys) == 1:
            self.show_file_type(keys[0])
            ic(self.reapers_table['class_path'][keys[0]], self.reapers_table['script'][keys[0]])
            self.proc = self.get_class(self.reapers_table['class_path'][keys[0]])
            self.proc.script_name = self.reapers_table['script'][keys[0]]

        elif len(keys) == 0:
            self.proc = None
        else:
            weights = self.calculate_weights(self.file_data, keys)
            ic(weights)

            if len(weights) == 1:
                self.show_file_type(weights[0])
                self.proc = self.get_class(self.reapers_table['class_path'][weights[0]])
                self.proc.script_name = self.reapers_table['script'][weights[0]]
            else:
                self.proc = {}

                for k in keys:
                    self.proc[self.reapers_table['file_type'][k]] = [
                        self.get_class(self.reapers_table['class_path'][k]),
                        self.reapers_table['script'][k]
                    ]

    def find_reaper(self, fn, fp=''):

        if os.path.exists(fn):
            self.proc = None
            self.file_data = FileData(fn)
            func_try = self.get_by_func(self.func_name)
            ic(self.file_data)

            # Check on ZIP signature
            if self.file_data.magic1 == int.from_bytes(b'PK\x03\x04', 'little'):
                self.proc = zip_archive.Zip()
            
            elif self.file_data.ext == 'json':
                jt = self.file_data.json_type

                match jt:
                    case 'locres':
                        self.proc = locres.TXT2Locres()
                    case jt if jt in ('strings', 'ilstrings', 'dlstrings'):
                        self.proc = strings.TXT2Strings()
                    case 'unknown':
                        self.proc = None

            elif func_try != 'not_found':
                self.proc = func_try

                if '%set_dir%' in self.script_name:
                    self.proc.change_dir = os.path.dirname(fn)
                    self.script_name = self.script_name.replace('%set_dir%', '')

                self.proc.script_name = self.script_name.replace('%out_dir%', fp)
                self.proc.key = self.script_name

            # TODO: Maybe need to rewrite or remove
            elif self.func_name == '_VGM' or self.file_data.ext in ('9tav', 'adpcm', 'afc', 'aif', 'aifc', 'aiff', 'at3', 'at9',
                                                        'aud', 'bgm', 'bnk', 'fsb', 'laif', 'laifc', 'laiff', 'logg',
                                                        'lopus', 'lwav', 'lwma', 'ogg', 'ogg_', 'opus', 'pcm', 'sngw',
                                                        'ss2', 'ue4opus', 'vag', 'wav', 'wem', 'wma', 'xma', 'xna',
                                                        'xopus', 'xvag', 'xwb', 'xwm', 'xwma', ):
                self.proc = other_prg.OtherProg()
                self.proc.script_name = (
                    f'data\\vgmstream\\vgmstream-cli.exe -o '
                    f'"{fp}\\{os.path.basename(fn).lower().replace(self.file_data.ext, "wav")}" '
                    f'"%full_file_name%"'
                )

            # TODO: Maybe need to rewrite or remove
            elif self.func_name == '_Wii_iso':
                self.proc = other_prg.OtherProg()

                try:
                    with open(fn, 'rb') as fff:
                        fff.seek(0x20 if self.file_data.ext == 'iso' else 0x220)
                        name = fff.read(0x40).strip(b'\0').decode('utf-8')
                except UnicodeDecodeError:
                    self.proc = None
                    print('Not valid GameCube or Wii file')

                self.proc.script_name = f'data\\wit\\wit.exe X "%full_file_name%" -d "%out_dir%\\{name}"'

            else:
                self.get_reaper()

        return self.proc
            