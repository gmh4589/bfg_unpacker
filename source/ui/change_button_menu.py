
import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QToolButton, QWidget, QGridLayout
from qt_material import apply_stylesheet

from source.ui import localize
from source.ui.custom_ui import CustomDialog
from source.setting import setting, set_setting


class CBWindow(QDialog):

    def __init__(self, letter, style=''):
        super().__init__()
        self.setWindowTitle("Change buttons")
        self.setMinimumSize(255, 255)
        self.setMaximumSize(255, 255)
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
                'height: 40px;'
                'width: 40px;'
                'font-size: 40px;'
                '}')
            grid_layout.addWidget(button, row, col)
            self.add_button(button, liter, letter)

            col += 1

            if col == 5:
                col = 0
                row += 1

    def add_button(self, btn, number, letter):
        btn.clicked.connect(lambda *args, n=str(number), literal=int(letter): self.save_button(n, literal))

    def save_button(self, a, num):

        if a != '✖':
            buttons = [button for button in setting['Buttons'].values()]

            if a in buttons:
                CustomDialog(
                    title='INFO',
                    style=self.style,
                    text=f'{localize.has_already_been}'
                ).exec()
            else:
                CustomDialog(
                    title='INFO',
                    style=self.style,
                    text=f'{localize.successfully}'
                ).exec()
                set_setting('Buttons', str(num), str(a))

                with open(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini', "w") as config_file:
                    setting.write(config_file)
        else:
            self.close()
