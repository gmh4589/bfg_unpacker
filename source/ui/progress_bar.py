
from PyQt6.QtCore import QRect, QMetaObject
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
from qt_material import apply_stylesheet

from source.ui import localize


class ProgressBar(QDialog):

    def __init__(self, style='dark_orange'):
        super().__init__()
        self.set_theme(style)
        self.resize(300, 130)
        self.setWindowIcon(QIcon('./source/ui/icons/i.ico'))
        self.setWindowTitle(f"{localize.wait}...")
        self.centralwidget = QWidget(self)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(10, 40, 270, 30))
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(10, 10, 280, 20))
        self.progress = QLabel(self.centralwidget)
        self.progress.setGeometry(QRect(10, 80, 100, 20))
        self.status = QLabel(self.centralwidget)
        self.status.setGeometry(QRect(10, 100, 500, 20))
        QMetaObject.connectSlotsByName(self)

    def set_theme(self, theme):
        apply_stylesheet(self, theme=f'{theme}.xml')
