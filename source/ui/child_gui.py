import os
from subprocess import Popen
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject, QThread
from PyQt6.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QDialog, QWidget, QToolButton, QLabel, QComboBox, QFileDialog
from tkinter import simpledialog
from icecream import ic

from qt_material import apply_stylesheet

from source.ui.custom_ui import AutoCompleteComboBox
from source.ui import localize
from source.setting import setting, theme


class ChildUIWindow(QDialog):

    def __init__(self, label_list=None, action_list=None, default_list=None, action=None, ok_run=None,
                 gui_name='test_child', ext_list='', drop_a=False, item1=0, item2=1, combos: str | dict=''):
        super().__init__()

        self.setting = setting
        apply_stylesheet(self, theme=f'{theme}.xml')
        self.setWindowTitle(gui_name)
        self.label_list = label_list
        self.drop_c = len(self.label_list)
        h = self.drop_c * 40 + 10 if self.drop_c > 1 else 90
        self.action = action
        self.action_list = action_list
        self.ext_list = ext_list
        self.setMinimumSize(400, h)
        self.setMaximumSize(400, h)
        self.setWindowIcon(QIcon('./data/icons/i.ico'))
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(8)
        self.cancel_button = QToolButton(self.centralwidget)
        self.cancel_button.setFont(self.font)
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setGeometry(QRect(260, int(h / 2), 130, 30))
        self.drops = []
        self.drop_a = drop_a
        self.combos = {} if not combos else combos
        self.item1 = item1
        self.item2 = item2
        self.outer = type(self.action) is str or None
        self.default_list = default_list
        self.set_items()
        
        self.ok_button = QToolButton(self.centralwidget)
        self.ok_button.setFont(self.font)
        self.ok_button.setGeometry(QRect(260, int((h / 2) - 40), 130, 30))
        self.ok_button.clicked.connect(self.run_p if ok_run is None else lambda *args, s=self.drops[0].currentText, c=self.close: ok_run(s, c))
        self.ok_button.text()
        self.retranslateUi()
        # self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)

    def set_items(self):
        if self.label_list is not None:

            for x, label in enumerate(self.label_list):
                new_l = QLabel(self.centralwidget)
                new_l.setGeometry(QRect(5, 40 * x + 10, 90, 30))
                new_l.setText(f"{label}: ")

            for i in range(self.drop_c):
                filter_model = QStandardItemModel()
                al = sorted(self.action_list[i].values()) if type(self.action_list[i]) is dict else self.action_list[i]

                for item in al:
                    filter_model.appendRow(QStandardItem(item))

                if len(al) > 100:
                    self.drops.append(AutoCompleteComboBox(self.centralwidget, items=al))
                    # self.drops[i].items = al
                else:
                    self.drops.append(QComboBox(self.centralwidget))

                self.drops[i].setGeometry(QRect(100, 40 * i + 10, 150, 30))
                self.drops[i].currentTextChanged.connect(self.upvote)
                self.drops[i].setModel(filter_model)
                self.drops[i].setCurrentText(self.default_list[i])

            if self.drop_a:
                self.drops[self.item1].currentTextChanged.connect(self.drop_action)


    def upvote(self):

        if len(self.drops) == len(self.label_list):

            for j in range(len(self.label_list)):

                if self.drops[j].currentText() == localize.other:
                    text = simpledialog.askstring("", localize.enter_value)
                    ic(text)
                    self.drops[j].addItem(text)
                    self.drops[j].setCurrentText(text)

    def drop_action(self):
        selected_text = self.drops[self.item1].currentText()
        self.drops[self.item2].clear()
        ic(selected_text)
        self.drops[self.item2].addItems(self.combos.get(selected_text, [selected_text, localize.other]))

    def file_open(self):

        try:
            f = self.ext_list.replace('|', ';;')
        except AttributeError:
            f = ''

        file_names = QFileDialog.getOpenFileNames(self, localize.open_file, filter=f,
                                                  directory=self.setting['Main']['last_dir'])[0]

        if file_names:

            for file_name in file_names:

                if file_name:
                    yield file_name

    def run_p(self):

        if self.action:
            fl = self.file_open()

            for file_name in fl:

                if file_name:
                    out_name = '.'.join(os.path.basename(file_name).split('.')[:-1])
                    file_name = file_name.replace('/', '\\')
                    self.close()

                    if self.outer:

                        for drop in range(len(self.drops)):

                            if type(self.action_list[drop]) is dict:
                                rev_list = {v: str(k) for k, v in self.action_list[drop].items()}
                                self.action = self.action.replace(f'%action_{drop}%',
                                                                  rev_list[self.drops[drop].currentText()])
                            else:
                                self.action = self.action.replace(f'%action_{drop}%',
                                                                  self.drops[drop].currentText())

                        self.action = (self.action
                                       .replace('%out_dir%', self.setting['Main']['out_path'])
                                       .replace('%file_name%', file_name)
                                       .replace('%out_name%', out_name)
                                       )

                        print(f'{localize.wait}, {localize.file} {file_name} {localize.is_process}...')
                        Popen(self.action).wait()

                    else:
                        args = {'file_name': file_name}

                        for drop in range(len(self.drops)):

                            match self.drops[drop].currentText():
                                case localize.yes:
                                    a = True
                                case localize.no:
                                    a = False
                                case _:
                                    a = self.drops[drop].currentText()

                            args[self.label_list[drop]] = a

                        QThread(self.action(**args)).run()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.ok_button.setText(_translate("MainWindow", localize.open_file))
        self.cancel_button.setText(_translate("MainWindow", localize.cancel))
