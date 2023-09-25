import configparser

setting = configparser.ConfigParser()
setting.read('./setting.ini')


def widget(size):
    return int(size * float(setting['Main']['zoom']))
