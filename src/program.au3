
Func _QuickBMSRun($iExtList, $iScriptName, $sFileName = '', $sFolder = $sFolderName) ;Для скриптов BMS: Список_расширений, Название_скрипта, Имя_файла
; Исправлено!
	Switch $sFileName					
		Case '', ' ', '	', "", " ", "	"
			$sFileName = FileOpenDialog ($tSelectFile, "", $iExtList & $tAllFile & " (*.*)", 1+4)
				If @error = 1 then Return
		EndSwitch
	_PathSplit ($iScriptName, $iDrive, $iDir, $iName, $iExp)
	$iFileList = StringSplit ($sFileName, '|')
	Local $a = UBound($iFileList) - 1, $fc = 2
	If $a = 1 Then $fc = 1
	GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)	
	For $i = $fc to $a
		If $iFileList[0] > 1 Then $sFileName = $iFileList[1] & '\' & $iFileList[$i]
			If GUICtrlRead($iHideOrShow) = 1 Then
				$iOutputWindow = ShellExecuteWait (@ScriptDir & "\data\quickbms.exe ", $rI & $iScriptName & ' "' & $sFileName & '" "' & $sFolder & '"', $iDrive & $iDir, "open")
				Output_MSG($iOutputWindow, $sFileName)
			Else
				_Console (@ScriptDir & "\data\quickbms.exe " &  $rI & $iScriptName & '"' & $sFileName & '" "' & $sFolder & '"')
			EndIf
	Next
EndFunc

Func _QuickBMSRunWCX2($iExtList, $iScriptName, $sFileName, $iExt2) 
	Switch $sFileName
		Case '', ' ', '	', "", " ", "	"
			$sFileName = FileOpenDialog ($tSelectFile, "", $iExtList & $tAllFile & " (*.*)", 1)
				If @error = 1 then Return
		EndSwitch
	GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)
	ShellExecuteWait (@ScriptDir & "\data\quickbms.exe ", $iScriptName & '"' & $sFileName & '" "' & $sFolderName & '"', @ScriptDir & "\data\wcx\", "open")
	FileMove ($sFolderName & "\*." & $iExt2, $sFolderName & "\unpack." & $iExt2)
	$iOutputWindow = ShellExecuteWait (@ScriptDir & "\data\quickbms.exe ", $iScriptName & '"' & $sFolderName & "\unpack."  & $iExt2 & '" "' & $sFolderName & '"', @ScriptDir & "\data\wcx\", "open")
	FileDelete ($sFolderName & "\unpack."  & $iExt2)
	Output_MSG($iOutputWindow, $sFileName)
EndFunc

Func _SAU($sFileName = '')
	Switch $sFileName
		Case '', ' ', '	', "", " ", "	"
			$sFileName = FileOpenDialog($tSelectFile, "", $tAllSupp & "(*.adf;*.agg;*.bdx;*.spr;*.pak;*.box;*.brig;*.chr;*.dat;*.bin;*.cam;*.cc;*.cmp;mas0*;*.df2;*.*c;*.rm;*.anm;*.4pp;*.epf;*.flx;*.gor;*.h4r;*.hrs;*.idx;*.ilb;*.key;*.lbx;*.lod;*.group;*.bin;*.mpq;*.dbi;*.ff;*.wdb;*.mul;*.nds;*.p00;*.p10;*.p99;*.pak;*.res;*.snd;*.tgw;*.tlb;*.uop;*.vid;*.vsr;*.war;*.xua;*.xub;*.jun;*.maa;*.jus;*.fan)|Amiga Disk File (*.adf)|Heroes of Might & Magic 1-2 (*.agg)|Black Moon Chronicles, Persian Wars (*.SPR)|Beats of Rage " & $tArchives & " (*.pak)|Beasts & Bumpkins " & $tArchives & " (*.box)|Brigandine (*.brig)|Beyond the Beyond (*CHR;*.DAT;*.BIN)|Cyberlore Library Manager (*.cam)|Kings Bounty " & $tAnd & " Might & Magic 3/4/5 " & $tArchives & " (*.cc)|Divine Divinity" & $tArchive & "(*.cmp)|Dark Seal 2: Wizard Fire (mas0*)|Tibia MMORPG (Tibia.dat)|Heroes of Might & Magic 4 sprite " & $tArchives & " (*.df2)|Divine Divinity sprite" & $tArchive & "(*.*c)|Dominus (*.rm;*anm;*.4pp;*.dat)|Realms of Arkania 2 (*.DAT)|East Point File System (*.epf)|Ultima 7, 8 " & $tAnd & " Crusader No Remorse " & $tArchives & " (*.flx)|Myth Fallen Lords " & $tArchives & " " & $tAnd & " Tagged Files (*.gor)|Stonekeep groupXX " & $tArchives & " (*.group)|Heroes of Might & Magic 4 " & $tArchives & " (*.h4r)|Heimdall (*.bin;*.dat)|Faery Tale Adventure 2 " & $tAnd & " Dinotopia " & $tArchives & " (*.hrs)|Jinyong Qunxia Zhuan " & $tArchives & " (*.idx)|Age of Wonders 1-2 image " & $tArchives & " (*.ilb)|Infinity Engine Directory (*.key)|Master of Magic " & $tArchives & " (*.lbx)|Lunar: Genesis / Dragon Song (*.dat)|Cyberlore Library (*.lib)|LOD " & $tArchives & " (*.lod)Majesty for IPhone/IPad (*.group.bin)|Blizzard MPQ " & $tArchives & " (*.mpq)|Disciples: Sacred Lands (*.DBI;*.FF;*.WDB)|Ultima Online" & $tArchive & "(*.mul)|Nintendo Nitro Filesystem " & $tAnd & " Formats (*.NDS)|Popolocrois" & $tArchive & "(*.p00;*.p1;*.p99)|Helbreath sprite " & $tArchives & " (*.pak)|Rage of Mages 1-2 (Allods) " & $tArchives & " (*.res)|Mystic Towers (rgmystus.dat)|SND " & $tArchives & " (*.snd)|Kohan: Immortal Sovereigns " & $tArchives & " (*.tgw)|SSI Tileset (*.tlb)|Ultima Online Mythic Package (*.uop)|Vandal Hearts (*.DAT)|VID " & $tArchives & " (*.vid)|Lemmings Paintball (*.vsr)|Warcraft 1 " & $tAnd & " 2 " & $tArchives & " (*.war)|Original Mulan " & $tArchives & " (*.XUA;*.XUB;*.JUN;*.MAA;*.JUS;*.FAN)|", 1)
				If @error = 1 then Return
		EndSwitch
		If @error <> 1 Then
			_PathSplit($sFileName, $iDrive, $iDir, $iName, $iExp)
			_OtherPRG('', 'sau.exe', ' ', " " & $sFolderName & '\', $iDrive & '\' & $iDir, $iName & $iExp)	
		EndIf
EndFunc

Func _OtherPRG($iExtList, $iPRGName, $iCommand1 = ' ', $iCommand2 = '', $iWorkDir = $sFolderName, $sFileName = '', $iFF = True) 
;Для прочих программ: Список_расширений, Название_программы, Комманда_перед_именем_файла, Комманда_после_имени_файла, Рабочая_папка, Имя_файла, Файл или папка (True - файл, False - папка))
; Исправлено!
	Switch $sFileName					
		Case '', ' ', '	', "", " ", "	"
			If $iFF = True Then
				$sFileName = FileOpenDialog ($tSelectFile, "", $iExtList & $tAllFile & " (*.*)", 1+4)
					If @error = 1 then Return
			ElseIf $iFF = False Then
				$sFileName = FileSelectFolder ('', $iLastDir)
					If @error = 1 then Return
			EndIf
	EndSwitch
	$iFileList = StringSplit ($sFileName, '|')
	Local $a = UBound($iFileList) - 1, $fc = 2
	If $a = 1 Then $fc = 1
	For $i = $fc to $a
		If $iFileList[0] > 1 Then $sFileName = $iFileList[1] & '\' & $iFileList[$i]
		If GUICtrlRead($iHideOrShow) = 1 Then
			$iOutputWindow = ShellExecuteWait (@ScriptDir & "\data\" & $iPRGName, $iCommand1 & '"' & $sFileName & '" ' & $iCommand2, $iWorkDir, "open")
			Output_MSG($iOutputWindow, $sFileName)
		Else
			_Console (@ScriptDir & "\data\" & $iPRGName & " " & $iCommand1 & '"' & $sFileName & '" ' & $iCommand2, $iWorkDir)
		EndIf
	Next
EndFunc

Func _ScriptCreate($iStringArray, $iJobFolder = $sFolderName)
	$hFile = FileOpen(@TempDir & "\temp.bat", 10)
	FileWriteLine ($hFile, "chcp 65001")
	If Not IsArray($iStringArray) Then FileWriteLine ($hFile, $iStringArray)
	For $i = 0 to UBound($iStringArray)-1
		FileWriteLine ($hFile, $iStringArray[$i])
	Next
	FileWriteLine ($hFile, "pause")
	FileClose ($hFile)
	ShellExecuteWait (@TempDir & "\temp.bat", "", $iJobFolder, "open")
	FileDelete (@TempDir & "\temp.bat")
EndFunc

Func _OtherPRG4Folder($iPRGName, $iCommand1, $iCommand2, $iWorkDir, $sFileName = '')
	Switch $sFileName
		Case '', ' ', '	', "", " ", "	"
			$sFileName = FileSelectFolder("", $iLastDir)
				If @error = 1 then Return
	EndSwitch
			GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)
			$iOutputWindow = ShellExecuteWait (@ScriptDir & "\data\" & $iPRGName, $iCommand1 & $sFileName & $iCommand2, $iWorkDir, "open")
			Output_MSG($iOutputWindow, $sFileName)
EndFunc

Func _DosBox($iExtList, $iProgName, $iArg1, $iArg2, $sFileName = '') ;Для старых программ, работающих через DosBox: Список_расширений, Название_программы, Аргумент_имени_файла (1 или 0), Комманда
	Switch $sFileName
		Case '', ' ', '	', "", " ", "	"
			$sFileName = FileOpenDialog ($tSelectFile, " ", $iExtList & $tAllFile & " (*.*)", 1)
				If @error = 1 then Return
		EndSwitch
			_PathSplit($sFileName, $iDrive, $iDir, $iName, $iExp)
				If $iArg1 = 1 Then
					$FullName = $iName & $iExp
				ElseIf $iArg1 = 0 Then
					$FullName = ''
				EndIf
			$iFile = FileOpen($sFolderName & "\dosbox.conf", 2)
			FileWrite ($iFile, "[autoexec]" & @CRLF & "@ECHO OFF" & @CRLF & 'MOUNT C "."' & @CRLF & "C:" & @CRLF & $iProgName & $FullName & $iArg2 & @CRLF & "EXIT")
			FileClose ($iFile)
			FileCopy (@ScriptDir & "\data\" & $iProgName, $sFolderName)
			FileCopy (@ScriptDir & "\data\dos4gw.exe", $sFolderName)
			FileCopy ($sFileName, $sFolderName)
			GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)
			ShellExecute (@ScriptDir & "\data\DosBox.exe", "", $sFolderName, "open")
			Sleep(5000)
			Send("1{ENTER}")
			ProcessWaitClose ("dosbox.exe")
			FileDelete ($sFolderName & "\" & $iProgName)
			FileDelete ($sFolderName & "\dos4gw.exe")
			FileDelete ($sFolderName & '\' & $iName & $iExp)
			FileDelete ($sFolderName & "\dosbox.conf")
			GUICtrlSetData($iEdit, $tDone & @CRLF, 1)
EndFunc

Func _WithArray($iGameName, $iFileArray, $iPRGName, $iSubFolder = '') ;Для программ, в которых нужно копировать файлы списком
; Исправлено!
	$sFolderPath = FileSelectFolder ($tSGF & $iGameName, $iLastDir)
		If @error = 1 then Return
			GUICtrlSetData($iEdit, $tWtCoping & @CRLF, 1)
			If $iSubFolder <> '' Then
				DirCreate ($sFolderName & $iSubFolder)
			EndIf
			$a = UBound($iFileArray)
			ProgressOn('', $tWtCoping, '', (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)
			For $i = 0 to $a - 1
				FileCopy ($sFolderPath & $iFileArray[$i], $sFolderName & $iSubFolder)
				GUICtrlSetData($iEdit, $tCopied & " " & $i & "/" & $a & @CRLF, 1)
				ProgressSet((100/$a) * $i, $tCopied & " " & $i & "/" & $a )
			Next			
			ProgressSet(100, $tDone)
			ProgressOff()
			FileCopy (@ScriptDir & "\Data\" & $iPRGName, $sFolderName)
			GUICtrlSetData($iEdit, $tCopied & " " & $a & "/" & $a  & @CRLF, 1)
			$iOutputWindow = ShellExecuteWait ($sFolderName & '\' & $iPRGName, "", $sFolderName, "open")
			For $j = 0 to $a - 1
				FileDelete ($sFolderName & $iFileArray[$j])
			Next
			FileDelete ($sFolderName & '\' & $iPRGName)
			Output_MSG($iOutputWindow, $sFileName)
EndFunc

Func _StringChange($sScriptName, $iString, $X) ;Путь к файлу, в котором нужно заменить строку, Новая строка, Номер строки
	Local $iStringScript
	_FileReadToArray ($sScriptName, $iStringScript)
	$iStringScript[$X] = $iString
	_FileWriteFromArray ($sScriptName, $iStringScript, 1)
EndFunc

Func Xenus($iProg);TODO: Удалить этот говнокод!!!
	$sFilePath = FileOpenDialog($tSelectFile, " ", "GRP File (*.grp)|" & $tAllFile & " (*.*)", 1)
		If @error = 1 then Return
			_PathSplit($sFilePath, $iDrive, $iDir, $iName, $iExp)
			$sFullFileName = ($iName & ".grp")
			$sJobFolder = StringReplace ($sFilePath, $sFullFileName, "")
			$hFile = FileOpen (@TempDir & "\start.bat", 10)
			FileWriteLine ($hFile, "chcp 65001")
			FileWriteLine ($hFile, "copy """ & @ScriptDir & "\data\" & $iProg & ".exe"" """  & $sJobFolder & """")
			FileWriteLine ($hFile, "set __compat_layer=WINXPSP3")
			FileWriteLine ($hFile, """" & $sJobFolder & $iProg & ".exe"" """ & $sFilePath & """")
			FileWriteLine ($hFile, "pause")
			FileClose ($hFile)
			$iOutputWindow = ShellExecute (@TempDir & "\start.bat", "", $sFolderName, "open")
			FileDelete (@TempDir & "\start.bat")
			Output_MSG($iOutputWindow, $sFileName)
EndFunc

Func Xenus2();TODO: Удалить этот говнокод!!!
	$sFilePath = FileOpenDialog($tSelectFile, " ", "GRP File (*.grp)|" & $tAllFile & " (*.*)", 1)
		If @error = 1 then Return
			_PathSplit($sFilePath, $iDrive, $iDir, $iName, $iExp)
			$sFullFileName = ($iName & ".grp")
			$sJobFolder = StringReplace ($sFilePath, $sFullFileName, "")
			$hFile = FileOpen (@TempDir & "\start.bat", 10)
			FileWriteLine ($hFile, "chcp 65001")
			FileWriteLine ($hFile, "copy """ & @ScriptDir & "\data\GrpUnpacker.exe"" """  & $sJobFolder & """")
			FileWriteLine ($hFile, """" & $sJobFolder & "GrpUnpacker.exe"" """ & $sFilePath & """")
			FileWriteLine ($hFile, "pause")
			FileClose ($hFile)
			ShellExecute (@TempDir & "\start.bat", "", $sFolderName, "open")
			FileDelete (@TempDir & "\start.bat")
EndFunc

Func _Console($Cmd, $WorkDir = $sFolderName)

	GUICtrlSetData($iEdit, @CRLF & $Cmd & @CRLF, 1)
	$iOutputWindow = Run($Cmd, $WorkDir, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)

	StdinWrite($iOutputWindow)

	While 1
		$line = StdoutRead($iOutputWindow)
		If @error Then ExitLoop
		GUICtrlSetData($iEdit, $line, 1)
	Wend

	While 1
		$line1 = StderrRead($iOutputWindow)
		If @error Then ExitLoop
		GUICtrlSetData($iEdit, $line1, 1)	
	Wend
	
		GUICtrlSetData($iEdit, @CRLF & $tDone & @CRLF, 1)
	
EndFunc
