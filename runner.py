import os
import sys


from PyQt6.QtCore import QRect, pyqtSignal, QObject
from PyQt6.QtWidgets import *
from icecream import ic

from source.setting import Setting


class MainWindow(QMainWindow, Setting):

    def __init__(self, test):
        super().__init__()
        ic(self.setting['Main']['last_dir'])
        self.test = test
        self.resize(300, 300)
        self.setWindowTitle("Simple Reaper")
        self.centralwidget = QWidget(self)
        self.logWindow = QTextBrowser(self.centralwidget)
        self.logWindow.setGeometry(QRect(0, 0, 300, 300))
        self.setCentralWidget(self.centralwidget)

        sys.stdout = EmittingStream(text_written=self.append_text)
        self.out_dir = 'E:\\out'
        os.makedirs(self.out_dir, exist_ok=True)
        self.test.file_name = self.file_open()
        self.test.output_folder = self.out_dir

        if self.test.file_name:
            self.test.start()

    def file_open(self, ext_list='', select_folder=False, more_one=False):

        if not select_folder:

            if more_one:
                file_name = ''
            else:

                try:
                    f = ext_list.replace('|', ';;')
                except AttributeError:
                    f = ''

                file_name = QFileDialog.getOpenFileName(self, 'Open file', filter=f,
                                                        directory=self.setting['Main']['last_dir'])[0]
        else:
            file_name = QFileDialog.getExistingDirectory(self, 'Select folder')

        return file_name

    def append_text(self, text):

        if text.strip():
            self.logWindow.append(text)


class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    from source.reapers.ba2_archives import BethesdaArchive
    win = MainWindow(BethesdaArchive())
    win.show()
    sys.exit(app.exec())

