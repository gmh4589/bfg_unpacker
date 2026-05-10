import os
from icecream import ic

from source.qprocess import QProcessList
from source.ui import localize
from source.ui.file_type_selector import TypeSelector
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

    def find_reaper(self, func_name=None, script_name=None, maximum=100):
        factory = ReapersFactory(self.reapers_table, func_name, script_name)
        ic(func_name, script_name)
        
        if self.file_list:
            fn = self.file_list.pop(0)
            subfolder = bool(int(self.setting['Main']['subfolders']))
            fp = f'{self.out_dir}\\{os.path.basename(fn).replace(".", "_")}' if subfolder else self.out_dir

            if len(self.file_list) == 0:
                self.last_run = None
            
            if func_name is None:
                reaper_result = factory.find_reaper(fn, fp) 
            else: 
                reaper_result = factory.get_class(func_name)

                try:
                    reaper_result.script_name = script_name
                    ic(type(reaper_result), reaper_result.__dict__)
                    
                    self.q_connect(nuke=reaper_result, fn=fn,
                                header=f'{localize.unpacking}: {fn}...',
                                maximum=maximum,
                                out_dir=self.setting['Main']['out_path'],
                                subfolder=bool(int(self.setting['Main']['subfolders'])))
                    return
                
                except (AttributeError, IndexError):
                    # TODO: Translate text below
                    msg = f"Can't get function {func_name} or script {script_name}. Maybe error in database...\n We will try to detect file type automatly..."
                    ic(msg)
                    print(msg)
                    reaper_result = factory.find_reaper(fn, fp)

            ic(reaper_result)

            if reaper_result:

                if len(reaper_result) > 1:
                    tp = TypeSelector(reaper_result)
                    tp.exec()
                    ic(tp.returned_data)
                    
                    if tp.returned_data is not None:
                        proc_list = reaper_result
                        reaper_result = {
                            tp.returned_data: [
                                proc_list[tp.returned_data][0], 
                                proc_list[tp.returned_data][1],
                                proc_list[tp.returned_data][2]
                            ]
                        }

                    else:
                        self.sorry()

                ic(reaper_result)
                proc_list = list(reaper_result.values())[0]
                print(f"{localize.file_type} {list(reaper_result.keys())[0]}")

                function = proc_list[0]
                function.script_name = proc_list[1]
                maximum = proc_list[2].item()
                ic(type(function), function.__dict__)

                self.q_connect(function, fn,
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
