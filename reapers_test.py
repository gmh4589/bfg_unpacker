import os
from icecream import ic
from source.reapers.bethesda.bsi import BSITexture

new_reaper = BSITexture()
path = r"I:\tests\esp\tesargog\Redguard\fxart"
file_list = os.listdir(path)


for file in file_list:

    if 'TEXBSI' in file:
        
        # try:
        ic(file)
        new_reaper.file_name = os.path.join(path, file)
        new_reaper.output_folder = f"I:\\out\\{file.replace('.', '_')}"
        new_reaper.run()
            
        # except Exception as e:
        #     ic(f"Error processing {file}: {e}")
            