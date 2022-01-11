
Func _Engine($iEnginesName, $sFileName = '', $iOther = '')

	Local $iExtList = ''

	If $iEnginesName = '_Unreal' Then $iExtList = 'Unreal Engine File (*.u*;*.xxx;*.pak;*.locres;*.pcc)|Unreal Engine 1-2 (*.u*)|Unreal Engine 3 (*.u*;*.xxx;*.pcc)|Unreal Engine 4 (*.pak;*.locres)|'
	If $iEnginesName = '_Unreal4' Then $iExtList = 'Unreal Engine 4 (*.pak;*.locres)|'
	If $iEnginesName = '_Unity' Then $iExtList = 'All Unity 3D Engine File (*.assets;globalgamemanagers;level*;*unity*)|Unity 3D Engine Assets File (*.assets)|Globalgamemanagers File (globalgamemanagers)|Unity 3D Engine Level File (level*)|Unity* files (*unity*)|'
	If $iEnginesName = '_idTech' Then $iExtList = 'idTech Resource File (*.wad;*.pak;*.pk3;*.pk4;*.pkz;*.*resource*;*.index;*.streamed;*.bimage;*.idwav;*.mega2;*.ptr;*.pages;*.vmtr;*.wl6;*.msf;*.xma;*.xpr;*.lib;*.pack)|DOOM\idTech 1 (*.wad)|Quake\idTech 2 (*.pak)|idTech 3 (*.pk3)|idTech 4 (*.pk4)|idTech 5, idTech 6 (*.*resource*;*.streamed;*.ptr;*.pages;*.vmtr;*.index;*.mega2)|Audio Files (*.idwav)|Textures Files (*.bimage)|Wolfenstin 3d Files (*.wl6)|Rage Console Audio (*.msf; *.xma)|Quake 4 XBOX 360 Files (*.xpr)|Doomsday Engine Files (*.lib;*.pack)|'
	If $iEnginesName = '_Bethesda' Then $iExtList = 'Bethesda Files (*.bsa; *.ba2; *.esp; *.esm; *.esl; *.esx; *.snd; *.pex; TEXBSI.*;*.omod;*.fomod)|Bethesda Softwork Archives (*.bsa; *.ba2)|Plaugin and master files (*.esp, *.esm; *.esl)|Decompressed pligin files (*.esx)|Daggerfall sound archives (*.snd)|Compiled Papyrus Scripts (*.pex)|Redgaurd Textures Archives (texbsi.*)|Nexus Mod Files (*.omod;*.fomod)|'
	If $iEnginesName = '_MTFramework' Then $iExtList = 'MT Framework Engine Files (*.arc;*.sngw)|'
	If $iEnginesName = '_Chrome' Then $iExtList = 'Chrome Engine Files (*.csb; *.spb; *.rpack; *.pak)|'
	If $iEnginesName = '_PopCapPackAll' Then $iExtList = $tAllSupp & "(*.pak;*.dll;*.obb;*.dz)|PopCap PAK Files (*.pak)|Download Library (*.dll)|Android Cache (*.obb)|DZIP " & $tArchives & " (*.dz)|"
	If $iEnginesName = '_RedEngine' Then $iExtList = $tAllSupp & "(*.bundle;*.w3strings;texture.cache;*.w3speech;*.archive;*.w2strings;*.dzip;*.xml)|"
	If $iEnginesName = '_ReEngine' Then $iExtList = 'RE Engine File (*.pak; *.tex; *.dds)|'
	If $iEnginesName = '_Aurora' Then $iExtList = $tAllSupp & "(*.erf;*.dzip;*.bif;*.key;*.rim)|ERF Files (*.erf)|BIF Files (*.bif)|KEY Files (*.key)|RIM Files (*.rim)|DZIP files (*.dzip)|"
	If $iEnginesName = '_RPGMaker' Then $iExtList = 'RPG Maker Archives(*.rgssad;*.rgss2a;*.rgss3a;*.pak)|'
	If $iEnginesName = '_Construct' Then $iExtList = 'Construct Engine Files (*.exe;*.dll;;*.pak)|'
	If $iEnginesName = '_Source' Then $iExtList = 'Source Engine File (*.gcf;*.wad;*.pak;*_dir.vpk;*.bsp;*.cache;*.vbsp;*.xzp)|GCF File (*.gcf)|Valve Package File (*.vpk)|Valve Package File Vol. 1 (*_dir.vpk)|Valve Map File (*.bsp;*.vbsp)|'
	IF $iEnginesName = '_TellTale' Then $iExtList = 'TellTale' & $tArchive & '(*.ttarch;*.ttarch2)|'
	IF $iEnginesName = '_RenPy' Then $iExtList = 'RPA File (*.rpa)|'
	IF $iEnginesName = '_GameMaker' Then $iExtList = 'data.win File (data.win)|'
	IF $iEnginesName = '_Asura' Then $iExtList = 'All Asura Engine File (*.asr;*.pc;*.hdr;*.ru;*.en;*.fr;*.it;*.ge;*.sp;*.pl;*.cz;*.gui)|ASR Filese (*.asr)|Localization Files (*.ru;*.en;*.fr;*.it;*.ge;*.sp;*.pl;*.cz)|GUI Files (*.gui)|HDR Files (*.hdr)|PC Files (*.pc)|'
	IF $iEnginesName = '_Unigene' Then $iExtList = 'UNG File (*.ung)|'
	IF $iEnginesName = '_Godot' Then $iExtList = 'Godot package files (*.pck; *.exe)|'
	If $iEnginesName = '_CryEngine' Then $iExtList = 'PAK Files (*.pak)|'
	If $iEnginesName = '_Glacier' Then $iExtList = 'Glacier Engine Files (*.wav; *.whd; *.prm; *.tex; *.anm; *.*_binkvid; *.zip; *.rpkg; *.bin; *.lgt"; *.spk; *.*_resourcelib; *.dcx; *.archive; *.str)|'
	If $iEnginesName = '_Chromium' Then $iExtList = 'PAK Files (*.pak)|'
	If $iEnginesName = '_FrostBite' Then 
		$iExtList = 'SB and TOC Files (*.sb;*.toc)|'
		If $iOther = '' Then $iOther = InputBox ($tEnterFBV, $tVer123, '3', '', '250', '125')
			If $iOther = '' Then Return
		If $iOther > 3 or $iOther < 1 Then 
			MsgBox (0, '', $tVer123_2)
			Return (_Engine('_FrostBite', 'folder'))
		ElseIf $iOther = 1 Then
			$sFileName = ''
		Else 
			$sFileName = 'folder'
		EndIf
	EndIf
	
	If $iExtList = '' Then Return(MsgBox (0, '', 'Error 404'))
	
	Switch $sFileName
		Case '', ' ', '	', "", " ", "	"
			$sFileName = FileOpenDialog($tSelectFile, " ", $iExtList & $tAllFile & " (*.*)", 1+4)
				If @error = 1 then Return
		Case 'folder'
			$sFileName = FileSelectFolder ('', $iLastDir)
				If @error = 1 then Return
		EndSwitch
		$iFileList1 = StringSplit ($sFileName, '|')
		Local $a = UBound($iFileList1) - 1, $fc = 2
		If $a = 1 Then $fc = 1
		For $i = $fc to $a
			If $iFileList1[0] > 1 Then $sFileName = $iFileList1[1] & '\' & $iFileList1[$i]
				_PathSplit($sFileName, $iDrive, $iDir, $iName, $iExp)
				
			Switch $iEnginesName
			
				Case '_Unreal', '_Unreal4'
					If $iExp = ".locres" then
						Unreal4LR($sFileName)
						$iOutputWindow = 0
					ElseIf $iExp = ".pak" then
						_StringChange(@ScriptDir & "\data\scripts\unreal_tournament_4.bms", 'set AES_KEY binary "' & $iOther & '"', 11)
						_QuickBMSRun('', @ScriptDir & "\data\scripts\unreal_tournament_4.bms ", $sFileName)
					Else
						_OtherPRG ('', 'extract.exe', ' -extract -out="' & $sFolderName & '" ', '', @ScriptDir & '\Data', $sFileName)
					EndIf
					
				Case '_Unity'
					GUICtrlSetData($iEdit, $tWtCoping & @CRLF, 1)
					FileCopy ($iDrive & $iDir & $iName & "*", $sFolderName)
					_OtherPRG ('', 'unityex.exe', ' export ', '', $sFolderName, $iName & $iExp)
					DirCopy ($iDrive & $iDir & 'Unity_Assets_Files', $sFolderName)
					FileDelete ($sFolderName & "\" & $iName & "*")
					
				Case '_idTech'
					Switch $iExp
						Case $iExp = ".wad" 
							DirCreate ($sFolderName & "\" & $iName)
							FileCopy (@ScriptDir & "\Data\wadext.exe", $sFolderName & "\" & $iName)
							_OtherPRG('', 'wadext', '', '', $sFolderName & "\" & $iName, $sFileName)
							FileDelete ($sFolderName & "\" & $iName & "\wadext.exe")
						Case ".pak" 
							If StringInStr ($iDir, "champions") Then
								_QuickBMSRun('', @ScriptDir & "\data\scripts\quake_champions.bms ", $sFileName)
							Else
								$iHead = FileRead($sFileName, 2)
								If $iHead = 'PK' Then
									_QuickBMSRun('', @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
								Else
									_QuickBMSRun('', @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
								EndIf
							EndIf
						Case ".pk3", ".pk4", ".pkz", ".lib", ".pack"
							_QuickBMSRun('', @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
						Case ".resources" 
							If StringInStr ($iDir, "doom") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\doom3BFG.bms ", $sFileName)
							If StringInStr ($iDir, "rage") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\RAGE_RESOURCES_files.bms ", $sFileName)
							If StringInStr ($iDir, "dishonored") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\dishonored2.bms ", $sFileName)
							If StringInStr ($iDir, "wolfenstein") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\wolfenstein2.bms ", $sFileName)
						Case ".tangoresource" 
							_QuickBMSRun('', @ScriptDir & "\data\scripts\the_evil_within.bms ", $sFileName)
						Case ".streamed" 
							If StringInStr ($iName, "eng") > 0 Then _QuickBMSRun('',@ScriptDir & "\data\scripts\idtech5streamed_eng.bms ", $sFileName)
							If StringInStr ($iName, "rus") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\idtech5streamed_rus.bms ", $sFileName)
							If StringInStr ($iDir, "within") > 0 Then _QuickBMSRun('',@ScriptDir & "\data\scripts\the_evil_within.bms ", $sFileName)
						Case ".bimage" 
							_QuickBMSRun('', @ScriptDir & "\data\scripts\idtech5_bimage_2_dds.bms ", $sFileName)
						Case ".index" 
							If $iName = 'master_resources' Then _QuickBMSRun('',@ScriptDir & "\data\scripts\deathloop.bms ", $sFileName)
							_OtherPRG('', 'DOOMExtract', '', $sFolderName, @ScriptDir, $sFileName)
						Case ".idwav" 
							_QuickBMSRun('', @ScriptDir & "\data\scripts\idwav_to_wav.bms ", $sFileName)
						Case ".mega2" 
							_QuickBMSRun('', @ScriptDir & "\data\scripts\doom2016_mega2.bms ", $sFileName)
						Case ".ptr", ".pages", ".vmtr" 
							_QuickBMSRun('', @ScriptDir & "\data\scripts\the_evil_within_2.bms ", $sFileName)
						Case ".wl6"
							$iFolPath = $iDrive & StringReplace($iDir, '\base', '')
							ShellExecuteWait (@ScriptDir & '\data\WolfExtractor.exe', "", $iFolPath, "open")
							_QuickBMSRun('', @ScriptDir &  '\data\wcx\Total7zip.wcx ', $iFolPath & '\base\wolf.pak')
							FileDelete ($iFolPath & '\base\wolf.pak')
						Case ".msf"
							_QuickBMSRun('',@ScriptDir & "\data\scripts\rage_idmsf.bms ", $sFileName)
						Case ".xma"
							_QuickBMSRun('',@ScriptDir & "\data\scripts\rage_idxma.bms ", $sFileName)
						Case ".xpr"
							_QuickBMSRun('',@ScriptDir & "\data\scripts\Quake_4_X360_xpr.bms ", $sFileName)
						Case Else
							MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoEngine & "idTech Engine")
					EndSwitch
					
				Case '_Bethesda'
					Switch $iExp
						Case ".bsa", ".ba2" 
							If $iName = 'ARCH3D' Then
								_DosBox($tFile & " (ARCH3D.BSA)|", "BSAD.EXE ", 1, '', $sFileName)
							ElseIf StringInStr($iDir, 'arena') > 0 Then
								_QuickBMSRun('', @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
							Else
								_OtherPRG("Bethesda Softwork Archives (*.bsa; *.ba2)|", "BSAE\bsab.exe", ' -e ', $sFolderName, $sFolderName, $sFileName)
							EndIf
						Case ".esp" , ".esm", ".esl"
							_OtherPRG("Elder Scrolls Plugin (*.esp; *.esm; *.esl)|", "bethkit.exe ", 'decompress "', '" "' & $sFolderName & '\' & $iName & $iExp, $sFolderName, $iFileName)
							_OtherPRG("", "bethkit.exe ", 'convert "', '" "' & $sFolderName & '\' & $iName & '.esx', $sFolderName, $iFileName)
						Case ".esx" 
							_OtherPRG("", "bethkit.exe ", 'convert "', '" "' & $sFolderName & '\' & $iName & '.esp', $sFolderName, $iFileName)
						Case ".snd"
							_DosBox("DAGGER.SND " & $tFile & " (DAGGER.SND)|", "DAGSND.EXE", 0, '', $sFileName)
						Case ".pex"
							If StringInStr($iDir, 'skyrim') Then
								_OtherPRG("PEX scripts (*.pex)|", "Champollion.exe ", '', '', $sFolderName, $sFileName)
							ElseIf StringInStr($iDir, 'fallout') Then
								_OtherPRG("PEX scripts (*.pex)|", "Champollion_f4.exe ", '', '', $sFolderName, $sFileName)
							EndIf
						Case ".omod", ".fomod"
							_OtherPRG('', '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
						Case ''
							Local $iAA = ['for /f "delims=" %%a in (''dir *.esm /b /a-d'') do (', 'IF not exist "%%~na.cel" @ECHO off>%%~na.cel', 'IF not exist "%%~na.top" @ECHO off>%%~na.top', 'IF not exist "%%~na.mrk" @ECHO off>%%~na.mrk', ')']
							_ScriptCreate($iAA, $sFileName)
						Case Else
							If $iName = 'TEXBSI' Then
								$iInvert = 1
								$iFile = FileOpen(@ScriptDir & "\data\REDPIC.INI", 2)
								FileWriteLine ($iFile, "Redguard_Path = """ & @ScriptDir & "\data\""")
								FileWriteLine ($iFile, "PCX_Path = """ & $sFolderName & """")
								FileClose ($iFile)
								_OtherPRG('', 'REDPIC95.EXE', '', '', @ScriptDir & "\data", $sFileName)
								FileDelete (@ScriptDir & "\data\REDPIC.INI")
							Else
								MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoEngine & "Bethesda Engines")
								$iOutputWindow = 1
								Output_MSG($iOutputWindow, $sFileName)
							EndIf
					EndSwitch
					
				Case '_MTFramework'
					If $iExp = ".arc" then
						_QuickBMSRun('', @ScriptDir & "\data\scripts\dmc4.bms ", $sFileName)
					ElseIf $iExp = ".sngw" then
						GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)
						FileCopy ($sFileName, $sFolderName)
						FileMove ($sFolderName & "\*.sngw", $sFolderName & "\*.ogg")
						Output_MSG(0, $sFileName)
					Else
						MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoEngine & "MT Framework")
						Output_MSG(1, $sFileName)
					EndIf
					
				Case '_ChromeEmgine'
					Switch $iExp
						Case ".csb", ".spb" 
							_QuickBMSRun('', @ScriptDir & "\data\scripts\dying_light.bms ", $sFileName)
						Case ".rpack" 
							If StringInStr ($iDir, 'dying') > 0 Then 
								_OtherPRG('', "lua_scripts\lua.exe", ' ' & @ScriptDir & '\data\lua_scripts\rp6l.lua ', $sFolderName, @ScriptDir & '\data\lua_scripts', $sFileName)
							ElseIf StringInStr ($iDir, 'sniper') > 0 Then 
								$iF = FileOpen($sFileName, 16)
								FileSetPos($iF, 20, 0)
								$iOffset = _Endian(FileRead($iF, 4))
								;MsgBox (0, '', $iOffset)
								_OtherPRG('', "offzip.exe ", ' -a ', $sFolderName & ' ' & $iOffset, $sFolderName, $sFileName)
							Else
								_OtherPRG('', "gibbed\Gibbed.Chrome.ResourceUnpack.exe", '', $sFolderName, $sFolderName, $sFileName) 
							EndIf
						Case ".pak" 
							_QuickBMSRun('', @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
						Case Else
							MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoEngine & "Chrome Engine")
							Output_MSG(1, $sFileName)
						EndSwitch
						
				Case '_CryEngine'
					$iHead = FileRead($sFileName, 2)
						If $iHead = 'PK' Then
							_QuickBMSRun('', @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
						Else
							If StringInStr ($iDir, "far cry") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\Far_Cry_PAK.bms ", $sFileName)
							If StringInStr ($iDir, "archeage") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\archeage.bms ", $sFileName)
							If StringInStr ($iDir, "crysis") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\crysis2.bms ", $sFileName)
							If StringInStr ($iDir, "prey") > 0 Then 
								_OtherPRG ('','PreyConvert.exe', '', $sFolderName & '\temp.zip', $sFolderName, $sFileName)
								_QuickBMSRun('', @ScriptDir & '\data\scripts\zip.bms ', $sFolderName & '\temp.zip')
								FileDelete ($sFolderName & "\temp.zip")
							Else
								MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoEngine & "CryEngine")
								Output_MSG(1, $sFileName)
							EndIf
						EndIf
						
				Case '_PopCapPackAll'
					Switch $iExp
						Case ".dll", ".obb"
							_QuickBMSRunWCX ('', @ScriptDir & "\data\wcx\Total7zip.wcx ", $sFileName)
						Case ".pak" 
							_QuickBMSRun("", @ScriptDir & "\data\scripts\7x7m.bms ", $sFileName)
						Case ".dz" 
							_QuickBMSRun("", @ScriptDir & "\data\scripts\vector.bms ", $sFileName)
						Case Else
							MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoGame & "PopCap")
							Output_MSG(1, $sFileName)	
					EndSwitch
					
				Case '_FrostBite'
					Switch $iOther
						Case 1, '1'
							_QuickBMSRun("", @ScriptDir & "\data\scripts\fbrb.bms ", $sFileName)
						Case 2, '2'
							_StringChange(@ScriptDir & "\data\python_script\Frostbite-Scripts-master\frostbite2\dumper.py", 'gameDirectory   = r"' & $sFileName & '"', 19)
							_StringChange(@ScriptDir & "\data\python_script\Frostbite-Scripts-master\frostbite2\dumper.py", 'targetDirectory   = r"' & $sFolderName & '"', 20)
							_OtherPRG('', 'python_script\Frostbite-Scripts-master\frostbite2\dumper.py', ' ', '', @ScriptDir & '\data\python_script\Frostbite-Scripts-master\frostbite2', $sFileName) 
						Case 3, '3'
							_StringChange(@ScriptDir & "\data\python_script\Frostbite-Scripts-master\frostbite3\dumper.py", 'gameDirectory   = r"' & $sFileName & '"', 17)
							_StringChange(@ScriptDir & "\data\python_script\Frostbite-Scripts-master\frostbite3\dumper.py", 'targetDirectory   = r"' & $sFolderName & '"', 18)
							_OtherPRG('', 'python_script\Frostbite-Scripts-master\frostbite3\dumper.py', ' ', '', @ScriptDir & '\data\python_script\Frostbite-Scripts-master\frostbite3', $sFileName) 
					EndSwitch
					
				Case '_RedEngine'
					Switch $iName & $iExp
						Case $iName & ".bundle" 
							_QuickBMSRun("", @ScriptDir & "\data\scripts\Witcher3.bms ", $sFileName)
						Case "texture.cache" 
							_OtherPRG('', "lua_scripts\lua.exe", ' ' & @ScriptDir & '\data\lua_scripts\unpack_textures.lua ', $sFolderName, @ScriptDir & '\data\lua_scripts', $sFileName)
							$iFileList1 = _FileListToArray($sFolderName, "*.dds")
							ProgressOn('', $tWtCoping, '', (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)
								$a = $iFileList1[0]
								For $i = 1 to $a
									$iDist = $sFolderName & '\' & StringReplace ($iFileList1[$i], '#', '\')
									_PathSplit($iDist, $iDrive, $iDir, $iName, $iExp)
									If Not FileExists ($iDrive & $iDir) Then DirCreate ($iDrive & $iDir)
									FileMove($sFolderName & '\' & $iFileList1[$i], $iDist , 8)
									ProgressSet((100/$a) * $i, $tCopied & " " & $i & "/" & $a )
								Next
							ProgressSet(100, $tDone)
							ProgressOff()
						Case $iName & ".w3strings" 
							_OtherPRG('', "lua_scripts\lua.exe", ' ' & @ScriptDir & '\data\lua_scripts\inspect_w3strings.lua ', $sFolderName & '\' & $iName & '.txt', @ScriptDir & '\data\lua_scripts', $sFileName)
						Case $iName & ".w3speech" 
							_OtherPRG('', "lua_scripts\lua.exe", ' ' & @ScriptDir & '\data\lua_scripts\inspect_w3speech.lua ', $sFolderName, @ScriptDir & '\data\lua_scripts', $sFileName)
						Case $iName & ".w2strings" 
							_OtherPRG('', "gibbed\Gibbed.RED.Strings.exe", ' -d ', $sFolderName & '\' & $iName & '.xml', $sFolderName, $sFileName)
						Case $iName & ".xml"
							_OtherPRG('', "gibbed\Gibbed.RED.Strings.exe", ' -e ', $sFolderName & '\' & $iName & '.w2strings', $sFolderName, $sFileName)
						Case $iName & ".archive" ; CP2077
							_QuickBMSRun("", @ScriptDir & "\data\scripts\cyberpunk_2077.bms ", $sFileName)
						Case $iName & ".dzip" 
							If GUICtrlRead($iReimport_Checkbox) = 1 Then 
								_OtherPRG('', "gibbed\Gibbed.RED.Pack.exe", '', $sFolderName, $sFolderName, $sFileName)
							Else
								_OtherPRG('', "gibbed\Gibbed.RED.Unpack.exe", '', $sFolderName, $sFolderName, $sFileName)
							EndIf
							;_QuickBMSRun("", @ScriptDir & "\data\scripts\witcher2.bms ", $sFileName) ;Прога вместо этого скрипта ^
						;TODO: Добавить поддержку форматов ниже v
						; Case $iName & ".w2speech" 
							; Sleep(1)
						; Case $iName & ".w2scripts" 
							; Sleep(1)
						; Case $iName & ".redscripts" 
							; Sleep(1)
						; Case $iName & ".cache" 
							; Sleep(1)
						Case Else
							MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoGame & "Red Engine")
							Output_MSG(1, $sFileName)
					EndSwitch	
					
				Case '_ReEngine'
					Switch $iExp
						Case ".pak" 
							$iProcess = ShellExecute (@ScriptDir & "\data\quickbms.exe ", @ScriptDir & "\data\scripts\zip.bms " & '"' & @ScriptDir & '\data\retools\retools.zip" ' & @TempDir, @ScriptDir & "\data\scripts\", "open", @SW_HIDE)
							Sleep(1000)
							ProcessClose($iProcess)
							_OtherPRG('', "retools\REtool.exe", ' -x ', ' -h ' & @TempDir & '\' & $iOther, $sFolderName, $sFileName)
						Case ".dds"
							_OtherPRG('', "retools\REtool.exe", ' -dds ', '', $sFolderName, $sFileName)
						Case ".tex"
							_OtherPRG('', "retools\REtool.exe", ' -tex ', '', $sFolderName, $sFileName)
						Case Else
							MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoGame & "Re Engine")
							Output_MSG(1, $sFileName)	
					EndSwitch
					
				Case '_Aurora'
					Switch $iExp
						Case ".erf", ".rim"
							If StringInStr ($iDir, "Dragon Age II") > 0 Then 
								_QuickBMSRun('', @ScriptDir & "\data\scripts\dragon_age__2.bms ", $sFileName)
							ElseIf StringInStr ($iDir, "jade") > 0 Then
								_QuickBMSRun('', @ScriptDir & "\data\scripts\RIM_RIMV10.bms ", $sFileName)
							Else
								ERFUnpacker($sFileName)
							EndIf
						Case ".dzip" 
							If StringInStr ($iDir, "dragon") > 0 Then _QuickBMSRun("", @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
							If StringInStr ($iDir, "witcher") > 0 Then _OtherPRG('', "gibbed\Gibbed.RED.Unpack.exe", '', $sFolderName, $sFolderName, $sFileName)
						Case ".bif"
							_QuickBMSRun("", @ScriptDir & "\data\scripts\BIF_BIFFV1.bms ", $sFileName)
						Case Else
							MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoGame & "Aurora Engine")
							Output_MSG(1, $sFileName)	
					EndSwitch
					
				Case '_RPGMaker'
					Switch $iExp
						Case ".rgss2a"
							;TODO: Найти что-то консольное для этого формата, или сделать ковырялку самому
							ShellExecuteWait (@ScriptDir & '\data\RGSSAD - RGSS2A - RGSS3A Decrypter.exe')
						Case ".rgss3a", ".rgssad"
							_QuickBMSRun("", @ScriptDir &  "\data\scripts\rgssad.bms ", $sFileName)
						Case ".pak"
							_OtherPRG('', 'pak_mingw64.exe ', ' -u ', ' "' & $sFolderName & '"', $sFolderName, $sFileName)
					EndSwitch
					
				Case '_Construct'
					Switch $iExp
						Case ".exe", ".dll"
							_OtherPRG('', '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
						Case ".pak"
							_OtherPRG('', 'pak_mingw64.exe ', ' -u ', ' "' & $sFolderName & '"', $sFolderName, $sFileName)
					EndSwitch
					
				Case '_Glacier'
					Switch $iExp
						Case ".wav", ".whd", ".prm", ".tex", ".anm", ".lgt", ".spk"
							If $iName = 'streams' Then Return(MsgBox(0, '', 'Error 404')) ;TODO: Добавить поддержку streams.wav
							_QuickBMSRun("", @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
							;TODO: Добавить поддержку форматов ниже v
							;".wav", ".whd" - Работает только с Hitman Blood Money
							;".prm", ".tex", ".anm" - c Hitman Blood Money - не работает
							;".prm", ".tex"- c Hitman Codename 47 - не работает
						Case ".zip"
							_QuickBMSRun("", @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
						Case ".rpkg"
							_QuickBMSRun("", @ScriptDir & "\data\scripts\hitman_2016.bms ", $sFileName)
						Case ".bin"
							_QuickBMSRun("", @ScriptDir & "\data\scripts\Hitman_BIN.bms ", $sFileName)
						Case ".dcx"
							_QuickBMSRun("", @ScriptDir & "\data\scripts\Glacier3_DCX.bms ", $sFileName)
						Case ".archive"
							_QuickBMSRun("", @ScriptDir & "\data\scripts\deus_ex_mankind_divided.bms ", $sFileName)
						Case ".str"
							_OtherPRG("", "towav.exe", ' ', '', $sFolderName, $sFileName)
						Case Else
							If StringInStr($iExp, '_binkvid') > 1 Then _QuickBMSRun("", @ScriptDir & "\data\scripts\binkvid.bms ", $sFileName)
							If StringInStr($iExp, '_resourcelib') > 1 Then _QuickBMSRun("", @ScriptDir & "\data\scripts\hitman_absolution.bms ", $sFileName)
					EndSwitch
					
				Case '_Source'
					_QuickBMSRun($iExtList, @ScriptDir &  "\data\wcx\TotalObserver.wcx ", $sFileName)
					
				Case '_TellTale'
					_OtherPRG($iExtList, 'ttarchext.exe ', '-m ' & $iOther & ' ', '"' & $sFolderName & '"', @ScriptDir & '\data', $sFileName)
					
				Case '_RenPy'
					_QuickBMSRun($iExtList, @ScriptDir &  "\data\scripts\rpa_renpy_nopython.bms ", $sFileName)
					
				Case '_GameMaker'
					_QuickBMSRun($iExtList, @ScriptDir &  "\data\scripts\yoyogames.bms ", $sFileName)
					
				Case '_Asura'
					_QuickBMSRun($iExtList, @ScriptDir &  "\data\scripts\asura.bms ", $sFileName)
					
				Case '_Chromium'
					_OtherPRG($iExtList, 'pak_mingw64.exe ', ' -u ', ' "' & $sFolderName & '"', $sFolderName, $sFileName)
					
				Case '_Unigene'
					_OtherPRG ($iExtList, "uniginex.exe ", '', ' "' & $sFolderName & '"', $sFolderName, $sFileName)
					
				Case '_Godot'
					_OtherPRG ($iExtList, "godot\godotdec.exe ", ' -c ', ' "' & $sFolderName & '"', $sFolderName, $sFileName)
						
			EndSwitch
	Next
EndFunc