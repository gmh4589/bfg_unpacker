
import os
import shutil
import configparser

from source.reaper import Reaper, file_reaper
from source.ui import localize


class DeleteThread(Reaper):

    @file_reaper
    def run(self):
        setting = configparser.ConfigParser()
        setting.read(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini')
        of = setting['Main']['out_path']
        not_deleted = []
        deleting_list = os.listdir(of)
        all_items = len(deleting_list)

        for i, item in enumerate(deleting_list):
            name = os.path.join(of, item)
            info_text = f'{localize.deleting} - {item}...'
            print(info_text)
            percent = int(100 / all_items * (i + 1))
            self.update_signal.emit(percent if percent < 95 else 95, f'{i + 1}/{all_items}', info_text, False)

            try:
                if int(setting['Main']['trash']):
                    os.system(f'{self.path_to_root}\\data\\AutoIt3.exe '
                              f'{self.path_to_root}\\data\\delete_to_trash.au3 "{name}"')
                else:
                    os.remove(name) if os.path.isfile(name) else shutil.rmtree(name)

            except (PermissionError, FileNotFoundError, OSError):
                not_deleted.append(name)

        # TODO: Text!!!
        msg = (f'Some files or folders ({len(not_deleted)}, {not_deleted}) '
               f'could not deleted. ') if not_deleted else ''
        self.update_signal.emit(100, f'{all_items}/{all_items}', msg, True)
        print(msg)
