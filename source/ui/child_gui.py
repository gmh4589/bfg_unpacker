import os.path
from subprocess import Popen
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject
from PyQt6.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import *
from tkinter import simpledialog
from icecream import ic

from qt_material import apply_stylesheet
import configparser

from source.ui import resize
import source.ui.localize as TL


class ChildUIWindow(QDialog):

    def __init__(self, style='dark_orange', gui_name='test_child',
                 label_list=None, action_list=None, default_list=None,
                 ext_list='', action=''):

        super().__init__()

        self.setting = configparser.ConfigParser()
        self.setting.read('./setting.ini')
        apply_stylesheet(self, theme=f'{style}.xml')
        self.style = style
        self.gui_name = gui_name
        self.setWindowTitle(gui_name)
        self.label_list = label_list
        drop_c = len(label_list)
        h = drop_c * 40 + 10 if drop_c > 1 else 90
        self.action = action
        self.ext_list = ext_list
        self.resize(resize.widget(400), resize.widget(h))
        self.setWindowIcon(QIcon('./source/ui/icons/i.ico'))
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(resize.widget(8))
        self.ok_button = QToolButton(self.centralwidget)
        self.ok_button.setFont(self.font)
        self.ok_button.clicked.connect(self.run_p)
        self.ok_button.setGeometry(QRect(resize.widget(260), resize.widget((h / 2) - 40),
                                         resize.widget(130), resize.widget(30)))
        self.ok_button.text()
        self.cancel_button = QToolButton(self.centralwidget)
        self.cancel_button.setFont(self.font)
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setGeometry(QRect(resize.widget(260), resize.widget((h / 2)),
                                             resize.widget(130), resize.widget(30)))
        self.drops = [QComboBox(self.centralwidget) for _ in range(drop_c)]

        if label_list is not None:

            for x, label in enumerate(label_list):
                new_l = QLabel(self.centralwidget)
                new_l.setGeometry(QRect(resize.widget(5), resize.widget(40 * x + 10),
                                        resize.widget(90), resize.widget(30)))
                new_l.setText(f"{label}: ")

            for i in range(drop_c):
                self.drops[i].setGeometry(QRect(resize.widget(100), resize.widget(40 * i + 10),
                                                resize.widget(150), resize.widget(30)))
                filter_model = QStandardItemModel()

                for item in action_list[i]:
                    filter_model.appendRow(QStandardItem(item))

                self.drops[i].setModel(filter_model)
                self.drops[i].setCurrentText(default_list[i])
                self.drops[i].currentTextChanged.connect(self.upvote)

            if self.gui_name == 'PlayStation Audio Tools':
                self.drops[0].currentTextChanged.connect(self.drop_action)

            self.retranslateUi()
            QMetaObject.connectSlotsByName(self)

    def upvote(self):

        for j in range(len(self.label_list)):
            self.enter_other(j)

    def enter_other(self, drop_index):
        ic(drop_index)

        if self.drops[drop_index].currentText() == TL.other:
            text = simpledialog.askstring("", "Enter value:")
            ic(text)
            self.drops[drop_index].addItem(text)
            self.drops[drop_index].setCurrentText(text)

    def drop_action(self):

        if self.gui_name == 'PlayStation Audio Tools':
            second_combobox_items = {
                'PS2': ['VAG2WAV', 'WAV2VAG', 'PS2_SoundBank'],
                'PS3': ['Atrac2WAV', 'WAV2Atrac', 'MSF2Atrac'],
                'PS4': ['Atrac2WAV', 'WAV2Atrac', 'SXD2Atrac'],
                'PSP': ['Atrac2WAV', 'WAV2Atrac'],
                'PS Vita': ['Atrac2WAV', 'WAV2Atrac']
            }

            selected_text = self.drops[0].currentText()
            self.drops[1].clear()
            self.drops[1].addItems(second_combobox_items.get(selected_text, []))

    def file_open(self):

        try:
            f = self.ext_list.replace('|', ';;')
        except AttributeError:
            f = ''

        file_names = QFileDialog.getOpenFileNames(self, TL.open_file, filter=f,
                                                  directory=self.setting['Main']['last_dir'])[0]
        if file_names:

            for file_name in file_names:

                if file_name:
                    yield file_name

    def run_p(self):

        if self.action:

            for file_name in self.file_open():

                if file_name:
                    out_name = os.path.basename(file_name).split('.')[-2]

                    for drop in range(len(self.drops)):
                        self.action = self.action.replace(f'%action_{drop}%', self.drops[drop].currentText())

                    action = (self.action
                                  .replace('%out_dir%', self.setting['Main']['out_path'])
                                  .replace('%file_name%', file_name)
                                  .replace('%out_name%', out_name))
                    ic(action)
                    Popen(action).wait()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.ok_button.setText(_translate("MainWindow", "OK"))
        self.cancel_button.setText(_translate("MainWindow", TL.cancel))
