import os
import time
import numpy as np

from source.reaper import Reaper, file_reaper

SH3_COEFF = 0x5D588B65
TBL_LEN = 0x2000
KEY_LEN = 0x400
TBL_MAX = TBL_LEN * 4
KEY_MAX = KEY_LEN * 4

KEY_1 = 21986
KEY_2 = 10844
KEY_3 = 15680
KEY_4 = 11742


class SH3Video(Reaper):
    crypt = 0

    @file_reaper
    def run(self):
        # Original C code from here: http://www.ctpax-x.org/index.php?goto=files&show=96&lang=en
        # Rewrite to Python with ChatGPT
            
        with open(self.file_name, "rb") as fl:
            sz = os.path.getsize(self.file_name)
            self.crypt = 2 if os.path.basename(self.file_name).split('.')[-1] == 'mpg' else 0

            if not self.crypt:
                if sz <= TBL_MAX:
                    raise ValueError("Invalid file")
                sz -= TBL_MAX

            # --- читаем таблицу ---
            if not self.crypt:
                k_bytes = bytearray(fl.read(TBL_MAX))
                k = np.frombuffer(k_bytes, dtype=np.uint32).copy()

                z = (
                    (k_bytes[KEY_1] << 24)
                    | (k_bytes[KEY_2] << 16)
                    | (k_bytes[KEY_3] << 8)
                    | k_bytes[KEY_4]
                ) & 0xFFFFFFFF
            else:
                k = np.zeros(TBL_LEN, dtype=np.uint32)
                k_bytes = bytearray(TBL_MAX)
                z = int(time.time() * 1000) & 0xFFFFFFFF

            t = z

            # --- (de)crypt таблицы ---
            for i in range(TBL_LEN):
                z = (z * SH3_COEFF + 1) & 0xFFFFFFFF
                k[i] ^= z

            # обратно в байты
            k_bytes = bytearray(k.astype('<u4').tobytes())

            if not self.crypt:
                k_bytes[KEY_1] = 0
                k_bytes[KEY_2] = 0
                k_bytes[KEY_3] = 0
                k_bytes[KEY_4] = 0

            else:
                k_bytes[KEY_1] = (t >> 24) & 0xFF
                k_bytes[KEY_2] = (t >> 16) & 0xFF
                k_bytes[KEY_3] = (t >> 8) & 0xFF
                k_bytes[KEY_4] = t & 0xFF

            new_ext = ".000" if self.crypt else ".mpg"
            ext = os.path.splitext(self.file_name)[1].lower()
            out_name = f'{self.output_folder}\\{os.path.basename(self.file_name).replace(ext, new_ext)}'

            with open(out_name, "wb") as f:
                if self.crypt:
                    f.write(k_bytes)

                for i in range(KEY_LEN):
                    z = (z * SH3_COEFF + 1) & 0xFFFFFFFF
                    k[i] = z

                key_stream = k.view(np.uint8)[:KEY_MAX]

                while sz > 0:
                    block_size = min(sz, TBL_MAX - KEY_MAX)
                    sz -= block_size

                    data = bytearray(fl.read(block_size))

                    # numpy XOR
                    arr = np.frombuffer(data, dtype=np.uint8)
                    arr ^= np.resize(key_stream, block_size)

                    f.write(arr.tobytes())
            
            self.update_pb(1, 1, out_name)
