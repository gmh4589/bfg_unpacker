
import os
import sys
from PyQt5.QtWidgets import *
from icecream import ic

from source.quick_open import QuickOpen
from source.ui import localize
from source.reaper import after_dot
import source.reapers as reapers


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
            func_name = data_string['func_name'].values[0]
            script_name = data_string['script_name'].values[0]
            after_dot['Default'] = (data_string['ext_list'].values[0]
                                    if data_string['ext_list'].values[0] != 'nan' else '')
            ext_list = after_dot[self.func_name] if self.func_name in after_dot.keys() else after_dot['Default']

            if self.func_name in ('_Unity', '_Frostbite2', '_Frostbite3'):
                select_folder = True

            self.create_queue(ext_list, select_folder, more_one, func_name, script_name)

        except IndexError:
            pass

    def create_queue(self, ext_list='', select_folder=False, more_one=False, func_name='', script_name=''):
        self.func_name = func_name
        self.script_name = script_name
        ext_list = f'{ext_list}{localize.all_files}(*.*)'
        self.file_list = list(self.file_open(ext_list, select_folder, more_one))
        self.last_run = self.select_unpacker
        self.select_unpacker()

    def select_unpacker(self):

        if self.file_list:
            file_name = self.file_list.pop(0)
            ic(file_name)

            if file_name:
                ext = file_name.split('.')[-1].lower()
                self.proc = None

                with open(file_name, 'rb') as fff:
                    header = fff.read(4)

                if header == b'PK\x03\x04':
                    self.proc = reapers.seven_zip.SevenZIP()
                else:

                    match self.func_name:
                        case '_7x7':
                            self.proc = reapers.seven_s_seven.Seven()
                        case '_Arx':
                            self.proc = reapers.arx_fatalis.PakExtractor()
                        case '_Aurora':
                            self.proc = reapers.aurora_engine.ERFUnpacker()
                        case '_ExoPlanet':
                            self.proc = reapers.celestia.Celestia()
                        case '_idTech':

                            if ext == 'wad':
                                self.proc = reapers.doom_wad.WadExtractor()
                            elif ext == 'pak':
                                self.proc = reapers.quake_pak.QPAKExtractor()
                            else:
                                # TODO: Add functions to unpack other file types
                                print(f'{localize.work_in_progress}...')

                        case '_Mor':
                            self.proc = reapers.pathologic.MorUnpacker()
                        case '_Sen':

                            if ext in ('phyre', 'dds', 'png', 'bmp', 'gxt'):
                                self.proc = reapers.phyre.PhyreSave()
                            elif ext == 'dat':

                                if 'book' in self.file_name:

                                    if self.checkBox_Reimport.isChecked():
                                        self.proc = reapers.sen_book.SenBookSave()
                                    else:
                                        self.proc = reapers.sen_book.SenBook()
                                else:
                                    # TODO: Add functions to unpack other file types
                                    print(f'{localize.work_in_progress}...')

                            else:
                                # TODO: Add functions to unpack other file types
                                print(f'{localize.work_in_progress}...')

                        case '_Unity':
                            self.proc = reapers.unity.Unity()
                        case '_Unreal' | '_Unreal4':

                            if ext == 'locres':
                                self.proc = reapers.locres.Locres2TXT()
                            elif ext == 'txt':
                                self.proc = reapers.locres.TXT2Locres()
                            else:
                                self.proc = reapers.unreal.Unreal()
                                self.proc.key = self.script_name

                        case '_ZIP':
                            self.proc = reapers.zip_archive.Zip()
                        case '_7ZIP':
                            self.proc = reapers.seven_zip.SevenZIP()
                        case '_ZPL':
                            self.proc = reapers.zpl2png.ZPL2PNG()
                        case '_Total':
                            self.proc = reapers.qbms.Q_BMS()
                            self.proc.script_name = 'data/wcx/TotalObserver.wcx'
                        case '_GAUP':
                            self.proc = reapers.qbms.Q_BMS()
                            self.proc.script_name = 'data/wcx/gaup_pro.wcx'
                        case '_Source':
                            self.proc = reapers.source_vpk.VPKExtractor()
                        case _:
                            self.proc = reapers.qbms.Q_BMS()
                            self.proc.script_name = self.script_name
                
                if self.proc is not None:
                    self.q_connect(self.proc, file_name, header=f'{localize.unpacking}: {file_name}...')

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
