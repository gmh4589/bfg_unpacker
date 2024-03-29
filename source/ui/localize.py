import configparser
import json
import os
import locale

setting = configparser.ConfigParser()

if os.path.exists('./setting.ini'):
    setting.read('./setting.ini')
    lang = setting['Main']['lang']
else:
    lang = locale.getdefaultlocale()[0].split('_')[0]

if not os.path.exists(f'./data/local/{lang}.json'):
    lang = 'en'

with open(f'./data/local/{lang}.json', 'r', encoding='utf-8') as json_file:
    local = json.load(json_file)

all_games = local['all_games']
find = local['find']
all_caps = local['all_caps']
fav_caps = local['fav_caps']
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
autofind = local['autofind']
archive_scanner = local['archive_scanner']
find_zip_method = local['find_zip_method']
zip_method = local['zip_method']
file_list = local['file_list']
create_theme = local['create_theme']
select_something = local['select_something']
change_button = local['change_button']
cancel = local['cancel']
delete_to_trash = local['delete_to_trash']
full_delete = local['full_delete']
group_by = local['group_by']
show_on = local['show_on']
by_name = local['by_name']
by_years = local['by_years']
context_menu = local['context_menu']
out_folder = local['out_folder']
apply = local['apply']
save_theme = local['save_theme']
primary_color = local['primary_color']
primary_light = local['primary_light']
second_color = local['second_color']
second_light = local['second_light']
second_dark = local['second_dark']
font_color_1 = local['font_color_1']
font_color_2 = local['font_color_2']
enter_theme_name = local['enter_theme_name']
zoom = local['zoom']
select_folder = local["select_folder"]
open_file = local["open_file"]
message = local["message"]
successfully = local["successfully"]
has_already_been = local["has_already_been"]
not_correct_file = local["not_correct_file"]
done = local["done"]
saving = local["saving"]
planet_added = local["planet_added"]
star_added = local["star_added"]
exo_catalog = local["exo_catalog"]
data_about = local["data_about"]
planets = local["planets"]
source = local["source"]
make_with = local["make_with"]
wait = local["wait"]
not_unzipped = local["not_unzipped"]
deleting = local["deleting"]
unpacking = local["unpacking"]
empty_folder = local["empty_folder"]
creating = local["creating"]
work_in_progress = local["work_in_progress"]
unsupported_platform = local["unsupported_platform"]
disc_image = local["disc_image"]
classic_consoles = local["classic_consoles"]
error = local["error"]
all_files = local["all_files"]
quick_of = local["quick_of"]
open_qbms = local["open_qbms"]
open_7z = local["open_7z"]
open_gaup = local["open_gaup"]
open_inno = local["open_inno"]
convert_ffmpeg = local["convert_ffmpeg"]
convert_bink = local["convert_bink"]
convert_wwise = local["convert_wwise"]
convert_nconvert = local["convert_nconvert"]
unpack_unreal = local["unpack_unreal"]
unpack_unity = local["unpack_unity"]
unpack_idtech = local["unpack_idtech"]
unpack_source = local["unpack_source"]
unpack_creation = local["unpack_creation"]
unpack_cry = local["unpack_cry"]
unpack_red = local["unpack_red"]
unpack_godot = local["unpack_godot"]
unpack_rpgmaker = local["unpack_rpgmaker"]
unpack_renpy = local["unpack_renpy"]
unpack_unigen = local["unpack_unigen"]
ps_audio_tool = local["ps_audio_tool"]
header_dds = local["header_dds"]
header_atrac = local["header_atrac"]
header_wav = local["header_wav"]
run_setting = local["run_setting"]
empty_of = local["empty_of"]
alphabet = local["alphabet"]
close = local["close"]
