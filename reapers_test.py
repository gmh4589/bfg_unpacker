import os
from icecream import ic
from source.reapers.capcom.tex import TEX2DDS

new_reaper = TEX2DDS()
path = r"D:\images\Sony - PlayStation 3\NPEB00553-[RESIDENT EVIL CODE Veronica X]\PS3_GAME\USRDIR\BHCV\nativePS3\system\texture"
file_list = os.listdir(path)


for file in file_list:

    if '.tex' in file.lower():
        
        # try:
        ic(file)
        new_reaper.file_name = os.path.join(path, file)
        # new_reaper.output_folder = f"D:\\out\\{file.replace('.', '_')}"
        new_reaper.output_folder = f"F:\\out"
        new_reaper.run()
            
        # except Exception as e:
        #     ic(f"Error processing {file}: {e}")
            