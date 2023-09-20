import configparser
import importlib
import json
import os
import shutil
import sys
from datetime import datetime
from time import sleep
import pandas
from threading import Thread
import asyncio

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import *

import source.ui.localize as TL
import source.ui.main_ui as ui
from qt_material import apply_stylesheet
from qt_material import list_themes
from source.unpacker import Unpacker
from source.ui import resize, setting as setting_ui, theme_creator, change_button_menu as cbm, progress_bar
from source.reapers import pathologic

setting = configparser.ConfigParser()
setting.read('./setting.ini')


class MainWindow(QMainWindow, ui.Ui_BFGUnpacker):

    def __init__(self):
        super().__init__()
        self.out_dir = setting['Main']['out_path']
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
        sys.stdout = EmittingStream(text_written=self.append_text)
        self.unpacker = Unpacker()

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

    def add_action(self, btn, action=''):

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
                # btn.clicked.connect(lambda: print('trashcan'))
                btn.clicked.connect(self.empty_out)
            case 'unreal':
                # btn.clicked.connect(lambda: print('unreal'))
                btn.clicked.connect(lambda: Thread(target=self.unpacker.unreal, args=(
                    self.file_open('Unreal Engine File(*.u*; *.xxx; *.pak; *.locres; *.pcc)|Unreal Engine 1-2(*.u*)|'
                                   'Unreal Engine 3(*.u*; *.xxx; *.pcc)|Unreal Engine 4(*.pak; *.locres)|'), )).start())
            case 'unigen':
                btn.clicked.connect(lambda: print('unigen'))
            case 'unity':
                # btn.clicked.connect(lambda: print('unity'))
                btn.clicked.connect(lambda: Thread(target=self.unpacker.unity,
                                                   args=(self.file_open('', True), )).start())
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
                self.add_button(btn, contexts=[TL.change_button, TL.cancel], action=tool_tips[a],
                                l_func=(lambda *args, l=i:
                                        self.new_button(style=setting["Main"]["theme"], alpha=l)))
            elif i == 14:
                self.add_button(btn, contexts=[TL.delete_to_trash, TL.full_delete, TL.cancel], action=tool_tips[a],
                                l_func=[lambda: print('trash1'), lambda: print('trash2')])
            else:
                self.add_button(btn, action=tool_tips[a])

            self.add_action(btn, tool_tips[a])
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

            match func_name:
                case "_Unity":
                    thread = Thread(target=self.unpacker.unity, args=(file_name, ), daemon=True)
                case "_Unreal" | "_Unreal4":
                    thread = Thread(target=self.unpacker.unreal, args=(self.file_open(
                        'Unreal Engine File(*.u*;*.xxx;*.pak;*.locres;*.pcc)|Unreal Engine 1-2(*.u*)|'
                        'Unreal Engine 3(*.u*;*.xxx;*.pcc)|Unreal Engine 4(*.pak;*.locres)|'
                    ), script_name), daemon=True)
                case "_Mor":
                    thread = Thread(target=pathologic.mor_unpacker, args=(file_name, self.out_dir), daemon=True)
                case _:
                    thread = Thread(target=self.unpacker.quick_bms, args=(file_name, script_name), daemon=True)

            thread.start()

    def empty_out(self):

        async def empty():
            not_deleted = 0
            deleting_list = os.listdir(self.out_dir)

            if deleting_list:
                a = len(deleting_list)
                pb = progress_bar.ProgressBar(setting["Main"]["theme"], header='Deleting...')
                pb.exec()

                for i, item in enumerate(deleting_list):
                    name = os.path.join(self.out_dir, item)
                    info_text = f'Deleting {item}...'
                    pb.update_info(int(100/a * i), f'{i}/{a}', info_text)

                    try:

                        if os.path.isfile(name):
                            os.remove(name)
                        elif os.path.isdir(name):
                            shutil.rmtree(name)

                        print(info_text)

                    except (PermissionError, FileNotFoundError):
                        not_deleted += 1

                if not_deleted:
                    print(f"Some files or folders ({not_deleted}) could not be deleted. Try removing them manually")
                else:
                    print('Done!')

                sleep(2)
                pb.close()

            else:
                print('The folder is empty!')

        asyncio.run(empty())


class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
