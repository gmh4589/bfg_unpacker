
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import *

import source.ui.main_ui as ui
from qt_material import apply_stylesheet
from qt_material import list_themes
import configparser
import pandas

from source import change_button_menu as cbm
from source import setting as setting_ui
from source import theme_creator
import source.ui.localize as TL

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class MainWindow(QMainWindow, ui.Ui_BFGUnpacker):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BFGUnpacker")
        self.resize(600, 650)
        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.parent_list = {}
        self.themes_list_create()
        self.buttons_create()
        self.tree_view_create()
        self.archive_list_create()
        self.changeTheme(setting["Main"]["theme"])
        self.exitAction.triggered.connect(self.close)
        self.action_Settings.triggered.connect(
            lambda: setting_ui.SettingWindow(style=setting["Main"]["theme"]).exec())
        self.create_theme.triggered.connect(
            lambda: theme_creator.ThemeCreateWindow(style=setting["Main"]["theme"]).exec())
        self.archive_list = {}

    # Создается список тем
    def themes_list_create(self):

        for action in self.themes_list_2.actions():
            self.themes_list_2.removeAction(action)

        for theme in list_themes():
            theme_name = theme.split('.')[0]
            new_theme = self.themes_list_2.addAction(theme_name.replace('_', ' ').title())
            new_theme.triggered.connect(lambda *args, x=theme_name: self.changeTheme(x))

            if theme_name == setting["Main"]["theme"]:
                new_theme.setIcon(QIcon('./source/ui/icons/checked.svg'))

    def add_button(self, btn, l_func=None, contexts=None):
        if contexts is not None:
            context_menu = QMenu(self)

            for i, action in enumerate(contexts):
                context = context_menu.addAction(action)

                if action != TL.cancel:
                    if isinstance(l_func, list):
                        context.triggered.connect(l_func[i])
                    else:
                        context.triggered.connect(l_func)

            btn.setContextMenuPolicy(3)
            btn.customContextMenuRequested.connect(lambda pos, b=btn: context_menu.exec_(b.mapToGlobal(pos)))

        self.upperButtons.addWidget(btn)

    # Создаются кнопки в верхнем меню
    def buttons_create(self):
        alpha = 'ABCDEFGHIJKLMYZ'
        tool_tips = ['folder', 'quickbms', '7zip', 'gaup', 'innosetup', 'ffmpeg', 'unreal', 'unity', 'idtech', 'source',
                     'creation', 'wwise', 'bink', 'setting', 'trashcan']

        for i in range(15):
            btn = QToolButton(text=alpha[i])
            btn.setStyleSheet(open('./source/ui/buttons.css').read())
            btn.setToolTip(tool_tips[i])

            if i not in (0, 13, 14, -1):
                self.add_button(btn, contexts=[TL.change_button, TL.cancel],
                                l_func=(lambda *args, l=alpha[i]:
                                        cbm.CBWindow(style=setting["Main"]["theme"], letter=l).exec()))
            elif i == 14:
                self.add_button(btn, contexts=[TL.delete_to_trash, TL.full_delete, TL.cancel],
                                l_func=[lambda: print('trash1'), lambda: print('trash2')])
            else:
                self.add_button(btn)

    # Наполняет списком меню "Архивы", "Образы дисков" и др.
    def archive_list_create(self):
        archivesList = pandas.read_csv('./game_list/archives_list.csv', delimiter='\t')
        archivesList = archivesList.sort_values(by='Archives Name', key=lambda x: x.str.lower()).reset_index(drop=True)
        abc = sorted(list({archivesList['Archives Name'][n][0].upper() for n in range(len(archivesList))
                           if archivesList['Index'][n] not in (3, 5) and archivesList['Archives Name'][n][0]
                           not in '0123456789'}), key=lambda x: x)

        self.archive_list = {'0-9': self.menu_5.addMenu('0-9')}

        for liter in abc:
            self.archive_list[liter] = self.menu_5.addMenu(liter)

        for n in range(len(archivesList)):
            liter = archivesList['Archives Name'][n][0].upper()

            if archivesList['Index'][n] == 3:
                self.menu_7.addAction(archivesList['Archives Name'][n])
            elif archivesList['Index'][n] == 5:
                self.menu_8.addAction(archivesList['Archives Name'][n])
            else:

                if liter in '0123456789':
                    self.archive_list['0-9'].addAction(archivesList['Archives Name'][n])
                else:
                    self.archive_list[liter].addAction(archivesList['Archives Name'][n])

    def filter_list_create(self, items):

        for action in self.comboBox_gameList.actions():
            self.comboBox_gameList.removeAction(action)

        self.comboBox_gameList.addItem('')
        self.comboBox_gameList.addItems(items)

    # Создается список игр в три-вью
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

        new_parent = QStandardItem(TL.other)
        self.parent_list[TL.other] = new_parent
        root_item.appendRow(new_parent)
        all_games = 0
        mainList = pandas.read_csv('./game_list/main_list.csv', delimiter='\t')
        mainList = mainList.sort_values(by='game_name', key=lambda x: x.str.lower()).reset_index(drop=True)
        names = [n for n in mainList['game_name']]
        self.filter_list_create(names)

        for name in names:

            if name[0].upper() in '0123456789':
                literal = '0-9'
            elif name[0].upper() in self.abc:
                literal = name[0].upper()
            else:
                literal = TL.other

            child = QStandardItem(name)
            child.setToolTip(name)
            self.parent_list[literal].appendRow(child)
            all_games += 1

        # pprint(self.parent_list)
        self.gameList_treeView.setModel(model)
        model.setHeaderData(0, Qt.Horizontal, TL.select_something)
        self.all_games_label.setText(f'{TL.all_games} {all_games}')

    def changeTheme(self, theme_name):
        apply_stylesheet(self, theme=f'{theme_name}.xml')
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
