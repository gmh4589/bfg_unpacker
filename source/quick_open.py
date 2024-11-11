import os
import shutil
from subprocess import Popen

from PyQt6.QtWidgets import QInputDialog, QComboBox
from icecream import ic
from source.qprocess import QProcessList
from source.ui import localize
from source.reapers import *
from source.codecs.image_tools import KTXConvert
from source.ui.custom_ui import CustomDialog


class QuickOpen(QProcessList):

    @staticmethod
    def sorry():  # 😢

        # TODO: Нужно локализовать текст!!!
        print('Не удалось найти распаковщик автоматически!\n'
              'Попробуйте выбрать игру или тип файла вручную!')
        return None

    def find_reaper(self):

        if self.file_list:
            fn = self.file_list.pop(0)
            subfolder = bool(int(self.setting['Main']['subfolders']))
            fp = f'{self.out_dir}\\{os.path.basename(fn).replace(".", "_")}'
            ic(fn)

            if os.path.exists(fn):
                self.proc = qbms.Q_BMS()

                try:

                    with open(fn, 'rb') as fff:
                        magic, magic2, magic3 = fff.read(4), fff.read(4), fff.read(4)

                except (PermissionError, FileNotFoundError, FileExistsError):
                    magic, magic2, magic3 = b'', b'', b''

                name_split = os.path.basename(fn).lower().split('.')
                ext = name_split.pop(-1)
                name = '.'.join(name_split)
                ic(name, ext)

                # Check on ZIP signature
                if magic == b'PK\x03\x04':
                    self.proc = zip_archive.Zip()

                elif self.func_name == '_QuickBMS':
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
                    self.proc.script_name = 'data\\wcx\\TotalObserver.wcx'

                elif self.func_name == '_GAUP':
                    self.proc.script_name = 'data\\wcx\\gaup_pro.wcx'

                elif self.func_name == '_SAU':
                    self.proc = other_prg.OtherProg(
                        program_name='tools\\sau.exe',
                        first_arg='./',
                        second_arg=f' "{fp if subfolder else self.out_dir}"')

                elif self.func_name == '_VGM' or ext in ('bnk', 'fsb', 'at3', 'at9', 'vag', 'wem', 'wav', 'lwav',
                                                         'adpcm', 'ss2', 'pcm', 'aud', 'ogg', 'logg', 'sngw', 'ogg_',
                                                         'bgm', 'aif', 'laif', 'aiff', 'laiff', 'aifc', 'laifc', 'afc',
                                                         'xwb', 'xna', 'opus', 'lopus', 'ue4opus', 'xwma', 'xwm',
                                                         'xma', 'wma', 'lwma', 'xopus', '9tav'):
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

                elif self.func_name == '_Unreal4':
                    self.proc = unreal.Unreal()
                    self.proc.key = self.script_name

                # A
                elif ext == "ace":
                    self.proc = unace.UnAce()

                elif ext == "aes":
                    self.proc.script_name = "data\\scripts\\coalescedaes.bms"

                elif ext == "afs":
                    self.proc = afs.AFSExtractor()

                # Check on UnArc support archive
                elif ext in ("alz", "egg", "bh", "ark", "g"):
                    self.proc.script_name = 'data\\wcx\\UnArkWCX.wcx'

                elif ext in ("ara",):
                    self.proc.script_name = "data\\scripts\\batmanara.bms"

                elif ext == "arc":
                    # TODO: The Incredible Hulk (2008)

                    if magic == b'ARC\x00':  # MT Framework
                        self.proc = mt_arc.ARCExtractor()
                    elif magic == b'ArC\x01':  # FreeARC Archive
                        self.proc.script_name = "data\\wcx\\UnArkWCX.wcx"
                    else:
                        self.proc = self.sorry()

                elif ext in ("arcv",):
                    self.proc.script_name = "data\\scripts\\3dsarcv.bms"

                elif ext in ("arch06",):
                    self.proc.script_name = "data\\scripts\\shadowofmordor.bms"

                elif ext == "argb":
                    self.proc = argb.ARGB2BMP()

                elif ext in ("art",):
                    self.proc = art.ARTExtractor()

                elif ext in ("arz",):
                    self.proc.script_name = "data\\scripts\\ironlorearz.bms"

                # Check on Asura Engine game
                elif ext in ("asr",):
                    self.proc.script_name = "data\\scripts\\asura.bms"

                # Check on Unity Engine game
                elif ext in ("assets", 'resS'):
                    self.proc = unity.Unity()

                elif ext in ("atd",):
                    self.proc.script_name = "data\\scripts\\ATD.bms"

                elif ext in ("atg", "rcf",):
                    self.proc.script_name = "data\\scripts\\atgcorecement.bms"

                elif ext in ("azp",):
                    self.proc.script_name = "data\\scripts\\CloseCombat4AZP.bms"

                # B
                # Check on Bethesda game
                elif ext == 'ba2':
                    self.proc = ba2_archives.BethesdaArchive()

                elif ext in ("bcc",):
                    self.proc.script_name = "data\\scripts\\bccpsp.bms"

                # Check on Dark Souls Engine game
                elif ext in ("bdt", "bhd5",):
                    self.proc.script_name = "data\\scripts\\darksoul.bms"

                elif ext in ("bf",):
                    self.proc.script_name = "data\\scripts\\BF.bms"

                elif ext in ("bfg",):
                    self.proc.script_name = "data\\scripts\\bigfishgames81.bms"

                elif ext in ("bfl",):
                    self.proc.script_name = "data\\scripts\\ColinMcRaeRallyBFL.bms"

                elif ext in ("bfp",):
                    self.proc.script_name = "data\\scripts\\BFP.bms"

                elif ext in ("bif", "key"):
                    self.proc = infinity_bif_key.BifKey()

                elif ext in ("big",):
                    # TODO: Lost: Via Domus, add from GAUP

                    if magic == b'':
                        pass
                    else:
                        self.proc = self.sorry()

                elif ext == 'bimage':
                    # self.proc.script_name = 'data/scripts/idtech5_bimage_2_dds.bms'
                    self.proc = bimage.Bimage2DDS()

                elif ext in ("bin",):
                    # TODO: Kyou Kara Maou - Hajimari no Tabi, Bratz, F1 2015, Mr. Driller G, from Remedy games,
                    #  Fatal Frame\Project Zero, BIN disk image (7zip), BIN archive (?)

                    if magic in (b'\x01\x00\x00\x00', b'\0' * 4, b'\x00\x09\x00\x00', b'\x01\x09\x00\x00'):
                        self.proc = remedy.Remedy()
                    else:
                        self.proc = self.sorry()

                elif ext in ("bkf",):
                    self.proc.script_name = "data\\scripts\\bitsquidstreams.bms"

                elif ext in ("blz",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = 'd'
                    self.proc.second_arg = '%out_dir%\\%file_name%'
                    self.proc.program_name = 'tools\\blzpack.exe'
                    self.proc.percent_type = 'not'

                elif ext in ("bmb",):
                    self.proc.script_name = "data\\scripts\\privatedancerbmb.bms"

                elif ext in ("box",):
                    self.proc.script_name = "data\\scripts\\BOXLEMBOX.bms"

                elif ext == 'bsa':

                    if magic == b'BSA\0':
                        self.proc = bsa_archives.BethesdaArchive()
                    elif magic == b'\x00\x01\x00\x00':
                        self.proc = morrowind.MorrowindBSA()
                    else:
                        self.proc = arena.OldBSA()
                        # self.proc.script_name = 'data\\wcx\\gaup_pro.wcx'

                elif ext == "bundle":
                    # TODO: Red Engine (The Witcher 3), PayDay 2, Bionic Commando

                    if magic == b'POTA':  # The Witcher 3
                        # self.proc.script_name = "data\\scripts\\Witcher3.bms"
                        self.proc = bundle.BundleUnpack()
                    else:
                        self.proc = self.sorry()

                # C
                elif ext == 'cache':
                    # TODO: Add *.cache from total observer
                    if name == 'texture':
                        self.proc = texture_cache.TextureCache()

                elif ext in ("car",):
                    self.proc.script_name = "data\\scripts\\CAR.bms"

                elif ext in ("cat",):
                    # TODO: Add from GAUP and other

                    if magic == b'':
                        pass
                    else:
                        self.proc = self.sorry()

                elif ext in ("cfs",):
                    self.proc.script_name = "data\\scripts\\c9.bms"

                elif ext in ("cgr",):
                    self.proc.script_name = "data\\scripts\\criticaldamage.bms"

                # Check on Java class file
                elif ext in ("class",):
                    self.proc.script_name = "\\data\\wcx\\JavaClassUnpacker.wcx"

                elif ext in ("cmp",):  # TODO: Add from GAUP
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = "/u"
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "ddcmpa.exe"

                elif ext in ("cnt",):
                    self.proc.script_name = "data\\scripts\\CNTHiddenAndDangerous.bms"

                elif ext == "coalesced":
                    # TODO: coalesced from various Unreal Engine 3 games

                    if magic == b'':
                        pass
                    else:
                        self.proc = self.sorry()

                elif ext in ("cpr",):  # TODO: Add from GAUP
                    self.proc.script_name = "data\\scripts\\coyoteconsole.bms"

                elif ext in ("cps",):
                    self.proc.script_name = "data\\scripts\\kofxiiicps.bms"

                elif ext in ("csa",):
                    self.proc.script_name = "data\\scripts\\CSAGEEK.bms"

                # Check on Chrome Engine game
                elif ext in ("csb", "spb"):
                    self.proc.script_name = 'data/scripts/dying_light.bms'

                elif ext in ("csc",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = ""
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "scsextractor.exe"

                elif ext in ("ctpk",):
                    self.proc.script_name = "data\\scripts\\3dsarcv.bms"

                elif ext in ("cxt",):
                    self.proc.script_name = "data\\scripts\\CXTXFIR.bms"

                elif ext in ("cub",):
                    self.proc.script_name = "data\\scripts\\enigmatis.bms"

                # D
                elif ext in ("dag",):
                    self.proc.script_name = "data\\scripts\\DAGPKR3.bms"

                elif ext == "dat":
                    # TODO: A Engine, Learning Company Games, Moto Racer 3, Dirt 5

                    if magic == b'GCAX':  # GCA Archive
                        self.proc.script_name = "data\\wcx\\gca.wcx"
                    elif magic == b'ADAT':  # Anachronox
                        self.proc.script_name = "data\\scripts\\anachronox.bms"
                    elif magic == b'\x20\x00\x00\x00':  # TLOH
                        # TODO: Try how it's be work in the game TLOH
                        self.proc = sen_book.SenBook()
                    else:
                        self.proc = self.sorry()

                elif ext in ("data", "mini", "wd2"):
                    self.proc.script_name = "data\\scripts\\asphyre.bms"

                # Check on DGC archive
                elif ext in ("dgc", "dgca",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = "e"
                    self.proc.second_arg = '"%out_dir%"'
                    self.proc.splitter = ","
                    self.proc.program_name = "tools\\dgcac.exe"

                elif ext == "dir":
                    # TODO: Add from GAUP and other

                    if magic == b'':
                        pass
                    else:
                        self.proc = self.sorry()

                elif ext in ("dfl",):
                    self.proc.script_name = "data\\scripts\\drivingsimulator.bms"

                elif ext in ("dlz",):
                    self.proc.script_name = "data\\scripts\\heroesphantasiadlz.bms"

                elif ext in ("dpk",):
                    self.proc.script_name = "data\\scripts\\darkeden.bms"

                elif ext in ("dr",):
                    self.proc.script_name = "data\\scripts\\DRShowdownLegendsOfWrestling.bms"

                elif ext in ("drg",):
                    self.proc.script_name = "data\\scripts\\drg2sbg.bms"

                elif ext in ("drs",):  # TODO: Add from GAUP
                    self.proc.script_name = "data\\scripts\\DRS.bms"

                elif ext in ("dv2",):
                    self.proc.script_name = "data\\scripts\\dv2.bms"

                elif ext in ("dz", "dzip"):

                    if magic == b'DZ\x03\x00':
                        self.proc = dzip.DZIPExtractor()
                    elif magic == b'DZIP':  # Witcher 2 DZIP
                        self.proc = w2dzip.Witcher2DZIP()
                    else:
                        self.proc.script_name = "data\\scripts\\vector.bms"

                # E
                # Check on Aurora Engine game
                elif ext in ("erf", "rim"):
                    self.proc = aurora_engine.ERFUnpacker()

                elif ext in ("epc",):
                    self.proc.script_name = "data\\scripts\\doctorwho.bms"

                elif ext in ("exo",):
                    self.proc = self.sorry()

                # F
                elif ext in ("far",):  # TODO: Add from GAUP
                    self.proc.script_name = "data\\scripts\\djherofar.bms"

                elif ext == "fat":
                    # TODO: Add from GAUP, FAT image

                    if magic == b'':
                        pass
                    else:
                        self.proc = self.sorry()

                elif ext in ("flx",):
                    self.proc.script_name = "data\\scripts\\CrusaderNoRemorseFLX.bms"

                elif ext in ("fmf",):
                    self.proc.script_name = "data\\scripts\\eafmf.bms"

                # Check on Scimitar Engine game
                elif ext in ("forge",):
                    self.proc.script_name = "data\\scripts\\scimitar.bms"

                elif ext in ("frm",):
                    self.proc.script_name = "data\\scripts\\frmfonts.bms"

                # G
                # Check on GCA archive
                elif ext in ("gca",):
                    self.proc.script_name = "\\data\\wcx\\gca.wcx"

                elif ext in ("gob",):
                    self.proc.script_name = "data\\scripts\\EACricket2004GOB.bms"

                elif ext in ("grp",):
                    self.proc = grp.GRPExtractor()

                elif ext in ("gxt",):
                    self.proc = None
                    os.system(f'data\\ps_tools\\vita\\GXTConvert.exe {fn}')

                # H
                # TODO: Check on HA archive
                elif ext in ("ha",):
                    self.proc.script_name = "\\data\\wcx\\HA.wcx"

                elif ext in ("hal",):
                    self.proc.script_name = "data\\scripts\\HALAPUK.bms"

                elif ext in ("hgpk",):
                    self.proc.script_name = "data\\scripts\\10minspacestrategy.bms"

                elif ext in ("hogg",):
                    self.proc.script_name = "data\\scripts\\hogg.bms"

                elif ext in ("hpf",):
                    self.proc.script_name = "data\\scripts\\HPFHMG.bms"

                # Check on Hrust archive
                elif ext in ("hrp", "hrip",):
                    self.proc.script_name = "\\data\\wcx\\inhrust.wcx"

                # I
                elif ext == 'idwav':
                    self.proc.script_name = 'data/scripts/idwav_to_wav.bms'

                elif ext == "img":
                    # TODO: GTA, Disc Image

                    if magic == b'':
                        pass
                    else:
                        self.proc = self.sorry()

                elif ext in ('index', 'pindex'):

                    if 'master_resources' in self.name:
                        self.proc.script_name = 'data/scripts/deathloop.bms'
                    elif magic == b'\x05SER':
                        self.proc = resources.Resources()

                # J
                # K
                elif ext == 'ktx':
                    self.proc = KTXConvert()

                # L
                elif ext == 'lip':
                    self.proc = of_orc_and_human.OGGPacker()

                elif ext in ("lfs",):
                    self.proc = self.sorry()

                elif ext in ("lgp",):
                    self.proc.script_name = "data\\scripts\\FinalFantasy7LGP.bms"

                # M
                elif ext in ("m4b",):
                    self.proc.script_name = "data\\scripts\\EscapeFromMonkeyIslandM4B.bms"

                elif ext in ("mbx",):
                    self.proc.script_name = "data\\scripts\\HostileWatersMBX.bms"

                elif ext == 'mega2':
                    self.proc.script_name = 'data/scripts/doom2016_mega2.bms'

                elif ext in ("mfd",):
                    self.proc.script_name = "data\\scripts\\187rideordie.bms"

                elif ext in ("mnf",):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = ""
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "EsoExtractData.exe"

                elif ext in ("mng",):
                    self.proc.script_name = "data\\scripts\\HostileWatersMNG.bms"

                elif ext in ("mpk",):
                    self.proc.script_name = "data\\scripts\\invizimals.bms"

                elif ext in ("mse",):
                    self.proc.script_name = "data\\scripts\\3dsmax.bms"

                elif ext == 'msf':
                    self.proc.script_name = 'data\\scripts\\rage_idmsf.bms'

                # N
                # O
                elif ext in ("orc", "ork"):
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = ""
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "orkdec.exe"

                # P
                elif ext in ("packed",):
                    self.proc.script_name = "data\\scripts\\CastlevaniaLOS2.bms"

                elif ext == "pac":
                    # TODO: Add PAC from GAUP and other

                    if magic == b'':
                        pass
                    else:
                        self.proc = self.sorry()

                elif ext in ("pack",):  # YZ2 from RE4HD
                    self.proc = self.sorry()

                elif ext == 'pak':
                    # TODO: Sacred, Necrovision, Painkiller

                    if magic == b'\x37\xBD\x37\x4D':  # 7Ѕ7M, PopCap PAK
                        self.proc = seven_s_seven.Seven()
                    elif magic == b'\x78\x03\0\0':  # God of war 1 PAK
                        # TODO: Add God of War 2 support
                        self.proc.script_name = "data\\scripts\\god_of_war.bms"
                    elif magic == b'PACK':

                        if 'data.000.pak' in fn:  # 1242
                            self.proc.script_name = "data\\scripts\\1242.bms"
                        elif 'azangara' in fn.lower():  # Azangara
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

                        combo = QComboBox()
                        game_list = [key for key in re_engine.game_list.__keys()]
                        combo.addItems(game_list)

                        dial = CustomDialog(
                            text='Select a game',
                            btnCancel=True,
                            combo=combo,
                            style=self.setting['Main']['theme']
                        )

                        ok = dial.exec()

                        if ok:
                            self.proc = re_engine.ReEngine()
                            self.proc.game = dial.returned_data
                        else:
                            self.proc = None

                    elif magic == b'SBPA':  # Arcania: Gothic 4
                        self.proc.script_name = "data\\scripts\\arcania.bms"
                    elif magic == b'PAK ':  # Risen
                        self.proc.script_name = "data\\scripts\\risen.bms"
                    elif magic == b'KCAP':
                        self.proc.script_name = "data\\scripts\\full_mojo.bms"
                    elif magic == b'TONG':
                        self.proc.script_name = "data\\scripts\\tongas.bms"
                    elif magic == b'PAK2':  # Alien: Isolation
                        # self.proc.script_name = "data\\scripts\\alien_isolation.bms"
                        self.proc = isolation.AlienIsolation()
                    elif magic == b'PSCD':
                        self.proc.script_name = "data\\scripts\\sega_classics.bms"

                    elif magic == b'\x00' * 4:

                        with open(fn, 'rb') as test_read:
                            test_read.seek(4)
                            head2 = test_read.read(4)

                        if head2 == b'\x00' * 4:  # Unreal Engine 4
                            self.proc = unreal.Unreal()
                        elif head2 in (b'\0\0\0\x0e', ):
                            # TODO: Script can't saving file name, need to write inner unpacker.
                            #  Names contains in BIN files
                            self.proc.script_name = "data\\scripts\\alien_isolation.bms"
                            # self.proc = isolation.AlienIsolation()
                        else:  # Alone in the Dark
                            self.proc.script_name = "data\\scripts\\alonedark.bms"

                    else:

                        with open(fn, 'rb') as test_read:
                            test_read.seek(int.from_bytes(magic, byteorder='little') + 4)
                            arx = int.from_bytes(test_read.read(4), byteorder='little')

                        if arx in (0x46515641, 0x4149534E):
                            self.proc = arx_fatalis.PakExtractor()
                        else:
                            fn = fn.replace("/", "\\")
                            Popen(f'data\\tools\\PreyConvert.exe {fn}').wait()

                            fn = fn.replace('pak', 'zip')
                            self.proc = zip_archive.Zip()

                elif ext in 'patch':
                    self.proc = resources.Resources()

                    # if magic == b'\x22\x94\xAB\xCD':
                    #     self.proc = id_tech.RageResources()
                    # elif magic == b'\x05SER':
                    #     self.proc = id_tech.Doom2016()

                elif ext in ("phyre",):
                    self.proc = phyre.PhyreSave()

                elif ext in ("pig",):
                    self.proc.script_name = "data\\scripts\\CityofHeroesPIG.bms"

                elif ext in ("pix",):
                    self.proc.script_name = "data\\scripts\\CloseCombat4PIX.bms"

                elif ext == "pkg":
                    # TODO: Space Rangers, SWAT 4

                    if magic in (b'\x40\x06\0\0', b'\xc7\x01\0\0'):
                        self.proc = limbo.LimboPKG()
                    elif magic in (b'\0' * 4, b'\x00\x00\x81\x60', b'\xB1\x83\x81\x60'):
                        self.proc = sen_pkg.PKGExtractor()
                    else:
                        self.proc = self.sorry()

                elif ext in ("pwf",):
                    self.proc.script_name = "data\\scripts\\DeltaForceLandwarriorPWF.bms"

                # Q
                # R
                elif ext == 'resources':
                    # TODO: Add support for Dishonored 2 and Wolfenstein 2

                    if magic == b'\xD0\x00\x00\x0D':
                        self.proc = doom3_resources.Doom3BFG()
                    else:
                        self.proc = resources.Resources()

                elif ext in ("rfa",):
                    self.proc.script_name = "data\\scripts\\battlefield2moderncombat.bms"

                elif ext in ("rff",):
                    self.proc = rff.RFFExtractor()

                elif ext in ("rkv",):
                    self.proc.script_name = "data\\scripts\\rkv.bms"

                elif ext in ('rmdtoc', 'rmdblob'):
                    # self.proc = aw2.AlanWake2()
                    print(f'{localize.work_in_progress}...')

                elif ext in ('rmdp', 'packmeta'):
                    self.proc = remedy.Remedy()

                # Check on RenPy Engine game
                elif ext in ("rpa",):
                    self.proc = self.sorry()

                elif ext in ("rpf",):
                    self.proc = rdr2_audio.RDR2Audio()

                elif ext in ("rpack",):

                    if magic == b'RP6L':
                        self.proc = chrome_engine.RP6L()
                    else:
                        # TODO: Add functions to unpack other file types
                        print(f'{localize.work_in_progress}...')

                elif ext in ("rpkg",):
                    self.proc.script_name = "data\\scripts\\hitman2016.bms"

                elif ext in ("rsr",):
                    self.proc.script_name = "data\\scripts\\ImperialismIIRSR.bms"

                elif ext in ('ptr', 'pages', 'vmtr'):
                    # TODO: Add PAGES from The Evil Within 1, Rage and other games
                    self.proc.script_name = 'data/scripts/the_evil_within_2.bms'

                elif ext in ("rzb",):
                    self.proc.script_name = "data\\scripts\\blur2rzb.bms"

                # S
                elif ext in ("sab",):
                    self.proc.script_name = "data\\scripts\\justcause2sab.bms"

                elif ext in ("scs",):
                    self.proc.script_name = "data\\scripts\\scsgames.bms"

                elif ext in ("sh",):  # TODO: Add functions to unpack other file types
                    self.proc.script_name = "data\\scripts\\install4j.bms"

                elif ext in ("shd",):
                    self.proc.script_name = "data\\scripts\\janeangel2.bms"

                elif ext == 'sin':
                    # TODO: Add support for Sin
                    self.proc = self.sorry()

                elif ext in ("sngw",):  # MT Framework Audio
                    self.proc = self.sorry()

                elif ext in ("snd",):  # TODO: SND from GAUP
                    self.proc = dagger.DaggerSND()

                elif ext in ("spf",):
                    self.proc.script_name = "data\\scripts\\jeannedarc.bms"

                elif ext in ("ssp",):
                    self.proc.script_name = "data\\scripts\\jasonstormspace.bms"

                elif ext in ("stk", "itk",):
                    self.proc.script_name = "data\\scripts\\goblins.bms"

                elif ext == 'streamed':
                    # TODO: Try streamed from other idTech games

                    if magic == b'\x23\x94\xAB\xCD':
                        self.proc = streamed.Streamed()
                    # self.proc.script_name = 'data/scripts/the_evil_within.bms'

                    # if magic == b'\x23\x94\xAB\xCD':
                    #     self.proc.script_name = 'data/scripts/the_evil_within.bms'
                    # elif magic == b'\0\x10\0\x9D':
                    #     self.proc.script_name = 'data/scripts/idtech5streamed_eng.bms'
                    # elif magic == b'\0\x10\0\0':
                    #     self.proc.script_name = 'data/scripts/idtech5streamed_rus.bms'
                    # else:
                    #     self.proc.script_name = 'data/scripts/rage.bms'

                # TODO: Check on ShockWave Flash game
                elif ext in ("swf",):
                    self.proc = self.sorry()

                # T
                elif ext in ("tab",):
                    self.proc.script_name = 'data\\scripts\\madmax.bms'

                elif ext == 'tangoresource':
                    self.proc = tango.Tango()

                elif ext == 'tex':

                    if magic == b'TEX\0':
                        self.proc = tex.TEX2DDS()
                    elif magic == b'DDS ':
                        shutil.move(fn, fn.replace('tex', 'dds'))
                        self.proc = None

                elif ext in ("tiger",):  # TODO: Add something else
                    self.proc = other_prg.OtherProg()
                    self.proc.first_arg = "e"
                    self.proc.second_arg = f'"{self.out_dir}'
                    self.proc.program_name = "gibbed/Gibbed.TombRaider9.Unpack.exe"

                elif ext in ("toc", "sb"):
                    self.proc = self.sorry()

                elif ext in ("txt",):
                    # TODO: Lumia Saga, Simple text

                    if magic == b'':
                        pass
                    else:
                        self.proc = self.sorry()

                # U
                # Check on Unigene Engine game
                elif ext in ("ung",):
                    self.proc = self.sorry()

                # For video format don't contained audio
                elif ext in ("usm",):
                    self.proc = ffmpeg_tool.Converter()
                    self.proc.map = '0'

                # V
                elif ext in ("vce",):
                    self.proc.script_name = "data\\scripts\\HomeworldCataclysmVCE.bms"

                elif ext in ('vcpk',):
                    self.proc.script_name = "data\\scripts\\fatal_frame.bms"

                elif ext in ("vfs",):
                    self.proc = pathologic.MorUnpacker()

                elif ext in ("voc",):
                    self.proc.script_name = "data\\scripts\\Lemmings2(VOC)VOC.bms"

                elif ext in ("vpk",):
                    self.proc = source_vpk.VPKExtractor()

                # W
                # Check on RED Engine game
                elif ext in ("w3strings", "archive", "w2strings", "dzip"):
                    self.proc = self.sorry()

                elif ext in ("w3speech", ):
                    self.proc = w3speech.SpeechUnpacker()

                elif ext in ("win",):
                    self.proc.script_name = "data\\scripts\\yoyogames.bms"

                elif ext in ("wfp",):
                    self.proc.script_name = "data\\scripts\\bloodyroar3wfp.bms"

                elif ext in ('wl1', 'wl2', 'wl3', 'wl4', 'wl51', 'wl6'):
                    # TODO: Add support for Wolfenstein 3D
                    self.proc = self.sorry()

                elif ext in ("wrs",):
                    self.proc.script_name = "data\\scripts\\gamestudio.bms"

                # X
                elif ext in ("xbp",):
                    self.proc.script_name = "data\\scripts\\blitzgamesxbp.bms"

                elif ext in ("xcd",):
                    self.proc.script_name = "data\\scripts\\darknessxcd.bms"

                elif ext in ("xma",):
                    self.proc.script_name = "data\\scripts\\xma2wav.bms"
                    # TODO: Add support for Rage XMA
                    # self.proc.script_name = 'data/scripts/rage_idxma.bms'

                elif ext in ("xnb",):
                    self.proc.script_name = "data\\scripts\\xnb.bms"

                elif ext == 'xpr':
                    self.proc.script_name = 'data/scripts/Quake_4_X360_xpr.bms'

                # Y
                elif ext in ("yz1",):
                    self.proc = self.sorry()

                elif ext in ("yz2",):
                    self.proc = self.sorry()

                # Z
                elif ext in ("z",):
                    # TODO: Z Archive, LEGO Chess

                    if magic == b'':
                        pass
                    else:
                        self.proc = self.sorry()

                elif ext in ("zfs",):
                    self.proc.script_name = "data\\scripts\\CallToPower2ZFS.bms"

                elif ext in ("zpl",):
                    # TODO: Localize text
                    width, ok1 = QInputDialog.getInt(self, 'WARNING', 'Enter a width (mm):', min=1, max=2000)
                    height, ok2 = QInputDialog.getInt(self, 'WARNING', 'Enter a height (mm):', min=1, max=2000)

                    if width and ok1 and height and ok2:
                        self.proc = zpl2png.ZPL2PNG(width, height)

                elif ext in ("zwp",):
                    self.proc.script_name = "data\\scripts\\DarkReign2ZWP.bms"

                elif ext in ('esl', 'esm', 'esp', 'esx', 'pex'):
                    # TODO: Add functions to unpack other file types
                    print(f'{localize.work_in_progress}...')

                # Check on extension in GAUP list
                elif ext in ('arch00', 'arch01', 'arch02', 'arch03', 'arch04', 'arch05', 'a2c', 'abg', 'abl', 'acm',
                             'act', 'adf', 'age3scn', 'agg', 'ahm', 'al4', 'al8', 'ama', 'anm', 'avix', 'awd', 'bag',
                             'bank1sbk', 'bar', 'bbk', 'bf', 'bfs', 'bgx', 'bpa', 'bpk', 'bun', 'ceg', 'clz', 'cmo',
                             'cob', 'ctm', 'cts', 'cud', 'dbc', 'dbs', 'ddt', 'dirinfo', 'dta', 'dua', 'dun', 'dx1',
                             'dx2', 'dx3', 'ebm', 'editordata', 'elmares', 'emi', 'exp', 'ezd', 'ff', 'fpk', 'fra',
                             'frame', 'fsh', 'fuk', 'gdp', 'gea', 'gfx', 'glb', 'grl', 'gsc', 'gtr', 'h2o',
                             'h4c', 'h4d', 'h4r', 'hak', 'his', 'hog', 'idx', 'ifx', 'ins', 'iwi', 'jap', 'jaz', 'jdr',
                             'jsr', 'jtr', 'lbx', 'lgr', 'lgt', 'lmp', 'lod', 'lte', 'lud', 'lug', 'lut', 'lzc', 'map',
                             'md5', 'mdl', 'meg', 'mix', 'mjp', 'mjz', 'mod', 'msk', 'mult', 'mus', 'nif', 'nmo',
                             'npk', 'pal', 'paq', 'pbd', 'pbo', 'pck', 'pcx', 'pff', 'poa', 'pod', 'prm', 'psk', 'psp',
                             'ptx', 'pvd', 'qar', 'qfs', 'r16', 'r24', 'r8', 'raw', 'res', 'rez', 'rfd', 'rfh', 'rmp',
                             'rr', 'rs', 'rsb', 'rss', 'rts', 's4m', 'sbf', 'sc3', 'sct', 'scx', 'sdf', 'sdt',
                             'sequence', 'sga', 'sh4', 'sks', 'sl', 'slf', 'slv', 'spa', 'spr', 'st3', 'stb',
                             'stg', 'str', 'sud', 'sue', 'swa', 'syb', 'syj', 't24', 'tbf', 'tdu', 'ted', 'tf', 'thu',
                             'trc', 'twd', 'twt', 'txd', 'ucx', 'uka', 'ukx', 'vdu', 'viv', 'vmp', 'vol', 'vpp',
                             'vtf', 'wd', 'wdt', 'wep', 'whd', 'wtn', 'xcr', 'xfs', 'xmb', 'xpk', 'xti', 'xwb',
                             # msf, vid, spk
                             ):
                    # TODO: Check NIF from here and maybe add NIF model from other game, check PAL, check PCK, MSF
                    #  check RAW, check RES, check REZ, check VID and maybe add selector for video and VID from  here
                    self.proc.script_name = 'data\\wcx\\gaup_pro.wcx'

                elif ext == 'wad':
                    # TODO: Add other games

                    if magic == b'\x78\x03\x00\x00':
                        self.proc.script_name = 'data\\scripts\\god_of_war_wad.bms'
                    else:
                        self.proc = doom_wad.WadExtractor()

                # TODO: Check on RPG Maker game
                elif ext in ('rgss2a', 'rgss3a', 'rgssad', 'rpgmvm', 'rpgmvo', 'rpgmvp'):
                    self.proc = self.sorry()

                # Check on extension in Total Observer list
                elif ext in ('s2ma', 'sc2', 'bsp', 'cache', 'etc', 'gcf', 'hdr', 'mim', 'mime', 'mpq', 'mpqe', 'msm',
                             'pbb', 'pst', 'udf', 'vbsp', 'vp', 'xzp'):
                    self.proc.script_name = 'data\\wcx\\TotalObserver.wcx'

                # TODO: Check on extension in SAU list
                elif ext in ('4pp', 'bdx', 'brig', 'c', 'cam', 'cc', 'chr', 'dbi', 'df2', 'epf', 'fan',
                             'gor', 'group', 'hrs', 'ilb', 'jun', 'jus', 'maa', 'mul', 'nds', 'p00',
                             'p10', 'p99', 'rm', 'tgw', 'tlb', 'uop', 'vsr', 'war', 'wdb', 'xua', 'xub',
                             # box, flx, key, lbx
                             ):
                    # TODO: Check LBX from GAUP and SAU, check BOX, FLX, KEY
                    self.proc = self.sorry()

                # Check on archives
                elif ext in ('7z', 'rar', '001', 'cab', 'iso', 'xz', 'lzma', 'tar', 'cpio', 'bz2', 'bzip2', 'tbz',
                             'tbz2', 'gz', 'gzip', 'tgz', 'tpz', 'taz', 'lzh', 'lha', 'rpm', 'deb', 'arj', 'vhd',
                             'vhdx', 'wim', 'swm', 'esd', 'ntfs', 'dmg', 'hfs', 'xar', 'squashfs', 'apfs', 'doc',
                             'xls', 'mgs', 'tnef', 'dbx', 'mbox', 'tbb', 'emlx', 'eml', 'nws', 'mht', 'spk',
                             'mhtml', 'b64', 'uue', 'xxe', 'ntx', 'hqx', 'warc', 'ccd', 'cdi', 'chd', 'pgz',
                             'ciso', 'cso', 'cue', 'ecm', 'gdi', 'isz', 'mds', 'mdf', 'nrg', 'zisofs', 'asar', 'phar',
                             's01', 'e01', 'ex01', 'lo1', 'lx01', 'aff', 'ad1', 'whx', 'exfat', 'lz', 'rar5', 'txz',
                             # mbx, pmm
                             ):
                    # TODO: Check MBX here and upper, check PMM from video and here, check TXZ
                    # TODO: SPK (Of orc and human) in seven_zip and GAUP
                    self.proc = seven_zip.SevenZIP()

                # Check on video formats
                elif ext in ('3g2', '3gp', '3gp2', '3gpp', 'amv', 'avi', 'divx', 'dvr-ms', 'f4v', 'flc', 'fli', 'flic',
                             'flv', 'm1v', 'm2v', 'm4v', 'mk3d', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'mve', 'ogm',
                             'ogv', 'pam', 'pmf', 'pmm', 'pss', 'psw', 'rm', 'thp', 'ts', 'vid', 'vob', 'webm', 'wmv', 'xvid'):
                    self.proc = ffmpeg_tool.Converter()

                # Check on Unreal Engine game
                elif ext in ('pcc', 'u', 'uax', 'ugx', 'umx', 'un2', 'unr', 'upk', 'upx', 'usa', 'usx', 'ut2', 'utx',
                             'uvx', 'xxx'):
                    self.proc = unreal.Unreal()

                # Check on X-Ray Engine game
                elif ext in (f'db{i}' for i in range(10)):
                    self.proc.script_name = 'data\\wcx\\stalker.wcx'

                else:

                    if name == 'texture':
                        self.proc = arena_texture.ArenaTexture()
                    elif 'unity' in name.lower():
                        self.proc = unity.Unity()
                    elif magic == b'\x50\x53\x53\x47':
                        self.proc = of_orc_and_human.OOMExtractor()
                    else:
                        self.proc = self.sorry()

                if self.proc is not None:

                    result = self.q_connect(self.proc, fn, header=f'{localize.unpacking}: {fn}...')

                    if result == 7:
                        self.proc = seven_zip.SevenZIP()
                        self.q_connect(self.proc, fn, header=f'{localize.unpacking}: {fn}...')
