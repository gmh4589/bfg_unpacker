import importlib
import json
import os
from datetime import datetime
from threading import Thread

import pandas
import sqlalchemy

from PyQt6.QtCore import Qt, QItemSelectionModel
from PyQt6.QtGui import QStandardItem, QIcon, QFontDatabase
from PyQt6.QtWidgets import *
from icecream import ic

import source.ui.main_ui as ui
from qt_material import apply_stylesheet
from qt_material import list_themes
from source.reaper import after_dot
from source.ui import (setting as setting_ui,
                       change_button_menu as cbm,
                       localize,
                       child_gui_data)


# Методы для наполнения интерфейса данными
class MainWindow(QMainWindow, ui.Ui_BFGUnpacker, child_gui_data.ChildGuiData):

    def __init__(self):
        super().__init__()

    @staticmethod
    def dragEnterEvent(event):
        mime_data = event.mimeData()

        if mime_data.hasUrls() and len(mime_data.urls()) == 1:
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()

        if mime_data.hasUrls():
            file_path = mime_data.urls()[0].toLocalFile()

            if not os.path.isdir(file_path):
                ic(file_path)
                self.file_list = [file_path]
                self.find_reaper()

    def find_item_in_treeview(self):

        item_text = self.comboBox_gameList.currentText()
        root_item = self.model.invisibleRootItem()
        index_to_activate = self.find_item_index(root_item, item_text)

        if index_to_activate is not None:
            self.gameList_treeView.selectionModel().select(index_to_activate, QItemSelectionModel.SelectionFlag.Select)
            self.gameList_treeView.scrollTo(index_to_activate)

    def find_item_index(self, parent_item, target_text):

        for row in range(parent_item.rowCount()):
            child_item = parent_item.child(row)

            if child_item.text() == target_text:
                return child_item.index()
            elif child_item.hasChildren():
                result = self.find_item_index(child_item, target_text)

                if result is not None:
                    return result

        return None

    def all_favorites(self):
        self.show_favorites = not self.show_favorites

        if self.show_favorites:
            self.filter_list_create(self.favorites)
            self.comboBox_gameList.items = self.favorites
            self.btn_All_Favorite.setText(localize.fav_caps)
        else:
            self.filter_list_create(self.names)
            self.comboBox_gameList.items = self.names
            self.btn_All_Favorite.setText(localize.all_caps)

    def favorite_setting(self, action, item):

        if item.strip() != '':

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

        if remove:
            self.setting.remove_option(section, key)
        else:
            self.setting.set(section, key, value)

        with open(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini', "w") as cf:
            self.setting.write(cf)

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

        # Default Theme
        default_theme = self.themes_list_2.addAction('Default')
        default_theme.triggered.connect(lambda *args, x='Default': self.change_theme(x))
        self.themes_list_2.addMenu(other_themes_submenu)

        if self.setting["Main"]["theme"].lower() == 'default':
            default_theme.setIcon(QIcon('./data/icons/checked.svg'))

        for theme in list_themes():
            theme_name = theme.split('.')[0]

            if theme_name not in default_themes or theme_name == self.setting["Main"]["theme"]:
                new_theme = self.themes_list_2.addAction(theme_name.replace('_', ' ').title())
            else:
                new_theme = other_themes_submenu.addAction(theme_name.replace('_', ' ').title())

            new_theme.triggered.connect(lambda *args, x=theme_name: self.change_theme(x))

            if theme_name == self.setting["Main"]["theme"]:
                new_theme.setIcon(QIcon('./data/icons/checked.svg'))

        self.themes_list_2.addMenu(other_themes_submenu)

    def lang_list_create(self):
        d = './data/local/'
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

            if lang_codes[i] in main_list or lang_codes[i] == self.setting["Main"]["lang"]:
                new_lang = self.action_Language.addAction(lang)
            else:
                new_lang = other_submenu.addAction(lang)

            new_lang.triggered.connect(lambda *args, x=lang_codes[i]: self.change_lang(x))

            if lang_codes[i] == self.setting["Main"]["lang"]:
                new_lang.setIcon(QIcon('./data/icons/checked.svg'))

                if lang_codes[i] not in main_list:
                    main_list.append(lang_codes[i])

        self.action_Language.addMenu(other_submenu)

    def add_button(self, btn, l_func=None, contexts=None):

        if contexts is not None:
            context_menu = QMenu(self)

            for i, action in enumerate(contexts):
                context = context_menu.addAction(action)

                if action != localize.cancel:

                    if isinstance(l_func, list):
                        context.triggered.connect(l_func[i])
                    else:
                        context.triggered.connect(l_func)

            btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda pos, b=btn: context_menu.exec(b.mapToGlobal(pos)))

    def add_btn_action(self, btn, action=''):

        match action:
            case 'A':
                btn.clicked.connect(self.q_open)
            case 'B':
                btn.clicked.connect(lambda: self.create_queue(script_name=QFileDialog.getOpenFileName(
                    self, localize.open_file, filter='QuickBMS Scripts (*.bms);;QuickBMS Scripts (*.txt);;'
                                                      f'{localize.all_files} (*.*)',
                    directory=self.setting['Main']['last_dir'])[0]))
            case 'C':
                btn.clicked.connect(lambda: self.create_queue(func_name='_7ZIP'))
            case 'D':
                btn.clicked.connect(lambda: self.create_queue(func_name='_GAUP'))
            case 'E':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Innosetup', ext_list=after_dot['_Innosetup']))
            case 'F':
                btn.clicked.connect(self.ffmpeg_video)
            case 'G':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Unreal', ext_list=after_dot['_Unreal']))
            case 'H':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Unity', select_folder=True))
            case 'I':
                btn.clicked.connect(lambda: self.create_queue(func_name='_idTech', ext_list=after_dot['_idTech']))
            case 'J':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Total'))
            case 'K':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Bethesda', ext_list=after_dot['_Bethesda']))
            case 'L':
                btn.clicked.connect(lambda: self.create_queue(func_name='_CryEngine', ext_list=after_dot['_CryEngine']))
            case 'M':
                btn.clicked.connect(lambda: os.system('data\\rad_tools\\radvideo64.exe'))
            case 'N':
                # btn.clicked.connect(self.wwise_tools)
                btn.clicked.connect(self.image_to_dds_nv)
            case 'O':
                # btn.clicked.connect(self.ps_audio_tools)
                btn.clicked.connect(self.image_to_dds_ms)
            case 'P':
                btn.clicked.connect(self.nConvert)
            case 'Q':
                btn.clicked.connect(lambda: self.create_queue(func_name='_RedEngine', ext_list=after_dot['_RedEngine']))
            case 'R':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Godot', ext_list=after_dot['_Godot']))
            case 'S':
                btn.clicked.connect(lambda: self.create_queue(func_name='_RPGMaker', ext_list=after_dot['_RPGMaker']))
            case 'T':
                btn.clicked.connect(lambda: self.create_queue(func_name='_RenPy', ext_list=after_dot['_RenPy']))
            case 'U':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Unigene', ext_list=after_dot['_Unigene']))
            case 'V':
                btn.clicked.connect(self.raw2dds)
            case 'W':
                btn.clicked.connect(self.raw2atrac)
            case 'X':
                btn.clicked.connect(self.raw2wav)
            case 'Y':
                btn.clicked.connect(lambda: setting_ui.SettingWindow(style=self.setting["Main"]["theme"]).exec())
            case 'Z':
                btn.clicked.connect(self.empty_out)

    # Создаются кнопки в верхнем меню
    def buttons_create(self):
        self.setting.read(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini')
        alpha = ['A']

        for j in range(1, 13):
            alpha.append(self.setting["Buttons"][str(j)])

        alpha.append('Y')
        alpha.append('Z')

        QFontDatabase.addApplicationFont('data/fonts/IconLib.otf')

        tool_tips = {'A': localize.quick_of,
                     'B': localize.open_qbms,
                     'C': localize.open_7z,
                     'D': localize.open_gaup,
                     'E': localize.open_inno,
                     'F': localize.convert_ffmpeg,
                     'G': localize.unpack_unreal,
                     'H': localize.unpack_unity,
                     'I': localize.unpack_idtech,
                     'J': localize.unpack_source,
                     'K': localize.unpack_creation,
                     'L': localize.unpack_cry,
                     'M': localize.convert_bink,
                     'N': localize.convert_wwise,
                     'O': localize.ps_audio_tool,
                     'P': localize.convert_nconvert,
                     'Q': localize.unpack_red,
                     'R': localize.unpack_godot,
                     'S': localize.unpack_rpgmaker,
                     'T': localize.unpack_renpy,
                     'U': localize.unpack_unigen,
                     'V': localize.header_dds,
                     'W': localize.header_atrac,
                     'X': localize.header_wav,
                     'Y': localize.run_setting,
                     'Z': localize.empty_of}

        for i in range(self.upperButtons.count()):
            item = self.upperButtons.itemAt(i)
            item.widget().deleteLater()

        for i, a in enumerate(alpha):
            btn = QToolButton(text=a, parent=None)
            btn.setToolTip(tool_tips[a])
            btn.setStyleSheet(
                'QToolButton {'
                f"font-family: IconLib;"
                'border: 0px;'
                'margin: 0px;'
                'padding: 0px;'
                'border-radius: 10px;'
                'height: 40px;'
                'width: 40px;'
                'font-size: 40px;'
                '}')

            if i not in (0, 13, 14, -1):
                self.add_button(btn, contexts=[localize.change_button, localize.cancel],
                                l_func=(lambda *args, l=i:
                                        self.new_button(style=self.setting["Main"]["theme"], alpha=l)))
            elif i == 14:
                self.add_button(btn, contexts=[localize.delete_to_trash, localize.full_delete, localize.cancel],
                                l_func=[lambda: self.set_setting('Main', 'trash', '1'),
                                        lambda: self.set_setting('Main', 'trash', '0')])
            else:
                self.add_button(btn)

            self.add_btn_action(btn, a)
            self.upperButtons.addWidget(btn)

    def new_button(self, style, alpha):
        cbm.CBWindow(style=style, letter=alpha).exec()
        self.buttons_create()

    # Наполняет списком меню "Архивы", "Образы дисков" и "Игровые Движки".
    def archive_list_create(self):

        engine = sqlalchemy.create_engine("sqlite:///game_base.db")

        with engine.connect() as conn:
            metadata = sqlalchemy.MetaData()
            archives_list = sqlalchemy.Table('archives_list', metadata, autoload_with=engine)
            table = sqlalchemy.Table(archives_list, metadata, autoload_with=engine)
            query = sqlalchemy.select(table)
            archivesList = pandas.read_sql_query(query, conn)

        if self.setting['Main']['group_arch'] == '2':
            abc = sorted(list({archivesList['ArchivesName'][n][0].upper() for n in range(len(archivesList))
                               if archivesList['Index'][n] not in (3, 5, 4) and archivesList['ArchivesName'][n][0]
                               not in '0123456789'}), key=lambda x: x)
            self.archive_list = {'0-9': self.menu_archives.addMenu('0-9')}

            for liter in abc:
                self.archive_list[liter] = self.menu_archives.addMenu(liter)

        if self.setting['Main']['group_ge'] == '2':
            abc2 = sorted(list({archivesList['ArchivesName'][n][0].upper() for n in range(len(archivesList))
                                if archivesList['Index'][n] == 4 and archivesList['ArchivesName'][n][0]
                                not in '0123456789'}), key=lambda x: x)
            self.engine_list = {'0-9': self.menu_game_engines.addMenu('0-9')}

            for liter in abc2:
                self.engine_list[liter] = self.menu_game_engines.addMenu(liter)

        for n in range(len(archivesList)):
            arch_name = archivesList['ArchivesName'][n]
            func_name = archivesList['Function'][n]
            ext_list = archivesList['ExtList'][n]
            program_name = archivesList['ProgramName'][n]
            unp_com1 = archivesList['Unpackcom1'][n]
            unp_com2 = archivesList['Unpackcom2'][n]
            pak_com = archivesList['Packcom'][n]
            arch_move = archivesList['Archivemove'][n]
            arch_ext = archivesList['ProgramName'][n]
            ff = archivesList['ff'][n]

            if archivesList['Index'][n] == 3:
                new_item = self.menu_disk_images.addAction(arch_name)
            elif archivesList['Index'][n] == 4:

                if self.setting['Main']['group_ge'] == '2':
                    liter = arch_name[0].upper()

                    if liter in '0123456789':
                        new_item = self.engine_list['0-9'].addAction(arch_name)
                    else:
                        new_item = self.engine_list[liter].addAction(arch_name)

                else:
                    new_item = self.menu_game_engines.addAction(arch_name)

            elif archivesList['Index'][n] == 5:
                new_item = self.menu_installers.addAction(arch_name)
            else:

                if self.setting['Main']['group_arch'] == '2':
                    liter = arch_name[0].upper()

                    if liter in '0123456789':
                        new_item = self.archive_list['0-9'].addAction(arch_name)
                    else:
                        new_item = self.archive_list[liter].addAction(arch_name)

                else:
                    new_item = self.menu_archives.addAction(arch_name)

            new_item.triggered.connect(lambda *args, func=func_name, ext=ext_list, prg=program_name, f_f=ff,
                                              c1=unp_com1, c2=unp_com2, pak=pak_com, a_move=arch_move, a_ext=arch_ext:
                                       self.create_queue(func_name=func, ext_list=ext, script_name=prg,
                                                         # ff=f_f, com1=c1, com2=c2, pak=pak, a_move=arch_move, a_ext=a_ext
                                                         ))

    def flc(self, items):
        self.comboBox_gameList.items = items
        self.filter_model.clear()
        self.filter_model.appendRow(QStandardItem(''))

        for item in items:
            self.filter_model.appendRow(QStandardItem(item))

        self.comboBox_gameList.setModel(self.filter_model)

    def filter_list_create(self, items):
        Thread(target=self.flc, daemon=True, args=(items,)).start()

    # Создается список игр в три-вью
    def tree_view_create(self):
        self.mainList = self.mainList.sort_values(by='game_name', key=lambda x: x.str.lower()).reset_index(drop=True)

        for _, row in self.mainList.iterrows():
            self.current_game += 1
            self.names[row['game_name']] = row['release_year']

        # Сортировка по имени
        if self.setting['Main']['group'] == 'name':
            new_parent = QStandardItem('0-9')
            self.parent_list['0-9'] = new_parent
            self.root_item.appendRow(new_parent)

            for item in self.abc:
                new_parent = QStandardItem(item)
                self.parent_list[item] = new_parent
                self.root_item.appendRow(new_parent)

            new_parent = QStandardItem(localize.other)
            self.parent_list[localize.other] = new_parent
            self.root_item.appendRow(new_parent)

            for name in self.names:

                if name[0].upper() in '0123456789':
                    literal = '0-9'
                elif name[0].upper() in self.abc:
                    literal = name[0].upper()
                else:
                    literal = localize.other

                child = QStandardItem(name)
                child.setToolTip(name)
                self.parent_list[literal].appendRow(child)

        # Сортировка по годам
        else:
            new_parent = QStandardItem(localize.other)
            self.parent_list[localize.other] = new_parent
            self.root_item.appendRow(new_parent)
            old_games = QStandardItem('... - 1990')
            self.parent_list['... - 1990'] = old_games
            year_now = datetime.now().year

            for i in range(year_now, 1990, -1):
                item = str(i)
                new_parent = QStandardItem(item)
                self.parent_list[item] = new_parent
                self.root_item.appendRow(new_parent)

            for name in self.names:

                try:
                    y = int(self.names[name])

                    if y < 1991:
                        y = '... - 1990'
                    else:
                        y = str(y)

                except (ValueError, TypeError):
                    y = localize.other

                child = QStandardItem(name)
                child.setToolTip(name)
                self.parent_list[y].appendRow(child)

            self.root_item.appendRow(old_games)

        self.filter_list_create(self.names)
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, localize.select_something)
        self.all_games_count.setText(f'{localize.all_games} {self.all_games}')

    def change_theme(self, theme_name):
        apply_stylesheet(self, theme=f'{theme_name}.xml')
        self.set_setting('Main', 'theme', theme_name)
        self.themes_list_create()

    def change_lang(self, lang):
        self.set_setting('Main', 'lang', lang)
        self.lang_list_create()
        importlib.reload(localize)
        self.buttons_create()
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, localize.select_something)
        self.all_games_count.setText(f'{localize.all_games} {self.all_games}')
        self.retranslateUi()
