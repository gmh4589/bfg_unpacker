
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import *

from qt_material import apply_stylesheet
import xml.etree.ElementTree as XML_Parce

import source.ui.localize as translate


class ThemeCreateWindow(QDialog):

    def __init__(self, style='dark_orange'):
        super().__init__()
        apply_stylesheet(self, theme=f'{style}.xml')

        try:
            root = XML_Parce.parse(f'./data/themes/{style}.xml').getroot()
        except FileNotFoundError:
            root = ''

        self.resize(270, 270)
        self.setWindowIcon(QIcon('./data/icons/i.ico'))
        self.centralwidget = QWidget(self)
        self.font = QFont()
        self.font.setPointSize(8)
        self.saveButton = QPushButton(self.centralwidget)
        self.saveButton.setFont(self.font)
        self.saveButton.setGeometry(QRect(10, 230, 250, 30))
        self.toolButton_1 = QToolButton(self.centralwidget)
        self.toolButton_1.setFont(self.font)
        self.toolButton_1.setGeometry(QRect(10, 10, 150, 30))
        self.toolButton_2 = QToolButton(self.centralwidget)
        self.toolButton_2.setFont(self.font)
        self.toolButton_2.setGeometry(QRect(10, 40, 150, 30))
        self.toolButton_3 = QToolButton(self.centralwidget)
        self.toolButton_3.setFont(self.font)
        self.toolButton_3.setGeometry(QRect(10, 70, 150, 30))
        self.toolButton_4 = QToolButton(self.centralwidget)
        self.toolButton_4.setFont(self.font)
        self.toolButton_4.setGeometry(QRect(10, 100, 150, 30))
        self.toolButton_5 = QToolButton(self.centralwidget)
        self.toolButton_5.setFont(self.font)
        self.toolButton_5.setGeometry(QRect(10, 130, 150, 30))
        self.toolButton_6 = QToolButton(self.centralwidget)
        self.toolButton_6.setFont(self.font)
        self.toolButton_6.setGeometry(QRect(10, 160, 150, 30))
        self.toolButton_7 = QToolButton(self.centralwidget)
        self.toolButton_7.setFont(self.font)
        self.toolButton_7.setGeometry(QRect(10, 190, 150, 30))
        self.widget = QWidget(self.centralwidget)
        self.widget.setGeometry(QRect(170, 10, 90, 200))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label1 = QLabel(self.widget)
        self.verticalLayout_2.addWidget(self.label1)
        self.label2 = QLabel(self.widget)
        self.verticalLayout_2.addWidget(self.label2)
        self.label3 = QLabel(self.widget)
        self.verticalLayout_2.addWidget(self.label3)
        self.label4 = QLabel(self.widget)
        self.verticalLayout_2.addWidget(self.label4)
        self.label5 = QLabel(self.widget)
        self.verticalLayout_2.addWidget(self.label5)
        self.label6 = QLabel(self.widget)
        self.verticalLayout_2.addWidget(self.label6)
        self.label7 = QLabel(self.widget)
        self.verticalLayout_2.addWidget(self.label7)

        colors = [child.text for child in root] if root else ['#808080', '#90ccff', '#ffffff', '#a0a0a0',
                                                              '#ffffff', '#000000', '#000000']

        self.label1.setStyleSheet(f"background-color: {colors[0]}")
        self.label2.setStyleSheet(f"background-color: {colors[1]}")
        self.label3.setStyleSheet(f"background-color: {colors[2]}")
        self.label4.setStyleSheet(f"background-color: {colors[3]}")
        self.label5.setStyleSheet(f"background-color: {colors[4]}")
        self.label6.setStyleSheet(f"background-color: {colors[5]}")
        self.label7.setStyleSheet(f"background-color: {colors[6]}")

        self.toolButton_1.clicked.connect(lambda: self.color_picker(self.label1))
        self.toolButton_2.clicked.connect(lambda: self.color_picker(self.label2))
        self.toolButton_3.clicked.connect(lambda: self.color_picker(self.label3))
        self.toolButton_4.clicked.connect(lambda: self.color_picker(self.label4))
        self.toolButton_5.clicked.connect(lambda: self.color_picker(self.label5))
        self.toolButton_6.clicked.connect(lambda: self.color_picker(self.label6))
        self.toolButton_7.clicked.connect(lambda: self.color_picker(self.label7))

        self.saveButton.clicked.connect(self.save_theme)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Theme Creator"))
        self.saveButton.setText(_translate("MainWindow", translate.save_theme))
        self.toolButton_1.setText(_translate("MainWindow", translate.primary_color))
        self.toolButton_2.setText(_translate("MainWindow", translate.primary_light))
        self.toolButton_3.setText(_translate("MainWindow", translate.second_color))
        self.toolButton_4.setText(_translate("MainWindow", translate.second_light))
        self.toolButton_5.setText(_translate("MainWindow", translate.second_dark))
        self.toolButton_6.setText(_translate("MainWindow", translate.font_color_1))
        self.toolButton_7.setText(_translate("MainWindow", translate.font_color_2))

    @staticmethod
    def color_picker(element):
        color = QColorDialog.getColor()
        element.setStyleSheet(f"background-color: {color.name()}")

    def save_theme(self):
        style_name, ok = QInputDialog.getText(self, translate.save_theme, translate.enter_theme_name)

        if ok and style_name:
            theme_xml = f'./data/themes/{style_name.lower().replace(" ", "_")}.xml'

            with open(theme_xml, 'w') as file:
                file.write('<!--?xml version="1.0" encoding="UTF-8"?-->\n')
                file.write('<resources>\n')
                labels = [self.label1, self.label2, self.label3, self.label4,
                          self.label5, self.label6, self.label7]
                names = ["primaryColor", "primaryLightColor", "secondaryColor", "secondaryLightColor",
                         "secondaryDarkColor", "primaryTextColor", "secondaryTextColor"]

                for i, label in enumerate(labels):
                    color = label.palette().color(label.backgroundRole())
                    file.write(f'  <color name="{names[i]}">{color.name()}</color>\n')

                file.write('</resources>\n')
