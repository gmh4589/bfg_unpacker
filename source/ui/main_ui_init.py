
import importlib
import json
import os
from datetime import datetime

import ffmpeg
import pandas

from PyQt6.QtCore import Qt, QItemSelectionModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt6.QtWidgets import *
import source.ui.main_ui as ui
from qt_material import apply_stylesheet
from qt_material import list_themes
from source.reaper import after_dot
from source.setting import Setting
from source.ui import (resize, setting as setting_ui, theme_creator, change_button_menu as cbm, progress_bar,
                       localize as translate, child_gui)


class MainWindow(QMainWindow, ui.Ui_BFGUnpacker, Setting):

    def __init__(self):
        super().__init__()

        self.out_dir = self.setting['Main']['out_path'] if os.path.exists(self.setting['Main']['out_path']) else (
            self.set_setting('Main', 'out_path',
                             QFileDialog.getExistingDirectory(self, 'Select folder')))

        self.path_to_root = os.path.abspath(__file__).split('source')[0]
        self.setWindowIcon(QIcon('./source/ui/icons/i.ico'))
        self.setWindowTitle("BFGUnpacker")
        self.resize(resize.widget(600), resize.widget(650))
        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.all_games = 0
        self.parent_list = {}
        self.lang_list_create()
        self.buttons_create()
        self.model = QStandardItemModel()
        self.gameList_treeView.setModel(self.model)
        self.root_item = self.model.invisibleRootItem()
        self.pb = progress_bar.ProgressBar(self.setting["Main"]["theme"])
        self.show_favorites = False
        self.filter_model = QStandardItemModel()
        self.quickOpen.triggered.connect(self.q_open)

        with open('./favorites.ini', 'r') as fav:
            self.favorites = []

            for line in fav.readlines():
                self.favorites.append(line[:-1])

        # Game list creating
        self.mainList = pandas.read_csv('./game_list/main_list.csv', delimiter='\t')

        if int(self.setting['Engines']['unity']) > 0:
            unity_list = pandas.read_csv('./game_list/unity_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, unity_list], axis=0, ignore_index=True)
        if int(self.setting['Engines']['unreal']) > 0:
            unreal_list = pandas.read_csv('./game_list/unreal_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, unreal_list], axis=0, ignore_index=True)
        if int(self.setting['Engines']['renpy']) > 0:
            renpy_list = pandas.read_csv('./game_list/renpy_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, renpy_list], axis=0, ignore_index=True)
        if int(self.setting['Engines']['game_maker']) > 0:
            gamemaker_list = pandas.read_csv('./game_list/gamemaker_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, gamemaker_list], axis=0, ignore_index=True)
        if int(self.setting['Engines']['rpg_maker']) > 0:
            rpgmaker_list = pandas.read_csv('./game_list/rpgmaker_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, rpgmaker_list], axis=0, ignore_index=True)
        if int(self.setting['Engines']['godot']) > 0:
            godot_list = pandas.read_csv('./game_list/godot_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, godot_list], axis=0, ignore_index=True)

        self.mainList = self.mainList.sort_values(by='game_name', key=lambda x: x.str.lower()).reset_index(drop=True)
        self.names = {row['game_name']: row['release_year'] for _, row in self.mainList.iterrows()}
        self.tree_view_create_by_name() if self.setting['Main']['group'] == 'name' else self.tree_view_create_by_year()
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, translate.select_something)
        self.all_games_count.setText(f'{translate.all_games} {self.all_games}')

        # Run functions and methods
        self.change_theme(self.setting["Main"]["theme"])
        self.archive_list = {}
        self.engine_list = {}
        self.archive_list_create()

        # Actions connected
        self.gameList_treeView.clicked.connect(self.file_reaper)
        self.action7z_Archiver.triggered.connect(  # ZIP
            lambda: self.select_unpacker('_ZIP'))
        self.actionGame_Archive_Unpacker_Plugin.triggered.connect(  # GAUP
            lambda: self.select_unpacker('_GAUP'))
        self.actionTotal_Observer.triggered.connect(  # Total Observer
            lambda: self.select_unpacker('_', script_name='data/wcx/TotalObserver.wcx'))
        self.exitAction.triggered.connect(self.close)
        self.action_Settings.triggered.connect(  # Settings run
            lambda: setting_ui.SettingWindow(style=self.setting["Main"]["theme"]).exec())
        self.create_theme.triggered.connect(  # Theme creator run
            lambda: theme_creator.ThemeCreateWindow(style=self.setting["Main"]["theme"]).exec())
        self.action_SelectOutPath.triggered.connect(  # Set out folder
            lambda: self.set_setting('Main', 'out_path', self.file_open(select_folder=True)))
        self.actionRad_Video_Tools.triggered.connect(  # Run RAD Video Tools
            lambda: os.system(f'{self.root_dir}data/rad_tools/radvideo64.exe'))
        self.actionMedia_Info.triggered.connect(lambda: print(ffmpeg.probe(
            QFileDialog.getOpenFileName(self, directory=self.setting['Main']['last_dir'])[0])))

        # Favorite block
        self.btn_All_Favorite.clicked.connect(lambda: self.all_favorites())  # All\favorite switch
        self.toolButton_plus.clicked.connect(  # Add to favorite
            lambda: self.favorite_setting(True, self.comboBox_gameList.currentText()))
        self.toolButton_minus.clicked.connect(  # Delete from favorite
            lambda: self.favorite_setting(False, self.comboBox_gameList.currentText()))
        self.toolButton_Find.clicked.connect(lambda: self.find_item_in_treeview())  # Find game button

        # Show console checkbox
        self.checkBox_ShowConsole.setChecked(bool(int(self.setting['Main']['show_console'])))
        self.checkBox_ShowConsole.stateChanged.connect(
            lambda: self.set_setting('Main', 'show_console', "2" if self.checkBox_ShowConsole.isChecked() else "0"))

        # Create subfolders checkbox
        self.checkBox_createSubfolders.setChecked(bool(int(self.setting['Main']['subfolders'])))
        self.checkBox_createSubfolders.stateChanged.connect(
            lambda: self.set_setting('Main', 'subfolders', "2" if self.checkBox_createSubfolders.isChecked() else "0"))

        # Converters with UI
        self.actionFFMPEG_Video_Converter.triggered.connect(self.ffmpeg_video)
        self.actionFFMPEG_Sound_Converter.triggered.connect(
            lambda: child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                            gui_name='FFMPEG Audio Converter',
                                            label_list=['Frequency', 'Channels', 'Audio Bitrate', 'Format'],
                                            action_list=[['8000', '12000', '16000', '22050', '24000', '32000', '36000', '44100', '48000', '96000', '192000', '384000', translate.other],
                                                         ['1', '2', '3', '4', '5', '6', '7', '8', translate.other],
                                                         ['8k', '12k', '16k', '20k', '24k', '32k', '48k', '64k', '96k', '112k', '128k', '160k', '192k', '256k', '320k', '448k', '512k', '768k', '1M', '2M', translate.other],
                                                         ['aac', 'ac3', 'flac', 'mp2', 'mp3', 'ogg', 'opus', 'ra', 'tta', 'wav', 'wma', 'wv', translate.other]],
                                            default_list=['44100', '2', '128k', 'mp3'],
                                            action=f'"{self.path_to_root}data\\ffmpeg\\ffmpeg.exe" '
                                                   f'-i "%file_name%" -vn '
                                                   f'-acodec %action_3% '
                                                   f'-ab %action_2% '
                                                   f'-ar[:stream_specifier] %action_0% '
                                                   # f'-af aresample=%action_1% '
                                                   # TODO: Add frequency
                                                   f'"%out_dir%/%out_name%.%action_3%"').exec())
        self.actionRAW_to_WAV.triggered.connect(self.raw2wav)
        self.actionRAW_to_Atrac.triggered.connect(self.raw2atrac)
        self.actionPlayStation_Audio_Converter.triggered.connect(self.ps_audio_tools)
        self.actionFFMPEG_Image_Converter.triggered.connect(
            lambda: child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                            gui_name='FFMPEG Image Converter',
                                            label_list=['Format'],
                                            action_list=[['apng', 'bmp', 'dpx', 'gif', 'jpg', 'pcx', 'pgm', 'pix', 'png', 'ppm', 'sgi', 'tga', 'tiff', 'xbm', 'xwd', translate.other]],
                                            default_list=['png'],
                                            action=f'"{self.path_to_root}data\\ffmpeg\\ffmpeg.exe" '
                                                   f'-i "%file_name%" '
                                                   f'"%out_dir%/%out_name%.%action_0%"').exec())
        self.action_nConvert.triggered.connect(self.nConvert)
        self.actionImage_to_DDS_Microsoft.triggered.connect(
            lambda: child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                            gui_name='Image to DDS (Microsoft)',
                                            label_list=['Format', 'Platform'],
                                            action_list=[['R32G32B32A32_FLOAT', 'R32G32B32A32_UINT', 'R32G32B32A32_SINT', 'R32G32B32_FLOAT', 'R32G32B32_UINT', 'R32G32B32_SINT', 'R16G16B16A16_FLOAT', 'R16G16B16A16_UNORM', 'R16G16B16A16_UINT', 'R16G16B16A16_SNORM', 'R16G16B16A16_SINT', 'R32G32_FLOAT', 'R32G32_UINT', 'R32G32_SINT', 'R10G10B10A2_UNORM', 'R10G10B10A2_UINT', 'R11G11B10_FLOAT', 'R8G8B8A8_UNORM', 'R8G8B8A8_UNORM_SRGB', 'R8G8B8A8_UINT', 'R8G8B8A8_SNORM', 'R8G8B8A8_SINT', 'R16G16_FLOAT', 'R16G16_UNORM', 'R16G16_UINT', 'R16G16_SNORM', 'R16G16_SINT', 'R32_FLOAT', 'R32_UINT', 'R32_SINT', 'R8G8_UNORM', 'R8G8_UINT', 'R8G8_SNORM', 'R8G8_SINT', 'R16_FLOAT', 'R16_UNORM', 'R16_UINT', 'R16_SNORM', 'R16_SINT', 'R8_UNORM', 'R8_UINT', 'R8_SNORM', 'R8_SINT', 'A8_UNORM', 'R9G9B9E5_SHAREDEXP', 'R8G8_B8G8_UNORM', 'G8R8_G8B8_UNORM', 'BC1_UNORM', 'BC1_UNORM_SRGB', 'BC2_UNORM', 'BC2_UNORM_SRGB', 'BC3_UNORM', 'BC3_UNORM_SRGB', 'BC4_UNORM', 'BC4_SNORM', 'BC5_UNORM', 'BC5_SNORM', 'B5G6R5_UNORM', 'B5G5R5A1_UNORM', 'B8G8R8A8_UNORM', 'B8G8R8X8_UNORM', 'R10G10B10_XR_BIAS_A2_UNORM', 'B8G8R8A8_UNORM_SRGB', 'B8G8R8X8_UNORM_SRGB', 'BC6H_UF16', 'BC6H_SF16', 'BC7_UNORM', 'BC7_UNORM_SRGB', 'AYUV', 'Y410', 'Y416', 'YUY2', 'Y210', 'Y216', 'B4G4R4A4_UNORM', translate.other],
                                                         ['PC', 'Xbox One']],
                                            default_list=['BC3_UNORM', 'PC']).exec())
        self.actionImage_to_DDS_nVidia.triggered.connect(
            lambda: child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                            gui_name='Image to DDS (nVidia)',
                                            label_list=['Format'],
                                            action_list=[['dxt1c', 'dxt1a', 'dxt3', 'dxt5', 'u1555', 'u4444', 'u565', 'u8888', 'u888', 'u555', 'p8c', 'p8a', 'p4c', 'p4a', 'a8', 'cxv8u8', 'v8u8', 'v16u16', 'A8L8', 'fp32x4', 'fp32', 'fp16x4', 'dxt5nm', 'g16r16', 'g16r16f', translate.other]],
                                            default_list=['dxt5']).exec())
        self.actionDDS_Header_Generator.triggered.connect(self.raw2dds)
        self.actionXWM_WAV_Audio_Converter.triggered.connect(
            lambda: child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                            gui_name='XWMA Tool GUI',
                                            label_list=['Frequency', 'Format'],
                                            action_list=[['20000', '32000', '48000', '64000', '96000', '160000', '192000', translate.other],
                                                         ['wav', 'xwm']],
                                            default_list=['48000', 'wav']).exec())
        self.actionWwise_Converter.triggered.connect(self.wwise_tools)

    def ffmpeg_video(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='FFMPEG Video Converter',
                                label_list=['Video Codec', 'Audio Codec', 'Video Bitrate', 'Audio Bitrate', 'Format', 'Width:High', 'Audio Track'],
                                action_list=[['a64_multi', 'a64_multi5', 'alias_pix', 'amv', 'apng', 'asv1', 'asv2', 'avrp', 'avui', 'ayuv', 'bmp', 'cinepak', 'cljr', 'dirac', 'dnxhd', 'dpx', 'dvvideo', 'ffv1', 'ffvhuff', 'flashsv', 'flashsv2', 'flv1', 'gif', 'h261', 'h263', 'h263p', 'h264', 'hap', 'hevc', 'huffyuv', 'jpeg2000', 'jpegls', 'ljpeg', 'mjpeg', 'mpeg1video', 'mpeg2video', 'mpeg4', 'msmpeg4v2', 'msmpeg4v3', 'msvideo1', 'pam', 'pbm', 'pcx', 'pgm', 'pgmyuv', 'png', 'ppm', 'prores', 'qtrle', 'r10k', 'r210', 'rawvideo', 'roq', 'rv10', 'rv20', 'sgi', 'snow', 'sunrast', 'svq1', 'targa', 'theora', 'tiff', 'utvideo', 'v210', 'v308', 'v408', 'v410', 'vp8', 'vp9', 'webp', 'wmv1', 'wmv2', 'wrapped_avframe', 'xbm', 'xface', 'xwd', 'y41p', 'yuv4', 'zlib', 'zmbv', translate.other],
                                             ['copy', 'aac', 'ac3', 'adpcm_adx', 'adpcm_g722', 'adpcm_g726', 'adpcm_ima_qt', 'adpcm_ima_wav', 'adpcm_ms', 'adpcm_swf', 'adpcm_yamaha', 'alac', 'amr_nb', 'amr_wb', 'comfortnoise', 'dts -strict -2', 'eac3', 'flac', 'g723_1', 'mp2', 'mp3',  'nellymoser', 'opus -strict -2', 'pcm_alaw', 'pcm_f32be',  'pcm_f32le', 'pcm_f64be', 'pcm_f64le', 'pcm_mulaw', 'pcm_s16be', 'pcm_s16be_planar', 'pcm_s16le', 'pcm_s16le_planar', 'pcm_s24be', 'pcm_s24daud', 'pcm_s24le', 'pcm_s24le_planar', 'pcm_s32be', 'pcm_s32le', 'pcm_s32le_planar', 'pcm_s8', 'pcm_s8_planar', 'pcm_u16be', 'pcm_u16le', 'pcm_u24be', 'pcm_u24le', 'pcm_u32be', 'pcm_u32le', 'pcm_u8', 'ra_144', 'roq_dpcm', 's302m', 'sonic', 'sonicls', 'speex', 'tta', 'vorbis -strict -2', 'wavpack', 'wmav1', 'wmav2', translate.other],
                                             ['64k', '128k', '192k', '256k', '512k', '768k', '1M', '2M', '3M', '4M', '5M', '6M', '8M', '10M', '12M', '15M', '16M', '20M', '25M', '30M', '40M', '50M', translate.other],
                                             ['16k', '24k', '32k', '48k', '64k', '96k', '112k', '128k', '160k', '192k', '224k', '256k', '320k', '360k', '448k', '512k', '768k', '1M', '2M', translate.other],
                                             ['3g2', '3gp', 'a64', 'asf', 'avi', 'dv', 'dvd', 'f4v', 'flv', 'hevc', 'ivf', 'm1v', 'm2v', 'm2t', 'm2ts', 'm4v', 'mkv', 'mjpeg', 'mov', 'mp4', 'mpeg', 'mpg', 'mts', 'mxf', 'ogv', 'pam', 'rm', 'roq', 'swf', 'ts', 'vc1', 'vp8', 'vob', 'webm', 'wmv', 'wtv', translate.other],
                                             ['160:120', '240:144', '240:160', '320:240', '360:240', '384:240', '400:240', '432:240', '480:320', '480:360', '480:360', '640:360', '512:384', '640:480', '720:480', '800:480', '854:480', '720:540', '960:540', '720:576', '1024:576', '800:600', '1024:600', '800:640', '960:640', '1024:640', '1136:640', '960:720', '1152:720', '1200:720', '1280:720', '1024:768', '1152:768', '1280:768', '1366:768', '1280:800', '1152:864', '1280:864', '1536:864', '1440:900', '1600:900', '1280:960', '1440:960', '1280:1024', '1400:1050', '1680:1050', '1440:1080', '1920:1080', '2560:1080', '2048:1152', '1600:1200', '1920:1200', '1920:1440', '2560:1440', '3440:1440', '1920:1536', '2048:1536', '2560:1600', '2880:1620', '2880:1800', '3200:1800', '2560:2048', '3200:2048', '3840:2160', '5120:2880', '4069:2160', '4096:3072', '5120:3200', '5760:3240', '5120:4096', '6400:4096', '7680:4320', '6400:4800', '7680:4800', translate.other],
                                             ['0', '1', '2', '3', '4', '5', '6', translate.other]],
                                default_list=['hevc', 'aac', '8M', '192k', 'mkv', '1920:1080', '1'],
                                action=f'"{self.path_to_root}data\\ffmpeg\\ffmpeg.exe" '
                                       f'-i "%file_name%" '
                                       f'-vcodec %action_0% '
                                       f'-vb %action_2% '
                                       f'-vf scale="%action_5%" '
                                       f'-acodec %action_1% '
                                       f'-ab %action_3% '
                                       f'-map 0:0 -map 0:%action_6% '
                                       f'"%out_dir%/%out_name%.%action_4%"').exec()

    def raw2wav(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='RAW to WAV Converter',
                                label_list=['Frequency', 'Channels', 'Bit', 'Format', 'Offset'],
                                action_list=[['8000', '12000', '16000', '22050', '24000', '36000', '44100', '48000', '96000', '192000', '384000', translate.other],
                                             ['1', '2', '3', '4', '5', '6', '7', '8', translate.other],
                                             ['8', '12', '16', '24', '32', '48', '64', '96', '128'],
                                             ['ADPCM', 'ALAW', 'ANTEX_ADPCME', 'APTX', 'ATRAC', 'AUDIOFILE_AF10', 'AUDIOFILE_AF36', 'BTV_DIGITAL', 'CANOPUS_ATRAC', 'CIRRUS', 'CONTROL_RES_CR10', 'CONTROL_RES_VQLPC', 'CREATIVE_ADPCM', 'CREATIVE_FASTSPEECH10', 'CREATIVE_FASTSPEECH8', 'CS2', 'CS_IMAADPCM', 'CU_CODEC', 'DF_G726', 'DF_GSM610', 'DIALOGIC_OKI_ADPCM', 'DIGIADPCM', 'DIGIFIX', 'DIGIREAL', 'DIGISTD', 'DIGITAL_G723', 'DOLBY_AC2', 'DOLBY_AC3_SPDIF', 'DRM', 'DSAT_DISPLAY', 'DSPGROUP_TRUESPEECH', 'DTS', 'DVI_ADPCM', 'DVM', 'ECHOSC1', 'ECHOSC3', 'ESPCM', 'ESST_AC3', 'FM_TOWNS_SND', 'G721_ADPCM', 'G722_ADPCM', 'G723_ADPCM', 'G726ADPCM', 'G726_ADPCM', 'G728_CELP', 'G729A', 'GSM610', 'IBM_CVSD', 'IEEE_FLOAT', 'ILINK_VC', 'IMA_ADPCM', 'IPI_HSX', 'IPI_RPELP', 'IRAT', 'ISIAUDIO', 'LH_CODEC', 'LRC', 'LUCENT_G723', 'MALDEN_PHONYTALK', 'MEDIASONIC_G723', 'MEDIASPACE_ADPCM', 'MEDIAVISION_ADPCM', 'MP3', 'MPEG', 'MSAUDIO1', 'MSG723', 'MSNAUDIO', 'MSRT24', 'MULAW', 'MVI_MVI2', 'NMS_VBXADPCM', 'NORRIS', 'OKI_ADPCM', 'OLIADPCM', 'OLICELP', 'OLIGSM', 'OLIOPR', 'OLISBC', 'ONLIVE', 'PAC', 'PACKED', 'PCM', 'PHILIPS_LPCBB', 'PROSODY_1612', 'PROSODY_8KBPS', 'QDESIGN_MUSIC', 'QUALCOMM_HALFRATE', 'QUALCOMM_PUREVOICE', 'QUARTERDECK', 'RAW_SPORT', 'RHETOREX_ADPCM', 'ROCKWELL_ADPCM', 'ROCKWELL_DIGITALK', 'RT24', 'SANYO_LD_ADPCM', 'SBC24', 'SIERRA_ADPCM', 'SIPROLAB_ACELP4800', 'SIPROLAB_ACELP8V3', 'SIPROLAB_ACEPLNET', 'SIPROLAB_G729', 'SIPROLAB_G729A', 'SIPROLAB_KELVIN', 'SOFTSOUND', 'SONARC', 'SONY_SCX', 'SOUNDSPACE_MUSICOMPRESS', 'TPC', 'TUBGSM', 'UHER_ADPCM', 'UNISYS_NAP_16K', 'UNISYS_NAP_ADPCM', 'UNISYS_NAP_ALAW', 'UNISYS_NAP_ULAW', 'UNKNOWN(0000)', 'UNKNOWN(FFFF)', 'VIVO_G723', 'VIVO_SIREN', 'VME_VMPCM', 'VOXWARE', 'VOXWARE_AC10', 'VOXWARE_AC16', 'VOXWARE_AC20', 'VOXWARE_AC8', 'VOXWARE_BYTE_ALIGNED', 'VOXWARE_RT24', 'VOXWARE_RT29', 'VOXWARE_RT29HW', 'VOXWARE_TQ40', 'VOXWARE_TQ60', 'VOXWARE_VR12', 'VOXWARE_VR18', 'VSELP', 'XEBEC', 'YAMAHA_ADPCM', 'ZYXEL_ADPCM'],
                                             ['0', translate.other]],
                                default_list=['44100', '2', '32', 'PCM', '0']).exec()

    def raw2atrac(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='RAW to Atrac Converter',
                                label_list=['Frequency', 'Channels', 'Bitrate', 'Format', 'Offset'],
                                action_list=[['8000', '12000', '16000', '22050', '24000', '36000', '44100', '48000', '96000', '192000', '384000'],
                                             ['1', '2'],
                                             ['32', '48', '52', '64', '66', '96', '105', '128', '132', '160', '192', '256', '320', '352'],
                                             ['AT3', 'AT3Plus', 'AT9'],
                                             ['0', translate.other]],
                                default_list=['44100', '2', '32', 'PCM', '0']).exec()

    def raw2dds(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='DDS Header Generator',
                                label_list=['Height', 'Width', 'Format', 'Offset'],
                                action_list=[['2', '4', '8', '12', '16', '24', '32', '48', '64', '96', '128', '256', '384', '512', '768', '1024', '1536', '2048', '3072', '4096', '8192', translate.other],
                                             ['2', '4', '8', '12', '16', '24', '32', '48', '64', '96', '128', '256', '384', '512', '768', '1024', '1536', '2048', '3072', '4096', '8192', translate.other],
                                             ['DXT1', 'DXT3', 'DXT5', 'DX10', 'BC4U', 'BC5U', 'BC4S', 'BC5S', 'ARGB8', translate.other],
                                             ['0', translate.other]],
                                default_list=['512', '512', 'DXT5', '0']).exec()

    def nConvert(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='nConverter',
                                label_list=['Format'],
                                action_list=[['bmp', 'cur', 'dcx', 'dds', 'dib', 'dng', 'gif', 'jif', 'jpeg', 'pcd', 'pcx', 'pdf', 'png', 'psb', 'psd', 'raw', 'svg', 'tga', 'tiff', 'wbmp', '------', '2bp', '2d', '3fr', '411', 'a64', 'abmp', 'abr', 'abs', 'acc', 'ace', 'aces', 'acorn', 'adex', 'adt', 'afphoto', 'afx', 'ai', 'aim', 'aip', 'aipd', 'alias', 'ami', 'ani', 'anv', 'aphp', 'apx', 'arcib', 'arf', 'arn', 'art', 'artdir', 'arw', 'atk', 'att', 'aurora', 'avs', 'avw', 'az7', 'b16', 'b3d', 'bdr', 'bfli', 'bfx', 'bga', 'bias', 'bif', 'biorad', 'bip', 'bld', 'blp', 'bmc', 'bmg', 'bms', 'bmx', 'bob', 'bpr', 'brk', 'bsg', 'btn', 'bum', 'byusir', 'c4', 'cadc', 'cals', 'cam', 'can', 'car', 'cart', 'cat', 'cbmf', 'cdr', 'cdu', 'ce', 'ce1', 'cel', 'cft', 'cgm', 'che', 'cin', 'cip', 'ciph', 'cipt', 'cish', 'cism', 'cloe', 'clp', 'cmt', 'cmu', 'cmx', 'cncd', 'cnct', 'cp8', 'cpa', 'cpat', 'cpc', 'cpt', 'cr2', 'craw', 'crd', 'crg', 'crw', 'csv', 'ct', 'cut', 'cvp', 'cwg', 'd3d', 'dali', 'dbw', 'dcmp', 'dcpy', 'dcr', 'dd', 'degas', 'dicom', 'dkb', 'dol', 'doodle', 'dpx', 'drz', 'dsi', 'dta', 'dwg', 'dwg', 'ecc', 'efx', 'eidi', 'eif', 'emf', 'emz', 'epa', 'epi', 'eps', 'epsp', 'erf', 'esm', 'esmp', 'eyes', 'f96', 'face', 'fax', 'fbm', 'fcx', 'fff', 'fff', 'ffpg', 'fgs', 'fi', 'fit', 'fits', 'fli', 'fmag', 'fmap', 'fmf', 'fp2', 'fpg', 'fpr', 'fpt', 'fre', 'frm', 'frm2', 'fsh', 'fsy', 'ftf', 'fx3', 'fxs', 'g16', 'g3n', 'gaf', 'gbr', 'gcd', 'gem', 'geo', 'gfaray', 'gg', 'gicon', 'gig', 'gih', 'gm', 'gmf', 'god', 'gpat', 'gpb', 'grob', 'gun', 'hdri', 'hdru', 'hed', 'hf', 'hir', 'hpgl', 'hpi', 'hr', 'hru', 'hrz', 'hsi', 'hta', 'icb', 'icd', 'icl', 'icn', 'icns', 'ico', 'icon', 'iff', 'ifx', 'iim', 'iimg', 'ilab', 'im5', 'img', 'imgt', 'imi', 'imt', 'indd', 'info', 'ingr', 'ioca', 'ipg', 'ipl', 'ipl2', 'ipseq', 'iris', 'ish', 'iss', 'j6i', 'jbf', 'jbr', 'jig', 'jig2', 'jj', 'jls', 'jps', 'jtf', 'jxr', 'k25', 'k25b', 'kdc', 'kdc2', 'kfx', 'kntr', 'koa', 'kps', 'kqp', 'kro', 'kskn', 'lbm', 'lcel', 'lda', 'lff', 'lif', 'lsm', 'lss', 'lvp', 'lwi', 'm8', 'mac', 'mag', 'map', 'mbig', 'mdl', 'mef', 'mfrm', 'mgr', 'mh', 'miff', 'mil', 'mjpg', 'mkcf', 'mklg', 'mng', 'mon', 'mos', 'mph', 'mpo', 'mrc', 'mrf', 'mrw', 'msp', 'msx2', 'mtv', 'mtx', 'ncr', 'ncy', 'ncy', 'nef', 'neo', 'ngg', 'nifti', 'nist', 'nitf', 'nlm', 'nol', 'npm', 'nrw', 'nsr', 'oaz', 'ocp', 'of', 'ofx', 'ohir', 'oil', 'ols', 'orf', 'os2', 'otap', 'otb', 'p64', 'p7', 'pabx', 'palm', 'pam', 'pan', 'patps', 'pbm', 'pbt', 'pcl', 'pcp', 'pd', 'pdd', 'pds', 'pdx', 'pef', 'pegs', 'pfi', 'pfm', 'pfs', 'pgc', 'pgf', 'pgm', 'pi', 'pic', 'pict', 'pig', 'pixi', 'pixp', 'pld', 'pm', 'pm', 'pmg', 'pmp', 'pmsk', 'pnm', 'pp4', 'pp5', 'ppm', 'ppp', 'pps', 'ppt', 'prc', 'prf', 'prisms', 'prx', 'ps', 'psa', 'pseg', 'psf', 'psion3', 'psion5', 'psp', 'pspb', 'pspf', 'pspm', 'pspp', 'pspt', 'ptg', 'pwp', 'pxa', 'pxr', 'pzl', 'pzp', 'q0', 'qcad', 'qdv', 'qrt', 'qtif', 'rad', 'raf', 'ras', 'raw1', 'raw2', 'raw3', 'raw4', 'raw5', 'raw6', 'raw7', 'raw8', 'raw9', 'rawa', 'rawb', 'rawdvr', 'rawe', 'ray', 'rdc', 'rfa', 'rfax', 'ript', 'rix', 'rla', 'rlc2', 'rle', 'rp', 'rpm', 'rsb', 'rsrc', 'rw2', 'rwl', 'sar', 'sci', 'sct', 'sdg', 'sdt', 'sfax', 'sfw', 'sgi', 'sif', 'sir', 'sj1', 'skf', 'skn', 'skp', 'smp', 'soft', 'spc', 'spot', 'sps', 'spu', 'srf', 'srf2', 'srw', 'ssi', 'ssp', 'sst', 'st4', 'stad', 'star', 'stm', 'stw', 'stx', 'syj', 'synu', 'taac', 'tdi', 'tdim', 'teal', 'tg4', 'thmb', 'ti', 'til', 'tile', 'tim', 'tim2', 'tiny', 'tjp', 'tnl', 'trup', 'tsk', 'ttf', 'tub', 'txc', 'uni', 'upe4', 'upi', 'upst', 'uyvy', 'uyvyi', 'v', 'vda', 'vfx', 'vi', 'vicar', 'vid', 'vif', 'viff', 'vista', 'vit', 'vivid', 'vob', 'vort', 'vpb', 'wad', 'wal', 'wbc', 'wfx', 'winm', 'wmf', 'wmz', 'wpg', 'wrl', 'wzl', 'x3f', 'xar', 'xbm', 'xcf', 'xif', 'xim', 'xnf', 'xp0', 'xpm', 'xwd', 'xyz', 'yuv411', 'yuv422', 'yuv444', 'zbr', 'zmf', 'zxhob', 'zxscr', 'zxsna', 'zzrough', translate.other]],
                                default_list=['png']).exec()

    def ps_audio_tools(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='PlayStation Audio Tools',
                                label_list=['Platform', 'Mode'],
                                action_list=[['PS2', 'PS3', 'PS4', 'PSP', 'PS Vita'],
                                             ['Atrac2WAV', 'WAV2Atrac', 'MSF2Atrac']],
                                default_list=['PS3', 'Atrac2WAV']).exec()

    def wwise_tools(self):
        child_gui.ChildUIWindow(style=self.setting["Main"]["theme"],
                                gui_name='Wwise Converter',
                                label_list=['Mode', 'Code book (only\nfor wwise2vorbis)'],
                                action_list=[['Wwise Unpacker', 'wwise2wav', 'wwise2vorbis'],
                                             ['packed_codebooks_aoTuV_603.bin', 'packed_codebooks3.bin']],
                                default_list=['Wwise Unpacker', 'packed_codebooks_aoTuV_603.bin']).exec()

    def find_item_in_treeview(self):

        item_text = self.comboBox_gameList.currentText()
        root_item = self.model.invisibleRootItem()
        index_to_activate = self.find_item_index(root_item, item_text)

        if index_to_activate is not None:
            self.gameList_treeView.selectionModel().select(index_to_activate, QItemSelectionModel.SelectionFlag.Select)
            self.gameList_treeView.scrollTo(index_to_activate)

    def find_item_index(self, parent_item, target_text):

        for row in range(parent_item.rowCount()):
            child_item = parent_item.child(row)

            if child_item.text() == target_text:
                return child_item.index()
            elif child_item.hasChildren():
                result = self.find_item_index(child_item, target_text)

                if result is not None:
                    return result

        return None

    def all_favorites(self):
        self.show_favorites = not self.show_favorites

        if self.show_favorites:
            self.filter_list_create(self.favorites)
            self.comboBox_gameList.items = self.favorites
            self.btn_All_Favorite.setText(translate.fav_caps)
        else:
            self.filter_list_create(self.names)
            self.comboBox_gameList.items = self.names
            self.btn_All_Favorite.setText(translate.all_caps)

    def favorite_setting(self, action, item):

        if item.strip() != '':

            if action:

                if item not in self.favorites:
                    self.favorites.append(item)
                    self.favorites.sort()
            else:
                self.favorites.remove(item)
                self.filter_list_create(self.favorites)

            with open('./favorites.ini', 'w') as fav:

                for favorite in self.favorites:
                    fav.write(favorite + '\n')

    def set_setting(self, section, key, value, remove=False):

        if remove:
            self.setting.remove_option(section, key)
        else:
            self.setting.set(section, key, value)

        with open('./setting.ini', "w") as cf:
            self.setting.write(cf)

    def append_text(self, text):

        if text.strip():
            self.logWindow.append(text)

    # Создается список тем
    def themes_list_create(self):

        default_themes = ['dark_amber', 'dark_blue', 'dark_blue_500', 'dark_cyan', 'dark_cyan_500', 'dark_lightgreen',
                          'dark_lightgreen_500', 'dark_medical', 'dark_orange', 'dark_pink', 'dark_pink_500',
                          'dark_purple', 'dark_purple_500', 'dark_red', 'dark_red_500', 'dark_teal', 'dark_teal_500',
                          'dark_yellow', 'light_amber', 'light_blue', 'light_blue_500', 'light_cyan', 'light_cyan_500',
                          'light_lightgreen', 'light_lightgreen_500', 'light_orange', 'light_pink', 'light_pink_500',
                          'light_purple', 'light_purple_500', 'light_red', 'light_red_500', 'light_teal',
                          'light_teal_500', 'light_yellow']

        other_themes_submenu = QMenu(self)
        other_themes_submenu.setTitle('...')

        for action in self.themes_list_2.actions():
            self.themes_list_2.removeAction(action)

        # Default Theme
        default_theme = self.themes_list_2.addAction('Default')
        default_theme.triggered.connect(lambda *args, x='Default': self.change_theme(x))
        self.themes_list_2.addMenu(other_themes_submenu)

        if self.setting["Main"]["theme"].lower() == 'default':
            default_theme.setIcon(QIcon('./source/ui/icons/checked.svg'))

        for theme in list_themes():
            theme_name = theme.split('.')[0]

            if theme_name not in default_themes or theme_name == self.setting["Main"]["theme"]:
                new_theme = self.themes_list_2.addAction(theme_name.replace('_', ' ').title())
            else:
                new_theme = other_themes_submenu.addAction(theme_name.replace('_', ' ').title())

            new_theme.triggered.connect(lambda *args, x=theme_name: self.change_theme(x))

            if theme_name == self.setting["Main"]["theme"]:
                new_theme.setIcon(QIcon('./source/ui/icons/checked.svg'))

        self.themes_list_2.addMenu(other_themes_submenu)

    def lang_list_create(self):
        d = './source/local/'
        lang_files = [file for file in os.listdir(d) if file.endswith('.json')]
        lang_list = [json.load(open(f'{d}{file}', 'r', encoding='utf-8'))['lang_name'] for file in lang_files]
        lang_codes = [json.load(open(f'{d}{file}', 'r', encoding='utf-8'))['lang_code'] for file in lang_files]
        main_list = ['ru', 'ua', 'pl', 'tr', 'de', 'it', 'fr', 'en', 'es', 'es_la',
                     'pt_br', 'ar', 'jp', 'ko', 'id', 'zh', 'zh_tw', 'th', 'vn', 'fi']

        for action in self.action_Language.actions():
            self.action_Language.removeAction(action)

        other_submenu = QMenu(self)
        other_submenu.setTitle('...')

        for i, lang in enumerate(lang_list):

            if lang_codes[i] in main_list or lang_codes[i] == self.setting["Main"]["lang"]:
                new_lang = self.action_Language.addAction(lang)
            else:
                new_lang = other_submenu.addAction(lang)

            new_lang.triggered.connect(lambda *args, x=lang_codes[i]: self.change_lang(x))

            if lang_codes[i] == self.setting["Main"]["lang"]:
                new_lang.setIcon(QIcon('./source/ui/icons/checked.svg'))

                if lang_codes[i] not in main_list:
                    main_list.append(lang_codes[i])

        self.action_Language.addMenu(other_submenu)

    def add_button(self, btn, l_func=None, contexts=None):

        if contexts is not None:
            context_menu = QMenu(self)

            for i, action in enumerate(contexts):
                context = context_menu.addAction(action)

                if action != translate.cancel:

                    if isinstance(l_func, list):
                        context.triggered.connect(l_func[i])
                    else:
                        context.triggered.connect(l_func)

            btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda pos, b=btn: context_menu.exec(b.mapToGlobal(pos)))

    def add_btn_action(self, btn, action=''):

        match action:
            case 'A': btn.clicked.connect(self.q_open)
            case 'B': btn.clicked.connect(lambda: self.create_queue(script_name=QFileDialog.getOpenFileName(
                self, translate.open_file, filter='QuickBMS Scripts (*.bms);;QuickBMS Scripts (*.txt);;'
                f'{translate.all_files} (*.*)', directory=self.setting['Main']['last_dir'])[0]))
            case 'C': btn.clicked.connect(lambda: self.create_queue(func_name='_7ZIP'))
            case 'D': btn.clicked.connect(lambda: self.create_queue(func_name='_GAUP'))
            case 'E': btn.clicked.connect(lambda: print('innosetup'))
            case 'F': btn.clicked.connect(self.ffmpeg_video)
            case 'G': btn.clicked.connect(lambda: self.create_queue(ext_list=after_dot['_Unreal'], func_name='_Unreal'))
            case 'H': btn.clicked.connect(lambda: self.create_queue(func_name='_Unity', select_folder=True))
            case 'I': btn.clicked.connect(lambda: self.create_queue(func_name='_idTech', ext_list=after_dot['_idTech']))
            case 'J': btn.clicked.connect(lambda: self.create_queue(func_name='_Total'))
            case 'K': btn.clicked.connect(lambda: print('creation'))
            case 'L': btn.clicked.connect(lambda: print('cry engine'))
            case 'M': btn.clicked.connect(lambda: os.system(f'{self.root_dir}data/rad_tools/radvideo64.exe'))
            case 'N': btn.clicked.connect(self.wwise_tools)
            case 'O': btn.clicked.connect(self.ps_audio_tools)
            case 'P': btn.clicked.connect(self.nConvert)
            case 'Q': btn.clicked.connect(lambda: print('red engine'))
            case 'R': btn.clicked.connect(lambda: print('godot'))
            case 'S': btn.clicked.connect(lambda: print('rpg maker'))
            case 'T': btn.clicked.connect(lambda: print('renpy'))
            case 'U': btn.clicked.connect(lambda: print('unigen'))
            case 'V': btn.clicked.connect(self.raw2dds)
            case 'W': btn.clicked.connect(self.raw2atrac)
            case 'X': btn.clicked.connect(self.raw2wav)
            case 'Y': btn.clicked.connect(lambda: setting_ui.SettingWindow(style=self.setting["Main"]["theme"]).exec())
            case 'Z': btn.clicked.connect(self.empty_out)

    # Создаются кнопки в верхнем меню
    def buttons_create(self):
        self.setting.read('./setting.ini')
        alpha = ['A']

        for j in range(1, 13):
            alpha.append(self.setting["Buttons"][str(j)])

        alpha.append('Y')
        alpha.append('Z')

        tool_tips = {'A': translate.quick_of,
                     'B': translate.open_qbms,
                     'C': translate.open_7z,
                     'D': translate.open_gaup,
                     'E': translate.open_inno,
                     'F': translate.convert_ffmpeg,
                     'G': translate.unpack_unreal,
                     'H': translate.unpack_unity,
                     'I': translate.unpack_idtech,
                     'J': translate.unpack_source,
                     'K': translate.unpack_creation,
                     'L': translate.unpack_cry,
                     'M': translate.convert_bink,
                     'N': translate.convert_wwise,
                     'O': translate.ps_audio_tool,
                     'P': translate.convert_nconvert,
                     'Q': translate.unpack_red,
                     'R': translate.unpack_godot,
                     'S': translate.unpack_rpgmaker,
                     'T': translate.unpack_renpy,
                     'U': translate.unpack_unigen,
                     'V': translate.header_dds,
                     'W': translate.header_atrac,
                     'X': translate.header_wav,
                     'Y': translate.run_setting,
                     'Z': translate.empty_of}

        for i in range(self.upperButtons.count()):
            item = self.upperButtons.itemAt(i)
            item.widget().deleteLater()

        for i, a in enumerate(alpha):
            btn = QToolButton(text=a, parent=None)
            btn.setToolTip(tool_tips[a])
            btn.setStyleSheet(
                'QToolButton {'
                "font-family: 'IconLib';"
                'border: 0px;'
                'margin: 0px;'
                'padding: 0px;'
                'border-radius: 10px;'
                f'height: {resize.widget(40)}px;'
                f'width: {resize.widget(40)}px;'
                f'font-size: {resize.widget(40)}px;'
                '}')

            if i not in (0, 13, 14, -1):
                self.add_button(btn, contexts=[translate.change_button, translate.cancel],
                                l_func=(lambda *args, l=i:
                                        self.new_button(style=self.setting["Main"]["theme"], alpha=l)))
            elif i == 14:
                self.add_button(btn, contexts=[translate.delete_to_trash, translate.full_delete, translate.cancel],
                                l_func=[lambda: self.set_setting('Main', 'trash', '1'),
                                        lambda: self.set_setting('Main', 'trash', '0')])
            else:
                self.add_button(btn)

            self.add_btn_action(btn, a)
            self.upperButtons.addWidget(btn)

    def new_button(self, style, alpha):
        cbm.CBWindow(style=style, letter=alpha).exec()
        self.buttons_create()

    # Наполняет списком меню "Архивы", "Образы дисков" и "Игровые Движки".
    def archive_list_create(self):
        archivesList = pandas.read_csv('./game_list/archives_list.csv', delimiter='\t')
        archivesList = archivesList.sort_values(by='Archives Name', key=lambda x: x.str.lower()).reset_index(drop=True)

        if self.setting['Main']['group_arch'] == '2':
            abc = sorted(list({archivesList['Archives Name'][n][0].upper() for n in range(len(archivesList))
                               if archivesList['Index'][n] not in (3, 5, 4) and archivesList['Archives Name'][n][0]
                               not in '0123456789'}), key=lambda x: x)
            self.archive_list = {'0-9': self.menu_archives.addMenu('0-9')}

            for liter in abc:
                self.archive_list[liter] = self.menu_archives.addMenu(liter)

        if self.setting['Main']['group_ge'] == '2':
            abc2 = sorted(list({archivesList['Archives Name'][n][0].upper() for n in range(len(archivesList))
                                if archivesList['Index'][n] == 4 and archivesList['Archives Name'][n][0]
                                not in '0123456789'}), key=lambda x: x)
            self.engine_list = {'0-9': self.menu_game_engines.addMenu('0-9')}

            for liter in abc2:
                self.engine_list[liter] = self.menu_game_engines.addMenu(liter)

        for n in range(len(archivesList)):

            if archivesList['Index'][n] == 3:
                self.menu_disk_images.addAction(archivesList['Archives Name'][n])
            elif archivesList['Index'][n] == 4:

                if self.setting['Main']['group_ge'] == '2':
                    liter = archivesList['Archives Name'][n][0].upper()

                    if liter in '0123456789':
                        self.engine_list['0-9'].addAction(archivesList['Archives Name'][n])
                    else:
                        self.engine_list[liter].addAction(archivesList['Archives Name'][n])
                else:
                    self.menu_game_engines.addAction(archivesList['Archives Name'][n])

            elif archivesList['Index'][n] == 5:
                self.menu_installers.addAction(archivesList['Archives Name'][n])
            else:

                if self.setting['Main']['group_arch'] == '2':
                    liter = archivesList['Archives Name'][n][0].upper()

                    if liter in '0123456789':
                        self.archive_list['0-9'].addAction(archivesList['Archives Name'][n])
                    else:
                        self.archive_list[liter].addAction(archivesList['Archives Name'][n])
                else:
                    self.menu_archives.addAction(archivesList['Archives Name'][n])

    def filter_list_create(self, items):
        self.comboBox_gameList.items = self.names
        self.filter_model.clear()
        self.filter_model.appendRow(QStandardItem(''))

        for item in items:
            self.filter_model.appendRow(QStandardItem(item))

        self.comboBox_gameList.setModel(self.filter_model)

    # Создается список игр в три-вью
    def tree_view_create_by_year(self):
        new_parent = QStandardItem(translate.other)
        self.parent_list[translate.other] = new_parent
        self.root_item.appendRow(new_parent)
        old_games = QStandardItem('... - 1990')
        self.parent_list['... - 1990'] = old_games
        year_now = datetime.now().year

        for i in range(year_now, 1990, -1):
            item = str(i)
            new_parent = QStandardItem(item)
            self.parent_list[item] = new_parent
            self.root_item.appendRow(new_parent)

        self.filter_list_create(self.names)

        for name in self.names:

            try:
                y = int(self.names[name])

                if y < 1991:
                    y = '... - 1990'
                else:
                    y = str(y)

            except ValueError:
                y = translate.other

            child = QStandardItem(name)
            child.setToolTip(name)
            self.parent_list[y].appendRow(child)
            self.all_games += 1

        self.root_item.appendRow(old_games)

    def tree_view_create_by_name(self):
        new_parent = QStandardItem('0-9')
        self.parent_list['0-9'] = new_parent
        self.root_item.appendRow(new_parent)

        for item in self.abc:
            new_parent = QStandardItem(item)
            self.parent_list[item] = new_parent
            self.root_item.appendRow(new_parent)

        new_parent = QStandardItem(translate.other)
        self.parent_list[translate.other] = new_parent
        self.root_item.appendRow(new_parent)
        self.filter_list_create(self.names)

        for name in self.names:

            if name[0].upper() in '0123456789':
                literal = '0-9'
            elif name[0].upper() in self.abc:
                literal = name[0].upper()
            else:
                literal = translate.other

            child = QStandardItem(name)
            child.setToolTip(name)
            self.parent_list[literal].appendRow(child)
            self.all_games += 1

    def change_theme(self, theme_name):
        apply_stylesheet(self, theme=f'{theme_name}.xml')
        self.set_setting('Main', 'theme', theme_name)
        self.themes_list_create()

    def change_lang(self, lang):
        self.set_setting('Main', 'lang', lang)
        self.lang_list_create()
        importlib.reload(translate)
        self.buttons_create()
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, translate.select_something)
        self.all_games_count.setText(f'{translate.all_games} {self.all_games}')
        self.retranslateUi()
