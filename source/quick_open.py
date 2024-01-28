import os.path

from icecream import ic
from source.reaper import after_dot2
from source.qprocess import QProcessList
from source.ui import localize

from source.reapers import (afs, arx_fatalis, aurora_engine, celestia, chrome_engine, doom_wad, ffmpeg_tool, locres,
                            mt_arc, other_prg, pathologic, phyre, qbms, quake_pak, rdr2_audio, sen_book, seven_s_seven,
                            seven_zip, source_vpk, unity, unreal, zip_archive, zpl2png)


class QuickOpen(QProcessList):

    @staticmethod
    def sorry():  # 😢
        print('Не удалось найти распаковщик автоматически!\n'
              'Попробуйте выбрать игру или тип файла вручную!')

    def find_reaper(self):

        if self.file_list:
            fn = self.file_list.pop(0)
            ic(fn)

            if os.path.exists(fn):
                self.proc = None

                with open(fn, 'rb') as fff:
                    self.head = fff.read(4)

                ext = fn.split('.')[-1].lower()

                # Check on ZIP signature
                if self.head == b'PK\x03\x04':
                    self.proc = zip_archive.Zip()

                # Check on Bethesda game
                elif ext in after_dot2['bethesda']:
                    # TODO: Add functions to unpack other file types
                    print(f'{localize.work_in_progress}...')

                # Check on extension in GAUP list
                elif ext in after_dot2['gaup']:
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f'{self.root_dir}/data/wcx/gauppro.wcx'

                # Check on idTech Engine game
                elif ext in after_dot2['id_tech']:

                    if ext == 'wad':
                        self.proc = doom_wad.WadExtractor()
                    elif ext == 'pak':
                        self.proc = quake_pak.QPAKExtractor()
                    else:
                        # TODO: Add functions to unpack other file types
                        print(f'{localize.work_in_progress}...')

                # Check on RPG Maker game
                elif ext in after_dot2['rpg_maker']:
                    print('TODO: Work in progress...')

                # Check on extension in Total Observer list
                elif ext in after_dot2['total_observer']:
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f'{self.root_dir}/data/wcx/TotalObserver.wcx'

                # Check on extension in SAU list
                elif ext in after_dot2['sau']:
                    print('TODO: Work in progress...')

                # Check on archives
                elif ext in after_dot2['seven_zip']:
                    self.proc = seven_zip.SevenZIP()

                # Check on video formats
                elif ext in after_dot2['video']:
                    self.proc = ffmpeg_tool.Converter()

                # Check on Unreal Engine game
                elif ext in after_dot2['unreal']:
                    self.proc = unreal.Unreal()

                # Check on X-Ray Engine game
                elif ext in after_dot2['x-ray']:
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f'{self.root_dir}/data/wcx/stalker.wcx'

                elif ext == "aes":
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/coalescedaes.bms"

                elif ext == "afs":

                    if self.head == b'AFS\00':
                        self.proc = afs.AFSExtractor()
                    else:
                        self.sorry()

                # Check on UnArk support archive
                elif ext in ("alz", "egg", "bh",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f'{self.root_dir}/data/wcx/UnArkWCX.wcx'

                elif ext in ("ara",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/batmanara.bms"

                elif ext == "arc":
                    # TODO: The Incredible Hulk (2008)

                    if self.head == b'ARC\x00':  # MT Framework
                        # self.proc = qbms.Q_BMS()
                        # self.proc.script_name = f"{self.root_dir}/data/scripts/dmc4.bms"
                        self.proc = mt_arc.ARCExtractor()
                    else:
                        self.sorry()

                elif ext in ("arcv",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/3dsarcv.bms"

                elif ext in ("arch06",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/shadowofmordor.bms"

                elif ext in ("arz",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/ironlorearz.bms"

                # Check on Asura Engine game
                elif ext in ("asr",):
                    print('TODO: Work in progress...')

                # Check on Unity Engine game
                elif ext in ("assets", 'resS'):
                    self.proc = unity.Unity()

                elif ext in ("atd",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/ATD.bms"

                elif ext in ("atg", "rcf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/atgcorecement.bms"

                elif ext in ("azp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/CloseCombat4AZP.bms"

                elif ext in ("bcc",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/bccpsp.bms"

                # Check on Dark Souls Engine game
                elif ext in ("bdt", "bhd5",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/darksoul.bms"

                elif ext in ("bf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/BF.bms"

                elif ext in ("bfg",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/bigfishgames81.bms"

                elif ext in ("bfl",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/ColinMcRaeRallyBFL.bms"

                elif ext in ("bfp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/BFP.bms"

                elif ext in ("bif", "key"):
                    # TODO: Add inner reaper
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = '/data/scripts/BIF_BIFFV1.bms'

                elif ext in ("big",):
                    # TODO: Lost: Via Domus

                    if self.head == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("bin",):
                    # TODO: Kyou Kara Maou - Hajimari no Tabi, Bratz, F1 2015, Mr. Driller G,
                    #  Fatal Frame\Project Zero

                    if self.head == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("bkf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/bitsquidstreams.bms"

                elif ext in ("blz",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = ""
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "blzpack.exe"

                elif ext in ("bmb",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/privatedancerbmb.bms"

                # Check on Wwise Audio
                elif ext in ("bnk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/wwisebnk.bms"

                elif ext in ("box",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/BOXLEMBOX.bms"

                elif ext == "bundle":
                    # TODO: Red Engine, Pay Day

                    if self.head == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("car",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/CAR.bms"

                elif ext in ("cfs",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/c9.bms"

                elif ext in ("cgr",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/criticaldamage.bms"

                # Check on Java class file
                elif ext in ("class",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/wcx/JavaClassUnpacker.wcx"

                elif ext in ("cmp",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = "/u"
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "ddcmpa.exe"

                elif ext in ("cnt",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/CNTHiddenAndDangerous.bms"

                elif ext in ("cpr",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/coyoteconsole.bms"

                elif ext in ("cps",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/kofxiiicps.bms"

                elif ext in ("csa",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/CSAGEEK.bms"

                # Check on Chrome Engine game
                elif ext in ("csb", "spb"):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = 'data/scripts/dying_light.bms'

                elif ext in ("csc",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = ""
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "scsextractor.exe"

                elif ext in ("ctpk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/3dsarcv.bms"

                elif ext in ("cxt",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/CXTXFIR.bms"

                elif ext in ("cub",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/enigmatis.bms"

                elif ext in ("dag",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/DAGPKR3.bms"

                elif ext == "dat":
                    # TODO: A Engine, Learning Company Games, Moto Racer 3, Dirt 5

                    if self.head == b'GCAX':  # GCA Archive
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = f"{self.root_dir}/data/wcx/gca.wcx"
                    elif self.head == b'ADAT':  # Anachronox
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = f"{self.root_dir}/data/scripts/anachronox.bms"
                    else:
                        self.sorry()

                elif ext in ("data", "mini", "wd2"):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/asphyre.bms"

                # Check on DGC archive
                elif ext in ("dgc", "dgca",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = "e"
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "dgcac.exe"

                elif ext in ("dfl",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/drivingsimulator.bms"

                elif ext in ("dlz",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/heroesphantasiadlz.bms"

                elif ext in ("dpk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/darkeden.bms"

                elif ext in ("dr",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/DRShowdownLegendsOfWrestling.bms"

                elif ext in ("drg",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/drg2sbg.bms"

                elif ext in ("drs",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/DRS.bms"

                elif ext in ("dv2",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/dv2.bms"

                elif ext in ("dz",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/vector.bms"

                # Check on Aurora Engine game
                elif ext in ("erf", "rim"):
                    self.proc = aurora_engine.ERFUnpacker()

                elif ext in ("epc",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/doctorwho.bms"

                elif ext in ("exo",):
                    print('TODO: Work in progress...')

                elif ext in ("far",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/djherofar.bms"

                elif ext in ("flx",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/CrusaderNoRemorseFLX.bms"

                elif ext in ("fmf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/eafmf.bms"

                # Check on Scimitar Engine game
                elif ext in ("forge",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/scimitar.bms"

                elif ext in ("frm",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/frmfonts.bms"

                # Check on GCA archive
                elif ext in ("gca",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/wcx/gca.wcx"

                elif ext in ("gob",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/EACricket2004GOB.bms"

                # Check on HA archive
                elif ext in ("ha",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/wcx/HA.wcx"

                elif ext in ("hal",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/HALAPUK.bms"

                elif ext in ("hgpk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/10minspacestrategy.bms"

                elif ext in ("hogg",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/hogg.bms"

                elif ext in ("hpf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/HPFHMG.bms"

                # Check on Hrust archive
                elif ext in ("hrp", "hrip",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/wcx/inhrust.wcx"

                elif ext == "img":
                    # TODO: GTA, Disc Image

                    if self.head == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("lfs",):
                    print('TODO: Work in progress...')

                elif ext in ("lgp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/FinalFantasy7LGP.bms"

                elif ext in ("m4b",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/EscapeFromMonkeyIslandM4B.bms"

                elif ext in ("mbx",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/HostileWatersMBX.bms"

                elif ext in ("mfd",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/187rideordie.bms"

                elif ext in ("mnf",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = ""
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "EsoExtractData.exe"

                elif ext in ("mng",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/HostileWatersMNG.bms"

                elif ext in ("mpk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/invizimals.bms"

                elif ext in ("mse",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/3dsmax.bms"

                elif ext in ("orc", "ork"):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = ""
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "orkdec.exe"

                elif ext in ("packed",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/CastlevaniaLOS2.bms"

                elif ext in ("pack",):  # YZ2 from RE4HD
                    print('TODO: Work in progress...')

                elif ext == 'pak':
                    # TODO: Arx Fatalis, Sacred, Necrovision, Painkiller

                    if self.head == b'\x37\xBD\x37\x4D':  # 7Ѕ7M, PopCap PAK
                        self.proc = seven_s_seven.Seven()
                    elif self.head == b'PACK':

                        if 'data.000.pak' in fn:  # 1242
                            self.proc = qbms.Q_BMS()
                            self.proc.script_name = f"{self.root_dir}/data/scripts/1242.bms"
                        elif 'azangara' in fn.lower():  # Azangara
                            self.proc = qbms.Q_BMS()
                            self.proc.script_name = f"{self.root_dir}/data/scripts/azangara.bms"
                        else:  # idTech 1+2
                            self.proc = quake_pak.QPAKExtractor()

                    elif self.head == b'KPKA':  # RE Engine
                        pass
                    elif self.head == b'SBPA':  # Arcania: Gothic 4
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = f"{self.root_dir}/data/scripts/arcania.bms"
                    elif self.head == b'PAK ':  # Risen
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = f"{self.root_dir}/data/scripts/risen.bms"
                    elif self.head == b'KCAP':
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = f"{self.root_dir}/data/scripts/full_mojo.bms"
                    elif self.head == b'TONG':
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = f"{self.root_dir}/data/scripts/tongas.bms"
                    elif self.head == b'PAK2':
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = f"{self.root_dir}/data/scripts/alien_isolation.bms"
                    elif self.head == b'PSCD':
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = f"{self.root_dir}/data/scripts/sega_classics.bms"

                    elif self.head == b'\x00' * 4:

                        with open(fn, 'rb') as test_read:
                            test_read.seek(4)
                            head2 = test_read.read(4)

                        if head2 == b'\x00' * 4:  # Unreal Engine 4
                            self.proc = unreal.Unreal()
                        else:  # Alone in the Dark
                            self.proc = qbms.Q_BMS()
                            self.proc.script_name = f"{self.root_dir}/data/scripts/alonedark.bms"

                    else:

                        with open(fn, 'rb') as test_read:
                            test_read.seek(int.from_bytes(self.head, byteorder='little') + 4)
                            arx = int.from_bytes(test_read.read(4), byteorder='little')

                        if arx in (0x46515641, 0x4149534E):
                            self.proc = arx_fatalis.PakExtractor()
                        else:
                            self.sorry()

                elif ext in ("phyre",):
                    self.proc = phyre.PhyreSave()

                elif ext in ("pig",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/CityofHeroesPIG.bms"

                elif ext in ("pix",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/CloseCombat4PIX.bms"

                elif ext == "pkg":
                    # TODO: Space Rangers, SWAT 4, Trails of Cold Steel

                    if self.head == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("pwf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/DeltaForceLandwarriorPWF.bms"

                elif ext in ("rfa",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/battlefield2moderncombat.bms"

                elif ext in ("rkv",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/rkv.bms"

                # Check on RenPy Engine game
                elif ext in ("rpa",):
                    self.sorry()

                elif ext in ("rpf", ):
                    self.proc = rdr2_audio.RDR2Audio()

                elif ext in ("rpack", ):

                    if self.head == b'RP6L':
                        self.proc = chrome_engine.RP6L()
                    else:
                        # TODO: Add functions to unpack other file types
                        print(f'{localize.work_in_progress}...')

                elif ext in ("rpkg",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/hitman2016.bms"

                elif ext in ("rsr",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/ImperialismIIRSR.bms"

                elif ext in ("rzb",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/blur2rzb.bms"

                elif ext in ("sab",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/justcause2sab.bms"

                elif ext in ("scs",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/scsgames.bms"

                elif ext in ("sh",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/install4j.bms"

                elif ext in ("shd",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/janeangel2.bms"

                elif ext in ("sngw",):  # MT Framework Audio
                    print('TODO: Work in progress...')

                elif ext in ("spf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/jeannedarc.bms"

                elif ext in ("ssp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/jasonstormspace.bms"

                elif ext in ("stk", "itk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/goblins.bms"

                # Check on ShockWave Flash game
                elif ext in ("swf",):
                    print('TODO: Work in progress...')

                elif ext in ("tab",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f'{self.root_dir}/data/scripts/madmax.bms'

                elif ext in ("tiger",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = "e"
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "gibbed/Gibbed.TombRaider9.Unpack.exe"

                elif ext in ("toc", "sb"):
                    print('TODO: Work in progress...')

                elif ext in ("txt",):
                    # TODO: Lumia Saga, Simple text

                    if self.head == b'':
                        pass
                    else:
                        self.sorry()

                # Check on Unigene Engine game
                elif ext in ("ung",):
                    print('TODO: Work in progress...')

                elif ext in ("vce",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/HomeworldCataclysmVCE.bms"

                elif ext in ("vfs",):
                    self.proc = pathologic.MorUnpacker()

                elif ext in ("voc",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/Lemmings2(VOC)VOC.bms"

                elif ext in ("vpk", ):
                    self.proc = source_vpk.VPKExtractor()

                # Check on RED Engine game
                elif ext in ("w3strings", "w3speech", "archive", "w2strings", "dzip"):
                    print('TODO: Work in progress...')

                elif ext in ("wfp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/bloodyroar3wfp.bms"

                elif ext in ("wrs",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/gamestudio.bms"

                elif ext in ("xbp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/blitzgamesxbp.bms"

                elif ext in ("xcd",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/darknessxcd.bms"

                elif ext in ("xma",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/xma2wav.bms"

                elif ext in ("xnb",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/xnb.bms"

                elif ext in ("yz1", ):
                    print('TODO: Work in progress...')

                elif ext in ("yz2", ):
                    print('TODO: Work in progress...')

                elif ext in ("z",):
                    # TODO: Z Archive, LEGO Chess

                    if self.head == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("zfs",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/CallToPower2ZFS.bms"

                elif ext in ("zpl",):
                    self.proc = zpl2png.ZPL2PNG()

                elif ext in ("zwp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = f"{self.root_dir}/data/scripts/DarkReign2ZWP.bms"

                else:
                    self.sorry()
                
                if self.proc is not None:
                    self.q_connect(self.proc, fn, header=f'{localize.unpacking}: {fn}...')
