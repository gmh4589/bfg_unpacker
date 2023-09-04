import configparser
import importlib
import json
import os
import sys
from datetime import datetime
import pandas
from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import *

import source.ui.localize as TL
import source.ui.main_ui as ui
from qt_material import apply_stylesheet
from qt_material import list_themes
from source.unpacker import Unpacker
from source.ui import resize, setting as setting_ui, theme_creator, change_button_menu as cbm

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class MainWindow(QMainWindow, ui.Ui_BFGUnpacker):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BFGUnpacker")
        self.resize(resize.widget(600), resize.widget(650))
        self.abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.all_games = 0
        self.parent_list = {}
        self.lang_list_create()
        self.buttons_create()
        self.model = QStandardItemModel()
        self.gameList_treeView.setModel(self.model)
        self.root_item = self.model.invisibleRootItem()

        self.mainList = pandas.read_csv('./game_list/main_list.csv', delimiter='\t')

        if int(setting['Engines']['unity']) > 0:
            unity_list = pandas.read_csv('./game_list/unity_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, unity_list], axis=0, ignore_index=True)
        if int(setting['Engines']['unreal']) > 0:
            unreal_list = pandas.read_csv('./game_list/unreal_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, unreal_list], axis=0, ignore_index=True)
        if int(setting['Engines']['renpy']) > 0:
            renpy_list = pandas.read_csv('./game_list/renpy_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, renpy_list], axis=0, ignore_index=True)
        if int(setting['Engines']['game_maker']) > 0:
            gamemaker_list = pandas.read_csv('./game_list/gamemaker_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, gamemaker_list], axis=0, ignore_index=True)
        if int(setting['Engines']['rpg_maker']) > 0:
            rpgmaker_list = pandas.read_csv('./game_list/rpgmaker_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, rpgmaker_list], axis=0, ignore_index=True)
        if int(setting['Engines']['godot']) > 0:
            godot_list = pandas.read_csv('./game_list/godot_list.csv', delimiter='\t')
            self.mainList = pandas.concat([self.mainList, godot_list], axis=0, ignore_index=True)

        self.mainList = self.mainList.sort_values(by='game_name', key=lambda x: x.str.lower()).reset_index(drop=True)
        self.names = {row['game_name']: row['release_year'] for _, row in self.mainList.iterrows()}

        if setting['Main']['group'] == 'name':
            self.tree_view_create_by_name()
        else:
            self.tree_view_create_by_year()

        # pprint(self.parent_list)

        self.gameList_treeView.clicked.connect(self.file_reaper)
        self.model.setHeaderData(0, Qt.Horizontal, TL.select_something)
        self.all_games_count.setText(str(self.all_games))
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

        default_themes = ['dark_amber', 'dark_blue', 'dark_blue_500', 'dark_cyan', 'dark_cyan_500', 'dark_lightgreen',
                          'dark_lightgreen_500', 'dark_medical', 'dark_orange', 'dark_pink', 'dark_pink_500',
                          'dark_purple', 'dark_purple_500', 'dark_red', 'dark_red_500', 'dark_teal', 'dark_teal_500',
                          'dark_yellow', 'light_amber', 'light_blue', 'light_blue_500', 'light_cyan', 'light_cyan_500',
                          'light_lightgreen', 'light_lightgreen_500', 'light_orange', 'light_pink', 'light_pink_500',
                          'light_purple', 'light_purple_500', 'light_red', 'light_red_500', 'light_teal',
                          'light_teal_500', 'light_yellow']

        other_themes_submenu = QMenu(self)
        other_themes_submenu.setTitle('...')

        for action in self.themes_list_2.actions():
            self.themes_list_2.removeAction(action)

        for theme in list_themes():
            theme_name = theme.split('.')[0]

            if theme_name not in default_themes or theme_name == setting["Main"]["theme"]:
                new_theme = self.themes_list_2.addAction(theme_name.replace('_', ' ').title())
            else:
                new_theme = other_themes_submenu.addAction(theme_name.replace('_', ' ').title())

            new_theme.triggered.connect(lambda *args, x=theme_name: self.changeTheme(x))

            if theme_name == setting["Main"]["theme"]:
                new_theme.setIcon(QIcon('./source/ui/icons/checked.svg'))

        self.themes_list_2.addMenu(other_themes_submenu)

    def lang_list_create(self):
        lang_files = [file for file in os.listdir('./source/local/') if file.endswith('.json')]
        lang_list = [json.load(open(f'./source/local/{file}', 'r', encoding='utf-8'))['lang_name'] for file in
                     lang_files]
        lang_codes = [json.load(open(f'./source/local/{file}', 'r', encoding='utf-8'))['lang_code'] for file in
                      lang_files]
        main_list = ['ru', 'ua', 'pl', 'tr', 'de', 'it', 'fr', 'en', 'es', 'es_la',
                     'pt_br', 'ar', 'jp', 'ko', 'id', 'zh', 'zh_tw', 'th', 'vn', 'fi']

        for action in self.action_Language.actions():
            self.action_Language.removeAction(action)

        other_submenu = QMenu(self)
        other_submenu.setTitle('...')

        for i, lang in enumerate(lang_list):

            if lang_codes[i] in main_list or lang_codes[i] == setting["Main"]["lang"]:
                new_lang = self.action_Language.addAction(lang)
            else:
                new_lang = other_submenu.addAction(lang)

            new_lang.triggered.connect(lambda *args, x=lang_codes[i]: self.changeLang(x))

            if lang_codes[i] == setting["Main"]["lang"]:
                new_lang.setIcon(QIcon('./source/ui/icons/checked.svg'))

                if lang_codes[i] not in main_list:
                    main_list.append(lang_codes[i])

        self.action_Language.addMenu(other_submenu)

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
            case '7zip':
                pass
            case 'bink':
                pass
            case 'creation':
                pass
            case 'cry engine':
                pass
            case 'ffmpeg':
                pass
            case 'folder':
                pass
            case 'gaup':
                pass
            case 'godot':
                pass
            case 'idtech':
                pass
            case 'innosetup':
                pass
            case 'playstation':
                pass
            case 'quickbms':
                pass
            case 'raw2atrac':
                pass
            case 'raw2dds':
                pass
            case 'raw2wav':
                pass
            case 'red engine':
                pass
            case 'renpy':
                pass
            case 'rpg maker':
                pass
            case 'setting':
                btn.clicked.connect(lambda: setting_ui.SettingWindow(style=setting["Main"]["theme"]).exec())
            case 'source':
                pass
            case 'trashcan':
                pass
            case 'unreal':
                pass
            case 'unigen':
                pass
            case 'unity':
                pass
            case 'wwise':
                pass
            case 'xnconvert':
                pass

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
                     'Y': 'setting', 'Z': 'trashcan'}  # TODO: Set really tooltips

        for i in range(self.upperButtons.count()):
            item = self.upperButtons.itemAt(i)
            item.widget().deleteLater()

        for i, a in enumerate(alpha):
            btn = QToolButton(text=a)
            btn.setToolTip(tool_tips[a])
            btn.setStyleSheet(
                'QToolButton {'
                "font-family: 'IconLib';"
                'border: 0px;'
                'margin: 0px;'
                'padding: 0px;'
                'border-radius: 10px;'
                f'height: {resize.widget(40)}px;'
                f'width: {resize.widget(40)}px;'
                f'font-size: {resize.widget(40)}px;'
                '}')

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
    def tree_view_create_by_year(self):
        new_parent = QStandardItem(TL.other)
        self.parent_list[TL.other] = new_parent
        self.root_item.appendRow(new_parent)
        old_games = QStandardItem('... - 1990')
        self.parent_list['... - 1990'] = old_games
        year_now = datetime.now().year

        for i in range(year_now, 1990, -1):
            item = str(i)
            new_parent = QStandardItem(item)
            self.parent_list[item] = new_parent
            self.root_item.appendRow(new_parent)

        self.filter_list_create(self.names)

        for name in self.names:

            try:
                y = int(self.names[name])

                if y < 1991:
                    y = '... - 1990'
                else:
                    y = str(y)

            except ValueError:
                y = TL.other

            child = QStandardItem(name)
            child.setToolTip(name)
            self.parent_list[y].appendRow(child)
            self.all_games += 1

        self.root_item.appendRow(old_games)

    def tree_view_create_by_name(self):
        new_parent = QStandardItem('0-9')
        self.parent_list['0-9'] = new_parent
        self.root_item.appendRow(new_parent)

        for item in self.abc:
            new_parent = QStandardItem(item)
            self.parent_list[item] = new_parent
            self.root_item.appendRow(new_parent)

        new_parent = QStandardItem(TL.other)
        self.parent_list[TL.other] = new_parent
        self.root_item.appendRow(new_parent)

        self.filter_list_create(self.names)

        for name in self.names:

            if name[0].upper() in '0123456789':
                literal = '0-9'
            elif name[0].upper() in self.abc:
                literal = name[0].upper()
            else:
                literal = TL.other

            child = QStandardItem(name)
            child.setToolTip(name)
            self.parent_list[literal].appendRow(child)
            self.all_games += 1

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

    def file_open(self, ext_list, select_folder=False, more_one=False):

        if not select_folder:

            if more_one:
                file_name = ''
            else:
                file_name = QFileDialog.getOpenFileName(self, 'Open file', filter=ext_list.replace('|', ';;'))[0]

        else:
            file_name = QFileDialog.getExistingDirectory(self, 'Select folder')

        return file_name

    def file_reaper(self, index, select_folder=False, more_one=False):

        item = self.model.itemFromIndex(index)
        data_string = self.mainList.loc[self.mainList['game_name'] == item.text()]
        func_name = data_string['func_name'].values[0]
        script_name = data_string['script_name'].values[0]
        ext_list = data_string['ext_list'].values[0]

        if func_name == '_Unity':
            select_folder = True

        file_name = self.file_open(ext_list, select_folder, more_one)

        if file_name:
            unpacker = Unpacker()

            if func_name == "_Unity":
                # unpacker.unity(file_name)
                thread = Thread(target=unpacker.unity, args=(file_name, ))

            else:
                # unpacker.quick_bms(file_name, script_name)
                thread = Thread(target=unpacker.quick_bms, args=(file_name, script_name))

            thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
