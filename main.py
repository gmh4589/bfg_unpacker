
import os
import sys
from threading import Thread

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import *
from source.ui.main_ui_init import MainWindow
from source.ui import localize
from source.reapers import (pathologic, aurora_engine, seven_s_seven, celestia, doom_wad, zip_archive, locres,
                            arx_fatalis, phyre)
from source import delete
from source.reaper import after_dot


class UnpackerMain(MainWindow):

    def __init__(self):
        super().__init__()
        sys.stdout = EmittingStream(text_written=self.append_text)

        # QProcesses connect
        self.aurora = aurora_engine.ERFUnpacker()
        self.arx = arx_fatalis.PakExtractor()
        self.celestia = celestia.Celestia()
        self.delete_thread = delete.DeleteThread()
        self.id_tech = doom_wad.WadExtractor()
        self.locres2txt = locres.Locres2TXT()
        self.txt2locres = locres.TXT2Locres()
        self.mor = pathologic.MorUnpacker()
        self.phyre = phyre.PhyreSave()
        self.x7 = seven_s_seven.Seven()
        self.zip = zip_archive.Zip()

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

            for file_name in file_names:

                if file_name:
                    self.set_setting('Main', 'last_dir', os.path.dirname(file_name))
                    yield file_name

    def file_reaper(self, index, select_folder=False, more_one=False):

        try:
            item = self.model.itemFromIndex(index)
            data_string = self.mainList.loc[self.mainList['game_name'] == item.text()]
            func_name = data_string['func_name'].values[0]
            script_name = data_string['script_name'].values[0]
            after_dot['Default'] = data_string['ext_list'].values[0] if data_string['ext_list'].values[0] != 'nan' else ''
            ext_list = after_dot[func_name] if func_name in after_dot.keys() else after_dot['Default']

            if func_name in ('_Unity', '_Frostbite2', '_Frostbite3'):
                select_folder = True

            for file_name in self.file_open(ext_list, select_folder, more_one):

                if file_name:
                    thread = None
                    ext = file_name.split('.')[-1].lower()

                    with open(file_name, 'rb') as fff:
                        header = fff.read(4)

                    if header == b'PK\x03\x04':
                        self.q_connect(self.zip, file_name)
                    else:

                        match func_name:
                            case '_7x7':
                                self.q_connect(self.x7, file_name)

                            case '_Arx':
                                self.q_connect(self.arx, file_name)

                            case '_Aurora':
                                self.q_connect(self.aurora, file_name)

                            case '_ExoPlanet':
                                self.q_connect(self.celestia, file_name, header=f'{localize.creating}...')

                            case '_idTech':

                                if ext == 'wad':
                                    self.q_connect(self.id_tech, file_name)
                                else:
                                    # TODO: Add functions to unpack other file types
                                    print(f'{localize.work_in_progress}...')

                            case '_Mor':
                                self.q_connect(self.mor, file_name)

                            case '_Sen':

                                if ext in ('phyre', 'dds', 'png', 'bmp', 'gxt'):
                                    self.q_connect(self.phyre, file_name)
                                else:
                                    # TODO: Add functions to unpack other file types
                                    print(f'{localize.work_in_progress}...')

                            case '_Unity':
                                thread = Thread(target=self.unpacker.unity, args=(file_name,), daemon=True)

                            case '_Unreal' | '_Unreal4':

                                if ext == 'locres':
                                    self.q_connect(self.locres2txt, file_name)
                                elif ext == 'txt':
                                    self.q_connect(self.txt2locres, file_name)
                                else:
                                    thread = Thread(target=self.unpacker.unreal, args=(file_name, script_name), daemon=True)

                            case '_ZIP':
                                thread = Thread(target=self.unpacker.seven_zip, args=(file_name,), daemon=True)

                            case _:
                                thread = Thread(target=self.unpacker.quick_bms, args=(file_name, script_name), daemon=True)

                        if thread is not None:
                            thread.start()

        except IndexError:
            pass

    def q_connect(self, threed, file_name='', header=f'{localize.unpacking}...'):
        threed.file_name = file_name
        threed.output_folder = self.out_dir
        self.pb.set_theme(self.setting["Main"]["theme"])
        self.pb.header.setText(header)
        self.pb.progressBar.setValue(0)
        self.pb.progress.setText('')
        self.pb.status.setText('')
        self.pb.show()
        threed.update_signal.connect(self.update_progress)
        threed.start()

    def empty_out(self):

        if os.listdir(self.out_dir):
            self.q_connect(self.delete_thread, header=f'{localize.deleting}...')
        else:
            print(localize.empty_folder)

    def update_progress(self, pb_value, p_text, info, process_done):
        self.pb.progressBar.setValue(pb_value)
        self.pb.progress.setText(p_text)
        self.pb.status.setText(info)

        if process_done:
            self.pb.close()


class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UnpackerMain()
    win.show()
    sys.exit(app.exec())
