import configparser

setting = configparser.ConfigParser()
setting.read('./setting.ini')

try:
    zoom = float(setting['Main']['zoom'])
except KeyError:
    zoom = 1.0


def widget(size):
    return int(size * zoom)
