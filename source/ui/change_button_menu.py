import configparser
import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
from qt_material import apply_stylesheet

from source.ui import localize
from source.ui.custom_ui import CustomDialog


class CBWindow(QDialog):

    def __init__(self, letter, style='dark_orange'):
        super().__init__()
        self.setWindowTitle("Change buttons")
        self.resize(255, 255)
        self.setWindowIcon(QIcon('./data/icons/i.ico'))
        self.style = style
        apply_stylesheet(self, theme=f'{style}.xml')

        central_widget = QWidget(self)

        grid_layout = QGridLayout(central_widget)

        alphabet = "BCDEFGHIJKLMNOPQRSTUVWX✖"
        row, col = 0, 0

        for liter in alphabet:
            button = QToolButton(text=liter)
            button.setStyleSheet(
                'QToolButton {'
                "font-family: 'IconLib';"
                'border: 0px;'
                'margin: 0px;'
                'padding: 0px;'
                'border-radius: 10px;'
                f'height: 40px;'
                f'width: 40px;'
                f'font-size: 40px;'
                '}')
            grid_layout.addWidget(button, row, col)
            self.add_button(button, liter, letter)

            col += 1

            if col == 5:
                col = 0
                row += 1

    def add_button(self, btn, number, letter):
        btn.clicked.connect(lambda *args, n=str(number), l=int(letter): self.save_button(n, l))

    def save_button(self, a, num):

        if a != '✖':
            setting = configparser.ConfigParser()
            setting.read(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini')
            buttons = [button for button in setting['Buttons'].values()]

            if a in buttons:
                CustomDialog(text=f'{localize.has_already_been}').exec()
            else:
                CustomDialog(text=f'{localize.successfully}').exec()
                setting.set('Buttons', str(num), str(a))

                with open(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini', "w") as config_file:
                    setting.write(config_file)
        else:
            self.close()
