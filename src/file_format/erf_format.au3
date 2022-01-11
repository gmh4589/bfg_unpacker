Func ERFUnpacker($sFileName = '')
	If GUICtrlRead($iHideOrShow) = 0 Then
		Sleep(1) ;TODO: доделать функцию упаковки
	Else
		Switch $sFileName		
			Case '', ' ', '	', "", " ", "	"
				$sFileName = FileOpenDialog ($tSelectFile, " ", 'Aurora Engine ERF Files (*.erf)|' & $tAllFile & " (*.*)", 1+4)
					If @error = 1 then Return
		EndSwitch
		$iFile = FileOpen($sFileName, 16)
		FileSetPos ($iFile, 4, 0)
		$iVer = FileRead($iFile, 4)
			If $iVer = '0x56312E30' Then
				;MsgBox($MB_SYSTEMMODAL, $tMessage, "v1")
					FileSetPos ($iFile, 16, 0)
						$iFileCount = FileRead ($iFile, 4)
						$iFileCount = Dec(StringTrimLeft (_Endian($iFileCount), 2))
					FileSetPos ($iFile, 24, 0)
						$iOff2Lst = FileRead ($iFile, 4)
						$iOff2Lst = Dec(StringTrimLeft (_Endian($iOff2Lst), 2))
					FileSetPos ($iFile, 28, 0)
						$iERFLst = FileRead ($iFile, 4)
						$iERFLst = Dec(StringTrimLeft (_Endian($iERFLst), 2))
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
					ProgressOn('', $tWtSaving, '', (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)
						For $j = 1 to $iFileCount
							$data1 = FileRead ($iFile, 4)
								$data1 = Dec(StringTrimLeft (_Endian($data1), 2))
							$data2 = FileRead ($iFile, 4)
								$data2 = Dec(StringTrimLeft (_Endian($data2), 2))
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
							ProgressSet((100/$iFileCount) * $j, $tSave & @TAB & $fName & @CRLF & $j & "/" & $iFileCount)
						Next
					ProgressSet(100, $tDone)
					GUICtrlSetData($iEdit, $tDone & @CRLF, 1)
					ProgressOff()
					FileClose ($iFile)
			Else
				FileSetPos($iFile, 8, 0)
				$iVer = FileRead($iFile, 4)
					If $iVer = '0x56003200' Then
						;MsgBox($MB_SYSTEMMODAL, $tMessage, "v2")
							FileSetPos ($iFile, 16, 0)
								$iFileCount = FileRead ($iFile, 4)
								$iFileCount = Dec(StringTrimLeft (_Endian($iFileCount), 2))
							FileSetPos ($iFile, 32, 0)
						ProgressOn('', $tWtSaving, '', (@DesktopWidth/2)-150, (@DesktopHeight/2)-62, 18)
							For $i = 0 to $iFileCount
								$RName = FileRead ($iFile, 64)
								$iOffs = FileRead ($iFile, 4)
									$iOffs = Dec(StringTrimLeft (_Endian($iOffs), 2))
								$iLong = FileRead ($iFile, 4)
									$iLong = Dec(StringTrimLeft (_Endian($iLong), 2))
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
								ProgressSet((100/$iFileCount) * $i, $tSave & @TAB & $fName & @CRLF & $i & "/" & $iFileCount)								
							Next
						ProgressSet(100, $tDone)
						GUICtrlSetData($iEdit, $tDone & @CRLF, 1)
						ProgressOff()						
						Return
					ElseIf $iVer = '0x56003300' Then
						MsgBox($MB_SYSTEMMODAL, $tMessage, "v3")
						FileClose ($iFile)
						_QuickBMSRun('', @ScriptDir & "\data\scripts\dragon_age__2.bms ", $sFileName)
					Else
						MsgBox($MB_SYSTEMMODAL, $tMessage, $tNoGame & "Aurora Engine")
						
					EndIf
			EndIf

	EndIf
EndFunc
