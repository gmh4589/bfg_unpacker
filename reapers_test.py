import os
from icecream import ic
from source.reapers.sega.awb import AFS2Extractor

in_dir = r"D:\SteamLibrary\steamapps\common\Bayonetta\data\bgm"

new_reaper = AFS2Extractor()
path = in_dir
file_list = os.listdir(path)
mask = '.awb'
out_dir="F:\\out"


for file in file_list:

    if mask in file.lower():
        base_name = os.path.splitext(os.path.basename(os.path.join(path, file)))[0]
        ic(file)
        new_reaper.file_name = os.path.join(path, file)
        new_reaper.output_folder = f"{out_dir}\\{base_name}"
        new_reaper.run()

            