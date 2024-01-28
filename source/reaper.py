import threading
from datetime import datetime
import os
from subprocess import Popen

from PyQt6.QtCore import QThread, pyqtSignal
from abc import abstractmethod
from source.ui import localize

DEBUG = True


def file_reaper(func_name):

    def wrapper(*args, **kwargs):
        error = None
        function = str(func_name).split(" ")[1]
        start = datetime.now()

        if DEBUG:
            func_name(*args, **kwargs)
        else:
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
        super().__init__()
        self.file_name = ''
        self.output_folder = ''
        self.unpack = True
        self.path_to_root = os.path.abspath(__file__).split('source')[0]
        self.update_signal.emit(0, '', '', False)

    @file_reaper
    @abstractmethod
    def run(self):
        pass

    def unzip(self, f_name: str, c_num=1, get_ext=False, test=False,
              encrypt=False, crypt_method='', crypt_key=''):

        if encrypt:
            # TODO: Need tests
            dump_name = crypt_method + '_enc.dmp'
            script = (f'"{self.path_to_root}data/QuickBMS/quickbms.exe" '
                      f'-o -a "{crypt_method}{" " + crypt_key if crypt_key else ""}" '
                      f'"{self.path_to_root}data/QuickBMS/encryption_scan.bms")" '
                      f'"{f_name}" "{self.output_folder}"').replace("/", "\\")
        else:
            dump_name = self.zip_methods[c_num] + '.dmp'
            script = (f'"{self.path_to_root}data/QuickBMS/quickbms.exe" -o -a "{c_num}" '
                      f'"{self.path_to_root}data/QuickBMS/comtype_scan2.bms" '
                      f'"{f_name}" "{self.output_folder}"').replace("/", "\\")

        if not test:

            Popen(script).wait()
            dump_file = os.path.join(self.output_folder, dump_name)

            with open(dump_file, 'rb') as dmp:
                unzip_data = dmp.read()

            os.remove(f_name)

            if get_ext:
                new_ext = self.get_ext(unzip_data[:4])
                f_name = f_name.replace('dat', new_ext)

            with open(f_name, 'wb') as out_f:
                out_f.write(unzip_data)

        else:
            proc = Popen(script)
            threading.Timer(10, proc.terminate).start()
            proc.wait()

    @file_reaper
    def zip_scan(self, f_name):

        for i in self.zip_methods.keys():
            self.unzip(f_name=f_name, c_num=i, test=True)

    @staticmethod
    def get_ext(index: bytes):
        ext_list = {b'RIFF': 'wav', b'RIFX': 'wav', b'DDS\x20': 'dds'}

        try:
            return ext_list[index]
        except (IndexError, KeyError):

            try:
                return index[:3].decode('utf-8').lower()
            except UnicodeDecodeError:
                return 'dat'

    zip_methods = {1: "ZLIB", 2: "DEFLATE", 3: "LZO1", 4: "LZO1A", 5: "LZO1B", 6: "LZO1C", 7: "LZO1F", 8: "LZO1X",
                   9: "LZO1Y", 10: "LZO1Z", 11: "LZO2A", 12: "LZSS", 13: "LZX", 14: "GZIP", 15: "EXPLODE",
                   16: "LZMA", 17: "LZMA_86HEAD", 18: "LZMA_86DEC", 19: "LZMA_86DECHEAD", 20: "LZMA_EFS",
                   21: "BZIP2", 22: "XMEMLZX", 23: "HEX", 24: "BASE64", 25: "UUENCODE", 26: "ASCII85", 27: "YENC",
                   28: "UNLZW", 29: "UNLZWX", 30: "LZXCAB", 31: "LZXCHM", 32: "RLEW", 33: "LZJB", 34: "SFL_BLOCK",
                   35: "SFL_RLE", 36: "SFL_NULLS", 37: "SFL_BITS", 38: "LZMA2", 39: "LZMA2_86HEAD",
                   40: "LZMA2_86DEC", 41: "LZMA2_86DECHEAD", 42: "NRV2b", 43: "NRV2d", 44: "NRV2e", 45: "HUFFBOH",
                   46: "UNCOMPRESS", 47: "DMC", 48: "LZH", 49: "LZARI", 50: "TONY", 51: "RLE7", 52: "RLE0",
                   53: "RLE", 54: "RLEA", 55: "BPE", 56: "QUICKLZ", 57: "Q3HUFF", 58: "UNMENG", 59: "LZ2K",
                   60: "DARKSECTOR", 61: "MSZH", 62: "UN49G", 63: "UNTHANDOR", 64: "DOOMHUFF", 65: "APLIB",
                   66: "TZAR_LZSS", 67: "LZF", 68: "CLZ77", 69: "LZRW1", 70: "DHUFF", 71: "FIN", 72: "LZAH",
                   73: "LZH12", 74: "LZH13", 75: "GRZIP", 76: "CKRLE", 77: "QUAD", 78: "BALZ", 79: "DEFLATE64",
                   80: "SHRINK", 81: "PPMDI", 82: "MULTIBASE", 83: "BRIEFLZ", 84: "PAQ6", 85: "SHCODEC",
                   86: "HSTEST1", 87: "HSTEST2", 88: "SIXPACK", 89: "ASHFORD", 90: "JCALG", 91: "JAM", 92: "LZHLIB",
                   93: "SRANK", 94: "ZZIP", 95: "SCPACK", 96: "RLE3", 97: "BPE2", 98: "BCL_HUF", 99: "BCL_LZ",
                   100: "BCL_RICE", 101: "BCL_RLE", 102: "BCL_SF", 103: "SCZ", 104: "SZIP", 105: "PPMDI_RAW",
                   106: "PPMDG", 107: "PPMDG_RAW", 108: "PPMDJ", 109: "PPMDJ_RAW", 110: "SR3C", 111: "HUFFMANLIB",
                   112: "SFASTPACKER", 113: "SFASTPACKER2", 114: "DK2", 115: "LZ77WII", 116: "LZ77WII_RAW10",
                   117: "DARKSTONE", 118: "SFL_BLOCK_CHUNKED", 119: "YUKE_BPE", 120: "STALKER_LZA", 121: "PRS_8ING",
                   122: "PUYO_CNX", 123: "PUYO_CXLZ", 124: "PUYO_LZ00", 125: "PUYO_LZ01", 126: "PUYO_LZSS",
                   127: "PUYO_ONZ", 128: "PUYO_PRS", 129: "FALCOM", 130: "CPK", 131: "BZIP2_FILE",
                   132: "LZ77WII_RAW11", 133: "LZ77WII_RAW30", 134: "LZ77WII_RAW20", 135: "PGLZ", 136: "SLZ",
                   137: "SLZ_01", 138: "SLZ_02", 139: "LZHL", 140: "D3101", 141: "SQUEEZE", 142: "LZRW3",
                   143: "TDCB_ahuff", 144: "TDCB_arith", 145: "TDCB_arith1", 146: "TDCB_arith1e",
                   147: "TDCB_arithn", 148: "TDCB_compand", 149: "TDCB_huff", 150: "TDCB_lzss", 151: "TDCB_lzw12",
                   152: "TDCB_lzw15v", 153: "TDCB_silence", 154: "RDC", 155: "ILZR", 156: "DMC2", 157: "diffcomp",
                   158: "LZR", 159: "LZS", 160: "LZS_BIG", 161: "COPY", 162: "MOHLZSS", 163: "MOHRLE", 164: "YAZ0",
                   165: "BYTE2HEX", 166: "UN434A", 167: "UNZIP_DYNAMIC", 168: "XXENCODE", 169: "GZPACK",
                   170: "ZLIB_NOERROR", 171: "DEFLATE_NOERROR", 172: "PPMDH", 173: "PPMDH_RAW", 174: "RNC",
                   175: "RNC_RAW", 176: "FITD", 177: "KENS_Nemesis", 178: "KENS_Kosinski",
                   179: "KENS_Kosinski_moduled", 180: "KENS_Enigma", 181: "KENS_Saxman", 182: "DRAGONBALLZ",
                   183: "NITROSDK", 184: "ZDAEMON", 185: "SKULLTAG", 186: "MSF", 187: "STARGUNNER",
                   188: "NTCOMPRESS", 189: "CRLE", 190: "CTW", 191: "DACT_DELTA", 192: "DACT_MZLIB2",
                   193: "DACT_MZLIB", 194: "DACT_RLE", 195: "DACT_SNIBBLE", 196: "DACT_TEXT", 197: "DACT_TEXTRLE",
                   198: "EXECUTE", 199: "LZ77_0", 200: "LZBSS", 201: "BPAQ0", 202: "LZPX", 203: "MAR_RLE",
                   204: "GDCM_RLE", 205: "LZMAT", 206: "DICT", 207: "REP", 208: "LZP", 209: "ELIAS_DELTA",
                   210: "ELIAS_GAMMA", 211: "ELIAS_OMEGA", 212: "PACKBITS", 213: "DARKSECTOR_NOCHUNKS", 214: "ENET",
                   215: "EDUKE32", 216: "XU4_RLE", 217: "RVL", 218: "LZFU", 219: "LZFU_RAW", 220: "XU4_LZW",
                   221: "HE3", 222: "IRIS", 223: "IRIS_HUFFMAN", 224: "IRIS_UO_HUFFMAN", 225: "NTFS", 226: "PDB",
                   227: "COMPRLIB_SPREAD", 228: "COMPRLIB_RLE1", 229: "COMPRLIB_RLE2", 230: "COMPRLIB_RLE3",
                   231: "COMPRLIB_RLE4", 232: "COMPRLIB_ARITH", 233: "COMPRLIB_SPLAY", 234: "CABEXTRACT",
                   235: "MRCI", 236: "HD2_01", 237: "HD2_08", 238: "HD2_01raw", 239: "RTL_LZNT1", 240: "RTL_XPRESS",
                   241: "RTL_XPRESS_HUFF", 242: "PRS", 243: "SEGA_LZ77", 244: "SAINT_SEYA", 245: "NTCOMPRESS30",
                   246: "NTCOMPRESS40", 247: "SLZ_03", 248: "YAKUZA", 249: "LZ4", 250: "SNAPPY", 251: "LUNAR_LZ1",
                   252: "LUNAR_LZ2", 253: "LUNAR_LZ3", 254: "LUNAR_LZ4", 255: "LUNAR_LZ5", 256: "LUNAR_LZ6",
                   257: "LUNAR_LZ7", 258: "LUNAR_LZ8", 259: "LUNAR_LZ9", 260: "LUNAR_LZ10", 261: "LUNAR_LZ11",
                   262: "LUNAR_LZ12", 263: "LUNAR_LZ13", 264: "LUNAR_LZ14", 265: "LUNAR_LZ15", 266: "LUNAR_LZ16",
                   267: "LUNAR_RLE1", 268: "LUNAR_RLE2", 269: "LUNAR_RLE3", 270: "LUNAR_RLE4", 271: "GOLDENSUN",
                   272: "LUMINOUSARC", 273: "LZV1", 274: "FASTLZAH", 275: "ZAX", 276: "SHRINKER",
                   277: "MMINI_HUFFMAN", 278: "MMINI_LZ1", 279: "MMINI", 280: "CLZW", 281: "LZHAM", 282: "LPAQ8",
                   283: "SEGA_LZS2", 284: "CALLDLL", 285: "WOLF", 286: "COREONLINE", 287: "MSZIP", 288: "QTM",
                   289: "MSLZSS", 290: "MSLZSS1", 291: "MSLZSS2", 292: "KWAJ", 293: "LZLIB", 294: "DFLT",
                   295: "LZMA_DYNAMIC", 296: "LZMA2_DYNAMIC", 297: "LZMA2_EFS", 298: "LZXCAB_DELTA",
                   299: "LZXCHM_DELTA", 300: "FFCE", 301: "SCUMMVM4", 302: "SCUMMVM5", 303: "SCUMMVM6",
                   304: "SCUMMVM7", 305: "SCUMMVM8", 306: "SCUMMVM9", 307: "SCUMMVM10", 308: "SCUMMVM11",
                   309: "SCUMMVM12", 310: "SCUMMVM13", 311: "SCUMMVM14", 312: "SCUMMVM15", 313: "SCUMMVM16",
                   314: "SCUMMVM17", 315: "SCUMMVM18", 316: "SCUMMVM19", 317: "SCUMMVM20", 318: "SCUMMVM21",
                   319: "SCUMMVM22", 320: "SCUMMVM23", 321: "SCUMMVM24", 322: "SCUMMVM25", 323: "SCUMMVM26",
                   324: "SCUMMVM27", 325: "SCUMMVM28", 326: "SCUMMVM29", 327: "SCUMMVM30", 328: "SCUMMVM31",
                   329: "SCUMMVM32", 330: "SCUMMVM33", 331: "SCUMMVM34", 332: "SCUMMVM35", 333: "SCUMMVM36",
                   334: "SCUMMVM37", 335: "SCUMMVM38", 336: "SCUMMVM39", 337: "SCUMMVM40", 338: "SCUMMVM41",
                   339: "SCUMMVM42", 340: "SCUMMVM43", 341: "SCUMMVM44", 342: "SCUMMVM45", 343: "SCUMMVM46",
                   344: "SCUMMVM47", 345: "SCUMMVM48", 346: "SCUMMVM49", 347: "SCUMMVM50", 348: "SCUMMVM51",
                   349: "SCUMMVM52", 350: "SCUMMVM53", 351: "LZS_UNZIP", 352: "LEGEND_OF_MANA", 353: "DIZZY",
                   354: "EDL1", 355: "EDL2", 356: "DUNGEON_KID", 357: "LUNAR_LZ17", 358: "LUNAR_LZ18",
                   359: "FRONTMISSION2", 360: "RLEINC1", 361: "RLEINC2", 362: "EVOLUTION", 363: "PUYO_LZ10",
                   364: "PUYO_LZ11", 365: "NISLZS", 366: "UNKNOWN1", 367: "UNKNOWN2", 368: "UNKNOWN3",
                   369: "UNKNOWN4", 370: "UNKNOWN5", 371: "UNKNOWN6", 372: "UNKNOWN7", 373: "UNKNOWN8",
                   374: "UNKNOWN9", 375: "UNKNOWN10", 376: "UNKNOWN11", 377: "UNKNOWN12", 378: "UNKNOWN13",
                   379: "UNKNOWN14", 380: "UNKNOWN15", 381: "UNKNOWN16", 382: "UNKNOWN17", 383: "UNKNOWN18",
                   384: "UNKNOWN19", 385: "BLACKDESERT", 386: "BLACKDESERT_RAW", 387: "PUCRUNCH", 388: "ZPAQ",
                   389: "ZYXEL_LZS", 390: "BLOSC", 391: "GIPFELI", 392: "CRUSH", 393: "YAPPY", 394: "LZG",
                   395: "DOBOZ", 396: "TORNADO", 397: "XPKSQSH", 398: "AMIGA_UNSQUASH", 399: "AMIGA_BYTEKILLER",
                   400: "AMIGA_FLASHSPEED", 401: "AMIGA_IAMICE", 402: "AMIGA_IAMATM", 403: "AMIGA_ISC1P",
                   404: "AMIGA_ISC2P", 405: "AMIGA_ISC3P", 406: "AMIGA_UPCOMP", 407: "AMIGA_UPHD",
                   408: "AMIGA_BYTEKILLER3", 409: "AMIGA_BYTEKILLER2", 410: "AMIGA_CRUNCHMANIA17b",
                   411: "AMIGA_POWERPACKER", 412: "AMIGA_STONECRACKER2", 413: "AMIGA_STONECRACKER3",
                   414: "AMIGA_STONECRACKER4", 415: "AMIGA_CRUNCHMASTER", 416: "AMIGA_CRUNCHMANIA",
                   417: "AMIGA_CRUNCHMANIAh", 418: "AMIGA_CRUNCHOMATIC", 419: "AMIGA_DISCOVERY",
                   420: "AMIGA_LIGHTPACK", 421: "AMIGA_MASTERCRUNCHER", 422: "AMIGA_MAXPACKER",
                   423: "AMIGA_MEGACRUNCHER", 424: "AMIGA_PACKIT", 425: "AMIGA_SPIKECRUNCHER",
                   426: "AMIGA_TETRAPACK", 427: "AMIGA_TIMEDECRUNCH", 428: "AMIGA_TRYIT", 429: "AMIGA_TUC",
                   430: "AMIGA_TURBOSQUEEZER61", 431: "AMIGA_TURBOSQUEEZER80", 432: "AMIGA_TURTLESMASHER",
                   433: "AMIGA_DMS", 434: "AMIGA_PACKFIRE", 435: "ALBA_BPE", 436: "ALBA_BPE2", 437: "FLZP",
                   438: "SR2", 439: "SR3", 440: "BPE2v3", 441: "BPE_ALT1", 442: "BPE_ALT2", 443: "CBPE",
                   444: "SCPACK0", 445: "LZMA_0", 446: "LZMA_86HEAD0", 447: "LZMA_86DEC0", 448: "LZMA_86DECHEAD0",
                   449: "LZMA_EFS0", 450: "LZMA2_0", 451: "LZMA2_86HEAD0", 452: "LZMA2_86DEC0",
                   453: "LZMA2_86DECHEAD0", 454: "LZMA2_EFS0", 455: "LZOVL", 456: "NITROSDK_DIFF8",
                   457: "NITROSDK_DIFF16", 458: "NITROSDK_HUFF8", 459: "NITROSDK_HUFF16", 460: "NITROSDK_LZ",
                   461: "NITROSDK_RL", 462: "QCMP", 463: "SPARSE", 464: "STORMHUFF", 465: "GZIP_STRICT",
                   466: "CT_HughesTransform", 467: "CT_LZ77", 468: "CT_ELSCoder", 469: "CT_RefPack", 470: "QFS",
                   471: "PXP", 472: "BOH", 473: "GRC", 474: "ZEN", 475: "LZHUFXR", 476: "FSE", 477: "FSE_RLE",
                   478: "ZSTD", 479: "CSC", 480: "RNCb", 481: "RNCb_RAW", 482: "RNCc_RAW", 483: "AZO", 484: "PP20",
                   485: "DS_BLZ", 486: "DS_HUF", 487: "DS_LZE", 488: "DS_LZS", 489: "DS_LZX", 490: "DS_RLE",
                   491: "FAB", 492: "LZ4F", 493: "PCLZFG", 494: "LZOO", 495: "DELZC", 496: "DEHUFF",
                   497: "HEATSHRINK", 498: "NEPTUNIA", 499: "SMAZ", 500: "LZFX", 501: "PITHY", 502: "ZLING",
                   503: "DENSITY", 504: "BROTLI", 505: "RLE32", 506: "RLE35", 507: "BSC", 508: "SHOCO",
                   509: "WFLZ", 510: "FASTARI", 511: "RLE_ORCOM", 512: "DICKY", 513: "SQUISH", 514: "LZNT1",
                   515: "XPRESS", 516: "XPRESS_HUFF", 517: "LZJODY", 518: "TRLE", 519: "SRLE", 520: "MRLE",
                   521: "LUNAR_LZ19", 522: "JCH", 523: "LZRW1KH", 524: "LZSS0", 525: "LHA_lz5", 526: "LHA_lzs",
                   527: "LHA_lh1", 528: "LHA_lh4", 529: "LHA_lh5", 530: "LHA_lh6", 531: "LHA_lh7", 532: "LHA_lhx",
                   533: "LHA_pm1", 534: "LHA_pm2", 535: "SQX1", 536: "MDIP_ARAD", 537: "MDIP_ARST",
                   538: "MDIP_DELTA", 539: "MDIP_FREQ", 540: "MDIP_HUFFMAN", 541: "MDIP_CANONICAL",
                   542: "MDIP_LZSS", 543: "MDIP_LZW", 544: "MDIP_RICE", 545: "MDIP_RLE", 546: "MDIP_VPACKBITS",
                   547: "BIZARRE", 548: "BIZARRE_SKIP", 549: "LZSSX", 550: "ASH", 551: "YAY0", 552: "DSTACKER",
                   553: "DSTACKER_SD3", 554: "DSTACKER_SD4", 555: "DBLSPACE", 556: "DBLSPACE_JM", 557: "XREFPACK",
                   558: "XREFPACK0", 559: "QCMP2", 560: "DEFLATEX", 561: "ZLIBX", 562: "LZRW1a", 563: "LZRW2",
                   564: "LZRW3a", 565: "LZRW5", 566: "LEGO_IXS", 567: "MCOMP", 568: "MCOMP0", 569: "MCOMP1",
                   570: "MCOMP2", 571: "MCOMP3", 572: "MCOMP4", 573: "MCOMP5", 574: "MCOMP6", 575: "MCOMP7",
                   576: "MCOMP8", 577: "MCOMP9", 578: "MCOMP10", 579: "MCOMP13", 580: "MCOMP14", 581: "MCOMP15",
                   582: "MCOMP16", 583: "MCOMP17", 584: "IROLZ", 585: "IROLZ2", 586: "UCLPACK", 587: "ACE",
                   588: "EA_COMP", 589: "EA_HUFF", 590: "EA_JDLZ", 591: "TORNADO_BYTE", 592: "TORNADO_BIT",
                   593: "TORNADO_HUF", 594: "TORNADO_ARI", 595: "LBALZSS1", 596: "LBALZSS2", 597: "DBPF",
                   598: "TITUS_LZW", 599: "TITUS_HUFFMAN", 600: "KB_LZW", 601: "KB_DOSLZW", 602: "CARMACK",
                   603: "MBASH", 604: "DDAVE", 605: "GOT", 606: "SKYROADS", 607: "ZONE66", 608: "EXEPACK",
                   609: "DE_LZW", 610: "JJRLE", 611: "K13RLE", 612: "SFRLC", 613: "WESTWOOD1", 614: "WESTWOOD3",
                   615: "WESTWOOD3b", 616: "WESTWOOD40", 617: "WESTWOOD80", 618: "PKWARE_DCL", 619: "TERSE",
                   620: "TERSE_SPACK_RAW", 621: "TERSE_PACK_RAW", 622: "REDUCE1", 623: "REDUCE2", 624: "REDUCE3",
                   625: "REDUCE4", 626: "LZW_ENGINE", 627: "LZW_BASH", 628: "LZW_EPFS", 629: "LZW_STELLAR7",
                   630: "ULTIMA6", 631: "LZ5", 632: "LZ5F", 633: "YALZ77", 634: "LZKN1", 635: "LZKN2",
                   636: "LZKN3", 637: "TFLZSS", 638: "SYNLZ1", 639: "SYNLZ1b", 640: "SYNLZ1partial", 641: "SYNLZ2",
                   642: "PPMZ2", 643: "OPENDARK", 644: "DSLZSS", 645: "KOF", 646: "KOF1", 647: "RFPK",
                   648: "WP16", 649: "LZ4_STREAM", 650: "OODLE", 651: "OODLE_LZH", 652: "OODLE_LZHLW",
                   653: "OODLE_LZNIB", 654: "OODLE_LZB16", 655: "OODLE_LZBLW", 656: "OODLE_LZNA",
                   657: "OODLE_BitKnit", 658: "OODLE_LZA", 659: "OODLE_LZQ1", 660: "OODLE_LZNIB2", 661: "SEGS",
                   662: "OODLE_Selkie", 663: "OODLE_Akkorokamui", 664: "ALZ", 665: "REVELATION_ONLINE",
                   666: "PS_LZ77", 667: "LZFSE", 668: "ZLE", 669: "KOF2", 670: "KOF3", 671: "HSQ", 672: "FACT5LZ",
                   673: "LZCAPTSU", 674: "TF3_RLE", 675: "WINIMPLODE", 676: "DZIP", 677: "DZIP_COMBUF",
                   678: "LBALZSS1X", 679: "LBALZSS2X", 680: "GHIREN", 681: "FALCOM_DIN", 682: "FALCOM_DIN1",
                   683: "FALCOM_DIN0", 684: "FALCOM_DINX", 685: "GLZA", 686: "M99CODER", 687: "LZ4X", 688: "TAIKO",
                   689: "LZ77EA_970", 690: "DRV3_SRD", 691: "RECET", 692: "LIZARD", 693: "MICROVISION",
                   694: "DR12AE", 695: "MSPACK", 696: "KONAMIAC", 697: "WOLF0", 698: "ARTSTATION", 699: "LEVEL5",
                   700: "ZENPXP", 701: "ZENPXP1", 702: "ZENPXP2", 703: "ZENPXP34", 704: "ZENPXPde", 705: "LIBLZS",
                   706: "SHREK", 707: "EA_MADDEN", 708: "NVCACHE", 709: "DE_HTML", 710: "HTML_EASY",
                   711: "JSON_VIEWER", 712: "XML_JSON_PARSER", 713: "OodleNetwork1UDP_State_Uncompact",
                   714: "OodleNetwork1_Shared_SetWindow", 715: "OodleNetwork1UDP_Decode",
                   716: "OodleNetwork1UDP_Encode", 717: "QCMP1", 718: "YKCMP", 719: "LZWAB", 720: "NCOMPRESS",
                   721: "SWZAP", 722: "MZX", 723: "LZRRV", 724: "BCM", 725: "ULZ", 726: "SLZ_ROF", 727: "LZ4X_NEW",
                   728: "COPY2", 729: "SLZ_03b", 730: "MPPC", 731: "MPPC_BIG", 732: "ALZSS", 733: "CLZ", 734: "GTC",
                   735: "ANCO", 736: "ANCO0", 737: "ANCO1", 738: "ANCO2", 739: "ANCO3", 740: "ANCO4", 741: "ANCO5",
                   742: "konami_lz77", 743: "vct_lzs", 744: "umesoft", 745: "systemaqua_catf", 746: "sogna",
                   747: "pac_ads", 748: "ail_lzs", 749: "agsi", 750: "foster_fa2", 751: "an21", 752: "arc_link",
                   753: "maika_bk", 754: "maika_mk2", 755: "propeller_mgr", 756: "qlie", 757: "avg32_seen",
                   758: "sas5_iar", 759: "seraphim_scn", 760: "ugos_det", 761: "aaru_fl4", 762: "inspire_ida",
                   763: "kurumi_mpk", 764: "dice_rlz", 765: "pulltop", 766: "vnsystem", 767: "QlzUnpack",
                   768: "umesoft_pk", 769: "tomcat_tcd", 770: "tail_pren", 771: "tail_crp0", 772: "tail_hp",
                   773: "tactics_arc", 774: "sviu_pkz", 775: "nekox_gpc", 776: "rec_arc", 777: "warc",
                   778: "warc10", 779: "warc_ylz", 780: "warc_huff", 781: "sh_him", 782: "pandora_pbx",
                   783: "origin_lz", 784: "origin_huffman", 785: "origin_rle", 786: "origin_alphav2",
                   787: "garbro_huffman", 788: "ankh_grp", 789: "ankh_hdj", 790: "caramelbox_arc3",
                   791: "caramelbox_arc4", 792: "circus_V1", 793: "circus_V2", 794: "circus_V3", 795: "cmvs_cpz",
                   796: "daisystem_pac", 797: "ethornell_bgi", 798: "fc01_mrg", 799: "fc01_mrg_quant",
                   800: "fc01_pak_lz", 801: "favorite_lzw", 802: "frontwing_rle", 803: "frontwing_huffman",
                   804: "g2_gcex", 805: "gss_arc", 806: "hypatia_mariel", 807: "interheart_fpk", 808: "kaguya_ari",
                   809: "kaguya_lin2", 810: "kaguya_link", 811: "kaguya_uf", 812: "kid_dat", 813: "lambda_lax",
                   814: "microvision_arc", 815: "moonhir_fpk", 816: "spack", 817: "azsys", 818: "dxlib",
                   819: "glibg", 820: "gamesystem_cmp", 821: "puremail", 822: "groover_pcg", 823: "mnp_mma",
                   824: "strikes_pck", 825: "SEGA_LZ77X", 826: "NEPTUNIA0", 827: "puff8", 828: "lzh8",
                   829: "romchu", 830: "okage", 831: "lzsd_of", 832: "lzsd_gfd", 833: "lzsd_gba2", 834: "pzz",
                   835: "SL01", 836: "rage_xfs", 837: "wangan1", 838: "wangan2", 839: "wangan3", 840: "wangan5",
                   841: "LZ48", 842: "exo_decrunch", 843: "exo_decrunch_new", 844: "bitbuster", 845: "lazy",
                   846: "nibrans", 847: "LZRS_ASOBO", 848: "lzrhys", 849: "lze", 850: "zx0", 851: "zx1", 852: "zx2",
                   853: "zx5", 854: "rzip", 855: "melt1", 856: "melt2"
                   }


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
                   'age3scn', 'agg', 'ahm', 'al4', 'al8', 'ama', 'anm', 'ark', 'avix', 'awd', 'bag', 'bank1sbk',
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
                   'mim', 'mime', 'mpq', 'mpqe', 'msm', 'nrg', 'pbb', 'pst', 'tbb', 'udf', 'vbsp', 'vp', 'xzp'),
              'sau':
                  ('4pp', 'bdx', 'box', 'brig', 'c', 'cam', 'cc', 'chr', 'dbi', 'df2', 'epf', 'fan', 'flx', 'gor',
                   'group', 'hrs', 'ilb', 'jun', 'jus', 'key', 'lbx', 'maa', 'mul', 'nds', 'p00', 'p10', 'p99', 'rm',
                   'tgw', 'tlb', 'uop', 'vsr', 'war', 'wdb', 'xua', 'xub'),
              'seven_zip':
                  ('7z', 'zip', 'rar', '001', 'cab', 'iso', 'xz', 'txz', 'lzma', 'tar', 'cpio', 'bz2', 'bzip2', 'tbz',
                   'tbz2', 'gz', 'gzip', 'tgz', 'tpz', 'z', 'taz', 'lzh', 'lha', 'rpm', 'deb', 'arj', 'vhd', 'vhdx',
                   'wim', 'swm', 'esd', 'fat', 'ntfs', 'dmg', 'hfs', 'xar', 'squashfs', 'apfs', 'epub', 'fbz', 'fb2z',
                   'docx', 'xlsx', 'doc', 'docm', 'dotm', 'xls', 'ods', 'odt', 'mgs', 'tnef', 'dbx', 'mbx', 'mbox',
                   'tbb', 'pmm', 'emlx', 'eml', 'nws', 'mht', 'mhtml', 'b64', 'uue', 'xxe', 'ntx', 'bin', 'hqx', 'warc',
                   'pyz', 'ccd', 'img', 'cdi', 'chd', 'ciso', 'cso', 'cue', 'ecm', 'gdi', 'isz', 'mds', 'mdf', 'nrg',
                   'zisofs', 'asar', 'phar', 's01', 'e01', 'ex01', 'lo1', 'lx01', 'aff', 'ad1', 'whx', 'exfat',
                   'gro', 'kfs', 'lz', 'grp', 'fb3', 'piz', 'omod', 'fomod', 'rar5', 'zipx', 'pk3', 'pk4', 'fb2x',
                   'txtz'),
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
                   'm1v', 'm2v', 'm4v', 'mk3d', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'mve', 'ogm', 'ogv', 'pam', 'pmf',
                   'pmm', 'pss', 'rm', 'thp', 'ts', 'vid', 'vob', 'webm', 'wmv', 'xvid')
              }
