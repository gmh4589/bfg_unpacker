import sys
from PyQt5.QtCore import QRect, QObject, pyqtSignal, QThread, QMetaObject, Qt, QCoreApplication, QMutex
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class Ui_test(QMainWindow):

    def __init__(self):
        super().__init__()
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(10)
        self.centralwidget.setFont(self.font)
        self.centralwidget.setGeometry(0, 0, 200, 150)
        self.setWindowTitle("TEST")
        self.resize(200, 150)
        self.btn1 = QToolButton(self.centralwidget)
        self.btn1.setGeometry(QRect(10, 10, 180, 20))
        self.btn1.setText('OPEN')
        self.btn1.clicked.connect(self.some_func)
        self.logWindow = QTextBrowser(self.centralwidget)
        self.logWindow.setGeometry(QRect(10, 35, 180, 100))
        sys.stdout = EmittingStream(text_written=self.append_text)
        self.pb = ProgressBar()
        self.reader = Reader()
        self.files_to_process = []
        self.mutex = QMutex()

    def file_open(self):
        file_names = QFileDialog.getOpenFileNames(self)[0]

        for file_name in file_names:
            yield file_name

    def append_text(self, text):
        if text.strip():
            self.logWindow.append(text)

    def some_func(self):
        self.files_to_process = list(self.file_open())
        self.process_next_file()

    def process_next_file(self):
        if self.files_to_process:
            file_name = self.files_to_process.pop(0)
            print(file_name)
            self.q_connect(self.reader, file_name)

    def q_connect(self, nuke, fn=''):
        nuke.file_name = fn
        self.pb.progressBar.setValue(0)
        self.pb.show()
        nuke.update_signal.connect(self.update_progress)
        nuke.finished.connect(self.process_next_file)  # Connect to the finished signal of Reader
        nuke.start()

    def update_progress(self, pb_value, process_done):
        self.pb.progressBar.setValue(pb_value)

        if process_done:
            self.pb.close()


class Reader(QThread):
    update_signal = pyqtSignal(int, bool)

    def __init__(self):
        super().__init__()
        self.file_name = ''

    def run(self):
        with open(self.file_name, "r") as file:
            lines = file.readlines()
            line_count = len(lines)

            for i in range(line_count):
                print(lines[i])
                self.update_signal.emit(int(100 / line_count * (i + 1)), False)

            self.update_signal.emit(100, True)


class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))


class ProgressBar(QDialog):

    def __init__(self):
        super().__init__()
        self.resize(250, 50)
        self.setWindowTitle("Wait...")
        self.centralwidget = QWidget(self)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(10, 10, 230, 30)
        QMetaObject.connectSlotsByName(self)

    def update_info(self, pb_value):
        self.progressBar.setValue(pb_value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Ui_test()
    win.show()
    sys.exit(app.exec())
