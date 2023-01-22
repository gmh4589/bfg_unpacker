
;TODO: Проверить. Добавить функции создания каталогов звезд экзопланет.

Func CelestiaExo($file)
	$iFile1 = FileOpen($sFolderName & "\exoplanets.ssc", 1)
	Local $line
	_FileReadToArray($file, $line)
	$iStringCount = $line[0]
	FileWriteLine($iFile1, "#" & $tExo1 & @YEAR & "\" & @MON & "\" & @MDAY & " " & @HOUR & ":" & @MIN)
	FileWriteLine($iFile1, "#" & $tExo2 & $iStringCount-3 & $tExo3)
	FileWriteLine($iFile1, "#" & $tExo4 & " Extrasolar planet enciclopedia http://exoplanet.eu/catalog/")
	FileWriteLine($iFile1, "#" & $tExo5 & " BFG Unpacker")
	FileWriteLine($iFile1, "")
	GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)
	
		For $i = 3 to $iStringCount
			$tab = StringSplit($line[$i],',')
			Local $name = $tab[1], $mass = $tab[3], $radius = $tab[9], $orbital_period = $tab[12], $semi_major_axis = $tab[15], $eccentricity = $tab[18], $inclination = $tab[21], $omega = $tab[27], $star_name = $tab[69], $ra = $tab[70], $dec = $tab[71], $star_distance = $tab[77], $star_mass = $tab[83], $star_radius = $tab[86], $star_sp_type = $tab[89], $star_alternate_names = $tab[98]
				FileWriteLine($iFile1, '"' & $name & '" "' & $star_name & '"')
				FileWriteLine($iFile1, '{')
					If $mass  = '' Then $mass = _MassCalc($radius)
				FileWriteLine($iFile1, 'Mass ' & $mass*317.8)
					If $radius  = '' Then $radius = _RadiusCalc($mass)
				FileWriteLine($iFile1, 'Radius ' & $radius*71492)
				FileWriteLine($iFile1, '')
				FileWriteLine($iFile1, 'EllipticalOrbit {')
					If $orbital_period  = '' Then $orbital_period  = _PeriodCalc($semi_major_axis)
				FileWriteLine($iFile1, 'Period ' & $orbital_period)
					If $semi_major_axis  = '' Then $semi_major_axis  = _SemiAxisCalc($orbital_period)
				FileWriteLine($iFile1, 'SemiMajorAxis ' & $semi_major_axis)
					If $eccentricity  = '' Then $eccentricity = 0
				FileWriteLine($iFile1, 'Eccentricity ' & $eccentricity)
					If $inclination  = '' Then $inclination = 90
				FileWriteLine($iFile1, 'Inclination ' & $inclination)
					If $omega  = '' Then $omega = 90
				FileWriteLine($iFile1, 'MeanLongitude ' & $omega)
				FileWriteLine($iFile1, '}')
				FileWriteLine($iFile1, '')
				FileWriteLine($iFile1, 'UniformRotation {')
				FileWriteLine($iFile1, 'Period 10')
				FileWriteLine($iFile1, 'Inclination 90')
				FileWriteLine($iFile1, 'AscendingNode 0')
				FileWriteLine($iFile1, 'MeridianAngle 0')
				FileWriteLine($iFile1, '}')
				FileWriteLine($iFile1, '}')
				FileWriteLine($iFile1, '')
		Next
	GUICtrlSetData($iEdit, $tDone & @CRLF, 1)
	FileClose($iFile1)
	FileClose($file)
EndFunc

Func SpaceEngineExo($file)
	$iFile1 = FileOpen($sFolderName & "\exoplanets.sc", 1)
	Local $line
	_FileReadToArray($file, $line)
	$iStringCount = $line[0]
	FileWriteLine($iFile1, "//" & $tExo1 & @YEAR & "\" & @MON & "\" & @MDAY & " " & @HOUR & ":" & @MIN)
	FileWriteLine($iFile1, "//" & $tExo2 & $iStringCount-3 & $tExo3)
	FileWriteLine($iFile1, "//" & $tExo4 & ": Extrasolar planet enciclopedia http://exoplanet.eu/catalog/")
	FileWriteLine($iFile1, "//" & $tExo5 & " BFG Unpacker")
	FileWriteLine($iFile1, "")
	GUICtrlSetData($iEdit, $tProcessingFile & @CRLF, 1)
	
		For $i = 2 to $iStringCount
			$tab = StringSplit($line[$i],',')
			Local $name = $tab[1], $mass = $tab[3], $radius = $tab[9], $orbital_period = $tab[12], $semi_major_axis = $tab[15], $eccentricity = $tab[18], $discovery_date = $tab[25], $epoch = $tab[30], $detection_type = $tab[64], $star_name = $tab[69]
			Local $iDiscoverMethod = [['Radial Velocity, RadVel'], ['Imaging, Imaging'], ['Astrometry, Astrometry'], ['Controversial, Transit'], ['Microlensing, MicroLens'], ['Other, Transit'], ['Primary Transit, Transit'], ['Primary Transit, TTV, Transit'], ['Timing, Pulsar'], ['TTV, TTV']]
				FileWriteLine($iFile1, 'Planet "' & $name & '"')
				FileWriteLine($iFile1, '{')
				FileWriteLine($iFile1, 'ParentBody "' & $star_name & '"')
					If $mass  = '' Then $mass = _MassCalc($radius)
				FileWriteLine($iFile1, 'Msini ' & $mass*317.8)
				$detection_type = $iDiscoverMethod[_ArraySearch($iDiscoverMethod, $detection_type)][1]
				FileWriteLine($iFile1, 'DiscMethod     "' & $detection_type & '"')
				FileWriteLine($iFile1, 'DiscDate       "' & $discovery_date & '"')
				FileWriteLine($iFile1, 'Orbit')
				FileWriteLine($iFile1, '{')
					If $epoch <> '' then FileWriteLine($iFile1, 'Epoch           ' & $epoch)
					If $orbital_period  = '' Then $orbital_period  = _PeriodCalc($semi_major_axis)
				FileWriteLine($iFile1, 'Period ' & $orbital_period)
					If $semi_major_axis  = '' Then $semi_major_axis  = _SemiAxisCalc($orbital_period)
				FileWriteLine($iFile1, 'SemiMajorAxis ' & $semi_major_axis)
					If $eccentricity  = '' Then $eccentricity = 0
				FileWriteLine($iFile1, 'Eccentricity ' & $eccentricity)
				FileWriteLine($iFile1, '}')
				FileWriteLine($iFile1, '}')
				FileWriteLine($iFile1, '')
		Next
	GUICtrlSetData($iEdit, $tDone & @CRLF, 1)
	FileClose($iFile1)
	FileClose($file)
EndFunc

Func _MassCalc($radius)
	If $radius < 0.1666667 Then $mass = $radius*5
	If $radius > 0.1666667 < 0.33333 Then $mass = $radius
	If $radius > 0.33333 < 0.75 Then $mass = $radius/0.67
	If $radius > 0.75 Then $mass = 1
	If $radius = '' Then $mass = 1
	Return($mass)
EndFunc

Func _RadiusCalc($mass)
	If $mass < 0.03 Then $radius = $mass/5
	If $mass > 0.03 < 0.15 Then $radius = $mass
	If $mass > 0.15 < 0.75 Then $radius = $mass/0.67
	If $mass > 0.75 Then $radius = 1
	If $mass = '' Then $radius = 1
	Return($radius)
EndFunc

Func _PeriodCalc($semi_major_axis)
	If $semi_major_axis  = '' Then
		$orbital_period = 1
	Else
		$orbital_period = $semi_major_axis*$semi_major_axis*365
	EndIf
	Return($orbital_period)
EndFunc

Func _SemiAxisCalc($orbital_period)
	If $orbital_period = '' Then
		$semi_major_axis = 1
	Else
		$semi_major_axis =(sqrt($orbital_period))/365
	EndIf
	Return($semi_major_axis)
EndFunc