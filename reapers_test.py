import os
from icecream import ic
from source.reapers.idtech.spk import WolfSPK

in_dir = r"C:\games\Wolfenstein2009\base\streampacks"

new_reaper = WolfSPK()
path = in_dir
file_list = os.listdir(path)
mask = '.spk'
out_dir="D:\\out"


for file in file_list:

    if mask in file.lower():
        base_name = os.path.splitext(os.path.basename(os.path.join(path, file)))[0]
        ic(file)
        new_reaper.file_name = os.path.join(path, file)
        new_reaper.output_folder = f"{out_dir}\\{base_name}"
        new_reaper.run()

            