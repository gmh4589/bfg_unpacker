;Содержит функции, вызываемые из интерфейса программы


Func OSLang()
	Switch @OSLang
		Case "0419", "0819", "0422", "0423", "0437", "082c", "0443", "0843", "043f", "0444", "0440"
			Return "russian"
		Case Else
			Return "english"
	EndSwitch
EndFunc

Func SelectFolder()
	$sFN = FileSelectFolder($tFolder1, '')
		If @error <> 1 Then
			$sFolderName = $sFN
			IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Path', $sFolderName)
		EndIf
EndFunc

Func _FileList($iFolderList, $pPath = @TempDir)
	$hFile = FileOpen(@TempDir & "\temp.bat", 10)
	FileWriteLine($hFile, "chcp 65001")
	FileWriteLine($hFile, "@echo off")
	FileWriteLine($hFile, "DIR/B/O:N/S """ & $iFolderList & """ > " & $pPath & "\file_list.txt");
	FileClose($hFile)
	$iOutputWindow = ShellExecuteWait(@TempDir & "\temp.bat", "", @ScriptDir, "open")
	Dim $iFileList1
	_FileReadToArray($pPath & "\file_list.txt", $iFileList1)
	FileDelete(@TempDir & "\temp.bat")
	Output_MSG($iOutputWindow, $iFolderList)
	Return $iFileList1
EndFunc

Func SelectLang()
	$sLangName = FileOpenDialog($tLNGSlct, @ScriptDir & "\data\local", "Localized Files(*.loc)", 1)
		If @error = 1 Then Return
			_PathSplit($sLangName, $iDrive, $iDir, $iName, $iExp)
			IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Language', $iName)
			_ScriptRestart(100)
EndFunc

Func ClearFolder($iTrash = False)
	If $iTrash = False Then $tDELAll = $tDELAll1
	If $iTrash = True Then $tDELAll = $tDELAll2
	$iAnswer = _MsgBox(4, $tWRNNG, $tDELAll & @CRLF & $sFolderName & "?")
		If $iAnswer = 6 Then
		
			Local $iFileList1 = _FileListToArray($sFolderName)
			$a = UBound($iFileList1)
			If $a = 0 Then Return(_MsgBox(0, $tMessage, $tFolderEmpty))
			
			Dim $Hour, $Mins, $Secs
			$begin = TimerInit()

			For $i = 0 to $a - 1
				If $iTrash = False Then FileDelete($sFolderName & '\' & $iFileList1[$i])
				If $iTrash = False Then DirRemove($sFolderName & '\' & $iFileList1[$i], 1)
				If $iTrash = True Then FileRecycle($sFolderName & '\' & $iFileList1[$i])
				$Percent =(100/$a) * $i
				$dif = TimerDiff($begin)
				$elaps =(($dif/$i) * $a) - $dif
				_TicksToTime(Int($dif), $Hour, $Mins, $Secs)
				$time = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
				_TicksToTime(Int($elaps), $Hour, $Mins, $Secs)
				$elaps = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
				If BitOr(Mod($i, 10) = 0, $a < 20) Then _BarCreate($Percent, $tWait, $tDeleting & $iFileList1[$i] & @CRLF & $tLeft & $i & $tFrom & $a - 1 & @TAB & StringLeft($Percent, 4) & ' %' & @CRLF & $tPassed & $time & @TAB & $tElapsed & $elaps, 300, 120)
			Next

		$dif = TimerDiff($begin)
		_TicksToTime(Int($dif), $Hour, $Mins, $Secs)
		$dif = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
		Sleep(1000)
		_BarOff()
		GUICtrlSetData($iEdit, $tAllFFF & @CRLF & $sFolderName & @CRLF & $tAlldel & @CRLF, 1)
		EndIf
EndFunc

Func DeFo()
	$iAnswer = _MsgBox(4, $tWRNNG, $tDAEFFF & @CRLF & $sFolderName & "?" & @CRLF & $tNote & @CRLF & $tUIFIDW & @CRLF & $tFOSAF)
		If $iAnswer = 6 then
		
			If UBound(_FileListToArray($sFolderName)) = 0 Then Return(_MsgBox(0, $tMessage, "Папка пуста!"))
			
			ShellExecuteWait(@ScriptDir & "\data\defo.bat", "", $sFolderName, "open")
			_MsgBox(0, $tMessage, $tAllFFF & @CRLF & $sFolderName & @CRLF & $tAlldel)
			GUICtrlSetData($iEdit, $tAllFFF & @CRLF & $sFolderName & @CRLF & $tAlldel & @CRLF, 1)
		EndIf
EndFunc

Func DeFi()
	$iAnswer = _MsgBox(4, $tWRNNG, $tDFWS0BFF & @CRLF & $sFolderName & "?" & @CRLF & $tFISAND & @CRLF & @CRLF & $tNote & @CRLF & $tUIFIDW & @CRLF & $tFOTFSOA)
		If $iAnswer = 6 Then
		
			Local $iFileList1 = _FileListToArray($sFolderName)
			$a = UBound($iFileList1)
			If $a = 0 Then Return(_MsgBox(0, $tMessage, "Папка пуста!"))
			
			For $i = 1 to $a - 1
				$iSize = FileGetSize($sFolderName & '\' & $iFileList1[$i])
				If $iSize = 0 Then FileDelete($sFolderName & '\' & $iFileList1[$i])
			Next
			
			_MsgBox(0, $tMessage, $tAllFFF & @CRLF & $sFolderName & @CRLF & $tAlldel)
			GUICtrlSetData($iEdit, $tAllFFF & @CRLF & $sFolderName & @CRLF & $tAlldel & @CRLF, 1)
		EndIf
EndFunc

Func MakeFolder()
	_MsgBox(4, $tWRNNG, $tCrFld & @CRLF & $sFolderName & "?")
		If $iAnswer = 6 Then
			DirCreate($sFolderName)
			GUICtrlSetData($iEdit, $tFolder2 & @CRLF & $sFolderName & @CRLF & $tCreated & @CRLF, 1)
		EndIf
EndFunc

Func Output_MSG($iOutputWindow, $iFName = '') ;Исправлено
	If $iInvert = 1 then
		If $iOutputWindow = 1 then
			$iOutputMsg =($tDone)
		Else
			$iOutputMsg =($tError)
		EndIf
		$iInvert = 0
	Else
		If $iOutputWindow = 0 then
			$iOutputMsg =($tDone)
		Else
			$iOutputMsg =($tError)
		EndIf
	EndIf
		GUICtrlSetData($iEdit, $iOutputMsg & ': ' & $iFName & '!' & @CRLF, 1)
EndFunc

Func _ScriptRestart($iTime)
	$hFile = FileOpen(@TempDir & "\temp.bat", 10)
	FileWriteLine($hFile, @ScriptFullPath)
	FileClose($hFile)
	Sleep($iTime)
		ShellExecute(@TempDir & "\temp.bat", "", $sFolderName, "open", @SW_HIDE)
	Exit
EndFunc

Func AutoSearch()
	$sFileName = FileOpenDialog($tSelectFile, " ", $tAllFile & "(*.*)", 1)
		If @error = 1 Then Return
		
			Local $iArr = [@CRLF & $tWaitList, @CRLF & $tSP_msg1, @CRLF & $tSP_msg2, @CRLF & $tSP_msg3, @CRLF & $tSP_msg4, "'it's not possible to create that file...'", "'...'", "'if you press ENTER a new name will be generated automatically'", "'OLD:'", "'NEW:'", $tSP_msg5, '']
			
			For $iString in $iArr
				GUICtrlSetData($iEdit, $iString & @CRLF, 1)
			Next
			
			$iFile = FileOpen(@TempDir & "\bfgunpacker\list.bat", 10)
			FileWriteLine($iFile, "chcp 65001")
			FileWriteLine($iFile, "@echo off")
			FileWriteLine($iFile, "DIR/B/O:N/S """ & @ScriptDir & "\data" & """ > " & @TempDir & "\bfgunpacker\file_list.txt")
			FileClose($iFile)
			$iOutputWindow = ShellExecuteWait(@TempDir & "\bfgunpacker\list.bat", "", $sFolderName, "open")
			FileDelete(@TempDir & "\bfgunpacker\list.bat")

			$hFile = FileOpen(@TempDir & "\bfgunpacker\search_plugin.bat", 10)
			FileWriteLine($hFile, "chcp 65001")
			FileWriteLine($hFile, "echo")
	
			Local $iStringCount = _FileCountLines(@TempDir & "\bfgunpacker\file_list.txt")
			
			For $a = 1 to $iStringCount
				$iScriptName = FileReadLine(@TempDir & "\bfgunpacker\file_list.txt", $a)
				_PathSplit($iScriptName, $iDrive, $iDir, $iName, $iExp)
					Switch $iExp
						Case ".wcx",".bms"
							DirCreate($sFolderName & "\" & $iName)
							FileWriteLine($hFile, @ScriptDir & "\data\quickbms.exe " & $iScriptName & ' "' & $sFileName & '" "' & $sFolderName & "\" & $iName & '"')
					EndSwitch
				$Percent =(100/$iStringCount) * $a
				If Mod($a, 100) = 0 Then _BarCreate($Percent, "Подождите...", $a & '\' & $iStringCount, 300, 90)
			Next
			_BarOff()
			
			FileWriteLine($hFile, "Pause")
			FileClose($hFile)
			
			ShellExecuteWait(@TempDir & "\bfgunpacker\search_plugin.bat", "", $sFolderName, "open")
			FileDelete(@TempDir & "\bfgunpacker\search_plugin.bat")
			FileDelete(@TempDir & "\bfgunpacker\file_list.txt")
			ShellExecuteWait(@ScriptDir & "\data\defo.bat", "", $sFolderName, "open")
EndFunc
