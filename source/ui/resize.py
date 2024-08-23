import configparser
import os

setting = configparser.ConfigParser()
setting.read(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini')

try:
    zoom = float(setting['Main']['zoom'])
except KeyError:
    zoom = 1.0


def widget(size):
    return int(size * zoom)
