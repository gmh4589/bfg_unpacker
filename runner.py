
import sys

from PyQt5.QtCore import QRect, pyqtSignal, QObject
from PyQt5.QtWidgets import *
from source.reapers import aurora_engine, pathologic, rdr2_audio, seven_s_seven


class MainWindow(QMainWindow):

    def __init__(self, run='7x7'):
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
                self.test = aurora_engine.ERFUnpacker(self.out_dir)
            case 'pathologic':
                self.test = pathologic.MorUnpacker(self.out_dir)
            case 'rdr2':
                self.test = rdr2_audio.RDR2Audio(self.out_dir)
            case '7x7':
                self.test = seven_x_seven.Seven(self.out_dir)

        self.test.file_name = self.file_open()

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
