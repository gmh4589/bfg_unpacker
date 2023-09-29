
from PyQt5.QtCore import QThread, pyqtSignal


class Reaper(QThread):
    update_signal = pyqtSignal(int, str, str, bool)

    def __init__(self):
        super().__init__()
        self.file_name = 'file_name'
        self.output_folder = 'output_folder'

    def run(self):
        pass
