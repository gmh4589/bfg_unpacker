import os

import vpk
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class VPKExtractor(Reaper):

    @file_reaper
    def run(self):

        vpk_file = self.file_name if '_dir.vpk' in self.file_name else self.file_name[:-7] + 'dir.vpk'
        ic(vpk_file)
        dir_pak = vpk.open(vpk_file)
        i = 0
        file_count = len(dir_pak)

        for name in dir_pak:
            pak_file = dir_pak.get_file(name)
            path = os.path.join(self.output_folder, name)
            ic(path)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pak_file.save(path)
            self.update_pb(file_count, i, name)
            i += 1


class VPKPacker(Reaper):

    VERSION = 2

    @file_reaper
    def run(self):

        # version = simpledialog.askinteger("", "Enter engine version (1 or 2):",
        #                                   minvalue=1, maxvalue=2)

        folder_path = self.file_name
        archive_name = os.path.basename(self.file_name)
        new_vpk = vpk.NewVPK(path=folder_path)
        ic(self.VERSION)
        new_vpk.version = self.VERSION
        out_path = os.path.join(self.output_folder, archive_name + '_dir.vpk')
        print(out_path)
        new_vpk.save(out_path)
        self.update_signal.emit(100, f'1/1', localize.done, True)
