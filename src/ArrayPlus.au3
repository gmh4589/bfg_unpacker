
#Include-once

#include <Array.au3>

#cs

_numArray ($z, $num = 0)

Creates numerals array. Parameter $z it's count elements in array, parameter $num is digit for filling, default is 0
Example 1: _numArray (100) - to create an array with 100 zeros
Example 2: _numArray (100, 5) - to create an array with 100 fives

_letterArray($lower = False, $digit = 0, $order = True)

Creates letter array. Parameter $lower: if True then all letter is lower case, if False then all letter is big case, parameter $digit: if 0 then don't add digits in array, if 1 then add in array digits 1 to 9, if >1 - then add in array once element '0-9', parameter $order is order of array, if True then [digits, letters], if False then [letters, digits]
Example 1: _letterArray() - to create array ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
Example 2: _letterArray(True) - to create array  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
Example 3: _letterArray(False, 1) - to create array ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
Example 4: _letterArray(False, 1, False) - to create array ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Example 5: _letterArray(False, 2, False) - to create array ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']

_digitArray($start = 0, $end = 100, $step = 1)

Creates an array filled with a sequence of digits. Parameter $start: start of array, parameter $end: end of array, parameter $step: step of array
Example 1: _digitArray() to create array with digits 0 to 100
Example 2: _digitArray(100, 0, -1) to create array with digits 100 to 0
Example 3: _digitArray(1, 100, 2) to create array with only even digits 0 to 100

_randomArray($z, $int = True, $min = 0, $max = 100)

Creates an array filled with random values. Parameter $z is count of elements, $min is minimal value, $max is maximal value, $int is integer(true) or float(false)
Example 1: _randomArray(100) - to create array with 100 integer random digits 0 to 100
Example 2: _randomArray(10, False) - to create array with 10 float random digits 0 to 100
Example 3: _randomArray(1000, True, 1000, 2000) - to create array with 1000 integer random digits 1000 to 2000
Example 4: _randomArray(25, True, 0, 1) - to create array with 25 random boolean value

_Bool($Bool)

Transform string value False or True to boolean. Can need if read value from text file or table.
Example 1: Bool('True') - to return boolean True
Example 2: 
	Local $testArray
	_FileReadToArray ('text.txt', $testArray)
	MsgBox(0, '', Bool($testArray[5])) 
- to read file text.txt with boolean value into array and show massage box with cell 5

#ce

Func _numArray ($z, $num = 0)
	local $_zeroArray[0]
		for $i = 0 to $z
			_ArrayAdd($_zeroArray, $num)
		Next
	Return ($_zeroArray)
EndFunc

Func _letterArray($lower = False, $digit = 0, $order = True)
	If $lower = False Then Local $_letterArray = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	If $lower = True Then Local $_letterArray = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	If $digit = 0 Then Local $_digitArray = ['']
	If $digit = 1 Then Local $_digitArray = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	If $digit > 1 Then Local $_digitArray = ['0-9']
	If $order = True Then 
		_ArrayConcatenate($_digitArray, $_letterArray)
		Return ($_digitArray)
	ElseIf $order = False Then 
		_ArrayConcatenate($_letterArray, $_digitArray)
		Return($_letterArray)
	EndIf
EndFunc

Func _digitArray($start = 0, $end = 100, $step = 1)
	local $_digitArray[0]
		for $i = $start to $end step $step
			_ArrayAdd($_digitArray, $i)
		Next
	Return ($_digitArray)
EndFunc

Func _randomArray($z, $int = True, $min = 0, $max = 100)
	local $_randomArray[0]
		for $i = 0 to $z
			_ArrayAdd($_randomArray, Random($min, $max, $int))
		Next
	Return ($_randomArray)
EndFunc

Func _Bool($Bool)
	If $Bool = 'True' Then Return True
	If $Bool = 'False' Then Return False
EndFunc