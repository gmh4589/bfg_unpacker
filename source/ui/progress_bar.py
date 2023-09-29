
from PyQt5.QtCore import QRect, QMetaObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet
import configparser

from source.ui import resize

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class ProgressBar(QDialog):

    def __init__(self, style='dark_orange'):
        super().__init__()
        self.set_theme(style)
        self.resize(resize.widget(300), resize.widget(130))
        self.setWindowIcon(QIcon('./source/ui/icons/i.ico'))
        self.setWindowTitle("Wait...")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(resize.widget(10), resize.widget(40), resize.widget(270), resize.widget(30)))
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(resize.widget(10), resize.widget(10), resize.widget(100), resize.widget(20)))
        self.progress = QLabel(self.centralwidget)
        self.progress.setGeometry(QRect(resize.widget(10), resize.widget(80), resize.widget(100), resize.widget(20)))
        self.status = QLabel(self.centralwidget)
        self.status.setGeometry(QRect(resize.widget(10), resize.widget(100), resize.widget(500), resize.widget(20)))

        QMetaObject.connectSlotsByName(self)

    def set_theme(self, theme):
        apply_stylesheet(self, theme=f'{theme}.xml')

    def update_info(self, pb_value, p_text, info):
        self.progressBar.setValue(pb_value)
        self.progress.setText(p_text)
        self.status.setText(info)
