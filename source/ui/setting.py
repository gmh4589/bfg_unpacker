import pandas
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import *
import configparser
from qt_material import apply_stylesheet

import source.ui.localize as TL
from source.ui import resize, theme_creator


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

        self.resize(resize.widget(300), resize.widget(280))
        self.setWindowIcon(QIcon('./source/ui/icons/i.ico'))
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(resize.widget(8))
        self.centralwidget.setFont(self.font)
        self.label_engines = QLabel(self.centralwidget)
        self.label_engines.setGeometry(
            QRect(resize.widget(10), resize.widget(10), resize.widget(150), resize.widget(20)))
        self.label_sort = QLabel(self.centralwidget)
        self.label_sort.setGeometry(QRect(resize.widget(160), resize.widget(10), resize.widget(150), resize.widget(20)))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(resize.widget(10), resize.widget(30), resize.widget(145), resize.widget(170)))
        self.widget = QWidget(self.groupBox)
        self.widget.setGeometry(QRect(resize.widget(10), resize.widget(10), resize.widget(130), resize.widget(150)))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.unity_checkBox = QCheckBox(self.widget)
        self.unity_checkBox.setFont(self.font)
        self.unity_checkBox.setCheckState(int(self.setting['Engines']['unity']))
        self.verticalLayout_2.addWidget(self.unity_checkBox)
        self.unreal_checkBox = QCheckBox(self.widget)
        self.unreal_checkBox.setFont(self.font)
        self.unreal_checkBox.setCheckState(int(self.setting['Engines']['unreal']))
        self.verticalLayout_2.addWidget(self.unreal_checkBox)
        self.rpg_checkBox = QCheckBox(self.widget)
        self.rpg_checkBox.setFont(self.font)
        self.rpg_checkBox.setCheckState(int(self.setting['Engines']['rpg_maker']))
        self.verticalLayout_2.addWidget(self.rpg_checkBox)
        self.gamemaker_checkBox = QCheckBox(self.widget)
        self.gamemaker_checkBox.setFont(self.font)
        self.gamemaker_checkBox.setCheckState(int(self.setting['Engines']['game_maker']))
        self.verticalLayout_2.addWidget(self.gamemaker_checkBox)
        self.renpy_checkBox = QCheckBox(self.widget)
        self.renpy_checkBox.setFont(self.font)
        self.renpy_checkBox.setCheckState(int(self.setting['Engines']['renpy']))
        self.verticalLayout_2.addWidget(self.renpy_checkBox)
        self.godot_checkBox = QCheckBox(self.widget)
        self.godot_checkBox.setFont(self.font)
        self.godot_checkBox.setCheckState(int(self.setting['Engines']['godot']))
        self.verticalLayout_2.addWidget(self.godot_checkBox)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QRect(resize.widget(160), resize.widget(30),
                                          resize.widget(130), resize.widget(60)))
        self.radioButton = QRadioButton(self.groupBox_2)
        self.radioButton.setFont(self.font)
        self.radioButton.setGeometry(QRect(resize.widget(10), resize.widget(10),
                                           resize.widget(100), resize.widget(20)))
        self.radioButton_2 = QRadioButton(self.groupBox_2)
        self.radioButton_2.setFont(self.font)
        self.radioButton_2.setGeometry(QRect(resize.widget(10), resize.widget(35),
                                             resize.widget(100), resize.widget(20)))
        self.checkBox_7 = QCheckBox(self.centralwidget)
        self.checkBox_7.setFont(self.font)
        self.checkBox_7.setGeometry(QRect(resize.widget(10), resize.widget(220),
                                          resize.widget(200), resize.widget(20)))

        self.zoom_label = QLabel(self.centralwidget)
        self.zoom_label.setGeometry(QRect(resize.widget(10), resize.widget(250),
                                          resize.widget(90), resize.widget(20)))
        self.zoom_slider = QSlider(Qt.Horizontal, self.centralwidget)
        self.zoom_slider.setRange(0, 4)
        self.zoom_slider.setGeometry(QRect(resize.widget(100), resize.widget(250),
                                           resize.widget(190), resize.widget(20)))
        self.zoom_slider.setValue(int((float(self.setting['Main']['zoom']) - 1) / .25))
        self.zoom_slider.valueChanged.connect(lambda:
                                              self.zoom_label.setText(
                                                  f"{self.zoom_label.text().split(' ')[0]} "
                                                  f"{int((1 + int(self.zoom_slider.value()) * .25) * 100)}%"))

        self.create_theme = QToolButton(self.centralwidget)
        self.create_theme.setFont(self.font)
        self.create_theme.setGeometry(QRect(resize.widget(160), resize.widget(100),
                                            resize.widget(130), resize.widget(25)))
        self.out_folder = QToolButton(self.centralwidget)
        self.out_folder.setFont(self.font)
        self.out_folder.setGeometry(QRect(resize.widget(160), resize.widget(130),
                                          resize.widget(130), resize.widget(25)))
        self.save_setting = QToolButton(self.centralwidget)
        self.save_setting.setFont(self.font)
        self.save_setting.setGeometry(QRect(resize.widget(160), resize.widget(160),
                                            resize.widget(130), resize.widget(25)))
        self.cancel_button = QToolButton(self.centralwidget)
        self.cancel_button.setFont(self.font)
        self.cancel_button.setGeometry(QRect(resize.widget(160), resize.widget(190),
                                             resize.widget(130), resize.widget(25)))

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
        global setting
        out_path = QFileDialog.getExistingDirectory(self, caption=TL.select_folder,
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
        self.setting.set('Main', 'zoom', str(1 + int(self.zoom_slider.value()) * .25))
        self.setting.set('Main', 'theme', style)

        with open('./setting.ini', "w") as config_file:
            self.setting.write(config_file)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", TL.settings))
        self.unity_checkBox.setText(_translate("MainWindow", f"Unity ({self.unity_list})"))
        self.unreal_checkBox.setText(_translate("MainWindow", f"Unreal ({self.unreal_list})"))
        self.rpg_checkBox.setText(_translate("MainWindow", f"RPG Maker ({self.rpgmaker_list})"))
        self.gamemaker_checkBox.setText(_translate("MainWindow", f"GameMaker ({self.gamemaker_list})"))
        self.renpy_checkBox.setText(_translate("MainWindow", f"RenPy ({self.renpy_list})"))
        self.godot_checkBox.setText(_translate("MainWindow", f"Godot ({self.godot_list})"))
        self.radioButton.setText(_translate("MainWindow", TL.by_name))
        self.radioButton_2.setText(_translate("MainWindow", TL.by_years))
        self.checkBox_7.setText(_translate("MainWindow", TL.context_menu))
        self.create_theme.setText(_translate("MainWindow", TL.create_theme))
        self.out_folder.setText(_translate("MainWindow", TL.out_folder))
        self.save_setting.setText(_translate("MainWindow", TL.apply))
        self.cancel_button.setText(_translate("MainWindow", TL.cancel))
        self.label_engines.setText(_translate("MainWindow", TL.show_on))
        self.label_sort.setText(_translate("MainWindow", TL.sort_by))
        self.zoom_label.setText(_translate("MainWindow", f"{TL.zoom} {int(float(self.setting['Main']['zoom']) * 100)}%"))
