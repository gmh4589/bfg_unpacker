
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import *
import configparser
from qt_material import apply_stylesheet
from qt_material import list_themes

from source import theme_creator

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class SettingWindow(QDialog):

    def __init__(self, style='dark_orange'):
        super().__init__()
        apply_stylesheet(self, theme=f'{style}.xml')

        self.resize(303, 330)
        self.centralwidget = QWidget(self)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(10, 110, 141, 181))
        self.widget = QWidget(self.groupBox)
        self.widget.setGeometry(QRect(10, 20, 121, 151))
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
        self.groupBox_2.setGeometry(QRect(160, 110, 130, 60))
        self.radioButton = QRadioButton(self.groupBox_2)
        self.radioButton.setGeometry(QRect(10, 20, 100, 17))
        self.radioButton_2 = QRadioButton(self.groupBox_2)
        self.radioButton_2.setGeometry(QRect(10, 40, 100, 17))
        self.checkBox_7 = QCheckBox(self.centralwidget)
        self.checkBox_7.setGeometry(QRect(10, 300, 200, 17))
        self.create_theme = QToolButton(self.centralwidget)
        self.create_theme.setGeometry(QRect(160, 180, 130, 25))
        self.out_folder = QToolButton(self.centralwidget)
        self.out_folder.setGeometry(QRect(160, 210, 130, 25))
        self.save_setting = QToolButton(self.centralwidget)
        self.save_setting.setGeometry(QRect(160, 240, 130, 25))
        self.cancel_button = QToolButton(self.centralwidget)
        self.cancel_button.setGeometry(QRect(160, 270, 130, 25))
        self.widget1 = QWidget(self.centralwidget)
        self.widget1.setGeometry(QRect(10, 10, 280, 86))
        self.verticalLayout = QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lang_label = QLabel(self.widget1)
        self.verticalLayout.addWidget(self.lang_label)
        self.lang_box = QComboBox(self.widget1)
        self.verticalLayout.addWidget(self.lang_box)
        self.themes_label = QLabel(self.widget1)
        self.verticalLayout.addWidget(self.themes_label)
        self.themes_box = QComboBox(self.widget1)
        self.themes_box.addItems(theme.replace('_', ' ').title().split('.')[0] for theme in list_themes())
        self.verticalLayout.addWidget(self.themes_box)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        self.cancel_button.clicked.connect(self.close)
        self.create_theme.clicked.connect(lambda: theme_creator.ThemeCreateWindow(style=style).show())

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Показать игры на"))
        self.checkBox.setText(_translate("MainWindow", "Unity"))
        self.checkBox_2.setText(_translate("MainWindow", "Unreal"))
        self.checkBox_3.setText(_translate("MainWindow", "RPG Maker"))
        self.checkBox_4.setText(_translate("MainWindow", "Game Maker"))
        self.checkBox_5.setText(_translate("MainWindow", "RenPy"))
        self.checkBox_6.setText(_translate("MainWindow", "Godot"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Группировать по"))
        self.radioButton.setText(_translate("MainWindow", "Названию"))
        self.radioButton_2.setText(_translate("MainWindow", "Году выхода"))
        self.checkBox_7.setText(_translate("MainWindow", "Пункт в контекстном меню"))
        self.create_theme.setText(_translate("MainWindow", "Создать тему"))
        self.out_folder.setText(_translate("MainWindow", "Выходная папка"))
        self.save_setting.setText(_translate("MainWindow", "Применить"))
        self.cancel_button.setText(_translate("MainWindow", "Отмена"))
        self.lang_label.setText(_translate("MainWindow", "Язык/Language"))
        self.themes_label.setText(_translate("MainWindow", "Тема"))
