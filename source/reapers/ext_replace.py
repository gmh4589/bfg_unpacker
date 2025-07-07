import os
from source.reaper import Reaper, file_reaper


class EXTReplace(Reaper):

    @file_reaper
    def run(self):
        base_name = os.path.basename(self.file_name)
        ext1, ext2 = self.script_name.split(', ')
        out_path = f"{self.output_folder}\\{base_name.replace(ext1, ext2)}"
        
        with open(self.file_name, 'rb') as f:
            file_data = f.read()

        self.file_save(out_path, file_data)
