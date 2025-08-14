import os
from tkinter.filedialog import askopenfilename
from PIL import Image
from source.reaper import Reaper, file_reaper
from source.ui import localize
# TODO: Something wrong with palette colors, need to check


class ARTExtractor(Reaper):

    @file_reaper
    def run(self):
        palette_file = os.path.join(os.path.dirname(self.file_name), 'PALETTE.DAT')

        if not os.path.exists(palette_file):
            palette_file = askopenfilename(filetypes=[("Palette files", "*.PAL; *.DAT"), (localize.all_files, "*.*")],)

        if not palette_file:
            self.update_signal.emit(100, '', '', True)
            return

        with open(palette_file, "rb") as palette:
            # color_seq = sum([[int.from_bytes(palette.read(1)) * 4 for _ in range(3)] for i in range(256)], [])
            color_seq = sum([[int.from_bytes(palette.read(1)) for _ in range(3)] for _ in range(256)], [])

        with open(self.file_name, "rb") as art_file:
            magic = art_file.read(4)

            if magic != b"\x01\0\0\0":
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Build Engine'), True)
                return

            art_file.seek(4, 1)
            start_num = int.from_bytes(art_file.read(4), byteorder="little")
            end_num = int.from_bytes(art_file.read(4), byteorder="little")
            tiles_count = end_num - start_num + 1
            heights_list = [int.from_bytes(art_file.read(2), byteorder="little") for _ in range(tiles_count)]
            widths_list = [int.from_bytes(art_file.read(2), byteorder="little") for _ in range(tiles_count)]
            art_file.seek(4 * tiles_count, 1)

            for i in range(tiles_count):
                w = widths_list[i]
                h = heights_list[i]
                size = h * w
                name = f"{str(start_num + i)}.{self.setting['Main']['fav_format']}"
                tile_data = list(art_file.read(size))

                if w != 0 and h != 0:
                    tile_data = [tile_data[i:i + w] for i in range(0, len(tile_data), w)]
                    tile_data = sum(map(list, zip(*tile_data)), [])
                    self.update_pb(tiles_count, i + 1, name)

                    with open(os.path.join(self.output_folder, name), 'wb') as new_image:
                        image = Image.new(mode="P", size=(h, w))
                        image.putpalette(color_seq)
                        image.putdata(tile_data)
                        image.save(new_image, transparency=255)

        self.update_pb(tiles_count, tiles_count, '')
