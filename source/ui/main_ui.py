import os
from datetime import datetime

from threading import Thread
import pandas
from icecream import ic

from PyQt6.QtCore import QRect, QMetaObject, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *
from source.ui.custom_ui import AutoCompleteComboBox
from source.ui.main_ui_text import Translate
from PyQt6.QtGui import QStandardItemModel, QIcon
from source.ui import setting as setting_ui, theme_creator, progress_bar, localize as translate
SHOW_LOAD = True

# noinspection PyTypeChecker
class Ui_BFGUnpacker(Translate):

    def __init__(self):
        self.path_to_root = os.path.curdir
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(8)
        self.big_font = QFont()
        self.big_font.setPointSize(10)
        self.centralwidget.setFont(self.font)
        self.centralwidget.setAcceptDrops(True)
        self.comboBox_gameList = AutoCompleteComboBox(self.centralwidget)
        self.comboBox_gameList.setGeometry(QRect(80, 40, 375, 30))
        self.toolButton_plus = QToolButton(self.centralwidget)
        self.toolButton_plus.setGeometry(QRect(455, 40, 30, 30))
        self.toolButton_minus = QToolButton(self.centralwidget)
        self.toolButton_minus.setGeometry(QRect(485, 40, 30, 30))
        self.logWindow = QTextBrowser(self.centralwidget)
        self.logWindow.setStyleSheet('QTextBrowser {font-size: 12px;}')
        self.logWindow.setGeometry(QRect(300, 80, 295, 520))
        self.all_games_count = QLabel(self.centralwidget)
        self.all_games_count.setGeometry(QRect(451, 603, 150, 20))
        self.all_games_count.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.all_games_count.setFont(self.big_font)
        self.gameList_treeView = QTreeView(self.centralwidget)
        self.gameList_treeView.setGeometry(QRect(0, 80, 295, 520))
        self.gameList_treeView.setStyleSheet('QTreeView::item {min-height: 20px;}')
        self.toolButton_Find = QToolButton(self.centralwidget)
        self.toolButton_Find.setGeometry(QRect(515, 40, 85, 30))
        self.btn_All_Favorite = QToolButton(self.centralwidget)
        self.btn_All_Favorite.setGeometry(QRect(0, 40, 80, 30))

        # Чекбоксы
        self.checkBoxes = QWidget(self.centralwidget)
        self.checkBoxes.setGeometry(QRect(10, 600, 451, 20))
        self.cb = QHBoxLayout(self.checkBoxes)
        self.cb.setContentsMargins(0, 0, 0, 0)

        self.checkBox_Reimport = QCheckBox(self.checkBoxes)
        self.cb.addWidget(self.checkBox_Reimport)
        self.checkBox_ShowConsole = QCheckBox(self.checkBoxes)
        self.cb.addWidget(self.checkBox_ShowConsole)
        self.checkBox_createSubfolders = QCheckBox(self.checkBoxes)
        self.cb.addWidget(self.checkBox_createSubfolders)

        # Панель кнопок
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QRect(0, 0, 600, 40))
        self.upperButtons = QHBoxLayout(self.layoutWidget)
        self.upperButtons.setContentsMargins(0, 0, 0, 0)

        # Меню
        self.menubar = QMenuBar(self)
        self.menu = QMenu(self.menubar)
        self.menubar.setStyleSheet('QMenu::item {height: 20px;}')
        self.unpackWith = QMenu(self.menu)
        self.zippedFormats = QMenu(self.menu)
        self.formatSearch = QMenu(self.menu)
        self.additionalMenu = QMenu(self.menu)

        # Consoles
        self.consolesMenu = QMenu(self.menu)

        # Sony
        self.menuSony = QMenu(self.consolesMenu)

        self.menuPlayStation_1 = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPlayStation_1.menuAction())
        self.ps1_xa = QWidgetAction(self.menuPlayStation_1)
        self.menuPlayStation_1.addAction(self.ps1_xa)

        self.menuPlayStation_2 = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPlayStation_2.menuAction())
        self.vag2wav = QWidgetAction(self.menuPlayStation_2)
        self.menuPlayStation_2.addAction(self.vag2wav)
        self.wav2vag = QWidgetAction(self.menuPlayStation_2)
        self.menuPlayStation_2.addAction(self.wav2vag)
        self.ps2_soundbank = QWidgetAction(self.menuPlayStation_2)
        self.menuPlayStation_2.addAction(self.ps2_soundbank)

        self.menuPlayStation_3 = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPlayStation_3.menuAction())
        self.ps3PsarcZlib = QWidgetAction(self.menuPlayStation_3)
        self.menuPlayStation_3.addAction(self.ps3PsarcZlib)
        self.ps3PsarcLzma = QWidgetAction(self.menuPlayStation_3)
        self.menuPlayStation_3.addAction(self.ps3PsarcLzma)
        self.ps3XWS = QWidgetAction(self.menuPlayStation_3)
        self.menuPlayStation_3.addAction(self.ps3XWS)
        self.ps3_atrac2wav = QWidgetAction(self.menuPlayStation_3)
        self.menuPlayStation_3.addAction(self.ps3_atrac2wav)
        self.ps3_wav2atrac = QWidgetAction(self.menuPlayStation_3)
        self.menuPlayStation_3.addAction(self.ps3_wav2atrac)
        self.msf2atrac = QWidgetAction(self.menuPlayStation_3)
        self.menuPlayStation_3.addAction(self.msf2atrac)

        self.menuPlayStation_4 = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPlayStation_4.menuAction())
        self.ps4PKG_CNT = QWidgetAction(self.menuPlayStation_4)
        self.menuPlayStation_4.addAction(self.ps4PKG_CNT)
        self.ps4_atrac2wav = QWidgetAction(self.menuPlayStation_4)
        self.menuPlayStation_4.addAction(self.ps4_atrac2wav)
        self.ps4_wav2atrac = QWidgetAction(self.menuPlayStation_4)
        self.menuPlayStation_4.addAction(self.ps3_wav2atrac)
        self.sxd2atrac = QWidgetAction(self.menuPlayStation_4)
        self.menuPlayStation_4.addAction(self.sxd2atrac)

        self.menuPlayStation_5 = QMenu(self.menuSony)
        # self.menuSony.addAction(self.menuPlayStation_5.menuAction())

        self.menuPSP = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPSP.menuAction())
        self.pspCSO = QWidgetAction(self.menuPSP)
        self.menuPSP.addAction(self.pspCSO)
        self.psp_atrac2wav = QWidgetAction(self.menuPSP)
        self.menuPSP.addAction(self.psp_atrac2wav)
        self.psp_wav2atrac = QWidgetAction(self.menuPSP)
        self.menuPSP.addAction(self.psp_wav2atrac)

        self.menuPlayStation_Vita = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPlayStation_Vita.menuAction())
        self.gxt2png = QWidgetAction(self.menuPlayStation_Vita)
        self.menuPlayStation_Vita.addAction(self.gxt2png)
        self.png2gxt = QWidgetAction(self.menuPlayStation_Vita)
        self.menuPlayStation_Vita.addAction(self.png2gxt)
        self.psvPsarc = QWidgetAction(self.menuPlayStation_Vita)
        self.menuPlayStation_Vita.addAction(self.psvPsarc)
        self.psv_atrac2wav = QWidgetAction(self.menuPlayStation_Vita)
        self.menuPlayStation_Vita.addAction(self.psv_atrac2wav)
        self.psv_wav2atrac = QWidgetAction(self.menuPlayStation_Vita)
        self.menuPlayStation_Vita.addAction(self.psv_wav2atrac)

        self.consolesMenu.addAction(self.menuSony.menuAction())

        # Microsoft
        self.menuMicrosoft = QMenu(self.consolesMenu)

        self.menuXBox_Classic = QMenu(self.menuMicrosoft)
        self.menuMicrosoft.addAction(self.menuXBox_Classic.menuAction())
        self.xboxISO = QWidgetAction(self.menuXBox_Classic)
        self.menuXBox_Classic.addAction(self.xboxISO)
        self.xboxAFS = QWidgetAction(self.menuXBox_Classic)
        self.menuXBox_Classic.addAction(self.xboxAFS)

        self.menuXBox_360 = QMenu(self.menuMicrosoft)
        self.menuMicrosoft.addAction(self.menuXBox_360.menuAction())

        self.menuXBox_One = QMenu(self.menuMicrosoft)
        self.menuMicrosoft.addAction(self.menuXBox_One.menuAction())

        self.menuXBox_Series = QMenu(self.menuMicrosoft)
        self.menuMicrosoft.addAction(self.menuXBox_Series.menuAction())

        self.consolesMenu.addAction(self.menuMicrosoft.menuAction())

        # Nintendo
        self.menuNintendo = QMenu(self.consolesMenu)

        self.menuGameCube = QMenu(self.menuNintendo)
        self.menuNintendo.addAction(self.menuGameCube.menuAction())
        self.game_cubeISO = QWidgetAction(self.menuGameCube)
        self.gcCISO = QWidgetAction(self.menuGameCube)
        self.gcCSO = QWidgetAction(self.menuGameCube)
        self.menuGameCube.addAction(self.gcCSO)
        self.menuGameCube.addAction(self.game_cubeISO)
        self.menuGameCube.addAction(self.gcCISO)

        self.menuWii = QMenu(self.menuNintendo)
        self.menuNintendo.addAction(self.menuWii.menuAction())
        self.wiiISO = QWidgetAction(self.menuWii)
        self.menuWii.addAction(self.wiiISO)
        self.wiiWDF = QWidgetAction(self.menuWii)
        self.menuWii.addAction(self.wiiWDF)

        self.menuWii_U = QMenu(self.menuNintendo)
        self.menuNintendo.addAction(self.menuWii_U.menuAction())

        self.menuSwitch = QMenu(self.menuNintendo)
        self.menuNintendo.addAction(self.menuSwitch.menuAction())
        self.switchNSP = QWidgetAction(self.menuSwitch)
        self.menuSwitch.addAction(self.switchNSP)

        self.menuClassic_Consoles = QMenu(self.menuNintendo)
        self.menuNintendo.addAction(self.menuClassic_Consoles.menuAction())
        self.nintendoSARC = QWidgetAction(self.menuClassic_Consoles)
        self.menuClassic_Consoles.addAction(self.nintendoSARC)
        self.nintendoDS_SDAT = QWidgetAction(self.menuClassic_Consoles)
        self.menuClassic_Consoles.addAction(self.nintendoDS_SDAT)
        self.nintendoNitro = QWidgetAction(self.menuClassic_Consoles)
        self.menuClassic_Consoles.addAction(self.nintendoNitro)

        self.consolesMenu.addAction(self.menuNintendo.menuAction())

        # Sega
        self.menuSega = QMenu(self.consolesMenu)

        self.menuDreamcast = QMenu(self.menuSega)
        self.menuSega.addAction(self.menuDreamcast.menuAction())
        self.dreamcastGDI = QWidgetAction(self.menuDreamcast)
        self.menuDreamcast.addAction(self.dreamcastGDI)

        self.menuMegaDrive = QMenu(self.menuSega)
        self.menuSega.addAction(self.menuMegaDrive.menuAction())

        self.menuSaturn = QMenu(self.menuSega)
        self.menuSega.addAction(self.menuSaturn.menuAction())

        self.menuSegaOther = QMenu(self.menuSega)
        self.menuSega.addAction(self.menuSegaOther.menuAction())

        self.consolesMenu.addAction(self.menuSega.menuAction())

        # Other
        self.menuOtherConsoles = QMenu(self.consolesMenu)
        self.consolesMenu.addAction(self.menuOtherConsoles.menuAction())

        self.menuAmigaDiskFile = QWidgetAction(self.menuOtherConsoles)  # SAU
        self.menuOtherConsoles.addAction(self.menuAmigaDiskFile)

        self.menu_archives = QMenu(self.menu)
        self.menu_game_engines = QMenu(self.menu)
        self.menu_disk_images = QMenu(self.menu)
        self.menu_installers = QMenu(self.menu)
        self.menu_convert = QMenu(self.menubar)
        self.videoConverters = QMenu(self.menu_convert)
        self.audioConverters = QMenu(self.menu_convert)
        self.imageConverters = QMenu(self.menu_convert)
        self.archiveConverters = QMenu(self.menu_convert)
        self.menu_settings = QMenu(self.menubar)
        self.themes_list_2 = QMenu(self.menu_settings)
        self.menu_about = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.quickOpen = QWidgetAction(self)
        self.exitAction = QWidgetAction(self)
        self.action_Language = QMenu(self)
        self.action_SelectOutPath = QWidgetAction(self)
        self.action_ClearOutPath = QWidgetAction(self)
        self.action_CreateOutPath = QWidgetAction(self)
        self.action_Settings = QWidgetAction(self)
        self.action_About = QWidgetAction(self)
        self.action7z_Archiver = QWidgetAction(self)
        self.actionGame_Archive_Unpacker_Plugin = QWidgetAction(self)
        self.actionTotal_Observer = QWidgetAction(self)
        self.actionSprite_and_Archive_Utility = QWidgetAction(self)
        self.actionZlib_Deflate = QWidgetAction(self)
        self.actionLZ4 = QWidgetAction(self)
        self.actionWAV = QWidgetAction(self)
        self.autoSearchScripts = QWidgetAction(self)
        self.actionFileList = QWidgetAction(self)
        self.actionArchiveScanner = QWidgetAction(self)
        self.actionFindZipMethod = QWidgetAction(self)
        self.actionFFMPEG_Video_Converter = QWidgetAction(self)
        self.actionRad_Video_Tools = QWidgetAction(self)
        self.actionMedia_Info = QWidgetAction(self)
        self.actionFFMPEG_Sound_Converter = QWidgetAction(self)
        self.actionVGM_Stream_Tools = QWidgetAction(self)
        self.actionFSBext = QWidgetAction(self)
        self.actionToWAV = QWidgetAction(self)
        self.actionRAW_to_WAV = QWidgetAction(self)
        self.actionRAW_to_Atrac = QWidgetAction(self)
        # self.actionRAW_to_MP3 = QWidgetAction(self)
        self.actionPlayStation_Audio_Converter = QWidgetAction(self)
        self.actionXWM_WAV_Audio_Converter = QWidgetAction(self)
        self.actionFFMPEG_Image_Converter = QWidgetAction(self)
        self.actionWwise_Converter = QWidgetAction(self)
        self.actionSAU = QWidgetAction(self)
        self.action_nConvert = QWidgetAction(self)
        self.actionImage_to_DDS_Microsoft = QWidgetAction(self)
        self.actionImage_to_DDS_nVidia = QWidgetAction(self)
        self.actionDDS_Header_Generator = QWidgetAction(self)
        self.actionCubeMap_Creator = QWidgetAction(self)
        self.actionICO_Icon_Splitter = QWidgetAction(self)
        self.create_theme = QWidgetAction(self)
        self.unpackWith.addAction(self.action7z_Archiver)
        self.unpackWith.addAction(self.actionGame_Archive_Unpacker_Plugin)
        self.unpackWith.addAction(self.actionTotal_Observer)
        self.unpackWith.addAction(self.actionSprite_and_Archive_Utility)
        self.zippedFormats.addAction(self.actionZlib_Deflate)
        self.zippedFormats.addAction(self.actionLZ4)
        self.formatSearch.addAction(self.actionWAV)
        self.additionalMenu.addAction(self.autoSearchScripts)
        self.additionalMenu.addAction(self.actionFileList)

        self.menu.addAction(self.quickOpen)
        self.menu.addAction(self.unpackWith.menuAction())
        self.menu.addAction(self.menu_archives.menuAction())
        self.menu.addAction(self.menu_game_engines.menuAction())
        self.menu.addAction(self.consolesMenu.menuAction())
        self.menu.addAction(self.menu_disk_images.menuAction())
        self.menu.addAction(self.menu_installers.menuAction())
        self.menu.addAction(self.zippedFormats.menuAction())
        self.menu.addAction(self.formatSearch.menuAction())
        self.menu.addAction(self.additionalMenu.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.exitAction)
        self.videoConverters.addAction(self.actionFFMPEG_Video_Converter)
        self.videoConverters.addAction(self.actionRad_Video_Tools)
        self.videoConverters.addAction(self.actionMedia_Info)
        self.audioConverters.addAction(self.actionFFMPEG_Sound_Converter)
        self.audioConverters.addAction(self.actionVGM_Stream_Tools)
        self.audioConverters.addAction(self.actionFSBext)
        self.audioConverters.addAction(self.actionToWAV)
        self.audioConverters.addAction(self.actionRAW_to_WAV)
        self.audioConverters.addAction(self.actionRAW_to_Atrac)
        # self.audioConverters.addAction(self.actionRAW_to_MP3)
        self.audioConverters.addAction(self.actionPlayStation_Audio_Converter)
        self.audioConverters.addAction(self.actionXWM_WAV_Audio_Converter)
        self.audioConverters.addAction(self.actionWwise_Converter)
        self.imageConverters.addAction(self.actionFFMPEG_Image_Converter)
        self.imageConverters.addAction(self.actionSAU)
        self.imageConverters.addAction(self.action_nConvert)
        self.imageConverters.addAction(self.actionImage_to_DDS_Microsoft)
        self.imageConverters.addAction(self.actionImage_to_DDS_nVidia)
        self.imageConverters.addAction(self.actionDDS_Header_Generator)
        self.imageConverters.addAction(self.actionCubeMap_Creator)
        self.imageConverters.addAction(self.actionICO_Icon_Splitter)
        self.archiveConverters.addAction(self.actionArchiveScanner)
        self.archiveConverters.addAction(self.actionFindZipMethod)
        self.menu_convert.addAction(self.videoConverters.menuAction())
        self.menu_convert.addAction(self.audioConverters.menuAction())
        self.menu_convert.addAction(self.imageConverters.menuAction())
        self.menu_convert.addAction(self.archiveConverters.menuAction())
        self.menu_settings.addAction(self.action_Language.menuAction())
        self.menu_settings.addAction(self.themes_list_2.menuAction())
        self.menu_settings.addAction(self.create_theme)
        self.menu_settings.addAction(self.action_Settings)
        self.menu_settings.addAction(self.action_SelectOutPath)
        self.menu_settings.addAction(self.action_ClearOutPath)
        self.menu_settings.addAction(self.action_CreateOutPath)
        self.menu_about.addAction(self.action_About)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_convert.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menubar.addAction(self.menu_about.menuAction())
        self.setCentralWidget(self.centralwidget)

        self.all_games = 0
        self.download = True
        self.current_game = 0
        self.last_run = None
        self.out_dir = self.setting['Main']['out_path'] if os.path.exists(self.setting['Main']['out_path']) else (
            self.set_setting('Main', 'out_path',
                             QFileDialog.getExistingDirectory(self, 'Select folder')))

        self.pb = progress_bar.ProgressBar(self.setting["Main"]["theme"])

        if int(self.setting["Main"]["load_bar"]):
            Thread(target=self.pb_show, daemon=True).start()

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

        self.all_games = len(self.mainList)
        ic(self.all_games)

        self.names = {}
        self.setWindowIcon(QIcon('./data/icons/i.ico'))
        self.setWindowTitle("BFGUnpacker")
        self.resize(600, 650)
        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.parent_list = {}
        self.lang_list_create()
        self.buttons_create()
        self.model = QStandardItemModel()
        self.gameList_treeView.setModel(self.model)
        self.root_item = self.model.invisibleRootItem()
        self.show_favorites = False
        self.filter_model = QStandardItemModel()

        Thread(target=self.tree_view_create, daemon=True).start()
        self.quickOpen.triggered.connect(self.q_open)
        self.wiiISO.triggered.connect(lambda: self.create_queue(func_name='_Wii_iso',
                                                                ext_list=f'Wii {translate.disc_image} (*.iso; *.wbfs)|'))
        self.wiiWDF.triggered.connect(lambda: self.create_queue(func_name='_Wii_iso',
                                                                ext_list=f'Wii WDF, WIA, CISO {translate.disc_image} (*.wdf; *.wia; *.ciso)|'))
        self.gcCISO.triggered.connect(lambda: self.create_queue(func_name='_Wii_iso',
                                                                ext_list=f'Game Cube {translate.disc_image} (*.ciso)|'))
        self.game_cubeISO.triggered.connect(lambda: self.create_queue(func_name='_Wii_iso',
                                                                      ext_list=f'Game Cube {translate.disc_image} (*.iso)|'))
        self.gcCSO.triggered.connect(lambda: self.create_queue(func_name='_7ZIP',
                                                               ext_list=f'CSO {translate.disc_image} (*.cso)|'))
        self.pspCSO.triggered.connect(lambda: self.create_queue(func_name='_7ZIP',
                                                                ext_list=f'CSO {translate.disc_image} (*.cso)|'))
        self.favorites = []

        if os.path.exists('favorites.ini'):

            with open('favorites.ini', 'r') as fav:

                for line in fav.readlines():
                    self.favorites.append(line[:-1])
        else:
            with open('favorites.ini', 'w'):
                pass

        # Run functions and methods
        self.change_theme(self.setting["Main"]["theme"])
        self.archive_list = {}
        self.engine_list = {}
        self.archive_list_create()
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, translate.select_something)

        # Actions connected
        self.actionArchiveScanner.triggered.connect(self.find_zip)
        self.gameList_treeView.clicked.connect(self.file_reaper)
        self.action7z_Archiver.triggered.connect(  # ZIP
            lambda: self.create_queue(func_name='_7ZIP'))
        self.actionGame_Archive_Unpacker_Plugin.triggered.connect(  # GAUP
            lambda: self.create_queue(func_name='_GAUP'))
        self.actionTotal_Observer.triggered.connect(  # Total Observer
            lambda: self.create_queue(func_name='_Total'))
        self.exitAction.triggered.connect(self.close)
        self.action_Settings.triggered.connect(  # Settings run
            lambda: setting_ui.SettingWindow(style=self.setting["Main"]["theme"]).exec())
        self.create_theme.triggered.connect(  # Theme creator run
            lambda: theme_creator.ThemeCreateWindow(style=self.setting["Main"]["theme"]).exec())
        self.action_SelectOutPath.triggered.connect(  # Set out folder
            lambda: self.set_setting('Main', 'out_path', self.file_open(select_folder=True)))
        self.actionRad_Video_Tools.triggered.connect(  # Run RAD Video Tools
            lambda: os.system(f'{self.path_to_root}\\data\\rad_tools\\radvideo64.exe'))
        # self.actionMedia_Info.triggered.connect(lambda: print(ffmpeg.probe(
        #     QFileDialog.getOpenFileName(self, directory=self.setting['Main']['last_dir'])[0])))

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
        self.actionFFMPEG_Sound_Converter.triggered.connect(self.ffmpeg_audio)
        self.actionRAW_to_WAV.triggered.connect(self.raw2wav)
        self.actionRAW_to_Atrac.triggered.connect(self.raw2atrac)
        self.actionFFMPEG_Image_Converter.triggered.connect(self.ffmpeg_image)
        self.action_nConvert.triggered.connect(self.nConvert)
        self.actionImage_to_DDS_Microsoft.triggered.connect(self.image_to_dds_ms)
        self.actionImage_to_DDS_nVidia.triggered.connect(self.image_to_dds_nv)
        self.actionDDS_Header_Generator.triggered.connect(self.raw2dds)
        self.actionXWM_WAV_Audio_Converter.triggered.connect(self.xwm2wav)
        self.actionWwise_Converter.triggered.connect(self.wwise_tools)
        self.actionPlayStation_Audio_Converter.triggered.connect(self.ps_audio_tools)
        self.actionFindZipMethod.triggered.connect(self.find_zip)

        self.download = False

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
