
from PyQt5.QtCore import QRect, QMetaObject
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet


class ProgressBar(QDialog):

    def __init__(self, style='dark_orange', header=''):
        super().__init__()
        apply_stylesheet(self, theme=f'{style}.xml')
        self.resize(300, 130)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(10, 40, 270, 30))
        self.progressBar.setProperty("value", 24)
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(10, 10, 100, 20))
        self.header.setText(header)
        self.progress = QLabel(self.centralwidget)
        self.progress.setGeometry(QRect(10, 80, 100, 20))
        self.status = QLabel(self.centralwidget)
        self.status.setGeometry(QRect(10, 100, 500, 20))
        # self.setCentralWidget(self.centralwidget)

        QMetaObject.connectSlotsByName(self)

    def update_info(self, pb_value, p_text, info):
        self.progressBar.setValue(pb_value)
        self.progress.setText(p_text)
        self.status.setText(info)
