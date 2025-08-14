import os
from icecream import ic

from source.qprocess import QProcessList
from source.ui import localize
from source.ui.file_type_selector import TypeSelector
from source import reapers
from source.setting import setting
from source.reapers_factory import ReapersFactory


class QuickOpen(QProcessList):

    def __init__(self):
        super().__init__()
        self.script_name = ''
        self.setting = setting

    @staticmethod
    def sorry(msg=localize.not_find_unpacker):  # 😢
        print(msg)
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
        self.factory = ReapersFactory(self.reapers_table, self.func_name, self.script_name)
        
        if self.file_list:
            fn = self.file_list.pop(0)
            subfolder = bool(int(self.setting['Main']['subfolders']))
            fp = f'{self.out_dir}\\{os.path.basename(fn).replace(".", "_")}' if subfolder else self.out_dir

            if len(self.file_list) == 0:
                self.last_run = None
            
            reaper_result = self.factory.find_reaper(fn, fp)
            ic(reaper_result)

            if reaper_result is not None:
                without_pb = ('_OtherPRG', '_CelTop', '_Total', '_GAUP', '_VGM', '_Wii_iso', '_XISO', '_PS3_PKG', '_PS3_PSARC', '_MediaInfo')

                try:
                    maximum = 0 if ('other_prg' in str(reaper_result) 
                                    or self.func_name in without_pb
                                    or (reaper_result.script_name is not None
                                        and 'wcx' in reaper_result.script_name)) else 100
                except AttributeError:
                    maximum = 100

                ic(maximum, reaper_result)

                if 'splitter' in str(reaper_result):
                    param = reaper_result.script_name.split(', ')
                    reaper_result.start_data = int(param[0])
                    reaper_result.header = int(param[1]).to_bytes(4, byteorder='little')
                    reaper_result.splitter = int(param[2]).to_bytes(4, byteorder='little')
                    reaper_result.file_type = param[3]
                    reaper_result.ext = param[4]

                if isinstance(reaper_result, dict):
                    tp = TypeSelector(reaper_result)
                    tp.exec()
                    ic(tp.returned_data)
                    
                    if tp.returned_data is not None:
                        proc_list = reaper_result
                        reaper_result = proc_list[tp.returned_data][0]
                        reaper_result.script_name = proc_list[tp.returned_data][1]
                        self.q_connect(reaper_result, fn,
                                       header=f'{localize.unpacking}: {fn}...',
                                       maximum=maximum,
                                       out_dir=self.setting['Main']['out_path'],
                                       subfolder=bool(int(self.setting['Main']['subfolders'])))

                else:
                    self.q_connect(reaper_result, fn,
                                   header=f'{localize.unpacking}: {fn}...',
                                   maximum=maximum,
                                   out_dir=self.setting['Main']['out_path'],
                                   subfolder=bool(int(self.setting['Main']['subfolders'])))

            else:
                self.sorry()

            
            # TODO:
            #  big Lost: Via Domus, add from GAUP
            #  Other prg
            #  bundle PayDay 2, Bionic Commando
            #  bin Kyou Kara Maou - Hajimari no Tabi, Bratz, F1 2015, Mr. Driller G,
            #  Fatal Frame\Project Zero, BIN disk image (7zip), BIN archive (?)
            #  cat Add from GAUP and other
            #  coalesced from various Unreal Engine 3 games
            #  dat A Engine, Learning Company Games, Moto Racer 3, Dirt 5
            #  dir Add from GAUP and other
            #  fat Add from GAUP, FAT image
            #  img GTA, Disc Image
            #  lfs
            #  pac Add PAC from GAUP and other
            #  pak Necrovision, Painkiller
            #  pak idTech2 (QUAKE)
            #  pak ReEngine file list
            #  pak Arx Fatalis and Prey
            #  rpack
            #  sh Add functions to unpack other file types
            #  SND from GAUP
            #  Add function to replace extension
            #  Add Frostbite Engine Support
            #  txt Lumia Saga, Simple text
            #  Check on Unigene Engine game
            #  Check on RED Engine game "w3strings", "archive", "w2strings", "dzip"
            #  Add support for Wolfenstein 3D
            #  Add support for YZ2 archives
            #  *.z Z Archive, LEGO Chess
            #  zpl, add change size to converter
            #  Add functions to convert ESM, ESP, ESL, PEX (this is really need?)
            #  Check NIF from here and maybe add NIF model from other game, check PAL, check PCK, MSF
            #  check RAW, check RES, check REZ, check VID and maybe add selector for video and VID from here
            #  wad Add other games
            #  Check on extension in SAU list
            #  Check LBX from GAUP and SAU, check BOX, FLX, KEY
            #  Check MBX here and upper, check PMM from video and here, check TXZ
            #  IDWAV by idTech
            #  Sen Book (TLOH books dat)
            #  Add PCK Unreal 2-3
            #  FOX Engine files (*.dat; *.qar; *.fpk; *.pftxs; *.sbp; *.xml)
            #  try Aurora Engine all games
            #  TESO
            #  try Chrome Engine diferent games
            #  try Cry Engine diferent games
            #  make Space Engine exoplanet catalog generator
            #  try Scimitar Engine diferent games
            #  try Glacier Engine diferent games
            #  try Infinity Engine diferent games
            #  try LithTech Engine diferent games
            #  test MTFramework engine
            #  Add texture support form Ego Engine in DB
            #  add BLZ archive support
            #  add BMA aarchive support
            #  add DGCA archive support
            #  add NanoZip archive support
            #  add Simbion OS installer suppor (A you realy need it?)
            #  add ZOO archive support
            #  add Unigen Engine support
            #  add FPS Creator support
            #  add Gameloft support
            #  add HuneX Engine support
            #  add ShiVa Engine support
            #  add Snowdrop Engine support
            #  add other idTech games support
