
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class CustomDialog(QDialog):

    def __init__(self, title='Warning!',
                 btnOK = True,
                 btnCancel = False,
                 text = 'Bla-bla-bla'):
        super().__init__()

        self.setWindowTitle(title)

        if btnOK and btnCancel:
            self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        elif btnOK:
            self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        elif btnCancel:
            self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(text)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
