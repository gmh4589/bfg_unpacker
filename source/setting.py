import os
import configparser
import locale


setting_path = os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini'
lng = locale.getdefaultlocale()[0].split('_')[0]
os.makedirs(os.path.dirname(setting_path), exist_ok=True)
setting = configparser.ConfigParser()

default_settings = {
    'Main': {
        'theme': 'default',
        'lang': lng,
        'group': 'name',
        'last_dir': '',
        'out_path': 'None',
        'show_console': '0',
        'subfolders': '2',
        'group_ge': '2',
        'group_arch': '2',
        'load_bar': '0',
        'trash': '0',
        'fav_format': 'png',
        'context_menu': '2',
        'save_original_images': '2',
    },
    'Buttons': {
        '1': 'B',
        '2': 'C',
        '3': 'D',
        '4': 'E',
        '5': 'F',
        '6': 'G',
        '7': 'H',
        '8': 'I',
        '9': 'J',
        '10': 'K',
        '11': 'L',
        '12': 'M'
    },
    'Engines': {
        'unreal': '0',
        'unity': '0',
        'rpg_maker': '0',
        'game_maker': '0',
        'godot': '0',
        'renpy': '0',
    }
}

if not os.path.exists(setting_path):
    setting.add_section('Main')
    setting.add_section('Buttons')
    setting.add_section('Engines')
    setting.set('Main', 'theme', 'default')
    setting.set('Main', 'lang', lng)
    setting.set('Main', 'group', 'name')
    setting.set('Main', 'last_dir', '')
    setting.set('Main', 'out_path', 'None')
    setting.set('Main', 'trash', '0')
    setting.set('Main', 'show_console', '0')
    setting.set('Main', 'subfolders', '2')
    setting.set('Main', 'group_ge', '2')
    setting.set('Main', 'group_arch', '2')
    setting.set('Main', 'load_bar', '0')
    setting.set('Main', 'trash', '0')
    setting.set('Main', 'fav_format', 'png')
    setting.set('Main', 'context_menu', "2")
    setting.set('Main', 'save_original_images', "2")
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

    with open(setting_path, "w") as config_file:
        setting.write(config_file)

else:
    setting.read(setting_path)

    for group, names in default_settings.items():

        for name, default in names.items():

            try:
                test = setting[group][name]
            except KeyError:

                try:
                    setting.add_section(group)
                except configparser.DuplicateSectionError:
                    pass

                setting.set(group, name, default)

theme = setting['Main']['theme']

def set_setting(group, key, value):

    try:
        setting.set(group, key, value)
        
        with open(setting_path, "w") as config_file:
            setting.write(config_file)

    except KeyError:
        setting.add_section(group)
        set_setting()
