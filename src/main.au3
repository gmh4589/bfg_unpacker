Func Main()
	Do
		$iLastDir = $iDrive & $iDir
		$msg = GUIGetMsg($hGui)
		
		$iShowFlag = GUICtrlRead($iHideOrShow) = 4 ? @SW_HIDE : GUICtrlRead($iHideOrShow) = 1 ? @SW_SHOW
		
		_CursorMove($hGui)
		
		Switch $msg
			Case $GUI_EVENT_CLOSE, $iExit 
				ExitLoop
				
		Case $GUI_EVENT_DROPPED
			QuickOpen(@GUI_DragFile)

		Case $iAll_Checkbox
			If $iFavPlus = 0 Then
				_GUICtrlComboBox_ResetContent($iFindMenu)
				GUICtrlSetData($iFindMenu, FileRead (@ScriptDir & '\data\favorites.ini'), "")
				$iFavPlus = 1
				GUICtrlSetData($iAll_Checkbox, $tFav2)
			ElseIf $iFavPlus = 1 Then
				_GUICtrlComboBox_ResetContent($iFindMenu)
				GUICtrlSetData($iFindMenu, $iLST, "")
				$iFavPlus = 0
				GUICtrlSetData($iAll_Checkbox, $tAll)
			EndIf
			
		Case $iReimport_Checkbox
			If GUICtrlRead($iReimport_Checkbox) = 1 Then  
				$rI = " -G -w -r "
			Else
				$rI = ""
			EndIf
		
		Case $iReimport_CheckboxTXT
			GUICtrlSetState($iReimport_Checkbox, _Checker($iReimport_Checkbox))
		Case $iHideOrShowTXT
			GUICtrlSetState($iHideOrShow, _Checker($iHideOrShow))
				
		Case $iDeFi 
			Defi()
		Case $iDeFo
			Defo()
		Case $iMakeFolder
			DirCreate(IniRead ('unpacker.ini', 'Main', 'Path', ''))
		Case $iClearFolder
			ClearFolder()
		Case $iSelectFolder
			SelectFolder()
		Case $iOpenINI
			SettingMenu()
		Case $iSelectLang
			SelectLang()
		Case $iAbout
			_MsgBox(0, $tAbout2, $tAbout3 & @CRLF & $tAbout4)

		Case $idButton[1], $iOpenQuick
			$sFileName = FileOpenDialog ($tSelectFile, " ", $tAllFile & " (*.*)", 1)
			If @error <> 1 Then
				QuickOpen($sFileName)
			EndIf
		Case $iTotal7zip
			_OtherPRG($tAllFile & " (*.*)|" & $tAllSupFile & " (*.zip;*.7z;*.rar;*.pak;*.dat;*.exe;*.tar;*.wim;*.gz;*.bz;*.gzip;*.bzip;*.gz2;*.bz2;*.lzma;*.iso;*.cab;*.xz;*.txz;*.cpio;*.tbz;*.tbz2;*.tgz;*.tgz2;*.tpz;*.taz;*.z;*.lzh;*.lha;*.rpm;*.deb;*.lzm;*.pk3;*.pk4;*.arj;*.vhd;*.swm;*.dmg;*.hfs;*.xar;*.chm;*.squashfs;*.dll;*.ocx;*.xpi;*.crf;*.epub;*.txtz;*.7zip;*.cb7;*.cb7z;*.omod;*.fomod;*.so1;*.phar;*.phr;*.lzma2;*.lzm2;*.lz4;*.lz5;*.zstd;*.nsz;*.xcz;*e01;*ex01;*.l01;*.lx01;*.aff;*.ad1;*.whx;*.ccs;*.cdi;*.img;*.chd;*.cso;*.bin;*.cue;*.ecm;*.gdi;*.isz;*.mds;*.mdf;*.nrg;*.ZiSofs)|Zip  " & $tArchives & "  (*.zip)|7z  " & $tArchives & "  (*.7z)|RAR  " & $tArchives & "  (*.rar)|PAK  " & $tArchives & "  (*.pak)|DAT " & $tFiles & " (*.dat)|" & $tExeFile & " (*.exe)|TAR  " & $tArchives & "  (*.tar)|WIM  " & $tArchives & "  (*.win;*.swm)|GZIP  " & $tArchives & "  (*.gz;*.gzip;*.gz2;*.tgz;*.tgz2)|BZIP  " & $tArchives & "  (*.bz;*.bzip;*.bz2;*.tbz;*.tbz2)|LZMA  " & $tArchives & "  (*.lzma;*.lzm)|" & $tDImage & " (*.iso;*.vhd)|Cabinet  " & $tArchives & "  (*.cab)|XZ  " & $tArchives & "  (*.xz;*.txz)|CPIO  " & $tArchives & "  (*.cpio)|TAZ  " & $tArchives & "  (*.tpz;*.taz;*.z)|LZH  " & $tArchives & "  (*.lzh)|LHA  " & $tArchives & "  (*.lha)|RPM  " & $tArchives & "  (*.rpm)|DEB Installer (*.deb)|idTech Plugin (*.pk3;*.pk4)|ARJ  " & $tArchives & "  (*.arj)|DMG Installer (*.dmg)|HFS " & $tFiles & "  (*.hfs)|XAR  " & $tArchives & "  (*.xar)|CHM " & $tFiles & " (*.chm)|squashfs " & $tFiles & " (*.squashfs)|" & $tDLL & " (*.dll;*.ocx)|XPI Archive\Firefox Plugin (*.xpi)|System Shock 2 (*.crf)|" & $teBooks & " (*.epub;*.txtz)", '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip')
		Case $iGAUP
			_QuickBMSRun($tAllFile & " (*.*)|AFS File (*.afs)|Age of Empires 1-3 (*.DRS;*.AGE3SCN;*.BAR)|BAG File (*.bag)|Bethesda BSA File (*.bsa)|BIG/VIV Files (*.big;*.viv)|BIN File (*.bin)|CAT File (*.cat)|COB File (*.cob)|DAT File (*.dat)|Earth 21*0 (*.WD)|F.E.A.R. (*.ARCH00)|Gothic 1-3 (*.vdf;*.pak)|GTA 2-4 (*.RAW;*.SDT;*.IMG;*.DIR)|DAT File (*.dat)|DIR File (*.dir)|Heroes of M&M 2-4 (*.AGG;*.LOD;*.SND;*.VID;*.H4C)|Hitman 1-4 (*.LGT;*.SPK;*.PRM;*.WAV;*.WHD)|idTech File (*.wad;*.pak)|IDX File (*.idx)|IMG File (*.img)|Lintech REZ File (*.rez)|Master Of Magic/Orion (*.LBX)|Neverwinter Nights 1-2 (*.ERF;*.MOD;*.HAK)|PAC File (*.pac)|PAK File (*.pak)|PBO File (*.pbo)|PFF File (*.pff)|PKG File (*.pkg)|POD File (*.pod)|Postal 2 (*.FUK;*.PSK)|RES File (*.res)|Unreal Engine 1-2 (*.u;*.u*)|WarCraft 2 (*.CUD;*.INS;*.SUD)|Windows Installer (*.exe;*.msi)|Age of Mythology (*.BAR;*.SCX;*.XMB)|Age of Wonders II (*.A2C;*.ACM;*.AHM)|Air Strike 3D (*.APK)|AirXonix (*.MUS)|Alpha Ball (*.ABL)|Aura; Fate Of The Ages (*.PSP;*.PVD)|Battle Realms (*.H2O)|Beach Head 2002 (*.*24)|Black and White 2 (*.LUD)|Bricks of Egypt (*.GFX)|Brothers in Arms (*.GBXMAP;*.LTE)|Call of Duty 4 (*.IWI)|Call of Duty; World at War (*.IWI)|Carmageddon II (*.TWT)|Championsheep Rally (*.DBC)|Civilization IV (*.FPK)|Colin McRae Rally 3 (*.BGX;*.PCX;*.TBF)|Color Eggs (*.STG)|Command & Conquer (*.MIX;*.DBS;*.THU)|Commandos 2; Men of Courage (*.PCK)|Corsairs (*.TF)|Cossacks (*.GSC)|Crash Time 2 (*.PTX)|Crimsonland (*.FRAME;*.JAZ;*.SEQUENCE)|Crysis (*.RAW)|Death Rally (*.BPA)|Death Track; Resurrection Demo (*.RR)|Demonstar (*.GLB)|Destruction Derby (*.000;*.001)|Destruction Derby 2 (DIRINFO.*)|Disciples II (*.FF)|Dragonshard (*.H2O)|Duke Nukem II (*.CMP)|Duke Nukem 3D (*.GRP;*.RTS)|Dune 2000 (*.R*)|Dungeon Lords (*.AL4;*.AL8;*.TWD)|Earth 21*0 (*.WD)|EPOC Operation System (*.SIS)|ExMachina (*.GDP)|Fable; The Lost Chapters (*.LUG;*.LUT;*.STB)|FlatOut (*.BFS)|Frank Herbert's Dune (*.DUN)|Fresco Wizard (*.SDF)|Giza (*.MJZ)|Gooka; The Mystery of Janatris (*.SAV)|Gunbound (*.XFS)|Hard Truck (*.RMP)|Jagged Alliance 2  (*.SLF)|Earth (*.0000)|Krush, Kill 'n' Destroy (*.SLV)|Knight Rider (*.NIF)|LOTR; War Of Ring (*.H2O)|Luxor (*.MJZ)|Mad Cars (*.FRAME;*.SEQUENCE)|Mafia (*.DTA)|Merchant Prince II (*.ANM;*.MSK)|Metal Gear Solid 2 (*.QAR)|MIG-29 Fulcrum (*.SBF)|Moorhuhn (*.WTN)|Mor.Utopia (*.VFS)|MotoGP 3 (*.ARK)|Nancy Drew (*.HIS)|Nuclear Titbit (*.EZD)|Patrician III (*.CPR;*.SKS)|Perimeter (*.AVIX)|Petka 2-4 (*.STR;*.MULT;*.RSS)|Pharaon (*.555)|Pocket Tanks (*.BBK;*.EMI;*.WEP)|Pool'm Up (*.MSF)|Primitive Wars (*.TRC)|Prince of Persia (*.FAT;*.BIK;*.BF)|Ragnarok (*.EBM;*.RAW;*.XPK)|Red Faction (*.VPP)|Ricochet (*.FRAME;*.SEQUENCE)|Rise of the Triad (*.RTS)|Roll'm Up (*.MSF)|Silent Hill 3 (*.ARC)|Silent Hill 4 (*.bin;*.pak;*.sh4)|SimCity 3000 (*.IFX;*.SC3;*.SCT;*.ST3)|Spell of Gold (*.JDR;*.JSR;*.JTR)|SpellForce Order of Dawn (*.MAP)|Standofood (*.MJP)|Starlancer (*.HOG)|Star Heritage 1 (*.BPK)|Star Wars; Empire at War (*.MEG)|Star Wars; Republic Commando (*.CTM;*.CTS)|Starsiege; TRIBES (*.TED;*.VOL)|Still Life (*.CMO;*.NMO;*.SL)|Sudden Strike (*.SUE)|SWAT 4 (*.S4M)|Syberia (*.CMO;*.NMO;*.SYJ)|Syberia 2 (*.NMO;*.SYB)|Test Drive Unlimited (*.BNK;*.2DB)|The Bard's Tale (*.LMP)|The Punisher (*.CEG;*.VPP)|The Sims Makin Magic (*.FAR)|The Suffering (*.TDU;*.VDU)|The Sum Of All Fears (*.RSB)|Theme Park World (*.SDT)|Ghost Recon (*.RSB)|Tomb Raider (*.TRC;*.CLZ;*.AWD)|Tzar (*.WDT)|Warhammer 40000; Dawn of War (*.SGA)|Warlords Battlecry III (*.XCR)|Z Expansion (*.EXP)", @ScriptDir & "\data\wcx\gaup_pro.wcx ")
		Case $iConv_12
			_ChildGUI("FFMPEG GUI", $VideoCodec & '|' & $AudioCodec & '|' & $VideoBitrate & '|' & $AudioBitrate & '|' & $Format & '|' & $H_W & '|' & $AudioTrack, "a64_multi|a64_multi5|alias_pix|amv|apng|asv1|asv2|avrp|avui|ayuv|bmp|cinepak|cljr|dirac|dnxhd|dpx|dvvideo|ffv1|ffvhuff|flashsv|flashsv2|flv1|gif|h261|h263|h263p|h264|hap|hevc|huffyuv|jpeg2000|jpegls|ljpeg|mjpeg|mpeg1video|mpeg2video|mpeg4|msmpeg4v2|msmpeg4v3|msvideo1|pam|pbm|pcx|pgm|pgmyuv|png|ppm|prores|qtrle|r10k|r210|rawvideo|roq|rv10|rv20|sgi|snow|sunrast|svq1|targa|theora|tiff|utvideo|v210|v308|v408|v410|vp8|vp9|webp|wmv1|wmv2|wrapped_avframe|xbm|xface|xwd|y41p|yuv4|zlib|zmbv;copy|aac|ac3|adpcm_adx|adpcm_g722|adpcm_g726|adpcm_ima_qt|adpcm_ima_wav|adpcm_ms|adpcm_swf|adpcm_yamaha|alac|amr_nb|amr_wb|comfortnoise|dts -strict -2|eac3|flac|g723_1|mp2|mp3|nellymoser|opus -strict -2|pcm_alaw|pcm_f32be|pcm_f32le|pcm_f64be|pcm_f64le|pcm_mulaw|pcm_s16be|pcm_s16be_planar|pcm_s16le|pcm_s16le_planar|pcm_s24be|pcm_s24daud|pcm_s24le|pcm_s24le_planar|pcm_s32be|pcm_s32le|pcm_s32le_planar|pcm_s8|pcm_s8_planar|pcm_u16be|pcm_u16le|pcm_u24be|pcm_u24le|pcm_u32be|pcm_u32le|pcm_u8|ra_144|roq_dpcm|s302m|sonic|sonicls|speex|tta|vorbis -strict -2|wavpack|wmav1|wmav2;64k|128k|192k|256k|512k|768k|1M|2M|3M|4M|5M|6M|8M|10M|12M|15M|16M|20M|25M|30M|40M|50M;16k|24k|32k|48k|64k|96k|112k|128k|160k|192k|224k|256k|320k|360k|448k|512k|768k|1M|2M;3g2|3gp|a64|asf|avi|dv|dvd|f4v|flv|hevc|ivf|m1v|m2v|m2t|m2ts|m4v|mkv|mjpeg|mov|mp4|mpeg|mpg|mts|mxf|ogv|pam|rm|roq|swf|ts|vc1|vp8|vob|webm|wmv|wtv;160:120|240:144|240:160|320:240|360:240|384:240|400:240|432:240|480:320|480:360|480:360|640:360|512:384|640:480|720:480|800:480|854:480|720:540|960:540|720:576|1024:576|800:600|1024:600|800:640|960:640|1024:640|1136:640|960:720|1152:720|1200:720|1280:720|1024:768|1152:768|1280:768|1366:768|1280:800|1152:864|1280:864|1536:864|1440:900|1600:900|1280:960|1440:960|1280:1024|1400:1050|1680:1050|1440:1080|1920:1080|2560:1080|2048:1152|1600:1200|1920:1200|1920:1440|2560:1440|3440:1440|1920:1536|2048:1536|2560:1600|2880:1620|2880:1800|3200:1800|2560:2048|3200:2048|3840:2160|5120:2880|4069:2160|4096:3072|5120:3200|5760:3240|5120:4096|6400:4096|7680:4320|6400:4800|7680:4800;0|1|2|3|4|5|6|7|8|9|10", "hevc|aac|8M|192k|mkv|" & @DesktopWidth & ":" & @DesktopHeight & "|1") 
		Case $iUnreal
			_Engine('_Unreal')
		Case $iUnity
			_Engine('_Unity')
		Case $iDTech
			_Engine('_idTech')
		Case $iSource
			_Engine('_Source')
		Case $iBethesda
			_Engine('_Bethesda')
		Case $iCryEngine
			_Engine('_CryEngine')
		Case $idButton[1]
			$sFileName = FileOpenDialog ($tSelectFile, " ", $tAllFile & " (*.*)", 1)
			If @error <> 1 Then
				QuickOpen($sFileName)
			EndIf	
			
		Case $idButton[2] to $idButton[14]
			For $i = 2 to 14
				If $msg = $idButton[$i] Then 
					Switch IniRead (@ScriptDir & '\unpacker.ini', 'Button', 'Button' & $i, $abcArray[$i])
						Case 'B'
							If GUICtrlRead($iReimport_Checkbox) = 1 Then
								ShellExecute (@ScriptDir & "\data\QuickBMS.exe", " -G -w -r ")
							Else
								Run (@ScriptDir & "\data\QuickBMS.exe")
							EndIf
						Case 'C'
							_OtherPRG($tAllFile & " (*.*)|" & $tAllSupFile & " (*.zip;*.7z;*.rar;*.pak;*.dat;*.exe;*.tar;*.wim;*.gz;*.bz;*.gzip;*.bzip;*.gz2;*.bz2;*.lzma;*.iso;*.cab;*.xz;*.txz;*.cpio;*.tbz;*.tbz2;*.tgz;*.tgz2;*.tpz;*.taz;*.z;*.lzh;*.lha;*.rpm;*.deb;*.lzm;*.pk3;*.pk4;*.arj;*.vhd;*.swm;*.dmg;*.hfs;*.xar;*.chm;*.squashfs;*.dll;*.ocx;*.xpi;*.crf;*.epub;*.txtz;*.7zip;*.cb7;*.cb7z;*.omod;*.fomod)|Zip  " & $tArchives & "  (*.zip)|7z  " & $tArchives & "  (*.7z)|RAR  " & $tArchives & "  (*.rar)|PAK  " & $tArchives & "  (*.pak)|DAT " & $tFiles & " (*.dat)|" & $tExeFile & " (*.exe)|TAR  " & $tArchives & "  (*.tar)|WIM  " & $tArchives & "  (*.win;*.swm)|GZIP  " & $tArchives & "  (*.gz;*.gzip;*.gz2;*.tgz;*.tgz2)|BZIP  " & $tArchives & "  (*.bz;*.bzip;*.bz2;*.tbz;*.tbz2)|LZMA  " & $tArchives & "  (*.lzma;*.lzm)|" & $tDImage & " (*.iso;*.vhd)|Cabinet  " & $tArchives & "  (*.cab)|XZ  " & $tArchives & "  (*.xz;*.txz)|CPIO  " & $tArchives & "  (*.cpio)|TAZ  " & $tArchives & "  (*.tpz;*.taz;*.z)|LZH  " & $tArchives & "  (*.lzh)|LHA  " & $tArchives & "  (*.lha)|RPM  " & $tArchives & "  (*.rpm)|DEB Installer (*.deb)|idTech Plugin (*.pk3;*.pk4)|ARJ  " & $tArchives & "  (*.arj)|DMG Installer (*.dmg)|HFS " & $tFiles & "  (*.hfs)|XAR  " & $tArchives & "  (*.xar)|CHM " & $tFiles & " (*.chm)|squashfs " & $tFiles & " (*.squashfs)|" & $tDLL & " (*.dll;*.ocx)|XPI Archive\Firefox Plugin (*.xpi)|System Shock 2 (*.crf)|" & $teBooks & " (*.epub;*.txtz)", '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', "")
						Case 'D'
							_QuickBMSRun($tAllFile & " (*.*)|AFS File (*.afs)|Age of Empires 1-3 (*.DRS;*.AGE3SCN;*.BAR)|BAG File (*.bag)|Bethesda BSA File (*.bsa)|BIG/VIV Files (*.big;*.viv)|BIN File (*.bin)|CAT File (*.cat)|COB File (*.cob)|DAT File (*.dat)|Earth 21*0 (*.WD)|F.E.A.R. (*.ARCH00)|Gothic 1-3 (*.vdf;*.pak)|GTA 2-4 (*.RAW;*.SDT;*.IMG;*.DIR)|DAT File (*.dat)|DIR File (*.dir)|Heroes of M&M 2-4 (*.AGG;*.LOD;*.SND;*.VID;*.H4C)|Hitman 1-4 (*.LGT;*.SPK;*.PRM;*.WAV;*.WHD)|idTech File (*.wad;*.pak)|IDX File (*.idx)|IMG File (*.img)|Lintech REZ File (*.rez)|Master Of Magic/Orion (*.LBX)|Neverwinter Nights 1-2 (*.ERF;*.MOD;*.HAK)|PAC File (*.pac)|PAK File (*.pak)|PBO File (*.pbo)|PFF File (*.pff)|PKG File (*.pkg)|POD File (*.pod)|Postal 2 (*.FUK;*.PSK)|RES File (*.res)|Unreal Engine 1-2 (*.u;*.u*)|WarCraft 2 (*.CUD;*.INS;*.SUD)|Windows Installer (*.exe;*.msi)|Age of Mythology (*.BAR;*.SCX;*.XMB)|Age of Wonders II (*.A2C;*.ACM;*.AHM)|Air Strike 3D (*.APK)|AirXonix (*.MUS)|Alpha Ball (*.ABL)|Aura; Fate Of The Ages (*.PSP;*.PVD)|Battle Realms (*.H2O)|Beach Head 2002 (*.*24)|Black and White 2 (*.LUD)|Bricks of Egypt (*.GFX)|Brothers in Arms (*.GBXMAP;*.LTE)|Call of Duty 4 (*.IWI)|Call of Duty; World at War (*.IWI)|Carmageddon II (*.TWT)|Championsheep Rally (*.DBC)|Civilization IV (*.FPK)|Colin McRae Rally 3 (*.BGX;*.PCX;*.TBF)|Color Eggs (*.STG)|Command & Conquer (*.MIX;*.DBS;*.THU)|Commandos 2; Men of Courage (*.PCK)|Corsairs (*.TF)|Cossacks (*.GSC)|Crash Time 2 (*.PTX)|Crimsonland (*.FRAME;*.JAZ;*.SEQUENCE)|Crysis (*.RAW)|Death Rally (*.BPA)|Death Track; Resurrection Demo (*.RR)|Demonstar (*.GLB)|Destruction Derby (*.000;*.001)|Destruction Derby 2 (DIRINFO.*)|Disciples II (*.FF)|Dragonshard (*.H2O)|Duke Nukem II (*.CMP)|Duke Nukem 3D (*.GRP;*.RTS)|Dune 2000 (*.R*)|Dungeon Lords (*.AL4;*.AL8;*.TWD)|Earth 21*0 (*.WD)|EPOC Operation System (*.SIS)|ExMachina (*.GDP)|Fable; The Lost Chapters (*.LUG;*.LUT;*.STB)|FlatOut (*.BFS)|Frank Herbert's Dune (*.DUN)|Fresco Wizard (*.SDF)|Giza (*.MJZ)|Gooka; The Mystery of Janatris (*.SAV)|Gunbound (*.XFS)|Hard Truck (*.RMP)|Jagged Alliance 2  (*.SLF)|Earth (*.0000)|Krush, Kill 'n' Destroy (*.SLV)|Knight Rider (*.NIF)|LOTR; War Of Ring (*.H2O)|Luxor (*.MJZ)|Mad Cars (*.FRAME;*.SEQUENCE)|Mafia (*.DTA)|Merchant Prince II (*.ANM;*.MSK)|Metal Gear Solid 2 (*.QAR)|MIG-29 Fulcrum (*.SBF)|Moorhuhn (*.WTN)|Mor.Utopia (*.VFS)|MotoGP 3 (*.ARK)|Nancy Drew (*.HIS)|Nuclear Titbit (*.EZD)|Patrician III (*.CPR;*.SKS)|Perimeter (*.AVIX)|Petka 2-4 (*.STR;*.MULT;*.RSS)|Pharaon (*.555)|Pocket Tanks (*.BBK;*.EMI;*.WEP)|Pool'm Up (*.MSF)|Primitive Wars (*.TRC)|Prince of Persia (*.FAT;*.BIK;*.BF)|Ragnarok (*.EBM;*.RAW;*.XPK)|Red Faction (*.VPP)|Ricochet (*.FRAME;*.SEQUENCE)|Rise of the Triad (*.RTS)|Roll'm Up (*.MSF)|Silent Hill 3 (*.ARC)|Silent Hill 4 (*.bin;*.pak;*.sh4)|SimCity 3000 (*.IFX;*.SC3;*.SCT;*.ST3)|Spell of Gold (*.JDR;*.JSR;*.JTR)|SpellForce Order of Dawn (*.MAP)|Standofood (*.MJP)|Starlancer (*.HOG)|Star Heritage 1 (*.BPK)|Star Wars; Empire at War (*.MEG)|Star Wars; Republic Commando (*.CTM;*.CTS)|Starsiege; TRIBES (*.TED;*.VOL)|Still Life (*.CMO;*.NMO;*.SL)|Sudden Strike (*.SUE)|SWAT 4 (*.S4M)|Syberia (*.CMO;*.NMO;*.SYJ)|Syberia 2 (*.NMO;*.SYB)|Test Drive Unlimited (*.BNK;*.2DB)|The Bard's Tale (*.LMP)|The Punisher (*.CEG;*.VPP)|The Sims Makin Magic (*.FAR)|The Suffering (*.TDU;*.VDU)|The Sum Of All Fears (*.RSB)|Theme Park World (*.SDT)|Ghost Recon (*.RSB)|Tomb Raider (*.TRC;*.CLZ;*.AWD)|Tzar (*.WDT)|Warhammer 40000; Dawn of War (*.SGA)|Warlords Battlecry III (*.XCR)|Z Expansion (*.EXP)", @ScriptDir & "\data\wcx\gaup_pro.wcx ")
						Case 'E'
							_OtherPRG('Inno Setup Installer (*.exe)|', 'innounp.exe', ' -x -d"' & $sFolderName & '" ', '', $sFolderName, '')
						Case 'F'
							_ChildGUI("FFMPEG GUI", $VideoCodec & '|' & $AudioCodec & '|' & $VideoBitrate & '|' & $AudioBitrate & '|' & $Format & '|' & $H_W & '|' & $AudioTrack, "a64_multi|a64_multi5|alias_pix|amv|apng|asv1|asv2|avrp|avui|ayuv|bmp|cinepak|cljr|dirac|dnxhd|dpx|dvvideo|ffv1|ffvhuff|flashsv|flashsv2|flv1|gif|h261|h263|h263p|h264|hap|hevc|huffyuv|jpeg2000|jpegls|ljpeg|mjpeg|mpeg1video|mpeg2video|mpeg4|msmpeg4v2|msmpeg4v3|msvideo1|pam|pbm|pcx|pgm|pgmyuv|png|ppm|prores|qtrle|r10k|r210|rawvideo|roq|rv10|rv20|sgi|snow|sunrast|svq1|targa|theora|tiff|utvideo|v210|v308|v408|v410|vp8|vp9|webp|wmv1|wmv2|wrapped_avframe|xbm|xface|xwd|y41p|yuv4|zlib|zmbv;copy|aac|ac3|adpcm_adx|adpcm_g722|adpcm_g726|adpcm_ima_qt|adpcm_ima_wav|adpcm_ms|adpcm_swf|adpcm_yamaha|alac|amr_nb|amr_wb|comfortnoise|dts -strict -2|eac3|flac|g723_1|mp2|mp3|nellymoser|opus -strict -2|pcm_alaw|pcm_f32be|pcm_f32le|pcm_f64be|pcm_f64le|pcm_mulaw|pcm_s16be|pcm_s16be_planar|pcm_s16le|pcm_s16le_planar|pcm_s24be|pcm_s24daud|pcm_s24le|pcm_s24le_planar|pcm_s32be|pcm_s32le|pcm_s32le_planar|pcm_s8|pcm_s8_planar|pcm_u16be|pcm_u16le|pcm_u24be|pcm_u24le|pcm_u32be|pcm_u32le|pcm_u8|ra_144|roq_dpcm|s302m|sonic|sonicls|speex|tta|vorbis -strict -2|wavpack|wmav1|wmav2;64k|128k|192k|256k|512k|768k|1M|2M|3M|4M|5M|6M|8M|10M|12M|15M|16M|20M|25M|30M|40M|50M;16k|24k|32k|48k|64k|96k|112k|128k|160k|192k|224k|256k|320k|360k|448k|512k|768k|1M|2M;3g2|3gp|a64|asf|avi|dv|dvd|f4v|flv|hevc|ivf|m1v|m2v|m2t|m2ts|m4v|mkv|mjpeg|mov|mp4|mpeg|mpg|mts|mxf|ogv|pam|rm|roq|swf|ts|vc1|vp8|vob|webm|wmv|wtv;160:120|240:144|240:160|320:240|360:240|384:240|400:240|432:240|480:320|480:360|480:360|640:360|512:384|640:480|720:480|800:480|854:480|720:540|960:540|720:576|1024:576|800:600|1024:600|800:640|960:640|1024:640|1136:640|960:720|1152:720|1200:720|1280:720|1024:768|1152:768|1280:768|1366:768|1280:800|1152:864|1280:864|1536:864|1440:900|1600:900|1280:960|1440:960|1280:1024|1400:1050|1680:1050|1440:1080|1920:1080|2560:1080|2048:1152|1600:1200|1920:1200|1920:1440|2560:1440|3440:1440|1920:1536|2048:1536|2560:1600|2880:1620|2880:1800|3200:1800|2560:2048|3200:2048|3840:2160|5120:2880|4069:2160|4096:3072|5120:3200|5760:3240|5120:4096|6400:4096|7680:4320|6400:4800|7680:4800;0|1|2|3|4|5|6|7|8|9|10", "hevc|aac|8M|192k|mkv|" & @DesktopWidth & ":" & @DesktopHeight & "|1") 
						Case 'G'
							_Engine('_Unreal')
						Case 'H'
							_Engine('_Unity')
						Case 'I'
							_Engine('_idTech')
						Case 'J'
							_Engine('_Source')
						Case 'K'
							_Engine('_Bethesda')
						Case 'L'
							_Engine('_CryEngine')
						Case 'M'
							ShellExecute (@ScriptDir & "\data\RADVideo\RADVideo64.exe", "", $sFolderName, "open")
						Case 'N'
							_ChildGUI("Wwise Converter", $Mode & '|' & $Codebook, "WWISE_Unpacker|wwise2wav|wwise2vorbis;packed_codebooks_aoTuV_603.bin|packed_codebooks3.bin", "WWISE_Unpacker|packed_codebooks3.bin", "All supported (*.pck;*.bnk;*.afc;*.akpk*.wav;*wwise*;*.lwav;*.pcm;*.wem;*.03f;*.0b2*;*.ogg;*.oga)|")
						Case 'O'
							_ChildGUI("PS Audio Converter", $Platform & '|' & $Mode, "PS2|PS3|PSP|PSVita|PS4;Atrac2WAV|WAV2Atrac", "PS3|Atrac2WAV", "Atrac audio file (*.vag;*.at3;*.at3p;*.at9;*.wav;*.genh;*.pcm)|")
						Case 'P'
							_ChildGUI("NCONVERT GUI", $Format, "bmp|cur|dcx|dds|dib|dng|gif|jif|jpeg|pcd|pcx|pdf|png|psb|psd|raw|svg|tga|tiff|wbmp|--Other--|2bp|2d|3fr|411|a64|abmp|abr|abs|acc|ace|aces|acorn|adex|adt|afphoto|afx|ai|aim|aip|aipd|alias|ami|ani|anv|aphp|apx|arcib|arf|arn|art|artdir|arw|atk|att|aurora|avs|avw|az7|b16|b3d|bdr|bfli|bfx|bga|bias|bif|biorad|bip|bld|blp|bmc|bmg|bms|bmx|bob|bpr|brk|bsg|btn|bum|byusir|c4|cadc|cals|cam|can|car|cart|cat|cbmf|cdr|cdu|ce|ce1|cel|cft|cgm|che|cin|cip|ciph|cipt|cish|cism|cloe|clp|cmt|cmu|cmx|cncd|cnct|cp8|cpa|cpat|cpc|cpt|cr2|craw|crd|crg|crw|csv|ct|cut|cvp|cwg|d3d|dali|dbw|dcmp|dcpy|dcr|dd|degas|dicom|dkb|dol|doodle|dpx|drz|dsi|dta|dwg|dwg|ecc|efx|eidi|eif|emf|emz|epa|epi|eps|epsp|erf|esm|esmp|eyes|f96|face|fax|fbm|fcx|fff|fff|ffpg|fgs|fi|fit|fits|fli|fmag|fmap|fmf|fp2|fpg|fpr|fpt|fre|frm|frm2|fsh|fsy|ftf|fx3|fxs|g16|g3n|gaf|gbr|gcd|gem|geo|gfaray|gg|gicon|gig|gih|gm|gmf|god|gpat|gpb|grob|gun|hdri|hdru|hed|hf|hir|hpgl|hpi|hr|hru|hrz|hsi|hta|icb|icd|icl|icn|icns|ico|icon|iff|ifx|iim|iimg|ilab|im5|img|imgt|imi|imt|indd|info|ingr|ioca|ipg|ipl|ipl2|ipseq|iris|ish|iss|j6i|jbf|jbr|jig|jig2|jj|jls|jps|jtf|jxr|k25|k25b|kdc|kdc2|kfx|kntr|koa|kps|kqp|kro|kskn|lbm|lcel|lda|lff|lif|lsm|lss|lvp|lwi|m8|mac|mag|map|mbig|mdl|mef|mfrm|mgr|mh|miff|mil|mjpg|mkcf|mklg|mng|mon|mos|mph|mpo|mrc|mrf|mrw|msp|msx2|mtv|mtx|ncr|ncy|ncy|nef|neo|ngg|nifti|nist|nitf|nlm|nol|npm|nrw|nsr|oaz|ocp|of|ofx|ohir|oil|ols|orf|os2|otap|otb|p64|p7|pabx|palm|pam|pan|patps|pbm|pbt|pcl|pcp|pd|pdd|pds|pdx|pef|pegs|pfi|pfm|pfs|pgc|pgf|pgm|pi|pic|pict|pig|pixi|pixp|pld|pm|pm|pmg|pmp|pmsk|pnm|pp4|pp5|ppm|ppp|pps|ppt|prc|prf|prisms|prx|ps|psa|pseg|psf|psion3|psion5|psp|pspb|pspf|pspm|pspp|pspt|ptg|pwp|pxa|pxr|pzl|pzp|q0|qcad|qdv|qrt|qtif|rad|raf|ras|raw1|raw2|raw3|raw4|raw5|raw6|raw7|raw8|raw9|rawa|rawb|rawdvr|rawe|ray|rdc|rfa|rfax|ript|rix|rla|rlc2|rle|rp|rpm|rsb|rsrc|rw2|rwl|sar|sci|sct|sdg|sdt|sfax|sfw|sgi|sif|sir|sj1|skf|skn|skp|smp|soft|spc|spot|sps|spu|srf|srf2|srw|ssi|ssp|sst|st4|stad|star|stm|stw|stx|syj|synu|taac|tdi|tdim|teal|tg4|thmb|ti|til|tile|tim|tim2|tiny|tjp|tnl|trup|tsk|ttf|tub|txc|uni|upe4|upi|upst|uyvy|uyvyi|v|vda|vfx|vi|vicar|vid|vif|viff|vista|vit|vivid|vob|vort|vpb|wad|wal|wbc|wfx|winm|wmf|wmz|wpg|wrl|wzl|x3f|xar|xbm|xcf|xif|xim|xnf|xp0|xpm|xwd|xyz|yuv411|yuv422|yuv444|zbr|zmf|zxhob|zxscr|zxsna|zzrough", "png")
						Case 'Q'
							_Engine('_RedEngine')
						Case 'R'
							_Engine('_Godot')
						Case 'S'
							_Engine('_RPGMaker')
						Case 'T'
							_Engine('_RenPy')
						Case 'U'
							_Engine('_Unigene')
						Case 'V'
							_ChildGUI("DDS Header Generator", $tWidth & '|' & $tHight & '|' & $Format & '|' & $Offset, "2|4|8|12|16|24|32|48|64|96|128|256|384|512|768|1024|1536|2048|3072|4096|8192;2|4|8|12|16|24|32|48|64|96|128|256|384|512|768|1024|1536|2048|3072|4096|8192;DXT1|DXT3|DXT5|DX10|BC4U|BC5U|BC4S|BC5S;0|8|16|32|64", '512|512|DXT5|0')
						Case 'W'
							_ChildGUI("Atrac Headler Generator", $Frequency & '|' & $Channel & '|' & $AudioBitrate & '|' & $Format & '|' & $Offset, '8000|12000|16000|22050|24000|36000|44100|48000|96000|192000|384000;1|2;32|48|52|64|66|96|105|128|132|160|192|256|320|352;AT3|AT3Plus|AT9;0x0|0x10|0x20|0x30|0x40|0x50|0x60|0x70|0x80|0x90|0xA0|0xB0|0xC0|0xD0|0xE0|0xF0', '44100|2|132|AT3|0x0') 
						Case 'X'
							_ChildGUI("Wav Headler Generator", $Frequency & '|' & $Channel & '|' & $Bit & '|' & $Format, "8000|12000|16000|22050|24000|36000|44100|48000|96000|192000|384000;1|2|3|4|5|6|7|8;8|12|16|24|32|48|64|96|128;ADPCM|ALAW|ANTEX_ADPCME|APTX|ATRAC|AUDIOFILE_AF10|AUDIOFILE_AF36|BTV_DIGITAL|CANOPUS_ATRAC|CIRRUS|CONTROL_RES_CR10|CONTROL_RES_VQLPC|CREATIVE_ADPCM|CREATIVE_FASTSPEECH10|CREATIVE_FASTSPEECH8|CS2|CS_IMAADPCM|CU_CODEC|DF_G726|DF_GSM610|DIALOGIC_OKI_ADPCM|DIGIADPCM|DIGIFIX|DIGIREAL|DIGISTD|DIGITAL_G723|DOLBY_AC2|DOLBY_AC3_SPDIF|DRM|DSAT_DISPLAY|DSPGROUP_TRUESPEECH|DTS|DVI_ADPCM|DVM|ECHOSC1|ECHOSC3|ESPCM|ESST_AC3|FM_TOWNS_SND|G721_ADPCM|G722_ADPCM|G723_ADPCM|G726ADPCM|G726_ADPCM|G728_CELP|G729A|GSM610|IBM_CVSD|IEEE_FLOAT|ILINK_VC|IMA_ADPCM|IPI_HSX|IPI_RPELP|IRAT|ISIAUDIO|LH_CODEC|LRC|LUCENT_G723|MALDEN_PHONYTALK|MEDIASONIC_G723|MEDIASPACE_ADPCM|MEDIAVISION_ADPCM|MP3|MPEG|MSAUDIO1|MSG723|MSNAUDIO|MSRT24|MULAW|MVI_MVI2|NMS_VBXADPCM|NORRIS|OKI_ADPCM|OLIADPCM|OLICELP|OLIGSM|OLIOPR|OLISBC|ONLIVE|PAC|PACKED|PCM|PHILIPS_LPCBB|PROSODY_1612|PROSODY_8KBPS|QDESIGN_MUSIC|QUALCOMM_HALFRATE|QUALCOMM_PUREVOICE|QUARTERDECK|RAW_SPORT|RHETOREX_ADPCM|ROCKWELL_ADPCM|ROCKWELL_DIGITALK|RT24|SANYO_LD_ADPCM|SBC24|SIERRA_ADPCM|SIPROLAB_ACELP4800|SIPROLAB_ACELP8V3|SIPROLAB_ACEPLNET|SIPROLAB_G729|SIPROLAB_G729A|SIPROLAB_KELVIN|SOFTSOUND|SONARC|SONY_SCX|SOUNDSPACE_MUSICOMPRESS|TPC|TUBGSM|UHER_ADPCM|UNISYS_NAP_16K|UNISYS_NAP_ADPCM|UNISYS_NAP_ALAW|UNISYS_NAP_ULAW|UNKNOWN(0000)|UNKNOWN(FFFF)|VIVO_G723|VIVO_SIREN|VME_VMPCM|VOXWARE|VOXWARE_AC10|VOXWARE_AC16|VOXWARE_AC20|VOXWARE_AC8|VOXWARE_BYTE_ALIGNED|VOXWARE_RT24|VOXWARE_RT29|VOXWARE_RT29HW|VOXWARE_TQ40|VOXWARE_TQ60|VOXWARE_VR12|VOXWARE_VR18|VSELP|XEBEC|YAMAHA_ADPCM|ZYXEL_ADPCM", "44100|2|32|PCM")
						Case 'Y'
							SettingMenu()
					EndSwitch
				EndIf
			Next
			
		Case $iDeleteFull, $idButton[15]
			ClearFolder()
			
		Case $iChangeButton[2] to $iChangeButton[14]
			For $j = 2 to 14
				If $msg = $iChangeButton[$j] Then
					_ChangeButton($j)
				EndIf
			Next
			
		Case $iDeleteToTrash
			ClearFolder(True)
		Case $iFindBTN
			If $iGroupBy = 'Name' Then ControlTreeView($hGUI, "", $idTreeView_1, "Select", $tListT & '|' & StringLeft(GUICtrlRead($iFindMenu),1) &  '|' & GUICtrlRead($iFindMenu))
			If $iGroupBy = 'Year' Then ControlTreeView($hGUI, "", $idTreeView_1, "Select", $tListT & '|' & $iYearList[_ArraySearch($iListFind, GUICtrlRead($iFindMenu))] & '|' & GUICtrlRead($iFindMenu))
			If @error = 1 Then ControlTreeView($hGUI, "", $idTreeView_1, "Select", $tListT & '|0-9|' & GUICtrlRead($iFindMenu))
			If @error = 1 Then ControlTreeView($hGUI, "", $idTreeView_1, "Select", $tListT & '|Other|' & GUICtrlRead($iFindMenu))
			If @error = 1 Then ControlTreeView($hGUI, "", $idTreeView_1, "Select", $tListT & '|1980-1979|' & GUICtrlRead($iFindMenu))
			If @error = 1 Then ControlTreeView($hGUI, "", $idTreeView_1, "Select", $tListT & '|Unknown|' & GUICtrlRead($iFindMenu))
			If @error = 1 Then _MsgBox (0, '', GUICtrlRead($iFindMenu) & ' ' & $tNotFind)
		Case $iFavAdd
			FileWrite ($FavIni, GUICtrlRead($iFindMenu) & '|')
			GUICtrlSetData ($iFindMenu, GUICtrlRead($iFindMenu) & '|', "")
		Case $iFavDel
			$SetData = StringReplace (FileRead (@ScriptDir & '\data\favorites.ini'), GUICtrlRead($iFindMenu) & '|', '')
			FileClose ($FavIni)
			FileWrite (FileOpen($FavIni, 2), $SetData)
			_GUICtrlComboBox_ResetContent($iFindMenu)
			GUICtrlSetData($iFindMenu, FileRead (@ScriptDir & '\data\favorites.ini'), "")

		Case $iObserver;, $iInstallShield
			_QuickBMSRun($tAllSupp & "(*.exe;*.msi;*.msm;*.vp;*.big;*.sga;*.pst;*.bsp;*.gcf;*.vbsp;*.vpk;*.pak;*.xzp;*.wad;*.udf;*.iso;*.cat;*.pck;*.pbd;*.pbb;*.mpq;*.S2MA;*.SC2*;*.mpqe;*.hdr;*.cab;*.z;*.cache;*.nrg;*.bin;*.cue;*.isz;*.mdf;*.mds;*.eml;*.mht;*.mhtml;*.etc;*.mime;*.mim;*.tbb;*.big)|Blizzard MPQ (*.mpq;*.exe;*.S2MA;*.SC2Data;*.SC2*;*.mpqe)|MHTML Web" & $tArchive & "(*.mht;*.mhtml)|MIME Container (*.eml;*.etc;*.mime;*.mim)|" & $tDImage & " (*.iso;*.udf;*.nrg;*.bin;*.cue;*.isz;*.mdf;*.mds)|Install Shield (*.hdr;*.cab;*.z;*.exe)|PST " & $tFiles & " (*.pst)|Source Engine " & $tFiles & " (*.gcf;*.wad;*.pak;*.vpk;*.bsp;*.cache;*.vbsp;*.xzp)|Volition Pack V2 (*.vp)|Windows Installer (*.exe;*.msi;*.msm)|X-CAT (*.cat;*.pck;*.pbd;*.pbb)|MS Outlook databases (*.pst)|The Bat! databases (*.tbb)|Relic Games SGA\BIG " & $tFiles & " (*.sga;*.big)|Blizzard MPQ File (*.mpq;*.exe;*.S2MA;*.SC2Data;*.SC2Map;*.SC2Mod;*.SC2Assets;*.SC2Archive;*.mpqe)|", @ScriptDir & "\data\wcx\TotalObserver.wcx ")
		Case $iUnpack816
			_QuickBMSRun("Gamestudio WRS File (*.wrs)|", @ScriptDir & "\data\scripts\gamestudio.bms ")
		Case $iAsura
			_Engine('_Asura')
		Case $iChromeEngine
			_Engine('_Chrome')
		Case $iRedEngine
			_Engine('_RedEngine')
		Case $iReEngine
			_Engine('_ReEngine')
		Case $iAurora
			_Engine('_Aurora')
		Case $iFoxEngine
			_OtherPRG("FOX Engine files (*.dat;*.qar;*.fpk;*.pftxs;*.sbp;*.xml)|", "gzsTool\gzsTool.exe", ' ', '' )
		Case $iFPS_Creator
			_QuickBMSRun("imageblock.bin file (imageblock.bin)|", @ScriptDir & "\data\scripts\fps_creator_imageblock.bms  ", '')
		Case $iLithTech
			_Engine('_LithTech')
		Case $iFrostBite
			_Engine('_Frostbite')
		Case $iGameloft
			_QuickBMSRun("GLA File (*.gla)|", @ScriptDir & "\data\scripts\lz_sprites_gla.bms ")
		Case $iGlacier
			_Engine('_Glacier')
		Case $iHuneX
			_QuickBMSRun("", @ScriptDir & "\data\scripts\hunex.bms ")
		Case $iDTech
			idTech()
		Case $Infinity 
			_Engine('_Infinity')
		Case $iConv_3, $iSAU
			_OtherPRGExt('_SAU')
		Case $iMTFramework
			_Engine('_MTFramework')	
		Case $iPhyre
			_QuickBMSRun('Phyre Engine Files (*.phyre)|', @ScriptDir & "\data\scripts\PhyreEngine_PTexture2D_phyre.bms  ")
		Case $iPopCapPackAll
			_Engine('_PopCapPackAll')
		Case $iGameMaker
			_Engine('_GameMaker')
		Case $iGodot
			_Engine('_Godot')
		Case $iRPGMaker
			_Engine('_RPGMaker')
		Case $iConstruct
			_Engine('_Construct')
		Case $iRenPy
			_Engine('_RenPy')
		Case $iAnvil
			_Engine('_Anvil')
		Case $iShiVa
			_QuickBMSRun("Shiva Engine Files (S3DMain.smf;S3DMain.stk;S3DMain.ste)|", @ScriptDir & "\data\scripts\shiva.bms ")
		Case $iOpenSWF
			_Engine('_Flash')
		Case $iUnigenex
			_Engine('_Unigene')
		Case $iOpenXNA
			_QuickBMSRun("XNB Files (*.xnb)|", @ScriptDir & "\data\scripts\xnb.bms ")
			
		;Archives
		Case $iArchiveItem[2] To $iArchiveItem[$iArcCount]
			For $itemA = 1 to $iArcCount
				If $msg = $iArchiveItem[$itemA] Then 
					StringReplace($iArchiveItem[$itemA], 'FolderName', $sFolderName)
					$iArchCall = StringSplit($iArchiveArray[$itemA], '	')
					Switch $iArchCall[2]
						Case '_7Zip'
							_OtherPRG($iArchCall[3], '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip')
						Case '_OtherPRG'
							If GUICtrlRead($iReimport_Checkbox) = 1 Then
								If $iArchCall[7] = 'not' Then
									_MsgBox(0, $tMessage, $tNotSupport)
								Else
									$ArchiveName = _InputBox($tArchiveName, '', 'new_archive')
									If $ArchiveName = '' Then ContinueLoop
									Switch $iArchCall[11] ;TODO Проверить упаковку!
										Case '1'
											_OtherPRG ('', $iArchCall[4], $iArchCall[7] & $ArchiveName & $iArchCall[9], $iArchCall[8], $sFolderName, '', _Bool($iArchCall[11]))
										Case '2'
											_OtherPRG ('', $iArchCall[4], $iArchCall[7], $iArchCall[8] & $ArchiveName & $iArchCall[9], $sFolderName, '', _Bool($iArchCall[11]))
									EndSwitch
								EndIf
							Else
								_OtherPRG ($iArchCall[3], $iArchCall[4], $iArchCall[5], $iArchCall[6], $sFolderName, '', _Bool($iArchCall[8]))
							EndIf
						Case '_QickBMS'
							_QuickBMSRun($iArchCall[3], @ScriptDir & $iArchCall[4])
					EndSwitch
				EndIf
			Next
		
		Case $iISZconv
			$sFileName = FileOpenDialog($tSelectFile, " ","ISZ Disc Image(*.isz)|" & $tAllFile & " (*.*)", 1)
				If @error <> 1 Then
					_PathSplit($sFileName, $iDrive, $iDir, $iName, $iExp)
					_OtherPRG('', '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
					_OtherPRG('', '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFolderName & "\" & $iName & '.iso"')
					FileDelete($sFolderName & "\" & $iName & '.iso"')
				EndIf
				
		Case $iPSARC_lzma
			_OtherPRG('PlayStation 2 PSARC Archives (*.psarc)|', 'PSARC.exe ', ' extract --lzma ', '', $sFolderName, '')
		Case $iPSARC_zlib
			_OtherPRG('PlayStation 2 PSARC Archives (*.psarc)|', 'PSARC.exe ', ' extract --zlib ', '', $sFolderName, '')
		Case $iZLib
			_ChildGUI("ZLIB GUI", $Mode & '|' & $Offset, "Scan_ZLIB|Cool_scan_ZLIB|Extract_ZLIB|Extract_Deflate|Reimport_ZLIB;", "Extract_ZLIB|")
		Case $ilz4_decompress
			_OtherPRG('', 'lz4_decompress.exe ', ' ', $sFolderName & '\lz4_decompress.dat')
		Case $iWavSearch
			_QuickBMSRun('', @ScriptDir & "\data\scripts\wav_search.bms ")
		Case $iAutoSearch
			AutoSearch()
		Case $iArchiveScan
			_OtherPRG('', 'comtype_scan2.bat', ' ' & @ScriptDir & '\data\scripts\comtype_scan2.bms ', '"' & $sFolderName & '"', @ScriptDir & "\data")
		Case $iFileList
			$iFolderList = FileSelectFolder($tFileList, $iLastDir)
				If @error <> 1 Then _FileList($iFolderList, $sFolderName)
			
		Case $iFSBext
			_OtherPRG("FSB files (*.fsb)|", "fsbext.exe", ' -d "' & $sFolderName & '" ')
		Case $iToWAV
			_OtherPRG($tAllSupp & "(*.fsb;*.xwb;*.ms;*.mus;*.vag;*.xma;*.aif;*.asf;*.emt;*.cmp;*.dat;*.fss;*.kvs;*.bag;*.cxs;*.waf;*.msv;*.str;*.sab;*.vms;*.wp2;*.eam;*.wwb;*.rib;*.zsm;*.zss;*.mib;*.mih;audio.idx;*.mic;*.aps;*.snd;*.seg;*.snu;*.adp;.vag;*.vpk;*.waa;*.wac;*.wad;*.wam;*.wav;*.xa)|FSB Audio Package (*.fsb)|XWB Audio File (*.xwb)|MS File (*.ms)|MUS File (*.mus)|PS2\PSX VAG File (*.vag)|XMA Xbox360 Audio (*.xma)|AIF Audio File (*.aif)|ASF Audio File (*.asf)|25 to Life EMT File(*.emt)|Crime Life; Gang Wars (*.CMP)|DAT File (*.dat)|Dead to Rights 2 (*.FSS)|Dynasty Warriors 4 (*.KVS)|Emperor; Battle for Dune (*.BAG)|Eternal Sonata (*.CXS)|Ever 17; Out of Infinity (*.WAF)|Fight Club (*.MSV)|Hitman; Blood Money (*.STR)|Just Cause (*.SAB)|Knight Rider 2 (*.VMS)|London Racer (*.WP2)|Madden NFL 07-08 (*.EAM)|Made Man (*.WWB)|Manhunt (*.RIB)|Marvel; Ultimate Alliance (*.ZSM;*.ZSS)|MIB\MIH File (*.mib;*.mih)|Nox (audio.idx)|Rogue Trooper (*.MIC)|Shadow of Rome (*.APS)|SND File (*.snd)|SEG File (*.seg)|SNU Audio File (*.snu)|Tony Tough and the Night of Roasted Moths (*.ADP)|VAG\VPK File (.VAG;*.VPK)|WA* File (*.waa;*.wac;*.wad;*.wam)|WAV File (*.wav)|XA Audio File (*.xa)|", "towav.exe")
		Case $iConv_4
			_ChildGUI("NCONVERT GUI", $Format, "bmp|cur|dcx|dds|dib|dng|gif|jif|jpeg|pcd|pcx|pdf|png|psb|psd|raw|svg|tga|tiff|wbmp|--Other--|2bp|2d|3fr|411|a64|abmp|abr|abs|acc|ace|aces|acorn|adex|adt|afphoto|afx|ai|aim|aip|aipd|alias|ami|ani|anv|aphp|apx|arcib|arf|arn|art|artdir|arw|atk|att|aurora|avs|avw|az7|b16|b3d|bdr|bfli|bfx|bga|bias|bif|biorad|bip|bld|blp|bmc|bmg|bms|bmx|bob|bpr|brk|bsg|btn|bum|byusir|c4|cadc|cals|cam|can|car|cart|cat|cbmf|cdr|cdu|ce|ce1|cel|cft|cgm|che|cin|cip|ciph|cipt|cish|cism|cloe|clp|cmt|cmu|cmx|cncd|cnct|cp8|cpa|cpat|cpc|cpt|cr2|craw|crd|crg|crw|csv|ct|cut|cvp|cwg|d3d|dali|dbw|dcmp|dcpy|dcr|dd|degas|dicom|dkb|dol|doodle|dpx|drz|dsi|dta|dwg|dwg|ecc|efx|eidi|eif|emf|emz|epa|epi|eps|epsp|erf|esm|esmp|eyes|f96|face|fax|fbm|fcx|fff|fff|ffpg|fgs|fi|fit|fits|fli|fmag|fmap|fmf|fp2|fpg|fpr|fpt|fre|frm|frm2|fsh|fsy|ftf|fx3|fxs|g16|g3n|gaf|gbr|gcd|gem|geo|gfaray|gg|gicon|gig|gih|gm|gmf|god|gpat|gpb|grob|gun|hdri|hdru|hed|hf|hir|hpgl|hpi|hr|hru|hrz|hsi|hta|icb|icd|icl|icn|icns|ico|icon|iff|ifx|iim|iimg|ilab|im5|img|imgt|imi|imt|indd|info|ingr|ioca|ipg|ipl|ipl2|ipseq|iris|ish|iss|j6i|jbf|jbr|jig|jig2|jj|jls|jps|jtf|jxr|k25|k25b|kdc|kdc2|kfx|kntr|koa|kps|kqp|kro|kskn|lbm|lcel|lda|lff|lif|lsm|lss|lvp|lwi|m8|mac|mag|map|mbig|mdl|mef|mfrm|mgr|mh|miff|mil|mjpg|mkcf|mklg|mng|mon|mos|mph|mpo|mrc|mrf|mrw|msp|msx2|mtv|mtx|ncr|ncy|ncy|nef|neo|ngg|nifti|nist|nitf|nlm|nol|npm|nrw|nsr|oaz|ocp|of|ofx|ohir|oil|ols|orf|os2|otap|otb|p64|p7|pabx|palm|pam|pan|patps|pbm|pbt|pcl|pcp|pd|pdd|pds|pdx|pef|pegs|pfi|pfm|pfs|pgc|pgf|pgm|pi|pic|pict|pig|pixi|pixp|pld|pm|pm|pmg|pmp|pmsk|pnm|pp4|pp5|ppm|ppp|pps|ppt|prc|prf|prisms|prx|ps|psa|pseg|psf|psion3|psion5|psp|pspb|pspf|pspm|pspp|pspt|ptg|pwp|pxa|pxr|pzl|pzp|q0|qcad|qdv|qrt|qtif|rad|raf|ras|raw1|raw2|raw3|raw4|raw5|raw6|raw7|raw8|raw9|rawa|rawb|rawdvr|rawe|ray|rdc|rfa|rfax|ript|rix|rla|rlc2|rle|rp|rpm|rsb|rsrc|rw2|rwl|sar|sci|sct|sdg|sdt|sfax|sfw|sgi|sif|sir|sj1|skf|skn|skp|smp|soft|spc|spot|sps|spu|srf|srf2|srw|ssi|ssp|sst|st4|stad|star|stm|stw|stx|syj|synu|taac|tdi|tdim|teal|tg4|thmb|ti|til|tile|tim|tim2|tiny|tjp|tnl|trup|tsk|ttf|tub|txc|uni|upe4|upi|upst|uyvy|uyvyi|v|vda|vfx|vi|vicar|vid|vif|viff|vista|vit|vivid|vob|vort|vpb|wad|wal|wbc|wfx|winm|wmf|wmz|wpg|wrl|wzl|x3f|xar|xbm|xcf|xif|xim|xnf|xp0|xpm|xwd|xyz|yuv411|yuv422|yuv444|zbr|zmf|zxhob|zxscr|zxsna|zzrough", "png")
		Case $iConv_5
			_ChildGUI("Wwise Converter", $Mode & '|' & $Codebook, "WWISE_Unpacker|wwise2wav|wwise2vorbis;packed_codebooks_aoTuV_603.bin|packed_codebooks3.bin", "WWISE_Unpacker|packed_codebooks3.bin", "All supported (*.pck;*.bnk;*.afc;*.akpk*.wav;*wwise*;*.lwav;*.pcm;*.wem;*.03f;*.0b2*;*.ogg;*.oga)|")
		Case $iConv_6
			_ChildGUI("Wav Headler Generator", $Frequency & '|' & $Channel & '|' & $Bit & '|' & $Format, "8000|12000|16000|22050|24000|36000|44100|48000|96000|192000|384000;1|2|3|4|5|6|7|8;8|12|16|24|32|48|64|96|128;ADPCM|ALAW|ANTEX_ADPCME|APTX|ATRAC|AUDIOFILE_AF10|AUDIOFILE_AF36|BTV_DIGITAL|CANOPUS_ATRAC|CIRRUS|CONTROL_RES_CR10|CONTROL_RES_VQLPC|CREATIVE_ADPCM|CREATIVE_FASTSPEECH10|CREATIVE_FASTSPEECH8|CS2|CS_IMAADPCM|CU_CODEC|DF_G726|DF_GSM610|DIALOGIC_OKI_ADPCM|DIGIADPCM|DIGIFIX|DIGIREAL|DIGISTD|DIGITAL_G723|DOLBY_AC2|DOLBY_AC3_SPDIF|DRM|DSAT_DISPLAY|DSPGROUP_TRUESPEECH|DTS|DVI_ADPCM|DVM|ECHOSC1|ECHOSC3|ESPCM|ESST_AC3|FM_TOWNS_SND|G721_ADPCM|G722_ADPCM|G723_ADPCM|G726ADPCM|G726_ADPCM|G728_CELP|G729A|GSM610|IBM_CVSD|IEEE_FLOAT|ILINK_VC|IMA_ADPCM|IPI_HSX|IPI_RPELP|IRAT|ISIAUDIO|LH_CODEC|LRC|LUCENT_G723|MALDEN_PHONYTALK|MEDIASONIC_G723|MEDIASPACE_ADPCM|MEDIAVISION_ADPCM|MP3|MPEG|MSAUDIO1|MSG723|MSNAUDIO|MSRT24|MULAW|MVI_MVI2|NMS_VBXADPCM|NORRIS|OKI_ADPCM|OLIADPCM|OLICELP|OLIGSM|OLIOPR|OLISBC|ONLIVE|PAC|PACKED|PCM|PHILIPS_LPCBB|PROSODY_1612|PROSODY_8KBPS|QDESIGN_MUSIC|QUALCOMM_HALFRATE|QUALCOMM_PUREVOICE|QUARTERDECK|RAW_SPORT|RHETOREX_ADPCM|ROCKWELL_ADPCM|ROCKWELL_DIGITALK|RT24|SANYO_LD_ADPCM|SBC24|SIERRA_ADPCM|SIPROLAB_ACELP4800|SIPROLAB_ACELP8V3|SIPROLAB_ACEPLNET|SIPROLAB_G729|SIPROLAB_G729A|SIPROLAB_KELVIN|SOFTSOUND|SONARC|SONY_SCX|SOUNDSPACE_MUSICOMPRESS|TPC|TUBGSM|UHER_ADPCM|UNISYS_NAP_16K|UNISYS_NAP_ADPCM|UNISYS_NAP_ALAW|UNISYS_NAP_ULAW|UNKNOWN(0000)|UNKNOWN(FFFF)|VIVO_G723|VIVO_SIREN|VME_VMPCM|VOXWARE|VOXWARE_AC10|VOXWARE_AC16|VOXWARE_AC20|VOXWARE_AC8|VOXWARE_BYTE_ALIGNED|VOXWARE_RT24|VOXWARE_RT29|VOXWARE_RT29HW|VOXWARE_TQ40|VOXWARE_TQ60|VOXWARE_VR12|VOXWARE_VR18|VSELP|XEBEC|YAMAHA_ADPCM|ZYXEL_ADPCM", "44100|2|32|PCM")
		Case $iVGM
			_OtherPRGExt('_VGM')
		Case $iConv_10
			_ChildGUI("DDS Header Generator", $tWidth & '|' & $tHight & '|' & $Format & '|' & $Offset, "2|4|8|12|16|24|32|48|64|96|128|256|384|512|768|1024|1536|2048|3072|4096|8192;2|4|8|12|16|24|32|48|64|96|128|256|384|512|768|1024|1536|2048|3072|4096|8192;DXT1|DXT3|DXT5|DX10|BC4U|BC5U|BC4S|BC5S;0|8|16|32|64", '512|512|DXT5|0')
		Case $iConv_11
			_ChildGUI("Atrac Headler Generator", $Frequency & '|' & $Channel & '|' & $AudioBitrate & '|' & $Format & '|' & $Offset, '8000|12000|16000|22050|24000|36000|44100|48000|96000|192000|384000;1|2;32|48|52|64|66|96|105|128|132|160|192|256|320|352;AT3|AT3Plus|AT9;0x0|0x10|0x20|0x30|0x40|0x50|0x60|0x70|0x80|0x90|0xA0|0xB0|0xC0|0xD0|0xE0|0xF0', '44100|2|132|AT3|0x0') 
		Case $iConv_13
			_ChildGUI("PS Audio Converter", $Platform & '|' & $Mode, "PS2|PS3|PSP|PSVita|PS4;Atrac2WAV|WAV2Atrac", "PS3|Atrac2WAV", "Atrac audio file (*.vag;*.at3;*.at3p;*.at9;*.wav;*.genh;*.pcm)|")
		Case $iConv_14
			_ChildGUI("FFMPEG IMAGE", $Format, 'apng|bmp|dpx|gif|jpg|pcx|pgm|pix|png|ppm|sgi|tga|tiff|xbm|xwd', 'png') 
		Case $iConv_15
			_ChildGUI("FFMPEG AUDIO", $Frequency & '|' & $Channel & '|' & $AudioBitrate & '|' & $Format, '8000|12000|16000|22050|24000|32000|36000|44100|48000|96000|192000|384000;1|2|3|4|5|6|7|8;8k|12k|16k|20k|24k|32k|48k|64k|96k|112k|128k|160k|192k|256k|320k|448k|512k|768k|1M|2M;aac|ac3|flac|mp2|mp3|ogg|opus|ra|tta|wav|wma|wv', '44100|2|128k|mp3') 
		Case $iConv_16
			_ChildGUI("DDS Tools GUI Microsoft", $Format & '|' & $Platform, "R32G32B32A32_FLOAT|R32G32B32A32_UINT|R32G32B32A32_SINT|R32G32B32_FLOAT|R32G32B32_UINT|R32G32B32_SINT|R16G16B16A16_FLOAT|R16G16B16A16_UNORM|R16G16B16A16_UINT|R16G16B16A16_SNORM|R16G16B16A16_SINT|R32G32_FLOAT|R32G32_UINT|R32G32_SINT|R10G10B10A2_UNORM|R10G10B10A2_UINT|R11G11B10_FLOAT|R8G8B8A8_UNORM|R8G8B8A8_UNORM_SRGB|R8G8B8A8_UINT|R8G8B8A8_SNORM|R8G8B8A8_SINT|R16G16_FLOAT|R16G16_UNORM|R16G16_UINT|R16G16_SNORM|R16G16_SINT|R32_FLOAT|R32_UINT|R32_SINT|R8G8_UNORM|R8G8_UINT|R8G8_SNORM|R8G8_SINT|R16_FLOAT|R16_UNORM|R16_UINT|R16_SNORM|R16_SINT|R8_UNORM|R8_UINT|R8_SNORM|R8_SINT|A8_UNORM|R9G9B9E5_SHAREDEXP|R8G8_B8G8_UNORM|G8R8_G8B8_UNORM|BC1_UNORM|BC1_UNORM_SRGB|BC2_UNORM|BC2_UNORM_SRGB|BC3_UNORM|BC3_UNORM_SRGB|BC4_UNORM|BC4_SNORM|BC5_UNORM|BC5_SNORM|B5G6R5_UNORM|B5G5R5A1_UNORM|B8G8R8A8_UNORM|B8G8R8X8_UNORM|R10G10B10_XR_BIAS_A2_UNORM|B8G8R8A8_UNORM_SRGB|B8G8R8X8_UNORM_SRGB|BC6H_UF16|BC6H_SF16|BC7_UNORM|BC7_UNORM_SRGB|AYUV|Y410|Y416|YUY2|Y210|Y216|B4G4R4A4_UNORM;PC|XBox One", "BC3_UNORM|PC", 'Image File (*.png;*.jpg;*.dds;*.tga;*.jpeg)|') 
		Case $iConv_17
			_ChildGUI("DDS Tools GUI nVidia", $Format, "dxt1c|dxt1a|dxt3|dxt5|u1555|u4444|u565|u8888|u888|u555|p8c|p8a|p4c|p4a|a8|cxv8u8|v8u8|v16u16|A8L8|fp32x4|fp32|fp16x4|dxt5nm|g16r16|g16r16f", "dxt5", 'Image File (*.png;*.jpg;*.dds;*.tga;*.jpeg)|') 
		Case $iConv_18
			_ChildGUI("XWMA Tool GUI", $Frequency & '|' & $Format, '20000|32000|48000|64000|96000|160000|192000;wav|xwm', '48000|wav', 'Audio Files (*.wma;*xwm;*.wav)|') 
		Case $iConv_mp3
			_fileReaper(_mp3)
		Case $iMediaInfo
			$sFilePath = FileOpenDialog("", "", "All file(*.*)", 1)
				If @error <> 1 Then _Console(@ScriptDir & '\data\ffprobe.exe "' & $sFilePath & '"', '', @ScriptDir & '\data\')
		Case $iBink2avi
			ShellExecute (@ScriptDir & "\data\RADVideo\RADVideo64.exe", "", $sFolderName, "open")
		Case $iCubeMapCreator
			CubeMapCreator()
		Case $iIcoSplitter
			_QuickBMSRun("ICO Files (*.ico)|", @ScriptDir & "\data\scripts\ico_splitter.bms ")
			
		Case $iMenuItem[2] To $iMenuItem[$iLoop]
			For $item = 1 to $iLoop
				If $msg = $iMenuItem[$item] Then 
					$iFuncCall = StringSplit($iGameList[$item], '	')
					;0 = количество элементов в строке\массиве
					;1 = название игры
					;2 = год релиза
					;3 = функция для запуска
					;4 = список расширений, для WithArray - список файлов для копирования, для Unreal - код от архива в Unreal Engine 4, для TellTale - код игры, для RE Engine - список файлов
					;5 = для QuickBMS - название скрипта, для OtherPRG, WithArray и DosBox - название программы
					;6 и 7 = для аргументов командной строки до и после имени файла, для WithArray - 6 подпапка в выходной папке
					If $iFuncCall[0] > 5 Then
						$iFuncCall[6] = StringReplace($iFuncCall[6], 'FolderName', $sFolderName)
						$iFuncCall[7] = StringReplace($iFuncCall[7], 'FolderName', $sFolderName)
					EndIf
					Switch $iFuncCall[3]
						Case '_QuickBMS'
							_QuickBMSRun ($iFuncCall[4], @ScriptDir & $iFuncCall[5])
						Case '_Unreal', '_Unity', '_RPGMaker', '_Bethesda', '_Aurora', '_RedEngine', '_Chrome', '_idTech', '_CryEngine', '_Construct', '_MTFramework', '_Source', '_RenPy', '_GameMaker', '_Asura', '_Chromium', '_Unigene', '_Godot', '_Glacier', '_Infinity', '_LithTech', '_Anvil', '_Dunia', '_Flash'
							_Engine($iFuncCall[3])
						Case '_Unreal4', '_ReEngine', '_TellTale', '_Sen'
							_Engine($iFuncCall[3], '', $iFuncCall[4])
						Case '_Frostbite'
							Switch $iFuncCall[4]
								Case 1, '1'
									_Engine($iFuncCall[3], '', $iFuncCall[4])
								Case 2, '2', 3, '3'
									_Engine($iFuncCall[3], 'folder', $iFuncCall[4])
							EndSwitch
						Case '_OtherPRG'
							_OtherPRG($iFuncCall[4], $iFuncCall[5], $iFuncCall[6], $iFuncCall[7])
						Case '_DosBox'
							_DosBox($iFuncCall[4], $iFuncCall[5], $iFuncCall[6], $iFuncCall[7])
						Case '_WithArray'
							_WithArray($iFuncCall[1], $iFuncCall[4], $iFuncCall[5], $iFuncCall[6])
						Case '_SAU', '_VGM'
							_OtherPRGExt($iFuncCall[3])
						Case '_GAUP'
							_QuickBMSRun($iFuncCall[4], @ScriptDir &  "\data\wcx\gaup_pro.wcx ")
						Case '_ZIP'
							_OtherPRG($iFuncCall[4], '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip')
						Case '_CelTop'
							_Engine('_Bethesda', 'folder')
						Case '_Mor'
							_fileReaper(MorUnpacker, "Pathologic Files (*.vfs)|")
						Case '_OOAM'
							OOAM_Unpacker()
						Case '_ExoPlanet'
							_getFile('', "Exoplanet catalog (exoplanet.eu_catalog.csv)|")
								If @error = 1 then Return
								If $iFuncCall[4] = 'Celestia' Then CelestiaExo($file)
								If $iFuncCall[4] = 'SpaceEngine' Then SpaceEngineExo($file)
					EndSwitch
				EndIf
			Next
	   EndSwitch
	Until False
EndFunc
