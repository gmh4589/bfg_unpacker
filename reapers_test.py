import os
from icecream import ic
from source.reapers.build.art import ARTExtractor

new_reaper = ARTExtractor()
path = r"I:\tests\blood classic"
file_list = os.listdir(path)


for file in file_list:

    if '.art' in file.lower():
        
        # try:
        ic(file)
        new_reaper.file_name = os.path.join(path, file)
        new_reaper.output_folder = f"I:\\out\\{file.replace('.', '_')}"
        new_reaper.run()
            
        # except Exception as e:
        #     ic(f"Error processing {file}: {e}")
            