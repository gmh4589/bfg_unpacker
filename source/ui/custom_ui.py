from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt6.QtCore import QRect, QMetaObject
from PyQt6.QtWidgets import QComboBox, QCompleter, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QWidget, QProgressBar

from qt_material import apply_stylesheet
from source.setting import Setting
from source.ui import localize


class AutoCompleteComboBox(QComboBox, Setting):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_model = QStandardItemModel()
        self.setEditable(True)
        self.completer = QCompleter(self)
        self.setCompleter(self.completer)
        self.items = []
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.line_edit = self.lineEdit()
        self.line_edit.textEdited.connect(self.on_text_edited)
        self.setModel(self.filter_model)

    def on_text_edited(self, text):

        with open(f'./data/themes/{self.setting["Main"]["theme"]}.xml', 'r') as style_sheet:
            colors = [color.replace('</color>\n', '').split('">')[-1] for color in style_sheet.readlines()]

        completer_popup = self.completer.popup()
        completer_popup.setStyleSheet("QListView {"
                                      "  background-color: " + colors[4] + ";"
                                      "  color: " + colors[8] + ";"
                                      "  border: 1px solid " + colors[6] + ";"
                                      "}")

        self.filter_model.clear()
        self.filter_model.appendRow(QStandardItem(self.line_edit.text() + text
                                                  if text != self.line_edit.text() else self.line_edit.text()))

        for item in self.items:

            if self.line_edit.text().lower() in item.lower():
                self.filter_model.appendRow(QStandardItem(item))

        self.setModel(self.filter_model)


class CustomDialog(QDialog):
    returned_data = None

    def __init__(self,
                 text: str,
                 title: str = 'Warning!',
                 btnOK: bool = True,
                 btnCancel: bool = False,
                 combo: QComboBox = None,
                 style: str = 'dark_orange') -> None:
        super().__init__()
        self.setWindowIcon(QIcon('./data/icons/i.ico'))
        apply_stylesheet(self, theme=f'{style}.xml')
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.combo = combo

        if btnOK and btnCancel:
            self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                              QDialogButtonBox.StandardButton.Cancel)
        elif btnOK:
            self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        elif btnCancel:
            self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        message = QLabel(text)
        self.layout.addWidget(message)

        if combo is not None:
            self.layout.addWidget(self.combo)
            self.returned_data = self.combo.currentText()
            self.combo.currentTextChanged.connect(self.return_selected)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def return_selected(self):
        self.returned_data = self.combo.currentText()


class ProgressBar(QDialog):

    def __init__(self, style='dark_orange'):
        super().__init__()
        apply_stylesheet(self, theme=f'{style}.xml')
        self.resize(300, 130)
        self.setWindowIcon(QIcon('./data/icons/i.ico'))
        self.setWindowTitle(f"{localize.wait}...")
        self.centralwidget = QWidget(self)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(10, 40, 270, 30))
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(10, 10, 280, 20))
        self.progress = QLabel(self.centralwidget)
        self.progress.setGeometry(QRect(10, 80, 100, 20))
        self.status = QLabel(self.centralwidget)
        self.status.setGeometry(QRect(10, 100, 500, 20))
        self.is_stop = False
        QMetaObject.connectSlotsByName(self)

    def closeEvent(self, a0):
        self.is_stop = True


class PrintTo(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))

    def flush(self):
        pass
