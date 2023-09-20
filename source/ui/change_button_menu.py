import configparser

from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet

from source.ui import resize


class CBWindow(QDialog):

    def __init__(self, letter, style='dark_orange'):
        super().__init__()
        self.setWindowTitle("Change buttons")
        self.resize(resize.widget(255), resize.widget(255))
        self.style = style
        apply_stylesheet(self, theme=f'{style}.xml')

        central_widget = QWidget(self)

        grid_layout = QGridLayout(central_widget)

        alphabet = "BCDEFGHIJKLMNOPQRSTUVWX12"
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
                f'height: {resize.widget(40)}px;'
                f'width: {resize.widget(40)}px;'
                f'font-size: {resize.widget(40)}px;'
                '}')
            grid_layout.addWidget(button, row, col)
            self.add_button(button, liter, letter)
            col += 1

            if col == 5:
                col = 0
                row += 1

    def add_button(self, btn, number, letter):
        btn.clicked.connect(lambda *args, n=str(number), l=int(letter): self.save_button(n, l))

    def show_message_box(self, text):
        message_box = QMessageBox()
        message_box.setWindowTitle('Сообщение')  # TODO: text!!!
        message_box.setText(f'Кнопка {text} добавлена!')  # TODO: text!!!
        message_box.setIcon(QMessageBox.Information)
        message_box.setStandardButtons(QMessageBox.Ok)
        apply_stylesheet(message_box, theme=f'{self.style}.xml')
        message_box.exec()

    def save_button(self, a, num):
        setting = configparser.ConfigParser()
        setting.read('./setting.ini')
        buttons = [button for button in setting['Buttons'].values()]

        if a in buttons:
            self.show_message_box('уже')  # TODO: text!!!
        else:
            self.show_message_box('успешно')  # TODO: text!!!
            setting.set('Buttons', str(num), str(a))

            with open('./setting.ini', "w") as config_file:
                setting.write(config_file)
