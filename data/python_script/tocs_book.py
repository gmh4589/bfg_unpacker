
import os
import sys

file_path = sys.argv[1]

book = open(file_path, 'rb')
book.seek(8, 0)
start = int.from_bytes(book.read(4), byteorder='little')
book.seek(20, 0)
count = int.from_bytes(book.read(4), byteorder='little')
startData = int.from_bytes(book.read(4), byteorder='little')
book.seek(start, 0)

offsetArray = []
nameOffsetArray = []

for i in range(count):
	offsetArray.append(int.from_bytes(book.read(4), byteorder='little'))

for i in range(count):
	nameOffsetArray.append(int.from_bytes(book.read(2), byteorder='little'))

a = book.tell()
size = os.path.getsize(file_path)

data = book.read(startData - a)
nameArray = data.split(b'\x00')

offsetArray.append(size)
name = str(sys.argv[1].split('\\')[-1].split('.')[0])

path = sys.argv[2] + '\\' + name + '\\'
os.makedirs(path)

for j in range(len(offsetArray) - 1):
	book.seek(offsetArray[j])
	data = book.read(offsetArray[j + 1] - offsetArray[j])
	coef = '0' * (5 - len(str(j))) + str(j)
	newFile = path + coef + '.' + str(nameArray[j])[2:-1] + '.dat'
	with open(newFile, 'wb') as file: file.write(data)

