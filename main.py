import json
import os
import sys
import importlib

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
        self.model = None
        self.setWindowTitle("BFGUnpacker")
        self.resize(600, 650)
        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.parent_list = {}
        self.themes_list_create()
        self.lang_list_create()
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

    def lang_list_create(self):
        lang_files = [file for file in os.listdir('./source/local/') if file.endswith('.json')]
        lang_list = [json.load(open(f'./source/local/{file}', 'r', encoding='utf-8'))['lang_name'] for file in lang_files]
        lang_codes = [json.load(open(f'./source/local/{file}', 'r', encoding='utf-8'))['lang_code'] for file in lang_files]
        print(len(lang_files))

        for action in self.action_Language.actions():
            self.action_Language.removeAction(action)

        for i, lang in enumerate(lang_list):
            new_lang = self.action_Language.addAction(lang)
            new_lang.triggered.connect(lambda *args, x=lang_codes[i]: self.changeLang(x))

            if lang_codes[i] == setting["Main"]["lang"]:
                new_lang.setIcon(QIcon('./source/ui/icons/checked.svg'))

    def add_button(self, btn, l_func=None, contexts=None, action=''):

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

        match action:
            case '7zip': pass
            case 'bink': pass
            case 'creation': pass
            case 'cry engine': pass
            case 'ffmpeg': pass
            case 'folder': pass
            case 'gaup': pass
            case 'godot': pass
            case 'idtech': pass
            case 'innosetup': pass
            case 'playstation': pass
            case 'quickbms': pass
            case 'raw2atrac': pass
            case 'raw2dds': pass
            case 'raw2wav': pass
            case 'red engine': pass
            case 'renpy': pass
            case 'rpg maker': pass
            case 'setting':
                btn.clicked.connect(lambda: setting_ui.SettingWindow(style=setting["Main"]["theme"]).exec())
            case 'source': pass
            case 'trashcan': pass
            case 'unreal': pass
            case 'unigen': pass
            case 'unity': pass
            case 'wwise': pass
            case 'xnconvert': pass

        self.upperButtons.addWidget(btn)

    # Создаются кнопки в верхнем меню
    def buttons_create(self):
        setting.read('./setting.ini')
        alpha = ['A']

        for j in range(1, 13):
            alpha.append(setting["Buttons"][str(j)])

        alpha.append('Y')
        alpha.append('Z')

        tool_tips = {'A': 'folder', 'B': 'quickbms', 'C': '7zip', 'D': 'gaup', 'E': 'innosetup', 'F': 'ffmpeg',
                     'G': 'unreal', 'H': 'unity', 'I': 'idtech', 'J': 'source', 'K': 'creation', 'L': 'cry engine',
                     'M': 'bink', 'N': 'wwise', 'O': 'playstation', 'P': 'xnconvert', 'Q': 'red engine', 'R': 'godot',
                     'S': 'rpg maker', 'T': 'renpy', 'U': 'unigen', 'V': 'raw2dds', 'W': 'raw2atrac', 'X': 'raw2wav',
                     'Y': 'setting', 'Z': 'trashcan'}

        for i in range(self.upperButtons.count()):
            item = self.upperButtons.itemAt(i)
            item.widget().deleteLater()

        for i, a in enumerate(alpha):
            btn = QToolButton(text=a)
            btn.setStyleSheet(open('./source/ui/buttons.css').read())
            btn.setToolTip(tool_tips[a])

            if i not in (0, 13, 14, -1):
                self.add_button(btn, contexts=[TL.change_button, TL.cancel], action=tool_tips[a],
                                l_func=(lambda *args, l=i:
                                        self.new_button(style=setting["Main"]["theme"], alpha=l)))
            elif i == 14:
                self.add_button(btn, contexts=[TL.delete_to_trash, TL.full_delete, TL.cancel], action=tool_tips[a],
                                l_func=[lambda: print('trash1'), lambda: print('trash2')])
            else:
                self.add_button(btn, action=tool_tips[a])

    def new_button(self, style, alpha):
        cbm.CBWindow(style=style, letter=alpha).exec()
        self.buttons_create()

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
        self.model = QStandardItemModel()
        root_item = self.model.invisibleRootItem()
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
        self.gameList_treeView.setModel(self.model)
        self.model.setHeaderData(0, Qt.Horizontal, TL.select_something)
        self.all_games_count.setText(str(all_games))

    def changeTheme(self, theme_name):
        apply_stylesheet(self, theme=f'{theme_name}.xml')
        setting.read('./setting.ini')
        setting.set('Main', 'theme', theme_name)

        with open('./setting.ini', "w") as config_file:
            setting.write(config_file)

        self.themes_list_create()

    def changeLang(self, lang):
        setting.read('./setting.ini')
        setting.set('Main', 'lang', lang)

        with open('./setting.ini', "w") as config_file:
            setting.write(config_file)

        self.lang_list_create()
        importlib.reload(TL)
        self.model.setHeaderData(0, Qt.Horizontal, TL.select_something)
        self.retranslateUi()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
