
from PyQt5.QtCore import QCoreApplication
import source.ui.localize as TL


class Translate:

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.toolButton_plus.setText(_translate("BFGUnpacker", "+"))
        self.toolButton_minus.setText(_translate("BFGUnpacker", "-"))
        self.toolButton_Find.setText(_translate("BFGUnpacker", TL.find))
        self.btn_All_Favorite.setText(_translate("BFGUnpacker", TL.all_caps))
        self.checkBox_Reimport.setText(_translate("BFGUnpacker", TL.reimport))
        self.checkBox_ShowConsole.setText(_translate("BFGUnpacker", TL.show_console))
        self.checkBox_createSubfolders.setText(_translate("BFGUnpacker", TL.create_subfolders))
        self.menu.setTitle(_translate("BFGUnpacker", TL.file))
        self.unpackWith.setTitle(_translate("BFGUnpacker", TL.unpack_with))
        self.zippedFormats.setTitle(_translate("BFGUnpacker", TL.compress_formats))
        self.formatSearch.setTitle(_translate("BFGUnpacker", TL.find_formats))
        self.additionalMenu.setTitle(_translate("BFGUnpacker", TL.additional))
        self.consolesMenu.setTitle(_translate("BFGUnpacker", TL.consoles))
        self.menuSony.setTitle(_translate("BFGUnpacker", "Sony"))
        self.menuPlayStation_1.setTitle(_translate("BFGUnpacker", "PlayStation 1"))
        self.menuPlayStation_2.setTitle(_translate("BFGUnpacker", "PlayStation 2"))
        self.menuPlayStation_3.setTitle(_translate("BFGUnpacker", "PlayStation 3"))
        self.menuPlayStation_4.setTitle(_translate("BFGUnpacker", "PlayStation 4"))
        self.menuPlayStation_5.setTitle(_translate("BFGUnpacker", "PlayStation 5"))
        self.menuPSP.setTitle(_translate("BFGUnpacker", "PSP"))
        self.menuPlayStation_Vita.setTitle(_translate("BFGUnpacker", "PlayStation Vita"))
        self.menuMicrosoft.setTitle(_translate("BFGUnpacker", "Microsoft"))
        self.menuXBox_Classic.setTitle(_translate("BFGUnpacker", "XBox Classic"))
        self.menuXBox_One.setTitle(_translate("BFGUnpacker", "XBox One"))
        self.menuXBox_Series.setTitle(_translate("BFGUnpacker", "XBox Series"))
        self.menuNintendo.setTitle(_translate("BFGUnpacker", "Nintendo"))
        self.menuGameCube.setTitle(_translate("BFGUnpacker", "GameCube"))
        self.menuWii.setTitle(_translate("BFGUnpacker", "Wii"))
        self.menuWii_U.setTitle(_translate("BFGUnpacker", "Wii U"))
        self.menuSwitch.setTitle(_translate("BFGUnpacker", "Switch"))
        self.menuClassic_Consoles.setTitle(_translate("BFGUnpacker", "Classic Consoles"))
        self.menuSega.setTitle(_translate("BFGUnpacker", "Sega"))
        self.menuDreamcast.setTitle(_translate("BFGUnpacker", "Dreamcast"))
        self.menuMegaDrive.setTitle(_translate("BFGUnpacker", "MegaDrive"))
        self.menuSaturn.setTitle(_translate("BFGUnpacker", "Saturn"))
        self.menuSegaOther.setTitle(_translate("BFGUnpacker", TL.other))
        self.menuOtherConsoles.setTitle(_translate("BFGUnpacker", TL.other))
        self.menu_5.setTitle(_translate("BFGUnpacker", TL.archives))
        self.menu_6.setTitle(_translate("BFGUnpacker", TL.game_engines))
        self.menu_7.setTitle(_translate("BFGUnpacker", TL.disk_images))
        self.menu_8.setTitle(_translate("BFGUnpacker", TL.installers))
        self.menu_2.setTitle(_translate("BFGUnpacker", TL.convert))
        self.videoConverters.setTitle(_translate("BFGUnpacker", TL.video))
        self.audioConverters.setTitle(_translate("BFGUnpacker", TL.audio))
        self.imageConverters.setTitle(_translate("BFGUnpacker", TL.textures))
        self.menu_3.setTitle(_translate("BFGUnpacker", TL.settings))
        self.themes_list_2.setTitle(_translate("BFGUnpacker", TL.themes))
        self.menu_4.setTitle(_translate("BFGUnpacker", TL.about))
        self.quickOpen.setText(_translate("BFGUnpacker", TL.quick_open))
        self.exitAction.setText(_translate("BFGUnpacker", TL.leave))
        self.action_Language.setTitle(_translate("BFGUnpacker", TL.language))
        self.action_SelectOutPath.setText(_translate("BFGUnpacker", TL.select_out_folder))
        self.action_ClearOutPath.setText(_translate("BFGUnpacker", TL.clear_out_folder))
        self.action_CreateOutPath.setText(_translate("BFGUnpacker", TL.make_out_folder))
        self.action_Settings.setText(_translate("BFGUnpacker", TL.settings))
        self.action_DeleteEmptyFiles.setText(_translate("BFGUnpacker", TL.delete_empty_files))
        self.action_DeleteEmptySubfolders.setText(_translate("BFGUnpacker", TL.delete_empty_subfolders))
        self.action_About.setText(_translate("BFGUnpacker", TL.about))
        self.action7z_Archiver.setText(_translate("BFGUnpacker", "7z Archiver"))
        self.actionGame_Archive_Unpacker_Plugin.setText(_translate("BFGUnpacker", "Game Archive Unpacker Plugin"))
        self.actionTotal_Observer.setText(_translate("BFGUnpacker", "Total Observer"))
        self.actionSprite_and_Archive_Utility.setText(_translate("BFGUnpacker", "Sprite and Archive Utility"))
        self.actionZlib_Deflate.setText(_translate("BFGUnpacker", "Zlib, Deflate"))
        self.actionLZ4.setText(_translate("BFGUnpacker", "LZ4"))
        self.actionWAV.setText(_translate("BFGUnpacker", "WAV"))
        self.autoSearchScripts.setText(_translate("BFGUnpacker", TL.autofind))
        self.actionFileList.setText(_translate("BFGUnpacker", TL.file_list))
        self.actionArchiveScanner.setText(_translate("BFGUnpacker", TL.archive_scanner))
        self.actionFFMPEG_Video_Converter.setText(_translate("BFGUnpacker", "FFMPEG Video Converter"))
        self.actionRad_Video_Tools.setText(_translate("BFGUnpacker", "Rad Video Tools"))
        self.actionMedia_Info.setText(_translate("BFGUnpacker", "Media Info"))
        self.actionFFMPEG_Sound_Converter.setText(_translate("BFGUnpacker", "FFMPEG Sound Converter"))
        self.actionVGM_Stream_Tools.setText(_translate("BFGUnpacker", "VGM Stream Tools"))
        self.actionFSBext.setText(_translate("BFGUnpacker", "FSBext "))
        self.actionToWAV.setText(_translate("BFGUnpacker", "ToWAV"))
        self.actionRAW_to_WAV.setText(_translate("BFGUnpacker", "RAW to WAV"))
        self.actionRAW_to_Atrac.setText(_translate("BFGUnpacker", "RAW to Atrac"))
        self.actionPlayStation_Audio_Converter.setText(_translate("BFGUnpacker", "PlayStation Audio Converter"))
        self.actionXWM_WAV_Audio_Converter.setText(_translate("BFGUnpacker", "XWM\\WAV Audio Converter"))
        self.actionFFMPEG_Image_Converter.setText(_translate("BFGUnpacker", "FFMPEG Image Converter"))
        self.actionSAU.setText(_translate("BFGUnpacker", "SAU"))
        self.actionnConvert.setText(_translate("BFGUnpacker", "nConvert"))
        self.actionImage_to_DDS_Microsoft.setText(_translate("BFGUnpacker", "Image to DDS (Microsoft)"))
        self.actionImage_to_DDS_nVidia.setText(_translate("BFGUnpacker", "Image to DDS (nVidia)"))
        self.actionDDS_Header_Generator.setText(_translate("BFGUnpacker", "DDS Header Generator"))
        self.actionCubeMap_Creator.setText(_translate("BFGUnpacker", "CubeMap Creator"))
        self.actionICO_Icon_Splitter.setText(_translate("BFGUnpacker", "ICO Icon Splitter"))
        self.create_theme.setText(_translate("BFGUnpacker", TL.create_theme))
