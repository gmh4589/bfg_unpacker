import os
from tkinter.messagebox import showinfo, showerror

from PIL.ImageQt import QImage
from PIL import Image
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QDialog, QMenu
from qt_material import apply_stylesheet
from icecream import ic

from source.setting import theme, out_path
from source.ui import localize


class CubeMapGUI(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./data/icons/i.ico'))
        apply_stylesheet(self, theme=f'{theme}.xml')
        self.setWindowTitle("CubeMap Creator")
        self.setAcceptDrops(True)
        self.resize(420, 365)
        self.setMinimumSize(420, 365)
        self.setMaximumSize(420, 365)
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 400, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label_0_0 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout.addWidget(self.label_0_0)
        self.label_0_1 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout.addWidget(self.label_0_1)
        self.label_0_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout.addWidget(self.label_0_2)
        self.label_0_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout.addWidget(self.label_0_3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.label_1_0 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.label_1_0)
        self.label_1_1 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.label_1_1)
        self.label_1_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.label_1_2)
        self.label_1_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.label_1_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.label_2_0 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.label_2_0)
        self.label_2_1 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.label_2_1)
        self.label_2_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.label_2_2)
        self.label_2_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.label_2_3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.create_btn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.create_btn.setGeometry(QtCore.QRect(200, 320, 100, 25))
        self.create_btn.setText(localize.create)
        self.create_btn.clicked.connect(self.create_cubemap)
        self.clear_btn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clear_btn.setGeometry(QtCore.QRect(305, 320, 100, 25))
        self.clear_btn.setText(localize.clear)
        self.clear_btn.clicked.connect(self.clear_all)

        self.dummy_image = QPixmap(QImage('data\\icons\\dummy.png')).scaled(95, 95)

        self.label_0_1.setPixmap(self.dummy_image)
        self.label_1_0.setPixmap(self.dummy_image)
        self.label_1_1.setPixmap(self.dummy_image)
        self.label_1_2.setPixmap(self.dummy_image)
        self.label_1_3.setPixmap(self.dummy_image)
        self.label_2_1.setPixmap(self.dummy_image)

        self.images = {
            '0': [self.label_0_1, None],
            '1': [self.label_1_0, None],
            '2': [self.label_1_1, None],
            '3': [self.label_1_2, None],
            '4': [self.label_1_3, None],
            '5': [self.label_2_1, None],
                       }

        for key, label in self.images.items():
            self.create_cm(key, label[0])

    def create_cm(self, key, label):
        context_menu = QMenu(self)
        delete = context_menu.addAction(localize.delete)
        delete.triggered.connect(lambda: self.clear_one(key, label))
        label.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        label.customContextMenuRequested.connect(lambda pos: context_menu.exec(label.mapToGlobal(pos)))

    def clear_one(self, key, label):
        self.images[key] = [label, None]
        label.setPixmap(self.dummy_image)

    def clear_all(self):

        for key, value in self.images.items():
            label = value[0]
            label.setPixmap(self.dummy_image)
            self.images[key] = [label, None]

    def create_cubemap(self):
        head = b''
        image_data = b''
        ic(self.images.items())

        for im in '310524':
            image_path = self.images[im][1]

            if image_path is None:
                showinfo(localize.info, localize.six_images)
                break

            if image_path.split('.')[-1] != 'dds':
                os.makedirs(os.environ['TEMP'] + '\\qmc', exist_ok=True)
                (Image
                     .open(image_path)
                     .convert('RGBA')
                     .save(os.environ['TEMP'] + '\\qmc\\temp.dds')
                     )
                image_path = os.environ['TEMP'] + '\\qmc\\temp.dds'

            with open(image_path, 'rb') as dds_image:

                if not head:
                    head = dds_image.read(0x80)
                    head = head[:0x71] + b'\xFE' + head[0x72:]
                else:
                    dds_image.seek(0x80)

                image_data += dds_image.read()

        if image_data and head:

            with open(f'{out_path}\\out.dds', 'wb') as new_cm:
                new_cm.write(head + image_data)

    @staticmethod
    def dragEnterEvent(event):
        mime_data = event.mimeData()

        if mime_data.hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()

        if mime_data.hasUrls():

            for path in mime_data.urls():
                path = path.toLocalFile()

                for label in self.images.values():

                    if label[1] is None:
                        ext = path.split('.')[-1]

                        if ext in ('png', 'bmp', 'tif', 'tiff', 'gif', 'jpeg', 'j', 'jpe', 'jpg'):
                            image = QImage(path)
                        else:
                            os.makedirs(os.environ['TEMP'] + '\\qmc', exist_ok=True)

                            try:
                                (Image
                                      .open(path)
                                      .convert('RGBA')
                                      .save(os.environ['TEMP'] + '\\qmc\\temp.png')
                                      )
                                image = QImage(os.environ['TEMP'] + '\\qmc\\temp.png')
                            except (NotImplementedError, OSError, ZeroDivisionError):
                                showerror(localize.warning, localize.unsupported_ftype)
                                image = None

                        if image is not None:
                            label[1] = path
                            pixmap = QPixmap(image).scaled(95, 95)
                            label[0].setPixmap(pixmap)

                        break

                else:
                    showinfo(localize.info, localize.already_6)

