Func SettingMenu()
	
Local $set_Gui = GUICreate($tOpenINI, 250, 220, -1, -1)
	If $iMenuColor <> 'Classic' then GUISetBkColor($iColor1)
	GUISetState(@SW_SHOW, $set_Gui)
	GUISetIcon (@ScriptDir & "\Data\ico\i.ico")
	
	$iLangLabel = GUICtrlCreateLabel($tLang,  10, 5, 100, 14)
	$LangList = StringReplace(_ArrayToString(_FileListToArray(@ScriptDir & '\data\local', '*.loc'), '|', 1), '.loc', '')
	Local $iLang = GUICtrlCreateCombo("", 10, 20, 230, 100)
	GUICtrlSetData(-1, $LangList, $sLanguage)
	
	$iEngineGroup = GUICtrlCreateGroup($tShowEngine, 5, 50, 130, 120)
	DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iEngineGroup), "wstr", 0, "wstr", 0)
	Local $iEngine1Lbl = GUICtrlCreateLabel("Unreal (" & _FileCountLines(@ScriptDir & '\game_list\unreal_list.csv')-1 & ")", 25, 68, 100)
	Local $iEngine1 = GUICtrlCreateCheckbox("", 10, 65, 15, 20)
	GUICtrlSetState(-1, $iUnrealBuild)
	Local $iEngine3Lbl = GUICtrlCreateLabel("Unity (" & _FileCountLines(@ScriptDir & '\game_list\unity_list.csv')-1 & ")", 25, 88, 100)
	Local $iEngine3 = GUICtrlCreateCheckbox("", 10, 85, 15, 20)
	GUICtrlSetState(-1, $iUnityBuild)
	Local $iEngine4Lbl = GUICtrlCreateLabel("RPG Maker (" & _FileCountLines(@ScriptDir & '\game_list\rpgmaker_list.csv')-1 & ")", 25, 108, 100)
	Local $iEngine4 = GUICtrlCreateCheckbox("", 10, 105, 15, 20)
	GUICtrlSetState(-1, $iRPGMBuild)
	Local $iEngine5Lbl = GUICtrlCreateLabel("Game Maker (" & _FileCountLines(@ScriptDir & '\game_list\gamemaker_list.csv')-1 & ")", 25, 128, 100)
	Local $iEngine5 = GUICtrlCreateCheckbox("", 10, 125, 15, 20)
	GUICtrlSetState(-1, $iGMBuild)
	Local $iEngine6Lbl = GUICtrlCreateLabel("RenPy (" & _FileCountLines(@ScriptDir & '\game_list\renpy_list.csv')-1 & ")", 25, 148, 100)
	Local $iEngine6 = GUICtrlCreateCheckbox("", 10, 145, 15, 20)
	GUICtrlSetState(-1, $iRenPyBuild)
		
	Local $iThemesLbl = GUICtrlCreateLabel($tUseThemes, 35, 173, 100)
	Local $iThemes = GUICtrlCreateCheckbox('', 20, 170, 15, 20)
	GUICtrlSetState(-1, $iUseThemes)
	Local $iOnLaodLbl = GUICtrlCreateLabel($tLoadProgress, 35, 193, 100)
	Local $iOnLaod = GUICtrlCreateCheckbox('', 20, 190, 15, 20)
		If $iPrOrSp = 'Progress' Then 
			$iCheck1 = 1
		Else
			$iCheck1 = 4
		EndIf
	GUICtrlSetState(-1, $iCheck1)
	
	$iGroupByGroup = GUICtrlCreateGroup($tGroupBy, 140, 50, 95, 60)
	DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iGroupByGroup), "wstr", 0, "wstr", 0)
	Local $iNameG = GUICtrlCreateRadio('', 150, 65, 15, 20)
	Local $iYearG = GUICtrlCreateRadio('', 150, 85, 15, 20)
	Local $iNameGLbl = GUICtrlCreateLabel($tName, 165, 68, 60)
	Local $iYearGLbl = GUICtrlCreateLabel($tYear, 165, 88, 60)
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
     0xCCFFCC, 0x66C850, 0x339966, 0x66CC99]
	 
	If GUICtrlRead($iThemes) = 1 Then
		$ThemList = StringReplace(_ArrayToString(_FileListToArray(@ScriptDir & '\data\themes', '*.ini'), '|', 1), '.ini', '')
		Local $Picker = GUICtrlCreateCombo("", 140, 113, 100, 25)
		If $ThemList = -1 Then $ThemList = ''
		GUICtrlSetData(-1, 'Classic|' & $ThemList, $iMenuColor)	
	ElseIf GUICtrlRead($iThemes) = 4 Then
		Local $Picker = _GUIColorPicker_Create('', 140, 110, 100, 25, $iColor1, BitOR($CP_FLAG_CHOOSERBUTTON, $CP_FLAG_DEFAULT, $CP_FLAG_ARROWSTYLE, $CP_FLAG_TIP), $iGamma, 4, 5, 1, '', 'More...')
		GUICtrlSetTip(-1, $tSelColor)
	EndIf
		
	Local $iBTNSet1 = GUICtrlCreateButton($tOutFolder, 140, 135, 100, 25)
	Local $iBTNSet2 = GUICtrlCreateButton($tCancel, 140, 160, 100, 25)
	Local $iBTNSet3 = GUICtrlCreateButton($tApply, 140, 185, 100, 25)
	
	If $iMenuColor <> 'Classic' Then
		GUICtrlSetColor($iEngine1Lbl, $iFontColor)
		GUICtrlSetColor($iEngine3Lbl, $iFontColor)
		GUICtrlSetColor($iEngine4Lbl, $iFontColor)
		GUICtrlSetColor($iEngine5Lbl, $iFontColor)
		GUICtrlSetColor($iEngine6Lbl, $iFontColor)
		GUICtrlSetColor($iOnLaodLbl, $iFontColor)
		GUICtrlSetColor($iThemesLbl, $iFontColor)
		GUICtrlSetColor($iLangLabel, $iFontColor)
		GUICtrlSetColor($iNameGLbl, $iFontColor)
		GUICtrlSetColor($iYearGLbl, $iFontColor)
		GUICtrlSetColor($iEngineGroup, $iFontColor)
		GUICtrlSetColor($iGroupByGroup, $iFontColor)
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
			Case $iNameGLbl, $iYearGLbl
				If BitAND(GUICtrlRead($iNameG) = 1, GUICtrlRead($iYearG) = 4) Then 
					GUICtrlSetState($iNameG, $GUI_UNCHECKED)
					GUICtrlSetState($iYearG, $GUI_CHECKED)
				ElseIf BitAND(GUICtrlRead($iNameG) = 4, GUICtrlRead($iYearG) = 1) Then 
					GUICtrlSetState($iNameG, $GUI_CHECKED)
					GUICtrlSetState($iYearG, $GUI_UNCHECKED)
				EndIf
			Case $iEngine1Lbl
				If GUICtrlRead($iEngine1) = 1 Then 
					GUICtrlSetState($iEngine1, $GUI_UNCHECKED)
				ElseIf GUICtrlRead($iEngine1) = 4 Then 
					GUICtrlSetState($iEngine1, $GUI_CHECKED)
				EndIf
			Case $iEngine3Lbl
				If GUICtrlRead($iEngine3) = 1 Then 
					GUICtrlSetState($iEngine3, $GUI_UNCHECKED)
				ElseIf GUICtrlRead($iEngine1) = 4 Then 
					GUICtrlSetState($iEngine3, $GUI_CHECKED)
				EndIf
			Case $iEngine4Lbl
				If GUICtrlRead($iEngine4) = 1 Then 
					GUICtrlSetState($iEngine4, $GUI_UNCHECKED)
				ElseIf GUICtrlRead($iEngine4) = 4 Then 
					GUICtrlSetState($iEngine4, $GUI_CHECKED)
				EndIf
			Case $iEngine5Lbl
				If GUICtrlRead($iEngine5) = 1 Then 
					GUICtrlSetState($iEngine5, $GUI_UNCHECKED)
				ElseIf GUICtrlRead($iEngine5) = 4 Then 
					GUICtrlSetState($iEngine5, $GUI_CHECKED)
				EndIf
			Case $iEngine6Lbl
				If GUICtrlRead($iEngine6) = 1 Then 
					GUICtrlSetState($iEngine6, $GUI_UNCHECKED)
				ElseIf GUICtrlRead($iEngine6) = 4 Then 
					GUICtrlSetState($iEngine6, $GUI_CHECKED)
				EndIf
			Case $iThemesLbl
				If GUICtrlRead($iThemes) = 1 Then 
					GUICtrlSetState($iThemes, $GUI_UNCHECKED)
				ElseIf GUICtrlRead($iThemes) = 4 Then 
					GUICtrlSetState($iThemes, $GUI_CHECKED)
				EndIf
			Case $iOnLaodLbl
				If GUICtrlRead($iOnLaod) = 1 Then 
					GUICtrlSetState($iOnLaod, $GUI_UNCHECKED)
				ElseIf GUICtrlRead($iOnLaod) = 4 Then 
					GUICtrlSetState($iOnLaod, $GUI_CHECKED)
				EndIf
		EndSwitch
	WEnd
EndFunc

Func _ChangeButton($j)
	
Local $but_Gui = GUICreate($tOpenINI, 250, 250, -1, -1)
	If $iMenuColor <> 'Classic' then GUISetBkColor($iColor1)
	GUISetState(@SW_SHOW, $but_Gui)
	GUISetIcon (@ScriptDir & "\Data\ico\i.ico")
	Local $arg1 = 0, $arg2 = 0, $btnArray = IniReadSection(@ScriptDir & '\unpacker.ini', 'Button')
		
	For $i = 2 To 25
		$setBTN[$i] = GUICtrlCreateLabel($abcArray[$i], $arg1, $arg2, 50, 50, $SS_CENTER+$SS_CENTERIMAGE)
		GUICtrlSetFont(-1, $iIconsArray[$i][0], 400, 0, "IconLib")
		GUICtrlSetTip(-1, $iIconsArray[$i][1])
		GUICtrlSetColor(-1, $iFontColor)
		$arg1 += 50
		If $arg1 = 250 Then
			$arg1 = 0
			$arg2 += 50
		EndIf
	Next
	
	$setBTN[26] = GUICtrlCreateLabel("@", $arg1, $arg2, 50, 50, $SS_CENTER+$SS_CENTERIMAGE)
		GUICtrlSetFont(-1, 40, 400, 0, "IconLib")
		GUICtrlSetTip(-1, $tCancel)
		GUICtrlSetColor(-1, $iFontColor)
		
		While 1
			_CursorMove($but_Gui)
			$msg2 = GUIGetMsg($but_Gui)
			Switch $msg2
				Case $GUI_EVENT_CLOSE, $setBTN[26]
					GUISetState(@SW_HIDE, $but_Gui)
						ExitLoop
				Case $setBTN[2] to $setBTN[25]
					For $i = 2 to 25
						If $msg2 = $setBTN[$i] Then 
							$btnName = $iIconsArray[_ArraySearch($abcArray, IniRead(@ScriptDir & '\unpacker.ini', 'Button', 'Button' & $j, $abcArray[$i]))][1]
							If _ArraySearch($btnArray, $abcArray[$i]) > -1 Then
								MsgBox(0, $tMessage, 'Кнопка "' & $iIconsArray[$i][1] & '" уже добавлена в быстрый доступ!')
							Else
								IniWrite(@ScriptDir & '\unpacker.ini', 'Button', 'Button' & $j, $abcArray[$i])
								GUICtrlSetData($idButton[$j], $abcArray[$i])
								GUICtrlSetFont($idButton[$j], $iIconsArray[$i][0], 400, 0, "IconLib")
								$btnArray[$j-1][1] = $abcArray[$i]
								MsgBox(0, $tMessage, 'Кнопка "' & $btnName & '" заменена на "' & $iIconsArray[$i][1] & '"')
							EndIf
						EndIf
					Next
			EndSwitch
		WEnd
EndFunc
