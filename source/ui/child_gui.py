from PyQt5.QtCore import QRect, QCoreApplication, QMetaObject
from PyQt5.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *

from qt_material import apply_stylesheet
import configparser

from source.ui import resize
import source.ui.localize as TL

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class ChildUIWindow(QDialog):

    def __init__(self, style='dark_orange', gui_name='test_child',
                 label_list=None, action_list=None, default_list=None):

        super().__init__()
        apply_stylesheet(self, theme=f'{style}.xml')
        self.setWindowTitle(gui_name)
        drop_c = len(label_list)
        h = drop_c * 40 + 10 if drop_c > 1 else 90
        self.resize(resize.widget(400), resize.widget(h))
        self.setWindowIcon(QIcon('./source/ui/icons/i.ico'))
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(resize.widget(8))
        self.ok_button = QToolButton(self.centralwidget)
        self.ok_button.setGeometry(QRect(resize.widget(260), resize.widget((h / 2) - 40),
                                         resize.widget(130), resize.widget(30)))
        self.ok_button.text()
        self.cancel_button = QToolButton(self.centralwidget)
        self.cancel_button.setGeometry(QRect(resize.widget(260), resize.widget((h / 2)),
                                             resize.widget(130), resize.widget(30)))
        self.drops = []

        if label_list is not None:

            for x, label in enumerate(label_list):
                new_l = QLabel(self.centralwidget)
                new_l.setGeometry(QRect(resize.widget(5), resize.widget(40 * x + 10),
                                        resize.widget(90), resize.widget(30)))
                new_l.setText(f"{label}:")

            for i in range(drop_c):
                self.drops.append(QComboBox(self.centralwidget))
                filter_model = QStandardItemModel()
                self.drops[i].setGeometry(QRect(resize.widget(100), resize.widget(40 * i + 10),
                                                resize.widget(150), resize.widget(30)))

                for item in action_list[i]:
                    filter_model.appendRow(QStandardItem(item))

                self.drops[i].setModel(filter_model)
                self.drops[i].setCurrentText(default_list[i])

            self.retranslateUi()
            QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.ok_button.setText(_translate("MainWindow", "OK"))
        self.cancel_button.setText(_translate("MainWindow", TL.cancel))
