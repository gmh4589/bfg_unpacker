import pandas
from PyQt6.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import *
import configparser
from qt_material import apply_stylesheet

import source.ui.localize as translate
from source.ui import theme_creator


class SettingWindow(QDialog):

    unity_list = len(pandas.read_csv('./game_list/unity_list.csv', delimiter='\t'))
    unreal_list = len(pandas.read_csv('./game_list/unreal_list.csv', delimiter='\t'))
    renpy_list = len(pandas.read_csv('./game_list/renpy_list.csv', delimiter='\t'))
    gamemaker_list = len(pandas.read_csv('./game_list/gamemaker_list.csv', delimiter='\t'))
    rpgmaker_list = len(pandas.read_csv('./game_list/rpgmaker_list.csv', delimiter='\t'))
    godot_list = len(pandas.read_csv('./game_list/godot_list.csv', delimiter='\t'))

    def __init__(self, style='dark_orange'):
        super().__init__()
        apply_stylesheet(self, theme=f'{style}.xml')
        self.setting = configparser.ConfigParser()
        self.setting.read('./setting.ini')

        self.resize(300, 350)
        self.setWindowIcon(QIcon('./data/icons/i.ico'))
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(8)
        self.centralwidget.setFont(self.font)
        self.label_engines = QLabel(self.centralwidget)
        self.label_engines.setGeometry(
            QRect(10, 10, 150, 20))
        self.label_sort = QLabel(self.centralwidget)
        self.label_sort.setGeometry(QRect(160, 10, 150, 20))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(10, 30, 145, 170))
        self.widget = QWidget(self.groupBox)
        self.widget.setGeometry(QRect(10, 10, 130, 150))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.unity_checkBox = QCheckBox(self.widget)
        self.unity_checkBox.setFont(self.font)
        self.unity_checkBox.setChecked(bool(int(self.setting['Engines']['unity'])))
        self.verticalLayout_2.addWidget(self.unity_checkBox)
        self.unreal_checkBox = QCheckBox(self.widget)
        self.unreal_checkBox.setFont(self.font)
        self.unreal_checkBox.setChecked(bool(int(self.setting['Engines']['unreal'])))
        self.verticalLayout_2.addWidget(self.unreal_checkBox)
        self.rpg_checkBox = QCheckBox(self.widget)
        self.rpg_checkBox.setFont(self.font)
        self.rpg_checkBox.setChecked(bool(int(self.setting['Engines']['rpg_maker'])))
        self.verticalLayout_2.addWidget(self.rpg_checkBox)
        self.gamemaker_checkBox = QCheckBox(self.widget)
        self.gamemaker_checkBox.setFont(self.font)
        self.gamemaker_checkBox.setChecked(bool(int(self.setting['Engines']['game_maker'])))
        self.verticalLayout_2.addWidget(self.gamemaker_checkBox)
        self.renpy_checkBox = QCheckBox(self.widget)
        self.renpy_checkBox.setFont(self.font)
        self.renpy_checkBox.setChecked(bool(int(self.setting['Engines']['renpy'])))
        self.verticalLayout_2.addWidget(self.renpy_checkBox)
        self.godot_checkBox = QCheckBox(self.widget)
        self.godot_checkBox.setFont(self.font)
        self.godot_checkBox.setChecked(bool(int(self.setting['Engines']['godot'])))
        self.verticalLayout_2.addWidget(self.godot_checkBox)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QRect(160, 30, 130, 60))
        self.radioButton = QRadioButton(self.groupBox_2)
        self.radioButton.setFont(self.font)
        self.radioButton.setGeometry(QRect(10, 10, 100, 20))
        self.radioButton_2 = QRadioButton(self.groupBox_2)
        self.radioButton_2.setFont(self.font)
        self.radioButton_2.setGeometry(QRect(10, 35, 100, 20))
        self.checkBox_7 = QCheckBox(self.centralwidget)
        self.checkBox_7.setFont(self.font)
        self.checkBox_7.setGeometry(QRect(10, 220, 200, 20))

        self.label_alpha_group = QLabel(self.centralwidget)
        self.label_alpha_group.setGeometry(QRect(160, 100, 120, 30))

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QRect(160, 135, 130, 60))
        self.arch_checkbox = QCheckBox(self.groupBox_3)
        self.arch_checkbox.setGeometry(QRect(10, 10, 120, 20))
        self.arch_checkbox.setChecked(bool(int(self.setting['Main']['group_arch'])))
        self.ge_checkbox = QCheckBox(self.groupBox_3)
        self.ge_checkbox.setGeometry(QRect(10, 35, 120, 20))
        self.ge_checkbox.setChecked(bool(int(self.setting['Main']['group_ge'])))

        self.create_theme = QToolButton(self.centralwidget)
        self.create_theme.setFont(self.font)
        self.create_theme.setGeometry(QRect(10, 280, 135, 25))
        self.out_folder = QToolButton(self.centralwidget)
        self.out_folder.setFont(self.font)
        self.out_folder.setGeometry(QRect(10, 310, 135, 25))
        self.save_setting = QToolButton(self.centralwidget)
        self.save_setting.setFont(self.font)
        self.save_setting.setGeometry(QRect(155, 280, 135, 25))
        self.cancel_button = QToolButton(self.centralwidget)
        self.cancel_button.setFont(self.font)
        self.cancel_button.setGeometry(QRect(155, 310,  135, 25))

        if self.setting['Main']['group'] == 'name':
            self.radioButton.setChecked(True)
        else:
            self.radioButton_2.setChecked(True)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        self.out_folder.clicked.connect(self.select)
        self.cancel_button.clicked.connect(self.close)
        self.create_theme.clicked.connect(lambda: theme_creator.ThemeCreateWindow(style=style).exec())
        self.save_setting.clicked.connect(lambda: self.apply_setting(style))

    def select(self):
        out_path = QFileDialog.getExistingDirectory(self, caption=translate.select_folder,
                                                    directory=self.setting['Main']['last_dir'])

        if out_path:
            self.setting.set('Main', 'out_path', out_path)
            self.setting.set('Main', 'last_dir', out_path)

            with open('./setting.ini', "w") as config_file:
                self.setting.write(config_file)

    def apply_setting(self, style):
        self.setting.set('Engines', 'unreal', "2" if self.unreal_checkBox.isChecked() else "0")
        self.setting.set('Engines', 'unity', "2" if self.unity_checkBox.isChecked() else "0")
        self.setting.set('Engines', 'rpg_maker', "2" if self.rpg_checkBox.isChecked() else "0")
        self.setting.set('Engines', 'game_maker', "2" if self.gamemaker_checkBox.isChecked() else "0")
        self.setting.set('Engines', 'godot', "2" if self.godot_checkBox.isChecked() else "0")
        self.setting.set('Engines', 'renpy', "2" if self.renpy_checkBox.isChecked() else "0")
        self.setting.set('Main', 'group', "name" if self.radioButton.isChecked() else "year")
        self.setting.set('Main', 'group_arch', "2" if self.arch_checkbox.isChecked() else "0")
        self.setting.set('Main', 'group_ge', "2" if self.ge_checkbox.isChecked() else "0")
        self.setting.set('Main', 'theme', style)

        with open('./setting.ini', "w") as config_file:
            self.setting.write(config_file)

        self.cancel_button.setText(translate.close)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", translate.settings))
        self.unity_checkBox.setText(_translate("MainWindow", f"Unity ({self.unity_list})"))
        self.unreal_checkBox.setText(_translate("MainWindow", f"Unreal ({self.unreal_list})"))
        self.rpg_checkBox.setText(_translate("MainWindow", f"RPG Maker ({self.rpgmaker_list})"))
        self.gamemaker_checkBox.setText(_translate("MainWindow", f"GameMaker ({self.gamemaker_list})"))
        self.renpy_checkBox.setText(_translate("MainWindow", f"RenPy ({self.renpy_list})"))
        self.godot_checkBox.setText(_translate("MainWindow", f"Godot ({self.godot_list})"))
        self.radioButton.setText(_translate("MainWindow", translate.by_name))
        self.radioButton_2.setText(_translate("MainWindow", translate.by_years))
        self.checkBox_7.setText(_translate("MainWindow", translate.context_menu))
        self.create_theme.setText(_translate("MainWindow", translate.create_theme))
        self.out_folder.setText(_translate("MainWindow", translate.out_folder))
        self.save_setting.setText(_translate("MainWindow", translate.apply))
        self.cancel_button.setText(_translate("MainWindow", translate.cancel))
        self.label_engines.setText(_translate("MainWindow", translate.show_on))
        self.label_sort.setText(_translate("MainWindow", f'{translate.group_by}:'))
        self.label_alpha_group.setText(_translate("MainWindow", f'{translate.group_by} {translate.alphabet}:'))
        self.ge_checkbox.setText(_translate("MainMenu", translate.game_engines))
        self.arch_checkbox.setText(_translate("MainMenu", translate.archives))
