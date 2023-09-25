
from tkinter import filedialog
import locale


def select(setting):
    out_path = filedialog.askdirectory(title='Select folder')
    set_setting(setting, 'Main', 'out_path', out_path)


def set_setting(setting, section, key, value):
    setting.set(section, key, value)

    with open('./setting.ini', "w") as config_file:
        setting.write(config_file)


def set_default(setting):

    setting.add_section('Main')
    setting.add_section('Buttons')
    setting.add_section('Engines')
    setting.set('Main', 'theme', 'classic_white')
    lng = locale.getdefaultlocale()[0].split('_')[0]
    setting.set('Main', 'lang', lng)
    setting.set('Main', 'group', 'name')
    setting.set('Main', 'zoom', '1.0')
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
