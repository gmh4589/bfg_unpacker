
Func _fileReaper($iFunc, $iExt = '', $sFileName = '', $iPar1 = '')
    Local $fDrive, $fDir, $fName, $fExp
    $sFileName = _getFile($sFileName, $iExt)
    If @error = 1 Then Return
    $iFileList = StringSplit($sFileName, '|')
    Local $a = UBound($iFileList) - 1, $fc = 2
    If $a = 1 Then $fc = 1
    GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)

    For $j = $fc To $a
        $sCurrentFileName = $iFileList[$j]
        _PathSplit($sCurrentFileName, $fDrive, $fDir, $fName, $fExp)
        $pth = GUICtrlRead($iSubFolder_Checkbox) = 1 ? $sFolderName & '\' & $fName : $sFolderName
        If Not FileExists($pth) Then DirCreate($pth)

        If IsArray($iPar1) Then
            If $iPar1[4] Then
                FileCopy($sCurrentFileName, $sFolderName & '\')
                $sCurrentFileName = $sFolderName & '\' & $fName & $fExp
            EndIf

            GUICtrlSetData($iEdit, @CRLF & $sCurrentFileName & @CRLF, 1)
            GUICtrlSetData($iEdit, @CRLF & "ТЕСТ 1" & @CRLF, 1)
            _Console(@ScriptDir & '\' & $iPar1[0], " " & $iPar1[1] & ' "' & $sCurrentFileName & '" ' & $iPar1[2], $sFolderName, $sCurrentFileName)

            If $iPar1[4] Then FileDelete($sFolderName & '\' & $fName & $fExp)

        ElseIf $iPar1 <> '' Then
            GUICtrlSetData($iEdit, @CRLF & $sCurrentFileName & @CRLF, 1)
            GUICtrlSetData($iEdit, @CRLF & "ТЕСТ 2" & @CRLF, 1)
            _Console(@ScriptDir & "\data\quickbms.exe ", $rI & $iPar1 & ' "' & $sCurrentFileName & '" "' & $pth & '"', $iDrive & $iDir, $sCurrentFileName)

        ElseIf $iPar1 = '' Then
            $iFunc($sCurrentFileName)
        EndIf
    Next
EndFunc
