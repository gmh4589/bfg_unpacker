
import os
import shutil
from send2trash import send2trash
import configparser
from source.reaper import Reaper


class DeleteThread(Reaper):

    def run(self):
        setting = configparser.ConfigParser()
        setting.read('./setting.ini')
        not_deleted = 0
        deleting_list = os.listdir(self.output_folder)
        all_items = len(deleting_list)

        for i, item in enumerate(deleting_list):
            name = os.path.join(self.output_folder, item)
            info_text = f'Deleting {item}...'
            print(info_text)
            self.update_signal.emit(int(100 / all_items * (i + 1)), f'{i + 1}/{all_items}', info_text, False)

            try:
                if int(setting['Main']['trash']):
                    send2trash(name)  # TODO: ?????
                else:
                    os.remove(name) if os.path.isfile(name) else shutil.rmtree(name)

            except (PermissionError, FileNotFoundError):
                # send2trash(name)
                not_deleted += 1

        msg = f'Some files or folders ({not_deleted}) could be moved to trashcan. ' if not_deleted else 'Done!'
        self.update_signal.emit(100, f'{all_items}/{all_items}', msg, True)
        print(msg)
