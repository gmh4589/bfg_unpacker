
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk

from source.setting import Setting
from source.codecs import wav_list, audio_tools, image_tools
from source.codecs.dds_tools import DDSCreator
from source.ui import localize as translate, child_gui
from source.codecs.zip_methods import zip_methods
# from source.codecs.zip_methods_bak import zip_methods


# Методы для создания и наполнения дочерних интерфейсов
class ChildGuiData(Setting):

    def ffmpeg_video(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='FFMPEG Video Converter',
                                label_list=['Video Codec', 'Audio Codec', 'Video Bitrate', 'Audio Bitrate', 'Format', 'Width', 'High', 'Audio Track'],
                                action_list=[['a64_multi', 'a64_multi5', 'alias_pix', 'amv', 'apng', 'asv1', 'asv2', 'avrp', 'avui', 'ayuv', 'bmp', 'cinepak', 'cljr', 'dirac', 'dnxhd', 'dpx', 'dvvideo', 'ffv1', 'ffvhuff', 'flashsv', 'flashsv2', 'flv1', 'gif', 'h261', 'h263', 'h263p', 'h264', 'hap', 'hevc', 'huffyuv', 'jpeg2000', 'jpegls', 'ljpeg', 'mjpeg', 'mpeg1video', 'mpeg2video', 'mpeg4', 'msmpeg4v2', 'msmpeg4v3', 'msvideo1', 'pam', 'pbm', 'pcx', 'pgm', 'pgmyuv', 'png', 'ppm', 'prores', 'qtrle', 'r10k', 'r210', 'rawvideo', 'roq', 'rv10', 'rv20', 'sgi', 'snow', 'sunrast', 'svq1', 'targa', 'theora', 'tiff', 'utvideo', 'v210', 'v308', 'v408', 'v410', 'vp8', 'vp9', 'webp', 'wmv1', 'wmv2', 'wrapped_avframe', 'xbm', 'xface', 'xwd', 'y41p', 'yuv4', 'zlib', 'zmbv', translate.other],
                                             ['copy', 'aac', 'ac3', 'adpcm_adx', 'adpcm_argo', 'adpcm_g722', 'adpcm_g726', 'adpcm_g726le', 'adpcm_ima_alp', 'adpcm_ima_amv', 'adpcm_ima_apm', 'adpcm_ima_qt', 'adpcm_ima_ssi', 'adpcm_ima_wav', 'adpcm_ima_ws', 'adpcm_ms', 'adpcm_swf', 'adpcm_yamaha', 'alac', 'amr_nb', 'aptx', 'aptx_hd', 'comfortnoise', 'dts', 'eac3', 'flac', 'g723_1', 'mlp', 'mp2', 'mp3', 'nellymoser', 'opus', 'pcm_alaw', 'pcm_dvd', 'pcm_f32be', 'pcm_f32le', 'pcm_f64be', 'pcm_f64le', 'pcm_mulaw', 'pcm_s16be', 'pcm_s16be_planar', 'pcm_s16le', 'pcm_s16le_planar', 'pcm_s24be', 'pcm_s24daud', 'pcm_s24le', 'pcm_s24le_planar', 'pcm_s32be', 'pcm_s32le', 'pcm_s32le_planar', 'pcm_s64be', 'pcm_s64le', 'pcm_s8', 'pcm_s8_planar', 'pcm_u16be', 'pcm_u16le', 'pcm_u24be', 'pcm_u24le', 'pcm_u32be', 'pcm_u32le', 'pcm_u8', 'pcm_vidc', 'ra_144', 'roq_dpcm', 's302m', 'sbc', 'sonic', 'sonicls', 'truehd', 'tta', 'libvorbis', 'wavpack', 'wmav1', 'wmav2', translate.other],
                                             ['64k', '128k', '192k', '256k', '512k', '768k', '1M', '2M', '3M', '4M', '5M', '6M', '8M', '10M', '12M', '15M', '16M', '20M', '25M', '30M', '40M', '50M', translate.other],
                                             ['16k', '24k', '32k', '48k', '64k', '96k', '112k', '128k', '160k', '192k', '224k', '256k', '320k', '360k', '448k', '512k', '768k', '1M', '2M', translate.other],
                                             ['3g2', '3gp', 'a64', 'asf', 'avi', 'dv', 'dvd', 'f4v', 'flv', 'hevc', 'ivf', 'm1v', 'm2v', 'm2t', 'm2ts', 'm4v', 'mkv', 'mjpeg', 'mov', 'mp4', 'mpeg', 'mpg', 'mts', 'mxf', 'ogv', 'pam', 'rm', 'roq', 'swf', 'ts', 'vc1', 'vp8', 'vob', 'webm', 'wmv', 'wtv', translate.other],
                                             ['120', '144', '160', '192', '240', '256', '272', '288', '308', '320', '342', '360', '384', '400', '426', '480', '512', '540', '576', '600', '640', '720', '768', '800', '810', '854', '864', '900', '960', '1024', '1050', '1064', '1080', '1136', '1200', '1152', '1200', '1280', '1350', '1360', '1366', '1400', '1440', '1536', '1600', '1620', '1800', '1920', '2025', '2048', '2160', '2250', '2400', '2560', '2880', '3072', '3200', '3240', '3440', '3384', '3840', '4096', '4320', '4800', '5120', '5760', '6016', '6400', '7680', '8192', '8640', '10240', '10320', '15360', translate.other],
                                             ['120', '144', '160', '192', '240', '256', '272', '288', '308', '320', '342', '360', '384', '400', '426', '480', '512', '540', '576', '600', '640', '720', '768', '800', '810', '854', '864', '900', '960', '1024', '1050', '1064', '1080', '1136', '1200', '1152', '1200', '1280', '1350', '1360', '1366', '1400', '1440', '1536', '1600', '1620', '1800', '1920', '2025', '2048', '2160', '2250', '2400', '2560', '2880', '3072', '3200', '3240', '3440', '3384', '3840', '4096', '4320', '4800', '5120', '5760', '6016', '6400', '7680', '8192', '8640', '10240', '10320', '15360', translate.other],
                                             ['0', '1', '2', '3', '4', '5', '6', translate.other]],
                                default_list=['hevc', 'aac', '8M', '192k', 'mkv', '1920', '1080', '1'],
                                action=f'"{self.path_to_root}\\data\\ffmpeg\\ffmpeg.exe" '
                                       f'-i "%file_name%" '
                                       f'-vcodec %action_0% '
                                       f'-vb %action_2% '
                                       f'-vf scale="%action_5%:%action_6%" '
                                       f'-acodec %action_1% -strict -2 '
                                       f'-ab %action_3% '
                                       f'-map 0:0 -map 0:%action_7% '
                                       f'-y "%out_dir%/%out_name%.%action_4%"').exec()

    def ffmpeg_audio(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='FFMPEG Audio Converter',
                                label_list=['Frequency', 'Channels', 'Audio Bitrate', 'Speed', 'Codec', 'Format'],
                                action_list=[['8000', '12000', '16000', '22050', '24000', '32000', '36000', '44100', '48000', '96000', '192000', '384000', translate.other],
                                             ['1', '2', '3', '4', '5', '6', '7', '8', translate.other],
                                             ['8k', '12k', '16k', '20k', '24k', '32k', '48k', '64k', '96k', '112k', '128k', '160k', '192k', '256k', '320k', '448k', '512k', '768k', '1M', '2M', translate.other],
                                             ['1/2', '1', '2', translate.other],
                                             ['mp3', translate.other],  # Codec list autocomplete
                                             ['aac', 'ac3', 'dts', 'flac', 'm4a', 'mka', 'mp2', 'mp3', 'ogg', 'opus', 'ra', 'tta', 'wav', 'wma', 'wv', translate.other]],
                                default_list=['44100', '2', '128k', '1', 'mp3', 'mp3'],
                                action=f'"{self.path_to_root}\\data\\ffmpeg\\ffmpeg.exe" '
                                       f'-i "%file_name%" -vn '
                                       f'-acodec %action_4% '
                                       f'-ab %action_2% -strict -2 '
                                       f"-af asetrate=%action_0% "
                                       f"-af atempo=%action_3% "
                                       f'-y "%out_dir%/%out_name%.%action_5%"',
                                drop_a=True, item1=5, item2=4,
                                combos={
                                    'mka':  ['alac', 'aac', 'ac3', 'mp3', 'flac', 'libvorbis', 'opus', translate.other],
                                    'm4a':  ['alac', 'aac', 'ac3', translate.other],
                                    'ra':   ['ra_144', translate.other],
                                    'ogg':  ['libvorbis', 'opus', 'flac', translate.other],
                                    'opus': ['opus', translate.other],
                                    'wav':  ['pcm_s24le', 'aac', 'ac3', 'adpcm_adx', 'adpcm_argo', 'adpcm_g722', 'adpcm_g726', 'adpcm_g726le', 'adpcm_ima_alp', 'adpcm_ima_amv', 'adpcm_ima_apm', 'adpcm_ima_qt', 'adpcm_ima_ssi', 'adpcm_ima_wav', 'adpcm_ima_ws', 'adpcm_ms', 'adpcm_swf', 'adpcm_yamaha', 'alac', 'amr_nb', 'aptx', 'aptx_hd', 'comfortnoise', 'dts', 'eac3', 'flac', 'g723_1', 'mlp', 'mp2', 'mp3', 'nellymoser', 'opus', 'pcm_alaw', 'pcm_dvd', 'pcm_f32be', 'pcm_f32le', 'pcm_f64be', 'pcm_f64le', 'pcm_mulaw', 'pcm_s16be', 'pcm_s16be_planar', 'pcm_s16le', 'pcm_s16le_planar', 'pcm_s24be', 'pcm_s24daud', 'pcm_s24le_planar', 'pcm_s32be', 'pcm_s32le', 'pcm_s32le_planar', 'pcm_s64be', 'pcm_s64le', 'pcm_s8', 'pcm_s8_planar', 'pcm_u16be', 'pcm_u16le', 'pcm_u24be', 'pcm_u24le', 'pcm_u32be', 'pcm_u32le', 'pcm_u8', 'pcm_vidc', 'ra_144', 'roq_dpcm', 's302m', 'sbc', 'sonic', 'sonicls', 'truehd', 'tta', 'libvorbis', 'wavpack', 'wmav1', 'wmav2', translate.other],
                                    'wma':  ['wmav1', 'wmav2', 'wmalossless', 'wmapro', 'wmavoice', translate.other],
                                    'wv':   ['wavpack', translate.other]}).exec()

    def ffmpeg_image(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='FFMPEG Image Converter',
                                label_list=['Format'],
                                action_list=[['apng', 'bmp', 'dpx', 'gif', 'jpg', 'pcx', 'pgm', 'pix', 'png', 'ppm', 'sgi', 'tga', 'tiff', 'xbm', 'xwd', translate.other]],
                                default_list=['png'],
                                action=f'"{self.path_to_root}\\data\\ffmpeg\\ffmpeg.exe" '
                                       f'-i "%file_name%" '
                                       f'-y "%out_dir%\\%out_name%.%action_0%"').exec()

    def raw2wav(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='RAW to WAV Converter',
                                label_list=['Frequency', 'Channels', 'Bit', 'Format', 'Offset'],
                                action_list=[['8000', '12000', '16000', '22050', '24000', '36000', '44100', '48000',
                                              '96000', '192000', '384000', translate.other],
                                             ['1', '2', '3', '4', '5', '6', '7', '8', translate.other],
                                             ['8', '12', '16', '24', '32', '48', '64', '96', '128', translate.other],
                                             [key for key in sorted(wav_list.wav_list)],
                                             ['0', translate.other]],
                                default_list=['48000', '2', '16', 'PCM', '0'],
                                action=audio_tools.wav_save).exec()

    def raw2atrac(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='RAW to Atrac Converter',
                                label_list=['Format', 'Channels', 'Bitrate', 'Loop', 'Offset'],
                                action_list=[['AT3', 'AT9'],
                                             ['1', '2', '6', '8'],
                                             ['64', '72', '96', '114', '128', '144', '160', '192', '256', '320'],
                                             [translate.yes, translate.no],
                                             ['0', translate.other]],
                                drop_a=True, item1=1, item2=2,
                                combos={'1': ['34', '48', '57', '64', '72', '96', '128'],
                                        '2': ['64', '72', '96', '114', '128', '144', '160', '192', '256', '320'],
                                        '6': ['192', '256', '320', '384', '512'],
                                        '8': ['384', '768']},
                                default_list=['AT3', '2', '192', translate.no, '0'],
                                action=audio_tools.atrac_save).exec()

    def raw2dds(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='DDS Header Generator',
                                label_list=['Height', 'Width', 'Format', 'Offset'],
                                action_list=[['2', '4', '8', '12', '16', '24', '32', '48', '64', '96', '128', '256', '384', '512', '768', '1024', '1536', '2048', '3072', '4096', '8192', translate.other],
                                             ['2', '4', '8', '12', '16', '24', '32', '48', '64', '96', '128', '256', '384', '512', '768', '1024', '1536', '2048', '3072', '4096', '8192', translate.other],
                                             DDSCreator.codec_list(),
                                             ['0', translate.other]],
                                default_list=['512', '512', 'BC3_UNORM', '0']).exec()

    def nConvert(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='nConverter',
                                label_list=['Format'],
                                action_list=[['bmp', 'cur', 'dcx', 'dds', 'dib', 'dng', 'gif', 'jif', 'jpeg', 'pcd', 'pcx', 'pdf', 'png', 'psb', 'psd', 'raw', 'svg', 'tga', 'tiff', 'wbmp', '------', '2bp', '2d', '3fr', '411', 'a64', 'abmp', 'abr', 'abs', 'acc', 'ace', 'aces', 'acorn', 'adex', 'adt', 'afphoto', 'afx', 'ai', 'aim', 'aip', 'aipd', 'alias', 'ami', 'ani', 'anv', 'aphp', 'apx', 'arcib', 'arf', 'arn', 'art', 'artdir', 'arw', 'atk', 'att', 'aurora', 'avs', 'avw', 'az7', 'b16', 'b3d', 'bdr', 'bfli', 'bfx', 'bga', 'bias', 'bif', 'biorad', 'bip', 'bld', 'blp', 'bmc', 'bmg', 'bms', 'bmx', 'bob', 'bpr', 'brk', 'bsg', 'btn', 'bum', 'byusir', 'c4', 'cadc', 'cals', 'cam', 'can', 'car', 'cart', 'cat', 'cbmf', 'cdr', 'cdu', 'ce', 'ce1', 'cel', 'cft', 'cgm', 'che', 'cin', 'cip', 'ciph', 'cipt', 'cish', 'cism', 'cloe', 'clp', 'cmt', 'cmu', 'cmx', 'cncd', 'cnct', 'cp8', 'cpa', 'cpat', 'cpc', 'cpt', 'cr2', 'craw', 'crd', 'crg', 'crw', 'csv', 'ct', 'cut', 'cvp', 'cwg', 'd3d', 'dali', 'dbw', 'dcmp', 'dcpy', 'dcr', 'dd', 'degas', 'dicom', 'dkb', 'dol', 'doodle', 'dpx', 'drz', 'dsi', 'dta', 'dwg', 'dwg', 'ecc', 'efx', 'eidi', 'eif', 'emf', 'emz', 'epa', 'epi', 'eps', 'epsp', 'erf', 'esm', 'esmp', 'eyes', 'f96', 'face', 'fax', 'fbm', 'fcx', 'fff', 'fff', 'ffpg', 'fgs', 'fi', 'fit', 'fits', 'fli', 'fmag', 'fmap', 'fmf', 'fp2', 'fpg', 'fpr', 'fpt', 'fre', 'frm', 'frm2', 'fsh', 'fsy', 'ftf', 'fx3', 'fxs', 'g16', 'g3n', 'gaf', 'gbr', 'gcd', 'gem', 'geo', 'gfaray', 'gg', 'gicon', 'gig', 'gih', 'gm', 'gmf', 'god', 'gpat', 'gpb', 'grob', 'gun', 'hdri', 'hdru', 'hed', 'hf', 'hir', 'hpgl', 'hpi', 'hr', 'hru', 'hrz', 'hsi', 'hta', 'icb', 'icd', 'icl', 'icn', 'icns', 'ico', 'icon', 'iff', 'ifx', 'iim', 'iimg', 'ilab', 'im5', 'img', 'imgt', 'imi', 'imt', 'indd', 'info', 'ingr', 'ioca', 'ipg', 'ipl', 'ipl2', 'ipseq', 'iris', 'ish', 'iss', 'j6i', 'jbf', 'jbr', 'jig', 'jig2', 'jj', 'jls', 'jps', 'jtf', 'jxr', 'k25', 'k25b', 'kdc', 'kdc2', 'kfx', 'kntr', 'koa', 'kps', 'kqp', 'kro', 'kskn', 'lbm', 'lcel', 'lda', 'lff', 'lif', 'lsm', 'lss', 'lvp', 'lwi', 'm8', 'mac', 'mag', 'map', 'mbig', 'mdl', 'mef', 'mfrm', 'mgr', 'mh', 'miff', 'mil', 'mjpg', 'mkcf', 'mklg', 'mng', 'mon', 'mos', 'mph', 'mpo', 'mrc', 'mrf', 'mrw', 'msp', 'msx2', 'mtv', 'mtx', 'ncr', 'ncy', 'ncy', 'nef', 'neo', 'ngg', 'nifti', 'nist', 'nitf', 'nlm', 'nol', 'npm', 'nrw', 'nsr', 'oaz', 'ocp', 'of', 'ofx', 'ohir', 'oil', 'ols', 'orf', 'os2', 'otap', 'otb', 'p64', 'p7', 'pabx', 'palm', 'pam', 'pan', 'patps', 'pbm', 'pbt', 'pcl', 'pcp', 'pd', 'pdd', 'pds', 'pdx', 'pef', 'pegs', 'pfi', 'pfm', 'pfs', 'pgc', 'pgf', 'pgm', 'pi', 'pic', 'pict', 'pig', 'pixi', 'pixp', 'pld', 'pm', 'pm', 'pmg', 'pmp', 'pmsk', 'pnm', 'pp4', 'pp5', 'ppm', 'ppp', 'pps', 'ppt', 'prc', 'prf', 'prisms', 'prx', 'ps', 'psa', 'pseg', 'psf', 'psion3', 'psion5', 'psp', 'pspb', 'pspf', 'pspm', 'pspp', 'pspt', 'ptg', 'pwp', 'pxa', 'pxr', 'pzl', 'pzp', 'q0', 'qcad', 'qdv', 'qrt', 'qtif', 'rad', 'raf', 'ras', 'raw1', 'raw2', 'raw3', 'raw4', 'raw5', 'raw6', 'raw7', 'raw8', 'raw9', 'rawa', 'rawb', 'rawdvr', 'rawe', 'ray', 'rdc', 'rfa', 'rfax', 'ript', 'rix', 'rla', 'rlc2', 'rle', 'rp', 'rpm', 'rsb', 'rsrc', 'rw2', 'rwl', 'sar', 'sci', 'sct', 'sdg', 'sdt', 'sfax', 'sfw', 'sgi', 'sif', 'sir', 'sj1', 'skf', 'skn', 'skp', 'smp', 'soft', 'spc', 'spot', 'sps', 'spu', 'srf', 'srf2', 'srw', 'ssi', 'ssp', 'sst', 'st4', 'stad', 'star', 'stm', 'stw', 'stx', 'syj', 'synu', 'taac', 'tdi', 'tdim', 'teal', 'tg4', 'thmb', 'ti', 'til', 'tile', 'tim', 'tim2', 'tiny', 'tjp', 'tnl', 'trup', 'tsk', 'ttf', 'tub', 'txc', 'uni', 'upe4', 'upi', 'upst', 'uyvy', 'uyvyi', 'v', 'vda', 'vfx', 'vi', 'vicar', 'vid', 'vif', 'viff', 'vista', 'vit', 'vivid', 'vob', 'vort', 'vpb', 'wad', 'wal', 'wbc', 'wfx', 'winm', 'wmf', 'wmz', 'wpg', 'wrl', 'wzl', 'x3f', 'xar', 'xbm', 'xcf', 'xif', 'xim', 'xnf', 'xp0', 'xpm', 'xwd', 'xyz', 'yuv411', 'yuv422', 'yuv444', 'zbr', 'zmf', 'zxhob', 'zxscr', 'zxsna', 'zzrough', translate.other]],
                                default_list=['png']).exec()

    def image_to_dds_ms(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='Image to DDS (Microsoft)',
                                label_list=['Format', 'Platform'],
                                action_list=[['R32G32B32A32_FLOAT', 'R32G32B32A32_UINT', 'R32G32B32A32_SINT', 'R32G32B32_FLOAT', 'R32G32B32_UINT', 'R32G32B32_SINT', 'R16G16B16A16_FLOAT', 'R16G16B16A16_UNORM', 'R16G16B16A16_UINT', 'R16G16B16A16_SNORM', 'R16G16B16A16_SINT', 'R32G32_FLOAT', 'R32G32_UINT', 'R32G32_SINT', 'R10G10B10A2_UNORM', 'R10G10B10A2_UINT', 'R11G11B10_FLOAT', 'R8G8B8A8_UNORM', 'R8G8B8A8_UNORM_SRGB', 'R8G8B8A8_UINT', 'R8G8B8A8_SNORM', 'R8G8B8A8_SINT', 'R16G16_FLOAT', 'R16G16_UNORM', 'R16G16_UINT', 'R16G16_SNORM', 'R16G16_SINT', 'R32_FLOAT', 'R32_UINT', 'R32_SINT', 'R8G8_UNORM', 'R8G8_UINT', 'R8G8_SNORM', 'R8G8_SINT', 'R16_FLOAT', 'R16_UNORM', 'R16_UINT', 'R16_SNORM', 'R16_SINT', 'R8_UNORM', 'R8_UINT', 'R8_SNORM', 'R8_SINT', 'A8_UNORM', 'R9G9B9E5_SHAREDEXP', 'R8G8_B8G8_UNORM', 'G8R8_G8B8_UNORM', 'BC1_UNORM', 'BC1_UNORM_SRGB', 'BC2_UNORM', 'BC2_UNORM_SRGB', 'BC3_UNORM', 'BC3_UNORM_SRGB', 'BC4_UNORM', 'BC4_SNORM', 'BC5_UNORM', 'BC5_SNORM', 'B5G6R5_UNORM', 'B5G5R5A1_UNORM', 'B8G8R8A8_UNORM', 'B8G8R8X8_UNORM', 'R10G10B10_XR_BIAS_A2_UNORM', 'B8G8R8A8_UNORM_SRGB', 'B8G8R8X8_UNORM_SRGB', 'BC6H_UF16', 'BC6H_SF16', 'BC7_UNORM', 'BC7_UNORM_SRGB', 'AYUV', 'Y410', 'Y416', 'YUY2', 'Y210', 'Y216', 'B4G4R4A4_UNORM', translate.other],
                                             {"texconv": 'PC', "xtexconv": 'Xbox One'}],
                                default_list=['BC3_UNORM', 'PC'],
                                action=f'"{self.path_to_root}\\data\\dds_tools\\%action_1%.exe" '
                                       f'-f %action_0% -o "%out_dir%" "%file_name%"').exec()

    def image_to_dds_nv(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='Image to DDS (nVidia)',
                                label_list=['Format'],
                                action_list=[['dxt1c', 'dxt1a', 'dxt3', 'dxt5', 'u1555', 'u4444', 'u565', 'u8888', 'u888', 'u555', 'p8c', 'p8a', 'p4c', 'p4a', 'a8', 'cxv8u8', 'v8u8', 'v16u16', 'A8L8', 'fp32x4', 'fp32', 'fp16x4', 'dxt5nm', 'g16r16', 'g16r16f', translate.other]],
                                default_list=['dxt5'],
                                action=f'"{self.path_to_root}\\data\\dds_tools\\nvdxt.exe" '
                                       f'-file "%file_name%" -%action_0% '
                                       f'-output "%out_dir%\\%out_name%.dds"').exec()

    # TODO: Нужна ли? VGM все это умеет
    def wwise_tools(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='Wwise Converter',
                                label_list=['Mode', 'Code book (only\nfor wwise2ogg)'],
                                action_list=[['Wwise Unpacker', 'wwise2wav', 'wwise2ogg'],
                                             ['packed_codebooks_aoTuV_603.bin', 'packed_codebooks3.bin']],
                                default_list=['Wwise Unpacker', 'packed_codebooks_aoTuV_603.bin']).exec()

    # TODO: Нужна ли? VGM все это умеет
    def xwm2wav(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='XWM/WAV Converter',
                                label_list=['Frequency', 'Format'],
                                action_list=[['20000', '32000', '48000', '64000', '96000', '160000', '192000', translate.other],
                                             ['wav', 'xwm']],
                                default_list=['48000', 'wav']).exec()

    # TODO: Нужна ли? VGM все это умеет
    def ps_audio_tools(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='PlayStation Audio Tools',
                                label_list=['Platform', 'Mode'],
                                action_list=[['PS2', 'PS3', 'PS4', 'PSP', 'PS Vita'],
                                             ['Atrac2WAV', 'WAV2Atrac', 'MSF2Atrac']],
                                default_list=['PS3', 'Atrac2WAV'],
                                drop_a=True,
                                combos={
                                    'PS2': ['VAG2WAV', 'WAV2VAG', 'PS2_SoundBank'],
                                    'PS3': ['Atrac2WAV', 'WAV2Atrac', 'MSF2Atrac'],
                                    'PS4': ['Atrac2WAV', 'WAV2Atrac', 'SXD2Atrac'],
                                    'PSP': ['Atrac2WAV', 'WAV2Atrac'],
                                    'PS Vita': ['Atrac2WAV', 'WAV2Atrac']},
                                action=audio_tools.ps_audio_tools).exec()

    def find_zip(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name=translate.find_zip_method,
                                label_list=[translate.zip_method],
                                # action_list=[sorted(key for key in zip_methods.values())],
                                # action_list=[zip_methods],
                                action_list=[zip_methods.get_zip_indexes()],
                                default_list=['DEFLATE'],
                                action=(f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" -o -a "%action_0%" '
                                        f'"{self.path_to_root}\\data\\QuickBMS\\comtype_scan2.bms" '
                                        f'"%file_name%" "%out_dir%"').replace("/", "\\")).exec()

    def pb_show(self):

        theme = f'data/themes/{self.setting["Main"]["theme"]}.xml'

        try:
            tree = ET.parse(theme)
        except FileNotFoundError:
            tree = ET.parse(f'data/themes/classic_white.xml')

        xml = tree.getroot()
        color_dict = {}

        for color in xml.findall('color'):
            name = color.get('name')
            value = color.text
            color_dict[name] = value

        root = tk.Tk()
        root.overrideredirect(True)
        x = (root.winfo_screenwidth() - 250) / 2
        y = (root.winfo_screenheight() - 38) / 2
        root.geometry('250x40')
        root.wm_geometry("+%d+%d" % (x, y))

        info = ttk.Label()
        info.grid(row=0, column=0)
        progress_var = tk.DoubleVar()

        while not self.all_games:
            info['text'] = f'{translate.wait}: {self.current_game}/{self.all_games}'

        bar = ttk.Progressbar(root, variable=progress_var, maximum=self.all_games, length=250)
        bar.grid(row=1, column=0)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar",
                        background=color_dict['primaryColor'],
                        troughcolor=color_dict['secondaryLightColor'])
        style.configure("TLabel",
                        background=color_dict['secondaryDarkColor'],
                        foreground=color_dict['secondaryTextColor'])
        root['bg'] = color_dict['secondaryDarkColor']

        while self.download:
            root.update()
            progress_var.set(self.current_game)
            info['text'] = f'{translate.wait}: {int(self.current_game)}/{self.all_games}'

        root.destroy()
        root.mainloop()
