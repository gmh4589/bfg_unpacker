import os
import sys

file_path = sys.argv[2]

try:
    name = sys.argv[1] + '\\' + (file_path.split('\\')[-1]).split('.')[0] + '\\'
    os.makedirs(name)

except FileExistsError:
    name = ''

print(name)

archive = open(file_path, 'rb')
data = archive.read()

files = data.split(b'ADAT')
files.pop(0)
i = 1

for file in files:

    # TODO: Localized text
    print(f'Unpacking: {i} from {len(files)}')

    with open(name + str(i) + '.awc', 'wb+') as new_track:
        new_track.write(b'ADAT' + file)

    i += 1
