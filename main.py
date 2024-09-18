import os
import sys

# Это костыль, без него не работает сборка в екзешник
from sqlalchemy.dialects.mysql.mariadb import *

from PyQt6.QtWidgets import QFileDialog, QApplication, QMainWindow
from icecream import ic

from source.quick_open import QuickOpen
from source.ui.main_ui_init import MainWindow
from source.ui.custom_ui import PrintTo
from source.ui import localize, custom_ui
from source.reaper import after_dot
from source.reapers import *
from source.delete import DeleteThread

ic.disable()


class UnpackerMain(MainWindow, QuickOpen):

    def __init__(self):
        super().__init__()
        sys.stdout = PrintTo(text_written=self.append_text)
        self.func_name = ''
        self.script_name = ''
        self.file_list = []

    def q_open(self):
        self.file_list = list(self.file_open())
        self.last_run = self.find_reaper
        self.find_reaper()

    def file_open(self, ext_list='', select_folder=False, more_one=False):

        if not select_folder:

            try:
                f = ext_list.replace('|', ';;').replace('None', '')
            except AttributeError:
                f = ''

            file_names = QFileDialog.getOpenFileNames(self, caption=localize.open_file, filter=f,
                                                      directory=self.setting['Main']['last_dir'])[0]

            if more_one and file_names:
                file_names = [file_names[0], '']

        else:
            file_names = [QFileDialog.getExistingDirectory(self, caption=localize.select_folder,
                                                           directory=self.setting['Main']['last_dir']), '']
        if file_names:
            self.set_setting('Main', 'last_dir', os.path.dirname(file_names[0]))
            ic(file_names)

            for file_name in file_names:

                if file_name:
                    yield file_name

    def file_reaper(self, index, select_folder=False, more_one=False):

        try:
            item = self.model.itemFromIndex(index)
            data_string = self.mainList.loc[self.mainList['game_name'] == item.text()]
            self.func_name = data_string['func_name'].values[0]
            script_name = data_string['script_name'].values[0]
            after_dot['Default'] = (data_string['ext_list'].values[0]
                                    if data_string['ext_list'].values[0] != 'nan' else '')
            ext_list = after_dot[self.func_name] if self.func_name in after_dot.keys() else after_dot['Default']

            if (self.func_name in ('_Unity', '_Frostbite2', '_Frostbite3', '_CelTop') or
                    self.checkBox_Reimport.isChecked()):
                select_folder = True

            self.create_queue(ext_list, select_folder, more_one, self.func_name, script_name)

        except IndexError:
            pass

    def create_queue(self, ext_list='', select_folder=False, more_one=False, func_name='', script_name=''):
        self.func_name = func_name
        self.script_name = script_name

        if type(ext_list) is float:
            ext_list = ''

        ext_list = f'{ext_list}{localize.all_files}(*.*)'
        ic(ext_list)
        self.file_list = list(self.file_open(ext_list, select_folder, more_one))
        self.last_run = self.find_reaper

        for _ in self.file_list:
            self.find_reaper()

    def find_zip_method(self):

        file_n = ''.join(self.file_open(more_one=True))

        if file_n:
            self.proc = zip_scan.ZipScanner()
            self.q_connect(self.proc, file_n, header=f'{localize.file}: {file_n}...')

    def empty_out(self):

        if os.listdir(self.out_dir):
            self.q_connect(DeleteThread(), header=f'{localize.deleting}...')
        else:
            print(localize.empty_folder)


class QuickUnpack(QMainWindow, QuickOpen):

    def __init__(self):
        super().__init__()

        self.is_stop = False
        self.pb = custom_ui.ProgressBar(self.setting["Main"]["theme"])
        self.last_run = None
        self.file_list = [sys.argv[1], ]
        self.func_name = None
        self.find_reaper()


if __name__ == "__main__":

    try:
        print(sys.argv[1])
        app = QApplication(sys.argv)
        win = QuickUnpack()

    except IndexError:
        app = QApplication(sys.argv)
        win = UnpackerMain()
        win.show()
        win.raise_()

    sys.exit(app.exec())
