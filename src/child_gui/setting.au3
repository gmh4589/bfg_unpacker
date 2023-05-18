Func SettingMenu()
	
	Local $set_Gui = GUICreate($tOpenINI, 250, 220, -1, -1)

	If BitOR($iMenuColor <> 'Classic', $iMenuColor = 0) then GUISetBkColor($iColor1)
	
	GUISetState(@SW_SHOW, $set_Gui)
	GUISetIcon(@ScriptDir & "\Data\ico\i.ico")
	
	$iLangLabel = GUICtrlCreateLabel($tLang,  10, 5, 100, 14)
	$LangList = StringReplace(_ArrayToString(_FileListToArray(@ScriptDir & '\data\local', '*.loc'), '|', 1), '.loc', '')
	Local $iLang = GUICtrlCreateCombo("", 10, 20, 230, 100)
	GUICtrlSetData(-1, $LangList, $sLanguage)
	
	$iEngineGroup = GUICtrlCreateGroup($tShowEngine, 5, 50, 130, 120)
	DllCall("UxTheme.dll", "int", "SetWindowTheme", "hwnd", GUICtrlGetHandle($iEngineGroup), "wstr", 0, "wstr", 0)
	Local $iEngine1Lbl = GUICtrlCreateLabel("Unreal(" & _FileCountLines(@ScriptDir & '\game_list\unreal_list.csv')-1 & ")", 25, 68, 100)
	Local $iEngine1 = GUICtrlCreateCheckbox("", 10, 65, 15, 20)
	GUICtrlSetState(-1, $iUnrealBuild)
	Local $iEngine3Lbl = GUICtrlCreateLabel("Unity(" & _FileCountLines(@ScriptDir & '\game_list\unity_list.csv')-1 & ")", 25, 88, 100)
	Local $iEngine3 = GUICtrlCreateCheckbox("", 10, 85, 15, 20)
	GUICtrlSetState(-1, $iUnityBuild)
	Local $iEngine4Lbl = GUICtrlCreateLabel("RPG Maker(" & _FileCountLines(@ScriptDir & '\game_list\rpgmaker_list.csv')-1 & ")", 25, 108, 100)
	Local $iEngine4 = GUICtrlCreateCheckbox("", 10, 105, 15, 20)
	GUICtrlSetState(-1, $iRPGMBuild)
	Local $iEngine5Lbl = GUICtrlCreateLabel("Game Maker(" & _FileCountLines(@ScriptDir & '\game_list\gamemaker_list.csv')-1 & ")", 25, 128, 100)
	Local $iEngine5 = GUICtrlCreateCheckbox("", 10, 125, 15, 20)
	GUICtrlSetState(-1, $iGMBuild)
	Local $iEngine6Lbl = GUICtrlCreateLabel("RenPy(" & _FileCountLines(@ScriptDir & '\game_list\renpy_list.csv')-1 & ")", 25, 148, 100)
	Local $iEngine6 = GUICtrlCreateCheckbox("", 10, 145, 15, 20)
	GUICtrlSetState(-1, $iRenPyBuild)
	
	Local $iThemesLbl = GUICtrlCreateLabel($tUseThemes, 35, 173, 100)
	Local $iThemes = GUICtrlCreateCheckbox('', 20, 170, 15, 20)
	GUICtrlSetState(-1, $iUseThemes)
	Local $iOnLaodLbl = GUICtrlCreateLabel($tLoadProgress, 35, 193, 100)
	Local $iOnLaod = GUICtrlCreateCheckbox('', 20, 190, 15, 20)
	Local $iRunAsAdm = False
	
	RegRead("HKEY_CLASSES_ROOT\*\shell\BFGUnp\command", "")
	
	If Not @error Then 
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

	Local $iGamma = _
		[0xFFFFFF, 0x000000, 0x303030, 0x808080, 0xC0C0C0, _
		 0xFF9900, 0xFFCC00, 0xFFCC99, 0xFFFF99, 0xA69E40, _
		 0xFF99CC, 0xFF80FF, 0x993366, 0xD74060, 0x821E55, _
		 0xCCFFFF, 0x99CCFF, 0x33CCCC, 0x666699, 0x1E5A82, _
		 0xCCFFCC, 0x66C850, 0x339966, 0x66CC99, 0x00BE32]
	 
	If GUICtrlRead($iThemes) = 1 Then
		$ThemList = StringReplace(_ArrayToString(_FileListToArray(@ScriptDir & '\data\themes', '*.ini'), '|', 1), '.ini', '')
		Local $Picker = GUICtrlCreateCombo("", 140, 113, 100, 25)
		
		If $ThemList = -1 Then $ThemList = ''
		
		GUICtrlSetData(-1, 'Classic|' & $ThemList, $iMenuColor)	
		
	ElseIf GUICtrlRead($iThemes) = 4 Then
		Local $Picker = _GUIColorPicker_Create('', 140, 110, 100, 25, $iColor1, _
			BitOR($CP_FLAG_CHOOSERBUTTON, $CP_FLAG_DEFAULT, $CP_FLAG_ARROWSTYLE, $CP_FLAG_TIP), $iGamma, 5, 5, 1, '', 'More...')
			
		GUICtrlSetTip(-1, $tSelColor)
	EndIf
		
	Local $iBTNSet1 = GUICtrlCreateButton($tOutFolder, 140, 135, 100, 25)
	Local $iBTNSet2 = GUICtrlCreateButton($tCancel, 140, 160, 100, 25)
	Local $iBTNSet3 = GUICtrlCreateButton($tApply, 140, 185, 100, 25)
	
	If BitOR($iMenuColor <> 'Classic', $iMenuColor = 0) Then
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
		GUICtrlSetBkColor($iLang, $iColor1)
		GUICtrlSetColor($iLang, $iFontColor)
		If GUICtrlRead($iThemes) = 1 Then GUICtrlSetBkColor($Picker, $iColor1)
		If GUICtrlRead($iThemes) = 1 Then GUICtrlSetColor($Picker, $iFontColor)
	EndIf

	While 1
		$set_msg = GUIGetMsg($set_Gui)
		Switch $set_msg
			Case $GUI_EVENT_CLOSE, $iBTNSet2
				GUISetState(@SW_HIDE, $set_Gui)
				GUIDelete($set_Gui)
					ExitLoop
			Case $iBTNSet1
				SelectFolder()
			Case $iBTNSet3
				If GUICtrlRead($iNameG) = 1 Then $iGroup = 'Name'
				If GUICtrlRead($iYearG) = 1 Then $iGroup = 'Year'
				$iUT = GUICtrlRead($Picker)
				If $iUT = '' Then $iUT = 'Classic'
				$iCLR = _GUIColorPicker_GetColor($Picker)
				If $iCLR < 0 Then $iCLR = 0xffffff
				
				If GUICtrlRead($iOnLaod) = 1 Then
					RegWrite("HKEY_CLASSES_ROOT\*\shell\BFGUnp", "", "REG_SZ", $tREG)
					RegWrite("HKEY_CLASSES_ROOT\*\shell\BFGUnp", "Icon", "REG_SZ", @ScriptDir & '\data\ico\i.ico, 0')
					RegWrite("HKEY_CLASSES_ROOT\*\shell\BFGUnp\command", "", "REG_SZ", '"C:\Users\40pja\AppData\Roaming\BFGUnpacker\BFGUnpacker.exe" "%1"')
				Else
					RegDelete("HKEY_CLASSES_ROOT\*\shell\BFGUnp")
				EndIf
				
				If @error and $iRunAsAdm Then _MsgBox(0, $tMessage, $tRunAsAdm)
				
				IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Language', GUICtrlRead($iLang))
				IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Group', $iGroup)
				IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'UseThemes', GUICtrlRead($iThemes))
				If GUICtrlRead($iThemes) = 4 Then IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Color', $iCLR)
				If GUICtrlRead($iThemes) = 1 Then IniWrite(@ScriptDir & '\unpacker.ini', 'Main', 'Color', $iUT)
				IniWrite(@ScriptDir & '\unpacker.ini', 'Engine', 'Unreal', GUICtrlRead($iEngine1))
				IniWrite(@ScriptDir & '\unpacker.ini', 'Engine', 'Unity', GUICtrlRead($iEngine3))
				IniWrite(@ScriptDir & '\unpacker.ini', 'Engine', 'RPGMaker', GUICtrlRead($iEngine4))
				IniWrite(@ScriptDir & '\unpacker.ini', 'Engine', 'GameMaker', GUICtrlRead($iEngine5))
				IniWrite(@ScriptDir & '\unpacker.ini', 'Engine', 'RenPy', GUICtrlRead($iEngine6))
				
				$iUnrealBuild = IniRead(@ScriptDir & '\unpacker.ini', 'Engine', 'Unreal', 4)
				$iUnityBuild = IniRead(@ScriptDir & '\unpacker.ini', 'Engine', 'Unity', 4)
				$iGMBuild = IniRead(@ScriptDir & '\unpacker.ini', 'Engine', 'GameMaker', 4)
				$iRPGMBuild = IniRead(@ScriptDir & '\unpacker.ini', 'Engine', 'RPGMaker', 4)
				$iRenPyBuild = IniRead(@ScriptDir & '\unpacker.ini', 'Engine', 'RenPy', 4)
				$iGroupBy = IniRead(@ScriptDir & '\unpacker.ini', 'Main', 'Group', 'Name')
				$iUseThemes = IniRead(@ScriptDir & '\unpacker.ini', 'Main', 'UseThemes', 4)
				$iMenuColor = IniRead(@ScriptDir & '\unpacker.ini', 'Main', 'Color', '0x000000')
				$iPrOrSp = IniRead(@ScriptDir & '\unpacker.ini', 'Main', 'OnLoad', 'Progress')
				
			Case $iThemes, $Picker, $iThemesLbl
				If $set_msg = $iThemesLbl Then GUICtrlSetState($iThemes, _Checker($iThemes))
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
				GUICtrlSetState($iEngine1, _Checker($iEngine1))
				
			Case $iEngine3Lbl
				GUICtrlSetState($iEngine3, _Checker($iEngine3))
				
			Case $iEngine4Lbl
				GUICtrlSetState($iEngine4, _Checker($iEngine4))
				
			Case $iEngine5Lbl
				GUICtrlSetState($iEngine5, _Checker($iEngine5))
				
			Case $iEngine6Lbl
				GUICtrlSetState($iEngine6, _Checker($iEngine6))
				
			Case $iOnLaodLbl
				GUICtrlSetState($iOnLaod, _Checker($iOnLaod))
				$iRunAsAdm = True
				
			Case $iOnLaod
				$iRunAsAdm = True
		EndSwitch
	WEnd
EndFunc

Func _Checker($checkboxID)

	If GUICtrlRead($checkboxID) = 1 Then 
		Return($GUI_UNCHECKED)
	ElseIf GUICtrlRead($checkboxID) = 4 Then 
		Return($GUI_CHECKED)
	EndIf
EndFunc

Func _ChangeButton($jBTN)
	Local $but_Gui = GUICreate($tOpenINI, 250, 250, -1, -1)
	If $iMenuColor <> 'Classic' then GUISetBkColor($iColor1)
	GUISetState(@SW_SHOW, $but_Gui)
	GUISetIcon(@ScriptDir & "\Data\ico\i.ico")
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
				GUIDelete($but_Gui)
					ExitLoop
			Case $setBTN[2] to $setBTN[25]
			
				For $i = 2 to 25
				
					If $msg2 = $setBTN[$i] Then 
						$btnName = $iIconsArray[_ArraySearch($abcArray, IniRead(@ScriptDir & '\unpacker.ini', 'Button', 'Button' & $jBTN, $abcArray[$jBTN]))][1]
						
						If _ArraySearch($btnArray, $abcArray[$i]) > -1 Then
							_MsgBox(0, $tMessage, $tBTN & $iIconsArray[$i][1] & $tBTN1) ;TODO!!!
						Else
							IniWrite(@ScriptDir & '\unpacker.ini', 'Button', 'Button' & $jBTN, $abcArray[$i])
							GUICtrlSetData($idButton[$jBTN], $abcArray[$i])
							GUICtrlSetFont($idButton[$jBTN], $iIconsArray[$i][0], 400, 0, "IconLib")
							GUICtrlSetTip($idButton[$jBTN], $iIconsArray[$i][1])
							$btnArray[$jBTN-1][1] = $abcArray[$i]
							_MsgBox(0, $tMessage, $tBTN & $btnName & $tBTN2 & $iIconsArray[$i][1] & '"')  ;TODO!!!
						EndIf
					EndIf
				Next
		EndSwitch
	WEnd
EndFunc
