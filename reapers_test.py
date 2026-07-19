import os
from icecream import ic
from source.reapers.idtech.doom_patch import Patch

in_dir = r"D:\SteamLibrary\steamapps\common\DOOM\base" 

new_reaper = Patch()
path = in_dir
file_list = os.listdir(path)
mask = ".patch"
out_dir="D:\\out"


for file in file_list:

    if mask in file.lower():
        base_name = os.path.splitext(os.path.basename(os.path.join(path, file)))[0]
        ic(file)
        new_reaper.file_name = os.path.join(path, file)
        new_reaper.output_folder = f"{out_dir}\\{base_name}"
        new_reaper.run()

            