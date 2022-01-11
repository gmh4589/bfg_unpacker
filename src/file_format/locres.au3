
Func Unreal4LR($sFileName)
	If GUICtrlRead($iReimport_Checkbox) = 1 Then
		LocresImport($sFileName)
	Else
		LocresExport($sFileName)
	EndIf
EndFunc

Func LocresImport($TxtPath)
Dim $NewData, $j=0

_PathSplit ($TxtPath, $iDrive, $iDir, $iName, $iExp)
_FileReadToArray($TxtPath,$NewData)

$File = FileOpen($iName,0+16)

If $File = -1 Then
	MsgBox(0,"Error","Can't open " & $iName & " file. Need to work nearby with him!")
	Return
EndIf

$hNewfile = FileOpen("NEW_"&$iName, 2+16)
$Files = FileRead($File,4)

If $Files = "0x0E147475" Then
	FileSetPos($File,16,0)
	$Byte = FileRead($File,1)
	$Size = FileRead($File,8)
	FileSetPos($File,0,0)
	$NewFile = FileRead($File,$Size)
	$Files = FileRead($File,4)
	$NewFile &= $Files
	FileWrite($hNewfile, $Newfile)
	For $i = 1 to $Files
		$NEWdata[$i] = StringReplace($NEWdata[$i],"<cf>",@CRLF)
		$NEWdata[$i] = StringReplace($NEWdata[$i],"<lf>",@LF)
		$NEWdata[$i] = StringReplace($NEWdata[$i],"<cr>",@CR)
		$Size = _BinaryToInt32(FileRead($File,4))
		If $Size < 0 Then
			$Size = -$Size*2
			FileRead($File,$Size)
		Else
			FileRead($File,$Size)
		EndIf
		If StringIsASCII($NEWdata[$i]) <> 1 Then
			$NewText = StringToBinary($NEWdata[$i],2) & Binary("0x0000")
			$Newfile = _BinaryFromInt32(-int(BinaryLen($NewText)/2)) & $NewText
		Else
			$NewText = StringToBinary($NEWdata[$i],1) & Binary("0x00")
			$Newfile = _BinaryFromInt32(int(BinaryLen($NewText))) & $NewText
		Endif
		If $Byte = 2 Then $Newfile &= FileRead($File,4)
		FileWrite($hNewfile, $Newfile)
	Next
Else
	$Newfile = $Files
	FileWrite($hNewfile, $Newfile)
	for $i = 1 to $Files
		$Size = FileRead($File,4)
		$Newfile = $Size
		$Size = _BinaryToInt32($Size)
		If $Size < 0 Then
			$Size = -$Size*2
			$Newfile &= FileRead($File,$Size)
		Else
			$Newfile &= FileRead($File,$Size)
		EndIf
		$Ent = FileRead($File,4)
		$Newfile &= $Ent
		FileWrite($hNewfile, $Newfile)
		For $e = 1 to $Ent
			$Size = FileRead($File,4)
			$Newfile = $Size
			$Size = _BinaryToInt32($Size)
			If $Size < 0 Then
				$Size = -$Size*2
				$Newfile &= FileRead($File,$Size+4)
			Else
				$Newfile &= FileRead($File,$Size+4)
			EndIf
			$NEWdata[$e+$k] = StringReplace($NEWdata[$e+$k],"<cf>",@CRLF)
			$NEWdata[$e+$k] = StringReplace($NEWdata[$e+$k],"<lf>",@LF)
			$NEWdata[$e+$k] = StringReplace($NEWdata[$e+$k],"<cr>",@CR)
			$Size = _BinaryToInt32(FileRead($File,4))
			If $Size < 0 Then
				$Size = -$Size*2
				FileRead($File,$Size)
			Else
				FileRead($File,$Size)
			EndIf
			If StringIsASCII($NEWdata[$e+$k]) <> 1 Then
				$NewText = StringToBinary($NEWdata[$e+$k],2) & Binary("0x0000")
				$Newfile &= _BinaryFromInt32(-int(BinaryLen($NewText)/2)) & $NewText
			Else
				$NewText = StringToBinary($NEWdata[$e+$k],1) & Binary("0x00")
				$Newfile &= _BinaryFromInt32(int(BinaryLen($NewText))) & $NewText
			Endif
			FileWrite($hNewfile, $Newfile)
		Next
		$j += $e-1
	Next
EndIf
FileClose($hNewfile)

GUICtrlSetData($iEdit, "UE4.25 Importer by FinalQ" & @CRLF & "Text taken from '" & $TxtPath & "' and loaded into 'NEW_" & $iName & "' using '" & $iName & "' successfully!" & @CRLF, 1)

EndFunc

Func LocresExport($Path)
;by FinalQ.NET for UE4.25

_PathSplit ($Path, $iDrive, $iDir, $iName, $iExp)
$file = Fileopen($path,16) ;Открытие файла в бинарном виде (16 - бинарный)

Dim $text

$files = FileRead($File,4)

If $files = "0x0E147475" Then
	FileSetPos($file, 16, 0)
	$byte = FileRead($file, 1)
	FileSetPos($file, FileRead($file, 8), 0)
	$files = FileRead($file, 4)
	For $i = 1 To $files
		$size = _binarytoint32(FileRead($file, 4))
		If $size < 0 Then
			$size = -$size * 2
			$str = BinaryToString(FileRead($file, $size), 2)
			$str = StringTrimRight($str, 1)
		Else
			$str = BinaryToString(FileRead($file, $size), 1)
			$str = StringTrimRight($str, 1)
		EndIf
		If $byte = 2 Then FileRead($file, 4)
		$str = StringReplace($str, @CRLF, "<cf>")
		$str = StringReplace($str, @LF, "<lf>")
		$str = StringReplace($str, @CR, "<cr>")
		$text &= $str & @CRLF
	Next
Else
	For $i = 1 To $files
		$size = _binarytoint32(FileRead($file, 4))
		If $size < 0 Then
			$size = -$size * 2
			FileRead($file, $size)
		Else
			FileRead($file, $size)
		EndIf
		$ent = FileRead($file, 4)
		For $e = 1 To $ent
			$size = _binarytoint32(FileRead($file, 4))
			If $size < 0 Then
				$size = -$size * 2
				FileRead($file, $size)
			Else
				FileRead($file, $size)
			EndIf
			FileRead($file, 4)
			$size = _binarytoint32(FileRead($file, 4))
			If $size < 0 Then
				$size = -$size * 2
				$str = BinaryToString(FileRead($file, $size), 2)
				$str = StringTrimRight($str, 1)
			Else
				$str = BinaryToString(FileRead($file, $size), 1)
				$str = StringTrimRight($str, 1)
			EndIf
			$str = StringReplace($str, @CRLF, "<cf>")
			$str = StringReplace($str, @LF, "<lf>")
			$str = StringReplace($str, @CR, "<cr>")
			$text &= $str & @CRLF
		Next
	Next
EndIf

$hAllTextFile = FileOpen($iDrive & $iDir & $iName & ".txt",2+32) ;256 - UTF-8; 32 - UTF-16-LE
FileWrite($hAllTextFile,$text)
FileClose($hAllTextFile)

GUICtrlSetData($iEdit, "UE4.25 Exporter by FinalQ" & @CRLF & "Text taken from '" & $iName & "' and loaded into '" & $iName & ".txt' successfully!" & @CRLF & "Please do not change the file name and text structure." & @CRLF & "'" & $iName & ".txt' in UTF-16 LE (CRLF) format." & @CRLF, 1)
;Вывод UTF-16 LE строк
;MsgBox(0, "UTF-16 LE count", $Uni)

EndFunc
