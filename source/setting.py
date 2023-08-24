
from PyQt5.QtWidgets import *
from PyQt5 import uic
from qt_material import apply_stylesheet
import configparser

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class SettingWindow(QMainWindow):

    def __init__(self):
        super(SettingWindow, self).__init__()
        self.window = uic.loadUi('./source/ui/setting.ui', self)
        apply_stylesheet(self.window, theme=f'dark_orange.xml')
        self.window.cancel_button.clicked.connect(self.close)
