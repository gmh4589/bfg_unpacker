from PyQt5.QtCore import QThread, pyqtSignal
from source.unpacker import file_reaper


class Reaper(QThread):
    update_signal = pyqtSignal(int, str, str, bool)

    def __init__(self, output_folder):
        super().__init__()
        self.file_name = 'file_name'
        self.output_folder = output_folder

    @file_reaper
    def run(self):
        pass
