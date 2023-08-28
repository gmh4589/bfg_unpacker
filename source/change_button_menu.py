
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet


class CBWindow(QDialog):

    def __init__(self, letter='A', style='dark_orange'):
        super().__init__()
        self.setWindowTitle("Change buttons")
        self.resize(255, 255)
        apply_stylesheet(self, theme=f'{style}.xml')
        print(letter)
        central_widget = QWidget(self)
        # self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(central_widget)

        alphabet = "BCDEFGHIJKLMNOPQRSTUVWXY1"
        row, col = 0, 0

        for liter in alphabet:
            button = QToolButton(text=liter)
            button.setStyleSheet(open('./source/ui/buttons.css').read())
            grid_layout.addWidget(button, row, col)
            col += 1

            if col == 5:
                col = 0
                row += 1

