import os
from icecream import ic
from source.reapers.konami.sh4_the_room import BINExtractor

in_dir = r"C:\GOG\Silent Hill 4\data"

new_reaper = BINExtractor()
path = in_dir
file_list = os.listdir(path)
mask='.bin'
out_dir="D:\\out"

for file in file_list:

    if mask in file.lower():

        ic(file)
        new_reaper.file_name = os.path.join(path, file)
        new_reaper.output_folder = out_dir
        new_reaper.run()

            