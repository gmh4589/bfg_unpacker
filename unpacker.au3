
#Include-once

;Стандартные библиотеки
#include <WindowsConstants.au3>
#include <GUIConstantsEx.au3>
#include <APIGdiConstants.au3>
#include <WinAPIGdi.au3>
#include <StaticConstants.au3>
#include <ComboConstants.au3>
#include <Constants.au3>
#include <File.au3>
#include <Array.au3>
#include <GDIPlus.au3>
#include <MsgboxConstants.au3>
#Include <EditConstants.au3>
#include <ButtonConstants.au3>
#include <GuiTreeView.au3>
#include <TreeviewConstants.au3>
#include <GuiMenu.au3>
#include <GuiComboBox.au3>
#include <Date.au3>
#include <Color.au3>
#include <String.au3>

;Дополнительные библиотеки
#include <ModernMenu.au3>
#include <Binary.au3>
#include <ColorPicker.au3>

;Внешние файлы
#include <src\main.au3>
#include <src\local.au3>
#include <src\menu.au3>
#include <src\program.au3>
#include <src\engines.au3>
#include <src\quickopen.au3>
#include <src\child_gui\child_gui.au3>
#include <src\child_gui\setting.au3>

;Инструменты от других авторов
#include <src\file_format\locres.au3>
#include <src\file_format\rdr.au3>

;Инструменты от автора
#include <src\file_format\erf_format.au3>
#include <src\file_format\spacesim.au3>
#include <src\file_format\ooam.au3>
#include <src\file_format\dds_tools.au3>

LocalizeRead() ;Читает локализацию, читает текст

;Основные глобальные переменные
Global $iDrive, $iDir, $iName, $iExp, $iOutputWindow, $rI, $iFavPlus = 1, $iInvert = 0, $iMouseMove = -1

;Чтение основных настроек интерфейса программы
GLobal $FavIni = @ScriptDir & "\data\favorites.ini", $iFavorites = FileRead($FavIni)

Global $iUnrealBuild = IniRead (@ScriptDir & '\unpacker.ini', 'Engine', 'Unreal', 4), _
$iUnityBuild = IniRead (@ScriptDir & '\unpacker.ini', 'Engine', 'Unity', 4), _
$iGMBuild = IniRead (@ScriptDir & '\unpacker.ini', 'Engine', 'GameMaker', 4), _
$iRPGMBuild = IniRead (@ScriptDir & '\unpacker.ini', 'Engine', 'RPGMaker', 4), _
$iRenPyBuild = IniRead (@ScriptDir & '\unpacker.ini', 'Engine', 'RenPy', 4), _
$iGroupBy = IniRead (@ScriptDir & '\unpacker.ini', 'Main', 'Group', 'Name'), _
$iUseThemes = IniRead (@ScriptDir & '\unpacker.ini', 'Main', 'UseThemes', 4), _
$iMenuColor = IniRead (@ScriptDir & '\unpacker.ini', 'Main', 'Color', '0x000000'), _
$iPrOrSp = IniRead (@ScriptDir & '\unpacker.ini', 'Main', 'OnLoad', 'Progress')

_WinAPI_AddFontResourceEx(@ScriptDir & '\data\ico\IconLib.otf', $FR_PRIVATE)
GLobal $iFontColor, $iFontColor2, $iColor1, $iColor2, $iColor3, $iFolderColor, $iRecicleColor
$bUseRGBColors = True

;Массивы для генерации меню
Global $iGameList, $iUnrealList[1] = [0], $iUnrealKeys[1] = [0], $iUnityList[1] = [0], $iGMList[1] = [0], $iRPGMList[1] = [0], $iRenPyList[1] = [0]
GLobal $abcArray = ['0-9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
Global $yearArray = ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992', '1991', '1990']
GLobal $iArchiveArray = ["7z" & $tArchive, "ACE" & $tArchive, "ALZ" & $tArchive, "ARC" & $tArchive, "ARK" & $tArchive, "ARJ" & $tArchive, "BH" & $tArchive, "BLZ" & $tArchive, "BMA" & $tArchive, "BZIP" & $tArchive, "BZIP2" & $tArchive, "CAB" & $tArchive, "CPIO" & $tArchive, "DGCA" & $tArchive, "DZ" & $tArchive, "DZIP" & $tArchive, "EGG" & $tArchive, "FPRG" & $tArchive, "FreeARC" & $tArchive, "FZIP" & $tArchive, "GCA" & $tArchive, "GZIP" & $tArchive, "HA" & $tArchive, "HRUST" & $tArchive, "JAR" & $tArchive, "LHA/LZH" & $tArchive, "LZHAM" & $tArchive, "LZMA" & $tArchive, "LZIP" & $tArchive, "LZO" & $tArchive, "LZO PKG" & $tArchive, "LZO PVR" & $tArchive, "LZSS" & $tArchive, "LZX" & $tArchive, "MBR" & $tArchive, "MHTML Web" & $tArchive, "NanoZIP" & $tArchive, "NSIS" & $tArchive, "PPMD" & $tArchive, "RAR" & $tArchive, "RPM" & $tArchive, "RPMCPIO" & $tArchive, "SIS" & $tArchive, "SQX" & $tArchive, "SWM" & $tArchive, "TAZ\TZ" & $tArchive, "TAR" & $tArchive, "TAZ" & $tArchive, "TARZIP" & $tArchive, "WIM" & $tArchive, "XPI" & $tArchive, "XXZ" & $tArchive, "XZ" & $tArchive, "YZ1" & $tArchive, "YZ2" & $tArchive, "Z" & $tArchive, "ZIP" & $tArchive, "ZIPX" & $tArchive, "ZOO" & $tArchive]

GLobal $iButtonTextArray = ['', $tQOpen, "Quick BMS", $tUnpWith & @CRLF & "7z Archiver", $tUnpWith & @CRLF & "Game Archive Unpacker Plugin", "Inno Setup Installer", $tVConv, "Unreal Engine", "Unity Engine", "idTech Engine", "Source Engine", "Creation Engine", "Cry Engine", "Bink Converter", "Wwise Audio Unpacker", $cTFolder]
Global $idTreeItemABC[27], $iSubmenuArchiveABC[27], $idTreeItemYear[UBound($yearArray)], $iArchiveItem[UBound($iArchiveArray)], $idButton[16], $iContMenu[16], $iChangeButton[16], $setBTN[27]

If $iPrOrSp = 'Splash' Then SplashImageOn("", @ScriptDir & "\data\ico\i.jpg", 256, 256, (@DesktopWidth/2)-128, (@DesktopHeight/2)-128, 19)
If $iPrOrSp = 'Progress' Then ProgressOn('', $tLoad, "", (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)

;Запуск интерфейса
$hGui = GUICreate("BFG Unpacker", 600, 630, -1, -1, $WS_OVERLAPPEDWINDOW + $WS_EX_ACCEPTFILES, $WS_EX_ACCEPTFILES)
GUISetIcon (@ScriptDir & "\data\ico\i.ico")

;Чтение списка игр из таблиц
_FileReadToArray(@ScriptDir & '\game_list\main_list.csv', $iGameList)

If $iUnrealBuild = 1 Then _FileReadToArray(@ScriptDir & '\game_list\unreal_list.csv', $iUnrealList)
_ArrayConcatenate($iGameList, $iUnrealList, 2)
If $iUnityBuild = 1 Then _FileReadToArray(@ScriptDir & '\game_list\unity_list.csv', $iUnityList)
_ArrayConcatenate($iGameList, $iUnityList, 2)
If $iGMBuild = 1 Then _FileReadToArray(@ScriptDir & '\game_list\gamemaker_list.csv', $iGMList)
_ArrayConcatenate($iGameList, $iGMList, 2)
If $iRPGMBuild = 1 Then _FileReadToArray(@ScriptDir & '\game_list\rpgmaker_list.csv', $iRPGMList)
_ArrayConcatenate($iGameList, $iRPGMList, 2)
If $iRenPyBuild = 1 Then _FileReadToArray(@ScriptDir & '\game_list\renpy_list.csv', $iRenPyList)
_ArrayConcatenate($iGameList, $iRenPyList, 2)

_ArraySort($iGameList, 0, 2)

Global $iLoop = UBound($iGameList)-1, $iMenuItem[$iLoop+1], $iListFind[$iLoop+1], $iYearList[$iLoop+1]

FolderProbe() ;Проверяет выходную папку, предлагает создать ее, если ее нет

Global $idTreeView_1 = GUICtrlCreateTreeView(5, 65, 290, 525)

GUICtrlSetTip(-1, $tListT)
Global $idTreeItem = GUICtrlCreateTreeViewItem($tListT, $idTreeView_1)

;Сортировка списка игр по названию либо году выпуска
If $iGroupBy <> BitOR ('Name', 'Year') Then
	IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Group', 'Name')
	$iGroupBy = 'Name'
EndIf

If $iGroupBy = 'Name' Then
		For $set = 0 to 26
			$idTreeItemABC[$set] = GUICtrlCreateTreeViewItem($abcArray[$set], $idTreeItem)
		Next
	Global $idTreeItemOther = GUICtrlCreateTreeViewItem("Other", $idTreeItem) 
	
ElseIf $iGroupBy = 'Year' Then
	Global $idTreeItemUnk = GUICtrlCreateTreeViewItem("Unknown", $idTreeItem)
		For $set = 0 to UBound($yearArray)-1
			$idTreeItemYear[$set] = GUICtrlCreateTreeViewItem($yearArray[$set], $idTreeItem)
		Next
	Global $idTreeItem1980 = GUICtrlCreateTreeViewItem("1970-1989", $idTreeItem)
EndIf

;Создает и наполняет список игр
For $item = 2 to $iLoop
	$iGameName = StringSplit($iGameList[$item], '	')
	If $iGroupBy = 'Name' Then $idItem = getChar(StringLeft($iGameName[1], 2))
	If $iGroupBy = 'Year' Then $idItem = getYear($iGameName[2])
	$iMenuItem[$item] = GUICtrlCreateTreeViewItem($iGameName[1], $idItem)
	$iListFind[$item] = $iGameName[1]
	$iYearList[$item] = $iGameName[2]
	$Percent = (100/$iLoop) * $item
	If $iPrOrSp = 'Progress' Then 
		If Mod($item, 1000) = 0 Then ProgressSet ($Percent, $item & '\' & $iLoop)
	EndIf
Next
	
Global $iLST = _ArrayToString($iListFind)
If $iPrOrSp = 'Progress' Then ProgressOff()
If $iPrOrSp = 'Splash' Then SplashOff()

Func getChar($iChar)
	If StringIsASCII($iChar) = 1 Then 
		$iChar = StringLeft(StringLower($iChar), 1)
			Local $nChar = _ArraySearch($abcArray, $iChar)
			If $nChar > -1 Then Return $idTreeItemABC[$nChar]
			If StringIsInt($iChar) = 1 Then Return $idTreeItemABC[0]
			If StringIsASCII($iChar) = 1 Then Return $idTreeItemOther
	Else
		Return $idTreeItemOther
	EndIf
EndFunc

Func getYear($iYear)
	If StringIsInt($iYear) = 1 Then 
		If $iYear < 1990 Then Return $idTreeItem1980
		If $iYear > 1989 Then Return $idTreeItemYear[_ArraySearch($yearArray, $iYear)]
	Else
		Return $idTreeItemUnk
	EndIf
EndFunc

GUICtrlSetState($idTreeItem, $GUI_EXPAND + $GUI_DROPACCEPTED)

;Создает остальной интерфейс
$iAll_Checkbox = GUICtrlCreateLabel($tFav2, 5, 42, 43, 20, $SS_CENTER+$SS_CENTERIMAGE)
	GUICtrlSetTip(-1, $tClick1 & @CRLF & $tClick2)
	GUICtrlSetResizing ($iAll_Checkbox, $GUI_DOCKSIZE)

$iFindMenu = GUICtrlCreateCombo('', 50, 42, 430, 20)
	GUICtrlSetData($iFindMenu, $iFavorites, "")
	
$iFindBTN = GUICtrlCreateLabel ($tFind, 527, 42, 70, 20, $SS_CENTER+$SS_CENTERIMAGE)
	GUICtrlSetTip(-1, $tFind)
	GUICtrlSetResizing ($iFindBTN, $GUI_DOCKSIZE)
	
$iFavAdd = GUICtrlCreateLabel ('+', 505, 42, 20, 20, $SS_CENTER+$SS_CENTERIMAGE)
	GUICtrlSetTip(-1, $tA2Fav)
	GUICtrlSetResizing ($iFavAdd, $GUI_DOCKSIZE)

$iFavDel = GUICtrlCreateLabel ('-', 483, 42, 20, 20, $SS_CENTER+$SS_CENTERIMAGE)
	GUICtrlSetTip(-1, $tD2Fav)
	GUICtrlSetResizing ($iFavDel, $GUI_DOCKSIZE)
	
#Region //Menu
#Region //File
	Global $iFileMenu = GUICtrlCreateMenu($tFile)
	$iOpenQuick = _GUICtrlCreateODMenuItem($tQOpen, $iFileMenu)

	$iSubmenu1 = _GUICtrlCreateODMenu($tUnpWith, $iFileMenu)
	;Распаковать с помощью
	$iTotal7zip = _GUICtrlCreateODMenuItem("Total 7z Archiver", $iSubmenu1)
	$iGAUP = _GUICtrlCreateODMenuItem("Game Archive Unpacker Plugin", $iSubmenu1)
	$iObserver = _GUICtrlCreateODMenuItem("Total Observer", $iSubmenu1)
	$iSAU = _GUICtrlCreateODMenuItem("Sprite and Archive Utility", $iSubmenu1)

#Region //Engine
	$iSubMenuEngine = _GUICtrlCreateODMenu($tEngine, $iFileMenu)
	;Игровые движки
	$iUnpack816 = _GUICtrlCreateODMenuItem("Acknex Engine", $iSubMenuEngine)
	$iAnvil = _GUICtrlCreateODMenuItem("Anvil\Scimitar Engine", $iSubMenuEngine)
	$iAsura = _GUICtrlCreateODMenuItem("Asura Engine", $iSubMenuEngine)
	$iAurora = _GUICtrlCreateODMenuItem("Aurora Engine", $iSubMenuEngine)
	$iChromeEngine = _GUICtrlCreateODMenuItem("Chrome Engine", $iSubMenuEngine)
	$iConstruct = _GUICtrlCreateODMenuItem("Construct Engine", $iSubMenuEngine)
	$iBethesda = _GUICtrlCreateODMenuItem("Creation Engine", $iSubMenuEngine)
	$iCryEngine = _GUICtrlCreateODMenuItem("Cry Engine", $iSubMenuEngine)
	$iGameMaker = _GUICtrlCreateODMenuItem("GameMaker", $iSubMenuEngine)
	$iGodot = _GUICtrlCreateODMenuItem("Godot Engine", $iSubMenuEngine)
	;$iDunia = _GUICtrlCreateODMenuItem("Dunia Engine", $iSubMenuEngine)
	$iFoxEngine = _GUICtrlCreateODMenuItem("Fox Engine", $iSubMenuEngine)
	$iFPS_Creator = _GUICtrlCreateODMenuItem("FPS Creator", $iSubMenuEngine)
	$iFrostBite = _GUICtrlCreateODMenuItem("FrostBite Engine", $iSubMenuEngine)
	$iGameloft = _GUICtrlCreateODMenuItem("Gameloft", $iSubMenuEngine) 
	$iGlacier = _GUICtrlCreateODMenuItem("Glacier Engine", $iSubMenuEngine)
	$iHuneX = _GUICtrlCreateODMenuItem("HuneX Engine", $iSubMenuEngine) ; не удалось найти ни одной игры на этом движке, есть студия HuneX, и это явно их движок, судя по всему - игр на нем много, но... Hunex выпускает игры и на других движках, а на собственно HuneX Engine игры выпускают, вероятно, и другие разрабы.
	$iDTech = _GUICtrlCreateODMenuItem("iDTech Engine", $iSubMenuEngine)
	$Infinity = _GUICtrlCreateODMenuItem("Infinity Engine", $iSubMenuEngine) 
	$iLithTech = _GUICtrlCreateODMenuItem("LithTech Engine", $iSubMenuEngine)
	$iMTFramework = _GUICtrlCreateODMenuItem("MT Framework", $iSubMenuEngine)
	$iPopCapPackAll = _GUICtrlCreateODMenuItem("PopCap Games", $iSubMenuEngine)
	$iReEngine = _GUICtrlCreateODMenuItem("RE Engine", $iSubMenuEngine)
	$iRedEngine = _GUICtrlCreateODMenuItem("RED Engine", $iSubMenuEngine)
	$iRenPy = _GUICtrlCreateODMenuItem("RenPy Engine", $iSubMenuEngine)
	$iRPGMaker = _GUICtrlCreateODMenuItem("RPG Maker", $iSubMenuEngine) ; добавить поддержку новых версий
	$iShiVa = _GUICtrlCreateODMenuItem("ShiVa Engine", $iSubMenuEngine) ; протестировать
	$iOpenSWF = _GUICtrlCreateODMenuItem("Shockwave Flash", $iSubMenuEngine)
	$iSource = _GUICtrlCreateODMenuItem("Source Engine", $iSubMenuEngine) 
	;$iUnpack1203 = _GUICtrlCreateODMenuItem("Ubisoft [Language] sorter", $iSubMenuEngine) ; что это вообще???
	;$iUnpack1151 = _GUICtrlCreateODMenuItem("Ubisoft Montreal - big/fat/000 archives", $iSubMenuEngine) ; ↓ - объединить
	;$iUnpack1204 = _GUICtrlCreateODMenuItem("Ubisoft Montreal - fat/000 archives", $iSubMenuEngine) ; ↑ - объединить
	$iUnigenex = _GUICtrlCreateODMenuItem("Unigene", $iSubMenuEngine)
	$iUnity = _GUICtrlCreateODMenuItem("Unity 3D Engine", $iSubMenuEngine)
	$iUnreal = _GUICtrlCreateODMenuItem("Unreal Engine", $iSubMenuEngine)
	$iOpenXNA = _GUICtrlCreateODMenuItem("XNA Framework", $iSubMenuEngine)
#EndRegion

#Region //Installers
	$iSubmenuInstaller = _GUICtrlCreateODMenu ($tInstaller, $iFileMenu)
	;Инсталляторы
	$iTotal7zip01 = _GUICtrlCreateODMenuItem("Amiga OS Installer (LHA)", $iSubmenuInstaller)
	$iOpenAPK = _GUICtrlCreateODMenuItem("Android Installer", $iSubmenuInstaller)
	$iTotal7zip06 = _GUICtrlCreateODMenuItem("Debian Installer (DEB)", $iSubmenuInstaller)
	$iInstExpl1 = _GUICtrlCreateODMenuItem("Eschalon Installer", $iSubmenuInstaller)
	$FreeArcEXE = _GUICtrlCreateODMenuItem("FreeArc Installer", $iSubmenuInstaller)
	$iOpenGadget = _GUICtrlCreateODMenuItem("Gadget Windows Installer", $iSubmenuInstaller)
	$iTotal7zip02 = _GUICtrlCreateODMenuItem("GCW-Zero Installer (OPK)", $iSubmenuInstaller)
	$iInstExpl2 = _GUICtrlCreateODMenuItem("Gentee Installer", $iSubmenuInstaller)
	$iInnoUnpacker = _GUICtrlCreateODMenuItem("Inno Setup Installer", $iSubmenuInstaller)
	$iOpenI20 = _GUICtrlCreateODMenuItem("Install4j Installer", $iSubmenuInstaller)
	$iInstallShield = _GUICtrlCreateODMenuItem("InstallShield Installer", $iSubmenuInstaller)
	$iOpenIOS = _GUICtrlCreateODMenuItem("iOS Installer", $iSubmenuInstaller)
	$iTotal7zip03 = _GUICtrlCreateODMenuItem("Java Installer", $iSubmenuInstaller)
	$iTotal7zip04 = _GUICtrlCreateODMenuItem("Linux Installer (TAR)", $iSubmenuInstaller)
	$OpenTAR = _GUICtrlCreateODMenuItem("Linux Installer (TARZIP)", $iSubmenuInstaller)
	$iOpenDMG = _GUICtrlCreateODMenuItem("Mac OS Installer (DMG)", $iSubmenuInstaller)
	$ObserverMSI = _GUICtrlCreateODMenuItem("MSI Windows Installer", $iSubmenuInstaller)
	$iInstExpl3 = _GUICtrlCreateODMenuItem("Nullsoft Installer", $iSubmenuInstaller)
	$iObserver_ = _GUICtrlCreateODMenuItem("Setup Factory Installer", $iSubmenuInstaller)
	$Total7zipEXE = _GUICtrlCreateODMenuItem("SFX Archive Installer", $iSubmenuInstaller)
	$iSISUnpack = _GUICtrlCreateODMenuItem("Symbian SIS Installer", $iSubmenuInstaller)
	$iSMIUnpack = _GUICtrlCreateODMenuItem("Smart Install Maker Installer", $iSubmenuInstaller)
	$iOpenXAP = _GUICtrlCreateODMenuItem("Windows Mobile Installer (XAP)", $iSubmenuInstaller)
	$iInstExpl4 = _GUICtrlCreateODMenuItem("Vise Installer", $iSubmenuInstaller)
	$iObserver_ = _GUICtrlCreateODMenuItem("Wise Installer", $iSubmenuInstaller)
	$iTotal7zip05 = _GUICtrlCreateODMenuItem("ZIP Installer", $iSubmenuInstaller)
	$iOpenZ9 = _GUICtrlCreateODMenuItem("ZLB Installer", $iSubmenuInstaller)
#EndRegion

#Region //Archives
	$iSubmenuArchive = _GUICtrlCreateODMenu($tArchives, $iFileMenu)
		For $set = 0 to 26
			$iSubmenuArchiveABC[$set] = _GUICtrlCreateODMenu($abcArray[$set], $iSubmenuArchive)
		Next
	
		For $arc = 0 to UBound($iArchiveArray)-1
			$iArchiveItem[$arc] = _GUICtrlCreateODMenuItem($iArchiveArray[$arc], getCharArc(StringLeft($iArchiveArray[$arc], 1)))
		Next
	
	Func getCharArc($iChar)
		If StringIsInt($iChar) = 1 Then Return $iSubmenuArchiveABC[0]
		Return $iSubmenuArchiveABC[_ArraySearch($abcArray, $iChar)]
	EndFunc

#EndRegion

#Region //Consoles
	$iSubmenuConsoles = _GUICtrlCreateODMenu($tConsoles, $iFileMenu)
	;Игровые консоли
	$iSubmenuPSARC = _GUICtrlCreateODMenu("PS3 - PSARC Archive", $iSubmenuConsoles)
	$iPSARC_zlib = _GUICtrlCreateODMenuItem("ZLIB", $iSubmenuPSARC)
	$iPSARC_lzma = _GUICtrlCreateODMenuItem("LZMA", $iSubmenuPSARC)
	$iISOCompressor1 = _GUICtrlCreateODMenuItem("PSP - CSO Disc Image", $iSubmenuConsoles)
	$iTotal7zip7 = _GUICtrlCreateODMenuItem("PS Vita - VPK Disc Image", $iSubmenuConsoles)
	$iNSPSwitch = _GUICtrlCreateODMenuItem("Switch - NSP Disc Image", $iSubmenuConsoles)
	$iISOCompressor2 = _GUICtrlCreateODMenuItem("Wii - ISO Disc Image", $iSubmenuConsoles)
	$iWiiISO = _GUICtrlCreateODMenuItem("Wii\DreamCube - ISO Disc Image", $iSubmenuConsoles)
	$iXboxISO = _GUICtrlCreateODMenuItem("Xbox - ISO Disc Image", $iSubmenuConsoles)
#EndRegion

#Region //Disc Image
	$iSubmenuDiscImage = _GUICtrlCreateODMenu($tDImage, $iFileMenu)
	;Образы дисков
	$iObserver_ = _GUICtrlCreateODMenuItem("BIN Disc Image (CUE/BIN)", $iSubmenuDiscImage)
	$iCDImage = _GUICtrlCreateODMenuItem("CDI\CDR Disc Image", $iSubmenuDiscImage)
	$iTotal7zip1 = _GUICtrlCreateODMenuItem("CramFS Image", $iSubmenuDiscImage)
	$iTotal7zip2 = _GUICtrlCreateODMenuItem("FAT File System Image", $iSubmenuDiscImage)
	$iTotal7zip3 = _GUICtrlCreateODMenuItem("FHS File System Image", $iSubmenuDiscImage)
	$iOpenISO = _GUICtrlCreateODMenuItem("ISO Disc Image", $iSubmenuDiscImage)
	$iISZconv = _GUICtrlCreateODMenuItem("ISZ Disc Image", $iSubmenuDiscImage)
	$iObserver_ = _GUICtrlCreateODMenuItem("MDF Disc Image (MDF/MDS)", $iSubmenuDiscImage)
	$iObserver_ = _GUICtrlCreateODMenuItem("NRG Disc Image", $iSubmenuDiscImage)
	$iTotal7zip4 = _GUICtrlCreateODMenuItem("NTFS File System Image", $iSubmenuDiscImage)
	$iTotal7zip5 = _GUICtrlCreateODMenuItem("SquashFS Image", $iSubmenuDiscImage)
	$iOpenUDF = _GUICtrlCreateODMenuItem("UDF Disc Image", $iSubmenuDiscImage)
	$iTotal7zip6 = _GUICtrlCreateODMenuItem("VHD Disc Image", $iSubmenuDiscImage)
#EndRegion

	$iSubmenu3 = _GUICtrlCreateODMenu($tCompFormat, $iFileMenu)
	;Форматы сжатия
	$iZLib = _GUICtrlCreateODMenuItem("ZLib, Deflate", $iSubmenu3)
	$ilz4_decompress = _GUICtrlCreateODMenuItem("LZ4", $iSubmenu3)

	$iSubmenuSearch = _GUICtrlCreateODMenu($tFSerch, $iFileMenu)
	$iWavSearch = _GUICtrlCreateODMenuItem("WAV", $iSubmenuSearch)
	; $iOGGSearch = _GUICtrlCreateODMenuItem("OGG", $iSubmenuSearch)
	; $iDDSSearch = _GUICtrlCreateODMenuItem("DDS", $iSubmenuSearch)
	; $iBinkSearch = _GUICtrlCreateODMenuItem("Bink", $iSubmenuSearch)
	; $iBink2Search = _GUICtrlCreateODMenuItem("Bink 2", $iSubmenuSearch)
	; $iOtherSearch = _GUICtrlCreateODMenuItem($tOtherF, $iSubmenuSearch) 

	$iSubmenu5 = _GUICtrlCreateODMenu($tAdv, $iFileMenu)
	$iAutoSearch = _GUICtrlCreateODMenuItem($ASearch, $iSubmenu5)
	$iArchiveScan = _GUICtrlCreateODMenuItem($AScan, $iSubmenu5)
	$iFileList = _GUICtrlCreateODMenuItem($Flist, $iSubmenu5)

	$iExit = _GUICtrlCreateODMenuItem($tExit, $iFileMenu)
#EndRegion

#Region //Converter
	$iConvMenu = GUICtrlCreateMenu($tConv)
	$iConvMenu1 = _GUICtrlCreateODMenu($tVideo, $iConvMenu)
	$iConv_12 = _GUICtrlCreateODMenuItem("FFMPEG Video Converter" , $iConvMenu1)
	$iBink2avi = _GUICtrlCreateODMenuItem("RAD Video Tools", $iConvMenu1)
	$iMediaInfo = _GUICtrlCreateODMenuItem("MediaInfo", $iConvMenu1)

	$iConvMenu2 = _GUICtrlCreateODMenu($tAudio, $iConvMenu)
	$iConv_15 = _GUICtrlCreateODMenuItem("FFMPEG Sound Converter", $iConvMenu2)
	$iVGM = _GUICtrlCreateODMenuItem("VGM Stream Tools", $iConvMenu2)
	$iFSBext = _GUICtrlCreateODMenuItem("FSBext (FSB " & $tTo & " WAV\MP3\OGG)", $iConvMenu2)
	$iToWAV = _GUICtrlCreateODMenuItem("ToWAV (FSB, XWB " & $toTo & " WAV\MP3\OGG )", $iConvMenu2)
	$iConv_5 = _GUICtrlCreateODMenuItem("Wwise Converter", $iConvMenu2)
	$iConv_6 = _GUICtrlCreateODMenuItem("RAW " & $tTo & "WAV", $iConvMenu2)
	$iConv_11 = _GUICtrlCreateODMenuItem("RAW " & $tTo & "Atrac", $iConvMenu2)
	$iConv_13 = _GUICtrlCreateODMenuItem("PlayStation Audio Converter", $iConvMenu2)
	$iConv_18 = _GUICtrlCreateODMenuItem("XWM\WAV Audio Converter", $iConvMenu2)

	$iConvMenu3 = _GUICtrlCreateODMenu($tTextures, $iConvMenu)
	$iConv_14 = _GUICtrlCreateODMenuItem("FFMPEG Image Converter", $iConvMenu3)
	$iConv_3 = _GUICtrlCreateODMenuItem($tTexturesIn & " PNG (SAU)", $iConvMenu3)
	$iConv_4 = _GUICtrlCreateODMenuItem("nCovert Image Converter", $iConvMenu3)
	$iConv_16 = _GUICtrlCreateODMenuItem("Image to DDS converter (by Microsoft)", $iConvMenu3)
	$iConv_17 = _GUICtrlCreateODMenuItem("Image to DDS converter (by nVidia)", $iConvMenu3)
	$iConv_10 = _GUICtrlCreateODMenuItem("DDS Header Generator", $iConvMenu3)
	$iCubeMapCreator = _GUICtrlCreateODMenuItem("CubeMap Creator", $iConvMenu3)

#EndRegion

#Region //Setting
	$iSettingMenu = GUICtrlCreateMenu ($tSetting)
	$iSelectLang = _GUICtrlCreateODMenuItem($tLang, $iSettingMenu)
	$iOpenINI = _GUICtrlCreateODMenuItem($tOpenINI, $iSettingMenu)
	$iSelectFolder = _GUICtrlCreateODMenuItem($sTFolder, $iSettingMenu)
	$iClearFolder = _GUICtrlCreateODMenuItem($cTFolder, $iSettingMenu)
	$iMakeFolder = _GUICtrlCreateODMenuItem($mTFolder, $iSettingMenu)
	$iDeFo = _GUICtrlCreateODMenuItem($delEFolder, $iSettingMenu)
	$iDeFi = _GUICtrlCreateODMenuItem($delEFile, $iSettingMenu)
#EndRegion

#Region //About

	$iAboutMenu = GUICtrlCreateMenu ($tAbout)
	$iAbout = _GUICtrlCreateODMenuItem($tAP, $iAboutMenu)

#EndRegion
#EndRegion

#Region //Checkbox
	$iReimport_Checkbox = GUICtrlCreateCheckbox('', 10, 590, 15, 20)
	$iHideOrShow = GUICtrlCreateCheckbox('', 90, 590, 15, 20)
	$iReimport_CheckboxTXT = GUICtrlCreateLabel($tPack, 25, 593, 55, 20)
	$iHideOrShowTXT = GUICtrlCreateLabel($tShowCon, 105, 593, 120, 20)
	GUICtrlSetState($iHideOrShow, $GUI_CHECKED)
	$iAllGamesLabel = GUICtrlCreateLabel($tAllGames & $iLoop, 300, 595, 200, 20)
#EndRegion

#Region //OutWindow
	$iEdit = GUICtrlCreateEdit($tAction & @CRLF, 300, 65, 295, 525, $ES_AUTOVSCROLL + $WS_VSCROLL + $ES_NOHIDESEL + $ES_WANTRETURN)
		GUICtrlSendMsg($iEdit, $EM_LIMITTEXT, -1, 0)
#EndRegion

Global $iIconsArray = [[0, 0], [30, $tQOpen], [30, "Quick BMS"], [40, $tUnpWith & @CRLF & "7z Archiver"], [40, $tUnpWith & @CRLF & "Game Archive Unpacker Plugin"], [40, "Inno Setup Installer"], [40, $tVConv], [40, "Unreal Engine"], [40, "Unity Engine"], [40, "idTech Engine"], [30, "Source Engine"], [32, "Creation Engine"], [35, "Cry Engine"], [40, "Bink Converter"], [40, "Wwise Audio Unpacker"], [30, 'PS Audio Converter'], [30, 'NCONVERT GUI'], [40, 'RED Engine'], [35, 'Godot Engine'], [20, 'RPG Maker'], [50, 'RenPy Engine'], [10, 'Unigene Engine'], [40, 'RAW to DDS'], [40, 'RAW to Atrac'], [40, 'RAW to WAV'], [30, $tSetting], [30, $cTFolder]]

#Region //ImageButton
	For $i = 1 to 15
		$iBtnName = IniRead (@ScriptDir & '\unpacker.ini', 'Button', 'Button' & $i, $abcArray[$i])
		If $i = 1 Then $iBtnName = "A"
		If $i = 15 Then $iBtnName = "Z"
		$idButton[$i] = GUICtrlCreateLabel($iBtnName, 40*$i-40, 0, 40, 40, $SS_CENTER+$SS_CENTERIMAGE)
		GUICtrlSetTip(-1, $iIconsArray[_ArraySearch($abcArray, $iBtnName)][1])
		GUICtrlSetFont(-1, $iIconsArray[_ArraySearch($abcArray, $iBtnName)][0], 400, 0, "IconLib")
		GUICtrlSetResizing (-1, $GUI_DOCKALL)
	Next
	;TODO Текст на русском!
	For $i = 2 to 14
		$iContMenu[$i] = GUICtrlCreateContextMenu ($idButton[$i])
		$iChangeButton[$i] = GUICtrlCreateMenuItem ("Настроить кнопку", $iContMenu[$i])
		GUICtrlCreateMenuItem ($tCancel, $iContMenu[$i])
	Next
	
	$iContMenuTrash = GUICtrlCreateContextMenu ($idButton[15])
	$iDeleteToTrash = GUICtrlCreateMenuItem ("Удалить в корзину", $iContMenuTrash)
	$iDeleteFull = GUICtrlCreateMenuItem ("Удалить полностью", $iContMenuTrash)
	GUICtrlCreateMenuItem ($tCancel, $iContMenuTrash)
#EndRegion

_SetColor()

#Region //Colors
Func _SetColor()
	$iFolderColor = 0xFFE68E
	$iRecicleColor = 0x0099FF
	If $iUseThemes = 4 Then
		If BitAND(Not StringIsXDigit($iMenuColor), $iUseThemes = 4) Then $iMenuColor = 0xFFFFFF
		$ColorArray = StringRegExp(Hex($iMenuColor), '\N\N', 3)

		$rC = (Dec($ColorArray[1]) + Dec('66'))/2
		$gC = (Dec($ColorArray[2]) + Dec('66'))/2
		$bC = (Dec($ColorArray[3]) + Dec('66'))/2

		$iColor1 = $iMenuColor
		$iColor2 = '0x' & Hex(Int($rC), 2) & Hex(Int($gC), 2) & Hex(Int($bC), 2)
		$iColor3 = '0x' & Hex(Int($bC), 2) & Hex(Int($gC), 2) & Hex(Int($rC), 2)
		If BitOR($rC, $gC, $bC) < 0xFF / 2 Then $iFontColor = 0xFFFFFF
		If BitOR($rC, $gC, $bC) < 0xFF / 2 Then $iFontColor2 = 0xFFFFFF
		If BitOR($rC, $gC, $bC) > 0xFF / 2 Then $iFontColor = 0x000000
		If BitOR($rC, $gC, $bC) > 0xFF / 2 Then $iFontColor2 = 0x000000
		If $iColor1 = $iColor3 Then $iColor3 = $iColor2
	EndIf
	
	If $iUseThemes = 1 Then
		If BitAND($iMenuColor = '', $iUseThemes = 1) Then $iMenuColor = "Classic"
		If $iMenuColor = 'Classic' then
			$iColor1 = 0xFFFFFF
			$iColor2 = 0xFFFFFF
			$iColor3 = 0xC0C0C0
			$iFontColor = 0x000000
			$iFontColor2 = 0x000000
		Else
			$iColor1 = IniRead (@ScriptDir & '\data\themes\' & $iMenuColor & '.ini', 'Main', 'Color1', 0xFFFFFF)
			$iColor2 = IniRead (@ScriptDir & '\data\themes\' & $iMenuColor & '.ini', 'Main', 'Color2', 0xFFFFFF)
			$iColor3 = IniRead (@ScriptDir & '\data\themes\' & $iMenuColor & '.ini', 'Main', 'Color3', 0xC0C0C0)
			$iFontColor = IniRead (@ScriptDir & '\data\themes\' & $iMenuColor & '.ini', 'Main', 'FontColor', 0x000000)
			$iFontColor2 = IniRead (@ScriptDir & '\data\themes\' & $iMenuColor & '.ini', 'Main', 'FontColor2', 0x000000)
			$iFolderColor = IniRead (@ScriptDir & '\data\themes\' & $iMenuColor & '.ini', 'Main', 'FolderColor', 0xFFE68E)
			$iRecicleColor = IniRead (@ScriptDir & '\data\themes\' & $iMenuColor & '.ini', 'Main', 'RecicleColor', 0x0099FF)
		EndIf
	EndIf
	
	GUISetBkColor($iColor2, $hGUI)
	GUICtrlSetBkColor ($iEdit, $iColor1)
	GUICtrlSetBkColor ($idTreeView_1, $iColor1)
	_SetMenuBkColor ($iColor1)
	_SetMenuIconBkColor($iColor2)
	_SetMenuSelectBkColor($iColor3)
	_SetMenuSelectTextColor($iFontColor)
	_SetMenuTextColor($iFontColor)
	GUICtrlSetColor($iEdit, $iFontColor)
	GUICtrlSetColor($idTreeView_1, $iFontColor)
	GUICtrlSetColor($iReimport_Checkbox, $iFontColor2)
	GUICtrlSetColor($iHideOrShow, $iFontColor2)
	GUICtrlSetColor($iAllGamesLabel, $iFontColor2)
	
	GUICtrlSetBkColor($iAll_Checkbox, $iColor1)
	GUICtrlSetColor($iAll_Checkbox, $iFontColor)
	GUICtrlSetBkColor($iFindBTN, $iColor1)
	GUICtrlSetColor($iFindBTN, $iFontColor)
	GUICtrlSetBkColor($iFavAdd, $iColor1)
	GUICtrlSetColor($iFavAdd, $iFontColor)
	GUICtrlSetBkColor($iFavDel, $iColor1)
	GUICtrlSetColor($iFavDel, $iFontColor)
	
	GUICtrlSetColor($iReimport_CheckboxTXT, $iFontColor2)
	GUICtrlSetColor($iHideOrShowTXT, $iFontColor2)
	
	For $i = 1 to 15
		GUICtrlSetColor($idButton[$i], $iFontColor)
		If $i = 1 Then GUICtrlSetColor($idButton[$i], $iFolderColor)
		If $i = 15 Then GUICtrlSetColor($idButton[$i], $iRecicleColor)
		GUICtrlSetBkColor($idButton[$i], $iColor1)
	Next
EndFunc
#EndRegion

#Region //Icon
	_GUICtrlODMenuItemSetIcon ($iOpenQuick, "shell32.dll", 5)
	_GUICtrlODMenuItemSetIcon ($iChromeEngine, @ScriptDir & "\data\ico\chrome.ico")
	_GUICtrlODMenuItemSetIcon ($iBethesda, @ScriptDir & "\data\ico\creation.ico")
	_GUICtrlODMenuItemSetIcon ($iCryEngine, @ScriptDir & "\data\ico\cry.ico")
	_GUICtrlODMenuItemSetIcon ($iFPS_Creator, @ScriptDir & "\data\ico\fps.ico")
	_GUICtrlODMenuItemSetIcon ($iFrostBite, @ScriptDir & "\data\ico\fb.ico")
	_GUICtrlODMenuItemSetIcon ($iDTech, @ScriptDir & "\data\ico\id.ico")
	_GUICtrlODMenuItemSetIcon ($Infinity, @ScriptDir & "\data\ico\Infinity.ico")
	_GUICtrlODMenuItemSetIcon ($iMTFramework, @ScriptDir & "\data\ico\mtf.ico")
	_GUICtrlODMenuItemSetIcon ($iPopCapPackAll, @ScriptDir & "\data\ico\popcap.ico")
	_GUICtrlODMenuItemSetIcon ($iRenPy, @ScriptDir & "\data\ico\renpy.ico")
	_GUICtrlODMenuItemSetIcon ($iRPGMaker, @ScriptDir & "\data\ico\rpgm.ico")
	_GUICtrlODMenuItemSetIcon ($iOpenSWF, @ScriptDir & "\data\ico\flash.ico")
	_GUICtrlODMenuItemSetIcon ($iSource, @ScriptDir & "\data\ico\source.ico")
	_GUICtrlODMenuItemSetIcon ($iUnity, @ScriptDir & "\data\ico\unity.ico")
	_GUICtrlODMenuItemSetIcon ($iUnreal, @ScriptDir & "\data\ico\unreal.ico")
	_GUICtrlODMenuItemSetIcon ($iOpenXNA, @ScriptDir & "\data\ico\xna.ico")
	_GUICtrlODMenuItemSetIcon ($iTotal7zip, @ScriptDir & "\data\7zip\7zG.exe", 0)
	_GUICtrlODMenuItemSetIcon ($iGAUP, @ScriptDir & "\data\ico\gaup_logo.ico")
	_GUICtrlODMenuItemSetIcon ($iConv_12, @ScriptDir & "\Data\ico\ffmpeg.ico")
	_GUICtrlODMenuItemSetIcon ($iBink2avi, @ScriptDir & "\data\RADVideo\radvideo64.exe", 0)
	_GUICtrlODMenuItemSetIcon ($iMediaInfo, @ScriptDir & "\data\ico\MediaInfo.ico")
	_GUICtrlODMenuItemSetIcon ($iConv_15, @ScriptDir & "\Data\ico\ffmpeg.ico")
	_GUICtrlODMenuItemSetIcon ($iConv_5, @ScriptDir & "\data\ico\wwise.ico")
	_GUICtrlODMenuItemSetIcon ($iConv_11, @ScriptDir & "\data\ico\ps.ico")
	_GUICtrlODMenuItemSetIcon ($iConv_13, @ScriptDir & "\data\ico\ps.ico")
	_GUICtrlODMenuItemSetIcon ($iConv_14, @ScriptDir & "\Data\ico\ffmpeg.ico")
	_GUICtrlODMenuItemSetIcon ($iConv_4, @ScriptDir & "\data\ico\xn.ico")
	_GUICtrlODMenuItemSetIcon ($iConv_16, @ScriptDir & "\Data\ico\directx.ico")
	_GUICtrlODMenuItemSetIcon ($iConv_17, @ScriptDir & "\Data\ico\nvidia.ico")
	_GUICtrlODMenuItemSetIcon ($iRedEngine, @ScriptDir & "\data\ico\red_engine.ico")
	_GUICtrlODMenuItemSetIcon ($iReEngine, @ScriptDir & "\data\ico\re_engine.ico")
	_GUICtrlODMenuItemSetIcon ($iGodot, @ScriptDir & "\data\ico\godot.ico")
#EndRegion

	GUISetState(@SW_SHOW)
	;GUIRegisterMsg(0x0111, 'Main') ;Нужно для ассинхронных функций

Main()

#cs
Пароли
Amnesia lke271tyr299odn314
Hard Reset 9dU36jSJ@h265^k0b1!jrx*945F1
Hard Reset Demo rNPXgxj12A#Ian@!K5qt%JSNx2I
#ce
