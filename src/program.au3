
Func _QuickBMSRun($iExtList, $iScriptName, $sFileName = '') ;Для скриптов BMS: Список_расширений, Название_скрипта, Имя_файла
	_fileReaper(_Console, $iExtList, $sFileName, $iScriptName)
EndFunc

Func _OtherPRG($iExtList, $iPRGName, $iCommand1 = ' ', $iCommand2 = '', $iWorkDir = $sFolderName, $sFileName = '', $iMove = False) 
;Для прочих программ: Список_расширений, Название_программы, Комманда_перед_именем_файла, Комманда_после_имени_файла, Рабочая_папка, Имя_файла, Файл или папка (True - файл, False - папка))
; Исправлено!
	Local $iParray = [$iPRGName, $iCommand1, $iCommand2, $iWorkDir, $iMove]
	_fileReaper(_Console, $iExtList, $sFileName, $iParray)
EndFunc

Func _7z($iExtList, $sFileName = '')
	;PASS
EndFunc

Func _OtherPRGExt($iMode1, $sFileName = '')
	If $iMode1 <> BitOR('_SAU', '_VGM') Then Return(_MsgBox(0, '', 'Error 404'))
	
	If $iMode1 = '_SAU' Then $iExtList = $tAllSupp & "(*.adf;*.agg;*.bdx;*.spr;*.pak;*.box;*.brig;*.chr;*.dat;*.bin;*.cam;*.cc;*.cmp;mas0*;*.df2;*.*c;*.rm;*.anm;*.4pp;*.epf;*.flx;*.gor;*.h4r;*.hrs;*.idx;*.ilb;*.key;*.lbx;*.lod;*.group;*.bin;*.mpq;*.dbi;*.ff;*.wdb;*.mul;*.nds;*.p00;*.p10;*.p99;*.pak;*.res;*.snd;*.tgw;*.tlb;*.uop;*.vid;*.vsr;*.war;*.xua;*.xub;*.jun;*.maa;*.jus;*.fan)|Amiga Disk File (*.adf)|Heroes of Might & Magic 1-2 (*.agg)|Black Moon Chronicles, Persian Wars (*.SPR)|Beats of Rage " & $tArchives & " (*.pak)|Beasts & Bumpkins " & $tArchives & " (*.box)|Brigandine (*.brig)|Beyond the Beyond (*CHR;*.DAT;*.BIN)|Cyberlore Library Manager (*.cam)|Kings Bounty " & $tAnd & " Might & Magic 3/4/5 " & $tArchives & " (*.cc)|Divine Divinity" & $tArchive & "(*.cmp)|Dark Seal 2: Wizard Fire (mas0*)|Tibia MMORPG (Tibia.dat)|Heroes of Might & Magic 4 sprite " & $tArchives & " (*.df2)|Divine Divinity sprite" & $tArchive & "(*.*c)|Dominus (*.rm;*anm;*.4pp;*.dat)|Realms of Arkania 2 (*.DAT)|East Point File System (*.epf)|Ultima 7, 8 " & $tAnd & " Crusader No Remorse " & $tArchives & " (*.flx)|Myth Fallen Lords " & $tArchives & " " & $tAnd & " Tagged Files (*.gor)|Stonekeep groupXX " & $tArchives & " (*.group)|Heroes of Might & Magic 4 " & $tArchives & " (*.h4r)|Heimdall (*.bin;*.dat)|Faery Tale Adventure 2 " & $tAnd & " Dinotopia " & $tArchives & " (*.hrs)|Jinyong Qunxia Zhuan " & $tArchives & " (*.idx)|Age of Wonders 1-2 image " & $tArchives & " (*.ilb)|Infinity Engine Directory (*.key)|Master of Magic " & $tArchives & " (*.lbx)|Lunar: Genesis / Dragon Song (*.dat)|Cyberlore Library (*.lib)|LOD " & $tArchives & " (*.lod)Majesty for IPhone/IPad (*.group.bin)|Blizzard MPQ " & $tArchives & " (*.mpq)|Disciples: Sacred Lands (*.DBI;*.FF;*.WDB)|Ultima Online" & $tArchive & "(*.mul)|Nintendo Nitro Filesystem " & $tAnd & " Formats (*.NDS)|Popolocrois" & $tArchive & "(*.p00;*.p1;*.p99)|Helbreath sprite " & $tArchives & " (*.pak)|Rage of Mages 1-2 (Allods) " & $tArchives & " (*.res)|Mystic Towers (rgmystus.dat)|SND " & $tArchives & " (*.snd)|Kohan: Immortal Sovereigns " & $tArchives & " (*.tgw)|SSI Tileset (*.tlb)|Ultima Online Mythic Package (*.uop)|Vandal Hearts (*.DAT)|VID " & $tArchives & " (*.vid)|Lemmings Paintball (*.vsr)|Warcraft 1 " & $tAnd & " 2 " & $tArchives & " (*.war)|Original Mulan " & $tArchives & " (*.XUA;*.XUB;*.JUN;*.MAA;*.JUS;*.FAN)|"
	
	If $iMode1 = '_VGM' Then  $iExtList =$tAllSupp & "(*.2dx9; *.aaap; *.aax; *.acm; *.adp; *.adpcm; *.ads; *.ss2; *.adx; *.adxkey; *.afc; *.agsc; *.ahx; *.ahxkey; *.aifc; *.aiff; *.aix; *.amts; *.asd; *.asf; *.as4; *.asr; *.ass; *.ast; *.ast; *.at3; *.aud; *.aus; *.baf; *.baka; *.bao; *.pk; *.bar; *.bg00; *.bgw; *.bh2pcm; *.bmdx; *.bns; *.bnsf; *.bnsfkey; *.bo2; *.brstm; *.caf; *.capdsp; *.ccc; *.cfn; *.cnk; *.dcs; *.dcsw; *.ddsp; *.dec; *.de2; *.dmsg; *.dsp; *.dvi; *.idvi; *.dxh; *.eam; *.emff; *.enth; *.fag; *.filp; *.fsb; *.wii; *.fsbkey; *.gca; *.gcm; *.gcsw; *.gcw; *.genh; *.gms; *.gsp; *.hca; *.hcakey; *.hgc1; *.his; *.hps; *.hwas; *.idsp; *.ikm; *.ild; *.int; *.ish; *.isd; *.ivaud; *.ivb; *.joe; *.kces; *.khv; *.kraw; *.leg; *.lps; *.lsf; *.lstm; *.lwav; *.matx; *.mc3; *.mca; *.mcg; *.mib; *.mi4; *.mic; *.mihb; *.mp4; *.lmp4; *.mpdsp; *.msa; *.msf; *.mss; *.msvp; *.mta2; *.mtaf; *.mus; *.musc; *.musx; *.mwv; *.myspd; *.ndp; *.npsf; *.nwa; *.ogg; *.logg; *.ogl; *.p3d; *.pcm; *.dvi; *.pcm; *.kcey; *.pcm; *.pdt; *.pnb; *.pos; *.ps2stm; *.psh; *.psw; *.raw; *.rkv; *.rnd; *.rrds; *.rsd; *.rsf; *.rstm; *.rwar; *.rwav; *.rws; *.rws; *.rwsd; *.rwx; *.rxw; *.s14; *.sss; *.sab; *.sad; *.sap; *.sb0; *.sb1; *.sb2; *.sb3; *.sb4; *.sb5; *.sb6; *.sb7; *.sc; *.scd; *.sd9; *.sdt; *.seg; *.sfl; *.sfs; *.sgd; *.sgb; *.sgh; *.sgx; *.sl3; *.sli; *.sm0; *.sm1; *.sm2; *.sm3; *.sm4; *.sm5; *.sm6; *.sm7; *.smp; *.smp; *.smpl; *.snd; *.snd; *.sng; *.sngw; *.sns; *.spd; *.sps; *.spsd; *.spt; *.spw; *.ssm; *.ster; *.sth; *.stm; *.stma; *.str; *.str; *.strm; *.sts; *.stx; *.svag; *.svs; *.swav; *.swd; *.tec; *.thp; *.tk5; *.txth; *.txtp; *.tydsp; *.ulw; *.um3; *.vag; *.vas; *.vgs; *.vig; *.vjdsp; *.voi; *.vpk; *.vs; *.vsf; *.waa; *.wac; *.wad; *.wam; *.was; *.wav; *.wavm; *.wb; *.wem; *.wp2; *.wsd; *.wsi; *.wvs; *.xa; *.xa2; *.xa30; *.xma; *.xmu; *.xss; *.xvas; *.xwav; *.xwb; *.xwb; *.xwh; *.xwh; *.ydsp; *.ymf; *.zsd; *.zwdsp)|"
	
	$sFileName = _getFile($sFileName, $iExtList)
		If @error = 1 then Return

	$iFileList1 = StringSplit ($sFileName, '|')
	Local $a1 = UBound($iFileList1) - 1, $fc1 = 2
	If $a1 = 1 Then $fc1 = 1
	For $i1 = $fc1 to $a1
		If $iFileList1[0] > 1 Then $sFileName = $iFileList1[1] & '\' & $iFileList1[$i1]
		_PathSplit($sFileName, $iDrive, $iDir, $iName, $iExp)
		If $iMode1 = '_SAU' Then _OtherPRG('', 'sau.exe', './', " " & $sFolderName & '\', $iDrive & '\' & $iDir, $iName & $iExp)	
		If $iMode1 = '_VGM' Then _OtherPRG('', 'vgmstream\test.exe', '-o ' & $sFolderName & '\' & $iName & '.wav ', '', $sFolderName, $sFileName)
	Next
EndFunc

Func _ScriptCreate($iStringArray, $iJobFolder = $sFolderName)
	$hFile = FileOpen(@TempDir & "\temp.bat", 10)
	FileWriteLine ($hFile, "chcp 65001")
	If Not IsArray($iStringArray) Then FileWriteLine ($hFile, $iStringArray)
	For $String in $iStringArray
		FileWriteLine ($hFile, $String)
	Next
	FileClose ($hFile)
	ShellExecuteWait (@TempDir & "\temp.bat", "", $iJobFolder, "open")
	FileDelete (@TempDir & "\temp.bat")
EndFunc

Func _DosBox($iExtList, $iProgName, $iArg1, $iArg2, $sFileName = '') 
;Для старых программ, работающих через DosBox: Список_расширений, Название_программы, Аргумент_имени_файла (1 или 0), Комманда

	$sFileName = _getFile($sFileName, $iExtList)
		If @error = 1 then Return
		
	_PathSplit($sFileName, $iDrive, $iDir, $iName, $iExp)
		If $iArg1 = 1 Then
			$FullName = $iName & $iExp
		ElseIf $iArg1 = 0 Then
			$FullName = ''
		EndIf
	$iFile = FileOpen($sFolderName & "\dosbox.conf", 2)
	FileWrite ($iFile, "[autoexec]" & @CRLF & "@ECHO OFF" & @CRLF & 'MOUNT C "."' & @CRLF & "C:" & @CRLF & $iProgName & $FullName & $iArg2 & @CRLF & "EXIT")
	FileClose ($iFile)
	FileCopy (@ScriptDir & "\data\" & $iProgName, $sFolderName)
	FileCopy (@ScriptDir & "\data\dos4gw.exe", $sFolderName)
	FileCopy ($sFileName, $sFolderName)
	GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)
	ShellExecute (@ScriptDir & "\data\DosBox.exe", "", $sFolderName, "open")
	Sleep(5000)
	Send("1{ENTER}")
	ProcessWaitClose ("dosbox.exe")
	FileDelete ($sFolderName & "\" & $iProgName)
	FileDelete ($sFolderName & "\dos4gw.exe")
	FileDelete ($sFolderName & '\' & $iName & $iExp)
	FileDelete ($sFolderName & "\dosbox.conf")
	GUICtrlSetData($iEdit, $tDone & ': ' & $sFileName & @CRLF, 1)
EndFunc

Func _WithArray($iGameName, $iFileArray, $iPRGName, $iSubFolder = '') ;Для программ, в которых нужно копировать файлы списком
; Исправлено!
	$sFolderPath = FileSelectFolder ($tSGF & $iGameName, $iLastDir)
		If @error = 1 then Return
			GUICtrlSetData($iEdit, $tWtCoping & @CRLF, 1)
			If $iSubFolder <> '' Then
				DirCreate ($sFolderName & $iSubFolder)
			EndIf
			$a = UBound($iFileArray)
			For $i = 0 to $a - 1
				FileCopy ($sFolderPath & $iFileArray[$i], $sFolderName & $iSubFolder)
				GUICtrlSetData($iEdit, $tCopied & " " & $i & "/" & $a & @CRLF, 1)
				;ProgressSet((100/$a) * $i, $tCopied & " " & $i & "/" & $a )
				_BarCreate((100/$a) * $i, $tWtCoping, $tCopied & " " & $i & "/" & $a, 300, 120)
			Next			
			ProgressSet(100, $tDone)
			_BarOFF()
			FileCopy (@ScriptDir & "\Data\" & $iPRGName, $sFolderName)
			GUICtrlSetData($iEdit, $tCopied & " " & $a & "/" & $a  & @CRLF, 1)
			$iOutputWindow = ShellExecuteWait ($sFolderName & '\' & $iPRGName, "", $sFolderName, "open")
			For $j = 0 to $a - 1
				FileDelete ($sFolderName & $iFileArray[$j])
			Next
			FileDelete ($sFolderName & '\' & $iPRGName)
			Output_MSG($iOutputWindow, $sFileName)
EndFunc

Func _StringChange($sScriptName, $iString, $X) ;Путь к файлу, в котором нужно заменить строку, Новая строка, Номер строки
	Local $iStringScript
	_FileReadToArray ($sScriptName, $iStringScript)
	$iStringScript[$X] = $iString
	_FileWriteFromArray ($sScriptName, $iStringScript, 1)
EndFunc

Func _headRead($iFN, $num = 2, $mode = 0)
	$iF = FileOpen($iFN, $mode)
	$iHead = FileRead($iF, $num)
	FileClose($iF)
	Return($iHead)
EndFunc

Func Xenus($iProg);TODO: Удалить этот говнокод!!!
	$sFilePath = FileOpenDialog($tSelectFile, " ", "GRP File (*.grp)|" & $tAllFile & " (*.*)", 1)
		If @error = 1 then Return
			_PathSplit($sFilePath, $iDrive, $iDir, $iName, $iExp)
			$sFullFileName = ($iName & ".grp")
			$sJobFolder = StringReplace ($sFilePath, $sFullFileName, "")
			$hFile = FileOpen (@TempDir & "\start.bat", 10)
			FileWriteLine ($hFile, "chcp 65001")
			FileWriteLine ($hFile, "copy """ & @ScriptDir & "\data\" & $iProg & ".exe"" """  & $sJobFolder & """")
			FileWriteLine ($hFile, "set __compat_layer=WINXPSP3")
			FileWriteLine ($hFile, """" & $sJobFolder & $iProg & ".exe"" """ & $sFilePath & """")
			FileWriteLine ($hFile, "pause")
			FileClose ($hFile)
			$iOutputWindow = ShellExecute (@TempDir & "\start.bat", "", $sFolderName, "open")
			FileDelete (@TempDir & "\start.bat")
			Output_MSG($iOutputWindow, $sFileName)
EndFunc

Func Xenus2();TODO: Удалить этот говнокод!!!
	$sFilePath = FileOpenDialog($tSelectFile, " ", "GRP File (*.grp)|" & $tAllFile & " (*.*)", 1)
		If @error = 1 then Return
			_PathSplit($sFilePath, $iDrive, $iDir, $iName, $iExp)
			$sFullFileName = ($iName & ".grp")
			$sJobFolder = StringReplace ($sFilePath, $sFullFileName, "")
			$hFile = FileOpen (@TempDir & "\start.bat", 10)
			FileWriteLine ($hFile, "chcp 65001")
			FileWriteLine ($hFile, "copy """ & @ScriptDir & "\data\GrpUnpacker.exe"" """  & $sJobFolder & """")
			FileWriteLine ($hFile, """" & $sJobFolder & "GrpUnpacker.exe"" """ & $sFilePath & """")
			FileWriteLine ($hFile, "pause")
			FileClose ($hFile)
			ShellExecute (@TempDir & "\start.bat", "", $sFolderName, "open")
			FileDelete (@TempDir & "\start.bat")
EndFunc

Func _Console($Cmd, $Cmd1 = '', $WorkDir = $sFolderName, $sFileName = '', $iHideConsole = GUICtrlRead($iHideOrShow) = 1 ? False : True)
	Local $SH = $iHideConsole = True ? @SW_HIDE : @SW_SHOW, $line, _
	$iShell = StringInStr($Cmd, '.py') > 0 ? True : False
	
		$logFile = @ScriptDir & '\log.txt'
		$iLog = FileOpen($logFile, 10)
		$size = FileGetSize($sFileName)
		FileWriteLine($iLog, $Cmd & $Cmd1)
		
	If $iHideConsole Then 
		If Not $iShell Then $iOutputWindow = Run($Cmd & $Cmd1, $WorkDir, $SH, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
		If $iShell Then $iOutputWindow = ShellExecuteWait($Cmd, $Cmd1, $WorkDir, 'open', $SH);, $STDERR_CHILD + $STDOUT_CHILD + $STDIN_CHILD)
		GUICtrlSetData($iEdit, @CRLF & $Cmd & @CRLF, 1)

		StdinWrite($iOutputWindow)

		While True
			$line = StdoutRead($iOutputWindow)
			If @error Then ExitLoop
			GUICtrlSetData($iEdit, $line, 1)
			If $line <> '' Then FileWriteLine($iLog, $line)
			
			$line1 = StderrRead($iOutputWindow)
			If @error Then ExitLoop
			GUICtrlSetData($iEdit, $line1, 1)
			If $line1 <> '' Then FileWriteLine($iLog, $line1)
			
			_EnginePB($iOutputWindow, 110, $size)
		Wend

		ProcessClose($iOutputWindow)
		StdioClose($iOutputWindow)
		FileClose($iLog)
		GUICtrlSetData($iEdit, @CRLF & $tDone & @CRLF, 1)
	Else
		$iOutputWindow = ShellExecuteWait($Cmd, $Cmd1, $WorkDir)
		Output_MSG($iOutputWindow, $sFileName)
	EndIf
	
EndFunc
