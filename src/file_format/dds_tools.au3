
Func DDSSaving($dwHeight, $dwWidth, $iMediaFile_dds, $iOffset, $DDSOpenFile)
	$DDSOpen = FileOpen ($DDSOpenFile, 16)
	_PathSplit ($DDSOpenFile, $iDrive, $iDir, $iName, $iExp)
	FileSetPos ($DDSOpen, $iOffset, 0)
	$iDDS_Data = FileRead ($DDSOpen)
	$iNewDDS = FileOpen ($sFolderName & "\" & $iName & ".dds", 2+8+16)
	FileWrite ($iNewDDS, "0x444453207C00000007100A00") 
	FileWrite ($iNewDDS, _Endian(Hex($dwHeight)))
	FileWrite ($iNewDDS, "0x00") 
	FileWrite ($iNewDDS, _Endian(Hex($dwWidth)))
	FileWrite ($iNewDDS, "0x0070550500010000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000004000000") 
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