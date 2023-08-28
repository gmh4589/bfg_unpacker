import configparser
import json

setting = configparser.ConfigParser()
setting.read('./setting.ini')
lang = setting['Main']['lang']

with open(f'./source/local/{lang}.json', 'r', encoding='utf-8') as json_file:
    local = json.load(json_file)


all_games = local['all_games']
find = local['find']
all_caps = local['all_caps']
reimport = local['reimport']
show_console = local['show_console']
create_subfolders = local['create_subfolders']
file = local['file']
unpack_with = local['unpack_with']
compress_formats = local['compress_formats']
find_formats = local['find_formats']
additional = local['additional']
consoles = local['consoles']
other = local['other']
archives = local['archives']
game_engines = local['game_engines']
disk_images = local['disk_images']
installers = local['installers']
convert = local['convert']
video = local['video']
audio = local['audio']
textures = local['textures']
settings = local['settings']
themes = local['themes']
about = local['about']
quick_open = local['quick_open']
leave = local['leave']
language = local['language']
select_out_folder = local['select_out_folder']
clear_out_folder = local['clear_out_folder']
make_out_folder = local['make_out_folder']
delete_empty_files = local['delete_empty_files']
delete_empty_subfolders = local['delete_empty_subfolders']
autofind = local['autofind']
archive_scanner = local['archive_scanner']
file_list = local['file_list']
create_theme = local['create_theme']
select_something = local['select_something']
change_button = local['change_button']
cancel = local['cancel']
delete_to_trash = local['delete_to_trash']
full_delete = local['full_delete']
