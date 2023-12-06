import os

from source.reaper import after_dot2
from source.qprocess import QProcessList
from source.unpacker import Unpacker


class QuickOpen(QProcessList):

    def QuickPAK(self, file):
        print('TODO: Work in progress...')

    def QuickDAT(self, file):
        print('TODO: Work in progress...')

    def QuickPKG(self, file):
        print('TODO: Work in progress...')

    def QuickIMG(self, file):
        print('TODO: Work in progress...')

    def QuickBIN(self, file):
        print('TODO: Work in progress...')

    def QuickBundle(self, file):
        print('TODO: Work in progress...')

    def find_reaper(self):

        with open(self.file_name, 'rb') as fff:
            self.head = fff.read(4)

        ext = self.file_name.split('.')[-1]
        unpacker = Unpacker()

        if self.head == b'PK\x03\x04':
            self.q_connect(self.zip, self.file_name)

        elif ext == 'pak':
            self.QuickPAK(self.file_name)

        elif ext == "dat":
            self.QuickDAT(self.file_name)

        elif ext == "pkg":
            self.QuickPKG(self.file_name)

        elif ext == "img":
            self.QuickIMG(self.file_name)

        elif ext == "bin":
            self.QuickBIN(self.file_name)

        elif ext in after_dot2['gaup']:
            unpacker.quick_bms(f'{self.root_dir}/data/wcx/gauppro.wcx', self.file_name)

        elif ext in ("Arch06",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/shadowofmordor.bms", self.file_name)

        elif ext in ("vfs",):
            self.q_connect(self.mor, self.file_name)

        elif ext in after_dot2['total_observer']:
            unpacker.quick_bms(f'{self.root_dir}/data/wcx/TotalObserver.wcx', self.file_name)

        elif ext in after_dot2['sau']:
            # SAU(self.file_name)
            print('TODO: Work in progress...')

        elif ext in after_dot2['seven_zip']:
            # OtherPRG('', '7zip/7z.exe ', ' x -o"' + self.sFolderName + '" ', '', self.root_dir + '/data/7zip',
            # self.file_name)
            print('TODO: Work in progress...')

        elif ext in after_dot2['unreal']:
            # Engine('Unreal', self.file_name)
            print('TODO: Work in progress...')

        elif ext in after_dot2['rpg_maker']:
            # Engine('RPGMaker', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("toc", "sb"):
            # Engine('Frostbite', self.file_name)
            print('TODO: Work in progress...')

        elif ext in after_dot2['bethesda']:
            # Engine('Bethesda', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("csb", "spb", "rpack"):
            # Engine('Chrome', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("erf", "bif", "rim"):
            self.q_connect(self.aurora, self.file_name)

        elif ext in ("bundle",):
            self.QuickBundle(self.file_name)

        elif ext in ("w3strings", "w3speech", "archive", "w2strings", "dzip"):
            # Engine('Red# Engine', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("assets", 'resS'):
            # Engine('Unity', self.file_name)
            print('TODO: Work in progress...')

        elif ext in after_dot2['id_tech']:
            self.q_connect(self.id_tech, self.file_name)

        elif ext in ("arc", "sbgw"):
            # Engine('MTFramework', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("bnk",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/wwisebnk.bms", self.file_name)

        elif ext in after_dot2['x-ray']:
            unpacker.quick_bms(f'{self.root_dir}/data/wcx/stalker.wcx', self.file_name)

        elif ext in ("cmp",):
            os.system(f'"{self.root_dir}/data/ddcmpa.exe" /u "{self.file_name}" "{self.sFolderName}"')

        elif ext in ("orc", "ork"):
            os.system(f'{self.root_dir}/data/orkdec.exe "{self.file_name}" "{self.sFolderName}"')

        elif ext in ("csc",):
            os.system(f'{self.root_dir}/data/scsextractor.exe "{self.file_name}" "{self.sFolderName}"')

        elif ext in ("data", "mini", "wd2"):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/asphyre.bms", self.file_name)

        elif ext in ("atd",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/ATD.bms", self.file_name)

        elif ext in ("atg", "rcf",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/atgcorecement.bms", self.file_name)

        elif ext in ("ara",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/batmanara.bms", self.file_name)

        elif ext in ("rfa",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/battlefield2moderncombat.bms", self.file_name)

        elif ext in ("bcc",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/bccpsp.bms", self.file_name)

        elif ext in ("bf",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/BF.bms", self.file_name)

        elif ext in ("bfp",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/BFP.bms", self.file_name)

        elif ext in ("bfg",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/bigfishgames81.bms", self.file_name)

        elif ext in ("bkf",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/bitsquidstreams.bms", self.file_name)

        elif ext in ("xbp",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/blitzgamesxbp.bms", self.file_name)

        elif ext in ("wfp",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/bloodyroar3wfp.bms", self.file_name)

        elif ext in ("rzb",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/blur2rzb.bms", self.file_name)

        elif ext in ("box",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/BOXLEMBOX.bms", self.file_name)

        elif ext in ("cfs",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/c9.bms", self.file_name)

        elif ext in ("zfs",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/CallToPower2ZFS.bms", self.file_name)

        elif ext in ("car",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/CAR.bms", self.file_name)

        elif ext in ("pig",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/CityofHeroesPIG.bms", self.file_name)

        elif ext in ("azp",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/CloseCombat4AZP.bms", self.file_name)

        elif ext in ("pix",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/CloseCombat4PIX.bms", self.file_name)

        elif ext in ("cnt",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/CNTHiddenAndDangerous.bms", self.file_name)

        elif ext in ("aes",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/coalescedaes.bms", self.file_name)

        elif ext in ("bfl",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/ColinMcRaeRallyBFL.bms", self.file_name)

        elif ext in ("cpr",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/coyoteconsole.bms", self.file_name)

        elif ext in ("cgr",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/criticaldamage.bms", self.file_name)

        elif ext in ("flx",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/CrusaderNoRemorseFLX.bms", self.file_name)

        elif ext in ("csa",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/CSAGEEK.bms", self.file_name)

        elif ext in ("cxt",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/CXTXFIR.bms", self.file_name)

        elif ext in ("dag",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/DAGPKR3.bms", self.file_name)

        elif ext in ("zwp",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/DarkReign2ZWP.bms", self.file_name)

        elif ext in ("dpk",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/darkeden.bms", self.file_name)

        elif ext in ("xcd",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/darknessxcd.bms", self.file_name)

        elif ext in ("pwf",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/DeltaForceLandwarriorPWF.bms", self.file_name)

        elif ext in ("far",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/djherofar.bms", self.file_name)

        elif ext in ("dr",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/DRShowdownLegendsOfWrestling.bms", self.file_name)

        elif ext in ("drg",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/drg2sbg.bms", self.file_name)

        elif ext in ("dfl",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/drivingsimulator.bms", self.file_name)

        elif ext in ("drs",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/DRS.bms", self.file_name)

        elif ext in ("gob",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/EACricket2004GOB.bms", self.file_name)

        elif ext in ("fmf",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/eafmf.bms", self.file_name)

        elif ext in ("cub",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/enigmatis.bms", self.file_name)

        elif ext in ("m4b",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/EscapeFromMonkeyIslandM4B.bms", self.file_name)

        elif ext in ("lgp",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/FinalFantasy7LGP.bms", self.file_name)

        elif ext in ("frm",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/frmfonts.bms", self.file_name)

        elif ext in ("wrs",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/gamestudio.bms", self.file_name)

        elif ext in ("stk", "itk",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/goblins.bms", self.file_name)

        elif ext in ("hal",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/HALAPUK.bms", self.file_name)

        elif ext in ("dlz",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/heroesphantasiadlz.bms", self.file_name)

        elif ext in ("vce",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/HomeworldCataclysmVCE.bms", self.file_name)

        elif ext in ("mbx",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/HostileWatersMBX.bms", self.file_name)

        elif ext in ("mng",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/HostileWatersMNG.bms", self.file_name)

        elif ext in ("hpf",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/HPFHMG.bms", self.file_name)

        elif ext in ("rsr",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/ImperialismIIRSR.bms", self.file_name)

        elif ext in ("sh",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/install4j.bms", self.file_name)

        elif ext in ("mpk",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/invizimals.bms", self.file_name)

        elif ext in ("arz",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/ironlorearz.bms", self.file_name)

        elif ext in ("shd",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/janeangel2.bms", self.file_name)

        elif ext in ("ssp",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/jasonstormspace.bms", self.file_name)

        elif ext in ("spf",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/jeannedarc.bms", self.file_name)

        elif ext in ("sab",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/justcause2sab.bms", self.file_name)

        elif ext in ("cps",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/kofxiiicps.bms", self.file_name)

        elif ext in ("voc",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/Lemmings2(VOC)VOC.bms", self.file_name)

        elif ext in ("bmb",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/privatedancerbmb.bms", self.file_name)

        elif ext in ("rkv",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/rkv.bms", self.file_name)

        elif ext in ("scs",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/scsgames.bms", self.file_name)

        elif ext in ("xnb",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/xnb.bms", self.file_name)

        elif ext in ("xma",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/xma2wav.bms", self.file_name)

        elif ext in ("tab",):
            unpacker.quick_bms(f'{self.root_dir}/data/scripts/madmax.bms"{self.file_name}"', self.file_name)

        elif ext in ("epc",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/doctorwho.bms", self.file_name)

        elif ext in after_dot2['video']:
            os.system(f'{self.root_dir}/data/ffmpeg.exe -i "{self.file_name}" -vb 5M -vcodec hevc "{self.sFolderName}'
                      f'{os.path.basename(self.file_name)}.mkv"')

        elif ext in ("rpa",):
            # Engine('RenPy', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("asr",):
            # Engine('Asura', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("ung",):
            # Engine('Unigene', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("swf",):
            # Engine('Flash', self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("dz",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/vector.bms", self.file_name)

        elif ext in ("class",):
            unpacker.quick_bms(f"{self.root_dir}/data/wcx/JavaClassUnpacker.wcx", self.file_name)

        elif ext in ("gca",):
            unpacker.quick_bms(f"{self.root_dir}/data/wcx/gca.wcx", self.file_name)

        elif ext in ("ha",):
            unpacker.quick_bms(f"{self.root_dir}/data/wcx/HA.wcx", self.file_name)

        elif ext in ("alz", "egg", "bh",):
            unpacker.quick_bms(f'{self.root_dir}/data/wcx/UnArkWCX.wcx', self.file_name)

        elif ext in ("hrp", "hrip",):
            unpacker.quick_bms(f"{self.root_dir}/data/wcx/inhrust.wcx", self.file_name)

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
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/3dsarcv.bms", self.file_name)

        elif ext in ("ctpk",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/3dsarcv.bms", self.file_name)

        elif ext in ("mse",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/3dsmax.bms", self.file_name)

        elif ext in ("hgpk",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/10minspacestrategy.bms", self.file_name)

        elif ext in ("mfd",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/187rideordie.bms", self.file_name)

        elif ext in ("packed",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/CastlevaniaLOS2.bms", self.file_name)

        elif ext in ("bdt", "bhd5",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/darksoul.bms", self.file_name)

        elif ext in ("dv2",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/dv2.bms", self.file_name)

        elif ext in ("hogg",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/hogg.bms", self.file_name)

        elif ext in ("lfs",):
            print('TODO: Work in progress...')

        elif ext in ("yz2", "pack",):
            print('TODO: Work in progress...')

        elif ext in ("rpkg",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/hitman2016.bms", self.file_name)

        elif ext in ("forge",):
            unpacker.quick_bms(f"{self.root_dir}/data/scripts/scimitar.bms", self.file_name)

        elif ext in ("exo",):
            # fileReaper(mp3, "", self.file_name)
            print('TODO: Work in progress...')

        elif ext in ("phyre",):
            self.q_connect(self.phyre, self.file_name)

        else:
            print('Не удалось найти распаковщик автоматически!\n'
                  'Попробуйте выбрать игру или тип файла вручную!')
