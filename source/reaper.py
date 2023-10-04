
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal

after_dot = {'_Asura': ('All Asura Engine File(*.asr;*.pc;*.hdr;*.ru;*.en;*.fr;*.it;*.ge;*.sp;*.pl;*.cz;*.gui)|'
                        'ASR Files(*.asr)|Localization Files(*.ru;*.en;*.fr;*.it;*.ge;*.sp;*.pl;*.cz)|'
                        'GUI Files(*.gui)|HDR Files(*.hdr)|PC Files(*.pc)|'),
             '_Anvil': "Forge file(*.forge)|",
             '_Aurora': "All Aurora Engine Files(*.erf;*.dzip;*.bif;*.rim)|"
                        "ERF Files(*.erf)|BIF Files(*.bif)|RIM Files(*.rim)|DZIP files(*.dzip)|",
             '_Bethesda': 'All Bethesda Game Files(*.bsa; *.ba2; *.esp; *.esm; *.esl; *.esx; *.snd; *.pex; '
                          'TEXBSI.*;*.omod;*.fomod; *.mnf)|Bethesda Softwork Archives(*.bsa; *.ba2)|'
                          'Plugin and master files(*.esp; *.esm; *.esl)|Decompressed plugin files(*.esx)|'
                          'TESO Data files(*.mnf)|Daggerfall sound archives(*.snd)|'
                          'Compiled Papyrus Scripts(*.pex)|Redgaurd Textures Archives(texbsi.*)|'
                          'Nexus Mod Files(*.omod;*.fomod)|Textures Archives(*textures*)|'
                          'Meshes Archives(*mesh*)|Audio Archives(*audio*; *sound*; *voice*)|'
                          'Miscs Archives(*misc*; *script*)|Main Archives(*main*)|'
                          'Animations Archives(*animation*)|',
             '_Build': 'Build Engine Files(*.grp; *.art; *.rff; *.tga)|',
             '_Chrome': 'Chrome Engine Files(*.csb; *.spb; *.rpack; *.pak)|',
             '_Chromium': 'PAK Files(*.pak)|',
             '_Construct': 'Construct Engine Files(*.exe;*.dll;;*.pak)|',
             '_CryEngine': 'PAK Files(*.pak)|',
             '_Flash': 'ShockWave Flash Files(*.swf)|',
             '_FrostBite': 'SB and TOC Files(*.sb;*.toc)|',
             '_GameMaker': 'data.win File(data.win)|',
             '_Glacier': 'Glacier Engine Files(*.wav; *.whd; *.prm; *.tex; *.anm; *.*_binkvid; *.zip; *.rpkg; '
                         '*.bin; *.lgt; *.spk; *.*_resourcelib; *.dcx; *.archive; *.str)|',
             '_Godot': 'Godot package files(*.pck; *.exe)|',
             '_idTech': 'All idTech Resource File(*.wad;*.pak;*.pk3;*.pk4;*.pkz;*.*resource*;*.index;*.streamed;'
                        '*.bimage;*.idwav;*.mega2;*.ptr;*.pages;*.vmtr;*.wl6;*.msf;*.xma;*.xpr;*.lib;*.pack;'
                        '*.sin)|DOOM\\idTech 1(*.wad)|Quake\\idTech 2(*.pak)|idTech 3(*.pk3)|idTech 4(*.pk4)|'
                        'idTech 5, 6(*.*resource*; *.tangoresource; *.streamed;*.ptr;*.pages;*.vmtr;*.index;'
                        '*.mega2)|Audio Files(*.idwav)|Textures Files(*.bimage)|Wolfenstin 3d Files(*.wl6)|'
                        'Rage Console Audio(*.msf; *.xma)|Quake 4 XBOX 360 Files(*.xpr)|'
                        'Doomsday Engine Files(*.lib;*.pack)|Sin Gold SIN files(*.sin)|',
             '_Infinity': 'Infinity Engine Files(*.key; *.gob; *.lmp)|',
             '_LithTech': 'LithTech Engine Files(*.rez; *.Arch*)|',
             '_MTFramework': 'MT Framework Engine Files(*.arc;*.sngw)|',
             '_PopCapPackAll': "All Suported(*.pak;*.dll;*.obb;*.dz)|"
                               "PopCap PAK Files(*.pak)|Download Library(*.dll)|Android Cache(*.obb)|"
                               "DZIP Archives(*.dz)|",
             '_RedEngine': "All Red Engine Files(*.bundle;*.w3strings;texture.cache;*.w3speech;*.archive;"
                           "*.w2strings;*.dzip;*.xml)|",
             '_ReEngine': 'RE Engine File(*.pak; *.tex; *.dds)|',
             '_RenPy': 'RPA File(*.rpa)|',
             '_RPGMaker': 'RPG Maker Archives(*.rgssad;*.rgss2a;*.rgss3a; *.rpgmvp; *.rpgmvo; *.rpgmvm; *.pak)|',
             '_Source': 'Source Engine File(*.gcf;*.wad;*.pak;*_dir.vpk;*.bsp;*.cache;*.vbsp;*.xzp)|'
                        'GCF File(*.gcf)|Valve Package File(*.vpk)|Valve Package File Vol. 1(*_dir.vpk)|'
                        'Valve Map File(*.bsp;*.vbsp)|',
             '_Sen': 'All supported(*.dat; *. pkg; *. phyre; *.xlsx)|DAT Scripts(*.dat)|'
                     'PKG Files(*.pkg)|PHYRE2D Files(*.phyre)|Book Files(book*.dat)|Decompiled Scripts(*.xlsx)|',
             '_Snowdrop': 'sdfdata files(*.sdfdata)|',
             '_TellTale': 'TellTale Archives(*.ttarch;*.ttarch2)|',
             '_Unigene': 'UNG File(*.ung)|',
             '_Unreal': 'Unreal Engine File(*.u*;*.xxx;*.pak;*.locres;*.pcc)|'
                        'Unreal Engine 1-2(*.u*)|Unreal Engine 3(*.u*;*.xxx;*.pcc)|'
                        'Unreal Engine 4(*.pak;*.locres)|',
             '_Unreal4': 'Unreal Engine 4(*.pak;*.locres)|',
             '_ZIP': 'All archive files (*.7z;*.zip;*.rar;*.001;*.cab;*.iso;*.xz;*.txz;*.lzma;*.tar;*.cpio;'
                     '*.bz2;*.bzip2;*.tbz;*.tbz2;*.gz;*.gzip;*.tgz;*.tpz;*.z;*.taz;*.lzh;*.lha;*.rpm;*.ded;'
                     '*.arj;*.vhd;*.vhdx;*.wim;*.swm;*.esd;*.fat;*.ntfs;*.dmg;*.hfs;*.xar;*.squashfs;*.apfs;'
                     '*.epub;*.fbz;*.fb2z;*.docx;*.xlsx;*.doc;*.docm;*.dotm;*.xls;*.ods;*.odt;*.mgs;*.tnef;'
                     '*.dbx;*.mbx;*.mbox;*.tbb;*.pmm;*.emlx;*.eml;*.nws;*.mht;*.mhtml;*.b64;*.uue;*.xxe;*.ntx;'
                     '*.bin;*.hqx;*.warc;*.pyz;*.ccd;*.img;*.cdi;*.chd;*.ciso;*.cso;*.cue;*.ecm;*.gdi;*.isz;'
                     '*.mds;*.mdf;*.nrg;*.zisofs;*.asar;*.phar;*.s01;*.e01;*.ex01;*.lo1;*.lx01;*.aff;*.ad1;'
                     '*.whx;*.exfat;*.pak;*.gro;*.kfs;*.lz)|'}


def file_reaper(func_name):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        func_name(*args, **kwargs)
        end = datetime.now()
        print('Done!', end - start)

    return wrapper


class Reaper(QThread):
    update_signal = pyqtSignal(int, str, str, bool)

    def __init__(self):
        super().__init__()
        self.file_name = 'file_name'
        self.output_folder = 'output_folder'
        self.unpack = True

    def run(self):
        pass
