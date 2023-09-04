
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import configparser
from qt_material import apply_stylesheet

import source.ui.localize as TL
from source.ui import resize, theme_creator

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class SettingWindow(QDialog):

    def __init__(self, style='dark_orange'):
        super().__init__()
        apply_stylesheet(self, theme=f'{style}.xml')

        self.resize(resize.widget(300), resize.widget(250))
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(resize.widget(8))
        self.centralwidget.setFont(self.font)
        self.label_engines = QLabel(self.centralwidget)
        self.label_engines.setGeometry(QRect(resize.widget(10), resize.widget(10), resize.widget(150), resize.widget(20)))
        self.label_sort = QLabel(self.centralwidget)
        self.label_sort.setGeometry(QRect(resize.widget(160), resize.widget(10), resize.widget(150), resize.widget(20)))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(resize.widget(10), resize.widget(30), resize.widget(140), resize.widget(170)))
        self.widget = QWidget(self.groupBox)
        self.widget.setGeometry(QRect(resize.widget(10), resize.widget(10), resize.widget(120), resize.widget(150)))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.unity_checkBox = QCheckBox(self.widget)
        self.unity_checkBox.setFont(self.font)
        self.unity_checkBox.setCheckState(int(setting['Engines']['unity']))
        self.verticalLayout_2.addWidget(self.unity_checkBox)
        self.unreal_checkBox = QCheckBox(self.widget)
        self.unreal_checkBox.setFont(self.font)
        self.unreal_checkBox.setCheckState(int(setting['Engines']['unreal']))
        self.verticalLayout_2.addWidget(self.unreal_checkBox)
        self.rpg_checkBox = QCheckBox(self.widget)
        self.rpg_checkBox.setFont(self.font)
        self.rpg_checkBox.setCheckState(int(setting['Engines']['rpg_maker']))
        self.verticalLayout_2.addWidget(self.rpg_checkBox)
        self.gamemaker_checkBox = QCheckBox(self.widget)
        self.gamemaker_checkBox.setFont(self.font)
        self.gamemaker_checkBox.setCheckState(int(setting['Engines']['game_maker']))
        self.verticalLayout_2.addWidget(self.gamemaker_checkBox)
        self.renpy_checkBox = QCheckBox(self.widget)
        self.renpy_checkBox.setFont(self.font)
        self.renpy_checkBox.setCheckState(int(setting['Engines']['renpy']))
        self.verticalLayout_2.addWidget(self.renpy_checkBox)
        self.godot_checkBox = QCheckBox(self.widget)
        self.godot_checkBox.setFont(self.font)
        self.godot_checkBox.setCheckState(int(setting['Engines']['godot']))
        self.verticalLayout_2.addWidget(self.godot_checkBox)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QRect(resize.widget(160), resize.widget(30), resize.widget(130), resize.widget(60)))
        self.radioButton = QRadioButton(self.groupBox_2)
        self.radioButton.setFont(self.font)
        self.radioButton.setGeometry(QRect(resize.widget(10), resize.widget(10), resize.widget(100), resize.widget(20)))
        self.radioButton_2 = QRadioButton(self.groupBox_2)
        self.radioButton_2.setFont(self.font)
        self.radioButton_2.setGeometry(QRect(resize.widget(10), resize.widget(35), resize.widget(100), resize.widget(20)))
        self.checkBox_7 = QCheckBox(self.centralwidget)
        self.checkBox_7.setFont(self.font)
        self.checkBox_7.setGeometry(QRect(resize.widget(10), resize.widget(220), resize.widget(200), resize.widget(20)))
        self.create_theme = QToolButton(self.centralwidget)
        self.create_theme.setFont(self.font)
        self.create_theme.setGeometry(QRect(resize.widget(160), resize.widget(100), resize.widget(130), resize.widget(25)))
        self.out_folder = QToolButton(self.centralwidget)
        self.out_folder.setFont(self.font)
        self.out_folder.setGeometry(QRect(resize.widget(160), resize.widget(130), resize.widget(130), resize.widget(25)))
        self.save_setting = QToolButton(self.centralwidget)
        self.save_setting.setFont(self.font)
        self.save_setting.setGeometry(QRect(resize.widget(160), resize.widget(160), resize.widget(130), resize.widget(25)))
        self.cancel_button = QToolButton(self.centralwidget)
        self.cancel_button.setFont(self.font)
        self.cancel_button.setGeometry(QRect(resize.widget(160), resize.widget(190), resize.widget(130), resize.widget(25)))

        if setting['Main']['group'] == 'name':
            self.radioButton.setChecked(True)
        else:
            self.radioButton_2.setChecked(True)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        self.cancel_button.clicked.connect(self.close)
        self.create_theme.clicked.connect(lambda: theme_creator.ThemeCreateWindow(style=style).exec())
        self.save_setting.clicked.connect(self.apply_setting)

    def apply_setting(self):
        setting.set('Engines', 'unreal', "2" if self.unreal_checkBox.isChecked() else "0")
        setting.set('Engines', 'unity', "2" if self.unity_checkBox.isChecked() else "0")
        setting.set('Engines', 'rpg_maker', "2" if self.rpg_checkBox.isChecked() else "0")
        setting.set('Engines', 'game_maker', "2" if self.gamemaker_checkBox.isChecked() else "0")
        setting.set('Engines', 'godot', "2" if self.godot_checkBox.isChecked() else "0")
        setting.set('Engines', 'renpy', "2" if self.renpy_checkBox.isChecked() else "0")
        setting.set('Main', 'group', "name" if self.radioButton.isChecked() else "year")

        with open('./setting.ini', "w") as config_file:
            setting.write(config_file)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", TL.settings))
        self.unity_checkBox.setText(_translate("MainWindow", "Unity"))
        self.unreal_checkBox.setText(_translate("MainWindow", "Unreal"))
        self.rpg_checkBox.setText(_translate("MainWindow", "RPG Maker"))
        self.gamemaker_checkBox.setText(_translate("MainWindow", "Game Maker"))
        self.renpy_checkBox.setText(_translate("MainWindow", "RenPy"))
        self.godot_checkBox.setText(_translate("MainWindow", "Godot"))
        self.radioButton.setText(_translate("MainWindow", TL.by_name))
        self.radioButton_2.setText(_translate("MainWindow", TL.by_years))
        self.checkBox_7.setText(_translate("MainWindow", TL.context_menu))
        self.create_theme.setText(_translate("MainWindow", TL.create_theme))
        self.out_folder.setText(_translate("MainWindow", TL.out_folder))
        self.save_setting.setText(_translate("MainWindow", TL.apply))
        self.cancel_button.setText(_translate("MainWindow", TL.cancel))
        self.label_engines.setText(_translate("MainWindow", TL.show_on))
        self.label_sort.setText(_translate("MainWindow", TL.sort_by))
