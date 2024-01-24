
import sys
import os
from PyQt5.QtCore import QObject, pyqtSignal

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
        nuke.output_folder = self.out_dir
        self.pb.set_theme(self.setting["Main"]["theme"])
        self.pb.header.setText(header)
        self.pb.progressBar.setValue(0)
        self.pb.progress.setText('')
        self.pb.status.setText('')
        self.pb.show()
        nuke.update_signal.connect(self.update_progress)

        if self.last_run is not None:
            nuke.finished.connect(self.last_run)

        nuke.start()

    def update_progress(self, pb_value, p_text, info, process_done):

        if process_done:
            self.pb.progressBar.setValue(0)
            self.pb.close()

        else:
            self.pb.progressBar.setValue(pb_value)
            self.pb.progress.setText(p_text)
            self.pb.status.setText(info)


class PrintTo(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))

    def flush(self):
        pass
