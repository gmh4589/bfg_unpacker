
import sys

from PyQt5.QtCore import QRect, pyqtSignal, QObject
from PyQt5.QtWidgets import *
from source.reapers import aurora_engine, pathologic, rdr2_audio, arx_fatalis


class MainWindow(QMainWindow):

    def __init__(self, run='arx'):
        super().__init__()
        self.resize(300, 300)
        self.setWindowTitle("Simple Reaper")
        self.centralwidget = QWidget(self)
        self.logWindow = QTextBrowser(self.centralwidget)
        self.logWindow.setGeometry(QRect(0, 0, 300, 300))
        self.setCentralWidget(self.centralwidget)
        sys.stdout = EmittingStream(text_written=self.append_text)
        self.out_dir = 'C:\\Users\\I\\Desktop\\unpack'

        match run:
            case 'aurora':
                self.test = aurora_engine.ERFUnpacker()
            case 'pathologic':
                self.test = pathologic.MorUnpacker()
            case 'rdr2':
                self.test = rdr2_audio.RDR2Audio()
            case 'arx':
                self.test = arx_fatalis.PakExtractor()

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

                file_name = QFileDialog.getOpenFileName(self, 'Open file', filter=f)[0]
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
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
