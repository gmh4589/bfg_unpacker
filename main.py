
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5 import uic
from qt_material import apply_stylesheet
from qt_material import list_themes
import configparser
import pandas
from pprint import pprint

pprint(list_themes())
setting = configparser.ConfigParser()
setting.read('./setting.ini')
print(setting["Main"]["theme"])


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.mainList = pandas.read_csv('./game_list/main_list.csv', delimiter='\t')
        pprint(self.mainList)

        window = uic.loadUi('./source/ui/main.ui', self)
        window.menubar.setStyleSheet(open('./source/ui/styles.css').read())
        window.checkBox.setStyleSheet(open('./source/ui/styles.css').read())
        window.checkBox_2.setStyleSheet(open('./source/ui/styles.css').read())
        window.checkBox_3.setStyleSheet(open('./source/ui/styles.css').read())
        apply_stylesheet(window, theme=f'{setting["Main"]["theme"]}.xml')
        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.parent_list = {}

        for i in range(15):
            btn = QToolButton(text=self.abc[i])
            btn.setStyleSheet(open('./source/ui/styles.css').read())
            window.upperButtons.addWidget(btn)

        model = QStandardItemModel()
        root_item = model.invisibleRootItem()
        newParent = QStandardItem('0-9')
        self.parent_list['0-9'] = newParent
        root_item.appendRow(newParent)

        for item in self.abc:
            newParent = QStandardItem(item)
            self.parent_list[item] = newParent
            root_item.appendRow(newParent)

        newParent = QStandardItem('Other')
        self.parent_list['Other'] = newParent
        root_item.appendRow(newParent)
        self.all_games = 0

        for name in self.mainList['game_name']:

            if name[0].upper() in '0123456789':
                literal = '0-9'
            elif name[0].upper() in self.abc:
                literal = name[0].upper()
            else:
                literal = 'Other'

            child = QStandardItem(name)
            self.parent_list[literal].appendRow(child)
            self.all_games += 1

        pprint(self.parent_list)
        window.treeView.setModel(model)
        window.treeView.setStyleSheet(open('./source/ui/styles.css').read())
        model.setHeaderData(0, Qt.Horizontal, "Выберите игру, приложение\nили тип файла")
        window.all_games_label.setText(f'Всего игр: {self.all_games}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
