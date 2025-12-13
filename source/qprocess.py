
import os
from icecream import ic

from PyQt6.QtWidgets import QComboBox, QDialog
from PyQt6.QtCore import pyqtSlot

from source.ui import localize
from source.ui.custom_ui import ProgressBar, CustomDialog
from source.reaper import logger


class QProcessList:

    def __init__(self):
        self.file_name = ''
        self.head = b''
        self.proc = None
        self.nuke = None
        self.last_run = None
        self.pb = None
        self.maximum = 100

    def q_connect(self, nuke, fn='', header=f'{localize.unpacking}...', maximum=100, out_dir='C:\\out', subfolder=True):
        self.pb = ProgressBar(maximum=maximum)
        self.maximum = maximum
        self.nuke = nuke
        self.nuke.file_name = fn
        fp = f'{out_dir}\\{os.path.basename(fn).replace(".", "_")}'
        ic(fp)

        try:
            self.nuke.output_folder = fp if subfolder else out_dir

            if subfolder:
                os.makedirs(fp, exist_ok=True)

        except AttributeError:
            pass

        self.pb.header.setText(self.get_short_text(header))
        self.pb.progressBar.setValue(0)
        self.pb.progress.setText('')
        self.pb.status.setText('')
        self.pb.is_stop = False
        self.pb.show()

        try:
            self.nuke.update_signal.connect(self.update_progress)
            self.nuke.user_choice_signal.connect(self.pb_user_choice)

            if self.last_run is not None:
                self.nuke.finished.connect(self.last_run)

            self.nuke.start()
        except Exception as error:
            logger(level='ERROR', 
                   message=f'\t\nError by slot-siganl connection!\t\n{error}\t\n{self.nuke}!', 
                   show=True)

    @staticmethod
    def get_short_text(text):

        if len(text) > 50:
            short_name = text[:10] + '...' + text[-30:]
        else:
            short_name = text

        return short_name
    
    # @pyqtSlot(str, list, object)
    def pb_user_choice(self, header_text, drop_list=None, callback=None):
        
        if callback:
            if drop_list:
                combo = QComboBox()
                combo.addItems(drop_list)
                dialog = CustomDialog(text=f"{header_text}:", title=header_text, btn_ok=True, btn_cancel=True, combo=combo)
            else:
                dialog = CustomDialog(text=f"{header_text}:", title=header_text, btn_ok=True, btn_cancel=True)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                result = dialog.get_selected()
                callback(result)
            else:
                callback(None)

    # @pyqtSlot(int, str, str, bool)
    def update_progress(self, pb_value, p_text, info, process_done):

        if self.pb.is_stop:
            self.nuke.terminate()

        if process_done:
            self.pb.close()

        else:
            self.pb.progressBar.setValue(pb_value if pb_value > 5 else 5)
            self.pb.progress.setText(self.get_short_text(p_text))
            self.pb.status.setText(self.get_short_text(info))
