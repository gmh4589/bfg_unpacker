
from PyQt5.QtWidgets import *
from PyQt5 import uic
from qt_material import apply_stylesheet
import configparser

from source import theme_creator

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class SettingWindow(QMainWindow):

    def __init__(self, style='dark_orange'):
        super(SettingWindow, self).__init__()
        self.window = uic.loadUi('./source/ui/setting.ui', self)
        apply_stylesheet(self.window, theme=f'{style}.xml')
        self.window.cancel_button.clicked.connect(self.close)
        self.window.create_theme.clicked.connect(
            lambda: theme_creator.ThemeCreateWindow(style=style).show())
