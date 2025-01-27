import os
from time import sleep

from icecream import ic

from source import reapers
from source.qprocess import QProcessList
from source.ui import localize
from source.reapers import *


class QuickOpen(QProcessList):

    @staticmethod
    def sorry():  # 😢

        # TODO: Нужно локализовать текст!!!
        print('Не удалось найти распаковщик автоматически!\n'
              'Попробуйте выбрать игру или тип файла вручную!')
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
            ic(fn)

            if os.path.exists(fn):
                self.proc = None

                try:

                    with open(fn, 'rb') as fff:
                        magic1, magic2, magic3 = fff.read(4), fff.read(4), fff.read(4)

                except (PermissionError, FileNotFoundError, FileExistsError):
                    magic1, magic2, magic3 = b'', b'', b''

                name_split = os.path.basename(fn).lower().split('.')
                ext = name_split.pop(-1)
                name = '.'.join(name_split)
                ic(name, ext)
                # TODO: big Lost: Via Domus, add from GAUP
                # TODO: Other prg
                # TODO: bundle Red Engine (The Witcher 3), PayDay 2, Bionic Commando
                # TODO: bin Kyou Kara Maou - Hajimari no Tabi, Bratz, F1 2015, Mr. Driller G,
                #  Fatal Frame\Project Zero, BIN disk image (7zip), BIN archive (?)
                # TODO: Add *.cache from total observer
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
                # TODO pack YZ2 from RE4HD
                # TODO: pak Sacred, Necrovision, Painkiller
                # TODO: pak idTech2 (QUAKE)
                # TODO: pak ReEngine file list
                # TODO: pak Arx Fatalis and Prey
                # TODO: rpack
                # TODO: add rpa RenPy Engine game
                # TODO: sh Add functions to unpack other file types
                # TODO: Add support for Sin
                # TODO: SND from GAUP
                # TODO: Add function to replace extension
                # TODO: Add Frosbite Engine Support
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

                elif self.func_name == '_QuickBMS':
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = self.script_name

                elif self.func_name == '_Unity':
                    self.proc = unity.Unity()

                elif self.func_name == '_Innosetup':
                    self.proc = other_prg.OtherProg(
                        program_name='tools\\innounp.exe',
                        first_arg=f' -x -d"{fp if subfolder else self.out_dir}"',
                        percent_type='random',
                        run_type='command_line')

                elif self.func_name == '_CelTop':
                    self.proc = cel_top.CelTop()

                elif self.func_name == '_Total':
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = 'data\\wcx\\TotalObserver.wcx'

                elif self.func_name == '_GAUP':
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = 'data\\wcx\\gaup_pro.wcx'

                elif self.func_name == '_SAU':
                    self.proc = other_prg.OtherProg(
                        program_name='tools\\sau.exe',
                        first_arg='./',
                        second_arg=f' "{fp if subfolder else self.out_dir}"')

                elif self.func_name == '_VGM' or ext in ('bnk', 'fsb', 'at3', 'at9', 'vag', 'wem', 'wav', 'lwav',
                                                         'adpcm', 'ss2', 'pcm', 'aud', 'ogg', 'logg', 'sngw', 'ogg_',
                                                         'bgm', 'aif', 'laif', 'aiff', 'laiff', 'aifc', 'laifc', 'afc',
                                                         'xwb', 'xna', 'opus', 'lopus', 'ue4opus', 'xwma', 'xwm', 'wav',
                                                         'xma', 'wma', 'lwma', 'xopus', '9tav'):
                    sleep(1)
                    self.proc = other_prg.OtherProg(
                        program_name='vgmstream\\vgmstream-cli.exe',
                        first_arg=f'-o "{fp if subfolder else self.out_dir}\\'
                                  f'{os.path.basename(fn).replace(ext, "wav")}"',
                        percent_type='not')

                elif self.func_name == '_7ZIP':
                    self.proc = seven_zip.SevenZIP()

                elif self.func_name == '_REEngine':
                    self.proc = re_engine.ReEngine()
                    self.proc.game_file_list = self.script_name

                elif self.func_name == '_Unreal':
                    self.proc = unreal.Unreal()

                elif self.func_name == '_Unreal4':
                    self.proc = unreal.Unreal()
                    self.proc.key = self.script_name

                else:
                    lst = list(self.reapers_table['ext'])
                    keys = [e for e in range(len(lst)) if lst[e] == ext]

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

                        for k in keys:

                            for c, v in check_list.items():

                                if self.reapers_table[c][k] == v:
                                    weights[keys.index(k)] += 1
                                elif self.reapers_table[c][k] == '*' or self.reapers_table[c][k] == -1:
                                    pass
                                else:
                                    weights[keys.index(k)] -= 1

                        weights = dict(zip(keys, weights))
                        max_value = max(weights.values())
                        weights = {key: [value, self.reapers_table['class_path'][key]] for key, value in weights.items() if value == max_value}
                        keys = list(weights.keys())
                        ic(weights, keys)

                        if len(weights) == 1:
                            self.proc = self.get_reaper(self.reapers_table['class_path'][keys[0]])
                            self.proc.script_name = self.reapers_table['script'][keys[0]]
                        else:
                            self.proc = []

                            for k in keys:
                                self.proc.append(self.get_reaper(self.reapers_table['class_path'][k]))
                                self.proc[-1].script_name = self.reapers_table['script'][k]

                if self.proc is not None:

                    def proc(prc):
                        result = self.q_connect(prc, fn, header=f'{localize.unpacking}: {fn}...')

                        if result == 7:
                            self.proc = seven_zip.SevenZIP()
                            self.q_connect(prc, fn, header=f'{localize.unpacking}: {fn}...')

                    if isinstance(self.proc, list):

                        for p in self.proc:
                            proc(p)

                    else:
                        proc(self.proc)
