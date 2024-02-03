import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QMimeData


class FileDropWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Перетащите файл")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.label = QLabel("Перетащите файл сюда", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()

        if mime_data.hasUrls() and len(mime_data.urls()) == 1:
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()

        if mime_data.hasUrls():
            file_path = mime_data.urls()[0].toLocalFile()
            self.label.setText(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileDropWidget()
    window.show()
    sys.exit(app.exec())
