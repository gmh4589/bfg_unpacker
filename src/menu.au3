;Содержит функции, вызываемых из интерфейса программы

Func AppClose()
	FileDelete (@TempDir & "\start.bat")
		Exit
EndFunc

Func _CloseWin()
	GUISetState(@SW_HIDE, @GUI_WinHandle)
EndFunc

Func FolderProbe()
	Global $sFolderName = IniRead (@ScriptDir & '\unpacker.ini', 'Main', 'Path', '')
	If $sFolderName = '' Then 
		SelectFolder()
	EndIf
EndFunc

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
			_ScriptRestart(100)
		EndIf
EndFunc

Func _FileList($iFolderList, $pPath = @TempDir)
	$hFile = FileOpen(@TempDir & "\temp.bat", 10)
	FileWriteLine ($hFile, "chcp 65001")
	FileWriteLine ($hFile, "@echo off")
	FileWriteLine ($hFile, "DIR/B/O:N/S """ & $iFolderList & """ > " & $pPath & "\file_list.txt");
	FileClose ($hFile)
	$iOutputWindow = ShellExecuteWait (@TempDir & "\temp.bat", "", @ScriptDir, "open")
	Dim $iFileList1
	_FileReadToArray($pPath & "\file_list.txt", $iFileList1)
	FileDelete (@TempDir & "\temp.bat")
	Output_MSG($iOutputWindow, $iFolderList)
	Return $iFileList1
EndFunc

Func SelectLang()
	$sLangName = FileOpenDialog($tLNGSlct, @ScriptDir & "\data\local", "Localized Files (*.loc)", 1)
		If @error = 1 Then Return
			_PathSplit ($sLangName, $iDrive, $iDir, $iName, $iExp)
			IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Language', $iName)
			_ScriptRestart(100)
EndFunc

Func ClearFolder(); TODO: ТЕКСТ НА РУССКОМ!!!
	$iAnswer = MsgBox(BitOR($MB_YESNO, $MB_SYSTEMMODAL), $tWRNNG, $tDELAll & @CRLF & $sFolderName & "?")
		If $iAnswer = 6 Then
			Local $iFileList1 = _FileListToArray ($sFolderName)
			;_ArrayDisplay($iFileList1, "$FileList")
			$a = UBound ($iFileList1)
			
			If $a = 0 Then 
				MsgBox($MB_SYSTEMMODAL, $tMessage, "Папка пуста!")
				Return
			EndIf
			
			Dim $Hour, $Mins, $Secs
			$begin = TimerInit()

			ProgressOn ('', "Подождите...", '', (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)
			For $i = 0 to $a - 1
				FileDelete ($sFolderName & '\' & $iFileList1[$i])
				DirRemove ($sFolderName & '\' & $iFileList1[$i], 1)
				$Percent = (100/$a) * $i
				$dif = TimerDiff($begin)
				$elaps = (($dif/$i) * $a)
				_TicksToTime(Int($dif), $Hour, $Mins, $Secs)
				$time = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
				_TicksToTime(Int($elaps), $Hour, $Mins, $Secs)
				$elaps = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
				ProgressSet ($Percent, 'Удаление: ' & $iFileList1[$i] & @CRLF & 'Осталось ' & $i & ' из ' & $a - 1 & @TAB & StringLeft ($Percent, 4) & ' %' & @CRLF & "Прошло: " & $time & @TAB & "Осталось: " & $elaps)
			Next
			
		$dif = TimerDiff($begin)
		_TicksToTime(Int($dif), $Hour, $Mins, $Secs)
		$dif = StringFormat("%02i:%02i:%02i", $Hour, $Mins, $Secs)
		ProgressSet(100, "Готово!" & @CRLF & "Прошло: "  & $dif)
		Sleep (1000)
		ProgressOff()
		GUICtrlSetData($iEdit, $tAllFFF & @CRLF & $sFolderName & @CRLF & $tAlldel & @CRLF, 1)
		EndIf
EndFunc

Func MakeFolder()
	MsgBox(BitOR($MB_YESNO, $MB_SYSTEMMODAL), $tWRNNG, $tCrFld & @CRLF & $sFolderName & "?")
		If $iAnswer = 6 Then
			DirCreate ($sFolderName)
			GUICtrlSetData($iEdit, $tFolder2 & @CRLF & $sFolderName & @CRLF & $tCreated & @CRLF, 1)
		EndIf
EndFunc

Func DeFo()
	$iAnswer = MsgBox(BitOR($MB_YESNO, $MB_SYSTEMMODAL), $tWRNNG, $tDAEFFF & @CRLF & $sFolderName & "?" & @CRLF & $tNote & @CRLF & $tUIFIDW & @CRLF & $tFOSAF)
		If $iAnswer = 6 then
			ShellExecuteWait (@ScriptDir & "\data\defo.bat", "", $sFolderName, "open")
			MsgBox($MB_SYSTEMMODAL, $tMessage, $tAllFFF & @CRLF & $sFolderName & @CRLF & $tAlldel)
			GUICtrlSetData($iEdit, $tAllFFF & @CRLF & $sFolderName & @CRLF & $tAlldel & @CRLF, 1)
		EndIf
EndFunc

Func DeFi()
	$iAnswer = MsgBox(BitOR($MB_YESNO, $MB_SYSTEMMODAL), $tWRNNG, $tDFWS0BFF & @CRLF & $sFolderName & "?" & @CRLF & $tFISAND & @CRLF & @CRLF & $tNote & @CRLF & $tUIFIDW & @CRLF & $tFOTFSOA)
		If $iAnswer = 6 Then
			Local $iFileList1 = _FileListToArray ($sFolderName)
			For $i = 1 to $iFileList1[0]
				$iSize = FileGetSize($sFolderName & '\' & $iFileList1[$i])
				If $iSize = 0 Then FileDelete($sFolderName & '\' & $iFileList1[$i])
			Next
			MsgBox($MB_SYSTEMMODAL, $tMessage, $tAllFFF & @CRLF & $sFolderName & @CRLF & $tAlldel)
			GUICtrlSetData($iEdit, $tAllFFF & @CRLF & $sFolderName & @CRLF & $tAlldel & @CRLF, 1)
		EndIf
EndFunc

Func Output_MSG($iOutputWindow, $iFName = '') ;Исправлено

	If $iInvert = 1 then
		If $iOutputWindow = 1 then
			$iOutputMsg = ($tDone)
		Else
			$iOutputMsg = ($tError)
		EndIf
		$iInvert = 0
	Else
		If $iOutputWindow = 0 then
			$iOutputMsg = ($tDone)
		Else
			$iOutputMsg = ($tError)
		EndIf
	EndIf

		GUICtrlSetData($iEdit, $iOutputMsg & ': ' & $iFName & '!' & @CRLF, 1)
EndFunc

Func _ScriptRestart($iTime)
	$hFile = FileOpen(@TempDir & "\temp.bat", 10)
	FileWriteLine ($hFile, @ScriptFullPath)
	FileClose ($hFile)
	Sleep ($iTime)
		ShellExecute (@TempDir & "\temp.bat", "", $sFolderName, "open", @SW_HIDE)
	Exit
EndFunc

Func AutoSearch()
	$sFileName = FileOpenDialog($tSelectFile, " ", $tAllFile & " (*.*)", 1)
		If @error = 1 Then Return
		
			Local $iArr = [@CRLF & $tWaitList, @CRLF & $tSP_msg1, @CRLF & $tSP_msg2, @CRLF & $tSP_msg3, @CRLF & $tSP_msg4, "'it's not possible to create that file...'", "'...'", "'if you press ENTER a new name will be generated automatically'", "'OLD:'", "'NEW:'", $tSP_msg5, '']
			
			For $i = 0 to UBound($iArr)-1
				GUICtrlSetData($iEdit, $iArr[$i] & @CRLF, 1)
			Next
			
			$iFile = FileOpen(@TempDir & "\bfgunpacker\list.bat", 10)
			FileWriteLine ($iFile, "chcp 65001")
			FileWriteLine ($iFile, "@echo off")
			FileWriteLine ($iFile, "DIR/B/O:N/S """ & @ScriptDir & "\data" & """ > " & @TempDir & "\bfgunpacker\file_list.txt")
			FileClose ($iFile)
			$iOutputWindow = ShellExecuteWait (@TempDir & "\bfgunpacker\list.bat", "", $sFolderName, "open")
			FileDelete (@TempDir & "\bfgunpacker\list.bat")

			$hFile = FileOpen(@TempDir & "\bfgunpacker\search_plugin.bat", 10)
			FileWriteLine ($hFile, "chcp 65001")
			FileWriteLine ($hFile, "echo")
	
			Local $iStringCount = _FileCountLines(@TempDir & "\bfgunpacker\file_list.txt")
			
			ProgressOn($tWaitList, '', "", (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)
			For $a = 1 to $iStringCount
				$iScriptName = FileReadLine (@TempDir & "\bfgunpacker\file_list.txt", $a)
				_PathSplit($iScriptName, $iDrive, $iDir, $iName, $iExp)
					Switch $iExp
						Case ".wcx",".bms"
							DirCreate ($sFolderName & "\" & $iName)
							FileWriteLine ($hFile, @ScriptDir & "\data\quickbms.exe " & $iScriptName & ' "' & $sFileName & '" "' & $sFolderName & "\" & $iName & '"')
					EndSwitch
				$Percent = (100/$iStringCount) * $a
				If Mod($a, 100) = 0 Then ProgressSet ($Percent, $a & '\' & $iStringCount)
			Next
			ProgressOff()
			
			FileWriteLine ($hFile, "Pause")
			FileClose ($hFile)
			
			ShellExecuteWait (@TempDir & "\bfgunpacker\search_plugin.bat", "", $sFolderName, "open")
			FileDelete (@TempDir & "\bfgunpacker\search_plugin.bat")
			FileDelete (@TempDir & "\bfgunpacker\file_list.txt")
			ShellExecuteWait (@ScriptDir & "\data\defo.bat", "", $sFolderName, "open")
EndFunc
 
Func _Endian($Binary)
	$Len = StringLen($Binary)
		;MsgBox (0, '', $Binary)
	If $Len < 6 or Mod($Len, 2) = 1 or StringIsXDigit(StringTrimLeft($Binary, 2)) = 0 Then
		MsgBox (0, '', $Binary & " не является 16-ричным числом!")
		Return
	EndIf
	
	$BinaryArray = StringRegExp($Binary, '\N\N', 3)
	$a = UBound($BinaryArray) - 1
	$txt = FileOpen (@TempDir & '\bindata.txt', 10)
	
		For $i = $a to 1 Step -1
			FileWrite ($txt, $BinaryArray[$i])
		Next
	FileClose ($txt)
	Return ('0x' & FileReadLine (@TempDir & '\bindata.txt', 1))
EndFunc
 
