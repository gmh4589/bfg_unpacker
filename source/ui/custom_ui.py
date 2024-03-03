
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QComboBox, QCompleter


class AutoCompleteComboBox(QComboBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.filter_model = QStandardItemModel()
        self.setEditable(True)
        self.completer = QCompleter(self)
        self.setCompleter(self.completer)
        self.items = []
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        line_edit = self.lineEdit()
        line_edit.textEdited.connect(self.on_text_edited)

    def on_text_edited(self, text):
        self.filter_model.clear()
        self.filter_model.appendRow(QStandardItem(self.lineEdit().text() + text
                                                  if text != self.lineEdit().text() else self.lineEdit().text()))

        for item in self.items:
            if self.lineEdit().text().lower() in item.lower():
                self.filter_model.appendRow(QStandardItem(item))

        self.setModel(self.filter_model)
