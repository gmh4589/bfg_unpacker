import os
from source.unpacker import file_reaper

@file_reaper
def mor_unpacker(file_name, output_folder):

    with open(file_name, 'rb') as f:
        f.seek(8, 0)

        file_count = int.from_bytes(f.read(4), byteorder='little')

        for i in range(file_count):

            name_length = int.from_bytes(f.read(1), byteorder='little')
            name = f.read(name_length).decode('unicode_escape')
            file_position = f.tell()
            file_size = int.from_bytes(f.read(4), byteorder='little')
            file_offset = int.from_bytes(f.read(4), byteorder='little')

            f.seek(file_offset, 0)
            file_data = f.read(file_size)

            output_path = os.path.join(output_folder, name)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'wb') as new_file:
                new_file.write(file_data)

            f.seek(file_position + 16, 0)

            print(f'{i + 1}/{file_count} - {name}')
