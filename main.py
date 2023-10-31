
import os
import sys
from threading import Thread

from PyQt5.QtWidgets import *
from source.quick_open import QuickOpen
from source.ui import localize
from source.reaper import after_dot


class UnpackerMain(QuickOpen):

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

            for self.file_name in file_names:

                if self.file_name:
                    yield self.file_name

            self.set_setting('Main', 'last_dir', os.path.dirname(self.file_name))

    def file_reaper(self, index, select_folder=False, more_one=False):

        try:
            item = self.model.itemFromIndex(index)
            data_string = self.mainList.loc[self.mainList['game_name'] == item.text()]
            func_name = data_string['func_name'].values[0]
            script_name = data_string['script_name'].values[0]
            after_dot['Default'] = (data_string['ext_list'].values[0]
                                    if data_string['ext_list'].values[0] != 'nan' else '')
            ext_list = after_dot[func_name] if func_name in after_dot.keys() else after_dot['Default']
            self.select_unpacker(func_name, script_name, ext_list, select_folder, more_one)

        except IndexError:
            pass

    def select_unpacker(self, func_name, script_name='', ext_list='', select_folder=False, more_one=False):

        if func_name in ('_Unity', '_Frostbite2', '_Frostbite3'):
            select_folder = True

        ext_list += f'{localize.all_files}(*.*)'

        for self.file_name in self.file_open(ext_list, select_folder, more_one):

            if self.file_name:
                thread = None
                ext = self.file_name.split('.')[-1].lower()

                with open(self.file_name, 'rb') as fff:
                    header = fff.read(4)

                if header == b'PK\x03\x04':
                    self.q_connect(self.zip, self.file_name)
                else:

                    match func_name:
                        case '_7x7': self.q_connect(self.x7, self.file_name)
                        case '_Arx': self.q_connect(self.arx, self.file_name)
                        case '_Aurora': self.q_connect(self.aurora, self.file_name)
                        case '_ExoPlanet': self.q_connect(self.celestia, self.file_name,
                                                          header=f'{localize.creating}...')
                        case '_idTech':

                            if ext == 'wad':
                                self.q_connect(self.id_tech, self.file_name)
                            else:
                                # TODO: Add functions to unpack other file types
                                print(f'{localize.work_in_progress}...')

                        case '_Mor': self.q_connect(self.mor, self.file_name)
                        case '_Sen':

                            if ext in ('phyre', 'dds', 'png', 'bmp', 'gxt'):
                                self.q_connect(self.phyre, self.file_name)
                            else:
                                # TODO: Add functions to unpack other file types
                                print(f'{localize.work_in_progress}...')

                        case '_Unity': thread = Thread(target=self.unpacker.unity,
                                                       args=(self.file_name,), daemon=True)
                        case '_Unreal' | '_Unreal4':

                            if ext == 'locres':
                                self.q_connect(self.locres2txt, self.file_name)
                            elif ext == 'txt':
                                self.q_connect(self.txt2locres, self.file_name)
                            else:
                                thread = Thread(target=self.unpacker.unreal,
                                                args=(self.file_name, script_name), daemon=True)

                        case '_ZIP': thread = Thread(target=self.unpacker.seven_zip,
                                                     args=(self.file_name,), daemon=True)
                        case '_ZPL': self.q_connect(self.zpl2png, self.file_name)
                        case _:  thread = Thread(target=self.unpacker.quick_bms,
                                                 args=(script_name, self.file_name), daemon=True)

                    if thread is not None:
                        thread.start()

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
