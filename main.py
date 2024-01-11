
import os
import sys
from PyQt5.QtWidgets import *
from icecream import ic

from source.quick_open import QuickOpen
from source.ui import localize
from source.reaper import after_dot


class UnpackerMain(QuickOpen):

    def __init__(self):
        super().__init__()
        self.func_name = ''
        self.script_name = ''
        self.file_list = []

        try:

            if self.setting['Main']['disable_ic'] == 'True':
                ic.disable()

        except KeyError:
            ic.disable()

    def q_open(self):
        self.file_list = list(self.file_open())
        self.last_run = self.find_reaper
        self.find_reaper()

    def file_open(self, ext_list='', select_folder=False, more_one=False):

        if not select_folder:

            try:
                f = ext_list.replace('|', ';;')
            except AttributeError:
                f = ''

            if more_one:
                file_names = QFileDialog.getOpenFileName(self, localize.open_file, filter=f,
                                                         directory=self.setting['Main']['last_dir'])[0]
            else:
                file_names = QFileDialog.getOpenFileNames(self, localize.open_file, filter=f,
                                                          directory=self.setting['Main']['last_dir'])[0]
        else:
            file_names = [QFileDialog.getExistingDirectory(self, localize.select_folder,
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
            self.script_name = data_string['script_name'].values[0]
            after_dot['Default'] = (data_string['ext_list'].values[0]
                                    if data_string['ext_list'].values[0] != 'nan' else '')
            ext_list = after_dot[self.func_name] if self.func_name in after_dot.keys() else after_dot['Default']
            ext_list += f'{localize.all_files}(*.*)'

            if self.func_name in ('_Unity', '_Frostbite2', '_Frostbite3'):
                select_folder = True

            self.file_list = list(self.file_open(ext_list, select_folder, more_one))
            self.last_run = self.select_unpacker
            self.select_unpacker()

        except IndexError:
            pass

    def select_unpacker(self):

        if self.file_list:
            file_name = self.file_list.pop(0)
            ic(file_name)

            if file_name:
                ext = file_name.split('.')[-1].lower()

                with open(file_name, 'rb') as fff:
                    header = fff.read(4)

                if header == b'PK\x03\x04':
                    self.q_connect(self.zip, file_name)
                else:

                    match self.func_name:
                        case '_7x7': self.q_connect(self.x7, file_name,
                                                    header=f'{localize.unpacking}: {file_name}...')
                        case '_Arx': self.q_connect(self.arx, file_name,
                                                    header=f'{localize.unpacking}: {file_name}...')
                        case '_Aurora': self.q_connect(self.aurora, file_name,
                                                       header=f'{localize.unpacking}: {file_name}...')
                        case '_ExoPlanet': self.q_connect(self.celestia, file_name,
                                                          header=f'{localize.creating}: {file_name}...')
                        case '_idTech':

                            if ext == 'wad':
                                self.q_connect(self.id_tech, file_name,
                                               header=f'{localize.unpacking}: {file_name}...')
                            elif ext == 'pak':
                                self.q_connect(self.quake_pak, file_name,
                                               header=f'{localize.unpacking}: {file_name}...')
                            else:
                                # TODO: Add functions to unpack other file types
                                print(f'{localize.work_in_progress}...')

                        case '_Mor': self.q_connect(self.mor, file_name,
                                                    header=f'{localize.unpacking}: {file_name}...')
                        case '_Sen':

                            if ext in ('phyre', 'dds', 'png', 'bmp', 'gxt'):
                                self.q_connect(self.phyre, file_name,
                                               header=f'{localize.unpacking}: {file_name}...')
                            elif ext == 'dat':

                                if 'book' in self.file_name:

                                    if self.checkBox_Reimport.isChecked():
                                        self.q_connect(self.sen_book_save, file_name,
                                                       header=f'{localize.unpacking}: {file_name}...')
                                    else:
                                        self.q_connect(self.sen_book, file_name,
                                                       header=f'{localize.unpacking}: {file_name}...')
                                else:
                                    pass

                            else:
                                # TODO: Add functions to unpack other file types
                                print(f'{localize.work_in_progress}...')

                        case '_Unity': self.q_connect(self.unity, file_name,
                                                      header=f'{localize.unpacking}: {file_name}...')
                        case '_Unreal' | '_Unreal4':

                            if ext == 'locres':
                                self.q_connect(self.locres2txt, file_name,
                                               header=f'{localize.unpacking}: {file_name}...')
                            elif ext == 'txt':
                                self.q_connect(self.txt2locres, file_name,
                                               header=f'{localize.unpacking}: {file_name}...')
                            else:
                                self.unreal.key = self.script_name
                                self.q_connect(self.unreal, file_name,
                                               header=f'{localize.unpacking}: {file_name}...')

                        case '_ZIP': self.q_connect(self.seven_zip, file_name,
                                                    header=f'{localize.unpacking}: {file_name}...')
                        case '_ZPL': self.q_connect(self.zpl2png, file_name,
                                                    header=f'{localize.unpacking}: {file_name}...')
                        case '_Total':
                            self.qbms.script_name = 'data/wcx/TotalObserver.wcx'
                            self.q_connect(self.qbms, file_name,
                                           header=f'{localize.unpacking}: {file_name}...')
                        case '_GAUP':
                            self.qbms.script_name = 'data/wcx/gaup_pro.wcx'
                            self.q_connect(self.qbms, file_name,
                                           header=f'{localize.unpacking}: {file_name}...')
                        case _:
                            self.qbms.script_name = self.script_name
                            self.q_connect(self.qbms, file_name,
                                           header=f'{localize.unpacking}: {file_name}...')

    def empty_out(self):

        if os.listdir(self.out_dir):
            self.q_connect(self.delete_thread, header=f'{localize.deleting}...')
        else:
            print(localize.empty_folder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UnpackerMain()
    win.show()
    sys.exit(app.exec())
