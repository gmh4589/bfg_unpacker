
Func OOAM_Unpacker() ;Исправлено
	If GUICtrlRead($iReimport_Checkbox) = 1 Then  
		OGG_Packer()
	Else
		OGG_Unpacker()
	EndIf
EndFunc

Func OGG_Unpacker() ;TODO: TEXT!!!
	$iFilePath = FileOpenDialog($tSelectFile, " ", "Of Orcs and Men files (*.spk; *.pgz; *_*)|" & $tAllFile & " (*.*)", 1+4)
		If @error = 1 then Return
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

Func OGG_Packer() ;TODO: TEXT!!!
	$iFilePath = FileOpenDialog($tSelectFile, " ", "OGG Audio Files (*.ogg)|" & $tAllFile & " (*.*)", 1+4)
		If @error = 1 then Return
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
				GUICtrlSetData($iEdit2, "Выполнено!" & @CRLF & "Файл " & $iName & " сохранен!" & @CRLF, 1)
			Else
				GUICtrlSetData ($iEdit2, 'Ошибка! Отсутствует файл ' & $iName & ".lip!" & @CRLF, 1)
			EndIf
		Else
			GUICtrlSetData ($iEdit2, 'Ошибка! Файл ' & $iName & $iExp & ' не является OGG Vorbis файлом!' & @CRLF, 1)
		EndIf
	FileClose ($iOGGFile)
EndFunc

