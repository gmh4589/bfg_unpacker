import importlib
import json
import os
from datetime import datetime
import pandas
import locale
from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import *
import configparser


setting = configparser.ConfigParser()

if not os.path.exists('./setting.ini'):
    setting.add_section('Main')
    setting.add_section('Buttons')
    setting.add_section('Engines')
    setting.set('Main', 'theme', 'classic_white')
    lng = locale.getdefaultlocale()[0].split('_')[0]
    setting.set('Main', 'lang', lng)
    setting.set('Main', 'group', 'name')
    setting.set('Main', 'zoom', '1.0')
    setting.set('Main', 'last_dir', '')
    setting.set('Main', 'out_path', '')
    setting.set('Main', 'trash', '1')
    setting.set('Main', 'show_console', '0')
    setting.set('Main', 'subfolders', '2')
    setting.set('Buttons', '1', 'B')
    setting.set('Buttons', '2', 'C')
    setting.set('Buttons', '3', 'D')
    setting.set('Buttons', '4', 'E')
    setting.set('Buttons', '5', 'F')
    setting.set('Buttons', '6', 'G')
    setting.set('Buttons', '7', 'H')
    setting.set('Buttons', '8', 'I')
    setting.set('Buttons', '9', 'J')
    setting.set('Buttons', '10', 'K')
    setting.set('Buttons', '11', 'L')
    setting.set('Buttons', '12', 'M')
    setting.set('Engines', 'unreal', '0')
    setting.set('Engines', 'unity', '0')
    setting.set('Engines', 'rpg_maker', '0')
    setting.set('Engines', 'game_maker', '0')
    setting.set('Engines', 'godot', '0')
    setting.set('Engines', 'renpy', '0')

    with open('./setting.ini', "w") as config_file:
        setting.write(config_file)

else:
    setting.read('./setting.ini')

import source.ui.localize as translate
import source.ui.main_ui as ui
from qt_material import apply_stylesheet
from qt_material import list_themes
from source.unpacker import Unpacker
from source.ui import resize, setting as setting_ui, theme_creator, change_button_menu as cbm, progress_bar
import source.ui.localize as TL


class MainWindow(QMainWindow, ui.Ui_BFGUnpacker):

    def __init__(self):
        super().__init__()

        self.setting = setting
        self.out_dir = setting['Main']['out_path'] if os.path.exists(setting['Main']['out_path']) else (
            self.set_setting('Main', 'out_path',
                             QFileDialog.getExistingDirectory(self, 'Select folder')))

        self.path_to_root = os.path.abspath(__file__).split('source')[0]
        self.setWindowIcon(QIcon('./source/ui/icons/i.ico'))
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
        self.unpacker = Unpacker()
        self.pb = progress_bar.ProgressBar(setting["Main"]["theme"])
        self.pb_header_text = ''
        self.show_favorites = False
        self.filter_model = QStandardItemModel()

        with open('./favorites.ini', 'r') as fav:
            self.favorites = []

            for line in fav.readlines():
                self.favorites.append(line[:-1])

        # Game list creating
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

        self.model.setHeaderData(0, Qt.Horizontal, translate.select_something)
        self.all_games_count.setText(f'{translate.all_games} {self.all_games}')

        # Run functions and methods
        self.change_theme(setting["Main"]["theme"])
        self.archive_list = {}
        self.archive_list_create()

        # Actions connected
        self.gameList_treeView.clicked.connect(self.file_reaper)
        self.exitAction.triggered.connect(self.close)
        self.action_Settings.triggered.connect(lambda: setting_ui.SettingWindow(style=setting["Main"]["theme"]).exec())
        self.create_theme.triggered.connect(
            lambda: theme_creator.ThemeCreateWindow(style=setting["Main"]["theme"]).exec())
        self.action_SelectOutPath.triggered.connect(lambda: self.set_setting('Main', 'out_path',
                                                                             self.file_open(select_folder=True)))
        self.checkBox_ShowConsole.setCheckState(int(setting['Main']['show_console']))
        self.checkBox_createSubfolders.setCheckState(int(setting['Main']['subfolders']))
        self.checkBox_ShowConsole.stateChanged.connect(
            lambda: self.set_setting('Main', 'show_console',
                                     "2" if self.checkBox_ShowConsole.isChecked() else "0"))
        self.checkBox_createSubfolders.stateChanged.connect(
            lambda: self.set_setting('Main', 'subfolders',
                                     "2" if self.checkBox_createSubfolders.isChecked() else "0"))
        self.btn_All_Favorite.clicked.connect(lambda: self.all_favorites())
        self.toolButton_plus.clicked.connect(lambda: self.favorite_setting(True, self.comboBox_gameList.currentText()))
        self.toolButton_minus.clicked.connect(lambda: self.favorite_setting(False, self.comboBox_gameList.currentText()))
        self.toolButton_Find.clicked.connect(lambda: print('find'))

    def all_favorites(self):
        self.show_favorites = not self.show_favorites

        if self.show_favorites:
            self.filter_list_create(self.favorites)
            self.btn_All_Favorite.setText(TL.fav_caps)
        else:
            self.filter_list_create(self.names)
            self.btn_All_Favorite.setText(TL.all_caps)

    def favorite_setting(self, action, item):

        if action:

            if item not in self.favorites:
                self.favorites.append(item)
                self.favorites.sort()
        else:
            self.favorites.remove(item)
            self.filter_list_create(self.favorites)

        with open('./favorites.ini', 'w') as fav:

            for favorite in self.favorites:
                fav.write(favorite + '\n')

    def set_setting(self, section, key, value, remove=False):
        global setting

        if remove:
            setting.remove_option(section, key)
        else:
            setting.set(section, key, value)

        with open('./setting.ini', "w") as cf:
            setting.write(cf)

        self.setting = setting

    def append_text(self, text):

        if text.strip():
            self.logWindow.append(text)

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

            new_theme.triggered.connect(lambda *args, x=theme_name: self.change_theme(x))

            if theme_name == setting["Main"]["theme"]:
                new_theme.setIcon(QIcon('./source/ui/icons/checked.svg'))

        self.themes_list_2.addMenu(other_themes_submenu)

    def lang_list_create(self):
        d = './source/local/'
        lang_files = [file for file in os.listdir(d) if file.endswith('.json')]
        lang_list = [json.load(open(f'{d}{file}', 'r', encoding='utf-8'))['lang_name'] for file in lang_files]
        lang_codes = [json.load(open(f'{d}{file}', 'r', encoding='utf-8'))['lang_code'] for file in lang_files]
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

            new_lang.triggered.connect(lambda *args, x=lang_codes[i]: self.change_lang(x))

            if lang_codes[i] == setting["Main"]["lang"]:
                new_lang.setIcon(QIcon('./source/ui/icons/checked.svg'))

                if lang_codes[i] not in main_list:
                    main_list.append(lang_codes[i])

        self.action_Language.addMenu(other_submenu)

    def add_button(self, btn, l_func=None, contexts=None):

        if contexts is not None:
            context_menu = QMenu(self)

            for i, action in enumerate(contexts):
                context = context_menu.addAction(action)

                if action != translate.cancel:

                    if isinstance(l_func, list):
                        context.triggered.connect(l_func[i])
                    else:
                        context.triggered.connect(l_func)

            btn.setContextMenuPolicy(3)
            btn.customContextMenuRequested.connect(lambda pos, b=btn: context_menu.exec_(b.mapToGlobal(pos)))

    def add_btn_action(self, btn, action=''):

        match action:
            case '7zip':
                btn.clicked.connect(lambda: print('7zip'))
            case 'bink':
                btn.clicked.connect(lambda: print('bink'))
            case 'creation':
                btn.clicked.connect(lambda: print('creation'))
            case 'cry engine':
                btn.clicked.connect(lambda: print('cry engine'))
            case 'ffmpeg':
                btn.clicked.connect(lambda: print('ffmpeg'))
            case 'folder':
                btn.clicked.connect(lambda: print('folder'))
            case 'gaup':
                btn.clicked.connect(lambda: print('gaup'))
            case 'godot':
                btn.clicked.connect(lambda: print('godot'))
            case 'idtech':
                btn.clicked.connect(lambda: print('idtech'))
            case 'innosetup':
                btn.clicked.connect(lambda: print('innosetup'))
            case 'playstation':
                btn.clicked.connect(lambda: print('playstation'))
            case 'quickbms':
                btn.clicked.connect(lambda: print('quickbms'))
            case 'raw2atrac':
                btn.clicked.connect(lambda: print('raw2atrac'))
            case 'raw2dds':
                btn.clicked.connect(lambda: print('raw2dds'))
            case 'raw2wav':
                btn.clicked.connect(lambda: print('raw2wav'))
            case 'red engine':
                btn.clicked.connect(lambda: print('red engine'))
            case 'renpy':
                btn.clicked.connect(lambda: print('renpy'))
            case 'rpg maker':
                btn.clicked.connect(lambda: print('rpg maker'))
            case 'setting':
                btn.clicked.connect(lambda: setting_ui.SettingWindow(style=setting["Main"]["theme"]).exec())
            case 'source':
                btn.clicked.connect(lambda: print('source'))
            case 'trashcan':
                btn.clicked.connect(self.empty_out)
            case 'unreal':
                btn.clicked.connect(lambda: Thread(target=self.unpacker.unreal, args=(
                    self.file_open('Unreal Engine File(*.u*; *.xxx; *.pak; *.locres; *.pcc)|Unreal Engine 1-2(*.u*)|'
                                   'Unreal Engine 3(*.u*; *.xxx; *.pcc)|Unreal Engine 4(*.pak; *.locres)|'),)).start())
            case 'unigen':
                btn.clicked.connect(lambda: print('unigen'))
            case 'unity':
                btn.clicked.connect(lambda: Thread(target=self.unpacker.unity,
                                                   args=(QFileDialog.getExistingDirectory(
                                                       self, 'Select folder',  # TODO: TEXT!!!
                                                       directory=setting['Main']['last_dir']),)).start())
            case 'wwise':
                btn.clicked.connect(lambda: print('wwise'))
            case 'xnconvert':
                btn.clicked.connect(lambda: print('xnconvert'))

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
                self.add_button(btn, contexts=[translate.change_button, translate.cancel],
                                l_func=(lambda *args, l=i:
                                        self.new_button(style=setting["Main"]["theme"], alpha=l)))
            elif i == 14:
                self.add_button(btn, contexts=[translate.delete_to_trash, translate.full_delete, translate.cancel],
                                l_func=[lambda: self.set_setting('Main', 'trash', '1'),
                                        lambda: self.set_setting('Main', 'trash', '0')])
            else:
                self.add_button(btn)

            self.add_btn_action(btn, tool_tips[a])
            self.upperButtons.addWidget(btn)

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

        self.filter_model.clear()
        self.filter_model.appendRow(QStandardItem(''))

        for item in items:
            self.filter_model.appendRow(QStandardItem(item))

        self.comboBox_gameList.setModel(self.filter_model)

    # Создается список игр в три-вью
    def tree_view_create_by_year(self):
        new_parent = QStandardItem(translate.other)
        self.parent_list[translate.other] = new_parent
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
                y = translate.other

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

        new_parent = QStandardItem(translate.other)
        self.parent_list[translate.other] = new_parent
        self.root_item.appendRow(new_parent)

        self.filter_list_create(self.names)

        for name in self.names:

            if name[0].upper() in '0123456789':
                literal = '0-9'
            elif name[0].upper() in self.abc:
                literal = name[0].upper()
            else:
                literal = translate.other

            child = QStandardItem(name)
            child.setToolTip(name)
            self.parent_list[literal].appendRow(child)
            self.all_games += 1

    def change_theme(self, theme_name):
        apply_stylesheet(self, theme=f'{theme_name}.xml')
        self.set_setting('Main', 'theme', theme_name)
        self.themes_list_create()

    def change_lang(self, lang):
        self.set_setting('Main', 'lang', lang)
        self.lang_list_create()
        importlib.reload(translate)
        self.buttons_create()
        self.model.setHeaderData(0, Qt.Horizontal, translate.select_something)
        self.all_games_count.setText(f'{translate.all_games} {self.all_games}')
        self.retranslateUi()
