
Func _ChildGUI($iGUIName, $iLabelList, $iComboList, $iDefaultList, $iExtList = '') 
;$iGUIName - заголовок меню, $GUIW - ширина окна, $GUIH - высота окна, $iComboStep - количество комбо, $iLabelList - список лейблов над комбиками, $iComboList - список значений комбо, $iDefaultList - список дефолтов комбо

Local $Argum = 0, _
$iLabelName = StringSplit($iLabelList, '|'), _
$iItemSize = $iLabelName[0], _
$iDefaultData = StringSplit($iDefaultList, '|'), _
$iComboData = StringSplit($iComboList, ';'), _
$iCombo[$iItemSize+1], _
$iLabel[$iItemSize+1], _
$iRead[$iItemSize+1], _
$GUIH = $iItemSize*42
If $GUIH < 90 Then $GUIH = 90

GUICtrlSetState($iHideOrShow, $GUI_UNCHECKED)

Global $NewGui = GUICreate($iGUIName, 250, $GUIH, -1, -1)
	If $iMenuColor <> 'Classic' then GUISetBkColor($iColor1)
	GUISetState(@SW_SHOW, $NewGui)
	GUISetIcon (@ScriptDir & "\Data\ico\i.ico")
	
	$OpenFileBTN = GUICtrlCreateButton($OpenFile, 140, ($GUIH/2)-40, 100, 30)

	$OpenFolderBTN = GUICtrlCreateButton($OpenFolder, 140, $GUIH/2, 100, 30)
	
	For $i = 1 to $iItemSize
		$iLabel[$i] = GUICtrlCreateLabel($iLabelName[$i], 15, 5+$Argum, 120, 14)
		GUICtrlSetTip(-1, $iLabelName[$i])
		If $iMenuColor <> 'Classic' then GUICtrlSetColor(-1, $iFontColor)
		$iCombo[$i] = GUICtrlCreateCombo("", 10, 20+$Argum, 120, 100)
		GUICtrlSetData(-1, $iComboData[$i], $iDefaultData[$i])
		$Argum += 40
	Next
	
	;Я против дискриминации цикла Do! Почему везде и все используют только While и For?
	Do 
		$iChMsg = GUIGetMsg($NewGui)
		$iLastDir = $iDrive & $iDir
		For $i = 1 to $iItemSize
			$iRead[$i] = GUICtrlRead($iCombo[$i]) 
		Next
			Switch $iChMsg
				Case $GUI_EVENT_CLOSE
					GUISetState(@SW_HIDE, $NewGui)
					GUICtrlSetState($iHideOrShow, $GUI_CHECKED)
						ExitLoop
						
				Case $iCombo[1]
					If $iRead[1] = 'PS2' Then GUICtrlSetTip($iLabel[2], $ForVAG1 & @CRLF & $ForVAG2)
					If $iGUIName = "PS Audio Converter" Then	
						Switch GUICtrlRead($iCombo[1])
							Case 'PS2'
								_GUICtrlComboBox_ResetContent($iCombo[2])
								GUICtrlSetData($iCombo[2], 'VAG2WAV|WAV2VAG|PS2_SoundBank', 'VAG2WAV')
							Case 'PS3' , 'PSP', 'PSVita'
								_GUICtrlComboBox_ResetContent($iCombo[2])
								GUICtrlSetData($iCombo[2], 'Atrac2WAV|WAV2Atrac', 'Atrac2WAV')
							Case 'PS4'
								_GUICtrlComboBox_ResetContent($iCombo[2])
								GUICtrlSetData($iCombo[2], 'Atrac2WAV|WAV2Atrac|SXD2Atrac', 'Atrac2WAV')
						EndSwitch
					EndIf
					
				Case $OpenFileBTN, $OpenFolderBTN
					If $iGUIName = "Atrac Headler Generator" Then BMSCreateAtrac($iRead[1], $iRead[2], $iRead[3], $iRead[4], $iRead[5])
					If $iGUIName = "Wav Headler Generator" Then BMSCreateWAV($iRead[1], $iRead[2], $iRead[3], $iRead[4])
					If $iGUIName = "PS Audio Converter" and $iRead[2] = 'VAG2WAV' Then BMSCreateWAV(48000, 1, 16, 'PCM')
					If $iGUIName = "ZLIB GUI" Then $iRead[1] = GetModeZlib($iRead[1])
					$iMenuData = _ArrayToString($iRead, "|", 1)
						
					If $iChMsg = $OpenFileBTN Then
						$sFilePath = FileOpenDialog("", "", $iExtList & "All file(*.*)", 1+4)
							If @error = 1 Then ContinueLoop
							
							$iFileList1 = StringSplit ($sFilePath, '|')
							Local $fk = 2
							If $iFileList1[0] = 1 Then $fk = 1
								For $j = $fk to $iFileList1[0]
									If $iFileList1[0] > 1 Then $sFilePath = $iFileList1[1] & '\' & $iFileList1[$j]
										_PathSplit($sFilePath, $iDrive, $iDir, $iName, $iExp)
											_ButtonDo($sFilePath, $iMenuData, $iGUIName)
								Next
					
					ElseIf $iChMsg = $OpenFolderBTN Then
						$sFilePath = FileSelectFolder("", $iLastDir)
							If @error = 1 Then ContinueLoop
								$sFileList = _FileList($sFilePath)
								For $j = 1 to $sFileList[0]
									_PathSplit($sFileList[$j], $iDrive, $iDir, $iName, $iExp)
									$newFolder = $sFolderName & StringTrimRight(StringReplace($iDrive & $iDir, $sFilePath, ''), 1)
									If Not FileExists($newFolder) Then DirCreate($newFolder)
										_ButtonDo($sFileList[$j], $iMenuData, $iGUIName, $newFolder)
								Next
							ShellExecuteWait (@ScriptDir & "\data\defo.bat", "", $sFolderName, "open")
					EndIf
					MsgBox (0, "", $tDone & '!')
					
			EndSwitch
	Until False
EndFunc

Func _ButtonDo($sFilePath, $iMenuData, $iGUIName, $nFolderName = $sFolderName)
Local $iCombo = StringSplit($iMenuData, '|')
;_OtherPRG($iExtList, $iPRGName, $iCommand1 = ' ', $iCommand2 = '', $iWorkDir = $nFolderName, $sFileName = '', $iFF = True) 
	Switch $iGUIName
	
		Case "Atrac Headler Generator"
			;_Console(@ScriptDir & '\Data\quickbms.exe ' & @ScriptDir & "\data\scripts\atrac_script.bms " & ' "' & $sFilePath & '" "' & $nFolderName & '"')
			_QuickBMSRun('', @ScriptDir & "\data\scripts\atrac_script.bms ", $sFilePath, $nFolderName)
			
		Case "Wav Headler Generator"
			;_Console(@ScriptDir & '\Data\quickbms.exe ' & @ScriptDir & "\data\scripts\wav_script.bms " & ' "' & $sFilePath & '" "' & $nFolderName & '"')
			_QuickBMSRun('', @ScriptDir & "\data\scripts\wav_script.bms ", $sFilePath, $nFolderName)
			
		Case "ZLIB GUI"
			_OtherPRG('', "offzip.exe ", $iCombo[1], $nFolderName & ' ' & $iCombo[2], $nFolderName, $sFilePath)
			
		Case "XWMA Tool GUI"
			_OtherPRG('', '\xWMAEncode.exe ', ' -b ' & $iCombo[1] & ' ', ' "' & $nFolderName & '\' & $iName & '.' & $iCombo[2] & '"', $nFolderName, $sFilePath)
		
		Case "DDS Tools GUI nVidia"
			_OtherPRG('', '\dds_tools\nvdxt.exe ', ' -file "', '" ' & '-' & $iCombo[1] & ' -output "' & $nFolderName & '\' & $iName & '.dds"', $nFolderName, $sFilePath)
		
		Case "DDS Tools GUI Microsoft"
			If $iCombo[2] = 'PC' then $iProg = "dds_tools\texconv.exe"
			If $iCombo[2] = 'XBox One' then $iProg = "dds_tools\xtexconv.exe"
			_OtherPRG('', $iProg, ' -f ' & $iCombo[1] & ' -o "' & $nFolderName & '" ', '', $nFolderName, $sFilePath)
		
		Case "FFMPEG GUI"
			_OtherPRG('*.*', 'ffmpeg.exe ', ' -i ', ' -vcodec ' & $iCombo[1] & " -vb " & $iCombo[3] & " -vf scale=" & $iCombo[6] & " -acodec " & $iCombo[2] & " -ab " & $iCombo[4] & " -map 0:0 -map 0:" & $iCombo[7] & ' "' & $nFolderName & "\" & $iName & "." & $iCombo[5] & '"', $nFolderName, $sFilePath)
		
		Case "FFMPEG AUDIO"
			_OtherPRG('', 'ffmpeg.exe', ' -i ', ' -vn -ab ' & $iCombo[3] & ' -ac ' & $iCombo[2] & " -af aresample=" & $iCombo[1] & ' "' & $nFolderName & "\" & $iName & "." & $iCombo[4] & '"', $nFolderName, $sFilePath)
		
		Case "FFMPEG IMAGE"
			_OtherPRG('', 'ffmpeg.exe', ' -i ', ' "' & $nFolderName & '\' & $iName & '.' & $iCombo[1] & '"', $nFolderName, $sFilePath)
			
		Case "DDS Header Generator"
			DDSSaving($iCombo[1], $iCombo[2], $iCombo[3], $iCombo[4], $sFilePath)
			GUICtrlSetData($iEdit, $tDone & ' ' & $sFilePath & @CRLF, 1)
			
		Case "NCONVERT GUI"
			FileCopy($sFilePath, $nFolderName & '\' & $iName & $iExp)
			_OtherPRG('', 'nconvert\nconvert.exe', ' -out ' & $iCombo[1] & ' ', '', $nFolderName, $nFolderName & '\' & $iName & $iExp, $sFilePath)
			FileDelete($nFolderName & '\' & $iName & $iExp)
		
		Case "Wwise Converter"
			If $iCombo[1] = 'WWISE_Unpacker' Then 
				Switch $iExp 
					Case ".pck", ".akpk"
						_QuickBMSRun('', @ScriptDir & '\data\scripts\wwsise_pck_akpk.bms ', $sFilePath)
					Case ".bnk"
						_QuickBMSRun('', @ScriptDir & '\data\scripts\wwsise_bnk.bms ', $sFilePath)
					Case ".afc"
						_OtherPRG('', 'afcextr.exe ', ' ', '', $nFolderName, $sFilePath)
					Case Else
						_QuickBMSRun('', @ScriptDir & '\data\scripts\wwsise_pck_akpk.bms ', $sFilePath)
						_QuickBMSRun('', @ScriptDir & '\data\scripts\wwsise_bnk.bms ', $sFilePath)
						_OtherPRG('', 'afcextr.exe ', ' ', '', $nFolderName, $sFilePath)
				EndSwitch
			ElseIf $iCombo[1] = 'wwise2wav' Then
				_OtherPRG('', "wwise_ima_adpcm.exe", ' -d ', '"' & $nFolderName & "\" & $iName & '.wav"', $nFolderName, $sFilePath)
			ElseIf $iCombo[1] = 'wwise2vorbis' Then
				_OtherPRG('', "ww2ogg.exe ", '', ' --pcb ' & @ScriptDir & '\data\' & $iCombo[2] & ' -o "' & $nFolderName & "\" & $iName & '.ogg"', $nFolderName, $sFilePath)
				ShellExecuteWait (@ScriptDir & '\data\revorb.exe', ' "' & $nFolderName & "\" & $iName & '.ogg"', $nFolderName, 'open', @SW_HIDE)
			EndIf
			
		Case "PS Audio Converter"
		;TODO: Сделать проверку параметров входных файлов
			Switch $iCombo[2] 
				Case 'VAG2WAV'
					FileCopy ($sFilePath, @TempDir)
					_OtherPRG('', "vagunpacker.exe", '', '' , $nFolderName, @TempDir & '\' & $iName & $iExp)
					_Console(@ScriptDir & '\Data\quickbms.exe ' & @ScriptDir & "\data\scripts\wav_script.bms " & ' "' & @TempDir & '\' &  $iName & '.pcm' & '" "' & $nFolderName & '"')
				Case 'WAV2VAG'
					FileCopy ($sFilePath, $nFolderName)
					_OtherPRG('', "vagpacker.exe", '', '' , $nFolderName, $nFolderName & '\' & $iName & $iExp)
					FileDelete ($nFolderName & '\' & $iName & $iExp)
				Case 'SXD2Atrac' 
					_QuickBMSRun("", @ScriptDir & "\data\scripts\sxd_at9.bms ", $sFilePath)
				Case 'PS2_SoundBank'
					_QuickBMSRun("", @ScriptDir & "\data\scripts\989_sound_bank.bms ", $sFilePath)
				Case "Atrac2WAV", "WAV2Atrac"
					If $iCombo[1] = "PS3" Then $iPrg = "PS3_at3tool"
					If $iCombo[1] = "PSP" Then $iPrg = "PSP_at3tool"
					If $iCombo[1] = "PSVita" Then $iPrg = "PSVita_at9tool"
					If $iCombo[1] = "PS4" Then $iPrg = "PS4_at9tool"
					If $iCombo[2] = "Atrac2WAV" Then $iLet = " -d "
					If $iCombo[2] = "WAV2Atrac" Then $iLet = " -e "
					If $iCombo[2] = "Atrac2WAV" Then $iFmt = "wav"
					If BitOR($iCombo[1] = "PS3", $iCombo[1] = "PSP") Then $iFmt = "at3"
					If BitOR($iCombo[1] = "PS4", $iCombo[1] = "PSVita") Then $iFmt = "at9"
					_OtherPRG('', $iPrg & ".exe", $iLet, ' "' & $nFolderName & "\" & $iName & "." & $iFmt & '"', $nFolderName, $sFilePath)
			EndSwitch
		
	EndSwitch
EndFunc

Func BMSCreateAtrac($iFreq, $iChan, $iBitrate, $iFormat, $iOffset)
	$hFile = FileOpen(@ScriptDir & "\data\scripts\atrac_script.bms", 10)
	Local $iBMSScript = ['include "func_header_' & $iFormat & '.bms"', 'set FREQ ' & $iFreq, 'set CH ' & $iChan, 'set OFFSET ' & $iOffset, 'set BITRATE ' & $iBitrate, 'get SIZE asize', 'math SIZE -= OFFSET', 'callfunction ' & $iFormat & ' 1']
	
	For $String in $iBMSScript
		FileWriteLine ($hFile, $String)
	Next
	
	FileClose ($hFile)
EndFunc

Func GetModeZlib($iModeSet)
	If $iModeSet = "Scan_ZLIB" Then Return (" -S ")
	If $iModeSet = "Cool_scan_ZLIB" Then Return (" -S -x -Q ")
	If $iModeSet = "Extract_ZLIB" Then Return ( " -a ")
	If $iModeSet = "Extract_Deflate" Then Return (" -a -z -15 -Q ")
	If $iModeSet = "Reimport_ZLIB" Then Return (" -a -r ")
EndFunc

Func BMSCreateWAV($iFreq, $iChan, $iBits, $iFormat)
	
	Local $iArrCodecList = ["UNKNOWN(0000)", "PCM", "ADPCM", "IEEE_FLOAT", "VSELP", "IBM_CVSD", "ALAW", "MULAW", "DTS", "DRM", "OKI_ADPCM", "DVI_ADPCM", "IMA_ADPCM", "MEDIASPACE_ADPCM", "SIERRA_ADPCM", "G723_ADPCM", "DIGISTD", "DIGIFIX", "DIALOGIC_OKI_ADPCM", "MEDIAVISION_ADPCM", "CU_CODEC", "YAMAHA_ADPCM", "SONARC", "DSPGROUP_TRUESPEECH", "ECHOSC1", "AUDIOFILE_AF36", "APTX", "AUDIOFILE_AF10", "PROSODY_1612", "LRC", "DOLBY_AC2", "GSM610", "MSNAUDIO", "ANTEX_ADPCME", "CONTROL_RES_VQLPC", "DIGIREAL", "DIGIADPCM", "CONTROL_RES_CR10", "NMS_VBXADPCM", "CS_IMAADPCM", "ECHOSC3", "ROCKWELL_ADPCM", "ROCKWELL_DIGITALK", "XEBEC", "G721_ADPCM", "G728_CELP", "MSG723", "MPEG", "RT24", "PAC", "MP3", "LUCENT_G723", "CIRRUS", "ESPCM", "VOXWARE", "CANOPUS_ATRAC", "G726_ADPCM", "G722_ADPCM", "DSAT_DISPLAY", "VOXWARE_BYTE_ALIGNED", "VOXWARE_AC8", "VOXWARE_AC10", "VOXWARE_AC16", "VOXWARE_AC20", "VOXWARE_RT24", "VOXWARE_RT29", "VOXWARE_RT29HW", "VOXWARE_VR12", "VOXWARE_VR18", "VOXWARE_TQ40", "SOFTSOUND", "VOXWARE_TQ60", "MSRT24", "G729A", "MVI_MVI2", "DF_G726", "DF_GSM610", "ISIAUDIO", "ONLIVE", "SBC24", "DOLBY_AC3_SPDElseIf", "MEDIASONIC_G723", "PROSODY_8KBPS", "ZYXEL_ADPCM", "PHILIPS_LPCBB", "PACKED", "MALDEN_PHONYTALK", "RHETOREX_ADPCM", "IRAT", "VIVO_G723", "VIVO_SIREN", "DIGITAL_G723", "SANYO_LD_ADPCM", "SIPROLAB_ACEPLNET", "SIPROLAB_ACELP4800", "SIPROLAB_ACELP8V3", "SIPROLAB_G729", "SIPROLAB_G729A", "SIPROLAB_KELVIN", "G726ADPCM", "QUALCOMM_PUREVOICE", "QUALCOMM_HALFRATE", "TUBGSM", "MSAUDIO1", "UNISYS_NAP_ADPCM", "UNISYS_NAP_ULAW", "UNISYS_NAP_ALAW", "UNISYS_NAP_16K", "CREATIVE_ADPCM", "CREATIVE_FASTSPEECH8", "CREATIVE_FASTSPEECH10", "UHER_ADPCM", "QUARTERDECK", "ILINK_VC", "RAW_SPORT", "ESST_AC3", "IPI_HSX", "IPI_RPELP", "CS2", "SONY_SCX", "FM_TOWNS_SND", "BTV_DIGITAL", "QDESIGN_MUSIC", "VME_VMPCM", "TPC", "OLIGSM", "OLIADPCM", "OLICELP", "OLISBC", "OLIOPR", "LH_CODEC", "NORRIS", "SOUNDSPACE_MUSICOMPRESS", "DVM", "ATRAC", "UNKNOWN(FFFF)"]

	Local $iArrCodecData = [0000, 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0010, 0011, 0011, 0012, 0013, 0014, 0015, 0016, 0017, 0018, 0019, 0020, 0021, 0022, 0023, 0024, 0025, 0026, 0027, 0028, 0030, 0031, 0032, 0033, 0034, 0035, 0036, 0037, 0038, 0039, "003A", "003B", "003C", "003D", 0040, 0041, 0042, 0050, 0052, 0053, 0055, 0059, 0060, 0061, 0062, 0063, 0064, 0065, 0067, 0069, 0070, 0071, 0072, 0073, 0074, 0075, 0076, 0077, 0078, 0079, 0080, 0081, 0082, 0083, 0084, 0085, 0086, 0088, 0089, 0091, 0092, 0093, 0094, 0097, 0098, 0099, "00A0", 0100, 0101, 0111, 0112, 0123, 0125, 0130, 0131, 0132, 0133, 0134, 0135, 0140, 0150, 0151, 0155, 0160, 0170, 0171, 0172, 0173, 0200, 0202, 0203, 0210, 0220, 0230, 0240, 0241, 0250, 0251, 0260, 0270, 0300, 0400, 0450, 0680, 0681, 1000, 1001, 1002, 1003, 1004, 1100, 1400, 1500, 2000, "FFFE", "FFFF"]
	
	$iCodec = Dec ($iArrCodecData[_ArraySearch($iArrCodecList, $iFormat)])
	If @error = 1 Then $iCodec = $iFormat
	
	$hFile = FileOpen(@ScriptDir & '\data\scripts\wav_script.bms', 10)
	Local $iWAVScript = ["set FREQUENCY long " & $iFreq, "set CHANNELS long " & $iChan, "set BITS long " & $iBits, "set CODEC long " & $iCodec, "get SIZE asize", "get NAME filename", 'string NAME += ".wav"', 'set MEMORY_FILE binary "\x52\x49\x46\x46\x00\x00\x00\x00\x57\x41\x56\x45\x66\x6d\x74\x20\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x64\x61\x74\x61\x00\x00\x00\x00"', "set RIFFSIZE long SIZE", "math RIFFSIZE += 36", "set BLOCKALIGN long BITS", "set AVGBYTES long FREQUENCY", "math BLOCKALIGN /= 8", "math BLOCKALIGN *= CHANNELS", "math AVGBYTES *= BLOCKALIGN", "putvarchr MEMORY_FILE 4 RIFFSIZE long", "putvarchr MEMORY_FILE 20 CODEC short", "putvarchr MEMORY_FILE 22 CHANNELS short", "putvarchr MEMORY_FILE 24 FREQUENCY long", "putvarchr MEMORY_FILE 28 AVGBYTES long", "putvarchr MEMORY_FILE 32 BLOCKALIGN short", "putvarchr MEMORY_FILE 34 BITS short", "putvarchr MEMORY_FILE 40 SIZE long", "log NAME 0 44 MEMORY_FILE", "append", "log NAME 0 SIZE", "append"]
	
	For $String in $iWAVScript
		FileWriteLine ($hFile, $String)
	Next
	
	FileClose ($hFile)
	
EndFunc


