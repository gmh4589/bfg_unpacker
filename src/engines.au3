
Func _Engine($iEnginesName, $sFileName = '', $iOther = '')

	Local $iExtListArray = [['_Asura', 'All Asura Engine File(*.asr;*.pc;*.hdr;*.ru;*.en;*.fr;*.it;*.ge;*.sp;*.pl;*.cz;*.gui)|ASR Filese(*.asr)|Localization Files(*.ru;*.en;*.fr;*.it;*.ge;*.sp;*.pl;*.cz)|GUI Files(*.gui)|HDR Files(*.hdr)|PC Files(*.pc)|'], _
		['_Anvil', "Forge file(*.forge)|"], _
		['_Aurora', "(*.erf;*.dzip;*.bif;*.rim)|ERF Files(*.erf)|BIF Files(*.bif)|RIM Files(*.rim)|DZIP files(*.dzip)|"], _
		['_Bethesda', 'Bethesda Files(*.bsa; *.ba2; *.esp; *.esm; *.esl; *.esx; *.snd; *.pex; TEXBSI.*;*.omod;*.fomod; *.mnf)|Bethesda Softwork Archives(*.bsa; *.ba2)|Plaugin and master files(*.esp; *.esm; *.esl)|Decompressed pligin files(*.esx)|TESO Data files(*.mnf)|Daggerfall sound archives(*.snd)|Compiled Papyrus Scripts(*.pex)|Redgaurd Textures Archives(texbsi.*)|Nexus Mod Files(*.omod;*.fomod)|Textures Archives(*textures*)|Meshes Archives(*mesh*)|Audio Archives(*audio*; *sound*; *voice*)|Miscs Archives(*misc*; *script*)|Main Archives(*main*)|Animations Archives(*animation*)|'], _
		['_Build', 'Build Engine Files(*.grp; *.art; *.rff; *.tga)|'], _
		['_Chrome', 'Chrome Engine Files(*.csb; *.spb; *.rpack; *.pak)|'], _
		['_Chromium', 'PAK Files(*.pak)|'], _
		['_Construct', 'Construct Engine Files(*.exe;*.dll;;*.pak)|'], _
		['_CryEngine', 'PAK Files(*.pak)|'], _
		['_Flash', 'SWF Files(*.swf)|'], _
		['_FrostBite', 'SB and TOC Files(*.sb;*.toc)|'], _
		['_GameMaker', 'data.win File(data.win)|'], _
		['_Glacier', 'Glacier Engine Files(*.wav; *.whd; *.prm; *.tex; *.anm; *.*_binkvid; *.zip; *.rpkg; *.bin; *.lgt; *.spk; *.*_resourcelib; *.dcx; *.archive; *.str)|'], _
		['_Godot', 'Godot package files(*.pck; *.exe)|'], _
		['_idTech', 'idTech Resource File(*.wad;*.pak;*.pk3;*.pk4;*.pkz;*.*resource*;*.index;*.streamed;*.bimage;*.idwav;*.mega2;*.ptr;*.pages;*.vmtr;*.wl6;*.msf;*.xma;*.xpr;*.lib;*.pack;*.sin)|DOOM\idTech 1(*.wad)|Quake\idTech 2(*.pak)|idTech 3(*.pk3)|idTech 4(*.pk4)|idTech 5, idTech 6(*.*resource*; *юtangoresource; *.streamed;*.ptr;*.pages;*.vmtr;*.index;*.mega2)|Audio Files(*.idwav)|Textures Files(*.bimage)|Wolfenstin 3d Files(*.wl6)|Rage Console Audio(*.msf; *.xma)|Quake 4 XBOX 360 Files(*.xpr)|Doomsday Engine Files(*.lib;*.pack)|Sin Gold SIN files(*.sin)|'], _
		['_Infinity', 'Infinity Engine Files(*.key; *.gob; *.lmp)|'], _
		['_LithTech',  'LithTech Engine Files(*.rez; *.Arch*)|'], _
		['_MTFramework', 'MT Framework Engine Files(*.arc;*.sngw)|'], _
		['_PopCapPackAll', $tAllSupp & "(*.pak;*.dll;*.obb;*.dz)|PopCap PAK Files(*.pak)|Download Library(*.dll)|Android Cache(*.obb)|DZIP " & $tArchives & "(*.dz)|"], _
		['_RedEngine', $tAllSupp & "(*.bundle;*.w3strings;texture.cache;*.w3speech;*.archive;*.w2strings;*.dzip;*.xml)|"], _
		['_ReEngine', 'RE Engine File(*.pak; *.tex; *.dds)|'], _
		['_RenPy', 'RPA File(*.rpa)|'], _
		['_RPGMaker', 'RPG Maker Archives(*.rgssad;*.rgss2a;*.rgss3a; *.rpgmvp; *.rpgmvo; *.rpgmvm; *.pak)|'], _
		['_Source', 'Source Engine File(*.gcf;*.wad;*.pak;*_dir.vpk;*.bsp;*.cache;*.vbsp;*.xzp)|GCF File(*.gcf)|Valve Package File(*.vpk)|Valve Package File Vol. 1(*_dir.vpk)|Valve Map File(*.bsp;*.vbsp)|'], _
		['_Sen', 'All supported(*.dat; *. pkg; *. phyre; *.xlsx)|DAT Scripts(*.dat)|PKG Files(*.pkg)|PHYRE2D Files(*.phyre)|Book Files(book*.dat)|Decompiled Scripts(*.xlsx)|'], _
		['_Snowdrop', 'sdfdata files(*.sdfdata)|'], _
		['_TellTale', 'TellTale' & $tArchive & '(*.ttarch;*.ttarch2)|'], _
		['_Unigene', 'UNG File(*.ung)|'], _
		['_Unity', 'All Unity 3D Engine File(data.unity3d; *.assets; *globalgamemanagers*; level*; *unity*; *.resource; *.unitypackage)|Unity 3D Engine Assets File(*.assets)|Globalgamemanagers File(*globalgamemanagers*)|Unity 3D Engine Level File(level*)|Unity* files(*unity*)|resource files(*.resource)|data.unity3d File(data.unity3d)|'], _
		['_Unreal', 'Unreal Engine File(*.u*;*.xxx;*.pak;*.locres;*.pcc)|Unreal Engine 1-2(*.u*)|Unreal Engine 3(*.u*;*.xxx;*.pcc)|Unreal Engine 4(*.pak;*.locres)|'], _
		['_Unreal4', 'Unreal Engine 4(*.pak;*.locres)|']]
	
	If $iEnginesName = '_FrostBite' Then 
		If $iOther = '' Then $iOther = _InputBox($tEnterFBV, $tVer123, 3, 200, 125, True)
			Switch $iOther
				Case 1
					$sFileName = ''
				Case 2, 3 
					$sFileName = 'folder'
				Case ''
				Case Else
					_MsgBox(0, '', $tVer123_2)
					Return(_Engine('_FrostBite'))
			EndSwitch
	EndIf
	
	Local $iScriptsArray = [['_Source', "\data\wcx\TotalObserver.wcx "], ['_RenPy', "\data\scripts\rpa_renpy_nopython.bms "], ['_GameMaker', "\data\scripts\yoyogames.bms "], ['_Asura', "\data\scripts\asura.bms "], ['_Anvil', "\data\scripts\scimitar.bms "], ['_Snowdrop', "\data\scripts\ubisoft_sdf.bms "]]
		
	$iExtList = $iExtListArray [_ArraySearch($iExtListArray, $iEnginesName)][1]
	If _ArraySearch($iScriptsArray, $iEnginesName) > -1 Then $iScriptName = $iScriptsArray [_ArraySearch($iScriptsArray, $iEnginesName)][1]
	
	
	$sFileName = _getFile($sFileName, $iExtList)
	If @error = 1 then Return

	$iFileList1 = StringSplit($sFileName, '|')
	Local $a = UBound($iFileList1) - 1, $fc = 2
	If $a = 1 Then $fc = 1
		
	For $i = $fc to $a
		If $iFileList1[0] > 1 Then $sFileName = $iFileList1[1] & '\' & $iFileList1[$i]
		_PathSplit($sFileName, $iDrive, $iDir, $iName, $iExp)
			
		Switch $iEnginesName

			Case '_Aurora'
				Switch $iExp
					Case ".erf", ".rim"
						If StringInStr($iDir, "jade") > 0 Then
							_QuickBMSRun('', @ScriptDir & "\data\scripts\RIM_RIMV10.bms ", $sFileName)
						Else
							_fileReaper(ERFUnpacker, "", $sFileName)
						EndIf
						
					Case ".dzip" 
						If StringInStr($iDir, "dragon") > 0 Then _QuickBMSRun("", @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
						If StringInStr($iDir, "witcher") > 0 Then _OtherPRG('', "\data\gibbed\Gibbed.RED.Unpack.exe", '', $sFolderName, $sFolderName, $sFileName)
						
					Case ".bif"
						_QuickBMSRun("", @ScriptDir & "\data\scripts\BIF_BIFFV1.bms ", $sFileName)
						
					Case Else
						_MsgBox(0, $tMessage, $tNoGame & "Aurora Engine")
						Output_MSG(1, $sFileName)	
				EndSwitch
				
			Case '_Bethesda'
				Switch $iExp
					Case ".bsa", ".ba2" 
						If $iName = 'ARCH3D' Then
							_DosBox($tFile & "(ARCH3D.BSA)|", "BSAD.EXE ", 1, '', $sFileName)
						ElseIf BitOR(StringInStr($iDir, 'arena'), StringInStr($iDir, 'battle'), StringInStr($iDir, 'terminator')) > 0 Then
							_QuickBMSRun('', @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
						Else
							;_OtherPRG("", "BSAE\bsab.exe", ' -e ', $sFolderName, $sFolderName, $sFileName)
							$iOutputWindow = Run(@ScriptDir & '\data\BSAE\bsab.exe -e "' & $sFileName & '" "' & $sFolderName & '"', $sFolderName, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
							_EnginePB($iOutputWindow, 115)
						EndIf
						
					Case ".esp" , ".esm", ".esl"
						_OtherPRG("", "\data\bethkit.exe ", 'decompress "', '" "' & $sFolderName & '\' & $iName & $iExp, $sFolderName, $iFileName)
						_OtherPRG("", "\data\bethkit.exe ", 'convert "', '" "' & $sFolderName & '\' & $iName & '.esx', $sFolderName, $iFileName)
						
					Case ".esx" 
						_OtherPRG("", "\data\bethkit.exe ", 'convert "', '" "' & $sFolderName & '\' & $iName & '.esp', $sFolderName, $iFileName)
						
					Case ".snd"
						If $iName = 'DAGGER' Then
							_DosBox("", "DAGSND.EXE", 0, '', $sFileName)
						ElseIf $iName = 'SPIRE' Then
							_QuickBMSRun('', @ScriptDir & "\data\scripts\wav_search.bms ", $sFileName)
						EndIf
						
					Case ".pex"
						If StringInStr($iDir, 'skyrim') Then
							_OtherPRG("PEX scripts(*.pex)|", "\data\Champollion.exe ", '', '', $sFolderName, $sFileName)
						ElseIf StringInStr($iDir, 'fallout') Then
							_OtherPRG("PEX scripts(*.pex)|", "\data\Champollion_f4.exe ", '', '', $sFolderName, $sFileName)
						Else
							_MsgBox(0, $tMessage, $tIntoFolder)
						EndIf
						
					Case ".omod", ".fomod"
						_OtherPRG('', '\data\7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
						
					Case '.mnf'
						_OtherPRG("", "\data\EsoExtractData.exe", '', ' "' & $sFolderName & '"', $sFolderName, $sFileName)
						
					Case ''
						Local $iAA = ['for /f "delims=" %%a in(''dir *.esm /b /a-d'') do(', 'IF not exist "%%~na.cel" @ECHO off>%%~na.cel', 'IF not exist "%%~na.top" @ECHO off>%%~na.top', 'IF not exist "%%~na.mrk" @ECHO off>%%~na.mrk', ')', 'pause']
						_ScriptCreate($iAA, $sFileName)
						
					Case Else
						If $iName = 'TEXBSI' Then
							$iInvert = 1
							$iFile = FileOpen(@ScriptDir & "\data\REDPIC.INI", 2)
							FileWriteLine($iFile, "Redguard_Path = """ & @ScriptDir & "\data\""")
							FileWriteLine($iFile, "PCX_Path = """ & $sFolderName & """")
							FileClose($iFile)
							_OtherPRG('', '\data\REDPIC95.EXE', '', '', @ScriptDir & "\data", $sFileName)
							FileDelete(@ScriptDir & "\data\REDPIC.INI")
						Else
							_MsgBox(0, $tMessage, $tNoEngine & "Bethesda Engines")
							$iOutputWindow = 1
							Output_MSG($iOutputWindow, $sFileName)
						EndIf
				EndSwitch
				
			Case '_Build'
			
				Switch $iExp
					Case ".grp"
						If _headRead($sFileName) = 'PK' Then
							_QuickBMSRun('', @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
						Else
							_QuickBMSRun("", @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
						EndIf
						
					Case ".art"
						_OtherPRG('', '\data\art2tga.exe', '', '', $sFolderName, $sFileName)
					
					Case ".rff"
						_DosBox('', 'barf.exe ', 1, ' -x ', $sFileName) 
						
					Case ".tga"
						For $start = 0 to 9999
							If FileExists($iDrive & $iDir & '\tile*' & $start & '.tga')	Then ExitLoop
						Next
						
						For $end = 9999 to 0 step -1
							If FileExists($iDrive & $iDir & '\tile*' & $end & '.tga')	Then ExitLoop
						Next
						
						$tileName = _InputBox('', 'Input out file name', 'tiles.art', 200, 125)
						
						ShellExecuteWait(@ScriptDir & "\data\tga2art.exe ", $sFolderName & "\" & $tileName & ' ' & $start & " " & $end)
						GUICtrlSetData($iEdit, $tDone, 1)
				EndSwitch
			
			Case '_ChromeEmgine'
				Switch $iExp
					Case ".csb", ".spb" 
					_QuickBMSRun('', @ScriptDir & "\data\scripts\dying_light.bms ", $sFileName)
						
					Case ".rpack" 
						If StringInStr($iDir, 'dying') > 0 Then 
							_OtherPRG('', "\data\lua_scripts\lua.exe", ' ' & @ScriptDir & '\data\lua_scripts\rp6l.lua ', $sFolderName, @ScriptDir & '\data\lua_scripts', $sFileName)
						ElseIf StringInStr($iDir, 'sniper') > 0 Then 
							$iF = FileOpen($sFileName, 16)
							FileSetPos($iF, 20, 0)
							$iOffset = _BinaryToInt16(FileRead($iF, 4))
							FileClose($iF)
							_OtherPRG('', "\data\offzip.exe ", ' -a ', $sFolderName & ' ' & $iOffset, $sFolderName, $sFileName)
						Else
							_OtherPRG('', "\data\gibbed\Gibbed.Chrome.ResourceUnpack.exe", '', $sFolderName, $sFolderName, $sFileName) 
						EndIf
						
					Case ".pak" 
						_QuickBMSRun('', @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
						
					Case Else
						_MsgBox(0, $tMessage, $tNoEngine & "Chrome Engine")
						Output_MSG(1, $sFileName)
					EndSwitch
			
			Case '_Construct', '_Chromium', '_Flash'
				_OtherPRG('', '\data\7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
				If $iEnginesName = '_Flash' Then _OtherPRG('', '\data\7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFolderName & '\' & $iName & '~.swf')
				
					
			Case '_CryEngine'
				If _headRead($sFileName) = 'PK' Then
					_QuickBMSRun('', @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
				Else
				
					If StringInStr($iDir, "far cry") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\Far_Cry_PAK.bms ", $sFileName)
					If StringInStr($iDir, "archeage") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\archeage.bms ", $sFileName)
					If StringInStr($iDir, "crysis") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\crysis2.bms ", $sFileName)
					If StringInStr($iDir, "prey") > 0 Then 
						_OtherPRG('','\data\PreyConvert.exe', '', $sFolderName & '\temp.zip', $sFolderName, $sFileName)
						_QuickBMSRun('', @ScriptDir & '\data\scripts\zip.bms ', $sFolderName & '\temp.zip')
						FileDelete($sFolderName & "\temp.zip")
					Else
						_MsgBox(0, $tMessage, $tNoEngine & "CryEngine")
						Output_MSG(1, $sFileName)
					EndIf
				EndIf
			
			Case '_FrostBite'
				Switch $iOther
					Case 1, '1'
						_QuickBMSRun("", @ScriptDir & "\data\scripts\fbrb.bms ", $sFileName)
						
					Case 2, '2'
						_StringChange(@ScriptDir & "\data\python_script\Frostbite-Scripts-master\frostbite2\dumper.py", 'gameDirectory   = r"' & $sFileName & '"', 19)
						_StringChange(@ScriptDir & "\data\python_script\Frostbite-Scripts-master\frostbite2\dumper.py", 'targetDirectory   = r"' & $sFolderName & '"', 20)
						_OtherPRG('', '\data\python_script\Frostbite-Scripts-master\frostbite2\dumper.py', ' ', '', @ScriptDir & '\data\python_script\Frostbite-Scripts-master\frostbite2', $sFileName) 
						
					Case 3, '3'
						_StringChange(@ScriptDir & "\data\python_script\Frostbite-Scripts-master\frostbite3\dumper.py", 'gameDirectory   = r"' & $sFileName & '"', 17)
						_StringChange(@ScriptDir & "\data\python_script\Frostbite-Scripts-master\frostbite3\dumper.py", 'targetDirectory   = r"' & $sFolderName & '"', 18)
						_OtherPRG('', '\data\python_script\Frostbite-Scripts-master\frostbite3\dumper.py', ' ', '', @ScriptDir & '\data\python_script\Frostbite-Scripts-master\frostbite3', $sFileName) 
				EndSwitch
			
			Case '_Glacier'
				Switch $iExp
					Case ".wav", ".whd", ".prm", ".tex", ".anm", ".lgt", ".spk"
						If $iName = 'streams' Then Return(_MsgBox(0, '', 'Error 404')) ;TODO: Добавить поддержку streams.wav
						_QuickBMSRun("", @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
						;TODO: Добавить поддержку форматов ниже ↓
						;".wav", ".whd" - Работает только с Hitman Blood Money
						;".prm", ".tex", ".anm" - c Hitman Blood Money - не работает
						;".prm", ".tex" - c Hitman Codename 47 - не работает
						
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
						_OtherPRG("", "\data\towav.exe", ' ', '', $sFolderName, $sFileName)
						
					Case ".ini", ".scrambled"
						_OtherPRG("", "\data\unscrambler.exe", ' ', '', $sFolderName, $sFileName)
						
					Case Else
						If StringInStr($iDir, 'Galaxy') > 1 Then 
							Run(@ScriptDir & '\data\ResourceExtractor.exe', $sFolderName)
							Sleep(1000)
							ControlV($iDrive & $iDir)
							ControlV($sFolderName)
						EndIf
						
						If StringInStr($iExp, '_binkvid') > 1 Then _QuickBMSRun("", @ScriptDir & "\data\scripts\binkvid.bms ", $sFileName)
						If StringInStr($iExp, '_resourcelib') > 1 Then _QuickBMSRun("", @ScriptDir & "\data\scripts\hitman_absolution.bms ", $sFileName)
				EndSwitch
			
			Case '_Godot'
				; _OtherPRG($iExtList, "\data\godot\godotdec.exe ", ' -c ', ' "' & $sFolderName & '"', $sFolderName, $sFileName)
				$size = FileGetSize($sFileName)
				$iOutputWindow = Run(@ScriptDir & "\data\godot\godotdec.exe " & '-c "' & $sFileName & '" "' & $sFolderName & '"', $iDrive & $iDir, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
				_EnginePB($iOutputWindow, 110, 1, '[]/\')
				
			Case '_idTech'
				Switch $iExp
					Case $iExp = ".wad" 
						DirCreate($sFolderName & "\" & $iName)
						; _OtherPRG('', '\data\wadext', '', '', $sFolderName & "\" & $iName, $sFileName)
						$iOutputWindow = Run(@ScriptDir & '\data\wadext.exe "' & $sFileName & '"', $sFolderName & "\" & $iName, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
						Local $ln[0], $per
							
							While 1
								$line = StdoutRead($iOutputWindow)
								If @error Then 
								
									For $i = 1 to $ln[0] Step 10
										$iMSGU = StringReplace($ln[$i],'processing', $tDone)
										$per = 100/$ln[0] * $i
										_BarCreate($per, "Распаковка", $iMSGU, 300, 100, 45, True)
										GUICtrlSetData($iEdit, $iMSGU & @CRLF, 1)
									Next
									
									ExitLoop
								EndIf
								
								If $line <> '' Then
									_ArrayConcatenate($ln, StringSplit($line, @CRLF))
								EndIf
							Wend
							_BarOff()
							
					Case ".pak" 
						If StringInStr($iDir, "champions") Then
							_QuickBMSRun('', @ScriptDir & "\data\scripts\quake_champions.bms ", $sFileName)
						Else
						
							If _headRead($sFileName) = 'PK' Then
								_QuickBMSRun('', @ScriptDir & "\data\scripts\zip.bms ", $sFileName)
							Else
								_QuickBMSRun('', @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
							EndIf
							
						EndIf
						
					Case ".pk3", ".pk4", ".pkz", ".lib", ".pack"
						_OtherPRG('', '\data\7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
						
					Case ".resources" 
						If StringInStr($iDir, "doom") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\doom3BFG.bms ", $sFileName)
						If StringInStr($iDir, "rage") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\RAGE_RESOURCES_files.bms ", $sFileName)
						If StringInStr($iDir, "dishonored") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\dishonored2.bms ", $sFileName)
						If StringInStr($iDir, "wolfenstein") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\wolfenstein2.bms ", $sFileName)
						
					Case ".tangoresource" 
						_QuickBMSRun('', @ScriptDir & "\data\scripts\the_evil_within.bms ", $sFileName)
						
					Case ".streamed" 
						If StringInStr($iDir, "within") > 0 Then _QuickBMSRun('',@ScriptDir & "\data\scripts\the_evil_within.bms ", $sFileName)
						If StringInStr($iName, "eng") > 0 Then _QuickBMSRun('',@ScriptDir & "\data\scripts\idtech5streamed_eng.bms ", $sFileName)
						If StringInStr($iName, "rus") > 0 Then _QuickBMSRun('', @ScriptDir & "\data\scripts\idtech5streamed_rus.bms ", $sFileName)
						
					Case ".bimage" 
						_QuickBMSRun('', @ScriptDir & "\data\scripts\idtech5_bimage_2_dds.bms ", $sFileName)
						
					Case ".index" 
						If $iName = 'master_resources' Then _QuickBMSRun('',@ScriptDir & "\data\scripts\deathloop.bms ", $sFileName)
						_OtherPRG('', '\data\DOOMExtract', '', $sFolderName, @ScriptDir, $sFileName)
						
					Case ".idwav" 
						_QuickBMSRun('', @ScriptDir & "\data\scripts\idwav_to_wav.bms ", $sFileName)
						
					Case ".mega2" 
						_QuickBMSRun('', @ScriptDir & "\data\scripts\doom2016_mega2.bms ", $sFileName)
						
					Case ".ptr", ".pages", ".vmtr" 
						_QuickBMSRun('', @ScriptDir & "\data\scripts\the_evil_within_2.bms ", $sFileName)
						
					Case ".wl6"
						$iFolPath = $iDrive & StringReplace($iDir, '\base', '')
						ShellExecuteWait(@ScriptDir & '\data\WolfExtractor.exe', "", $iFolPath, "open")
						_OtherPRG('', '\data\7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $iFolPath & '\base\wolf.pak')
						FileDelete($iFolPath & '\base\wolf.pak')
						
					Case ".msf"
						_QuickBMSRun('',@ScriptDir & "\data\scripts\rage_idmsf.bms ", $sFileName)
						
					Case ".xma"
						_QuickBMSRun('',@ScriptDir & "\data\scripts\rage_idxma.bms ", $sFileName)
						
					Case ".xpr"
						_QuickBMSRun('',@ScriptDir & "\data\scripts\Quake_4_X360_xpr.bms ", $sFileName)
						
					Case ".sin"
						FileCopy($sFileName, $sFolderName)
						_OtherPRG('', '\data\PAKExtract.exe', '', '', $sFolderName, $sFolderName & '\' & $iName & $iExp)
						FileDelete($sFolderName & '\' & $iName & $iExp)
						
					Case Else
						_MsgBox(0, $tMessage, $tNoEngine & "idTech Engine")
				EndSwitch
			
			Case '_Infinity'
				Switch $iExp
					Case '.key'
						_OtherPRGExt('_SAU', $sFileName)
						
					Case '.gob'
						_QuickBMSRun($iExtList, @ScriptDir &  "\data\scripts\baldurs_gate_da_gob.bms ", $sFileName)
						
					Case '.lmp'
						_QuickBMSRun($iExtList, @ScriptDir &  "\data\scripts\LMP.bms ", $sFileName)
						_QuickBMSRun($iExtList, @ScriptDir &  "\data\scripts\baldurs_gate_gc_lmp.bms ", $sFileName)
						_QuickBMSRun($iExtList, @ScriptDir &  "\data\scripts\baldurs_gate_da_lmp.bms ", $sFileName)
				EndSwitch
			
			Case '_LithTech'
				Switch $iExp
					Case '.rez', '.Arch00', '.Arch01', '.Arch02', '.Arch03', '.Arch04', '.Arch05'
						_QuickBMSRun("", @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
						
					Case '.Arch06'
						_QuickBMSRun("", @ScriptDir & "\data\scripts\shadow_of_mordor.bms ", $sFileName)
				EndSwitch
				
			Case '_MTFramework'
				If $iExp = ".arc" then
					_QuickBMSRun('', @ScriptDir & "\data\scripts\dmc4.bms ", $sFileName)
				ElseIf $iExp = ".sngw" then
					_OtherPRGExt('_VGM', $sFileName)
				EndIf
				
			Case '_PopCapPackAll'
				Switch $iExp
					Case ".dll", ".obb"
						_OtherPRG('', '\data\7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
						
					Case ".pak" 
						_QuickBMSRun("", @ScriptDir & "\data\scripts\7x7m.bms ", $sFileName)
						
					Case ".dz" 
						_QuickBMSRun("", @ScriptDir & "\data\scripts\vector.bms ", $sFileName)
						
					Case Else
						_MsgBox(0, $tMessage, $tNoGame & "PopCap")
						Output_MSG(1, $sFileName)	
				EndSwitch
				
			Case '_ReEngine'
				Switch $iExp
					Case ".pak" 
						$iProcess = ShellExecute(@ScriptDir & "\data\quickbms.exe ", @ScriptDir & "\data\scripts\zip.bms " & '"' & @ScriptDir & '\data\retools\retools.zip" ' & @TempDir, @ScriptDir & "\data\scripts\", "open", @SW_HIDE)
						Sleep(1000)
						ProcessClose($iProcess)
						_OtherPRG('', "\data\retools\REtool.exe", ' -x ', ' -h ' & @TempDir & '\' & $iOther, $sFolderName, $sFileName)
						
					Case ".dds"
						_OtherPRG('', "\data\retools\REtool.exe", ' -dds ', '', $sFolderName, $sFileName)
						
					Case ".tex"
						_OtherPRG('', "\data\retools\REtool.exe", ' -tex ', '', $sFolderName, $sFileName)
						
					Case Else
						_MsgBox(0, $tMessage, $tNoGame & "Re Engine")
						Output_MSG(1, $sFileName)	
				EndSwitch
				
			Case '_RedEngine'
				Switch $iName & $iExp
					Case $iName & ".bundle" 
						_QuickBMSRun("", @ScriptDir & "\data\scripts\Witcher3.bms ", $sFileName)
						
					Case "texture.cache" 
						_OtherPRG('', "\data\lua_scripts\lua.exe", ' ' & @ScriptDir & '\data\lua_scripts\unpack_textures.lua ', $sFolderName, @ScriptDir & '\data\lua_scripts', $sFileName)
						$iFileList1 = _FileListToArray($sFolderName, "*.dds")
							$a = $iFileList1[0]
							
							For $i = 1 to $a
								$iDist = $sFolderName & '\' & StringReplace($iFileList1[$i], '#', '\')
								_PathSplit($iDist, $iDrive, $iDir, $iName, $iExp)
								If Not FileExists($iDrive & $iDir) Then DirCreate($iDrive & $iDir)
								FileMove($sFolderName & '\' & $iFileList1[$i], $iDist , 8)
								If Mod($i, 10) = 0 Then _BarCreate((100/$a) * $i, $tWtCoping, $tCopied & " " & $i & "/" & $a, 300, 95)
							Next
							
						ProgressSet(100, $tDone)
						_BarOff()
						
					Case $iName & ".w3strings" 
						_OtherPRG('', "\data\lua_scripts\lua.exe", ' ' & @ScriptDir & '\data\lua_scripts\inspect_w3strings.lua ', $sFolderName & '\' & $iName & '.txt', @ScriptDir & '\data\lua_scripts', $sFileName)
						
					Case $iName & ".w3speech" 
						_OtherPRG('', "\data\lua_scripts\lua.exe", ' ' & @ScriptDir & '\data\lua_scripts\inspect_w3speech.lua ', $sFolderName, @ScriptDir & '\data\lua_scripts', $sFileName)
						
					Case $iName & ".w2strings" 
						_OtherPRG('', "\data\gibbed\Gibbed.RED.Strings.exe", ' -d ', $sFolderName & '\' & $iName & '.xml', $sFolderName, $sFileName)
						
					Case $iName & ".xml"
						_OtherPRG('', "\data\gibbed\Gibbed.RED.Strings.exe", ' -e ', $sFolderName & '\' & $iName & '.w2strings', $sFolderName, $sFileName)
						
					Case $iName & ".archive" ; CP2077
						_QuickBMSRun("", @ScriptDir & "\data\scripts\cyberpunk_2077.bms ", $sFileName)
						
					Case $iName & ".dzip" 
						If GUICtrlRead($iReimport_Checkbox) = 1 Then 
							_OtherPRG('', "\data\gibbed\Gibbed.RED.Pack.exe", '', $sFolderName, $sFolderName, $sFileName)
						Else
							_OtherPRG('', "\data\gibbed\Gibbed.RED.Unpack.exe", '', $sFolderName, $sFolderName, $sFileName)
						EndIf
						
						;_QuickBMSRun("", @ScriptDir & "\data\scripts\witcher2.bms ", $sFileName) ;Прога вместо этого скрипта ↑
					;TODO: Добавить поддержку форматов ниже ↓
					; Case $iName & ".w2speech" 
						; Sleep(1)
					; Case $iName & ".w2scripts" 
						; Sleep(1)
					; Case $iName & ".redscripts" 
						; Sleep(1)
					; Case $iName & ".cache" 
						; Sleep(1)
					Case Else
						_MsgBox(0, $tMessage, $tNoGame & "Red Engine")
						Output_MSG(1, $sFileName)
				EndSwitch	
			
			Case '_RPGMaker'
				;ShellExecuteWait(@ScriptDir & '\data\RgssDecrypter.exe ', ' -o "' & $sFolderName & '" "' & $sFileName & '"')
				;_OtherPRG($iExtList, "RgssDecrypter.exe ", ' -o "' & $sFolderName & '"', '', $sFolderName, $sFileName)
				Switch $iExp
					Case '.rgssad', '.rgss2a', '.rgss3a'
						$size = FileGetSize($sFileName)
						$iOutputWindow = Run(@ScriptDir & "\data\RgssDecrypter.exe " & '-o "' & $sFolderName & '" "' & $sFileName & '"', $iDrive & $iDir, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
						_EnginePB($iOutputWindow, 110, 1, '[]\/', 4, 3)
						
					Case '.rpgmvp', '.rpgmvo', '.rpgmvm'
						;TODO Make with rmvdec
						_MsgBox(0, '', 'Work in process')
						
					Case '.pak'
						_OtherPRG('', '\data\7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
				EndSwitch

			Case '_Sen'
				Switch $iExp
					Case '.pkg'	
						_QuickBMSRun("", @ScriptDir & "\data\scripts\legend_of_heroes.bms ", $sFileName)
						
					Case '.phyre'
						_QuickBMSRun("", @ScriptDir & "\data\scripts\PhyreEngine_PTexture2D_phyre.bms ", $sFileName)
						
					Case '.dat'
					
						If StringInStr($iName, 'book') > 0 Then 
							If GUICtrlRead($iReimport_Checkbox) = 1 Then _Console(@ScriptDir & "\data\python_script\tocs_book.py")
							If GUICtrlRead($iReimport_Checkbox) = 4 Then _Console(@ScriptDir & "\data\python_script\tocs_book2dat.py")
						EndIf
						
						If GUICtrlRead($iReimport_Checkbox) = 4 Then _OtherPRG('', '\data\SSD\SenScriptsDecompiler.exe ', $iOther, $sFolderName, $sFolderName, $sFileName)
						
					Case '.xlsx'
						_OtherPRG('', '\data\SSD\SenScriptsDecompiler.exe ', $iOther, $sFolderName, $sFolderName, $sFileName)
				EndSwitch
			
			Case '_TellTale'
				;_OtherPRG($iExtList, '\data\ttarchext.exe ', '-m ' & $iOther & ' ', '"' & $sFolderName & '"', @ScriptDir & '\data', $sFileName)
				$size = FileGetSize($sFileName)
				$iOutputWindow = Run(@ScriptDir & "\data\ttarchext.exe " & '-o -m ' & $iOther & ' "' & $sFileName & '" "' & $sFolderName & '"', $iDrive & $iDir, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
				_EnginePB($iOutputWindow, 110, $size)
			
			Case '_Unigene'
				;_OtherPRG($iExtList, "\data\uniginex.exe ", '', ' "' & $sFolderName & '"', $sFolderName, $sFileName)
				$size = FileGetSize($sFileName)
				$iOutputWindow = Run(@ScriptDir & "\data\uniginex.exe " & ' -o "' & $sFileName & '" "' & $sFolderName & '"', $iDrive & $iDir, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
				_EnginePB($iOutputWindow, 115, $size)
				
			Case '_Unity'
				If $iExp = '.unitypackage' Then
					_OtherPRG('', '\data\7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
					_OtherPRG('', '\data\7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFolderName & '\archtemp.tar')
					FileDelete($sFolderName & '\archtemp.tar')
				Else
					$iUnityPath = $iDrive & StringLeft($iDir, StringLen($iDir) - 1)
					$iOutputWindow = Run(@ScriptDir & '\data\AssetStudio\AssetStudioCLI.exe "' & $iUnityPath & '" "' & $sFolderName & '" --game Normal', @ScriptDir & '\data\AssetStudio', @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
					_EnginePB($iOutputWindow, 110, 1, ' []/', 6, 5)
				EndIf
			
			Case '_Unreal', '_Unreal4'
				If $iExp = ".locres" then
					Unreal4LR($sFileName)
					$iOutputWindow = 0
				ElseIf $iExp = ".umod" then
					_QuickBMSRun('', @ScriptDir & "\data\scripts\unreal_umod.bms.bms ", $sFileName)
				ElseIf $iExp = ".pak" then
					_StringChange(@ScriptDir & "\data\scripts\unreal_tournament_4.bms", 'set AES_KEY binary "' & $iOther & '"', 11)
					_QuickBMSRun('', @ScriptDir & "\data\scripts\unreal_tournament_4.bms ", $sFileName)
				Else
					;_OtherPRG('', 'extract.exe', ' -extract -out="' & $sFolderName & '" ', '', @ScriptDir & '\Data', $sFileName)
					$iOutputWindow = Run(@ScriptDir & '\data\extract.exe -extract -out="' & $sFolderName & '" "' & $sFileName & '"', $sFolderName, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
					_EnginePB($iOutputWindow, 95)
				EndIf
			
			;Остальные движки, файлы которых распаковываются через QuickBMS
			Case '_Source', '_RenPy', '_GameMaker', '_Asura', '_Anvil', '_Snowdrop'
				_QuickBMSRun($iExtList, @ScriptDir &  $iScriptName, $sFileName)
				
		EndSwitch
		;Для прочих программ: Список_расширений, Название_программы, Комманда_перед_именем_файла, Комманда_после_имени_файла, Рабочая_папка, Имя_файла, Файл или папка(True - файл, False - папка))
	Next
EndFunc

Func ControlV($clip)
	ClipPut($clip)
	Send('^v')
	Send('{ENTER}')
EndFunc

Func _EnginePB($iOutputWindow, $iSize, $mode = 1, $delimeter = ' /\', $id1 = 3, $id2 = 2)
;Процесс, Высота прогресс-бара, режим, разделитель строки(для замены и подстановки), текущее кол-во файлов в архиве, общее кол-во файлов в архиве
	Local $per, $per1
	$iLog = FileOpen(@ScriptDir & '\log.txt', 8+2)
	$a = 0
	
	While 1
		$line = StdoutRead($iOutputWindow)
		$line1 = StderrRead($iOutputWindow)
		
		If BitOR(@error, GUIGetMsg($progressGUI) = $exitBTN) Then 
			ProcessClose($iOutputWindow)
			ExitLoop
		Else
			If $line <> '' Then FileWriteLine($iLog, $line)
			If $line1 <> '' Then FileWriteLine($iLog, $line1)
		EndIf
		
		If $mode = 1 Then
			$per = StringSplit($line, @CRLF)
			
			If $per[0] > 2 Then 
				$per1 = StringSplit($per[UBound($per) - 3], $delimeter)
				; _ArrayDisplay($per1)
				Local $indexes = [$id1, $id2]
				
				If $per1[0] >= _ArrayMax($indexes) Then 
					$iMSGU = $tDone & ': ' & $per1[$id2] & '/' & $per1[$id1]
					_BarCreate(100/$per1[$id1] * $per1[$id2], $tUnpacking, $iMSGU, 300, $iSize, 45, True) 
					GUICtrlSetData($iEdit, $iMSGU & @CRLF, 1)
				EndIf
			EndIf
			
		ElseIf $mode > 1 Then
		
			$per = StringSplit($line, @CRLF)
			If $per[0] > 2 Then 
			
				For $i = 0 to UBound($per) - 2
					$per1 = StringSplit($per[$i], ' ' & @TAB)
					
					If $per1[0] > 7 Then 
						$prc = StringLeft(100/$mode * Dec($per1[3]), 4)
						$str = $per1[UBound($per1) - 1]
						If BitOR(StringInStr($str, '\'), StringInStr($str, '.')) < 1 Then $str = $line
						_BarCreate($prc, $tUnpacking, $str, 300, $iSize, 45, True)
						GUICtrlSetData($iEdit, $str & @CRLF, 1)
					EndIf
				Next
			EndIf
		EndIf
	Wend
	
	FileClose($iLog)
	GUICtrlSetData($iEdit, $tDone & '!' & @CRLF, 1)
	_BarOff()
	
EndFunc
