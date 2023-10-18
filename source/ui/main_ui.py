
from PyQt5.QtCore import QRect, QMetaObject, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from source.ui.main_ui_text import Translate
from source.ui import resize


# noinspection PyTypeChecker
class Ui_BFGUnpacker(Translate):

    def __init__(self):
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(resize.widget(8))
        self.centralwidget.setFont(self.font)
        self.comboBox_gameList = QComboBox(self.centralwidget)
        self.comboBox_gameList.setGeometry(
            QRect(resize.widget(80), resize.widget(40), resize.widget(375), resize.widget(30)))
        self.toolButton_plus = QToolButton(self.centralwidget)
        self.toolButton_plus.setGeometry(
            QRect(resize.widget(455), resize.widget(40), resize.widget(30), resize.widget(30)))
        self.toolButton_minus = QToolButton(self.centralwidget)
        self.toolButton_minus.setGeometry(
            QRect(resize.widget(485), resize.widget(40), resize.widget(30), resize.widget(30)))
        self.logWindow = QTextBrowser(self.centralwidget)
        self.logWindow.setStyleSheet('QTextBrowser {'
                                     f'font-size: {resize.widget(12)}px;'
                                     '}')
        self.logWindow.setGeometry(QRect(resize.widget(300), resize.widget(80), resize.widget(295), resize.widget(520)))

        self.all_games_count = QLabel(self.centralwidget)
        self.all_games_count.setGeometry(
            QRect(resize.widget(451), resize.widget(600), resize.widget(150), resize.widget(20)))
        self.all_games_count.setAlignment(Qt.AlignCenter)

        self.gameList_treeView = QTreeView(self.centralwidget)
        self.gameList_treeView.setGeometry(QRect(0, resize.widget(80), resize.widget(295), resize.widget(520)))
        self.gameList_treeView.setStyleSheet('QTreeView::item {'
                                             f'min-height: {resize.widget(20)}px;'
                                             '}')
        self.toolButton_Find = QToolButton(self.centralwidget)
        self.toolButton_Find.setGeometry(
            QRect(resize.widget(515), resize.widget(40), resize.widget(85), resize.widget(30)))
        self.btn_All_Favorite = QToolButton(self.centralwidget)
        self.btn_All_Favorite.setGeometry(QRect(0, resize.widget(40), resize.widget(80), resize.widget(30)))

        # Чекбоксы
        self.checkBoxes = QWidget(self.centralwidget)
        self.checkBoxes.setGeometry(QRect(resize.widget(10), resize.widget(600), resize.widget(451), resize.widget(20)))
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
        self.layoutWidget.setGeometry(QRect(0, 0, resize.widget(600), resize.widget(40)))
        self.upperButtons = QHBoxLayout(self.layoutWidget)
        self.upperButtons.setContentsMargins(0, 0, 0, 0)

        # Меню
        self.menubar = QMenuBar(self)
        self.menu = QMenu(self.menubar)
        self.menubar.setStyleSheet('QMenu::item {'
                                   f'height: {resize.widget(20)}px;'
                                   '}')
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
        self.ps1_xa = QAction(self.menuPlayStation_1)
        self.menuPlayStation_1.addAction(self.ps1_xa)

        self.menuPlayStation_2 = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPlayStation_2.menuAction())

        self.menuPlayStation_3 = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPlayStation_3.menuAction())
        self.ps3PsarcZlib = QAction(self.menuPlayStation_3)
        self.menuPlayStation_3.addAction(self.ps3PsarcZlib)
        self.ps3PsarcLzma = QAction(self.menuPlayStation_3)
        self.menuPlayStation_3.addAction(self.ps3PsarcLzma)
        self.ps3XWS = QAction(self.menuPlayStation_3)
        self.menuPlayStation_3.addAction(self.ps3XWS)

        self.menuPlayStation_4 = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPlayStation_4.menuAction())
        self.ps4PKG_CNT = QAction(self.menuPlayStation_4)
        self.menuPlayStation_4.addAction(self.ps4PKG_CNT)

        self.menuPlayStation_5 = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPlayStation_5.menuAction())

        self.menuPSP = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPSP.menuAction())
        self.pspCSO = QAction(self.menuPSP)
        self.menuPSP.addAction(self.pspCSO)

        self.menuPlayStation_Vita = QMenu(self.menuSony)
        self.menuSony.addAction(self.menuPlayStation_Vita.menuAction())
        self.gxt2png = QAction(self.menuPlayStation_Vita)
        self.menuPlayStation_Vita.addAction(self.gxt2png)
        self.png2gxt = QAction(self.menuPlayStation_Vita)
        self.menuPlayStation_Vita.addAction(self.png2gxt)
        self.psvPsarc = QAction(self.menuPlayStation_Vita)
        self.menuPlayStation_Vita.addAction(self.psvPsarc)

        self.consolesMenu.addAction(self.menuSony.menuAction())

        # Microsoft
        self.menuMicrosoft = QMenu(self.consolesMenu)

        self.menuXBox_Classic = QMenu(self.menuMicrosoft)
        self.menuMicrosoft.addAction(self.menuXBox_Classic.menuAction())
        self.xboxISO = QAction(self.menuXBox_Classic)
        self.menuXBox_Classic.addAction(self.xboxISO)
        self.xboxAFS = QAction(self.menuXBox_Classic)
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

        self.menuWii = QMenu(self.menuNintendo)
        self.menuNintendo.addAction(self.menuWii.menuAction())
        self.wiiISO = QAction(self.menuWii)
        self.menuWii.addAction(self.wiiISO)
        self.wiiCSO = QAction(self.menuWii)
        self.menuWii.addAction(self.wiiCSO)
        self.wiiWBFS = QAction(self.menuWii)
        self.menuWii.addAction(self.wiiWBFS)
        self.wiiWDF = QAction(self.menuWii)
        self.menuWii.addAction(self.wiiWDF)

        self.menuWii_U = QMenu(self.menuNintendo)
        self.menuNintendo.addAction(self.menuWii_U.menuAction())

        self.menuSwitch = QMenu(self.menuNintendo)
        self.menuNintendo.addAction(self.menuSwitch.menuAction())
        self.switchNSP = QAction(self.menuSwitch)
        self.menuSwitch.addAction(self.switchNSP)

        self.menuClassic_Consoles = QMenu(self.menuNintendo)
        self.menuNintendo.addAction(self.menuClassic_Consoles.menuAction())
        self.nintendoSARC = QAction(self.menuClassic_Consoles)
        self.menuClassic_Consoles.addAction(self.nintendoSARC)
        self.nintendoDS_SDAT = QAction(self.menuClassic_Consoles)
        self.menuClassic_Consoles.addAction(self.nintendoDS_SDAT)

        self.consolesMenu.addAction(self.menuNintendo.menuAction())

        # Sega
        self.menuSega = QMenu(self.consolesMenu)

        self.menuDreamcast = QMenu(self.menuSega)
        self.menuSega.addAction(self.menuDreamcast.menuAction())
        self.dreamcastGDI = QAction(self.menuDreamcast)
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

        self.menu_5 = QMenu(self.menu)
        self.menu_6 = QMenu(self.menu)
        self.menu_7 = QMenu(self.menu)
        self.menu_8 = QMenu(self.menu)
        self.menu_2 = QMenu(self.menubar)
        self.videoConverters = QMenu(self.menu_2)
        self.audioConverters = QMenu(self.menu_2)
        self.imageConverters = QMenu(self.menu_2)
        self.menu_3 = QMenu(self.menubar)
        self.themes_list_2 = QMenu(self.menu_3)
        self.menu_4 = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.quickOpen = QAction(self)
        self.exitAction = QAction(self)
        self.action_Language = QMenu(self)
        self.action_SelectOutPath = QAction(self)
        self.action_ClearOutPath = QAction(self)
        self.action_CreateOutPath = QAction(self)
        self.action_Settings = QAction(self)
        self.action_DeleteEmptyFiles = QAction(self)
        self.action_DeleteEmptySubfolders = QAction(self)
        self.action_About = QAction(self)
        self.action7z_Archiver = QAction(self)
        self.actionGame_Archive_Unpacker_Plugin = QAction(self)
        self.actionTotal_Observer = QAction(self)
        self.actionSprite_and_Archive_Utility = QAction(self)
        self.actionZlib_Deflate = QAction(self)
        self.actionLZ4 = QAction(self)
        self.actionWAV = QAction(self)
        self.autoSearchScripts = QAction(self)
        self.actionFileList = QAction(self)
        self.actionArchiveScanner = QAction(self)
        self.actionFFMPEG_Video_Converter = QAction(self)
        self.actionRad_Video_Tools = QAction(self)
        self.actionMedia_Info = QAction(self)
        self.actionFFMPEG_Sound_Converter = QAction(self)
        self.actionVGM_Stream_Tools = QAction(self)
        self.actionFSBext = QAction(self)
        self.actionToWAV = QAction(self)
        self.actionRAW_to_WAV = QAction(self)
        self.actionRAW_to_Atrac = QAction(self)
        self.actionPlayStation_Audio_Converter = QAction(self)
        self.actionXWM_WAV_Audio_Converter = QAction(self)
        self.actionFFMPEG_Image_Converter = QAction(self)
        self.actionSAU = QAction(self)
        self.action_nConvert = QAction(self)
        self.actionImage_to_DDS_Microsoft = QAction(self)
        self.actionImage_to_DDS_nVidia = QAction(self)
        self.actionDDS_Header_Generator = QAction(self)
        self.actionCubeMap_Creator = QAction(self)
        self.actionICO_Icon_Splitter = QAction(self)
        self.create_theme = QAction(self)
        self.unpackWith.addAction(self.action7z_Archiver)
        self.unpackWith.addAction(self.actionGame_Archive_Unpacker_Plugin)
        self.unpackWith.addAction(self.actionTotal_Observer)
        self.unpackWith.addAction(self.actionSprite_and_Archive_Utility)
        self.zippedFormats.addAction(self.actionZlib_Deflate)
        self.zippedFormats.addAction(self.actionLZ4)
        self.formatSearch.addAction(self.actionWAV)
        self.additionalMenu.addAction(self.autoSearchScripts)
        self.additionalMenu.addAction(self.actionArchiveScanner)
        self.additionalMenu.addAction(self.actionFileList)

        self.menu.addAction(self.quickOpen)
        self.menu.addAction(self.unpackWith.menuAction())
        self.menu.addAction(self.menu_5.menuAction())
        self.menu.addAction(self.menu_6.menuAction())
        self.menu.addAction(self.consolesMenu.menuAction())
        self.menu.addAction(self.menu_7.menuAction())
        self.menu.addAction(self.menu_8.menuAction())
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
        self.audioConverters.addAction(self.actionPlayStation_Audio_Converter)
        self.audioConverters.addAction(self.actionXWM_WAV_Audio_Converter)
        self.imageConverters.addAction(self.actionFFMPEG_Image_Converter)
        self.imageConverters.addAction(self.actionSAU)
        self.imageConverters.addAction(self.action_nConvert)
        self.imageConverters.addAction(self.actionImage_to_DDS_Microsoft)
        self.imageConverters.addAction(self.actionImage_to_DDS_nVidia)
        self.imageConverters.addAction(self.actionDDS_Header_Generator)
        self.imageConverters.addAction(self.actionCubeMap_Creator)
        self.imageConverters.addAction(self.actionICO_Icon_Splitter)
        self.menu_2.addAction(self.videoConverters.menuAction())
        self.menu_2.addAction(self.audioConverters.menuAction())
        self.menu_2.addAction(self.imageConverters.menuAction())
        self.menu_3.addAction(self.action_Language.menuAction())
        self.menu_3.addAction(self.themes_list_2.menuAction())
        self.menu_3.addAction(self.create_theme)
        self.menu_3.addAction(self.action_Settings)
        self.menu_3.addAction(self.action_SelectOutPath)
        self.menu_3.addAction(self.action_ClearOutPath)
        self.menu_3.addAction(self.action_CreateOutPath)
        self.menu_3.addAction(self.action_DeleteEmptyFiles)
        self.menu_3.addAction(self.action_DeleteEmptySubfolders)
        self.menu_4.addAction(self.action_About)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
