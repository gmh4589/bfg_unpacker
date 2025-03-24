
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QLabel, QWidget, QDialog, QComboBox, QPushButton

from source.ui import localize

class TypeSelector(QDialog):

    def __init__(self, file_type_list):
        super().__init__()
        self.setWindowTitle(localize.tf_selector)
        self.returned_data = None

        self.resize(250, 120)
        self.setWindowIcon(QIcon('./data/icons/i.ico'))
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(8)
        self.centralwidget.setFont(self.font)

        self.label_selector = QLabel(self.centralwidget)
        self.label_selector.setGeometry(QRect(10, 10, 200, 30))
        self.label_selector.setText(localize.hand_select)

        self.file_type_selector = QComboBox(self.centralwidget)
        self.file_type_selector.addItems(key for key, value in file_type_list.items())
        self.file_type_selector.setGeometry(QRect(10, 40, 230, 30))

        self.ok_btn = QPushButton(self.centralwidget)
        self.ok_btn.clicked.connect(self.ok_action)
        self.ok_btn.setGeometry(QRect(10, 75, 110, 30))
        self.ok_btn.setText('OK')

        self.cancel_btn = QPushButton(self.centralwidget)
        self.cancel_btn.clicked.connect(self.close)
        self.cancel_btn.setGeometry(QRect(130, 75, 110, 30))
        self.cancel_btn.setText(localize.cancel)

    def ok_action(self):
        file_type = self.file_type_selector.currentText()
        print(file_type)
        self.returned_data = file_type
        self.close()
