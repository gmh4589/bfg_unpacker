from datetime import datetime
import os
from PyQt5.QtCore import QThread, pyqtSignal
from source.ui import localize


def file_reaper(func_name):

    def wrapper(*args, **kwargs):
        error = None
        function = str(func_name).split(" ")[1]
        start = datetime.now()

        try:
            func_name(*args, **kwargs)
        except Exception as e:
            error = e

        end = datetime.now()
        print(f'{localize.done}\n'
              f'{end - start}')

        with open('./log.txt', 'a') as log:

            if error is None:
                log.write(f'Function: {function}\n'
                          f'\tStart: {start}\tEnd: {end}\tDuration: {end-start}\n')
            else:
                print(f'ERROR IN {function}: {error}!!!')
                log.write(f'Function: {function}\n'
                          f'\tStart: {start}\tError: {error}\n')

    return wrapper


class Reaper(QThread):
    update_signal = pyqtSignal(int, str, str, bool)

    def __init__(self):
        super().__init__()
        self.file_name = ''
        self.output_folder = ''
        self.unpack = True
        self.path_to_root = os.path.abspath(__file__).split('source')[0]


after_dot = {'_Asura': 'All Asura Engine File(*.asr;*.pc;*.hdr;*.ru;*.en;*.fr;*.it;*.ge;*.sp;*.pl;*.cz;*.gui)|'
                       'ASR Files(*.asr)|Localization Files(*.ru;*.en;*.fr;*.it;*.ge;*.sp;*.pl;*.cz)|'
                       'GUI Files(*.gui)|HDR Files(*.hdr)|PC Files(*.pc)|',
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
                          'Scripts Archives(*misc*; *script*)|Main Archives(*main*)|'
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
                     '*.bz2;*.bzip2;*.tbz;*.tbz2;*.gz;*.gzip;*.tgz;*.tpz;*.z;*.taz;*.lzh;*.lha;*.rpm;*.deb;'
                     '*.arj;*.vhd;*.vhdx;*.wim;*.swm;*.esd;*.fat;*.ntfs;*.dmg;*.hfs;*.xar;*.squashfs;*.apfs;'
                     '*.epub;*.fbz;*.fb2z;*.docx;*.xlsx;*.doc;*.docm;*.dotm;*.xls;*.ods;*.odt;*.mgs;*.tnef;'
                     '*.dbx;*.mbx;*.mbox;*.tbb;*.pmm;*.emlx;*.eml;*.nws;*.mht;*.mhtml;*.b64;*.uue;*.xxe;*.ntx;'
                     '*.bin;*.hqx;*.warc;*.pyz;*.ccd;*.img;*.cdi;*.chd;*.ciso;*.cso;*.cue;*.ecm;*.gdi;*.isz;'
                     '*.mds;*.mdf;*.nrg;*.zisofs;*.asar;*.phar;*.s01;*.e01;*.ex01;*.lo1;*.lx01;*.aff;*.ad1;'
                     '*.whx;*.exfat;*.pak;*.gro;*.kfs;*.lz;*.grp;*fb3;*.piz;*.omod;*.fomod;*.rar5)|'
                     '7zip Archives(*.7z)|ZIP archives(*.zip,*.zipx;*.piz;*.grp;*.gro;*.pk3;*.pk4;*.pak)|'
                     'RAR Archives(*.rar;*.rar5;*.001)|Cabinet Archives(*.cab)|Mod Archives(*.omod;*.fomod)|'
                     'E-book files(*.epub,*.fbz;*,fb2x;*.fb3;*.txtz)|GZIP Archives(*.gz;*.gzip)|'
                     'Disc Image Files(*.iso;*.vhd;*.vhdx;*.wim;*.swm;*.esd;*.fat;*.ntfs;*.dmg;*.hfs;*.squashfs;'
                     '*.apfs;*.bin;*.cue;*.img;*.cdi;*.chd;*.ciso;*.cso;*.ecm;*.gdi;*.isz;*.mds;*.mdf;*.nrg;*.zisofs|'
                     'Web Archives(*.dbx;*.mbx;*.mbox;*.tbb;*.pmm;*.emlx;*.eml;*.nws;*.mht;*.mhtml;*.b64)|'}

after_dot2 = {'gaup':
                  ('Arch00', 'Arch01', 'Arch02', 'Arch03', 'Arch04', 'Arch05', 'a2c', 'abg', 'abl', 'acm', 'act', 'adf',
                   'afs', 'age3scn', 'agg', 'ahm', 'al4', 'al8', 'ama', 'anm', 'ark', 'avix', 'awd', 'bag', 'bank1sbk',
                   'bar', 'bbk', 'bf', 'bfs', 'bgx', 'big', 'bpa', 'bpk', 'bun', 'cat', 'ceg', 'clz', 'cmo', 'cmp',
                   'cob', 'cpr', 'ctm', 'cts', 'cud', 'dbc', 'dbs', 'ddt', 'dir', 'dirinfo', 'drs', 'dta', 'dua', 'dun',
                   'dx1', 'dx2', 'dx3', 'ebm', 'editordata', 'elmares', 'emi', 'exp', 'ezd', 'far', 'fat', 'ff', 'fpk',
                   'fra', 'frame', 'fsh', 'fuk', 'gdp', 'gea', 'gfx', 'glb', 'grl', 'grp', 'gsc', 'gtr', 'h2o', 'h4c',
                   'h4d', 'h4r', 'hak', 'his', 'hog', 'idx', 'ifx', 'ins', 'iwi', 'jap', 'jaz', 'jdr', 'jsr', 'jtr',
                   'lbx', 'lgr', 'lgt', 'lmp', 'lod', 'lte', 'lud', 'lug', 'lut', 'lzc', 'map', 'md5', 'mdl', 'meg',
                   'mix', 'mjp', 'mjz', 'mod', 'msf', 'msk', 'mult', 'mus', 'nif', 'nmo', 'npk', 'pac', 'pal', 'paq',
                   'pbd', 'pbo', 'pck', 'pcx', 'pff', 'poa', 'pod', 'prm', 'psk', 'psp', 'ptx', 'pvd', 'qar', 'qfs',
                   'r16', 'r24', 'r8', 'raw', 'res', 'rez', 'rfd', 'rfh', 'rmp', 'rr', 'rs', 'rsb', 'rss', 'rts', 's4m',
                   'sbf', 'sc3', 'sct', 'scx', 'sdf', 'sdt', 'sdt', 'sequence', 'sga', 'sh4', 'sks', 'sl', 'slf', 'slv',
                   'snd', 'spa', 'spk', 'spr', 'st3', 'stb', 'stg', 'str', 'sud', 'sue', 'swa', 'syb', 'syj', 't24',
                   'tbf', 'tdu', 'ted', 'tf', 'thu', 'trc', 'twd', 'twt', 'txd', 'ucx', 'ugx', 'uka', 'ukx', 'unr',
                   'uvx', 'vdu', 'vid', 'viv', 'vmp', 'vol', 'vpp', 'vtf', 'wd', 'wdt', 'wep', 'whd', 'wtn', 'xcr',
                   'xfs', 'xmb', 'xpk', 'xti', 'xwb'),
              'total_observer':
                  ('S2MA', 'SC2', 'bsp', 'cache', 'cue', 'eml', 'etc', 'gcf', 'hdr', 'isz', 'mdf', 'mds', 'mht', 'mhtml',
                   'mim', 'mime', 'mpq', 'mpqe', 'msm', 'nrg', 'pbb', 'pst', 'tbb', 'udf', 'vbsp', 'vp', 'vpk', 'xzp'),
              'sau':
                  ('4pp', 'bdx', 'box', 'brig', 'c', 'cam', 'cc', 'chr', 'dbi', 'df2', 'epf', 'fan', 'flx', 'gor',
                   'group', 'hrs', 'ilb', 'jun', 'jus', 'key', 'lbx', 'maa', 'mul', 'nds', 'p00', 'p10', 'p99', 'rm',
                   'tgw', 'tlb', 'uop', 'vsr', 'war', 'wdb', 'xua', 'xub'),
              'seven_zip':
                  ('7z', 'apk', 'arj', 'bz', 'bz2', 'bza', 'bzip', 'cab', 'cb7', 'cb7z', 'cbr', 'cbt', 'cbz', 'chm',
                   'cpio', 'dazip', 'deb', 'dgdat', 'dll', 'dmg', 'docx', 'dotx', 'epub', 'exe', 'fods', 'fodt',
                   'gadget', 'gog', 'gro', 'gz', 'gz2', 'gzip', 'hfs', 'ipa', 'ipg', 'iso', 'jar', 'kfs', 'lha', 'love',
                   'lp', 'lzh', 'lzm', 'lzma', 'msi', 'nob', 'obb', 'ocx', 'odb', 'ods', 'odt', 'ots', 'ott', 'pgz',
                   'piz', 'pk3', 'pk4', 'potm', 'ppsx', 'pptx', 'rar', 'rpm', 'squashfs', 'swm', 'tar', 'taz', 'tbz',
                   'tbz2', 'tgz', 'tgz2', 'tpz', 'txtz', 'txz', 'unitypackage', 'vhd', 'wim', 'xap', 'xar', 'xlsm',
                   'xlsx', 'xpi', 'xz', 'z', 'zip'),
              'unreal':
                  ('pcc', 'u', 'uax', 'ugx', 'umx', 'un2', 'unr', 'upk', 'upx', 'usa', 'usx', 'ut2', 'utx', 'uvx',
                   'xxx'),
              'rpg_maker':
                  ('rgss2a', 'rgss3a', 'rgssad', 'rpgmvm', 'rpgmvo', 'rpgmvp'),
              'bethesda':
                  ('ba2', 'bsa', 'esl', 'esm', 'esp', 'esx', 'pex'),
              'id_tech':
                  ('bimage', 'idwav', 'index', 'mega2', 'msf', 'pages', 'ptr', 'resources', 'streamed', 'vmtr', 'wad',
                   'wl6', 'xma', 'xpr'),
              'x-ray':
                  ('db0', 'db1', 'db2', 'db3', 'db4', 'db5', 'db6', 'db7', 'db8', 'db9'),
              'video':
                  ('3g2', '3gp', '3gp2', '3gpp', 'amv', 'avi', 'divx', 'dvr-ms', 'f4v', 'flc', 'fli', 'flic', 'flv',
                   'm1v', 'm2v', 'm4v', 'mk3d', 'mkv', 'mov', 'mpeg', 'mpg', 'mve', 'ogm', 'ogv', 'pam', 'pmf', 'pmm',
                   'pss', 'rm', 'thp', 'ts', 'vid', 'vob', 'webm', 'wmv', 'xvid')
              }
