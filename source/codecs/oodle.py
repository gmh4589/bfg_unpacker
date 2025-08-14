
import os
from ctypes import cdll, c_char_p, create_string_buffer

from source.ui import localize


class OodleDecompress:

    def __init__(self, dll_path: str):
        self.dll_path = f"{os.getcwd()}\\data\\tools\\{dll_path}"

        if not os.path.exists(self.dll_path):
            print(f'{localize.not_correct_file} {dll_path}')

        self.oodle = cdll.LoadLibrary(self.dll_path)

    def decompress(self, source_data: bytes, output_size: int=0) -> bytes:
        output = create_string_buffer(output_size)
        zip_size = len(source_data)

        if output_size == None:
            output_size = zip_size * 20

        try:
            self.oodle.OodleLZ_Decompress(
                c_char_p(source_data), zip_size, output, output_size,
                0, 0, 0, None, None, None, None, None, None, 3)
        except OSError:
            return False
        
        return output.raw

