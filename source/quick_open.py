import os.path

from PyQt6.QtWidgets import QInputDialog
from icecream import ic
from source.qprocess import QProcessList
from source.ui import localize
from source.reapers import *


class QuickOpen(QProcessList):

    @staticmethod
    def sorry():  # 😢

        # TODO: Нужно локализовать текст!!!
        print('Не удалось найти распаковщик автоматически!\n'
              'Попробуйте выбрать игру или тип файла вручную!')

    def find_reaper(self):

        if self.file_list:
            fn = self.file_list.pop(0)
            ic(fn)

            if os.path.exists(fn):
                self.proc = None

                with open(fn, 'rb') as fff:
                    magic = fff.read(4)
                    magic2 = fff.read(4)
                    magic3 = fff.read(4)

                ext = fn.split('.')[-1].lower()

                # Check on ZIP signature
                if magic == b'PK\x03\x04':
                    self.proc = zip_archive.Zip()

                elif ext == "aes":
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\coalescedaes.bms"

                elif ext == "afs":

                    if magic == b'AFS\00':
                        self.proc = afs.AFSExtractor()
                    else:
                        self.sorry()

                # Check on UnArk support archive
                elif ext in ("alz", "egg", "bh",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = 'data\\wcx\\UnArkWCX.wcx'

                elif ext in ("ara",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\batmanara.bms"

                elif ext == "arc":
                    # TODO: The Incredible Hulk (2008)

                    if magic == b'ARC\x00':  # MT Framework
                        # self.proc = qbms.Q_BMS()
                        # self.proc.script_name = "data\\scripts\\dmc4.bms"
                        self.proc = mt_arc.ARCExtractor()
                    else:
                        self.sorry()

                elif ext in ("arcv",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\3dsarcv.bms"

                elif ext in ("arch06",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\shadowofmordor.bms"

                elif ext == "ark":
                    # TODO: Add ARK, FreeARK archive and other

                    if magic == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("arz",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\ironlorearz.bms"

                # Check on Asura Engine game
                elif ext in ("asr",):
                    print('TODO: Work in progress...')

                # Check on Unity Engine game
                elif ext in ("assets", 'resS'):
                    self.proc = unity.Unity()

                elif ext in ("atd",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\ATD.bms"

                elif ext in ("atg", "rcf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\atgcorecement.bms"

                elif ext in ("azp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\CloseCombat4AZP.bms"

                elif ext in ("bcc",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\bccpsp.bms"

                # Check on Dark Souls Engine game
                elif ext in ("bdt", "bhd5",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\darksoul.bms"

                elif ext in ("bf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\BF.bms"

                elif ext in ("bfg",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\bigfishgames81.bms"

                elif ext in ("bfl",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\ColinMcRaeRallyBFL.bms"

                elif ext in ("bfp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\BFP.bms"

                elif ext in ("bif", "key"):
                    self.proc = aurora_bif_key.BifKey()

                elif ext in ("big",):
                    # TODO: Lost: Via Domus, add from GAUP

                    if magic == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("bin",):
                    # TODO: Kyou Kara Maou - Hajimari no Tabi, Bratz, F1 2015, Mr. Driller G, from Remedy games,
                    #  Fatal Frame\Project Zero, BIN disk image (7zip), BIN archive (?)

                    if magic == b'\x01\x00\x00\x00':  # Alan Wake Remastered
                        pass
                    elif magic == b'\x00\x09\x00\x00':  # Control
                        pass
                    else:
                        self.sorry()

                elif ext in ("bkf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\bitsquidstreams.bms"

                elif ext in ("blz",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = ""
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "blzpack.exe"

                elif ext in ("bmb",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\privatedancerbmb.bms"

                # Check on Wwise Audio
                elif ext in ("bnk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\wwisebnk.bms"

                elif ext in ("box",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\BOXLEMBOX.bms"

                elif ext == "bundle":
                    # TODO: Red Engine (The Witcher 3), PayDay 2, Bionic Commando

                    if magic == b'POTA':  # The Witcher 3
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = "data\\scripts\\Witcher3.bms"
                    else:
                        self.sorry()

                elif ext in ("car",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\CAR.bms"

                elif ext in ("cat",):
                    # TODO: Add from GAUP and other

                    if magic == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("cfs",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\c9.bms"

                elif ext in ("cgr",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\criticaldamage.bms"

                # Check on Java class file
                elif ext in ("class",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "\\data\\wcx\\JavaClassUnpacker.wcx"

                elif ext in ("cmp",):  # TODO: Add from GAUP
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = "/u"
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "ddcmpa.exe"

                elif ext in ("cnt",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\CNTHiddenAndDangerous.bms"

                elif ext == "coalesced":
                    # TODO: coalesced from various Unreal Engine 3 games

                    if magic == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("cpr",):  # TODO: Add from GAUP
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\coyoteconsole.bms"

                elif ext in ("cps",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\kofxiiicps.bms"

                elif ext in ("csa",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\CSAGEEK.bms"

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
                    self.proc.script_name = "data\\scripts\\3dsarcv.bms"

                elif ext in ("cxt",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\CXTXFIR.bms"

                elif ext in ("cub",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\enigmatis.bms"

                elif ext in ("dag",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\DAGPKR3.bms"

                elif ext == "dat":
                    # TODO: A Engine, Learning Company Games, Moto Racer 3, Dirt 5

                    if magic == b'GCAX':  # GCA Archive
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = "data\\wcx\\gca.wcx"
                    elif magic == b'ADAT':  # Anachronox
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = "data\\scripts\\anachronox.bms"
                    elif magic == b'\x20\x00\x00\x00':  # TLOH
                        # TODO: Try how it's be work in the game TLOH
                        self.proc = sen_book.SenBook()
                    else:
                        self.sorry()

                elif ext in ("data", "mini", "wd2"):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\asphyre.bms"

                # Check on DGC archive
                elif ext in ("dgc", "dgca",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = "e"
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "dgcac.exe"

                elif ext == "dir":
                    # TODO: Add from GAUP and other

                    if magic == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("dfl",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\drivingsimulator.bms"

                elif ext in ("dlz",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\heroesphantasiadlz.bms"

                elif ext in ("dpk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\darkeden.bms"

                elif ext in ("dr",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\DRShowdownLegendsOfWrestling.bms"

                elif ext in ("drg",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\drg2sbg.bms"

                elif ext in ("drs",):  # TODO: Add from GAUP
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\DRS.bms"

                elif ext in ("dv2",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\dv2.bms"

                elif ext in ("dz",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\vector.bms"

                # Check on Aurora Engine game
                elif ext in ("erf", "rim"):
                    self.proc = aurora_engine.ERFUnpacker()

                elif ext in ("epc",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\doctorwho.bms"

                elif ext in ("exo",):
                    print('TODO: Work in progress...')

                elif ext in ("far",):  # TODO: Add from GAUP
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\djherofar.bms"

                elif ext == "fat":
                    # TODO: Add from GAUP, FAT image

                    if magic == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("flx",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\CrusaderNoRemorseFLX.bms"

                elif ext in ("fmf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\eafmf.bms"

                # Check on Scimitar Engine game
                elif ext in ("forge",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\scimitar.bms"

                elif ext in ("frm",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\frmfonts.bms"

                # Check on GCA archive
                elif ext in ("gca",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "\\data\\wcx\\gca.wcx"

                elif ext in ("gob",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\EACricket2004GOB.bms"

                # Check on HA archive
                elif ext in ("ha",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "\\data\\wcx\\HA.wcx"

                elif ext in ("hal",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\HALAPUK.bms"

                elif ext in ("hgpk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\10minspacestrategy.bms"

                elif ext in ("hogg",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\hogg.bms"

                elif ext in ("hpf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\HPFHMG.bms"

                # Check on Hrust archive
                elif ext in ("hrp", "hrip",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "\\data\\wcx\\inhrust.wcx"

                elif ext == "img":
                    # TODO: GTA, Disc Image

                    if magic == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("lfs",):
                    print('TODO: Work in progress...')

                elif ext in ("lgp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\FinalFantasy7LGP.bms"

                elif ext in ("m4b",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\EscapeFromMonkeyIslandM4B.bms"

                elif ext in ("mbx",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\HostileWatersMBX.bms"

                elif ext in ("mfd",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\187rideordie.bms"

                elif ext in ("mnf",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = ""
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "EsoExtractData.exe"

                elif ext in ("mng",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\HostileWatersMNG.bms"

                elif ext in ("mpk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\invizimals.bms"

                elif ext in ("mse",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\3dsmax.bms"

                elif ext in ("orc", "ork"):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = ""
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "orkdec.exe"

                elif ext in ("packed",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\CastlevaniaLOS2.bms"

                elif ext == "pac":
                    # TODO: Add PAC from GAUP and other

                    if magic == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("pack",):  # YZ2 from RE4HD
                    print('TODO: Work in progress...')

                elif ext == 'packmeta':
                    self.sorry()
                    # TODO: Add Control

                elif ext == 'pak':
                    # TODO: Sacred, Necrovision, Painkiller

                    if magic == b'\x37\xBD\x37\x4D':  # 7Ѕ7M, PopCap PAK
                        self.proc = seven_s_seven.Seven()
                    elif magic == b'PACK':

                        if 'data.000.pak' in fn:  # 1242
                            self.proc = qbms.Q_BMS()
                            self.proc.script_name = "data\\scripts\\1242.bms"
                        elif 'azangara' in fn.lower():  # Azangara
                            self.proc = qbms.Q_BMS()
                            self.proc.script_name = "data\\scripts\\azangara.bms"
                        else:  # idTech 1+2
                            magic3 = int.from_bytes(magic3, 'little')

                            if magic3 % 576 != 0:
                                l2 = magic3 % 64
                                version = 1 if l2 == 0 else 2
                            else:
                                version, ok = QInputDialog.getInt(self, 'WARNING', 'Select a version:', min=1, max=2)

                            self.proc = quake_pak.QPAKExtractor(version)

                    elif magic == b'KPKA':  # RE Engine
                        pass
                    elif magic == b'SBPA':  # Arcania: Gothic 4
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = "data\\scripts\\arcania.bms"
                    elif magic == b'PAK ':  # Risen
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = "data\\scripts\\risen.bms"
                    elif magic == b'KCAP':
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = "data\\scripts\\full_mojo.bms"
                    elif magic == b'TONG':
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = "data\\scripts\\tongas.bms"
                    elif magic == b'PAK2':  # Alien: Isolation
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = "data\\scripts\\alien_isolation.bms"
                    elif magic == b'PSCD':
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = "data\\scripts\\sega_classics.bms"

                    elif magic == b'\x00' * 4:

                        with open(fn, 'rb') as test_read:
                            test_read.seek(4)
                            head2 = test_read.read(4)

                        if head2 == b'\x00' * 4:  # Unreal Engine 4
                            self.proc = unreal.Unreal()
                        else:  # Alone in the Dark
                            self.proc = qbms.Q_BMS()
                            self.proc.script_name = "data\\scripts\\alonedark.bms"

                    else:

                        with open(fn, 'rb') as test_read:
                            test_read.seek(int.from_bytes(magic, byteorder='little') + 4)
                            arx = int.from_bytes(test_read.read(4), byteorder='little')

                        if arx in (0x46515641, 0x4149534E):
                            self.proc = arx_fatalis.PakExtractor()
                        else:
                            self.sorry()

                elif ext in ("phyre",):
                    self.proc = phyre.PhyreSave()

                elif ext in ("pig",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\CityofHeroesPIG.bms"

                elif ext in ("pix",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\CloseCombat4PIX.bms"

                elif ext == "pkg":
                    # TODO: Space Rangers, SWAT 4
                    self.proc = sen_pkg.PKGExtractor()

                    # if magic in (b'\0' * 4, b'\x00\x00\x81\x60', b'\xB1\x83\x81\x60'):
                    #     self.proc = sen_pkg.PKGExtractor()
                    # else:
                    #     self.sorry()

                elif ext in ("pwf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\DeltaForceLandwarriorPWF.bms"

                elif ext in ("rfa",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\battlefield2moderncombat.bms"

                elif ext in ("rkv",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\rkv.bms"

                elif ext == 'rmdp':
                    # TODO: Add Remedy games support
                    self.sorry()

                # Check on RenPy Engine game
                elif ext in ("rpa",):
                    self.sorry()

                elif ext in ("rpf", ):
                    self.proc = rdr2_audio.RDR2Audio()

                elif ext in ("rpack", ):

                    if magic == b'RP6L':
                        self.proc = chrome_engine.RP6L()
                    else:
                        # TODO: Add functions to unpack other file types
                        print(f'{localize.work_in_progress}...')

                elif ext in ("rpkg",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\hitman2016.bms"

                elif ext in ("rsr",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\ImperialismIIRSR.bms"

                elif ext in ("rzb",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\blur2rzb.bms"

                elif ext in ("sab",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\justcause2sab.bms"

                elif ext in ("scs",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\scsgames.bms"

                elif ext in ("sh",):  # TODO: Add functions to unpack other file types
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\install4j.bms"

                elif ext in ("shd",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\janeangel2.bms"

                elif ext in ("sngw",):  # MT Framework Audio
                    print('TODO: Work in progress...')

                elif ext in ("snd",):  # TODO: Add Daggerfall SND, SND from GAUP
                    print('TODO: Work in progress...')

                elif ext in ("spf",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\jeannedarc.bms"

                elif ext in ("ssp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\jasonstormspace.bms"

                elif ext in ("stk", "itk",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\goblins.bms"

                # Check on ShockWave Flash game
                elif ext in ("swf",):
                    print('TODO: Work in progress...')

                elif ext in ("tab",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = 'data\\scripts\\madmax.bms'

                elif ext in ("tiger",):  # TODO: Add something else
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = "e"
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "gibbed/Gibbed.TombRaider9.Unpack.exe"

                elif ext in ("toc", "sb"):
                    print('TODO: Work in progress...')

                elif ext in ("txt",):
                    # TODO: Lumia Saga, Simple text

                    if magic == b'':
                        pass
                    else:
                        self.sorry()

                # Check on Unigene Engine game
                elif ext in ("ung",):
                    print('TODO: Work in progress...')

                # For video format don't contained audio
                elif ext in ("usm", ):
                    self.proc = ffmpeg_tool.Converter()
                    self.proc.map = '0'

                elif ext in ("vce",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\HomeworldCataclysmVCE.bms"

                elif ext in ("vfs",):
                    self.proc = pathologic.MorUnpacker()

                elif ext in ("voc",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\Lemmings2(VOC)VOC.bms"

                elif ext in ("vpk", ):
                    self.proc = source_vpk.VPKExtractor()

                # Check on RED Engine game
                elif ext in ("w3strings", "w3speech", "archive", "w2strings", "dzip"):
                    print('TODO: Work in progress...')

                elif ext in ("wfp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\bloodyroar3wfp.bms"

                elif ext in ("wrs",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\gamestudio.bms"

                elif ext in ("xbp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\blitzgamesxbp.bms"

                elif ext in ("xcd",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\darknessxcd.bms"

                elif ext in ("xma",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\xma2wav.bms"

                elif ext in ("xnb",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\xnb.bms"

                elif ext == "xxx":
                    self.proc = unreal.Unreal()

                elif ext in ("yz1", ):
                    print('TODO: Work in progress...')

                elif ext in ("yz2", ):
                    print('TODO: Work in progress...')

                elif ext in ("z",):
                    # TODO: Z Archive, LEGO Chess

                    if magic == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("zfs",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\CallToPower2ZFS.bms"

                elif ext in ("zpl",):
                    self.proc = zpl2png.ZPL2PNG()

                elif ext in ("zwp",):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = "data\\scripts\\DarkReign2ZWP.bms"

                # Check on Bethesda game
                elif ext == 'ba2':
                    self.proc = ba2_archives.BethesdaArchive()
                elif ext == 'bsa':
                    if magic == b'BSA\0':
                        self.proc = bsa_archives.BethesdaArchive()
                    else:
                        self.proc = qbms.Q_BMS()
                        self.proc.script_name = 'data\\wcx\\gaup_pro.wcx'
                elif ext in ('esl', 'esm', 'esp', 'esx', 'pex'):
                    # TODO: Add functions to unpack other file types
                    print(f'{localize.work_in_progress}...')

                # Check on extension in GAUP list
                elif ext in ('arch00', 'arch01', 'arch02', 'arch03', 'arch04', 'arch05', 'a2c', 'abg', 'abl', 'acm',
                             'act', 'adf', 'age3scn', 'agg', 'ahm', 'al4', 'al8', 'ama', 'anm', 'avix', 'awd', 'bag',
                             'bank1sbk', 'bar', 'bbk', 'bf', 'bfs', 'bgx', 'bpa', 'bpk', 'bun', 'ceg', 'clz', 'cmo',
                             'cob', 'ctm', 'cts', 'cud', 'dbc', 'dbs', 'ddt', 'dirinfo', 'dta', 'dua', 'dun', 'dx1',
                             'dx2', 'dx3', 'ebm', 'editordata', 'elmares', 'emi', 'exp', 'ezd', 'ff', 'fpk', 'fra',
                             'frame', 'fsh', 'fuk', 'gdp', 'gea', 'gfx', 'glb', 'grl', 'grp', 'gsc', 'gtr', 'h2o',
                             'h4c', 'h4d', 'h4r', 'hak', 'his', 'hog', 'idx', 'ifx', 'ins', 'iwi', 'jap', 'jaz', 'jdr',
                             'jsr', 'jtr', 'lbx', 'lgr', 'lgt', 'lmp', 'lod', 'lte', 'lud', 'lug', 'lut', 'lzc', 'map',
                             'md5', 'mdl', 'meg', 'mix', 'mjp', 'mjz', 'mod', 'msf', 'msk', 'mult', 'mus', 'nif', 'nmo',
                             'npk', 'pal', 'paq', 'pbd', 'pbo', 'pck', 'pcx', 'pff', 'poa', 'pod', 'prm', 'psk', 'psp',
                             'ptx', 'pvd', 'qar', 'qfs', 'r16', 'r24', 'r8', 'raw', 'res', 'rez', 'rfd', 'rfh', 'rmp',
                             'rr', 'rs', 'rsb', 'rss', 'rts', 's4m', 'sbf', 'sc3', 'sct', 'scx', 'sdf', 'sdt',
                             'sequence', 'sga', 'sh4', 'sks', 'sl', 'slf', 'slv', 'spa', 'spk', 'spr', 'st3', 'stb',
                             'stg', 'str', 'sud', 'sue', 'swa', 'syb', 'syj', 't24', 'tbf', 'tdu', 'ted', 'tf', 'thu',
                             'trc', 'twd', 'twt', 'txd', 'ucx', 'uka', 'ukx', 'vdu', 'vid', 'viv', 'vmp', 'vol', 'vpp',
                             'vtf', 'wd', 'wdt', 'wep', 'whd', 'wtn', 'xcr', 'xfs', 'xmb', 'xpk', 'xti', 'xwb'):
                    # TODO: Check NIF from here and maybe add NIF model from other game, check PAL, check PCK,
                    #  check RAW, check RES, check REZ, check VID and maybe add selector for video and VID from  here
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = 'data\\wcx\\gaup_pro.wcx'

                # Check on idTech Engine game
                elif ext in ('bimage', 'idwav', 'index', 'mega2', 'msf', 'pages', 'ptr', 'resources', 'streamed',
                             'vmtr', 'wad', 'wl6', 'xpr'):
                    # TODO: WAD move out, check MSF from GAUP and here

                    if ext == 'wad':
                        self.proc = doom_wad.WadExtractor()
                    else:
                        # TODO: Add functions to unpack other file types
                        print(f'{localize.work_in_progress}...')

                # Check on RPG Maker game
                elif ext in ('rgss2a', 'rgss3a', 'rgssad', 'rpgmvm', 'rpgmvo', 'rpgmvp'):
                    print('TODO: Work in progress...')

                # Check on extension in Total Observer list
                elif ext in ('s2ma', 'sc2', 'bsp', 'cache', 'etc', 'gcf', 'hdr', 'mim', 'mime', 'mpq', 'mpqe', 'msm',
                             'pbb', 'pst', 'udf', 'vbsp', 'vp', 'xzp'):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = 'data\\wcx\\TotalObserver.wcx'

                # Check on extension in SAU list
                elif ext in ('4pp', 'bdx', 'box', 'brig', 'c', 'cam', 'cc', 'chr', 'dbi', 'df2', 'epf', 'fan', 'flx',
                             'gor', 'group', 'hrs', 'ilb', 'jun', 'jus', 'key', 'lbx', 'maa', 'mul', 'nds', 'p00',
                             'p10', 'p99', 'rm', 'tgw', 'tlb', 'uop', 'vsr', 'war', 'wdb', 'xua', 'xub'):
                    # TODO: Check LBX from GAUP and SAU, check BOX, FLX, KEY
                    print('TODO: Work in progress...')

                # Check on archives
                elif ext in ('7z', 'rar', '001', 'cab', 'iso', 'xz', 'lzma', 'tar', 'cpio', 'bz2', 'bzip2', 'tbz',
                             'tbz2', 'gz', 'gzip', 'tgz', 'tpz', 'taz', 'lzh', 'lha', 'rpm', 'deb', 'arj', 'vhd',
                             'vhdx', 'wim', 'swm', 'esd', 'ntfs', 'dmg', 'hfs', 'xar', 'squashfs', 'apfs', 'doc',
                             'xls', 'mgs', 'tnef', 'dbx', 'mbx', 'mbox', 'tbb', 'pmm', 'emlx', 'eml', 'nws', 'mht',
                             'mhtml', 'b64', 'uue', 'xxe', 'ntx', 'hqx', 'warc', 'ccd', 'cdi', 'chd',
                             'ciso', 'cso', 'cue', 'ecm', 'gdi', 'isz', 'mds', 'mdf', 'nrg', 'zisofs', 'asar', 'phar',
                             's01', 'e01', 'ex01', 'lo1', 'lx01', 'aff', 'ad1', 'whx', 'exfat', 'lz', 'rar5', 'txz'):
                    # TODO: Check MBX here and upper, check PMM from video and here, check TXZ
                    self.proc = seven_zip.SevenZIP()

                # Check on video formats
                elif ext in ('3g2', '3gp', '3gp2', '3gpp', 'amv', 'avi', 'divx', 'dvr-ms', 'f4v', 'flc', 'fli', 'flic',
                             'flv', 'm1v', 'm2v', 'm4v', 'mk3d', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'mve', 'ogm',
                             'ogv', 'pam', 'pmf', 'pmm', 'pss', 'rm', 'thp', 'ts', 'vid', 'vob', 'webm', 'wmv', 'xvid'):
                    self.proc = ffmpeg_tool.Converter()

                # Check on Unreal Engine game
                elif ext in ('pcc', 'u', 'uax', 'ugx', 'umx', 'un2', 'unr', 'upk', 'upx', 'usa', 'usx', 'ut2', 'utx',
                             'uvx', 'xxx'):
                    self.proc = unreal.Unreal()

                # Check on X-Ray Engine game
                elif ext in ('db0', 'db1', 'db2', 'db3', 'db4', 'db5', 'db6', 'db7', 'db8', 'db9'):
                    self.proc = qbms.Q_BMS()
                    self.proc.script_name = 'data\\wcx\\stalker.wcx'

                else:
                    self.sorry()
                
                if self.proc is not None:
                    result = self.q_connect(self.proc, fn, header=f'{localize.unpacking}: {fn}...')

                    if result == 7:
                        self.proc = seven_zip.SevenZIP()
                        self.q_connect(self.proc, fn, header=f'{localize.unpacking}: {fn}...')

