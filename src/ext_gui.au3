Global $mButton[4], $exitBTN, $okButton, $cancelButton, $OpenFolderBTN, $OpenFileBTN

Func _CursorMove($iGuiID, $c1 = $iColor1, $c2 = $iColor2)
	$iCursorPos = GUIGetCursorInfo($iGuiID)
	
	If $iCursorPos[4] Then
		Switch $iCursorPos[4]
			Case $iAll_Checkbox, $iFindBTN, $iFavAdd, $iFavDel, $idButton[1] to $idButton[15], $setBTN[2] to $setBTN[26], $mButton[1] to $mButton[3], $exitBTN, $okButton, $cancelButton, $OpenFolderBTN, $OpenFileBTN
				If $iMouseMove <> -1 Then
					If $iMouseMove <> $iCursorPos[4] Then
						GUICtrlSetBkColor($iMouseMove, $c1)
					EndIf
				EndIf
				If $iMouseMove <> $iCursorPos[4] Then
					$iMouseMove = $iCursorPos[4]
					GUICtrlSetBkColor($iMouseMove, $c2)
				EndIf
			Case Else
				If $iMouseMove <> -1 Then
					GUICtrlSetBkColor($iMouseMove, $c1)
					$iMouseMove = -1
				EndIf
		EndSwitch
	EndIf
EndFunc

Func _BarCreate($percent, $txt = "Test", $txt2 = 'Test', $W = 250, $H = 90, $iSize = 45, $iShowClose = False, $iColor = '0xff' & StringTrimLeft($iColor2, 2), $iGuiColor = $iColor1, $fColor = $iFontColor)

	If $iProgressFlagStart = True Then
		$progressGUI = GUICreate('', $W, $H, -1, -1,  $WS_POPUP + $WS_BORDER, -1, $hGUI)
		GUISetIcon (@ScriptDir & "\Data\ico\i.ico")
		GUISetState()
		GUISetBkColor($iGuiColor)
		$Label = GUICtrlCreateLabel ('', 15, 5, $W - 30, 20)
		GUICtrlSetColor (-1, $fColor)
		$Label2 = GUICtrlCreateLabel ('', 15, $iSize + 30, $W - 30, $H - ($iSize + 30))
		GUICtrlSetColor (-1, $fColor)
		$exitBTN = GUICtrlCreateLabel ('', $W - 15, 0, 15, 15, $SS_CENTER+$SS_CENTERIMAGE)
		GUICtrlSetColor ($exitBTN, $fColor)
		GUICtrlSetFont($exitBTN, 15, 400, 0, "IconLib")
		If $iShowClose Then GUICtrlSetData($exitBTN, '@')
		$iProgressFlagStart = False
	EndIf

	_CursorMove($progressGUI)
	
	If $percent >= 0 Then
		$hGraphic = _GDIPlus_GraphicsCreateFromHWND ($progressGUI)
		$hPen = _GDIPlus_PenCreate ($iColor, $iSize, 2)
		If $percent >= 100 Then $percent = 100
		$long = $percent*($W/100)-10 < 10 ? 10 : $percent*($W/100)-10
		
		_GDIPlus_GraphicsDrawLine ($hGraphic, 10, $iSize/2+25, $long, $iSize/2+25, $hPen)
	EndIf
	
	GUICtrlSetData($Label, $txt)
	GUICtrlSetData($Label2, $txt2)
EndFunc   

Func _BarOff()
	GUISetState(@SW_HIDE, $progressGUI)	
	GUIDelete($progressGUI)
	$iProgressFlagStart = True
EndFunc

Func _MsgBox($flag, $title, $text, $c1 = $iColor2, $c2 = $iColor1, $fcolor = $iFontColor)

	Local $H = 150, $W = 250, $r1 = 0, $r2 = 0, $r3 = 0
	Local $sz = _StringSize($text, 9, 400, 0, "Arial", 285)
	
	If @error <> 1 Then
		$H = $sz[3] < 30 ? 30 : $sz[3]
		$W = $sz[2] < 150 ? 150 : $sz[2]
	EndIf
	
	$MsgGUI = GUICreate($title, $W + 15, $H + 80, -1, -1, $WS_POPUP+$WS_BORDER)
	GUISetIcon (@ScriptDir & "\Data\ico\i.ico")
	GUISetBkColor($c2, $MsgGUI)
	GUICtrlCreateLabel(StringUpper($title), 10, 10, 285, 30, $SS_CENTERIMAGE, $GUI_WS_EX_PARENTDRAG)
	GUICtrlSetColor(-1, $fcolor)
	GUICtrlCreateLabel($text, 10, 50, $W, $H, -1, $GUI_WS_EX_PARENTDRAG)
	GUICtrlSetColor(-1, $fcolor)

	If $flag = 0 Then	
		$mButton[1] = GUICtrlCreateLabel('OK', $W - 65, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[2] = GUICtrlCreateLabel('', 1000, 1000)
		$mButton[3] = GUICtrlCreateLabel('', 1000, 1000)
		$r1 = 1

	ElseIf $flag = 1 Then
		$mButton[1] = GUICtrlCreateLabel('OK', $W - 65, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[2] = GUICtrlCreateLabel(StringUpper($tcancel), $W - 145, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[3] = GUICtrlCreateLabel('', 1000, 1000)
		$r1 = 1
		$r2 = 2

	ElseIf $flag = 2 Then
		$mButton[1] = GUICtrlCreateLabel(StringUpper($tabort), $W - 65, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[2] = GUICtrlCreateLabel(StringUpper($tretry), $W - 145, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[3] = GUICtrlCreateLabel(StringUpper($tignore), $W - 225, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$r1 = 3
		$r2 = 4
		$r3 = 5

	ElseIf $flag = 3 Then
		$mButton[1] = GUICtrlCreateLabel(StringUpper($tno), $W - 65, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[2] = GUICtrlCreateLabel(StringUpper($tyes), $W - 145, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[3] = GUICtrlCreateLabel(StringUpper($tcancel), $W - 225, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$r1 = 7
		$r2 = 6
		$r3 = 2

	ElseIf $flag = 4 Then
		$mButton[1] = GUICtrlCreateLabel(StringUpper($tno), $W - 65, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[2] = GUICtrlCreateLabel(StringUpper($tyes), $W - 145, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[3] = GUICtrlCreateLabel('', 1000, 1000)
		$r1 = 7
		$r2 = 6
		
	ElseIf $flag = 5 Then
		$mButton[1] = GUICtrlCreateLabel(StringUpper($tretry), $W - 65, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[2] = GUICtrlCreateLabel(StringUpper($tcancel), $W - 145, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[3] = GUICtrlCreateLabel('', 1000, 1000)
		$r1 = 4
		$r2 = 2
		
	ElseIf $flag = 6 Then
		$mButton[1] = GUICtrlCreateLabel(StringUpper($tcontinue), $W - 65, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[2] = GUICtrlCreateLabel(StringUpper($tagain), $W - 145, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$mButton[3] = GUICtrlCreateLabel(StringUpper($tcancel), $W - 225, $H + 50, 75, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
		$r1 = 11
		$r2 = 10
		$r3 = 2
	EndIf
	
	GUICtrlSetColor($mButton[1], $fcolor)
	GUICtrlSetColor($mButton[2], $fcolor)
	GUICtrlSetColor($mButton[3], $fcolor)

	GUISetState(@SW_SHOW, $MsgGUI)

	While 1
		_CursorMove($MsgGUI, $c2, $c1)
		Switch GUIGetMsg($MsgGUI)
			Case $mButton[1]
				GUIDelete($MsgGUI)
				Return $r1
			Case $mButton[2]
				GUIDelete($MsgGUI)
				Return $r2
			Case $mButton[3]
				GUIDelete($MsgGUI)
				Return $r3
		EndSwitch
	WEnd
EndFunc

Func _InputBox($title, $text, $default, $wSize = 150, $hSize = 100, $UD = False, $limitMax = 3, $limitMin = 1, $c1 = $iColor2, $c2 = $iColor1, $fcolor = $iFontColor)
	$InpGUI = GUICreate($title, $wSize, $hSize, -1, -1, $WS_POPUP+$WS_BORDER)
	GUISetIcon (@ScriptDir & "\Data\ico\i.ico")
	GUISetBkColor($c2, $InpGUI)
	GUICtrlCreateLabel(StringUpper($title), 10, 5, $wSize - 20, 30, $SS_CENTERIMAGE, $GUI_WS_EX_PARENTDRAG)
	GUICtrlSetColor(-1, $fcolor)
	GUICtrlCreateLabel($text, 10, 35, $wSize - 20, 20, -1, $GUI_WS_EX_PARENTDRAG)
	GUICtrlSetColor(-1, $fcolor)
	$input1 = GUICtrlCreateInput($default, 5, $hSize - 60, $wSize - 20, 25)
	GUICtrlSetFont(-1, 12)
	
	If $UD Then
		GUICtrlCreateUpdown(-1, $UDS_WRAP)
		GUICtrlSetLimit(-1, $limitMax, $limitMin)
	EndIf
	
	$btnSize = ($wSize/2) - 5

	$okButton = GUICtrlCreateLabel("OK", 7, $hSize - 30, $btnSize - 6, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
	GUICtrlSetColor(-1, $fcolor)
	$cancelButton = GUICtrlCreateLabel(StringUpper($tcancel), $btnSize + 7, $hSize - 30, $btnSize - 6, 25, BitOR($SS_CENTER, $SS_CENTERIMAGE), -1)
	GUICtrlSetColor(-1, $fcolor)
	
	GUISetState(@SW_SHOW, $InpGUI)

	While 1
		_CursorMove($InpGUI, $c2, $c1)
		$read = GUICtrlRead($input1)
		Switch GUIGetMsg($InpGUI)
			Case $okButton
				GUIDelete($InpGUI)
				; MsgBox(0, '', $read)
				Return $read
			Case $cancelButton
				GUIDelete($InpGUI)
				Return
		EndSwitch
	WEnd
	
EndFunc

Func _SetBorder($xPos, $yPos, $xSize, $ySize, $color=$iColor2)
	GUICtrlCreateGraphic($xPos, $yPos, $xSize, $ySize)
    GUICtrlSetBkColor(-1, $color)
    GUICtrlSetColor(-1, $color)
	GUICtrlSetState(-1,$GUI_DISABLE)
EndFunc

