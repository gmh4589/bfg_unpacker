
Func QuickOpen($sFileName)
_PathSplit($sFileName, $iDrive, $iDir, $iName, $iExp)
Switch $iExp
;TODO: Добавить новые расширения
	Case ".pak" 
		QuickPAK($sFileName)
	Case ".dat"
		QuickDAT($sFileName)
	Case ".pkg"
		QuickPKG($sFileName)
	Case ".img"
		QuickIMG($sFileName)
	Case ".a2c", ".abg", ".abl", ".acm", ".adf", ".afs", ".age3scn", ".agg", ".ahm", ".al4", ".al8", ".ama", ".anm", '.Arch00', '.Arch01', '.Arch02', '.Arch03', '.Arch04', '.Arch05', ".ark", ".avix", ".awd", ".bag", ".bank1sbk", ".bar", ".bbk", ".bf", ".bfs", ".bgx", ".big", ".fat", ".bpa", ".bpk", ".bun", ".cat", ".ceg", ".clz", ".cmo", ".cmp", ".cob", ".cpr", ".ctm", ".cts", ".cud", ".idx", ".pal", ".dbc", ".dbs", ".ddt", ".dir", ".dirinfo", ".drs", ".dta", ".dua", ".dun", ".dx1", ".dx2", ".dx3", ".ebm", ".editor_data", ".elmares", ".emi", ".exp", ".ezd", ".far", ".ff", ".fpk", ".fra", ".frame", ".fsh", ".fuk", ".gdp", ".gea", ".gfx", ".glb", ".grl", ".grp", ".gsc", ".gtr", ".h2o", ".h4c", ".h4d", ".h4r", ".hak", ".his", ".hog", ".ifx", ".ins", ".iwi", ".jap", ".jaz", ".jdr", ".jsr", ".jtr", ".lbx", ".lgr", ".lgt", ".lmp", ".lod", ".lte", ".lud", ".lug", ".lut", ".lzc", ".map", ".md5", ".mdl", ".meg", ".mix", ".mjp", ".mjz", ".mod", ".msf", ".msk", ".mult", ".mus", ".nif", ".nmo", ".npk", ".pac", ".paq", ".pbo", ".pck", ".pcx", ".pff", ".poa", ".pod", ".prm", ".psk", ".psp", ".ptx", ".pvd", ".qar", ".qfs", ".r16", ".r24", ".r8", ".raw", ".act", ".sdt", ".res", ".rfd", ".rfh", ".rmp", ".rr", ".rs", ".rsb", ".rss", ".rts", ".s4m", ".sbf", ".sc3", ".sct", ".scx", ".sdf", ".sdt", ".sequence", ".sga", ".sh4", ".sks", ".sl", ".slf", ".slv", ".snd", ".spa", ".spk", ".spr", ".st3", ".stb", ".stg", ".str", ".sud", ".sue", ".swa", ".syb", ".syj", ".t24", ".tbf", ".tdu", ".ted", ".tf", ".thu", ".trc", ".twd", ".twt", ".txd", ".ucx", ".ugx", ".uka", ".ukx", ".unr", ".uvx", ".vdu", ".vid", ".viv", ".vmp", ".vol", ".vpp", ".vtf", ".whd", ".wd", ".wdt", ".wep", ".wtn", ".xcr", ".xfs", ".xmb", ".xpk", ".xti", ".xwb", ".pbd", ".rez"
		_QuickBMSRun('', @ScriptDir &  '\data\wcx\gaup_pro.wcx ', $sFileName)
	Case '.Arch06'
		_QuickBMSRun("", @ScriptDir & "\data\scripts\shadow_of_mordor.bms ", $sFileName)
	Case ".vfs"
		_fileReaper(MorUnpacker, "", $sFileName)
	Case ".pbb", ".mpq", ".S2MA", ".SC2", ".mpqe", ".hdr", ".cache", ".etc", ".mime", ".mim", ".tbb", ".msm", ".vp", ".pst", ".bsp", ".gcf", ".vbsp", ".vpk", ".xzp", ".udf", ".nrg", ".cue", ".isz", ".mdf", ".mds", ".eml", ".mht", ".mhtml"
		_QuickBMSRun('', @ScriptDir &  '\data\wcx\TotalObserver.wcx ', $sFileName)
	Case ".bdx", "box", ".brig", ".chr", ".cam", ".cc", ".df2", ".c", ".rm", ".4pp", ".epf", ".flx", ".gor", ".group", ".hrs", ".ilb", ".key", ".lbx", ".dbi", ".wdb", ".mul", ".nds", ".p00", ".p10", ".p99", ".tgw", ".tlb", ".uop", ".vsr", ".war", ".xua", ".xub", ".jun", ".maa", ".jus", ".fan" 
		_SAU($sFileName)
	Case ".zip", ".pk4", ".pk3", ".xap", ".7z", ".rar", ".tar", ".wim", ".gz", ".bz", ".gzip", ".bzip", ".gz2", ".bz2", ".lzma", ".iso", ".cab", ".xz", ".nob", ".txz", ".txtz", ".cpio", ".tbz", ".tbz2", ".tgz", ".tgz2", ".tpz", ".taz", ".z", ".lzh", ".lha", ".rpm", ".deb", ".lzm", ".arj", ".vhd", ".swm", ".dmg", ".hfs", ".xar", ".chm", ".squashfs", ".dll", ".ocx", ".cbz", ".cbr", ".cb7", ".cbt", ".cb7z", ".dgdat", ".obb", ".bza", ".docx", ".dotx", ".epub", ".fods", ".fodt", ".jar", ".odb", ".ods", ".odt", ".ots", ".ott", ".piz", ".potm", ".ppsx", ".pptx", ".xlsm", ".xlsx", ".xpi", ".gro", ".lp", ".apk", ".ipa", ".ipg", ".gadget", ".kfs", ".dazip", ".love", ".pgz", ".exe", ".msi", ".unitypackage", ".gog"
		GUICtrlSetData($iEdit, $tIFA & @CRLF, 1)
		_OtherPRG('', '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
	Case ".bin"
		QuickBIN($sFileName)
	Case ".u", ".upk", ".uax", ".umx", ".xxx", ".unr", ".utx", ".ugx", ".un2", ".upx", ".usa", ".usx", ".ut2", ".uvx", ".pcc"
		GUICtrlSetData($iEdit, $tIFFGO & " Unreal Engine" & @CRLF, 1)
		_Engine('_Unreal', $sFileName)
	Case ".rgssad", ".rgss3a", ".rgss2a", '.rpgmvp', '.rpgmvo', '.rpgmvm'
		GUICtrlSetData($iEdit, $tIFFGO & " RPG Maker" & @CRLF, 1)
		_Engine('_RPGMaker', $sFileName)
	Case ".toc", ".sb"
		GUICtrlSetData($iEdit, $tIFFGO & " FrostBite Engine" & @CRLF, 1)
		_Engine('_Frostbite', $sFileName)
	Case ".bsa", ".ba2", "*.esp", "*.esm", "*.esl", "*.esx", "*.pex"
		GUICtrlSetData($iEdit, $tIFFGB & " Bethesda Game Studio" & @CRLF, 1)
		_Engine('_Bethesda', $sFileName)
	Case ".csb", ".spb", ".rpack"
		GUICtrlSetData($iEdit, $tIFFGO & " Chrome Engine" & @CRLF, 1)
		_Engine('_Chrome', $sFileName)
	Case ".erf", ".bif", ".rim"
		GUICtrlSetData($iEdit, $tIFFGO & " Aurora Engine" & @CRLF, 1)
		_Engine('_Aurora', $sFileName)
	Case ".bundle"
		QuickBundle($sFileName)
	Case ".w3strings", ".w3speech", ".archive", ".w2strings", ".dzip"
		GUICtrlSetData($iEdit, $tIFFGO & " Red Engine" & @CRLF, 1)
		_Engine('_RedEngine', $sFileName)
	Case ".assets", '.resS'
		GUICtrlSetData($iEdit, $tIFFGO & " Unity Engine" & @CRLF, 1)
		_Engine('_Unity', $sFileName)
	Case ".resources", ".wad", ".index", ".streamed", ".bimage", ".idwav", ".mega2", ".ptr", ".pages", ".vmtr", "*.wl6", "*.msf", "*.xma", "*.xpr"
		GUICtrlSetData($iEdit, $tIFFGO & " idTech Engine" & @CRLF, 1)
		_Engine('_idTech', $sFileName)
	Case ".arc", ".sbgw"
		GUICtrlSetData($iEdit, $tIFFGO & "  MT Framework, " & $tSelHand & @CRLF, 1)
		_Engine('_MTFramework', $sFileName)
	Case ".bnk"
		GUICtrlSetData($iEdit, $tItsfile & " Wwise Audio Bank" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir & "\data\scripts\wwsise_bnk.bms ", $sFileName)
	Case ".db0", ".db1", ".db2", ".db3", ".db4", ".db5", ".db6", ".db7", ".db8", ".db9"
		GUICtrlSetData($iEdit, $tIFFGO & "  X-Ray Engine" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir &  '\data\wcx\stalker.wcx ', $sFileName)
	Case ".cmp" 
		$iOutputWindow = ShellExecuteWait(@ScriptDir & "\data\ddcmpa.exe /u """ & $sFileName &""" """ & $sFolderName & """", @ScriptDir & "\data\scripts\", "open")
	Case ".orc", ".ork" 
		$iOutputWindow = ShellExecuteWait(@ScriptDir & "\data\orkdec.exe """ & $sFileName &""" """ & $sFolderName & """", @ScriptDir & "\data\scripts\", "open")
	Case ".csc" 
		$iOutputWindow = ShellExecuteWait(@ScriptDir & "\data\scs_extractor """ & $sFileName &""" """ & $sFolderName & """", @ScriptDir & "\data\scripts\", "open")
	Case ".data", ".mini", ".wd2" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\asphyre.bms ", $sFileName)
	Case ".atd" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\ATD.bms ", $sFileName)
	Case ".atg", ".rcf" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\atg_core_cement.bms ", $sFileName)
	Case ".ara" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\batman_ara.bms ", $sFileName)
	Case ".rfa" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\battlefield_2_modern_combat.bms ", $sFileName)
	Case ".bcc" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\bcc_psp.bms ", $sFileName)
	Case ".bf" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\BF.bms ", $sFileName)
	Case ".bfp" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\BFP.bms ", $sFileName)
	Case ".bfg" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\bigfishgames81.bms ", $sFileName)
	Case ".bkf" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\bitsquid_streams.bms ", $sFileName)
	Case ".xbp" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\blitz_games_xbp.bms ", $sFileName)
	Case ".wfp" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\bloody_roar_3_wfp.bms ", $sFileName)
	Case ".rzb" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\blur_2rzb.bms ", $sFileName)
	Case ".box" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\BOX_LEMBOX.bms ", $sFileName)
	Case ".cfs" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\c9.bms ", $sFileName)
	Case ".zfs" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Call_To_Power_2_ZFS.bms ", $sFileName)
	Case ".car" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\CAR.bms ", $sFileName)
	Case ".pig" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\City_of_Heroes_PIG.bms ", $sFileName)
	Case ".azp" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Close_Combat_4_AZP.bms ", $sFileName)
	Case ".pix" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Close_Combat_4_PIX.bms ", $sFileName)
	Case ".cnt" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\CNT_HiddenAndDangerous.bms ", $sFileName)
	Case ".aes" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\coalesced_aes.bms ", $sFileName)
	Case ".bfl" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Colin_McRae_Rally_BFL.bms ", $sFileName)
	Case ".cpr" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\coyote_console.bms ", $sFileName)
	Case ".cgr" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\critical_damage.bms ", $sFileName)
	Case ".flx" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Crusader_No_Remorse_FLX.bms ", $sFileName)
	Case ".csa" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\CSA_GEEK.bms ", $sFileName)
	Case ".cxt" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\CXT_XFIR.bms ", $sFileName)
	Case ".dag" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\DAG_PKR3.bms ", $sFileName)
	Case ".zwp" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Dark_Reign_2_ZWP.bms ", $sFileName)
	Case ".dpk" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\darkeden.bms ", $sFileName)
	Case ".xcd" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\darkness_xcd.bms ", $sFileName)
	Case ".pwf" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Delta_Force_Landwarrior_PWF.bms ", $sFileName)
	Case ".far" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\djhero_far.bms ", $sFileName)
	Case ".dr" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\DR_ShowdownLegendsOfWrestling.bms ", $sFileName)
	Case ".drg" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\drg2sbg.bms ", $sFileName)
	Case ".dfl" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\driving_simulator.bms ", $sFileName)
	Case ".drs" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\DRS.bms ", $sFileName)
	Case ".gob" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\EA_Cricket_2004_GOB.bms ", $sFileName)
	Case ".fmf" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\ea_fmf.bms ", $sFileName)
	Case ".cub" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\enigmatis.bms ", $sFileName)
	Case ".m4b" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Escape_From_Monkey_Island_M4B.bms ", $sFileName)
	Case ".lgp" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Final_Fantasy_7_LGP.bms ", $sFileName)
	Case ".frm" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\frm_fonts.bms ", $sFileName)
	Case ".wrs" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\gamestudio.bms ", $sFileName)
	Case ".stk", ".itk" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\goblins.bms ", $sFileName)
	Case ".hal" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\HAL_APUK.bms ", $sFileName)
	Case ".dlz" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\heroes_phantasia_dlz.bms ", $sFileName)
	Case ".vce" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Homeworld_Cataclysm_VCE.bms ", $sFileName)
	Case ".mbx" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Hostile_Waters_MBX.bms ", $sFileName)
	Case ".mng" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Hostile_Waters_MNG.bms ", $sFileName)
	Case ".hpf" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\HPF_HMG.bms ", $sFileName)
	Case ".rsr" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Imperialism_II_RSR.bms ", $sFileName)
	Case ".sh" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\install4j.bms ", $sFileName)
	Case ".mpk" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\invizimals.bms ", $sFileName)
	Case ".arz" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\iron_lore_arz.bms ", $sFileName)
	Case ".shd" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\jane_angel_2.bms ", $sFileName)
	Case ".ssp" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\jason_storm_space.bms ", $sFileName)
	Case ".spf" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\jeanne_darc.bms ", $sFileName)
	Case ".sab" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\justcause2_sab.bms ", $sFileName)
	Case ".cps" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\kofxiii_cps.bms ", $sFileName)
	Case ".voc" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Lemmings_2_(VOC)_VOC.bms ", $sFileName)
	Case ".bmb" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\private_dancer_bmb.bms ", $sFileName)
	Case ".rkv" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\rkv.bms ", $sFileName)
	Case ".scs" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\scsgames.bms ", $sFileName)
	Case ".xnb" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\xnb.bms ", $sFileName)
	Case ".xma" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\xma2wav.bms ", $sFileName)
	Case ".tab" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\mad_max.bms """ & $sFileName &""" """ & $sFolderName & """", @ScriptDir & "\data\scripts\", "open")
	Case ".epc" 
		_QuickBMSRun('', @ScriptDir & "\data\scripts\doctor_who.bms ", $sFileName)
	Case ".mve", ".mov", ".mkv", ".flv", ".webm", ".mpg", ".mpeg", ".vob", ".ogv", ".ogm", ".divx", ".3gp", ".ts", ".dvr-ms", ".wmv", ".rm", ".m4v", ".mk3d", ".3g2", ".3gpp", ".3gp2", ".amv", ".xvid", ".f4v", ".m1v", ".m2v", ".vid", ".thp", ".flc", ".fli", ".flic", ".avi", ".pam", ".pmm", ".pss", ".pmf" 
		GUICtrlSetData($iEdit, $tIFV & @CRLF, 1)
		ShellExecuteWait(@ScriptDir & '\data\ffmpeg.exe ', ' -i ' & '"' & $sFileName & '" -vb 5M -vcodec hevc ' & '"' & $sFolderName & '\' & $iName & '.mkv"')
	Case ".rpa" 
		GUICtrlSetData($iEdit, $tIFFG & " RenPy Engine" & @CRLF, 1)
		_Engine('_RenPy', $sFileName)
	Case ".asr" 
		GUICtrlSetData($iEdit, $tIFFG & " Asura Engine" & @CRLF, 1)
		_Engine('_Asura', $sFileName)
	Case ".ung"
		GUICtrlSetData($iEdit, $tItsfile & " Unigene Engine" & @CRLF, 1) 
		_Engine('_Unigene', $sFileName)
	Case ".swf"
		GUICtrlSetData($iEdit, $tItsfile & " ShockWave Flash" & @CRLF, 1) 
		_Engine('_Flash', $sFileName)
	Case ".dz"
		_QuickBMSRun('', @ScriptDir & "\data\scripts\vector.bms ", $sFileName)
	Case ".class"
		GUICtrlSetData($iEdit, $tItsfile & " Java" & @CRLF, 1) 
		_QuickBMSRun('', @ScriptDir &  "\data\wcx\JavaClassUnpacker.wcx ", $sFileName)
	Case ".gca"
		GUICtrlSetData($iEdit, $tIFA & "  GCA" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir &  "\data\wcx\gca.wcx ", $sFileName)
	Case ".fb2"
		GUICtrlSetData($iEdit, $tIFEB & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir &  "\data\wcx\wcx_fb2.wcx ", $sFileName)
	Case ".ha"
		_QuickBMSRun('', @ScriptDir &  "\data\wcx\HA.wcx ", $sFileName)
	Case ".alz", ".egg", ".bh"
		GUICtrlSetData($iEdit, $tIFA & "  BlackHole" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir &  '\data\wcx\UnArkWCX.wcx ', $sFileName)
	Case ".hrp", ".hrip"
		GUICtrlSetData($iEdit, $tIFA & " Hrust" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir &  "\data\wcx\inhrust.wcx ", $sFileName)
	Case ".dgc", ".dgca"
		GUICtrlSetData($iEdit, $tIFA & " DGCA" & @CRLF, 1)
		$iOutputWindow = ShellExecuteWait(@ScriptDir & "\data\dgcac", "e """ & $sFileName & """ """ & $sFolderName & """", @ScriptDir & "\data\scripts\", "open")
	Case ".tiger" ;TODO - Something Wrong
		GUICtrlSetData($iEdit, $tIFFG & " Rise of Tomb Raider" & @CRLF, 1)
		$iOutputWindow = ShellExecuteWait(@ScriptDir & '\data\gibbed\Gibbed.TombRaider9.Unpack.exe', '"' & $sFileName & '" "' & $sFolderName & '"')
	Case ".blz"
		GUICtrlSetData($iEdit, $tIFA & " BLZ" & @CRLF, 1)
		$iOutputWindow = ShellExecuteWait(@ScriptDir & "\data\blzpack.exe ", " d """ & $sFileName &""" """ & $sFolderName & """", @ScriptDir & "\data\", "open")
	Case ".mnf"
		GUICtrlSetData($iEdit, $tIFFG & " Elder Scrolls Online" & @CRLF, 1)
		$iOutputWindow = ShellExecuteWait(@ScriptDir & "\data\EsoExtractData """ & $sFileName &""" """ & $sFolderName & """", @ScriptDir & "\data\", "open")
	Case ".arcv"
		_QuickBMSRun('', @ScriptDir & "\data\scripts\3ds_arcv.bms ", $sFileName)
	Case ".ctpk"
		_QuickBMSRun('', @ScriptDir & "\data\scripts\3ds_arcv.bms ", $sFileName)
	Case ".mse"
		_QuickBMSRun('', @ScriptDir & "\data\scripts\3dsmax.bms ", $sFileName)
	Case ".hgpk"
		_QuickBMSRun('', @ScriptDir & "\data\scripts\10minspacestrategy.bms ", $sFileName)
	Case ".mfd"
		_QuickBMSRun('', @ScriptDir & "\data\scripts\187_ride_or_die.bms ", $sFileName)
	Case ".packed"
		_QuickBMSRun('', @ScriptDir & "\data\scripts\Castlevania_LOS2.bms ", $sFileName)
	Case ".bdt", ".bhd5"
		GUICtrlSetData($iEdit, $tIFFG & " Dark Soul" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir & "\data\scripts\dark_soul.bms  ", $sFileName)
	Case ".dv2"
		GUICtrlSetData($iEdit, $tIFFG & " Divinity 2" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir & "\data\scripts\dv2.bms  ", $sFileName)
	Case ".hogg"
		GUICtrlSetData($iEdit, $tIFFG & " Newerwinter Online" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir & "\data\scripts\hogg.bms  ", $sFileName)
	Case ".lfs"
		GUICtrlSetData($iEdit, $tIFFG & " Resident Evil 4 HD Remastered" & @CRLF, 1)
		;TODO PASS
		;FileWriteLine($hFile, $sFolderName & "\YZ2tool.exe -x """ & $sFolderName & "\" & $iName & """")
	Case ".yz2", ".pack"
		GUICtrlSetData($iEdit, $tIFFG & " Resident Evil 4 HD Remastered" & @CRLF, 1)
		GUICtrlSetData($iEdit, $tSelHand & @CRLF, 1)
		;TODO PASS
		;FileWriteLine($hFile, $sFolderName & "\yzdec.exe """ & $sFolderName & "\" & $sFullFileName & """")
	Case ".rpkg"
		GUICtrlSetData($iEdit, $tIFFG & " Hitman(2016)" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir & "\data\scripts\hitman_2016.bms  ", $sFileName)
	Case ".forge"
		GUICtrlSetData($iEdit, $tIFFG & " Anvil Engine" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir & "\data\scripts\scimitar.bms  ", $sFileName)
	Case ".exo"
		_fileReaper(_mp3, "", $sFileName)
	Case ".phyre"
		GUICtrlSetData($iEdit, $tIFFG & " Phyre Engine" & @CRLF, 1)
		_QuickBMSRun('', @ScriptDir & "\data\scripts\PhyreEngine_PTexture2D_phyre.bms  ", $sFileName)
	Case Else
		_MsgBox(0, $tMessage, $tNotice3)
		GUICtrlSetData($iEdit, $tNotice3 & @CRLF, 1)
	EndSwitch
EndFunc

Func QuickPAK($sFileName); TODO: Дописать GAUP(Quake и др.)!!!	
	$iFind = _headRead($sFileName, 3, 16)
	Switch $iFind
		Case '0x504B03', '0x526172', '0x377ABC', '0x050000' ; Archives
			_OtherPRG('', '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
		Case '0x000000' ; UE4
			If StringInStr($iDir, 'Content\Paks') > 0 Then
				_QuickBMSRun('', @ScriptDir & "\data\scripts\unreal_tournament_4.bms ", $sFileName)
			Else
				_QuickBMSRun('', @ScriptDir & "\data\scripts\alonedark.bms ", $sFileName)
			EndIf
		Case '0x4B504B' ; RE
			_OtherPRG('', "retools\REtool.exe", ' -x ', '', $sFolderName, $sFileName)
		Case '0x37BD37' ; PopCapPack
			_QuickBMSRun('', @ScriptDir & "\data\scripts\7x7m.bms ", $sFileName)
		Case '0x61D119', '0xF93103', '0x30D302', '0xE9D580', '0xF308B1', '0x6A9C12', '0x7C32DF', '0x1ABBC3', '0xDA4F03', '0xE666A5', '0x2F4D03', '0xBC4B03', '0xFA9463', '0xF0E781', '0xFD8D02' ; Arx Fatalis
			_OtherPRG('', "afunpak.exe ", '', '', $sFolderName, $sFileName)
		Case '0x534250' ; Arcania
			_QuickBMSRun('', @ScriptDir & "\data\scripts\arcania.bms ", $sFileName)
		Case '0x010000' ; Risen
			_QuickBMSRun('', @ScriptDir & "\data\scripts\risen.bms ", $sFileName)
		Case '0x504143' ; 1242
			If $iName = 'data.000' Then _QuickBMSRun('', @ScriptDir & "\data\scripts\1242.bms ", $sFileName)
			If $iName = 'data' Then _QuickBMSRun('', @ScriptDir & "\data\scripts\azangara.bms ", $sFileName)
			If $iName = 'pak1' Then _QuickBMSRun('', @ScriptDir & "\data\scripts\Daikatana_PAK.bms ", $sFileName)
			If $iName = 'pak2' Then _QuickBMSRun('', @ScriptDir & "\data\scripts\Daikatana_PAK.bms ", $sFileName)
			If $iName  = 'pak3' Then _QuickBMSRun('', @ScriptDir & "\data\scripts\Daikatana_PAK.bms ", $sFileName)
		Case '0x4B4341' ; Full Mojo Rampage
			_QuickBMSRun('', @ScriptDir & "\data\scripts\full_mojo.bms ", $sFileName)
		Case '0x746F6E' ; Tongas - TODO: проверить
			_QuickBMSRun('', @ScriptDir & "\data\scripts\tongas.bms ", $sFileName)
		Case '0x50414B' 
			_QuickBMSRun('', @ScriptDir & "\data\scripts\alien_isolation.bms ", $sFileName)
		Case '0x544558'
			_OtherPRG('', 'sacred_tex_extractor.exe ', '', '', $sFolderName, $sFileName)
		Case '0x505343'
			_QuickBMSRun('', @ScriptDir & "\data\scripts\sega_classics.bms ", $sFileName)
		Case '0x000006'
			_QuickBMSRun('', @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
			
		Case Else
			If StringInStr($iDir, 'Necrovision') or StringInStr($iDir, 'Painkiller') Then
				_QuickBMSRun('', @ScriptDir & "\data\scripts\necrovision.bms ", $sFileName)
			ElseIf StringInStr($iDir, 'Sacred') Then
				_MsgBox(0, $tMessage, 'Оnly textures support for Sacred!')
			Else
				_MsgBox(0, $tMessage, $tNotice3)
				GUICtrlSetData($iEdit, $tNotice3 & @CRLF, 1)
				;_QuickBMSRun('', @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
			EndIf
	EndSwitch
EndFunc

Func QuickDAT($sFileName); TODO: Дописать!!!
Local $iFuncArray = [ _
	@ScriptDir & "\data\quickbms.exe " & @ScriptDir & "\data\7zip\Total7zip.wcx """ & $sFileName &""" """ & $sFolderName & "", _
	@ScriptDir & "\data\quickbms.exe " & @ScriptDir & "\data\wcx\gaup_pro.wcx """ & $sFileName &""" """ & $sFolderName & "", _
	@ScriptDir & "\data\quickbms.exe " & @ScriptDir & "\data\wcx\TotalObserver.wcx """ & $sFileName &""" """ & $sFolderName & "", _
	@ScriptDir & "\data\quickbms.exe " & @ScriptDir & "\data\scripts\agameengine.bms """ & $sFileName &""" """ & $sFolderName & ""]
	_ScriptCreate($iFuncArray)
EndFunc

Func QuickBIN($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickCache($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickWAD($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickEXE($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickDZIP($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickPGZ($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickARK($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickARC($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickBIF($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickBIG($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickFAT($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickKEY($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickVOL($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickPKG($sFileName); TODO: Дописать!!!
	Switch _headRead($sFileName, 3, 16)
		Case '0x504B03', '0x526172', '0x377ABC', '0x050000' ; Archives
			_OtherPRG('', '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
		Case 'TODO: Space Rangers, SWAT 4'
			_QuickBMSRun('', @ScriptDir & "\data\wcx\gaup_pro.wcx ", $sFileName)
		Case Else
			If StringInStr($sFileName, 'Trails of Cold Steel') Then
				_QuickBMSRun('', @ScriptDir & "\data\scripts\legend_of_heroes.bms ", $sFileName)
			EndIf
	EndSwitch
EndFunc

Func QuickSPK($sFileName); TODO: Дописать!!!
	;PASS Of Orcs and Men
EndFunc

Func QuickVID($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickVIV($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickMOD($sFileName); TODO: Дописать!!!
	;PASS
EndFunc

Func QuickBundle($sFileName); TODO: Дописать!!!
	Switch _headRead($sFileName, 3, 16)
		Case '0x504F54'
			_Engine('_RedEngine', $sFileName)
		Case Else
			_QuickBMSRun('', @ScriptDir & "\data\scripts\payday.bms ", $sFileName)
			
	EndSwitch
EndFunc

Func QuickSND($sFileName); TODO: Дописать!!!
	;PASS GAUP, Daggerfall
EndFunc

Func QiuckIMG($sFileName)
	Switch _headRead($sFileName, 3, 16)
		Case '0xFAB800'
			_OtherPRG('', '7zip\7z.exe ', ' x -o"' & $sFolderName & '" ', '', @ScriptDir & '\data\7zip', $sFileName)
			
	EndSwitch	
EndFunc
