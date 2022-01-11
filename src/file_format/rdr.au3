
Func RDR_STRTLB()
	GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)
		If GUICtrlRead($iReimport_Checkbox) = 1 Then
			RDR_STRTLB_Import()
		Else
			RDR_STRTLB_Export()
		EndIf
EndFunc

Func RDR_STRTLB_Export()
;Function uses resource from https://zenhax.com/viewtopic.php?f=12&t=7073&hilit=Red+Dead+Redemption
$Path = FileOpenDialog("Select the STRTLB file", @ScriptDir, "strtbl files (*.strtbl)",1)
If @error <> 1 Then
	$File = fileopen($Path,16)
	$Langs = FileRead($File,4)
	Dim $Offsets[$Langs]
		For $i = 1 to $Langs
			$Offsets[$i-1] = FileRead($File,4)
		Next
		For $i = 1 to $Langs
			$Text = ""
			FileSetPos($File,$Offsets[$i-1],0)
			$Files = FileRead($File,4)
				For $f = 1 to $Files
					FileRead($File,10)
					$Str = StringTrimRight(BinaryToString(FileRead($File,_BinaryToInt32(FileRead($File,4))*2),2),1)
					$Str = StringRegExpReplace($Str,@CRLF,"<cf>")
					$Str = StringRegExpReplace($Str,@LF,"<lf>")
					$Str = StringRegExpReplace($Str,@CR,"<cr>")
					$Text &= $Str & @CRLF
					FileRead($File,10)
				Next
			$hFile = FileOpen($i&".txt", 2+32)
			FileWrite($hFile, $Text)
			FileClose($hFile)
		Next
	TrayTip("Exporter", "Finish!", 3)
	sleep(3000)
EndIf
EndFunc

Func RDR_STRTLB_Import()
;Function uses resource from https://zenhax.com/viewtopic.php?f=12&t=7073&hilit=Red+Dead+Redemption
Dim $NEWdata
$TxtPath = FileOpenDialog("Select the TXT file", @ScriptDir, "text files (*.txt)",1)
_PathSplit($TxtPath, $iDrive, $iDir, $iName, $iExp)
If @error <> 1 Then
_FileReadToArray($TxtPath,$NEWdata)
$Path = FileOpenDialog("Select the STRTLB file", @ScriptDir, "strtbl files (*.strtbl)",1)
If @error <> 1 Then
$Name = StringTrimRight($iName,4)
$File = FileOpen($Path, 0+16)
If $File = -1 Then
MsgBox(0,"Error","Can't open "&$Name&" file.")
Exit
EndIf
$Langs = FileRead($File,4)
Dim $Offsets[$Langs]
For $i = 1 to $Langs
	$Offsets[$i-1] = FileRead($File,4)
Next
FileSetPos($File,$Offsets[$Name-1],0)
$Files = FileRead($File,4)
$Newfiletext = $Files
For $i = 1 to $Files
	$Newfiletext &= FileRead($File,10)
	FileRead($File,_BinaryToInt32(FileRead($File,4))*2)
	$NEWdata[$i] = StringReplace($NEWdata[$i],"<cf>",@CRLF)
	$NEWdata[$i] = StringReplace($NEWdata[$i],"<lf>",@LF)
	$NEWdata[$i] = StringReplace($NEWdata[$i],"<cr>",@CR)
	$NewText = StringToBinary($NEWdata[$i],2) & Binary("0x0000")
	$Newfiletext &= _BinaryFromInt32(BinaryLen($NewText)/2) & $NewText & FileRead($File,10)
Next
If $Name = $Langs Then
	$Offset = FileGetSize($Path)
Else
	$Offset = _BinaryToInt32($Offsets[$Name])
EndIf
$Diff = BinaryLen($Newfiletext) - ($Offset - _BinaryToInt32($Offsets[$Name-1]))
$Newfile = $Langs
For $i = 1 to $Langs
	If $i > $Name Then
		$Offsets[$i-1] = _BinaryToInt32($Offsets[$i-1]) + $Diff
		$Newfile &= _BinaryFromInt32($Offsets[$i-1])
	Else
		$Newfile &= $Offsets[$i-1]
	EndIf
Next
FileSetPos($File,_BinaryToInt32($Langs)*4+4,0)
$Newfile &= FileRead($File,_BinaryToInt32($Offsets[$Name-1]) - (_BinaryToInt32($Langs)*4+4)) & $Newfiletext
FileSetPos($File,$Offset,0)
$Newfile &= FileRead($File)
$hNewfile = FileOpen("NEW_"& $iName, 2+16)
FileWrite($hNewfile, $Newfile)
FileClose($hNewfile)
TrayTip("Importer", "Finish!", 3)
sleep(3000)
EndIf
EndIf
EndFunc