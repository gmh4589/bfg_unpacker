
Func LocalizeRead()
	Global $sLanguage = IniRead (@ScriptDir & '\unpacker.ini', 'Main', 'Language', '')
	
		If $sLanguage = '' or Not FileExists(@ScriptDir & '\data\local\' & $sLanguage & '.loc') Then 
			$sLanguage = OSLang()
			IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Language', $sLanguage)
		EndIf
		
		Local $sLng
		_FileReadToArray(@ScriptDir & '\data\local\' & $sLanguage & '.loc', $sLng)
		
		Global $tFile = $sLng[1], _
		$tQOpen = $sLng[2], _
		$tPack = $sLng[3], _
		$tUnpWith = $sLng[4], _
		$tEngine = $sLng[5], _
		$tInstaller = $sLng[6], _
		$tArchives = $sLng[7], _
		$tDImage = $sLng[8], _
		$tCompFormat = $sLng[9], _
		$tConv = $sLng[10], _
		$tFSerch = $sLng[11], _
		$tAdv = $sLng[12], _
		$ASearch = $sLng[13], _
		$AScan = $sLng[14], _
		$Flist = $sLng[15], _
		$tExit = $sLng[16], _
		$tTools = $sLng[17], _
		$tHEX = $sLng[18], _
		$tFav = $sLng[19], _
		$tA2Fav = $sLng[20], _
		$tD2Fav = $sLng[21], _
		$c2Fav = $sLng[22], _
		$tSetting = $sLng[23], _
		$sTFolder = $sLng[24], _
		$mTFolder = $sLng[25], _
		$cTFolder = $sLng[26], _
		$delEFolder = $sLng[27], _
		$delEFile = $sLng[28], _
		$tLink = $sLng[29], _
		$tAbout = $sLng[30], _
		$tAP = $sLng[31], _
		$tLang = $sLng[32], _
		$tAction = $sLng[33], _
		$tCancel = $sLng[34], _
		$tE2A = $sLng[35], _
		$tListT = $sLng[36], _
		$tWarning = $sLng[37], _
		$tWarning2 = $sLng[38], _
		$tWarning3 = $sLng[39], _
		$tWarning4 = $sLng[40], _
		$tFolder1 = $sLng[41], _
		$tSelectFile = $sLng[42], _
		$tAllFile = $sLng[43], _
		$tFile = $sLng[44], _
		$tFiles = $sLng[45], _
		$tAll = $sLng[46], _
		$tArchive = $sLng[47], _
		$tProcessingFile = $sLng[48], _
		$tDone = $sLng[49], _
		$tError = $sLng[50], _
		$tiD56 = $sLng[51], _
		$tMessage = $sLng[52], _
		$tNoEngine = $sLng[53], _
		$tAllSupp = $sLng[54], _
		$tNoGame = $sLng[55], _
		$tNLNSupp = $sLng[56], _
		$tAllVideo = $sLng[57], _
		$tSelectAudioFolder = $sLng[58], _
		$tFileList = $sLng[59], _
		$tFileList1 = $sLng[60], _
		$tFileList2 = $sLng[61], _
		$tAllSupFile = $sLng[62], _
		$tExeFile = $sLng[63], _
		$tDLL = $sLng[64], _
		$teBooks = $sLng[65], _
		$tAnd = $sLng[66], _
		$tWtCoping = $sLng[67], _
		$tWtAComv = $sLng[68], _
		$tSNGV2OGG = $sLng[69], _
		$tSNGVno = $sLng[70], _
		$tLoad = $sLng[71], _
		$tClsd = $sLng[72], _
		$tLNGSlct = $sLng[73], _
		$tWRNNG = $sLng[74], _
		$tDELAll1 = $sLng[75], _
		$tAllFFF = $sLng[76], _
		$tAlldel = $sLng[77], _
		$tCrFld = $sLng[78], _
		$tFolder2 = $sLng[79], _
		$tCreated = $sLng[80], _
		$tDAEFFF = $sLng[81], _
		$tNote = $sLng[82], _
		$tUIFIDW = $sLng[83], _
		$tFOSAF = $sLng[84], _
		$tDFWS0BFF = $sLng[85], _
		$tFISAND = $sLng[86], _
		$tOLCITNAS = $sLng[87], _
		$tFOTFSOA = $sLng[88], _
		$tTFANF = $sLng[89], _
		$tAbout2 = $sLng[90], _
		$tAbout3 = $sLng[91], _
		$tAbout4 = $sLng[92], _
		$tOpenINI = $sLng[93], _
		$tVideoIn = $sLng[94], _
		$tTexturesIn = $sLng[95], _
		$tBPTIn = $sLng[96], _
		$tTo = $sLng[97], _
		$toTo = $sLng[98], _
		$tWarning5 = $sLng[99], _
		$tWarning6 = $sLng[100], _
		$tVConv = $sLng[101], _
		$tSGF = $sLng[102], _
		$tIFFGB = $sLng[103], _
		$tIFFGO = $sLng[104], _
		$tIFA = $sLng[105], _
		$tIFDI = $sLng[106], _
		$tIFEB = $sLng[107], _
		$tIFAFOS = $sLng[108], _
		$tCBMSG1 = $sLng[109], _
		$tCBMSG2 = $sLng[110], _
		$tCBMSG3 = $sLng[111], _
		$tCBMSG4 = $sLng[112], _
		$tCBMSG5 = $sLng[113], _
		$tCBMSG6 = $sLng[114], _
		$tCBMSG7 = $sLng[115], _
		$tCBMSG8 = $sLng[116], _
		$tUsing = $sLng[117], _
		$tExo1 = $sLng[118], _
		$tExo2 = $sLng[119], _
		$tExo3 = $sLng[120], _
		$tExo4 = $sLng[121], _
		$tExo5 = $sLng[122], _
		$tIsSaved = $sLng[123], _
		$tCopied = $sLng[124], _
		$tIFCHF = $sLng[125], _
		$tIFAL = $sLng[126], _
		$tIFFP = $sLng[127], _
		$tItsfile = $sLng[128], _
		$tIFI = $sLng[129], _
		$tIFWA = $sLng[130], _
		$tIFFG = $sLng[131], _
		$tSelHand = $sLng[132], _
		$tIFCFAG = $sLng[133], _
		$tIFD = $sLng[134], _
		$tIFPFWB = $sLng[135], _
		$tIFV = $sLng[136], _
		$tIFAu = $sLng[137], _
		$tIFDGW = $sLng[138], _
		$tNotice1 = $sLng[139], _
		$tNotice2 = $sLng[140], _
		$tNotice3 = $sLng[141], _
		$tFavAdd = $sLng[142], _
		$tF12 = $sLng[143], _
		$tOGGno = $sLng[144], _
		$OpenFile = $sLng[145], _
		$OpenFolder = $sLng[146], _
		$Fullpath = $sLng[147], _
		$Format = $sLng[148], _
		$VideoCodec = $sLng[149], _
		$AudioCodec = $sLng[150], _
		$VideoBitrate = $sLng[151], _
		$AudioBitrate = $sLng[152], _
		$Platform = $sLng[153], _
		$Mode = $sLng[154], _
		$Offset = $sLng[155], _
		$Frequency = $sLng[156], _
		$Channel = $sLng[157], _
		$Bit = $sLng[158], _
		$Codebook = $sLng[159], _
		$ForVAG1 = $sLng[160], _
		$ForVAG2 = $sLng[161], _
		$tWaitList = $sLng[162], _
		$tSP_msg1 = $sLng[163], _
		$tSP_msg2 = $sLng[164], _
		$tSP_msg3 = $sLng[165], _
		$tSP_msg4 = $sLng[166], _
		$tSP_msg5 = $sLng[167], _
		$tNotSupport = $sLng[168], _
		$tConsoles = $sLng[169], _
		$tWtSaving = $sLng[170], _
		$tSave = $sLng[171], _
		$tAll = $sLng[172], _
		$tFav2 = $sLng[173], _
		$tFind = $sLng[174], _
		$tShowCon = $sLng[175], _
		$tFNF = $sLng[176], _
		$tFCF = $sLng[177], _
		$tOtherF = $sLng[178], _
		$tLoad = $sLng[179], _
		$tAllGames = $sLng[180], _
		$tEnterFBV = $sLng[181], _
		$tVer123 = $sLng[182], _
		$tVer123_2 = $sLng[183], _
		$tClick1 = $sLng[184], _
		$tClick2 = $sLng[185], _
		$H_W = $sLng[186], _
		$AudioTrack = $sLng[187], _
		$tShowEngine = $sLng[188], _
		$tUseThemes = $sLng[189], _
		$tLoadProgress = $sLng[190], _
		$tGroupBy = $sLng[191], _
		$tName = $sLng[192], _
		$tYear = $sLng[193], _
		$tSelColor = $sLng[194], _
		$tOutFolder = $sLng[195], _
		$tApply = $sLng[196], _
		$tNotFind = $sLng[197], _
		$tWidth = $sLng[198], _
		$tHight = $sLng[199], _
		$tAudio = $sLng[200], _
		$tVideo = $sLng[201], _
		$tTextures = $sLng[202], _
		$tDELAll2 = $sLng[203], _
		$tyes = $sLng[204], _
		$tno = $sLng[205], _
		$tabort = $sLng[206], _
		$tretry = $sLng[207], _
		$tignore = $sLng[208], _
		$tagain = $sLng[209], _
		$tcontinue = $sLng[210], _
		$tChangeBTN = $sLng[211], _
		$tTarsh = $sLng[212], _
		$tDelete = $sLng[213], _
		$tIntoFolder = $sLng[214], _
		$tUnpacking = $sLng[215], _
		$tArchiveName = $sLng[216], _
		$tWait = $sLng[217], _
		$tDeleting = $sLng[218], _
		$tLeft = $sLng[219], _
		$tPassed = $sLng[220], _
		$tElapsed = $sLng[221], _
		$tFolderEmpty = $sLng[222], _
		$tFrom = $sLng[223], _
		$tRunAsAdm = $sLng[224], _
		$tBTN = $sLng[225], _
		$tBTN1 = $sLng[226], _
		$tBTN2 = $sLng[227], _
		$tREG = $sLng[228], _
		$tADD = $sLng[229], _
		$tCreateSubFolder = $sLng[230]
EndFunc
