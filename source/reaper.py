import threading
import os
import shutil
from subprocess import Popen
from PyQt6.QtCore import QThread, pyqtSignal
from abc import abstractmethod
from tkinter.messagebox import showinfo
from icecream import ic
from datetime import datetime
from pathlib import Path

from source.ui import localize
from source.setting import Setting
from source.codecs.zip_methods import zip_methods

DEBUG = False if os.path.exists('dev_tools') else True


def logger(level: str, message: str, show: bool = False, messagebox: bool = False) -> None:

    if show:
        print(message)

    with open('log.txt', 'a') as log:
        log.write(f'{datetime.now()} - [{level}]: {message}\n')

    if messagebox:
        showinfo(title=level, message=message)


def file_reaper(func_name):

    def wrapper(*args, **kwargs):
        error = None
        function = str(func_name).split(" ")[1]
        start = datetime.now()

        if DEBUG:

            try:
                func_name(*args, **kwargs)
            except Exception as e:
                error = e

        else:
            func_name(*args, **kwargs)

        end = datetime.now()
        print(f'{localize.done}\n'
              f'{localize.duration} {end - start}')

        if error is None:
            logger(f'INFO',
                   f'\n\tFunction: {function}\n\tStart: {start}\n\tEnd: {end}\n\tDuration: {end - start}\n')
        else:
            print(f'ERROR IN {function}: {error}!!!')
            logger(f'ERROR',
                   f'\n\tFunction: {function}\n\tStart: {start}\n\tError: {error}\n')

    return wrapper


class Reaper(QThread, Setting):
    update_signal = pyqtSignal(int, str, str, bool)
    COMPRESSED = True
    file_name = ''
    path_to_root = os.path.curdir
    com_type = None
    new_ext = 'dat'

    def __init__(self):
        super().__init__()
        self.output_folder = self.setting['Main']['out_path']
        os.makedirs(self.output_folder, exist_ok=True)
        self.out = ''
        self.err = ''
        self.output = []
        self.end = False

    @staticmethod
    def folderSize(path, was_files=0):
        fsize = 0
        numfile = 0
        iteration = 0
        for file in Path(path).rglob('*'):

            if os.path.isfile(file):
                fsize += os.path.getsize(file)
                numfile += 1
            iteration += 1

        return fsize, numfile - was_files, iteration

    def update_pb(self, file_count: int, current_file: int, file_name: str):

        file_count = 1 if file_count == 0 else file_count
        current_file = 1 if current_file == 0 else current_file
        ic(f'{current_file}/{file_count}: {localize.saving} - {file_name}...')
        print(f'{current_file}/{file_count}: {localize.saving} - {file_name}...')

        self.update_signal.emit(int(100 / file_count * current_file),
                                f'{current_file + 1}/{file_count}',
                                f'{localize.saving} - {file_name}...',
                                True if current_file + 1 >= file_count else False)

    @abstractmethod
    def run(self):
        pass

    def magic(self, magic: list, read_magic: bytes | int, message: str) -> bool:

        for m in magic:

            if m == read_magic:
                return True

        else:
            print(localize.not_correct_file.replace('%%', message))
            self.update_signal.emit(100, '', '', True)
            return False

    # TODO: Very slow working... 🐌
    def unzip(self, f_name: str,
              c_num: int = 1,
              get_ext: bool = False,
              test: bool = False,
              encrypt: bool = False,
              crypt_method: str = '',
              crypt_key='') -> None:

        out_path = self.output_folder if test else os.environ['TEMP']

        if encrypt:
            # TODO: Need tests
            dump_name = crypt_method + '_enc.dmp'
            script = (f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" '
                      f'-o -a "{crypt_method}{" " + crypt_key if crypt_key else ""}" '
                      f'"{self.path_to_root}\\data\\QuickBMS\\encryption_scan.bms")" '
                      f'"{f_name}" "{out_path}"').replace("/", "\\")
        else:
            dump_name = zip_methods.get_zip_indexes()[c_num] + '.dmp'
            script = (f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" -o -a "{c_num}" '
                      f'"{self.path_to_root}\\data\\QuickBMS\\comtype_scan2.bms" '
                      f'"{f_name}" "{out_path}"').replace("/", "\\")

        if not test:
            Popen(script).wait()
            dump_file = os.path.join(out_path, dump_name)

            try:

                with open(dump_file, 'rb') as dmp:
                    unzip_data = dmp.read()

                try:
                    os.remove(f_name)
                except OSError:
                    pass

                if get_ext:
                    self.new_ext = self.get_ext(unzip_data[:4])
                    f_name = f_name.replace('dat', self.new_ext)

                with open(f_name, 'wb') as out_f:
                    out_f.write(unzip_data)

            except (FileNotFoundError, PermissionError):
                print(localize.filed_to_unzip)
                ic(localize.filed_to_unzip)

        else:
            proc = Popen(script)
            threading.Timer(10, proc.terminate).start()
            proc.wait()

    @staticmethod
    def get_ext(index: bytes) -> str:
        ext_list = {  # Image Formats
            b'DDS\x20': 'dds', b'\x89PNG': 'png', b'GIF8': 'gif', b'\xFF\xD8\xFF\xE0': 'jpg',
            # Audio Formats
            b'RIFF': 'wav', b'RIFX': 'wav', b'OggS': 'ogg',
            # Archive Formats
            b'PK\x03\x04': 'zip',
            # Document formats
            b'\x25PDF': 'pdf',
        }

        try:
            return ext_list[index]
        except (IndexError, KeyError):

            try:
                return index[:3].decode('ascii').lower()
            except UnicodeDecodeError:
                return 'dat'


class OutReader:

    def __init__(self):
        self.out = ''
        self.err = ''
        self.output = []
        self.end = False

    def sim_reader(self, prg):

        while True:
            self.out = prg.stdout.read()

            if self.out:
                ic(self.out)

            if self.end:
                break

    def sim_e_reader(self, prg):

        while True:
            self.err = prg.stderr.read()

            if self.err:
                ic(self.err)

            if self.end:
                break

    def out_reader(self, prg, splitter=' '):

        while True:
            self.out = prg.stdout.readline().strip()
            self.output = self.out.split(splitter)

            if self.out:
                ic(self.out)

            if self.end:
                break

    def err_reader(self, prg):

        while True:
            self.err = prg.stderr.readline().strip()

            if self.err:
                ic(self.err)
                print(self.err)

            if self.end:
                break

after_dot = {'_Asura':
                 'All Asura Engine File (*.asr;*.pc;*.hdr;*.ru;*.en;*.fr;*.it;*.ge;*.sp;*.pl;*.cz;*.gui)|'
                 'ASR Files (*.asr)|Localization Files (*.ru;*.en;*.fr;*.it;*.ge;*.sp;*.pl;*.cz)|'
                 'GUI Files (*.gui)|HDR Files (*.hdr)|PC Files (*.pc)|',
             '_Anvil':
                 "Forge file (*.forge)|",
             '_Aurora':
                 "All Aurora Engine Files (*.erf;*.dzip;*.bif;*.rim)|"
                 "ERF Files (*.erf)|BIF Files (*.bif)|RIM Files (*.rim)|DZIP files (*.dzip)|",
             '_Bethesda':
                 'All Bethesda Game Files (*.bsa; *.ba2; *.esp; *.esm; *.esl; *.esx; *.snd; *.pex; '
                 'TEXBSI.*; TEXTURE.*; *.omod; *.fomod; *.mnf)|Bethesda Softwork Archives (*.bsa; *.ba2)|'
                 'Plugin and master files (*.esp; *.esm; *.esl)|Decompressed plugin files (*.esx)|'
                 'TESO Data files (*.mnf)|SND sound archives (*.snd)|'
                 'Compiled Papyrus Scripts (*.pex)|Redgaurd Textures (texbsi.*)|Arena Textures (texture.*)|'
                 'Nexus Mod Files (*.omod; *.fomod)|Textures Archives (*textures*)|'
                 'Meshes Archives (*mesh*)|Audio Archives (*audio*; *sound*; *voice*)|'
                 'Scripts Archives (*misc*; *script*)|Main Archives (*main*)|'
                 'Animations Archives (*animation*)|',
             '_Build':
                 'Build Engine Files (*.grp; *.art; *.rff; *.tga)|',
             '_Chrome':
                 'Chrome Engine Files (*.csb; *.spb; *.rpack; *.pak)|',
             '_Chromium':
                 'PAK Files (*.pak)|',
             '_Construct':
                 'Construct Engine Files (*.exe; *.dll; *.pak)|',
             '_CryEngine':
                 'PAK Files (*.pak)|',
             '_Flash':
                 'ShockWave Flash Files (*.swf)|',
             '_FrostBite':
                 'SB and TOC Files (*.sb;*.toc)|',
             '_GameMaker':
                 'data.win File (data.win)|',
             '_Glacier':
                 'Glacier Engine Files (*.wav; *.whd; *.prm; *.tex; *.anm; *.*_binkvid; *.zip; *.rpkg; '
                 '*.bin; *.lgt; *.spk; *.*_resourcelib; *.dcx; *.archive; *.str)|',
             '_Godot':
                 'Godot package files (*.pck; *.exe)|',
             '_idTech':
                 'All idTech Resource File (*.wad;*.pak;*.pk3;*.pk4;*.pkz;*.*resource*;*.index;*.pindex;*.streamed;'
                 '*.bimage;*.idwav;*.mega2;*.ptr;*.pages;*.vmtr;*.wl6;*.msf;*.xma;*.xpr;*.lib;*.pack;*.patch;'
                 '*.sin)|DOOM\\idTech 1 (*.wad)|Quake\\idTech 2 (*.pak)|idTech 3 (*.pk3)|idTech 4 (*.pk4)|'
                 'idTech 5, 6 (*.*resource*; *.tangoresource; *.streamed;*.ptr;*.pages;*.vmtr;*.index;*.pindex;'
                 '*.patch; *.mega2)|Audio Files (*.idwav)|Textures Files (*.bimage)|Wolfenstin 3d Files (*.wl6)|'
                 'Rage Console Audio (*.msf; *.xma)|Quake 4 XBOX 360 Files (*.xpr)|'
                 'Doomsday Engine Files (*.lib;*.pack)|Sin Gold SIN files (*.sin)|',
             '_Infinity':
                 'Infinity Engine Files (*.key; *.gob; *.lmp)|',
             '_Innosetup':
                 '_Innosetup Installer Files (*.exe)|',
             '_LithTech':
                 'LithTech Engine Files (*.rez; *.Arch*)|',
             '_MTFramework':
                 'MT Framework Engine Files (*.arc;*.sngw)|',
             '_PopCapPackAll':
                 "All Suported (*.pak;*.dll;*.obb;*.dz)|"
                 "PopCap PAK Files (*.pak)|Download Library (*.dll)|Android Cache (*.obb)|"
                 "DZIP Archives (*.dz)|",
             '_RedEngine':
                 "All Red Engine Files (*.bundle;*.w3strings;texture.cache;*.w3speech;*.archive;"
                 "*.w2strings;*.dzip;*.xml)|",
             '_ReEngine':
                 'RE Engine File (*.pak; *.tex; *.dds)|',
             '_RenPy':
                 'RPA File (*.rpa)|',
             '_RPGMaker':
                 'RPG Maker Archives (*.rgssad;*.rgss2a;*.rgss3a; *.rpgmvp; *.rpgmvo; *.rpgmvm; *.pak)|',
             '_Source':
                 'Source Engine File (*.gcf;*.wad;*.pak;*_dir.vpk;*.bsp;*.cache;*.vbsp;*.xzp)|'
                 'GCF File (*.gcf)|Valve Package File (*.vpk)|Valve Package File Vol. 1 (*_dir.vpk)|'
                 'Valve Map File (*.bsp;*.vbsp)|',
             '_Sen':
                 'All supported (*.dat; *.pkg; *.phyre; *.xlsx)|DAT Scripts (*.dat)|'
                 'PKG Files (*.pkg)|PHYRE2D Files (*.phyre)|Book Files (book*.dat)|Decompiled Scripts (*.xlsx)|',
             '_Snowdrop':
                 'sdfdata files (*.sdfdata)|',
             '_TellTale':
                 'TellTale Archives (*.ttarch;*.ttarch2)|',
             '_Unigene':
                 'UNG File (*.ung)|',
             '_Unreal':
                 'Unreal Engine File (*.u*;*.xxx;*.pak;*.locres;*.pcc)|'
                 'Unreal Engine 1-2 (*.u*)|Unreal Engine 3 (*.u*;*.xxx;*.pcc)|'
                 'Unreal Engine 4 (*.pak;*.locres)|',
             '_Unreal4':
                 'Unreal Engine 4 (*.pak;*.locres)|',
             '_ZIP':
                 'All archive files (*.7z;*.zip;*.rar;*.001;*.cab;*.iso;*.xz;*.txz;*.lzma;*.tar;*.cpio;'
                 '*.bz2;*.bzip2;*.tbz;*.tbz2;*.gz;*.gzip;*.tgz;*.tpz;*.z;*.taz;*.lzh;*.lha;*.rpm;*.deb;'
                 '*.arj;*.vhd;*.vhdx;*.wim;*.swm;*.esd;*.fat;*.ntfs;*.dmg;*.hfs;*.xar;*.squashfs;*.apfs;'
                 '*.epub;*.fbz;*.fb2z;*.docx;*.xlsx;*.doc;*.docm;*.dotm;*.xls;*.ods;*.odt;*.mgs;*.tnef;'
                 '*.dbx;*.mbx;*.mbox;*.tbb;*.pmm;*.emlx;*.eml;*.nws;*.mht;*.mhtml;*.b64;*.uue;*.xxe;*.ntx;'
                 '*.bin;*.hqx;*.warc;*.pyz;*.ccd;*.img;*.cdi;*.chd;*.ciso;*.cso;*.cue;*.ecm;*.gdi;*.isz;'
                 '*.mds;*.mdf;*.nrg;*.zisofs;*.asar;*.phar;*.s01;*.e01;*.ex01;*.lo1;*.lx01;*.aff;*.ad1;'
                 '*.whx;*.exfat;*.pak;*.gro;*.kfs;*.lz;*.grp;*fb3;*.piz;*.omod;*.fomod;*.rar5)|'
                 '7zip Archives (*.7z)|ZIP archives (*.zip,*.zipx;*.piz;*.grp;*.gro;*.pk3;*.pk4;*.pak)|'
                 'RAR Archives (*.rar;*.rar5;*.001)|Cabinet Archives (*.cab)|Mod Archives (*.omod;*.fomod)|'
                 'E-book files (*.epub,*.fbz;*,fb2x;*.fb3;*.txtz)|GZIP Archives (*.gz;*.gzip)|'
                 'Disc Image Files (*.iso;*.vhd;*.vhdx;*.wim;*.swm;*.esd;*.fat;*.ntfs;*.dmg;*.hfs;*.squashfs;'
                 '*.apfs;*.bin;*.cue;*.img;*.cdi;*.chd;*.ciso;*.cso;*.ecm;*.gdi;*.isz;*.mds;*.mdf;*.nrg;*.zisofs|'
                 'Web Archives (*.dbx;*.mbx;*.mbox;*.tbb;*.pmm;*.emlx;*.eml;*.nws;*.mht;*.mhtml;*.b64)|'
             }
