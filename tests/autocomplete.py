from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QCompleter


class AutoCompleteComboBox(QComboBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.filter_model = QStandardItemModel()
        self.setEditable(True)

        # Создаем QCompleter и связываем его с QComboBox
        self.completer = QCompleter(self)
        self.setCompleter(self.completer)

        # Настраиваем QCompleter
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)  # Регистронезависимый поиск

        # Получаем связанный с QCompleter QLineEdit
        line_edit = self.lineEdit()

        # Подключаем обработчик события textEdited для QLineEdit
        line_edit.textEdited.connect(self.on_text_edited)

    def on_text_edited(self, text):
        # Очищаем модель
        self.filter_model.setRowCount(0)

        # Добавляем элементы для автозавершения
        items = ["Apple", "Banana", "Orange", "Mango", "Pineapple"]

        for item in items:
            if self.lineEdit().text().lower() in item.lower():
                self.filter_model.appendRow(QStandardItem(item))

        self.setModel(self.filter_model)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    combo_box = AutoCompleteComboBox()
    layout.addWidget(combo_box)

    window.setGeometry(100, 100, 300, 100)
    window.setWindowTitle("AutoComplete ComboBox Example")
    window.show()

    sys.exit(app.exec_())
