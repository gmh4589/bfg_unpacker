
import sys
import os
from PyQt6.QtCore import QObject, pyqtSignal
from icecream import ic

from source.ui.main_ui_init import MainWindow
from source.ui import localize
from source import delete


class QProcessList(MainWindow):

    def __init__(self):
        super().__init__()
        sys.stdout = PrintTo(text_written=self.append_text)
        self.root_dir = os.path.abspath(__file__).split('source')[0]
        self.file_name = ''
        self.last_run = None
        self.head = b''
        self.delete_thread = delete.DeleteThread()
        self.proc = None

    def q_connect(self, nuke, fn='', header=f'{localize.unpacking}...'):
        nuke.file_name = fn
        fp = f'{self.out_dir}\\{os.path.basename(fn)}'
        ic(fp)
        nuke.output_folder = fp if self.checkBox_createSubfolders.isChecked() else self.out_dir

        if self.checkBox_createSubfolders.isChecked():
            os.makedirs(fp, exist_ok=True)

        self.pb.set_theme(self.setting["Main"]["theme"])
        self.pb.header.setText(self.get_short_text(header))
        self.pb.progressBar.setValue(0)
        self.pb.progress.setText('')
        self.pb.status.setText('')
        self.pb.show()
        nuke.update_signal.connect(self.update_progress)

        if self.last_run is not None:
            nuke.finished.connect(self.last_run)

        nuke.start()

    @staticmethod
    def get_short_text(text):

        if len(text) > 50:
            short_name = text[:30] + '...' + text[-15:]
        else:
            short_name = text

        return short_name

    def update_progress(self, pb_value, p_text, info, process_done):

        if process_done:
            self.pb.progressBar.setValue(0)
            self.pb.close()

        else:
            self.pb.progressBar.setValue(pb_value)
            self.pb.progress.setText(self.get_short_text(p_text))
            self.pb.status.setText(self.get_short_text(info))


class PrintTo(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))

    def flush(self):
        pass
