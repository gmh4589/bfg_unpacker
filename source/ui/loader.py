
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk

from source.reaper import Reaper, file_reaper
from source.setting import theme as theme_1
from source.ui import localize

class LoaderData:
    _instance = None

    def __init__(self):
        self.current_game = 0
        self.game_name = ''
        self.all_games = 0

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(LoaderData, cls).__new__(cls)

        return cls._instance

class Loader(Reaper):

    def __init__(self):
        super().__init__()

    @file_reaper
    def run(self):
        loader = LoaderData()

        while loader.current_game < loader.all_games:
            self.update_pb(loader.all_games, loader.current_game, loader.game_name)

        self.update_pb(loader.all_games, loader.all_games, loader.game_name)

def pb_show():
    loader = LoaderData()
    theme = f'data/themes/{theme_1}.xml'

    try:
        tree = ET.parse(theme)
    except FileNotFoundError:
        tree = ET.parse('data/themes/classic_white.xml')

    xml = tree.getroot()
    color_dict = {}

    for color in xml.findall('color'):
        name = color.get('name')
        value = color.text
        color_dict[name] = value

    root = tk.Tk()
    root.overrideredirect(True)
    x = (root.winfo_screenwidth() - 250) / 2
    y = (root.winfo_screenheight() - 38) / 2
    root.geometry('250x40')
    root.wm_geometry("+%d+%d" % (x, y))

    info = ttk.Label()
    info.grid(row=0, column=0)
    progress_var = tk.DoubleVar()

    while not loader.all_games:
        info['text'] = f'{localize.wait}: {loader.current_game}/{loader.all_games}'

    bar = ttk.Progressbar(root, variable=progress_var, maximum=loader.all_games, length=250)
    bar.grid(row=1, column=0)
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TProgressbar",
                    background=color_dict['primaryColor'],
                    troughcolor=color_dict['secondaryLightColor'])
    style.configure("TLabel",
                    background=color_dict['secondaryDarkColor'],
                    foreground=color_dict['secondaryTextColor'])
    root['bg'] = color_dict['secondaryDarkColor']

    while loader.current_game < loader.all_games:
        root.update()
        progress_var.set(loader.current_game)
        info['text'] = f'{localize.wait}: {int(loader.current_game)}/{loader.all_games}'

    root.destroy()
    root.mainloop()
