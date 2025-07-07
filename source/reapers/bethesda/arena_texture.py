import os
import struct
from icecream import ic
from PIL import Image
from tkinter.filedialog import askopenfilename
from source.reaper import Reaper, file_reaper
from source.ui import localize


class ImgData:

    def __init__(self, 
                 pos_x: int = 0,
                 pos_y: int = 0,
                 offset: int = 0, 
                 width: int = 0, 
                 height: int = 0, 
                 data_size: int = 70,
                 frames: int = 1,
                 duration: int = 100,
                 data: bytes = b''):
        self.offset = offset
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.data_size = data_size
        self.frames = frames
        self.duration = duration
        self.data = data

    @property
    def zipped(self):
        return self.__zipped
    
    @zipped.setter
    def zipped(self, zipped):

        zip_list = {
            2: 'RLE',
            0x8000: 'RLE',
            0x108: 'ImageRLE',
            0x1108: 'RecordRLE'
        }
        
        self.__zipped = zip_list.get(zipped, 'Uncompressed')



class ArenaTexture(Reaper):
    palette = None

    def save_image(self, path, width, height, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        image = Image.frombytes('P', (width, height), data)
        image.putpalette(self.color_seq)
        image.save(path)
    
    def un_rle(self, file, img):
        output = b''
        zip_list = []

        for _ in range(img.height):
            zip_list.append([
                int.from_bytes(file.read(2), 'little'), # String offset by data start
                int.from_bytes(file.read(2), 'big')  # Zipped flag. 0x80 for RLE, 0 for uncompressed
                             ])

        for i in range(img.height):
            offset, zipped = zip_list[i]
            string = b''
            file.seek(offset + img.offset) 

            if not zipped:
                string += file.read(img.width)
            else:
                w = int.from_bytes(file.read(2), 'little')

                while len(string) < w:
                    probe = struct.unpack('<h', file.read(2))[0]  # Int16

                    if probe < 0:
                        probe = -probe
                        pixel = file.read(1)
                        string += pixel * probe
                    elif probe > 0:
                        string += file.read(probe)
                
            output += string

        return output
    
    def read_frame(self, file, page):
        b_width = int.from_bytes(file.read(2), 'little')
        b_height = int.from_bytes(file.read(2), 'little')

        for _ in range(b_height):
            row = bytearray(b_width)
            c = file.read(1)[0]
            is_zero = True
            p = 0

            while p < b_width:

                for _ in range(c):

                    if is_zero:
                        row[p] = 0
                    else:
                        row[p] = file.read(1)[0]
                        
                    p += 1

                if p < b_width or (p == b_width and is_zero):
                    c = file.read(1)[0]

                is_zero = not is_zero

            page.data += row

    def gif_read(self, file, img):
        page_list = [ImgData(width=img.width, height=img.height, data=b'') for _ in range(img.frames)]
        img_list = []

        if 'RLE' not in img.zipped:
            anim_data_len = int.from_bytes(file.read(4), 'little')
            file.seek(anim_data_len - 4, 1)

        for page in page_list:

            if 'RLE' in img.zipped:
                here = file.tell()
                page.data = self.un_rle(file, img)
                file.seek(here + (img.height * 4))  # Skip to next frame
            else:
                self.read_frame(file, page)
            
            new_page = Image.frombytes('P', (img.width, img.height), page.data)
            new_page.putpalette(self.color_seq)
            img_list.append(new_page)
        
        return img_list
    
    def set_palette(self, palette=None):
        dir_path = os.path.dirname(self.file_name)

        if 'ARENA2' in self.file_name and palette is None:
            palette = "ART_PAL.COL"
        elif '3dart' in self.file_name and palette is None:
            palette = "redguard.col"

        if os.path.exists(f"{dir_path}\\{palette}"):
            palette = f"{dir_path}\\{palette}"
        else:
            palette = askopenfilename(filetypes=[("Palette files", "*.pal, *.col")], initialdir=dir_path)
                    
        if not palette:
            self.update_pb(1, 1, localize.error_in_file)
            return 0
        
        with open(palette, 'rb') as pal:
            pal.seek(8)
            self.color_seq = sum([[int.from_bytes(pal.read(1)) for _ in range(3)] for _ in range(256)], [])
        
        return 1

    @file_reaper
    def run(self):

        if self.palette is None:
            set_pal = self.set_palette()

            if not set_pal:
                return

        offset_list = []

        with open(self.file_name, 'rb') as tex:
            img_count = int.from_bytes(tex.read(2), 'little')
            dummy = tex.read(1)
            texture_set_name = tex.read(0x17).decode('ascii').strip('\x00').strip(' ').strip('\t')
            dummy = tex.read(1)
            dummy = int.from_bytes(tex.read(1))

            # For Solid Colors Type. Save 64x64 onecoclored images 
            if 'Solid Colors' in texture_set_name:
                start_color = dummy
                print(start_color, img_count)
                img_list = [ImgData(width=64, height=64, data=j.to_bytes(1) * (64 * 64)) for j in range(start_color, img_count + start_color)]
                
                format = self.setting['Main']['fav_format']

                for i, img in enumerate(img_list):
                    pth = f"{self.output_folder}/{texture_set_name}_{str(i).rjust(4, '0')}.{format}"
                    self.update_pb(img_count, i + 1, pth)
                    self.save_image(pth, img.width, img.height, img.data)
                
            # For surface, normal and animated textures
            else:

                # Read offsets block
                for _ in range(img_count):
                    data_offset = int.from_bytes(tex.read(4), 'little')
                    offset_list.append(data_offset)
                    tex.seek(0x10, 1)

                block = []
                offset_list = sorted(offset_list)
                img_list = []

                # Create block list
                for n in range(len(offset_list)):

                    try:

                        if offset_list[n + 1] - offset_list[n] == 0x1c:
                            block.append(ImgData(offset=offset_list[n]))
                        else:
                            block.append(ImgData(offset=offset_list[n]))
                            img_list.append(block)
                            block = []

                    except IndexError:
                        block.append(ImgData(offset=offset_list[n]))
                        img_list.append(block)
                        block = []

                a = 0

                # Read image data (width, height, etc)
                for block in img_list:

                    for b in block:

                        if b.offset > 0:
                            tex.seek(b.offset)
                            b.pos_x = int.from_bytes(tex.read(2), 'little')
                            b.pos_y = int.from_bytes(tex.read(2), 'little')
                            b.width = int.from_bytes(tex.read(2), 'little')
                            b.height = int.from_bytes(tex.read(2), 'little')
                            b.zipped = int.from_bytes(tex.read(2), 'little')
                            imgs_size = int.from_bytes(tex.read(4), 'little')
                            b.data_size = int.from_bytes(tex.read(4), 'little')
                            is_normal = int.from_bytes(tex.read(2), 'little')
                            b.frames = int.from_bytes(tex.read(2), 'little')
                            b.duration = int.from_bytes(tex.read(2), 'little')
                            x_scale = int.from_bytes(tex.read(2), 'little')
                            y_scale = int.from_bytes(tex.read(2), 'little')

                    for img in block:
                        tex.seek(img.offset + img.data_size)
                        ic(hex(img.offset), hex(img.data_size), img.width, img.height, img.frames, img.zipped)

                        if img.frames == 1:
                            format = self.setting['Main']['fav_format']
                            pth = f"{self.output_folder}/{texture_set_name}_{str(a).rjust(4, '0')}.{format}"
                            self.update_pb(img_count, a + 1, pth)
                            a += 1
                            img.data = b''

                            if 'RLE' in img.zipped:
                                img.data = self.un_rle(tex, img)
                                self.save_image(pth, img.width, img.height, img.data)
                            else:
                                
                                for _ in range(img.height):
                                    img.data += tex.read(img.width)
                                    tex.seek(256 - img.width, 1)
                                    
                                self.save_image(pth, img.width, img.height, img.data)

                        elif img.frames == 0:
                            continue
                        else:
                            pth = f"{self.output_folder}/{texture_set_name}_{str(a).rjust(4, '0')}.gif"
                            self.update_pb(img_count, a + 1, pth)
                            a += 1
                            img_list = self.gif_read(tex, img)
                            os.makedirs(os.path.dirname(pth), exist_ok=True)
                            img_list[0].save(pth,
                                        save_all = True, append_images = img_list[1:], 
                                        optimize = False, duration = 10)
                            