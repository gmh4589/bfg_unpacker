import os
import io
# from icecream import ic
from PIL import Image
from tkinter.filedialog import askopenfilename
from source.reaper import Reaper, file_reaper
from source.ui import localize


class BSITexture(Reaper):

    def read_palette(self, pal):
        return sum([[int.from_bytes(pal.read(1)) for _ in range(3)] for _ in range(256)], [])

    def set_palette(self, palette):
        dir_path = os.path.dirname(self.file_name)
        # palette = "REDGUARD.COL"

        if os.path.exists(f"{dir_path}\\{palette}"):
            palette = f"{dir_path}\\{palette}"
        else:
            palette = askopenfilename(filetypes=[("Palette files", "*.pal, *.col")], initialdir=dir_path)
                    
        if not palette:
            self.update_pb(1, 1, localize.error_in_file)
            return 0
        
        with open(palette, 'rb') as pal:
            pal.seek(8)
            return self.read_palette(pal)
    
    def save_image(self, path, image_data, width, height, pallette):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        image = Image.frombytes('P', (width, height), image_data)
        image.putpalette(pallette)
        image.save(path)

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as tex:
            zipped = True if tex.read(1) == b'\xFF' else False
            in_path = os.path.dirname(self.file_name)
            img_count = 0
            palette_list = [p for p in os.listdir(in_path) if p.lower().endswith(('.pal', '.col'))]

            if len(palette_list) > 1:
                print('Found more 1 palette files. Files be save with all Found palettes')

            if zipped:
                return
            else:
                tex.seek(0, 0)

            while True:
                img_count += 1
                start = tex.tell()
                magic = tex.read(4)
                tex.seek(start, 0)
                pallette = None

                if not magic:
                    break

                if magic != b'IFHD':
                    image_name = tex.read(9).decode('ascii').strip('\x00')
                    data_size = int.from_bytes(tex.read(4), 'little')

                    if not image_name:
                        break
                else:
                    image_name = os.path.splitext(os.path.basename(self.file_name))[0]

                while True:
                    header = tex.read(4)
                    block_len = int.from_bytes(tex.read(4), 'big')
                    pos = tex.tell()

                    if header == b'BHDR':
                        tex.seek(4, 1)
                        width = int.from_bytes(tex.read(2), 'little')
                        height = int.from_bytes(tex.read(2), 'little')
                    
                    elif header == b'CMAP':
                        pallette = self.read_palette(io.BytesIO(tex.read(block_len)))

                    elif header == b'DATA':
                        image_data = tex.read(block_len)

                        if pallette is not None:
                            path = f"{self.output_folder}\\{image_name}.{self.setting['Main']['fav_format']}"
                            self.save_image(path, image_data, width, height, pallette)
                        else:

                            for pal in palette_list:
                                path = f"{self.output_folder}\\{pal}\\{image_name}.{self.setting['Main']['fav_format']}"
                                pallette = self.set_palette(pal)
                                self.save_image(path, image_data, width, height, pallette)

                    elif header == b'END ':
                        break

                    tex.seek(pos + block_len)
                
            self.update_pb(img_count, img_count, path)
