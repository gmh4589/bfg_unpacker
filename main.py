import os
import sys

# Это костыль, без него не работает компилляция
from sqlalchemy.dialects.mysql.mariadb import *

from PyQt6.QtWidgets import QFileDialog, QApplication, QInputDialog
from icecream import ic

from source.quick_open import QuickOpen
from source.ui import localize, custom_ui
from source.reaper import after_dot
from source.reapers import *


class UnpackerMain(QuickOpen):

    def __init__(self):
        super().__init__()
        self.func_name = ''
        self.script_name = ''
        self.file_list = []

        if true_false(self.setting['Main']['disable_ic'].lower()):
            ic.disable()

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
        self.last_run = self.select_unpacker
        self.select_unpacker()

    def find_zip_method(self):

        file_n = ''.join(self.file_open(more_one=True))

        if file_n:
            self.proc = zip_scan.ZipScanner()
            self.q_connect(self.proc, file_n, header=f'{localize.file}: {file_n}...')

    def select_unpacker(self):

        if self.file_list:
            file_name = self.file_list.pop(0)
            ic(file_name)

            if file_name:
                ext = file_name.split('.')[-1].lower()
                self.proc = None

                try:

                    with open(file_name, 'rb') as fff:
                        magic = fff.read(4)
                        magic2 = fff.read(4)
                        magic3 = fff.read(4)

                except PermissionError:
                    magic, magic2, magic3 = b'', b'', b''

                if magic == b'PK\x03\x04':
                    self.proc = zip_archive.Zip()
                else:

                    match self.func_name:
                        case '_7x7':
                            self.proc = seven_s_seven.Seven()
                        case '_7ZIP' | '_Chromium' | '_Construct' | '_Flash':
                            self.proc = seven_zip.SevenZIP()
                        case '_Arx':
                            self.proc = arx_fatalis.PakExtractor()
                        case '_Anvil':
                            # TODO: Move to QuickBMS
                            self.proc = qbms.Q_BMS()
                            self.proc.script_name = '/data/scripts/scimitar.bms'
                        case '_Asura':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_Aurora':

                            if ext in ('erf', 'rim'):
                                self.proc = aurora_engine.ERFUnpacker()
                            elif ext == 'bif':
                                self.proc = aurora_bif_key.BifKey()
                            elif ext == 'key':
                                # TODO: Нужно локализовать текст!!!
                                custom_ui.CustomDialog(text='Select a BIF file!',
                                                       style=self.setting["Main"]["theme"]).exec()

                            elif ext == 'dzip':
                                # TODO: Need test!!!
                                self.proc = other_prg.OtherProg()
                                self.proc.program_name = "gibbed\\Gibbed.RED.Unpack.exe"

                            else:
                                print(localize.not_correct_file.replace('%%', 'Aurora Engine'))

                        case '_Bethesda' | '_CelTop':

                            match ext:
                                case 'bsa':

                                    if magic == b'BSA\0':

                                        if magic2 in (104, 105):
                                            self.proc = bsa_archives.BethesdaArchive()
                                        else:
                                            self.proc = qbms.Q_BMS()
                                            self.proc.script_name = 'data/wcx/gaup_pro.wcx'

                                    else:
                                        self.proc = qbms.Q_BMS()
                                        self.proc.script_name = 'data/wcx/gaup_pro.wcx'

                                    if 'ARCH3D' in self.file_name:
                                        pass
                                    elif 'arena' in self.file_name.lower() or 'battle' in self.file_name.lower():
                                        pass

                                case 'ba2':
                                    self.proc = ba2_archives.BethesdaArchive()

                                case 'esp' | 'esm' | 'esl':
                                    pass
                                case 'esx':
                                    pass
                                case 'snd':
                                    pass
                                case 'pex':
                                    pass
                                case '':
                                    pass
                                    # TODO: CEL\TOP creator
                                case _:

                                    if 'TEXBSI' in self.file_name:
                                        pass
                                    else:
                                        print(localize.not_correct_file.replace('%%', 'Bethesda Game'))

                        case '_Build':

                            if ext == 'grp':
                                self.proc = qbms.Q_BMS()
                                self.proc.script_name = 'data/wcx/gaup_pro.wcx'
                            elif ext == 'art':
                                # TODO: Add functions to unpack other file types
                                # TODO: '\data\art2tga.exe'
                                print(f'{localize.work_in_progress}...')
                            elif ext == 'tga':
                                # TODO: Add functions to unpack other file types
                                # TODO: '\data\tga2art.exe'
                                print(f'{localize.work_in_progress}...')
                            elif ext == 'rff':
                                # TODO: Add functions to unpack other file types
                                # TODO: _DosBox('', 'barf.exe ', 1, ' -x ', $sFileName)
                                print(f'{localize.work_in_progress}...')
                            else:
                                print(localize.not_correct_file.replace('%%', 'Build Engine'))

                        case '_Chrome':

                            if ext in ("csb", "spb"):
                                self.proc = qbms.Q_BMS()
                                self.proc.script_name = 'data/scripts/dying_light.bms'
                            elif ext == ".rpack":

                                if magic == b'RP6L':
                                    self.proc = chrome_engine.RP6L()
                                else:
                                    # TODO: Add functions to unpack other file types
                                    print(f'{localize.work_in_progress}...')

                            else:
                                print(localize.not_correct_file.replace('%%', 'Chrome Engine'))

                        case '_CryEngine':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_ExoPlanet':
                            self.proc = celestia.Celestia()
                            # TODO: Add Space Engine support
                        case '_FrostBite':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_Gamemaker':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_GAUP':
                            self.proc = qbms.Q_BMS()
                            self.proc.script_name = 'data/wcx/gaup_pro.wcx'
                        case '_Glacier':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_Godot':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_idTech':

                            if ext == 'wad':
                                self.proc = doom_wad.WadExtractor()
                            elif ext == 'pak':
                                magic3 = int.from_bytes(magic2, 'little')

                                if magic3 % 576 != 0:
                                    l2 = magic3 % 64
                                    version = 1 if l2 == 0 else 2
                                else:
                                    version, ok = QInputDialog.getInt(self, 'WARNING', 'Select a version:', min=1, max=2)

                                self.proc = quake_pak.QPAKExtractor(version)
                            else:
                                # TODO: Add functions to unpack other file types
                                print(localize.not_correct_file.replace('%%', 'idTech Engine'))
                                print(f'{localize.work_in_progress}...')

                        case '_LithTech':

                            if ext in ('rez', 'arch00', 'arch01', 'arch02', 'arch03', 'arch04', 'arch05'):
                                self.proc = qbms.Q_BMS()
                                self.proc.script_name = 'data/wcx/gaup_pro.wcx'
                            elif ext == 'arch06':
                                self.proc = qbms.Q_BMS()
                                self.proc.script_name = 'data/scripts/shadow_of_mordor.bms'
                            else:
                                print(localize.not_correct_file.replace('%%', 'LithTech Engine'))

                        case '_Mor':
                            self.proc = pathologic.MorUnpacker()
                        case '_MTFramework':
                            self.proc = mt_arc.ARCExtractor()
                        case '_OOAM':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_OtherPRG':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_RedEngine':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_REEngine':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_RenPy':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_RPGMaker':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_SAU':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_Sen':

                            if ext in ('phyre', 'dds', 'png', 'bmp', 'gxt'):
                                self.proc = phyre.PhyreSave()
                            elif ext == 'pkg':
                                self.proc = sen_pkg.PKGExtractor()
                            elif ext == 'dat':

                                if self.checkBox_Reimport.isChecked():
                                    self.proc = sen_book.SenBookSave()
                                else:

                                    if magic == b'\x20\x00\x00\x00':
                                        self.proc = sen_book.SenBook()
                                    else:
                                        # TODO: Add functions to unpack other file types
                                        print(f'{localize.work_in_progress}...')

                            elif os.path.isdir(file_name):

                                if self.checkBox_Reimport.isChecked():
                                    self.proc = sen_pkg.PKGPacker()
                                    self.proc.COMPRESSED = self.checkBox_ZipData.isChecked()

                            else:
                                # TODO: Add functions to unpack other file types
                                print(f'{localize.work_in_progress}...')

                        case '_Source':

                            if ext == 'vpk':
                                self.proc = source_vpk.VPKExtractor()
                            elif os.path.isdir(file_name):
                                version, ok = QInputDialog.getInt(self,
                                                                  title='WARNING', label='Select a version:',
                                                                  min=1, max=2)

                                if ok and version:
                                    self.proc = source_vpk.VPKPacker()
                                    self.proc.VERSION = version

                            else:
                                # TODO: Add functions to unpack other file types
                                print(f'{localize.work_in_progress}...')

                        case '_TellTale':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_Total':
                            self.proc = qbms.Q_BMS()
                            self.proc.script_name = 'data/wcx/TotalObserver.wcx'
                        case '_Unigene':
                            # TODO: Add functions to unpack other file types
                            print(f'{localize.work_in_progress}...')
                        case '_Unity':
                            self.proc = unity.Unity()
                        case '_Unreal' | '_Unreal4':

                            if self.checkBox_Reimport.isChecked():

                                if ext in ('upk', 'upx', 'xxx', 'u'):
                                    self.proc = ue3_injector.U3Injector()
                                    self.proc.source_folder = self.file_open(select_folder=True)
                                    self.proc.new_folder = self.file_open(select_folder=True)
                                elif ext == 'txt':
                                    self.proc = locres.TXT2Locres()

                            else:

                                if ext in ('upk', 'upx', 'xxx', 'u'):
                                    self.proc = ue3_reaper.UE3()
                                elif ext == 'locres':
                                    self.proc = locres.Locres2TXT()
                                elif ext == 'txt':
                                    self.proc = locres.TXT2Locres()
                                else:
                                    self.proc = unreal.Unreal()
                                    self.proc.key = self.script_name

                        case '_Wii_iso':
                            empty = os.path.basename(file_name).split('.')[0]
                            new_empty_folder = empty
                            a = 0

                            while True:

                                if not os.path.exists(f"{self.out_dir}\\{new_empty_folder}"):
                                    break
                                else:
                                    new_empty_folder = f"{empty}_{a}"
                                    a += 1

                            self.proc = other_prg.OtherProg()
                            self.proc.percent_type = '50'

                            if ext in ('iso', 'wbfs'):
                                self.proc.program_name = 'wit\\wit.exe'
                                self.proc.first_arg = 'x'
                                self.proc.second_arg = f'-d "{self.out_dir}\\{new_empty_folder}"'
                            else:  # TODO: Test with CISO, WDF and WIA disc images
                                self.proc.program_name = 'wit\\wdf.exe'
                                self.proc.first_arg = '+u'
                                self.proc.second_arg = f'"{self.out_dir}\\{new_empty_folder}"'

                        case '_ZPL':
                            self.proc = zpl2png.ZPL2PNG()
                        case '_Zaglushka':
                            print(f'{localize.work_in_progress}...')
                        case _:
                            self.proc = qbms.Q_BMS()
                            self.proc.script_name = self.script_name

                if self.proc is not None:
                    self.q_connect(self.proc, file_name, header=f'{localize.unpacking}: {file_name}...')

    def empty_out(self):

        if os.listdir(self.out_dir):
            self.q_connect(self.delete_thread, header=f'{localize.deleting}...')
        else:
            print(localize.empty_folder)


def true_false(boo):
    try:
        b1 = bool(int(boo))
    except ValueError:
        b1 = True if boo.lower() == 'true' else False

    return b1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UnpackerMain()
    win.show()
    win.raise_()
    sys.exit(app.exec())
