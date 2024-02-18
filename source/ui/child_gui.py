import os.path
from subprocess import Popen
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject
from PyQt6.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import *
from tkinter import simpledialog
from icecream import ic

from qt_material import apply_stylesheet
import configparser

import source.ui.localize as TL


class ChildUIWindow(QDialog):

    def __init__(self, style='', gui_name='test_child',
                 label_list=None, action_list=None, default_list=None,
                 ext_list='', action='', drop_a=False, item1=0, item2=1,
                 combos=''):

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
        self.command_line = ''
        self.ext_list = ext_list
        self.resize(400, h)
        self.setWindowIcon(QIcon('./source/ui/icons/i.ico'))
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(8)
        self.ok_button = QToolButton(self.centralwidget)
        self.ok_button.setFont(self.font)
        self.ok_button.clicked.connect(self.run_p)
        self.ok_button.setGeometry(QRect(260, int((h / 2) - 40), 130, 30))
        self.ok_button.text()
        self.cancel_button = QToolButton(self.centralwidget)
        self.cancel_button.setFont(self.font)
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setGeometry(QRect(260, int(h / 2), 130, 30))
        self.drops = [QComboBox(self.centralwidget) for _ in range(drop_c)]
        self.drop_a = drop_a
        self.combos = {} if not combos else combos
        self.item1 = item1
        self.item2 = item2

        if label_list is not None:

            for x, label in enumerate(label_list):
                new_l = QLabel(self.centralwidget)
                new_l.setGeometry(QRect(5, 40 * x + 10, 90, 30))
                new_l.setText(f"{label}: ")

            for i in range(drop_c):
                self.drops[i].setGeometry(QRect(100, 40 * i + 10, 120, 30))
                filter_model = QStandardItemModel()

                for item in action_list[i]:
                    filter_model.appendRow(QStandardItem(item))

                self.drops[i].setModel(filter_model)
                self.drops[i].setCurrentText(default_list[i])
                self.drops[i].currentTextChanged.connect(self.upvote)

            if self.drop_a:
                self.drops[item1].currentTextChanged.connect(self.drop_action)

            self.retranslateUi()
            QMetaObject.connectSlotsByName(self)

    def upvote(self):

        for j in range(len(self.label_list)):
            self.enter_other(j)

    def enter_other(self, drop_index):

        if self.drops[drop_index].currentText() == TL.other:
            text = simpledialog.askstring("", "Enter value:")
            ic(text)
            self.drops[drop_index].addItem(text)
            self.drops[drop_index].setCurrentText(text)

    def drop_action(self):
        selected_text = self.drops[self.item1].currentText()
        self.drops[self.item2].clear()
        ic(selected_text)
        self.drops[self.item2].addItems(self.combos.get(selected_text, [selected_text, TL.other]))

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
            self.command_line = self.action

            for file_name in self.file_open():

                if file_name:
                    out_name = os.path.basename(file_name).split('.')[-2]

                    for drop in range(len(self.drops)):
                        self.command_line = self.command_line.replace(f'%action_{drop}%', self.drops[drop].currentText())

                    self.command_line = (self.command_line
                                            .replace('%out_dir%', self.setting['Main']['out_path'])
                                            .replace('%file_name%', file_name)
                                            .replace('%out_name%', out_name)
                                            .replace('/', '\\')
                                            .replace('%x%', 'x' if self.drops[1] == 'Xbox One' else ''))

                    ic(self.command_line)
                    Popen(self.command_line).wait()
                    self.command_line = ''

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.ok_button.setText(_translate("MainWindow", TL.open_file))
        self.cancel_button.setText(_translate("MainWindow", TL.cancel))
