
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import *
import configparser
from qt_material import apply_stylesheet

from source import theme_creator
import source.ui.localize as TL

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class SettingWindow(QDialog):

    def __init__(self, style='dark_orange'):
        super().__init__()
        apply_stylesheet(self, theme=f'{style}.xml')

        self.resize(300, 250)
        self.centralwidget = QWidget(self)
        self.label_engines = QLabel(self.centralwidget)
        self.label_engines.setGeometry(QRect(10, 10, 150, 20))
        self.label_sort = QLabel(self.centralwidget)
        self.label_sort.setGeometry(QRect(160, 10, 150, 20))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(10, 30, 140, 170))
        self.widget = QWidget(self.groupBox)
        self.widget.setGeometry(QRect(10, 10, 120, 150))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.checkBox = QCheckBox(self.widget)
        self.verticalLayout_2.addWidget(self.checkBox)
        self.checkBox_2 = QCheckBox(self.widget)
        self.verticalLayout_2.addWidget(self.checkBox_2)
        self.checkBox_3 = QCheckBox(self.widget)
        self.verticalLayout_2.addWidget(self.checkBox_3)
        self.checkBox_4 = QCheckBox(self.widget)
        self.verticalLayout_2.addWidget(self.checkBox_4)
        self.checkBox_5 = QCheckBox(self.widget)
        self.verticalLayout_2.addWidget(self.checkBox_5)
        self.checkBox_6 = QCheckBox(self.widget)
        self.verticalLayout_2.addWidget(self.checkBox_6)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QRect(160, 30, 130, 60))
        self.radioButton = QRadioButton(self.groupBox_2)
        self.radioButton.setGeometry(QRect(10, 10, 100, 20))
        self.radioButton_2 = QRadioButton(self.groupBox_2)
        self.radioButton_2.setGeometry(QRect(10, 35, 100, 20))
        self.checkBox_7 = QCheckBox(self.centralwidget)
        self.checkBox_7.setGeometry(QRect(10, 220, 200, 17))
        self.create_theme = QToolButton(self.centralwidget)
        self.create_theme.setGeometry(QRect(160, 100, 130, 25))
        self.out_folder = QToolButton(self.centralwidget)
        self.out_folder.setGeometry(QRect(160, 130, 130, 25))
        self.save_setting = QToolButton(self.centralwidget)
        self.save_setting.setGeometry(QRect(160, 160, 130, 25))
        self.cancel_button = QToolButton(self.centralwidget)
        self.cancel_button.setGeometry(QRect(160, 190, 130, 25))

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        self.cancel_button.clicked.connect(self.close)
        self.create_theme.clicked.connect(lambda: theme_creator.ThemeCreateWindow(style=style).exec())

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", TL.settings))
        self.checkBox.setText(_translate("MainWindow", "Unity"))
        self.checkBox_2.setText(_translate("MainWindow", "Unreal"))
        self.checkBox_3.setText(_translate("MainWindow", "RPG Maker"))
        self.checkBox_4.setText(_translate("MainWindow", "Game Maker"))
        self.checkBox_5.setText(_translate("MainWindow", "RenPy"))
        self.checkBox_6.setText(_translate("MainWindow", "Godot"))
        self.radioButton.setText(_translate("MainWindow", TL.by_name))
        self.radioButton_2.setText(_translate("MainWindow", TL.by_years))
        self.checkBox_7.setText(_translate("MainWindow", TL.context_menu))
        self.create_theme.setText(_translate("MainWindow", TL.create_theme))
        self.out_folder.setText(_translate("MainWindow", TL.out_folder))
        self.save_setting.setText(_translate("MainWindow", TL.apply))
        self.cancel_button.setText(_translate("MainWindow", TL.cancel))
        self.label_engines.setText(_translate("MainWindow", TL.show_on))
        self.label_sort.setText(_translate("MainWindow", TL.sort_by))
        # self.lang_label.setText(_translate("MainWindow", TL.language))
        # self.themes_label.setText(_translate("MainWindow", TL.themes))
