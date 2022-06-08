
Func _fileReaper($iFunc, $iExt = '', $sFileName = '', $iPar1 = '')
	$sFileName = _getFile($sFileName, $iExt)
		If @error = 1 then Return
	
		$iFileList = StringSplit ($sFileName, '|')
		Local $a = UBound($iFileList) - 1, $fc = 2
		If $a = 1 Then $fc = 1
		GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)	
			For $j = $fc to $a
				If $iFileList[0] > 1 Then $sFileName = $iFileList[1] & '\' & $iFileList[$j]
				If IsArray($iPar1) Then
					_PathSplit($sFileName, $iDrive, $iDir, $iName, $iExp)
					If $iPar1[4] Then
						FileCopy($sFileName, $sFolderName & '\')
						$sFileName = $sFolderName & '\' & $iName & $iExp
					EndIf
					_Console (@ScriptDir & "\data\" & $iPar1[0], " " & $iPar1[1] & ' "' & $sFileName & '" ' & $iPar1[2], $iPar1[3], $sFileName)
					If $iPar1[4] Then FileDelete($sFolderName & '\' & $iName & $iExp)
				ElseIf $iPar1 <> '' Then
					_PathSplit($iPar1, $iDrive, $iDir, $iName, $iExp)
					; _Console(@ScriptDir & "\data\quickbms.exe ", $rI & $iPar1 & ' "' & $sFileName & '" "' & $sFolderName & '"', $iDrive & $iDir, $sFileName)
					$size = FileGetSize($sFileName)
					$iOutputWindow = Run(@ScriptDir & "\data\quickbms.exe " & $rI & ' -K ' & $iPar1 & ' "' & $sFileName & '" "' & $sFolderName & '"', $iDrive & $iDir, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
					_EnginePB($iOutputWindow, '', 110, $size)
				ElseIf $iPar1 = '' Then
					$iFunc($sFileName)
				EndIf
			Next
EndFunc

Func _getFile($sFileName, $iExtList = '')
	Switch $sFileName
		Case '', ' ', '	', "", " ", "	"
			$sFileName = FileOpenDialog($tSelectFile, " ", $iExtList & $tAllFile & " (*.*)", 1+4)
				If @error = 1 then SetError(1)
		Case 'folder'
			$sFileName = FileSelectFolder ('', $iLastDir)
				If @error = 1 then SetError(1)
		Case Else
			$sFileName = $sFileName
	EndSwitch
	Return($sFileName)
EndFunc

Func DDSSaving($dwHeight, $dwWidth, $iMediaFile_dds, $iOffset, $DDSOpenFile)
	$DDSOpen = FileOpen ($DDSOpenFile, 16)
	_PathSplit ($DDSOpenFile, $iDrive, $iDir, $iName, $iExp)
	FileSetPos ($DDSOpen, $iOffset, 0)
	$iDDS_Data = FileRead ($DDSOpen)
	$iNewDDS = FileOpen ($sFolderName & "\" & $iName & ".dds", 2+8+16)
	FileWrite ($iNewDDS, "0x444453207C00000007100A00") 
	FileWrite ($iNewDDS, _BinaryFromInt32($dwHeight))
	FileWrite ($iNewDDS, _BinaryFromInt32($dwWidth))
	FileWrite ($iNewDDS, "0x70550500010000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000004000000") 
	FileWrite ($iNewDDS, $iMediaFile_dds)
	FileWrite ($iNewDDS, "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000") 
	FileWrite ($iNewDDS, $iDDS_Data)
EndFunc

Func CubeMapCreator()
	$sFilePath = _getFile('folder')
		If @error Then Return
	
	$tCBMSG = (@CRLF & "CubeMap Creator" & @CRLF & @CRLF & $tCBMSG1 & @CRLF & $tCBMSG2 & @CRLF & $tCBMSG3 & @CRLF & $tCBMSG4 & @CRLF & $tCBMSG5 & @CRLF & $tCBMSG6 & @CRLF & $tCBMSG7 & @CRLF & $tCBMSG8)
	For $i = 1 to 6
		If Not FileExists ($sFilePath & "\" & $i & ".dds") Then BitAND(_MsgBox(0, $tUsing, $tCBMSG), GUICtrlSetData($iEdit, $tCBMSG, 1), SetError(1))
		If @error Then Return
	Next

	_PathSplit ($sFilePath, $iDrive, $iDir, $iName, $iExp)
	$hFile = FileOpen($sFilePath & "\1.dds", 16)
	$hOutFile = FileOpen($sFolderName & "\" & $iName & ".dds", 25)
	$hText = FileRead($hFile, 112)
	FileWrite($hOutFile, $hText)
	FileWrite($hOutFile, "0x00FE0000000000000000000000000000")
	FileClose($hFile)
		For $a = 1 to 6
			$hFile = FileOpen($sFilePath & "\" & $a & ".dds", 16)
			FileSetPos ($hFile, 128, 0)
			$sSourceCode = FileRead($hFile)
			FileWrite($hOutFile, $sSourceCode)
			FileClose($hFile)
		Next
	GUICtrlSetData($iEdit, $tDone & @CRLF, 1)
	FileClose($hOutFile)
EndFunc

Func _mp3($sFileName)
	_PathSplit ($sFileName, $iDrive, $iDir, $iName, $iExp)
	$iFile = FileOpen($sFileName, 16)
	$data = FileRead($iFile)
	$iNewFile = FileOpen($sFolderName & '\' & $iName & '.mp3', 26)
	FileWrite ($iNewFile, "0x544147756E6B6E6F776E0000000000000000000000000000000000000000000000000000000000000000000000000000000000756E6B6E6F776E0000000000000000000000000000000000000000000000000000000000000000000000000000000000756E6B6E6F776E00000000000000000000000000000000000000000000000000000000000000000000000000000000003232303332303232756E6B6E6F776E00000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
	FileWrite ($iNewFile, $data)
	FileClose ($iFile)
	FileClose ($iNewFile)
	GUICtrlSetData($iEdit, $tDone & ' ' & $sFileName & @CRLF, 1)
EndFunc

Func MorUnpacker($sFileName)
	_PathSplit ($sFileName, $iDrive, $iDir, $iName, $iExp)
	$iFile = FileOpen($sFileName, 16)
	FileSetPos ($iFile, 8, 0)

	$iFileC = _BinaryToInt32(FileRead($iFile, 4))

		For $i = 1 to $iFileC
			If GUIGetMsg($progressGUI) = $exitBTN Then ExitLoop
			$iNameLong = FileRead($iFile, 1)
			$iNameFile = BinaryToString(FileRead($iFile, $iNameLong))
			$iPos = FileGetPos ($iFile)
			$iFileSize = _BinaryToInt32(FileRead($iFile, 4))
			$iFileOffset = _BinaryToInt32(FileRead($iFile, 4))
			FileSetPos ($iFile, $iFileOffset, 0)
			$iData = FileRead($iFile, $iFileSize)
			$iNewFile = FileOpen($sFolderName & '\' & $iName & '\' & $iNameFile, 26)
			FileWrite ($iNewFile, $iData)
			FileClose ($iNewFile)
			FileSetPos ($iFile, $iPos + 16, 0)
			GUICtrlSetData($iEdit,  $tSave & ' ' & $i & "/" & $iFileC & ' ' & $iNameFile  & @CRLF, 1)
			If Mod($i, 10) = 0 Then _BarCreate((100/$iFileC) * $i, $tWtSaving, $tSave & @CRLF & $iNameFile & @CRLF & $i & "/" & $iFileC, 300, 120, 45, True)
		Next
	GUICtrlSetData($iEdit, $tDone & @CRLF, 1)
	_BarOff()
EndFunc

Func OOAM_Unpacker() ;Исправлено
	If GUICtrlRead($iReimport_Checkbox) = 1 Then  
		_fileReaper(OGG_Packer, "OGG Audio Files (*.ogg)|")
	Else
		_fileReaper(OGG_Unpacker, "Of Orcs and Men files (*.spk; *.pgz; *_*)|")
	EndIf
EndFunc

Func OGG_Unpacker($iFilePath) ;TODO: TEXT!!!
	_PathSplit($iFilePath, $iDrive, $iDir, $iName, $iExp)
		If $iExp = '' Then
			$iFile = FileOpen ($iFilePath, 16)
			FileSetPos ($iFile, 858+StringLen ($iName), 0)
			$iOffset = FileRead ($iFile, 4)
			$iFileSize = Dec (StringTrimLeft ($iOffset, 2))
			FileSetPos ($iFile, 866+StringLen ($iName), 0)
			$iOGGSource = FileRead ($iFile, $iFileSize)
			$iOGGFile = FileOpen ($sFolderName & '\' & $iName & '.ogg', 26)
			FileWrite ($iOGGFile, $iOGGSource)
			FileClose ($iOGGFile)
			FileSetPos ($iFile, 866+StringLen ($iName)+$iFileSize, 0)
			$iLIPSource = FileRead ($iFile)
			$iLIPFile = FileOpen ($sFolderName & '\' & $iName & '.lip', 26)
			FileWrite ($iLIPFile, $iLIPSource)
			FileClose ($iLIPFile)
			FileClose ($iFile)
			GUICtrlSetData($iEdit, "Выполнено!" & @CRLF & "Файл " & $iName & ".lip" & " сохранен!" & @CRLF, 1)
			GUICtrlSetData($iEdit, "Выполнено!" & @CRLF & "Файл " & $iName & ".ogg" & " сохранен!" & @CRLF, 1)
		ElseIf $iExp = BitOR('.spk', '.pzg') Then
			_OtherPRG('', '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $iFilePath)
		Else
			GUICtrlSetData ($iEdit, 'Ошибка! Файл ' & $iName & $iExp & ' не является аудио архивом из игры "Of orc and human"!' & @CRLF, 1)
		EndIf
EndFunc

Func OGG_Packer($iFilePath) ;TODO: TEXT!!!
	_PathSplit($iFilePath, $iDrive, $iDir, $iName, $iExp)
	$iOGGFile = FileOpen ($iFilePath, 16)
	$iFileHead = FileRead ($iOGGFile, 4)
		If $iFileHead = ('0x4F676753') Then
			If FileExists ($iDrive & $iDir & $iName & ".lip") Then
				$iNewFile = FileOpen ($sFolderName & '\' & $iName, 26)
				$iLIPFile = FileOpen ($iDrive & $iDir & $iName & ".lip", 16)
				$iOGGSize = FileGetSize ($iFilePath)
				$iLIPSize = FileGetSize ($iDrive & $iDir & $iName & ".lip")
				$iNameLong = StringLen ($iName)
				$ArchiveSize = ($iOGGSize+$iLIPSize+858+$iNameLong)
				FileWrite ($iNewFile, "0x50535347")
				FileWrite ($iNewFile, "0x" & StringTrimleft (Hex ($ArchiveSize), 8))
				FileWrite ($iNewFile,  "0x000000110000000B0000000100000009415544494F4441544100000002000000010000000C62696E6172794F626A526566000000020000000B6D61726B6572436F756E7400000002000000074F4747444154410000000000000003000000114C495053594E435F414E494D4154494F4E0000000000000004000000114C495053594E435F44415441424C4F434B000000040000000300000005776964746800000004000000066C656E6774680000000500000009737461727454696D650000000600000007656E6454696D6500000005000000174C495053594E435F44415441424C4F434B5F56414C554500000000000000060000000C50535347444154414241534500000005000000070000000D73706964657256657273696F6E000000080000001173706964657246696C6556657273696F6E00000009000000157370696465724C61796572656444617461626173650000000A000000057363616C650000000B00000002757000000007000000074C494252415259000000010000000C0000000474797065000000080000000854595045494E464F000000020000000D00000008747970654E616D650000000E0000000974797065436F756E740000000900000003585858000000010000000F0000000269640000000A0000000C42494E4152594F424A45435400000001000000100000000E62696E6172794461746153697A650000000B0000000A42494E415259444154410000000000000006")
				FileWrite ($iNewFile, "0x" & StringTrimleft (Hex ($ArchiveSize-546), 8))
				FileWrite ($iNewFile,  "0x0000004C0000000700000004000000000000000800000004000000000000000900000004000000000000000A0000000C3F8000003F8000003F8000000000000B0000000C000000003F800000000000000000000800000028000000240000000D000000100000000C42494E4152594F424A4543540000000E0000000400000001000000080000002D000000290000000D00000015000000114C495053594E435F414E494D4154494F4E0000000E000000040000000100000008000000230000001F0000000D0000000B000000074F4747444154410000000E000000040000000100000007")
				FileWrite ($iNewFile, "0x" & StringTrimleft (Hex ($iOGGSize+$iNameLong+76), 8))
				FileWrite ($iNewFile, "0x000000180000000C000000100000000C42494E4152594F424A4543540000000A")
				FileWrite ($iNewFile, "0x" & StringTrimleft (Hex ($iOGGSize+$iNameLong+40), 8))
				FileWrite ($iNewFile, "0x" & Hex ($iNameLong+28))
				FileWrite ($iNewFile, "0x0000001000000004")
				FileWrite ($iNewFile, "0x" & StringTrimleft (Hex ($iOGGSize-4), 8))
				FileWrite ($iNewFile, "0x0000000F")
				FileWrite ($iNewFile, "0x" & Hex ($iNameLong+8))
				FileWrite ($iNewFile, "0x" & Hex ($iNameLong+4))
				FileWrite ($iNewFile, $iName)
				FileWrite ($iNewFile, "0x2E6F67670000000B")
				FileWrite ($iNewFile, "0x" & StringTrimleft (Hex ($iOGGSize), 8))
				FileWrite ($iNewFile, "0x00000000")
				FileSetPos ($iOGGFile, 0, 0)
				$iOGGData = FileRead ($iOGGFile)
				FileWrite ($iNewFile, $iOGGData)
				FileSetPos ($iLIPFile, 0, 0)
				$iLIPData = FileRead ($iLIPFile)
				FileWrite ($iNewFile, $iLIPData)
				FileClose ($iNewFile)
				FileClose ($iLIPFile)
				ShellExecuteWait (@ScriptDir & "\data\gzip.exe", ' -1 ' & $sFolderName & '\' & $iName, '', "open", @SW_HIDE)
				FileMove ($sFolderName & '\' & $iName & '.gz', $sFolderName & '\' & $iName & '.pgz')
				GUICtrlSetData($iEdit, "Выполнено!" & @CRLF & "Файл " & $iName & ".pgz сохранен!" & @CRLF, 1)
			Else
				GUICtrlSetData ($iEdit, 'Ошибка! Отсутствует файл ' & $iName & ".lip!" & @CRLF, 1)
			EndIf
		Else
			GUICtrlSetData ($iEdit, 'Ошибка! Файл ' & $iName & $iExp & ' не является OGG Vorbis файлом!' & @CRLF, 1)
		EndIf
	FileClose ($iOGGFile)
EndFunc

Func ERFUnpacker($sFileName = '')
	If GUICtrlRead($iHideOrShow) = 0 Then
		Sleep(1) ;TODO: доделать функцию упаковки
	Else
		$iFile = FileOpen($sFileName, 16)
		FileSetPos ($iFile, 4, 0)
		$iVer = FileRead($iFile, 4)
			If $iVer = '0x56312E30' Then
				;MsgBox($MB_SYSTEMMODAL, $tMessage, "v1")
					FileSetPos ($iFile, 16, 0)
						$iFileCount = FileRead ($iFile, 4)
						$iFileCount = _BinaryToInt32($iFileCount) - 1
					FileSetPos ($iFile, 24, 0)
						$iOff2Lst = FileRead ($iFile, 4)
						$iOff2Lst = _BinaryToInt32($iOff2Lst)
					FileSetPos ($iFile, 28, 0)
						$iERFLst = FileRead ($iFile, 4)
						$iERFLst = _BinaryToInt32($iERFLst)
					FileSetPos ($iFile, $iOff2Lst, 0)
					Local $FileNameArray[0], $FileExtArray[0]
						For $i = 0 to $iFileCount
							$RName = FileRead ($iFile, 16)
							_ArrayAdd($FileNameArray, $RName)
							FileSetPos ($iFile, 4, 1)
							$fEXT = FileRead ($iFile, 4)
							If $fEXT = '0xBF0B0000' Then
								$fEXT = '.dds'
							Else
								$fEXT = '.dat'
							EndIf
							_ArrayAdd($FileExtArray, $fEXT)
						Next
					FileSetPos ($iFile, $iERFLst, 0)
					
						For $j = 1 to $iFileCount
							If GUIGetMsg($progressGUI) = $exitBTN Then ExitLoop
							$data1 = FileRead ($iFile, 4)
								$data1 = _BinaryToInt32($data1)
							$data2 = FileRead ($iFile, 4)
								$data2 = _BinaryToInt32($data2)
							$c = FileGetPos($iFile)
							FileSetPos ($iFile, $data1, 0)
							$Data = FileRead ($iFile, $data2)
							$RName = StringReplace($FileNameArray[$j], '00', '')
							$fName = BinaryToString($RName) & $FileExtArray[$j]
							$iNewFile = FileOpen ($sFolderName & '\' & $fName, 26)
							FileWrite ($iNewFile, $Data)
							FileClose ($iNewFile)
							FileSetPos ($iFile, $c, 0)
							GUICtrlSetData($iEdit,  $tSave & ' ' & $j & "/" & $iFileCount & ' ' & $fName  & @CRLF, 1)
							If Mod($j, 10) = 0 Then _BarCreate((100/$iFileCount) * $j, $tWtSaving, $tSave & @TAB & $fName & @CRLF & $j & "/" & $iFileCount, 300, 110, 45, True)
						Next
					ProgressSet(100, $tDone)
					GUICtrlSetData($iEdit, $tDone & @CRLF, 1)
					_BarOff()
					FileClose ($iFile)
			Else
				FileSetPos($iFile, 8, 0)
				$iVer = FileRead($iFile, 4)
					If $iVer = '0x56003200' Then
						;MsgBox($MB_SYSTEMMODAL, $tMessage, "v2")
							FileSetPos ($iFile, 16, 0)
								$iFileCount = FileRead ($iFile, 4)
								$iFileCount = _BinaryToInt32($iFileCount) - 1
							FileSetPos ($iFile, 32, 0)
							For $i = 0 to $iFileCount
								If GUIGetMsg($progressGUI) = $exitBTN Then ExitLoop
								$RName = FileRead ($iFile, 64)
								$iOffs = FileRead ($iFile, 4)
									$iOffs = _BinaryToInt32($iOffs)
								$iLong = FileRead ($iFile, 4)
									$iLong = _BinaryToInt32($iLong)
								$c = FileGetPos($iFile)
								FileSetPos ($iFile, $iOffs, 0)
								$Data = FileRead ($iFile, $iLong)
								$RName = StringReplace($RName, '00', '')
								$fName = BinaryToString($RName)
								$iNewFile = FileOpen ($sFolderName & '\' & $fName, 26)
								FileWrite ($iNewFile, $Data)
								FileClose ($iNewFile)
								FileSetPos ($iFile, $c, 0)
								GUICtrlSetData($iEdit,  $tSave & ' ' & $i & "/" & $iFileCount & ' ' & $fName  & @CRLF, 1)
								If Mod($i, 10) = 0 Then _BarCreate((100/$iFileCount) * $i, $tWtSaving, $tSave & @TAB & $fName & @CRLF & $i & "/" & $iFileCount, 300, 110, 45, True)
							Next
						ProgressSet(100, $tDone)
						GUICtrlSetData($iEdit, $tDone & @CRLF, 1)
						_BarOff()						
						Return
					ElseIf $iVer = '0x56003300' Then
						;MsgBox($MB_SYSTEMMODAL, $tMessage, "v3")
						FileClose ($iFile)
						_QuickBMSRun('', @ScriptDir & "\data\scripts\dragon_age__2.bms ", $sFileName)
					Else
						_MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoGame & "Aurora Engine")
						
					EndIf
			EndIf
	EndIf
EndFunc
