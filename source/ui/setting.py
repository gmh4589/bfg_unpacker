import os
import winreg

import pandas
import sqlalchemy
from PyQt6.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt6.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import *
import configparser
from qt_material import apply_stylesheet

import source.ui.localize as translate
from source.ui import theme_creator
from source.ui.custom_ui import CustomDialog


class SettingWindow(QDialog):

    def __init__(self, style='dark_orange'):
        super().__init__()
        apply_stylesheet(self, theme=f'{style}.xml')
        self.setting = configparser.ConfigParser()
        self.setting.read(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini')

        engine = sqlalchemy.create_engine("sqlite:///game_base.db")

        with engine.connect() as conn:
            metadata = sqlalchemy.MetaData()

            def load_table(table_name):
                table = sqlalchemy.Table(table_name, metadata, autoload_with=engine)
                query = sqlalchemy.select(table)
                return len(pandas.read_sql_query(query, conn))

            self.unity_list = load_table('unity_list')
            self.unreal_list = load_table('unreal_list')
            self.renpy_list = load_table('renpy_list')
            self.gamemaker_list = load_table('gamemaker_list')
            self.rpgmaker_list = load_table('rpgmaker_list')
            self.godot_list = load_table('godot_list')

        self.resize(300, 350)
        self.setWindowIcon(QIcon('./data/icons/i.ico'))
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(8)
        self.centralwidget.setFont(self.font)
        self.label_engines = QLabel(self.centralwidget)
        self.label_engines.setGeometry(QRect(10, 10, 150, 20))
        self.label_sort = QLabel(self.centralwidget)
        self.label_sort.setGeometry(QRect(160, 10, 150, 20))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(10, 30, 145, 170))
        self.widget = QWidget(self.groupBox)
        self.widget.setGeometry(QRect(10, 10, 130, 150))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        # Unity checkbox
        self.unity_checkBox = QCheckBox(self.widget)
        self.unity_checkBox.setFont(self.font)
        self.unity_checkBox.setChecked(bool(int(self.setting['Engines']['unity'])))
        self.verticalLayout_2.addWidget(self.unity_checkBox)

        # Unreal checkbox
        self.unreal_checkBox = QCheckBox(self.widget)
        self.unreal_checkBox.setFont(self.font)
        self.unreal_checkBox.setChecked(bool(int(self.setting['Engines']['unreal'])))
        self.verticalLayout_2.addWidget(self.unreal_checkBox)

        # RPG Maker checkbox
        self.rpg_checkBox = QCheckBox(self.widget)
        self.rpg_checkBox.setFont(self.font)
        self.rpg_checkBox.setChecked(bool(int(self.setting['Engines']['rpg_maker'])))
        self.verticalLayout_2.addWidget(self.rpg_checkBox)

        # Game Maker checkbox
        self.gamemaker_checkBox = QCheckBox(self.widget)
        self.gamemaker_checkBox.setFont(self.font)
        self.gamemaker_checkBox.setChecked(bool(int(self.setting['Engines']['game_maker'])))
        self.verticalLayout_2.addWidget(self.gamemaker_checkBox)

        # RenPy checkbox
        self.renpy_checkBox = QCheckBox(self.widget)
        self.renpy_checkBox.setFont(self.font)
        self.renpy_checkBox.setChecked(bool(int(self.setting['Engines']['renpy'])))
        self.verticalLayout_2.addWidget(self.renpy_checkBox)

        # Godot checkbox
        self.godot_checkBox = QCheckBox(self.widget)
        self.godot_checkBox.setFont(self.font)
        self.godot_checkBox.setChecked(bool(int(self.setting['Engines']['godot'])))
        self.verticalLayout_2.addWidget(self.godot_checkBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QRect(160, 30, 130, 60))
        self.sort_by_names = QRadioButton(self.groupBox_2)
        self.sort_by_names.setFont(self.font)
        self.sort_by_names.setGeometry(QRect(10, 10, 100, 20))
        self.sort_by_years = QRadioButton(self.groupBox_2)
        self.sort_by_years.setFont(self.font)
        self.sort_by_years.setGeometry(QRect(10, 35, 100, 20))
        self.context_menu = QCheckBox(self.centralwidget)
        self.context_menu.setFont(self.font)
        self.context_menu.setGeometry(QRect(10, 200, 150, 40))
        self.context_menu.setChecked(bool(int(self.setting['Main']['context_menu'])))
        self.load_bar = QCheckBox(self.centralwidget)
        self.load_bar.setFont(self.font)
        self.load_bar.setGeometry(QRect(10, 240, 200, 20))
        self.load_bar.setChecked(bool(int(self.setting['Main']['load_bar'])))
        self.context_changed = self.context_menu.isChecked()

        # Favorite image format
        filter_model = QStandardItemModel()

        for item in ['png', 'bmp', 'tga', 'gif']:
            filter_model.appendRow(QStandardItem(item))

        self.fav_image_label = QLabel(self.centralwidget)
        self.fav_image_label.setFont(self.font)
        self.fav_image_label.setGeometry(QRect(160, 210, 120, 20))
        self.fav_image_drop = QComboBox(self.centralwidget)
        self.fav_image_drop.setFont(self.font)
        self.fav_image_drop.setGeometry(QRect(160, 240, 120, 20))
        self.fav_image_drop.setModel(filter_model)
        self.fav_image_drop.setCurrentText(self.setting['Main']['fav_format'])

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
            self.sort_by_names.setChecked(True)
        else:
            self.sort_by_years.setChecked(True)

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

            with open(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini', "w") as config_file:
                self.setting.write(config_file)

    def apply_setting(self, style):
        self.setting.set('Engines', 'unreal', "2" if self.unreal_checkBox.isChecked() else "0")
        self.setting.set('Engines', 'unity', "2" if self.unity_checkBox.isChecked() else "0")
        self.setting.set('Engines', 'rpg_maker', "2" if self.rpg_checkBox.isChecked() else "0")
        self.setting.set('Engines', 'game_maker', "2" if self.gamemaker_checkBox.isChecked() else "0")
        self.setting.set('Engines', 'godot', "2" if self.godot_checkBox.isChecked() else "0")
        self.setting.set('Engines', 'renpy', "2" if self.renpy_checkBox.isChecked() else "0")
        self.setting.set('Main', 'group', "name" if self.sort_by_names.isChecked() else "year")
        self.setting.set('Main', 'group_arch', "2" if self.arch_checkbox.isChecked() else "0")
        self.setting.set('Main', 'group_ge', "2" if self.ge_checkbox.isChecked() else "0")
        self.setting.set('Main', 'load_bar', "2" if self.load_bar.isChecked() else "0")
        self.setting.set('Main', 'fav_format', self.fav_image_drop.currentText())
        self.setting.set('Main', 'theme', style)

        if self.context_menu.isChecked() != self.context_changed:

            try:
                if self.context_menu.isChecked():
                    script_dir = os.path.dirname(os.path.abspath(__file__)).replace(r"\_internal\source\ui", "")

                    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r'*\shell\BFGUnp') as key:
                        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, 'Open with BFG Unpacker')
                        winreg.SetValueEx(key, 'Icon', 0, winreg.REG_SZ, f'{script_dir}\\data\\icons\\i.ico, 2')

                    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r'*\shell\BFGUnp\command') as key:
                        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, f'"{script_dir}\\bfg_unpacker.exe" "%1"')

                else:
                    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r'*\shell\BFGUnp\command')
                    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r'*\shell\BFGUnp')

                self.setting.set('Main', 'context_menu', "2" if self.context_menu.isChecked() else "0")

            except PermissionError:
                CustomDialog(title='WARNING!', text='To aplay setting run program as admin!').exec()
            except FileNotFoundError:
                self.setting.set('Main', 'context_menu', "0")

        with open(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini', "w") as config_file:
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

        self.sort_by_names.setText(_translate("MainWindow", translate.by_name))
        self.sort_by_years.setText(_translate("MainWindow", translate.by_years))
        self.context_menu.setText(_translate("MainWindow", translate.context_menu))
        self.load_bar.setText(_translate("MainWindow", translate.load_bar))
        self.create_theme.setText(_translate("MainWindow", translate.create_theme))
        self.out_folder.setText(_translate("MainWindow", translate.out_folder))
        self.save_setting.setText(_translate("MainWindow", translate.apply))
        self.cancel_button.setText(_translate("MainWindow", translate.cancel))
        self.label_engines.setText(_translate("MainWindow", translate.show_on))
        self.label_sort.setText(_translate("MainWindow", f'{translate.group_by}:'))
        self.label_alpha_group.setText(_translate("MainWindow", f'{translate.group_by} {translate.alphabet}:'))
        self.ge_checkbox.setText(_translate("MainMenu", translate.game_engines))
        self.arch_checkbox.setText(_translate("MainMenu", translate.archives))
        self.fav_image_label.setText(_translate("MainMenu", translate.fav_image_format))
