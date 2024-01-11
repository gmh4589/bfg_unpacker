import os.path

from icecream import ic
from source.reaper import after_dot2
from source.qprocess import QProcessList
from source.ui import localize

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

                with open(fn, 'rb') as fff:
                    self.head = fff.read(4)

                ext = fn.split('.')[-1].lower()

                # Check on ZIP signature
                if self.head == b'PK\x03\x04':
                    self.q_connect(self.zip, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on Bethesda game
                elif ext in after_dot2['bethesda']:
                    print('TODO: Work in progress...')

                # Check on extension in GAUP list
                elif ext in after_dot2['gaup']:
                    self.qbms.script_name = f'{self.root_dir}/data/wcx/gauppro.wcx'
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on idTech Engine game
                elif ext in after_dot2['id_tech']:
                    self.q_connect(self.id_tech, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on RPG Maker game
                elif ext in after_dot2['rpg_maker']:
                    print('TODO: Work in progress...')

                # Check on extension in Total Observer list
                elif ext in after_dot2['total_observer']:
                    self.qbms.script_name = f'{self.root_dir}/data/wcx/TotalObserver.wcx'
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on extension in SAU list
                elif ext in after_dot2['sau']:
                    print('TODO: Work in progress...')

                # Check on archives
                elif ext in after_dot2['seven_zip']:
                    self.q_connect(self.seven_zip, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on video formats
                elif ext in after_dot2['video']:
                    self.q_connect(self.ffmpeg, fn, header='Convert...')

                # Check on Unreal Engine game
                elif ext in after_dot2['unreal']:
                    self.q_connect(self.unreal, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on X-Ray Engine game
                elif ext in after_dot2['x-ray']:
                    self.qbms.script_name = f'{self.root_dir}/data/wcx/stalker.wcx'
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("aes",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/coalescedaes.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext == "afs":

                    if self.head == b'AFS\00':
                        self.q_connect(self.afs, fn,
                                       header=f'{localize.unpacking}: {fn}...')
                    else:
                        self.sorry()

                # Check on UnArk support archive
                elif ext in ("alz", "egg", "bh",):
                    self.qbms.script_name = f'{self.root_dir}/data/wcx/UnArkWCX.wcx'
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("ara",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/batmanara.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext == "arc":
                    # TODO: The Incredible Hulk (2008)

                    if self.head == b'ARC\x00':  # MT Framework
                        self.qbms.script_name = f"{self.root_dir}/data/scripts/dmc4.bms"
                        self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                    else:
                        self.sorry()

                elif ext in ("arcv",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/3dsarcv.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("arch06",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/shadowofmordor.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("arz",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/ironlorearz.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on Asura Engine game
                elif ext in ("asr",):
                    print('TODO: Work in progress...')

                # Check on Unity Engine game
                elif ext in ("assets", 'resS'):
                    self.q_connect(self.unity, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("atd",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/ATD.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("atg", "rcf",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/atgcorecement.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("azp",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/CloseCombat4AZP.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("bcc",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/bccpsp.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on Dark Souls Engine game
                elif ext in ("bdt", "bhd5",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/darksoul.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("bf",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/BF.bms"
                    self.q_connect(self.qbms,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("bfg",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/bigfishgames81.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("bfl",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/ColinMcRaeRallyBFL.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("bfp",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/BFP.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

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
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/bitsquidstreams.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("blz",):
                    self.other_prg.first_arg = ""
                    self.other_prg.second_arg = f'"{self.out_dir}'
                    self.other_prg.program_name = "blzpack.exe"
                    self.q_connect(self.other_prg, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("bmb",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/privatedancerbmb.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on Wwise Audio
                elif ext in ("bnk",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/wwisebnk.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("box",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/BOXLEMBOX.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext == "bundle":
                    # TODO: Red Engine, Pay Day

                    if self.head == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("car",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/CAR.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("cfs",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/c9.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("cgr",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/criticaldamage.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on Java class file
                elif ext in ("class",):
                    self.qbms.script_name = f"{self.root_dir}/data/wcx/JavaClassUnpacker.wcx"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("cmp",):
                    self.other_prg.first_arg = "/u"
                    self.other_prg.second_arg = f'"{self.out_dir}'
                    self.other_prg.program_name = "ddcmpa.exe"
                    self.q_connect(self.other_prg, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("cnt",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/CNTHiddenAndDangerous.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("cpr",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/coyoteconsole.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("cps",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/kofxiiicps.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("csa",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/CSAGEEK.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on Chrome Engine game
                elif ext in ("csb", "spb", "rpack"):
                    print('TODO: Work in progress...')

                elif ext in ("csc",):
                    self.other_prg.first_arg = ""
                    self.other_prg.second_arg = f'"{self.out_dir}'
                    self.other_prg.program_name = "scsextractor.exe"
                    self.q_connect(self.other_prg, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("ctpk",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/3dsarcv.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("cxt",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/CXTXFIR.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("cub",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/enigmatis.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("dag",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/DAGPKR3.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext == "dat":
                    # TODO: A Engine, Learning Company Games, Moto Racer 3, Dirt 5

                    if self.head == b'GCAX':  # GCA Archive
                        self.qbms.script_name = f"{self.root_dir}/data/wcx/gca.wcx"
                        self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                    elif self.head == b'ADAT':  # Anachronox
                        self.qbms.script_name = f"{self.root_dir}/data/scripts/anachronox.bms"
                    else:
                        self.sorry()

                elif ext in ("data", "mini", "wd2"):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/asphyre.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on DGC archive
                elif ext in ("dgc", "dgca",):
                    self.other_prg.first_arg = "e"
                    self.other_prg.second_arg = f'"{self.out_dir}'
                    self.other_prg.program_name = "dgcac.exe"
                    self.q_connect(self.other_prg, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("dfl",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/drivingsimulator.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("dlz",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/heroesphantasiadlz.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("dpk",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/darkeden.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("dr",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/DRShowdownLegendsOfWrestling.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("drg",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/drg2sbg.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("drs",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/DRS.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("dv2",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/dv2.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("dz",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/vector.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on Aurora Engine game
                elif ext in ("erf", "bif", "rim"):
                    self.q_connect(self.aurora, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("epc",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/doctorwho.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("exo",):
                    # fileReaper(mp3, "", header=f'{localize.unpacking}: {fn}...')
                    print('TODO: Work in progress...')

                elif ext in ("far",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/djherofar.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("flx",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/CrusaderNoRemorseFLX.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("fmf",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/eafmf.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on Scimitar Engine game
                elif ext in ("forge",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/scimitar.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("frm",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/frmfonts.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on GCA archive
                elif ext in ("gca",):
                    self.qbms.script_name = f"{self.root_dir}/data/wcx/gca.wcx"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("gob",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/EACricket2004GOB.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on HA archive
                elif ext in ("ha",):
                    self.qbms.script_name = f"{self.root_dir}/data/wcx/HA.wcx"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("hal",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/HALAPUK.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("hgpk",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/10minspacestrategy.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("hogg",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/hogg.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("hpf",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/HPFHMG.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on Hrust archive
                elif ext in ("hrp", "hrip",):
                    self.qbms.script_name = f"{self.root_dir}/data/wcx/inhrust.wcx"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext == "img":

                    # TODO: GTA, Disc Image

                    if self.head == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("lfs",):
                    print('TODO: Work in progress...')

                elif ext in ("lgp",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/FinalFantasy7LGP.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("m4b",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/EscapeFromMonkeyIslandM4B.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("mbx",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/HostileWatersMBX.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("mfd",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/187rideordie.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("mnf",):
                    self.other_prg.first_arg = ""
                    self.other_prg.second_arg = f'"{self.out_dir}'
                    self.other_prg.program_name = "EsoExtractData.exe"
                    self.q_connect(self.other_prg, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("mng",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/HostileWatersMNG.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("mpk",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/invizimals.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("mse",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/3dsmax.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("orc", "ork"):
                    self.other_prg.first_arg = ""
                    self.other_prg.second_arg = f'"{self.out_dir}'
                    self.other_prg.program_name = "orkdec.exe"
                    self.q_connect(self.other_prg, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("packed",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/CastlevaniaLOS2.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("pack",):  # YZ2 from RE4HD
                    print('TODO: Work in progress...')

                elif ext == 'pak':

                    # TODO: Arx Fatalis, Sacred, Necrovision, Painkiller

                    if self.head == b'\x37\xBD\x37\x4D':  # 7Ѕ7M, PopCap PAK
                        self.q_connect(self.x7, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                    elif self.head == b'PACK':

                        if 'data.000.pak' in fn:  # 1242
                            self.qbms.script_name = f"{self.root_dir}/data/scripts/1242.bms"
                            self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                        elif 'azangara' in fn.lower():  # Azangara
                            self.qbms.script_name = f"{self.root_dir}/data/scripts/azangara.bms"
                            self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                        else:  # idTech 1+2
                            self.q_connect(self.quake_pak, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                    elif self.head == b'KPKA':  # RE Engine
                        pass
                    elif self.head == b'SBPA':  # Arcania: Gothic 4
                        self.qbms.script_name = f"{self.root_dir}/data/scripts/arcania.bms"
                        self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                    elif self.head == b'PAK ':  # Risen
                        self.qbms.script_name = f"{self.root_dir}/data/scripts/risen.bms"
                        self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                    elif self.head == b'KCAP':
                        self.qbms.script_name = f"{self.root_dir}/data/scripts/full_mojo.bms"
                        self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                    elif self.head == b'TONG':
                        self.qbms.script_name = f"{self.root_dir}/data/scripts/tongas.bms"
                        self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                    elif self.head == b'PAK2':
                        self.qbms.script_name = f"{self.root_dir}/data/scripts/alien_isolation.bms"
                        self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                    elif self.head == b'PSCD':
                        self.qbms.script_name = f"{self.root_dir}/data/scripts/sega_classics.bms"
                        self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                    elif self.head == b'\x00' * 4:

                        if 'Content/Paks' in fn:  # Unreal Engine 4
                            self.q_connect(self.unreal, fn,
                                   header=f'{localize.unpacking}: {fn}...')
                        else:  # Alone in the Dark
                            self.qbms.script_name = f"{self.root_dir}/data/scripts/alonedark.bms"
                            self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                    else:
                        self.sorry()

                elif ext in ("phyre",):
                    self.q_connect(self.phyre, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("pig",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/CityofHeroesPIG.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("pix",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/CloseCombat4PIX.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext == "pkg":

                    # TODO: Space Rangers, SWAT 4, Trails of Cold Steel

                    if self.head == b'':
                        pass
                    else:
                        self.sorry()

                elif ext in ("pwf",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/DeltaForceLandwarriorPWF.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("rfa",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/battlefield2moderncombat.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("rkv",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/rkv.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on RenPy Engine game
                elif ext in ("rpa",):
                    # Engine('RenPy', header=f'{localize.unpacking}: {fn}...')
                    print('TODO: Work in progress...')

                elif ext in ("rpkg",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/hitman2016.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("rsr",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/ImperialismIIRSR.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("rzb",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/blur2rzb.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("sab",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/justcause2sab.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("scs",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/scsgames.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("sh",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/install4j.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("shd",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/janeangel2.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("sngw",):  # MT Framework Audio
                    print('TODO: Work in progress...')

                elif ext in ("spf",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/jeannedarc.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("ssp",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/jasonstormspace.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("stk", "itk",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/goblins.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on ShockWave Flash game
                elif ext in ("swf",):
                    print('TODO: Work in progress...')

                elif ext in ("tab",):
                    self.qbms.script_name = f'{self.root_dir}/data/scripts/madmax.bms'
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("tiger",):
                    self.other_prg.first_arg = "e"
                    self.other_prg.second_arg = f'"{self.out_dir}'
                    self.other_prg.program_name = "gibbed/Gibbed.TombRaider9.Unpack.exe"
                    self.q_connect(self.other_prg, fn,
                                   header=f'{localize.unpacking}: {fn}...')

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
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/HomeworldCataclysmVCE.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("vfs",):
                    self.q_connect(self.mor, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("voc",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/Lemmings2(VOC)VOC.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("vpk", ):
                    self.q_connect(self.source_vpk, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                # Check on RED Engine game
                elif ext in ("w3strings", "w3speech", "archive", "w2strings", "dzip"):
                    print('TODO: Work in progress...')

                elif ext in ("wfp",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/bloodyroar3wfp.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("wrs",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/gamestudio.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("xbp",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/blitzgamesxbp.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("xcd",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/darknessxcd.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("xma",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/xma2wav.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("xnb",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/xnb.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

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
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/CallToPower2ZFS.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("zpl",):
                    self.q_connect(self.zpl2png, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                elif ext in ("zwp",):
                    self.qbms.script_name = f"{self.root_dir}/data/scripts/DarkReign2ZWP.bms"
                    self.q_connect(self.qbms, fn,
                                   header=f'{localize.unpacking}: {fn}...')

                else:
                    self.sorry()
