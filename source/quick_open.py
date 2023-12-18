import os

from source.reaper import after_dot2
from source.qprocess import QProcessList


class QuickOpen(QProcessList):

    @staticmethod
    def sorry():  # 😢
        print('Не удалось найти распаковщик автоматически!\n'
              'Попробуйте выбрать игру или тип файла вручную!')

    def QuickPAK(self):

        if self.head == b'7S7M':
            self.q_connect(self.x7, self.file_name)
        elif self.head == b'PACK':
            self.q_connect(self.quake_pak, self.file_name)
        elif self.head == b'KPKA':  # RE Engine
            pass
        elif self.head == b'\x00' * 4:
            self.q_connect(self.unreal, self.file_name)
        else:
            self.sorry()

    def QuickDAT(self):

        if self.head == b'GCAX':  # GCA Archive
            pass
        else:
            self.sorry()

    def QuickARC(self):

        if self.head == b'ARC\x00':  # MT Framework
            self.qbms.script_name = f"{self.root_dir}/data/scripts/dmc4.bms"
            self.q_connect(self.qbms, self.file_name)
        else:
            self.sorry()

    def QuickPKG(self):

        if self.head == b'':
            pass
        else:
            self.sorry()

    def QuickIMG(self):

        if self.head == b'':
            pass
        else:
            self.sorry()

    def QuickBIN(self):

        if self.head == b'':
            pass
        else:
            self.sorry()

    def QuickBundle(self):

        if self.head == b'':
            pass
        else:
            self.sorry()

    def find_reaper(self):

        with open(self.file_name, 'rb') as fff:
            self.head = fff.read(4)

        ext = self.file_name.split('.')[-1]

        # Check on ZIP signature
        if self.head == b'PK\x03\x04':
            self.q_connect(self.zip, self.file_name)

        # Check on multi format extension
        elif ext == 'pak':
            self.QuickPAK()

        elif ext == "dat":
            self.QuickDAT()

        elif ext == "pkg":
            self.QuickPKG()

        elif ext == "img":
            self.QuickIMG()

        elif ext == "bin":
            self.QuickBIN()

        elif ext == "bundle":
            self.QuickBundle()

        # Check on extension in GAUP list
        elif ext in after_dot2['gaup']:
            self.qbms.script_name = f'{self.root_dir}/data/wcx/gauppro.wcx'
            self.q_connect(self.qbms, self.file_name)

        # Check on extension in Total Observer list
        elif ext in after_dot2['total_observer']:
            self.qbms.script_name = f'{self.root_dir}/data/wcx/TotalObserver.wcx'
            self.q_connect(self.qbms, self.file_name)

        # Check on extension in SAU list
        elif ext in after_dot2['sau']:
            # SAU(self.file_name)
            print('TODO: Work in progress...')

        # Check on archives
        elif ext in after_dot2['seven_zip']:
            # OtherPRG('', '7zip/7z.exe ', ' x -o"' + self.sFolderName + '" ', '', self.root_dir + '/data/7zip',
            # self.file_name)
            print('TODO: Work in progress...')

        # Check on Unreal Engine game
        elif ext in after_dot2['unreal']:
            # Engine('Unreal', self.file_name)
            print('TODO: Work in progress...')

        # Check on RPG Maker game
        elif ext in after_dot2['rpg_maker']:
            # Engine('RPGMaker', self.file_name)
            print('TODO: Work in progress...')

        # Check on Bethesda game
        elif ext in after_dot2['bethesda']:
            # Engine('Bethesda', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("Arch06",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/shadowofmordor.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("vfs",):
            self.q_connect(self.mor, self.file_name)

        elif ext in ("toc", "sb"):
            # Engine('Frostbite', self.file_name)
            print('TODO: Work in progress...')

        # Check on Chrome Engine game
        elif ext in ("csb", "spb", "rpack"):
            # Engine('Chrome', self.file_name)
            print('TODO: Work in progress...')

        # Check on Aurora Engine game
        elif ext in ("erf", "bif", "rim"):
            self.q_connect(self.aurora, self.file_name)

        # Check on RED Engine game
        elif ext in ("w3strings", "w3speech", "archive", "w2strings", "dzip"):
            # Engine('Red# Engine', self.file_name)
            print('TODO: Work in progress...')

        # Check on Unity Engine game
        elif ext in ("assets", 'resS'):
            # Engine('Unity', self.file_name)
            print('TODO: Work in progress...')

        # Check on idTech Engine game
        elif ext in after_dot2['id_tech']:
            self.q_connect(self.id_tech, self.file_name)

        elif ext == "arc":
            self.QuickARC()

        elif ext in ("sngw",):
            pass

        # Check on Wwise Audio
        elif ext in ("bnk",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/wwisebnk.bms"
            self.q_connect(self.qbms, self.file_name)

        # Check on X-Ray Engine game
        elif ext in after_dot2['x-ray']:
            self.qbms.script_name = f'{self.root_dir}/data/wcx/stalker.wcx'
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("cmp",):
            os.system(f'"{self.root_dir}/data/ddcmpa.exe" /u "{self.file_name}" "{self.sFolderName}"')

        elif ext in ("orc", "ork"):
            os.system(f'{self.root_dir}/data/orkdec.exe "{self.file_name}" "{self.sFolderName}"')

        elif ext in ("csc",):
            os.system(f'{self.root_dir}/data/scsextractor.exe "{self.file_name}" "{self.sFolderName}"')

        elif ext in ("data", "mini", "wd2"):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/asphyre.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("atd",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/ATD.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("atg", "rcf",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/atgcorecement.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("ara",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/batmanara.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("rfa",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/battlefield2moderncombat.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("bcc",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/bccpsp.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("bf",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/BF.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("bfp",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/BFP.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("bfg",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/bigfishgames81.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("bkf",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/bitsquidstreams.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("xbp",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/blitzgamesxbp.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("wfp",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/bloodyroar3wfp.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("rzb",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/blur2rzb.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("box",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/BOXLEMBOX.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("cfs",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/c9.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("zfs",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/CallToPower2ZFS.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("car",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/CAR.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("pig",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/CityofHeroesPIG.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("azp",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/CloseCombat4AZP.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("pix",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/CloseCombat4PIX.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("cnt",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/CNTHiddenAndDangerous.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("aes",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/coalescedaes.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("bfl",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/ColinMcRaeRallyBFL.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("cpr",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/coyoteconsole.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("cgr",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/criticaldamage.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("flx",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/CrusaderNoRemorseFLX.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("csa",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/CSAGEEK.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("cxt",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/CXTXFIR.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("dag",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/DAGPKR3.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("zwp",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/DarkReign2ZWP.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("dpk",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/darkeden.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("xcd",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/darknessxcd.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("pwf",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/DeltaForceLandwarriorPWF.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("far",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/djherofar.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("dr",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/DRShowdownLegendsOfWrestling.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("drg",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/drg2sbg.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("dfl",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/drivingsimulator.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("drs",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/DRS.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("gob",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/EACricket2004GOB.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("fmf",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/eafmf.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("cub",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/enigmatis.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("m4b",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/EscapeFromMonkeyIslandM4B.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("lgp",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/FinalFantasy7LGP.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("frm",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/frmfonts.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("wrs",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/gamestudio.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("stk", "itk",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/goblins.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("hal",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/HALAPUK.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("dlz",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/heroesphantasiadlz.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("vce",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/HomeworldCataclysmVCE.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("mbx",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/HostileWatersMBX.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("mng",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/HostileWatersMNG.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("hpf",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/HPFHMG.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("rsr",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/ImperialismIIRSR.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("sh",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/install4j.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("mpk",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/invizimals.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("arz",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/ironlorearz.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("shd",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/janeangel2.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("ssp",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/jasonstormspace.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("spf",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/jeannedarc.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("sab",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/justcause2sab.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("cps",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/kofxiiicps.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("voc",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/Lemmings2(VOC)VOC.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("bmb",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/privatedancerbmb.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("rkv",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/rkv.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("scs",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/scsgames.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("xnb",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/xnb.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("xma",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/xma2wav.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("tab",):
            self.qbms.script_name = f'{self.root_dir}/data/scripts/madmax.bms'
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("epc",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/doctorwho.bms"
            self.q_connect(self.qbms, self.file_name)

        # Check on video formats
        elif ext in after_dot2['video']:
            os.system(f'{self.root_dir}/data/ffmpeg.exe -i "{self.file_name}" -vb 5M -vcodec hevc "{self.sFolderName}'
                      f'{os.path.basename(self.file_name)}.mkv"')

        # Check on RenPy Engine game
        elif ext in ("rpa",):
            # Engine('RenPy', self.file_name)
            print('TODO: Work in progress...')

        # Check on Asura Engine game
        elif ext in ("asr",):
            # Engine('Asura', self.file_name)
            print('TODO: Work in progress...')

        # Check on Unigene Engine game
        elif ext in ("ung",):
            # Engine('Unigene', self.file_name)
            print('TODO: Work in progress...')

        # Check on ShockWave Flash game
        elif ext in ("swf",):
            # Engine('Flash', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("dz",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/vector.bms"
            self.q_connect(self.qbms, self.file_name)

        # Check on Java class file
        elif ext in ("class",):
            self.qbms.script_name = f"{self.root_dir}/data/wcx/JavaClassUnpacker.wcx"
            self.q_connect(self.qbms, self.file_name)

        # Check on GCA archive
        elif ext in ("gca",):
            self.qbms.script_name = f"{self.root_dir}/data/wcx/gca.wcx"
            self.q_connect(self.qbms, self.file_name)

        # Check on HA archive
        elif ext in ("ha",):
            self.qbms.script_name = f"{self.root_dir}/data/wcx/HA.wcx"
            self.q_connect(self.qbms, self.file_name)

        # Check on UnArk support archive
        elif ext in ("alz", "egg", "bh",):
            self.qbms.script_name = f'{self.root_dir}/data/wcx/UnArkWCX.wcx'
            self.q_connect(self.qbms, self.file_name)

        # Check on Hrust archive
        elif ext in ("hrp", "hrip",):
            self.qbms.script_name = f"{self.root_dir}/data/wcx/inhrust.wcx"
            self.q_connect(self.qbms, self.file_name)

        # Check on DGC archive
        elif ext in ("dgc", "dgca",):
            os.system(f'{self.root_dir}/data/dgcac.exe e "{self.file_name}" "{self.sFolderName}"')

        elif ext in ("tiger",):
            os.system(f'{self.root_dir}/data/gibbed/Gibbed.TombRaider9.Unpack.exe e "{self.file_name}" '
                      f'"{self.sFolderName}"')

        elif ext in ("blz",):
            os.system(f'{self.root_dir}/data/blzpack.exe "{self.file_name}" "{self.sFolderName}"')

        elif ext in ("mnf",):
            os.system(f'{self.root_dir}/data/EsoExtractData.exe "{self.file_name}" "{self.sFolderName}"')

        elif ext in ("arcv",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/3dsarcv.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("ctpk",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/3dsarcv.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("mse",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/3dsmax.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("hgpk",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/10minspacestrategy.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("mfd",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/187rideordie.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("packed",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/CastlevaniaLOS2.bms"
            self.q_connect(self.qbms, self.file_name)

        # Check on Dark Souls Engine game
        elif ext in ("bdt", "bhd5",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/darksoul.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("dv2",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/dv2.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("hogg",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/hogg.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("lfs",):
            print('TODO: Work in progress...')

        elif ext in ("yz2", "pack",):
            print('TODO: Work in progress...')

        elif ext in ("rpkg",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/hitman2016.bms"
            self.q_connect(self.qbms, self.file_name)

        # Check on Scimitar Engine game
        elif ext in ("forge",):
            self.qbms.script_name = f"{self.root_dir}/data/scripts/scimitar.bms"
            self.q_connect(self.qbms, self.file_name)

        elif ext in ("exo",):
            # fileReaper(mp3, "", self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("phyre",):
            self.q_connect(self.phyre, self.file_name)

        elif ext in ("zpl",):
            self.q_connect(self.zpl2png, self.file_name)

        else:
            self.sorry()
