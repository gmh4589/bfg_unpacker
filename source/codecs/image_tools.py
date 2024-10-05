import os
from PIL import Image

from source.ui import localize


def bmp_save(x: int, y: int, b: int, name: str, image_data: bytes) -> None:

    with open(f'{name}.bmp', 'wb') as bmp_file:
        bmp_file.write(b'BM' + (len(image_data) + 0x36).to_bytes(4, byteorder='little') +
                       b'\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00' +
                       x.to_bytes(4, byteorder='little') +
                       y.to_bytes(4, byteorder='little') + b'\x01\x00' +
                       b.to_bytes(2, byteorder='little') + b'\x00\x00\x00\x00' +
                       len(image_data).to_bytes(4, byteorder='little') + (b'\x00' * 16) +
                       image_data)


def gxt_save(name, data):
    name = f'{name}.gxt'

    with open(name, 'wb') as gxt_file:
        gxt_file.write(data)

    os.system(f'./data/ps_tools/vita/GXTConvert.exe {name}')


def ktx_save(save_path: str, source_path: str) -> None:

    with open(source_path, 'rb') as ktx_stream:
        ktx_stream.seek(0x24)
        width = int.from_bytes(ktx_stream.read(4), byteorder="little")
        height = int.from_bytes(ktx_stream.read(4), byteorder="little")
        ktx_stream.seek(0x60)
        image_data = ktx_stream.read()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    new_image = Image.frombytes('RGBA', (width, height), image_data)
    new_image.save(save_path)
    print(f'{localize.file}: {source_path} -> {save_path}. {localize.saving}...\n'
          f'{localize.done}')


# For 24 and 32 bits
def BGR2RGB(data: bytes, color_order: str) -> bytes:
    byte_array = list(data)

    a = [byte_array[g] for g in
         range(color_order.index('A'), len(byte_array), len(color_order))] if 'A' in color_order else []
    x = [byte_array[h] for h in
         range(color_order.index('X'), len(byte_array), len(color_order))] if 'X' in color_order else []
    r = [byte_array[d] for d in range(color_order.index('R'), len(byte_array), len(color_order))]
    g = [byte_array[e] for e in range(color_order.index('G'), len(byte_array), len(color_order))]
    b = [byte_array[f] for f in range(color_order.index('B'), len(byte_array), len(color_order))]

    new_data = [item for sublist in (zip(r, g, b, a) if 'A' in color_order else zip(r, g, b)) for item in sublist]
    return bytes(new_data)
