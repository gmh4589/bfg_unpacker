import os
from icecream import ic
from source.reapers.capcom.re_engine import ReEngine

in_dir = r"D:\SteamLibrary\steamapps\common\RE3"

new_reaper = ReEngine()
path = in_dir
file_list = os.listdir(path)
mask = 're_chunk_000.pak.patch_001.pak'
out_dir="E:\\out"

new_reaper.game_file_list = 'RE3_PC_Release.list'

for file in file_list:

    if mask in file.lower():
        base_name = os.path.splitext(os.path.basename(os.path.join(path, file)))[0]
        ic(file)
        new_reaper.file_name = os.path.join(path, file)
        new_reaper.output_folder = f"{out_dir}\\{base_name}"
        new_reaper.run()

            