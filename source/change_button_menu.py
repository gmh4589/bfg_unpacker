
from PyQt5.QtWidgets import *
from PyQt5 import uic
from qt_material import apply_stylesheet
import configparser
import sys

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class CBWindow(QMainWindow):

    def __init__(self, letter='A', style='dark_orange'):
        super(CBWindow, self).__init__()
        self.window = uic.loadUi('./source/ui/change_buttons.ui', self)
        apply_stylesheet(self.window, theme=f'{style}.xml')
        print(letter)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(central_widget)

        alphabet = "BCDEFGHIJKLMNOPQRSTUVWXY1"
        row, col = 0, 0

        for liter in alphabet:
            button = QToolButton(text=liter)
            button.setStyleSheet(open('./source/ui/buttons.css').read())
            grid_layout.addWidget(button, row, col)

            col += 1
            if col == 5:
                col = 0
                row += 1

