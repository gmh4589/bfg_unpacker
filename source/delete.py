
import os
import shutil
# from send2trash import send2trash
import configparser
from source.reaper import Reaper, file_reaper
from source.ui import localize


class DeleteThread(Reaper):

    @file_reaper
    def run(self):
        setting = configparser.ConfigParser()
        setting.read('./setting.ini')
        of = setting['Main']['out_path']
        not_deleted = []
        deleting_list = os.listdir(of)
        all_items = len(deleting_list)

        for i, item in enumerate(deleting_list):
            name = os.path.join(of, item)
            info_text = f'{localize.deleting} - {item}...'
            print(info_text)
            self.update_signal.emit(int(100 / all_items * (i + 1)), f'{i + 1}/{all_items}', info_text, False)

            try:
                if int(setting['Main']['trash']):
                    # send2trash(name)  # TODO: ?????
                    pass
                else:
                    os.remove(name) if os.path.isfile(name) else shutil.rmtree(name)

            except (PermissionError, FileNotFoundError):
                # send2trash(name)
                not_deleted.append(name)

        # TODO: Text!!!
        msg = (f'Some files or folders ({len(not_deleted)}, {not_deleted}) '
               f'could not deleted. ') if not_deleted else ''
        self.update_signal.emit(100, f'{all_items}/{all_items}', msg, True)
        print(msg)
