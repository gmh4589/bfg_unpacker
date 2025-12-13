import importlib
import json
import os
from datetime import datetime

from PyQt6.QtCore import Qt, QItemSelectionModel, QRect
from PyQt6.QtGui import QStandardItem, QIcon, QFontDatabase
from PyQt6.QtWidgets import QMainWindow, QMenu, QFileDialog, QToolButton
from icecream import ic

from source.ui.main_ui import Ui_BFGUnpacker
from qt_material import apply_stylesheet
from qt_material import list_themes
from source.reapers.ext_list import after_dot
from source.ui.loader import LoaderData
from source.ui.setting import SettingWindow
from source.ui.change_button_menu import CBWindow
from source.db_connect import DatabaseConnect
from source.ui import localize
from source.setting import setting, set_setting


# Методы для наполнения интерфейса данными
class MainWindow(QMainWindow, Ui_BFGUnpacker):
    db = DatabaseConnect()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        item = item.strip()

        if item != '':

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

        if self.theme == 'default':
            default_theme.setIcon(QIcon('./data/icons/checked.svg'))

        for theme in list_themes():
            theme_name = theme.split('.')[0]

            if theme_name not in default_themes or theme_name == self.theme:
                new_theme = self.themes_list_2.addAction(theme_name.replace('_', ' ').title())
            else:
                new_theme = other_themes_submenu.addAction(theme_name.replace('_', ' ').title())

            new_theme.triggered.connect(lambda *args, x=theme_name: self.change_theme(x))

            if theme_name == self.theme:
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

            if lang_codes[i] in main_list or lang_codes[i] == self.lang:
                new_lang = self.action_Language.addAction(lang)
            else:
                new_lang = other_submenu.addAction(lang)

            new_lang.triggered.connect(lambda *args, x=lang_codes[i]: self.change_lang(x))

            if lang_codes[i] == self.lang:
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
                # btn.clicked.connect(self.q_open)
                btn.clicked.connect(self.create_queue)
            case 'B':
                btn.clicked.connect(lambda: self.create_queue(script_name=QFileDialog.getOpenFileName(
                                                              self, localize.open_file,
                                                              filter='QuickBMS Scripts (*.bms);;QuickBMS Scripts (*.txt);;'
                                                              f'{localize.all_files} (*.*)',
                                                              directory=self.setting['Main']['last_dir'])[0]))
            case 'C':
                btn.clicked.connect(lambda: self.create_queue(func_name='_7ZIP'))
            case 'D':
                btn.clicked.connect(lambda: self.create_queue(func_name='_QuickBMS', script_name=f"{self.path_to_root}\\data\\wcx\\gaup_pro.wcx"))
            case 'E':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Innosetup', ext_list=after_dot['_Innosetup']))
            case 'F':
                btn.clicked.connect(lambda: self.childs.ffmpeg_video())
            case 'G':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Unreal', ext_list=after_dot['_Unreal']))
            case 'H':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Unity', select_folder=True))
            case 'I':
                btn.clicked.connect(lambda: self.create_queue(func_name='_idTech', ext_list=after_dot['_idTech']))
            case 'J':
                btn.clicked.connect(lambda: self.create_queue(func_name='_QuickBMS', script_name=f"{self.path_to_root}\\data\\wcx\\TotalObserver.wcx"))
            case 'K':
                btn.clicked.connect(lambda: self.create_queue(func_name='_Bethesda', ext_list=after_dot['_Bethesda']))
            case 'L':
                btn.clicked.connect(lambda: self.create_queue(func_name='_CryEngine', ext_list=after_dot['_CryEngine']))
            case 'M':
                btn.clicked.connect(lambda: os.system('data\\rad_tools\\radvideo64.exe'))
            case 'N':
                # btn.clicked.connect(self.wwise_tools)
                btn.clicked.connect(lambda: self.childs.image_to_dds_nv())
            case 'O':
                # btn.clicked.connect(self.ps_audio_tools)
                btn.clicked.connect(lambda: self.childs.image_to_dds_ms())
            case 'P':
                btn.clicked.connect(lambda: self.childs.pillow_conv())
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
                btn.clicked.connect(lambda: self.childs.raw2dds())
            case 'W':
                btn.clicked.connect(lambda: self.childs.raw2atrac())
            case 'X':
                btn.clicked.connect(lambda: self.childs.raw2wav())
            case 'Y':
                btn.clicked.connect(lambda: SettingWindow().exec())
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
                     'P': localize.convert_pillow,
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
                'font-family: IconLib;'
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
                                l_func=(lambda *args, literal=i:
                                        self.new_button(style=self.theme, alpha=literal)))
            elif i == 14:
                self.add_button(btn, contexts=[localize.delete_to_trash, localize.full_delete, localize.cancel],
                                l_func=[lambda: set_setting('Main', 'trash', '1'),
                                        lambda: set_setting('Main', 'trash', '0')])
            else:
                self.add_button(btn)

            self.add_btn_action(btn, a)
            self.upperButtons.addWidget(btn)

    def new_button(self, style, alpha):
        CBWindow(style=style, letter=alpha).exec()
        self.buttons_create()

    # Наполняет списком меню "Архивы", "Образы дисков" и "Игровые Движки".
    def archive_list_create(self):
        archivesList = self.db.get_table('archives_list', filter=True)

        def create_literal_submenus(idx, menu_item):
            abc = sorted(list({archivesList['ArchivesName'][n][0].upper() for n in range(len(archivesList))
                               if archivesList['Index'][n] == idx and archivesList['ArchivesName'][n][0] not in '0123456789'}), 
                               key=lambda x: x)
            items_list = {'0-9': menu_item.addMenu('0-9')}

            for liter in abc:
                items_list[liter] = menu_item.addMenu(liter)
            
            return items_list

        if self.setting['Main']['group_arch'] == '2':
            self.archive_list = create_literal_submenus(1, self.menu_archives)

        if self.setting['Main']['group_ge'] == '2':
            self.engine_list = create_literal_submenus(4, self.menu_game_engines)

        # 1 = Archives, 3 = Disk images, 4 = Game Engines, 5 = Installers
        for n in range(len(archivesList)):
            arch_name = archivesList['ArchivesName'][n]
            func_name = archivesList['Function'][n]
            ext_list = archivesList['ExtList'][n]
            unp_com = archivesList['Unpackcom'][n]
            pak_com = archivesList['Packcom'][n]

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

            new_item.triggered.connect(lambda *args, func=func_name, exts=ext_list, unpack_com=unp_com, pack_com=pak_com:
                                       self.archive_execute(func_name=func, ext_list=exts, unpack_com=unpack_com, pack_com=pack_com))

    def archive_execute(self, func_name, ext_list, unpack_com, pack_com):
        packing = (True if self.checkBox_Reimport.isChecked() else False) if pack_com != 'not' else False
        ic(self.checkBox_Reimport.isChecked())
        self.func_name = func_name
        self.script_name = pack_com if packing else unpack_com
        self.file_list = list(self.file_open(ext_list, select_folder=True if packing else False))
        self.last_run = self.find_reaper
        self.find_reaper()

    def filter_list_create(self, items):
        self.comboBox_gameList.items = items
        self.filter_model.clear()
        self.filter_model.appendRow(QStandardItem(''))

        for item in items:
            self.filter_model.appendRow(QStandardItem(item))

        self.comboBox_gameList.setModel(self.filter_model)

    def get_literal(self, name, year, sort_by_names, def_item):
        literal = name[0].upper()

        # Проверка на название, начинающиеся не с цифры и не с латиницы, либо год неизвестен
        if (sort_by_names and literal not in self.abc + '0123456789') or (not sort_by_names and year == -1):
            return localize.other
        # Проверка на название, начинающиеся с цифры, либо игра выпущена до 1991 года
        if (sort_by_names and literal in '0123456789') or (not sort_by_names and year <= 1990):
            return def_item

        # Возвращает букву либо год, если предыдущие условие не выполнены
        return literal if sort_by_names else str(year)
    
    def create_parent_list(self, root, sort_by_names, default_item_name):
        items_list = self.abc if sort_by_names else range(1991, datetime.now().year + 1)

        default_parent = QStandardItem(default_item_name)
        self.parent_list[default_item_name] = default_parent
        root.appendRow(default_parent)

        for item in items_list:
            item = str(item)
            new_parent = QStandardItem(item)
            self.parent_list[item] = new_parent
            root.appendRow(new_parent)
        
        other_parent = QStandardItem(localize.other)
        self.parent_list[localize.other] = other_parent
        root.appendRow(other_parent)

    # Создается список игр в три-вью
    def tree_view_create(self):
        self.mainList = self.mainList.sort_values(by='game_name', key=lambda x: x.str.lower()).reset_index(drop=True)
        loader_data = LoaderData()
        loader_data.all_games = len(self.mainList)
        sort_by_names = self.setting['Main']['group'] == 'name'
        default_item_name = '0-9' if sort_by_names else '... - 1990'
        self.create_parent_list(self.root_item, sort_by_names, default_item_name)

        for _, row in self.mainList.iterrows():
            self.current_game += 1
            name = row['game_name']
            loader_data.current_game = self.current_game
            loader_data.game_name = name
            self.names[row['game_name']] = row['release_year']

            try:
                year = int(row['release_year'])
            except (ValueError, TypeError):
                year = -1
            
            new_lit = self.get_literal(name, year, sort_by_names, default_item_name)

            child = QStandardItem(name)
            child.setToolTip(name)
            self.parent_list[new_lit].appendRow(child)

        self.filter_list_create(self.names)
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, localize.select_something)
        self.all_games_count.setText(f'{localize.all_games} {str(self.all_games)}')

    def change_theme(self, theme_name):
        apply_stylesheet(self, theme=f'{theme_name}.xml')
        set_setting('Main', 'theme', theme_name)
        self.theme = setting['Main']['theme']
        self.themes_list_create()

    def change_lang(self, lang):
        set_setting('Main', 'lang', lang)
        self.lang = setting['Main']['lang']
        importlib.reload(localize)
        self.buttons_create()
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, localize.select_something)
        self.all_games_count.setText(f'{localize.all_games} {self.all_games}')
        self.retranslateUi()
        self.lang_list_create()

    def resizeEvent(self, event):
        x = event.size().width()
        y = event.size().height()

        self.btn_All_Favorite.setGeometry(QRect(0, 40, 80, 30))
        self.comboBox_gameList.setGeometry(QRect(80, 40, x - 255, 30))
        self.toolButton_plus.setGeometry(QRect(x - 145, 40, 30, 30))
        self.toolButton_minus.setGeometry(QRect(x - 115, 40, 30, 30))
        self.toolButton_Find.setGeometry(QRect(x - 85, 40, 85, 30))
        
        self.gameList_treeView.setGeometry(QRect(0, 80, int(x / 2) - 5, y - 130))
        self.logWindow.setGeometry(QRect(int(x / 2), 80, int(x / 2) - 5, y - 130))

        self.all_games_count.setGeometry(QRect(x - 149, y - 47, 150, 20))
        self.checkBoxes.setGeometry(QRect(10, y - 50, 451, 20))

