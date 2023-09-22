
import os
import shutil
from send2trash import send2trash
from PyQt5.QtCore import QThread, pyqtSignal
import configparser


class DeleteThread(QThread):
    update_signal = pyqtSignal(int, str, str, bool)

    def __init__(self, out_dir):
        super().__init__()
        self.out_dir = out_dir
        self.deleting_list = os.listdir(self.out_dir)

    def run(self):
        setting = configparser.ConfigParser()
        setting.read('./setting.ini')
        not_deleted = 0
        all_items = len(self.deleting_list)
        print(setting['Main']['trash'])

        for i, item in enumerate(self.deleting_list):
            name = os.path.join(self.out_dir, item)
            info_text = f'Deleting {item}...'
            print(info_text)
            self.update_signal.emit(int(100 / all_items * (i + 1)), f'{i + 1}/{all_items}', info_text, False)

            try:
                if int(setting['Main']['trash']):
                    send2trash(name)
                else:
                    os.remove(name) if os.path.isfile(name) else shutil.rmtree(name)

            except (PermissionError, FileNotFoundError):
                not_deleted += 1

        msg = (f'Some files or folders ({not_deleted}) could not be deleted. '
               f'Try removing them manually') if not_deleted else 'Done!'
        self.update_signal.emit(100, f'{all_items}/{all_items}', msg, True)

        print(msg)