
class GetExt:
    
    @staticmethod
    def get_ext(index: bytes) -> str:
        ext_list = {
            # Image Formats
            b'DDS ': 'dds', 
            b'\x89PNG': 'png', 
            b'GIF8': 'gif', 
            b'\xFF\xD8\xFF\xE0': 'jpg', 
            b'\xFF\xD8\xFF\xDB': 'jpg', 
            b'\xFF\xD8\xFF\xEE': 'jpg', 
            b'\xFF\xD8\xFF\xE1': 'jpg', 
            b'\xFF\xD8\xFF\x51': 'jp2', 
            b'\0\0\x02\0': 'tga', 
            b'\0\0\x0a\0': 'tga',
            b'\0\0\x01\0': 'ico',
            b'icns': 'icns',
            b'II*\0': 'tiff',
            b'MM\0*': 'tiff',
            b'II+\0': 'tiff',
            b'MM\0+': 'tiff',
            b'\x80*_\xD7': 'cin',
            b'SDPX': 'dpx',
            b'XPDS': 'dpx',
            b'v/1\x01': 'exr',
            b'BPG\xFB': 'bpg',
            b'\0\0\0\x0C': 'jp2',
            b'qoif': 'qoi',
            b'FORM': 'iff',
            b'%!PS': 'eps',
            b'8BPS': 'psd',
            b'FLIF': 'flif',
            b'DICM': 'dcm',
            b'gimp': 'xcf',
            b'#?RA': 'hdr',
            b'KTX ': 'ktx',
            b'TEX\0': 'tex',
            b'\0XET': 'tex',
            b'GXT\0': 'gxt',
            b'\0TXG': 'gxt',
            b'TIM2': 'tm2',

            # Audio Formats
            b'RIFF': 'wav', 
            b'RIFX': 'wav', 
            b'OggS': 'ogg', 
            b'fLaC': 'flac', 
            b'MThd': 'midi', 
            b'Crea': 'voc', 
            b'.snd': 'snd', 
            b'#!AM': 'amr', 
            b'#!SI': 'sil', 

            # Archive Formats
            b'PK\x03\x04': 'zip', 
            b'PK\x05\x06': 'zip', 
            b'PK\x07\x08': 'zip', 
            b'7z\xBC\xAF': '7z',
            b'-lh0': 'lzh',
            b'-lh5': 'lzh',
            b'LZIP': 'lz',
            b'0707': 'cpio',
            b'Rar!': 'rar',
            b'usta': 'tar',
            b'\xFD7zX': 'xz',
            b'\x04\x22\x4D\x18': 'lz4',
            b'MSCF': 'cab',
            b'bvx2': 'lzfse',
            b'\x28\xB5\x2F\xFD': 'xst',
            b'RSVK': 'rs',
            b'**AC': 'ace',

            # Disc images and roms
            b'CD00': 'iso',
            b'NES\x1A': 'nes',
            b'IsZ!': 'isz',
            b'MSWI': 'wim',
            b'\x0DNer': 'nri',

            # Document formats
            b'%PDF': 'pdf', 
            b'<?xm': 'xml', 
            b'\x3C\0\x3F\0': 'xml', 
            b'\0\x3C\0\x3F': 'xml', 
            b'\x3C\0\0\0': 'xml', 
            b'\0\0\0\x3C': 'xml', 
            b'\x4C\x6F\xA7\x94': 'xml', 
            b'{\n  ': 'json', 
            b'ITSF': 'chm', 
            b'AT&T': 'djvu', 
            b'----': 'crt', 
            b'{\\rt': 'rtf', 

            # Video formats
            b'BIKi': 'bik',
            b'BIKb': 'bik', 
            b'SMK2': 'smk', 
            b'BIK2': 'bk2', 
            b'\0\0\x01\xBA': 'mpeg',
            b'\0\0\x01\xB3': 'mpeg',
            b'ftyp': 'mp4',
            b'\x1A\x45\xDF\xA3': 'mkv',

            # 3D formats
            b'BLEN': 'blend', 
            b'STLB': 'stl', 
            b'Kayd': 'fbx', 
            b'ply\x0A': 'ply', 
            b'glTF': 'glb',
            b'DRAC': 'drc',
            b'MDL\0': 'mdl',

            # Programs, installers and executables
            b'MZ\x90\x00': 'exe', 
            b'\xCB\x0D\x0D\x0A': 'pyc', 
            b'\x7fELF': 'elf', 
            b'PE\x00\x00': 'dll', 
            b'LuaQ': 'luac',
            b'\x1BLua': 'luac',
            b'\xCA\xFE\xBA\xBE': 'class',
            b'koly': 'dmg',
            b'!<ar': 'deb',
            b'<rob': 'rbxl',
            b'ISc(': 'cab',

            # Data Bases
            b'SQLi': 'db',
            b'\x0D\xF0\x1D\xC0': 'cdb',
            b'DUCK': 'duckdb',

            # Fonts
            b'\0\1\0\0': 'ttf',
            b'OTTO': 'otf',

            # Playlists
            b'#EXT': 'm3u',

            # Game files
            b'-==-': 'utoc',
            b'exte': 'gd'

        }

        if index[:2] in (b'\x08\x1D', b'\x08\x5B', b'\x08\x99', b'\x08\xD7', b'\x18\x19', b'\x18\x57', b'\x18\x95', b'\x18\xD3', 
                         b'\x28\x15', b'\x28\x53', b'\x28\x91', b'\x28\xCF', b'\x38\x11', b'\x38\x4F', b'\x38\x8D', b'\x38\xCB', 
                         b'\x48\x0D', b'\x48\x4B', b'\x48\x89', b'\x48\xC7', b'\x58\x09', b'\x58\x47', b'\x58\x85', b'\x58\xC3', 
                         b'\x68\x05', b'\x68\x43', b'\x68\x81', b'\x68\xDE', b'\x78\x01', b'\x78\x5E', b'\x78\x9C', b'\x78\xDA' 
                         b'\x78\x20', b'\x78\x7D', b'\x78\xBB', b'\x78\xF9', ):
            return 'zlib'
        
        if index[:2] == b'\x1F\x8B':
            return 'gzip'
        
        if index[:3] in (b'CWS', b'FWS'):
            return 'swf'
        
        if index[:3] in (b'\xEF\xBB\xBF', b'\x0E\xFE\xFF'):
            return 'txt'
        
        if index[:2] in (b'\xFF\xFE', b'\xFE\xFF'):
            return 'txt'
        
        if index[:3] in (b'\xFF\xFB', b'\xFF\xF2', b'\xFF\xF3'):
            return 'mp3'
        
        if index[:3] == b'BZh':
            return 'bz2'
        
        if index[:3] == b'\x8C\x0A\x00':
            return 'ucas'
        
        if index[:3] == b'FLV':
            return 'flv'
        
        if index[:3] == b'ID3':
            return 'mp3'
        
        if index[:3] == b'NES':
            return 'nes'
        
        if index[:2] == b'BM':
            return 'bmp'

        index_rev = index[::-1]
        res = ext_list.get(index, None)
        res_rev = ext_list.get(index_rev, None)
        
        if res:
            return res
        elif res_rev:
            return res_rev  
        else:

            if index[0] == 0:
                index = index_rev

            try:
                ext = index[:3].decode('utf-8').lower()
            except UnicodeDecodeError:
                return 'dat'
            
            white_list = 'abcdefghijklmnopqrstuvwxyz0123456789'

            for s in ext:

                if s not in white_list:
                    ext = 'dat'
                    break

            return ext
