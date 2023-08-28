import sys
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet


class ChildWindow(QDialog):

    def __init__(self, letter='A', style='dark_orange'):
        super().__init__()
        self.setWindowTitle("Child Window")
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


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(300, 200, 600, 400)

        self.button = QPushButton("Open Child Window", self)
        self.button.setGeometry(200, 150, 200, 50)
        self.button.clicked.connect(lambda: ChildWindow().exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
