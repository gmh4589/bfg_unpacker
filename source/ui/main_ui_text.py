
from PyQt6.QtCore import QCoreApplication
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
        self.gxt2png.setText(_translate("BFGUnpacker", f"{TL.convert} GXT2PNG"))
        self.png2gxt.setText(_translate("BFGUnpacker", f"{TL.convert} PNG2GXT"))
        self.psvPsarc.setText(_translate("BFGUnpacker", f"PSARC Extractor"))
        self.ps1_xa.setText(_translate("BFGUnpacker", "PlayStation XA"))
        self.ps3PsarcZlib.setText(_translate("BFGUnpacker", f"PSARC Extractor (ZLIB)"))
        self.ps3PsarcLzma.setText(_translate("BFGUnpacker", f"PSARC Extractor (LZMA)"))
        self.ps3XWS.setText(_translate("BFGUnpacker", "XWS File"))
        self.ps4PKG_CNT.setText(_translate("BFGUnpacker", "PKG CNT File"))
        self.pspCSO.setText(_translate("BFGUnpacker", f"PSP CSO {TL.disc_image}"))
        self.dreamcastGDI.setText(_translate("BFGUnpacker", f"GDI {TL.disc_image}"))
        self.nintendoSARC.setText(_translate("BFGUnpacker", "Nintendo SARC"))
        self.nintendoDS_SDAT.setText(_translate("BFGUnpacker", "Nintendo DS SDAT Sound"))
        self.nintendoDS_SDAT.setText(_translate("BFGUnpacker", "Nintendo DS SDAT Sound"))
        self.switchNSP.setText(_translate("BFGUnpacker", f"Switch NSP {TL.disc_image}"))
        self.wiiISO.setText(_translate("BFGUnpacker", f"Wii ISO, WBFS {TL.disc_image}"))
        self.game_cubeISO.setText(_translate("BFGUnpacker", f"Game Cube ISO {TL.disc_image}"))
        self.gcCSO.setText(_translate("BFGUnpacker", f"Game Cube CSO {TL.disc_image}"))
        self.wiiWDF.setText(_translate("BFGUnpacker", f"Wii WDF, WIA {TL.disc_image}"))
        self.gcCISO.setText(_translate("BFGUnpacker", f"Game Cube CISO {TL.disc_image}"))
        self.xboxISO.setText(_translate("BFGUnpacker", f"Xbox ISO {TL.disc_image}"))
        self.xboxAFS.setText(_translate("BFGUnpacker", "Xbox AFS Archives"))
        self.menuMicrosoft.setTitle(_translate("BFGUnpacker", "Microsoft"))
        self.menuXBox_Classic.setTitle(_translate("BFGUnpacker", "XBox Classic"))
        self.menuXBox_360.setTitle(_translate("BFGUnpacker", "XBox 360"))
        self.menuXBox_One.setTitle(_translate("BFGUnpacker", "XBox One"))
        self.menuXBox_Series.setTitle(_translate("BFGUnpacker", "XBox Series"))
        self.menuNintendo.setTitle(_translate("BFGUnpacker", "Nintendo"))
        self.menuGameCube.setTitle(_translate("BFGUnpacker", "GameCube"))
        self.menuWii.setTitle(_translate("BFGUnpacker", "Wii"))
        self.menuWii_U.setTitle(_translate("BFGUnpacker", "Wii U"))
        self.menuSwitch.setTitle(_translate("BFGUnpacker", "Switch"))
        self.menuClassic_Consoles.setTitle(_translate("BFGUnpacker", TL.classic_consoles))
        self.menuSega.setTitle(_translate("BFGUnpacker", "Sega"))
        self.menuDreamcast.setTitle(_translate("BFGUnpacker", "DreamCast"))
        self.menuMegaDrive.setTitle(_translate("BFGUnpacker", "MegaDrive"))
        self.menuSaturn.setTitle(_translate("BFGUnpacker", "Saturn"))
        self.menuSegaOther.setTitle(_translate("BFGUnpacker", TL.other))
        self.menuOtherConsoles.setTitle(_translate("BFGUnpacker", TL.other))
        self.menu_archives.setTitle(_translate("BFGUnpacker", TL.archives))
        self.menu_game_engines.setTitle(_translate("BFGUnpacker", TL.game_engines))
        self.menu_disk_images.setTitle(_translate("BFGUnpacker", TL.disk_images))
        self.menu_installers.setTitle(_translate("BFGUnpacker", TL.installers))
        self.menu_convert.setTitle(_translate("BFGUnpacker", TL.convert))
        self.videoConverters.setTitle(_translate("BFGUnpacker", TL.video))
        self.audioConverters.setTitle(_translate("BFGUnpacker", TL.audio))
        self.imageConverters.setTitle(_translate("BFGUnpacker", TL.textures))
        self.archiveConverters.setTitle(_translate("BFGUnpacker", TL.archives))
        self.menu_settings.setTitle(_translate("BFGUnpacker", TL.settings))
        self.themes_list_2.setTitle(_translate("BFGUnpacker", TL.themes))
        self.menu_about.setTitle(_translate("BFGUnpacker", TL.about))
        self.quickOpen.setText(_translate("BFGUnpacker", TL.quick_open))
        self.exitAction.setText(_translate("BFGUnpacker", TL.leave))
        self.action_Language.setTitle(_translate("BFGUnpacker", TL.language))
        self.action_SelectOutPath.setText(_translate("BFGUnpacker", TL.select_out_folder))
        self.action_ClearOutPath.setText(_translate("BFGUnpacker", TL.clear_out_folder))
        self.action_CreateOutPath.setText(_translate("BFGUnpacker", TL.make_out_folder))
        self.action_Settings.setText(_translate("BFGUnpacker", TL.settings))
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
        self.actionFindZipMethod.setText(_translate("BFGUnpacker", TL.find_zip_method))
        self.actionFFMPEG_Video_Converter.setText(_translate("BFGUnpacker", "FFMPEG Video Converter"))
        self.actionRad_Video_Tools.setText(_translate("BFGUnpacker", "Rad Video Tools"))
        self.actionMedia_Info.setText(_translate("BFGUnpacker", "Media Info"))
        self.actionFFMPEG_Sound_Converter.setText(_translate("BFGUnpacker", "FFMPEG Sound Converter"))
        self.actionVGM_Stream_Tools.setText(_translate("BFGUnpacker", "VGM Stream Tools"))
        self.actionFSBext.setText(_translate("BFGUnpacker", "FSBext"))
        self.actionToWAV.setText(_translate("BFGUnpacker", "ToWAV"))
        self.actionRAW_to_WAV.setText(_translate("BFGUnpacker", "RAW to WAV"))
        self.actionRAW_to_Atrac.setText(_translate("BFGUnpacker", "RAW to Atrac"))
        # self.actionPlayStation_Audio_Converter.setText(_translate("BFGUnpacker", "PlayStation Audio Converter"))
        self.actionXWM_WAV_Audio_Converter.setText(_translate("BFGUnpacker", "XWM\\WAV Audio Converter"))
        self.actionFFMPEG_Image_Converter.setText(_translate("BFGUnpacker", "FFMPEG Image Converter"))
        self.actionWwise_Converter.setText(_translate("BFGUnpacker", "Wwise Converter"))
        self.actionSAU.setText(_translate("BFGUnpacker", "SAU"))
        self.action_nConvert.setText(_translate("BFGUnpacker", "nConvert"))
        self.actionImage_to_DDS_Microsoft.setText(_translate("BFGUnpacker", "Image to DDS (Microsoft)"))
        self.actionImage_to_DDS_nVidia.setText(_translate("BFGUnpacker", "Image to DDS (nVidia)"))
        self.actionDDS_Header_Generator.setText(_translate("BFGUnpacker", "DDS Header Generator"))
        self.actionCubeMap_Creator.setText(_translate("BFGUnpacker", "CubeMap Creator"))
        self.actionICO_Icon_Splitter.setText(_translate("BFGUnpacker", "ICO Icon Splitter"))
        self.create_theme.setText(_translate("BFGUnpacker", TL.create_theme))
        self.menuAmigaDiskFile.setText(_translate("BFGUnpacker", "Amiga Disk File"))
        self.nintendoNitro.setText(_translate("BFGUnpacker", "Nintendo DS Nitro File System"))
        self.vag2wav.setText(_translate("BFGUnpacker", f"{TL.convert} VAG2WAV"))
        self.wav2vag.setText(_translate("BFGUnpacker", f"{TL.convert} WAV2VAG"))
        self.ps2_soundbank.setText(_translate("BFGUnpacker", "PS2 SoundBank"))
        self.ps3_atrac2wav.setText(_translate("BFGUnpacker", f"{TL.convert} Atrac2WAV"))
        self.ps3_wav2atrac.setText(_translate("BFGUnpacker", f"{TL.convert} WAV2Atrac"))
        self.msf2atrac.setText(_translate("BFGUnpacker", f"{TL.convert} MSF2Atrac"))
        self.ps4_atrac2wav.setText(_translate("BFGUnpacker", f"{TL.convert} Atrac2WAV"))
        self.ps4_wav2atrac.setText(_translate("BFGUnpacker", f"{TL.convert} WAV2Atrac"))
        self.sxd2atrac.setText(_translate("BFGUnpacker", f"{TL.convert} SXD2Atrac"))
        self.psp_atrac2wav.setText(_translate("BFGUnpacker", f"{TL.convert} Atrac2WAV"))
        self.psp_wav2atrac.setText(_translate("BFGUnpacker", f"{TL.convert} WAV2Atrac"))
        self.psv_atrac2wav.setText(_translate("BFGUnpacker", f"{TL.convert} Atrac2WAV"))
        self.psv_wav2atrac.setText(_translate("BFGUnpacker", f"{TL.convert} WAV2Atrac"))
