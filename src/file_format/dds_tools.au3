
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
	$sFilePath = FileSelectFolder("", "")
	If FileExists ($sFilePath & "\1.dds") and FileExists ($sFilePath & "\2.dds") and FileExists ($sFilePath & "\3.dds") and FileExists ($sFilePath & "\4.dds") and FileExists ($sFilePath & "\5.dds") and FileExists ($sFilePath & "\6.dds") then
		$hFile = FileOpen($sFilePath & "\1.dds", 16)
		$hOutFile = FileOpen($sFolderName & "\out.dds", 25)
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
	Else
		$tCBMSG = (@CRLF & "CubeMap Creator" & @CRLF & @CRLF & $tCBMSG1 & @CRLF & $tCBMSG2 & @CRLF & $tCBMSG3 & @CRLF & $tCBMSG4 & @CRLF & $tCBMSG5 & @CRLF & $tCBMSG6 & @CRLF & $tCBMSG7 & @CRLF & $tCBMSG8)
		MsgBox($MB_SYSTEMMODAL, $tUsing, $tCBMSG)
		GUICtrlSetData($iEdit, $tCBMSG, 1)
	EndIf
EndFunc

Func MorUnpacker()
	$sFileName = FileOpenDialog ('', " ", "Pathologic Files (*.vfs)|All Files (*.*)", 1+4)
		If @error = 1 then Return
	
		$iFileList = StringSplit ($sFileName, '|')
		Local $a = UBound($iFileList) - 1, $fc = 2
		If $a = 1 Then $fc = 1
		GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)	
			For $j = $fc to $a
				If $iFileList[0] > 1 Then $sFileName = $iFileList[1] & '\' & $iFileList[$j]
				_PathSplit ($sFileName, $iDrive, $iDir, $iName, $iExp)
				$iFile = FileOpen($sFileName, 16)
				FileSetPos ($iFile, 8, 0)
				
				$iFileC = _BinaryToInt32(FileRead($iFile, 4))
			
				ProgressOn('', $tWtSaving, '', (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)
					For $i = 1 to $iFileC
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
						ProgressSet((100/$iFileC) * $i, $tSave & @TAB & $iNameFile & @CRLF & $i & "/" & $iFileC)
					Next
				ProgressSet(100, $tDone)
				GUICtrlSetData($iEdit, $tDone & @CRLF, 1)
				ProgressOff()	
			Next
EndFunc