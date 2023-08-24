
from PyQt5.QtWidgets import *
from PyQt5 import uic
from qt_material import apply_stylesheet
import configparser
import sys

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class CBWindow(QMainWindow):

    def __init__(self, letter='', style='dark_orange'):
        super(CBWindow, self).__init__()
        self.window = uic.loadUi('./ui/change_buttons.ui', self)
        apply_stylesheet(self.window, theme=f'{style}.xml')
        print(letter)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(central_widget)

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXY"
        row, col = 0, 0

        for letter in alphabet:
            button = QToolButton(text=letter)
            button.setStyleSheet(open('./ui/buttons.css').read())
            grid_layout.addWidget(button, row, col)

            col += 1
            if col == 5:
                col = 0
                row += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CBWindow()
    window.show()
    sys.exit(app.exec_())