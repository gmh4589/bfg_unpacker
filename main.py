
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic
from qt_material import apply_stylesheet
from qt_material import list_themes
import configparser
import pandas

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.window = uic.loadUi('./source/ui/main.ui', self)
        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.parent_list = {}
        self.themes_list_create()
        self.buttons_create()
        self.tree_view_create()
        self.archive_list_create()
        self.changeTheme(setting["Main"]["theme"])
        self.window.exitAction.triggered.connect(self.close)

    # Создается список тем
    def themes_list_create(self):
        themes = list_themes()

        for action in self.window.themes_list_2.actions():
            self.window.themes_list_2.removeAction(action)

        for theme in themes:
            theme_name = theme.split('.')[0]
            new_theme = self.window.themes_list_2.addAction(theme_name.replace('_', ' ').title())
            new_theme.triggered.connect(lambda *args, x=theme_name: self.changeTheme(x))

            if theme_name == setting["Main"]["theme"]:
                new_theme.setIcon(QIcon('./source/ui/icons/checked.svg'))

    # Создаются кнопки в верхнем меню
    def buttons_create(self):

        for i in range(14):
            btn = QToolButton(text=self.abc[i])
            btn.setStyleSheet(open('./source/ui/buttons.css').read())
            self.window.upperButtons.addWidget(btn)

        trashBTN = QToolButton(text='Z')
        trashBTN.setStyleSheet(open('./source/ui/buttons.css').read())
        self.window.upperButtons.addWidget(trashBTN)

    # Наполняет списком меню "Архивы", "Образы дисков" и др.
    def archive_list_create(self):
        archivesList = pandas.read_csv('./game_list/archives_list.csv', delimiter='\t')
        archivesList = archivesList.sort_values(by='Archives Name')
        abc = {arc[0].upper() for arc in archivesList['Archives Name'] if arc[0] not in '0123456789'}
        abc = sorted(list(abc), key=lambda x: x[0])
        self.window.menu_5.removeAction(self.window.actionarchives_dummy)
        self.window.archive_list = {'0-9': self.window.menu_5.addMenu('0-9')}

        for liter in abc:
            self.window.archive_list[liter] = self.window.menu_5.addMenu(liter)

        for archive in archivesList['Archives Name']:
            liter = archive[0].upper()

            if liter in '0123456789':
                self.window.archive_list['0-9'].addAction(archive)
            else:
                self.window.archive_list[liter].addAction(archive)

    # Создается список игр в три вью
    def tree_view_create(self):
        model = QStandardItemModel()
        root_item = model.invisibleRootItem()
        new_parent = QStandardItem('0-9')
        self.parent_list['0-9'] = new_parent
        root_item.appendRow(new_parent)

        for item in self.abc:
            new_parent = QStandardItem(item)
            self.parent_list[item] = new_parent
            root_item.appendRow(new_parent)

        new_parent = QStandardItem('Other')
        self.parent_list['Other'] = new_parent
        root_item.appendRow(new_parent)
        all_games = 0
        mainList = pandas.read_csv('./game_list/main_list.csv', delimiter='\t')
        # pprint(self.mainList)

        for name in mainList['game_name']:

            if name[0].upper() in '0123456789':
                literal = '0-9'
            elif name[0].upper() in self.abc:
                literal = name[0].upper()
            else:
                literal = 'Other'

            child = QStandardItem(name)
            self.parent_list[literal].appendRow(child)
            all_games += 1

        # pprint(self.parent_list)
        self.window.gameList_treeView.setModel(model)
        model.setHeaderData(0, Qt.Horizontal, "Выберите игру, приложение или тип файла")
        self.window.all_games_label.setText(f'Всего игр: {all_games}')

    def changeTheme(self, theme_name):
        apply_stylesheet(self.window, theme=f'{theme_name}.xml')
        setting.read('./setting.ini')
        setting.set('Main', 'theme', theme_name)

        with open('./setting.ini', "w") as config_file:
            setting.write(config_file)

        self.themes_list_create()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
