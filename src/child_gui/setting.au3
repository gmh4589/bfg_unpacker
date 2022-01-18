Func SettingMenu()
	
Global $set_Gui = GUICreate($tOpenINI, 250, 220, -1, -1)
	If $iMenuColor <> 'Classic' then GUISetBkColor($iColor1)
	GUISetState(@SW_SHOW, $set_Gui)
	GUISetIcon (@ScriptDir & "\Data\ico\i.ico")
	$iShowMessageFlag = True
	
	$iLangLabel = GUICtrlCreateLabel($tLang,  10, 5, 100, 14)
	$LangList = StringReplace(_ArrayToString(_FileListToArray(@ScriptDir & '\data\local', '*.loc'), '|', 1), '.loc', '')
	Global $iLang = GUICtrlCreateCombo("", 10, 20, 230, 100)
	GUICtrlSetData(-1, $LangList, $sLanguage)
	
	$iEngineGroup = GUICtrlCreateGroup($tShowEngine, 5, 50, 130, 120)
	Global $iEngine1 = GUICtrlCreateCheckbox("Unreal (" & _FileCountLines(@ScriptDir & '\game_list\unreal_list.csv')-1 & ")", 10, 65, 120)
	GUICtrlSetState(-1, $iUnrealBuild)
	Global $iEngine3 = GUICtrlCreateCheckbox("Unity (" & _FileCountLines(@ScriptDir & '\game_list\unity_list.csv')-1 & ")", 10, 85, 120)
	GUICtrlSetState(-1, $iUnityBuild)
	Global $iEngine4 = GUICtrlCreateCheckbox("RPG Maker (" & _FileCountLines(@ScriptDir & '\game_list\rpgmaker_list.csv')-1 & ")", 10, 105, 120)
	GUICtrlSetState(-1, $iRPGMBuild)
	Global $iEngine5 = GUICtrlCreateCheckbox("Game Maker (" & _FileCountLines(@ScriptDir & '\game_list\gamemaker_list.csv')-1 & ")", 10, 125, 120)
	GUICtrlSetState(-1, $iGMBuild)
	Global $iEngine6 = GUICtrlCreateCheckbox("RenPy (" & _FileCountLines(@ScriptDir & '\game_list\renpy_list.csv')-1 & ")", 10, 145, 120)
	GUICtrlSetState(-1, $iRenPyBuild)
		
	Global $iThemes = GUICtrlCreateCheckbox($tUseThemes, 20, 170, 100)
	GUICtrlSetState(-1, $iUseThemes)
	Global $iOnLaod = GUICtrlCreateCheckbox($tLoadProgress, 20, 190, 100)
		If $iPrOrSp = 'Progress' Then 
			$iCheck1 = 1
		Else
			$iCheck1 = 4
		EndIf
	GUICtrlSetState(-1, $iCheck1)
	
	$iGroupByGroup = GUICtrlCreateGroup($tGroupBy, 140, 50, 95, 60)
	Global $iNameG = GUICtrlCreateRadio($tName, 150, 65, 80)
	Global $iYearG = GUICtrlCreateRadio($tYear, 150, 85, 80)
		If $iGroupBy = 'Name' Then
			GUICtrlSetState($iNameG, 1)
		ElseIf  $iGroupBy = 'Year' Then
			GUICtrlSetState($iYearG, 1)
		EndIf
		
	;TODO: Добавить адекватные цвета в гамму
	Local $iGamma = _
    [0xFFFFFF, 0x000000, 0xC0C0C0, 0x808080, _
     0xFF9900, 0xFFCC00, 0xFFCC99, 0xFFFF99, _
     0xFF99CC, 0xFF80FF, 0x993366, 0xD74060, _
     0xCCFFFF, 0x99CCFF, 0x33CCCC, 0x666699, _
     0xCCFFCC, 0x66C851, 0x339966, 0x66CC99]
	 
	If GUICtrlRead($iThemes) = 1 Then
		$ThemList = StringReplace(_ArrayToString(_FileListToArray(@ScriptDir & '\data\themes', '*.ini'), '|', 1), '.ini', '')
		Global $Picker = GUICtrlCreateCombo("", 140, 113, 100, 25)
		If $ThemList = -1 Then $ThemList = ''
		GUICtrlSetData(-1, 'Classic|' & $ThemList, $iMenuColor)	
	ElseIf GUICtrlRead($iThemes) = 4 Then
		Global $Picker = _GUIColorPicker_Create('', 140, 110, 100, 25, $iColor1, BitOR($CP_FLAG_CHOOSERBUTTON, $CP_FLAG_DEFAULT, $CP_FLAG_ARROWSTYLE, $CP_FLAG_TIP), $iGamma, 4, 5, 1, '', 'More...')
		GUICtrlSetTip(-1, $tSelColor)
	EndIf
		
	GLobal $iBTNSet1 = GUICtrlCreateButton($tOutFolder, 140, 135, 100, 25)
	GLobal $iBTNSet2 = GUICtrlCreateButton($tCancel, 140, 160, 100, 25)
	GLobal $iBTNSet3 = GUICtrlCreateButton($tApply, 140, 185, 100, 25)
	
	If $iMenuColor <> 'Classic' Then
		GUICtrlSetColor($iLangLabel, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iEngineGroup), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iEngineGroup, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iGroupByGroup), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iGroupByGroup, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iEngine1), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iEngine1, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iEngine3), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iEngine3, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iEngine4), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iEngine4, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iEngine5), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iEngine5, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iEngine6), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iEngine6, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iOnLaod), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iOnLaod, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iNameG), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iNameG, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iYearG), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iYearG, $iFontColor)
		DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iThemes), "wstr", 0, "wstr", 0)
		GUICtrlSetColor($iThemes, $iFontColor)
	EndIf

	While 1
		Switch GUIGetMsg($set_Gui)
			Case $GUI_EVENT_CLOSE, $iBTNSet2
				GUISetState(@SW_HIDE, $set_Gui)
					ExitLoop
			Case $iBTNSet1
				SelectFolder()
			Case $iBTNSet3
				If GUICtrlRead($iNameG) = 1 Then $iGroup = 'Name'
				If GUICtrlRead($iYearG) = 1 Then $iGroup = 'Year'
				If GUICtrlRead($iOnLaod) = 1 Then $oLoad = 'Progress'
				If GUICtrlRead($iOnLaod) = 4 Then $oLoad = 'Splash'
				$iUT = GUICtrlRead($Picker)
				If $iUT = '' Then $iUT = 'Classic'
				$iCLR = _GUIColorPicker_GetColor($Picker)
				If $iCLR < 0 Then $iCLR = 0xffffff
				IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Language', GUICtrlRead($iLang))
				IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Group', $iGroup)
				IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'OnLoad', $oLoad)
				IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'UseThemes', GUICtrlRead($iThemes))
				If GUICtrlRead($iThemes) = 4 Then IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Color', $iCLR)
				If GUICtrlRead($iThemes) = 1 Then IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Color', $iUT)
				IniWrite(@ScriptDir & '\unpacker.ini', 'Engine', 'Unreal', GUICtrlRead($iEngine1))
				IniWrite(@ScriptDir & '\unpacker.ini', 'Engine', 'Unity', GUICtrlRead($iEngine3))
				IniWrite(@ScriptDir & '\unpacker.ini', 'Engine', 'RPGMaker', GUICtrlRead($iEngine4))
				IniWrite(@ScriptDir & '\unpacker.ini', 'Engine', 'GameMaker', GUICtrlRead($iEngine5))
				IniWrite(@ScriptDir & '\unpacker.ini', 'Engine', 'RenPy', GUICtrlRead($iEngine6))
			Case $iThemes, $Picker
				$iUseThemes = GUICtrlRead($iThemes)
				If $iUseThemes = 4 Then $iMenuColor = _GUIColorPicker_GetColor($Picker)
				If $iUseThemes = 1 Then $iMenuColor = GUICtrlRead($Picker)
				_SetColor()
				GUISetState(@SW_HIDE, $set_Gui)
				Return(SettingMenu())
		EndSwitch
	WEnd
EndFunc

