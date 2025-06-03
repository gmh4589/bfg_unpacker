import os
import json

from icecream import ic

from source import reapers
from source.qprocess import QProcessList
from source.ui import localize, file_type_selector
from source.reapers import *


class QuickOpen(QProcessList):

    @staticmethod
    def sorry():  # 😢
        print(localize.not_find_unpacker)
        return None

    @classmethod
    def get_reaper(cls, path):
        parts = path.split('.')
        obj = reapers
        ic(parts)

        for part in parts:
            ic(part)
            obj = getattr(obj, part)

        return obj()

    def find_reaper(self):

        if self.file_list:
            fn = self.file_list.pop(0)
            subfolder = bool(int(self.setting['Main']['subfolders']))
            fp = f'{self.out_dir}\\{os.path.basename(fn).replace(".", "_")}'
            ic(fn, self.script_name, self.func_name)

            if len(self.file_list) == 0:
                self.last_run = None

            if os.path.exists(fn):
                self.proc = None

                try:

                    with open(fn, 'rb') as fff:
                        magic1, magic2, magic3 = fff.read(4), fff.read(4), fff.read(4)

                except (PermissionError, FileNotFoundError, FileExistsError):
                    magic1, magic2, magic3 = b'', b'', b''

                base_name = os.path.basename(fn)
                name_split = base_name.lower().split('.')

                if '.' in base_name:
                    ext = name_split.pop(-1)
                    name = '.'.join(name_split)
                else:
                    ext = '*'
                    name = '*'

                ic(name, ext)
                # TODO: big Lost: Via Domus, add from GAUP
                # TODO: Other prg
                # TODO: bundle PayDay 2, Bionic Commando
                # TODO: bin Kyou Kara Maou - Hajimari no Tabi, Bratz, F1 2015, Mr. Driller G,
                #  Fatal Frame\Project Zero, BIN disk image (7zip), BIN archive (?)
                # TODO: Add *.cache from total observer (Source Engine)
                # TODO: cat Add from GAUP and other
                # TODO: coalesced from various Unreal Engine 3 games
                # TODO: dat A Engine, Learning Company Games, Moto Racer 3, Dirt 5
                # TODO: dir Add from GAUP and other
                # TODO: exo
                # TODO: fat Add from GAUP, FAT image
                # TODO: img GTA, Disc Image
                # TODO: ktx
                # TODO: lfs
                # TODO: pac Add PAC from GAUP and other
                # TODO: pak Necrovision, Painkiller
                # TODO: pak idTech2 (QUAKE)
                # TODO: pak ReEngine file list
                # TODO: pak Arx Fatalis and Prey
                # TODO: rpack
                # TODO: add rpa RenPy Engine game
                # TODO: sh Add functions to unpack other file types
                # TODO: Add support for Sin
                # TODO: SND from GAUP
                # TODO: Add function to replace extension
                # TODO: Add Frostbite Engine Support
                # TODO: txt Lumia Saga, Simple text
                # TODO: Check on Unigene Engine game
                # TODO: Check on RED Engine game "w3strings", "archive", "w2strings", "dzip"
                # TODO: Add support for Wolfenstein 3D
                # TODO: Add support for YZ1 and YZ2 archives
                # TODO: *.z Z Archive, LEGO Chess
                # TODO: zpl, add change size to converter
                # TODO: Add functions to convert ESM, ESP, ESL, PEX (this is really need?)
                # TODO: Check NIF from here and maybe add NIF model from other game, check PAL, check PCK, MSF
                #  check RAW, check RES, check REZ, check VID and maybe add selector for video and VID from  here
                # TODO: wad Add other games
                # TODO: Check on RPG Maker game
                # TODO: Check on extension in SAU list
                # TODO: Check LBX from GAUP and SAU, check BOX, FLX, KEY
                # TODO: Check MBX here and upper, check PMM from video and here, check TXZ
                # TODO: SPK (Of orc and human) in seven_zip and GAUP
                # TODO: IDWAV by idTech
                # TODO: Sen Book (TLOH books dat)
                # TODO: Add PCK Unreal 2-3

                # Check on ZIP signature
                if magic1 == b'PK\x03\x04':
                    self.proc = zip_archive.Zip()
                
                elif ext == 'json':
                    
                    with open(fn, 'r') as js:
                        json_data = json.load(js)
                    
                    json_type = json_data.get('type', 'unknown')

                    match json_type:
                        case 'locres':
                            self.proc = locres.TXT2Locres()
                        case 'strings':
                            self.proc = strings.TXT2Strings()
                        case 'ilstrings':
                            self.proc = strings.TXT2Strings()
                        case 'dlstrings':
                            self.proc = strings.TXT2Strings()
                        case 'unknown':
                            self.proc = None

                elif self.func_name == '_QuickBMS':
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = self.script_name

                elif self.func_name == '_Unity':
                    self.proc = unity.Unity()

                elif self.func_name == '_OtherPRG':
                    self.proc = other_prg.OtherProg()

                    if '%set_dir%' in self.script_name:
                        self.proc.change_dir = os.path.dirname(fn) if self.checkBox_Reimport.isChecked() else (fp if subfolder else self.out_dir)
                        self.script_name = self.script_name.replace('%set_dir%', '')

                    self.proc.script_name = self.script_name

                elif self.func_name == '_Innosetup':
                    self.proc = other_prg.OtherProg()
                    self.proc.script_name = f'data\\tools\\innounp.exe -x -d"{fp if subfolder else self.out_dir}" "%full_file_name%"'

                elif self.func_name == '_CelTop':
                    self.proc = cel_top.CelTop()

                elif self.func_name == '_Total':
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = 'data\\wcx\\TotalObserver.wcx'

                elif self.func_name == '_GAUP':
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = 'data\\wcx\\gaup_pro.wcx'

                elif self.func_name == '_SAU':
                    self.proc = other_prg.OtherProg()
                    self.proc.script_name = 'sau'

                elif self.func_name == '_VGM' or ext in ('9tav', 'adpcm', 'afc', 'aif', 'aifc', 'aiff', 'at3', 'at9',
                                                         'aud', 'bgm', 'bnk', 'fsb', 'laif', 'laifc', 'laiff', 'logg',
                                                         'lopus', 'lwav', 'lwma', 'ogg', 'ogg_', 'opus', 'pcm', 'sngw',
                                                         'ss2', 'ue4opus', 'vag', 'wav', 'wem', 'wma', 'xma', 'xna',
                                                         'xopus', 'xvag', 'xwb', 'xwm', 'xwma', ):
                    self.proc = other_prg.OtherProg()
                    self.proc.script_name = (
                        f'data\\vgmstream\\vgmstream-cli.exe -o '
                        f'"{fp if subfolder else self.out_dir}\\{os.path.basename(fn).lower().replace(ext, "wav")}" '
                        f'"%full_file_name%"'
                    )

                elif self.func_name == '_7ZIP':
                    # self.proc = seven_zip.SevenZIP()
                    self.proc = other_prg.OtherProg()
                    self.proc.script_name = f'data\\7zip\\7z.exe x -o"%out_dir%" "%full_file_name%"'

                elif self.func_name == '_REEngine':
                    self.proc = re_engine.ReEngine()
                    self.proc.game_file_list = self.script_name

                elif self.func_name == '_Unreal':
                    self.proc = unreal.Unreal()

                elif self.func_name == '_Unreal4':
                    self.proc = unreal.Unreal()
                    self.proc.key = self.script_name

                elif self.func_name == '_Wii_iso':
                    self.proc = other_prg.OtherProg()

                    try:
                        with open(fn, 'rb') as fff:
                            fff.seek(0x20 if ext == 'iso' else 0x220)
                            name = fff.read(0x40).strip(b'\0').decode('utf-8')
                    except UnicodeDecodeError:
                        self.proc = None
                        print('Not valid GameCube or Wii file')

                    self.proc.script_name = f'data\\wit\\wit.exe X "%full_file_name%" -d "%out_dir%\\{name}"'

                elif self.func_name == '_XISO':
                    self.proc = other_prg.OtherProg()
                    self.proc.script_name = 'data\\tools\\extract-xiso.exe -d "%out_dir%" -x "%full_file_name%"'

                elif self.func_name == '_PS3_PKG':
                    self.proc = other_prg.OtherProg()
                    self.proc.script_name = 'data\\ps_tools\\ps3\\ps3p_pkg_ripper.exe -o "%out_dir%" "%full_file_name%"'

                elif self.func_name == '_PS4_PKG':
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\pkg_cnt.bms"

                elif self.func_name == '_PS3_PSARC':
                    self.proc = other_prg.OtherProg()
                    self.proc.script_name = (f'data\\ps_tools\\ps3\\psarc.exe extract{" --lzma" if magic3 == b"zlib" else ""}'
                                             ' --input="%full_file_name%" --to="%out_dir%"')

                else:
                    lst = list(self.reapers_table['ext'])
                    keys = [e for e in range(len(lst)) if lst[e] == ext]
                    ic(len(keys))

                    if len(keys) == 1:
                        ic(self.reapers_table['class_path'][keys[0]], self.reapers_table['script'][keys[0]])
                        self.proc = self.get_reaper(self.reapers_table['class_path'][keys[0]])
                        self.proc.script_name = self.reapers_table['script'][keys[0]]

                    elif len(keys) == 0:
                        self.proc = None
                        self.sorry()
                    else:
                        check_list = {
                            'file_name': name,
                            'magic1': int.from_bytes(magic1, byteorder="little"),
                            'magic2': int.from_bytes(magic2, byteorder="little"),
                            'magic3': int.from_bytes(magic3, byteorder="little"),
                        }

                        weights = [0 for _ in range(len(keys))]
                        ic(check_list)

                        for k in keys:

                            for c, v in check_list.items():
                                ic(v, self.reapers_table[c][k])

                                if self.reapers_table[c][k] == '*' or self.reapers_table[c][k] == -1:
                                    pass
                                elif self.reapers_table[c][k] == v or (isinstance(v, str) and self.reapers_table[c][k] in v):
                                    weights[keys.index(k)] += 1
                                else:
                                    weights[keys.index(k)] -= 1

                        weights = dict(zip(keys, weights))
                        max_value = max(weights.values())
                        weights = {key: [value, self.reapers_table['class_path'][key]] for key, value in weights.items() if value == max_value}
                        keys = list(weights.keys())
                        ic(weights, keys)

                        if len(weights) == 1:

                            if self.reapers_table['file_type'][keys[0]] is not None:
                                print(f"{localize.file_type}: {self.reapers_table['file_type'][keys[0]]}")

                            self.proc = self.get_reaper(self.reapers_table['class_path'][keys[0]])
                            self.proc.script_name = self.reapers_table['script'][keys[0]]
                        else:
                            self.proc = {}

                            for k in keys:
                                self.proc[self.reapers_table['file_type'][k]] = [
                                    self.get_reaper(self.reapers_table['class_path'][k]),
                                    self.reapers_table['script'][k]
                                ]

                if self.proc is not None:
                    without_pb = ('_Innosetup', '_CelTop', '_Total', '_GAUP', '_SAU', '_VGM', '_7ZIP', '_Wii_iso', '_XISO', '_PS3_PKG', '_PS3_PSARC')

                    try:
                        maximum = 0 if ('other_prg' in str(self.proc)
                                        # or 'seven' in str(self.proc))
                                        or self.func_name in without_pb
                                        or (self.proc.script_name is not None
                                            and 'wcx' in self.proc.script_name)) else 100
                    except AttributeError:
                        maximum = 100

                    ic(self.proc, maximum)

                    if 'splitter' in str(self.proc):
                        param = self.proc.script_name.split(', ')
                        self.proc.start_data = int(param[0])
                        self.proc.header = int(param[1]).to_bytes(4, byteorder='little')
                        self.proc.splitter = int(param[2]).to_bytes(4, byteorder='little')
                        self.proc.file_type = param[3]
                        self.proc.ext = param[4]

                    if isinstance(self.proc, dict):
                        tp = file_type_selector.TypeSelector(self.proc)
                        tp.exec()
                        ic(tp.returned_data)
                        
                        if tp.returned_data is not None:
                            proc_list = self.proc
                            self.proc = proc_list[tp.returned_data][0]
                            self.proc.script_name = proc_list[tp.returned_data][1]
                            self.q_connect(self.proc, fn, header=f'{localize.unpacking}: {fn}...', maximum=maximum)

                    else:
                        self.q_connect(self.proc, fn, header=f'{localize.unpacking}: {fn}...', maximum=maximum)
