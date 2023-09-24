
from tkinter import filedialog
import configparser


def select():
    setting = configparser.ConfigParser()
    setting.read('./setting.ini')
    out_path = filedialog.askdirectory(title='Select folder')

    setting['Main']['out_path'] = out_path

    with open('./setting.ini', "w") as config_file:
        setting.write(config_file)
