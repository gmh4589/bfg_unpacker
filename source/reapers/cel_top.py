import os
from source.reaper import Reaper, file_reaper


class CelTop(Reaper):

    @file_reaper
    def run(self):
        files = os.listdir(self.file_name)

        for i, file in enumerate(files):
            ext, name = file.split('.')

            if ext.lower() == 'esp':

                with open(os.path.join(self.file_name, f"{name}.cel"), 'wb'):
                    pass

                with open(os.path.join(self.file_name, f"{name}.top"), 'wb'):
                    pass

            self.update_pb(len(files), i, file)
