
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from qt_material import apply_stylesheet
import configparser
import xml.etree.ElementTree as ET


setting = configparser.ConfigParser()
setting.read('./setting.ini')


class ThemeCreateWindow(QMainWindow):

    def __init__(self, style='dark_orange'):
        super(ThemeCreateWindow, self).__init__()
        self.window = uic.loadUi('./source/ui/theme_creator.ui', self)
        apply_stylesheet(self.window, theme=f'{style}.xml')
        root = ET.parse(f'./qt_material/themes/{style}.xml').getroot()
        colors = []

        for child in root:
            colors.append(child.text)

        self.window.label1.setStyleSheet(f"background-color: {colors[0]}")
        self.window.label2.setStyleSheet(f"background-color: {colors[1]}")
        self.window.label3.setStyleSheet(f"background-color: {colors[2]}")
        self.window.label4.setStyleSheet(f"background-color: {colors[3]}")
        self.window.label5.setStyleSheet(f"background-color: {colors[4]}")
        self.window.label6.setStyleSheet(f"background-color: {colors[5]}")
        self.window.label7.setStyleSheet(f"background-color: {colors[6]}")

        self.window.toolButton_1.clicked.connect(lambda: self.color_picker(self.window.label1))
        self.window.toolButton_2.clicked.connect(lambda: self.color_picker(self.window.label2))
        self.window.toolButton_3.clicked.connect(lambda: self.color_picker(self.window.label3))
        self.window.toolButton_4.clicked.connect(lambda: self.color_picker(self.window.label4))
        self.window.toolButton_5.clicked.connect(lambda: self.color_picker(self.window.label5))
        self.window.toolButton_6.clicked.connect(lambda: self.color_picker(self.window.label6))
        self.window.toolButton_7.clicked.connect(lambda: self.color_picker(self.window.label7))

        self.window.saveButton.clicked.connect(self.save_theme)

    @staticmethod
    def color_picker(element):
        color = QColorDialog.getColor()
        element.setStyleSheet(f"background-color: {color.name()}")

    def save_theme(self):
        style_name, ok = QInputDialog.getText(self, "Сохранить тему", "Введите название темы:")

        if ok and style_name:
            theme_xml = f'./qt_material/themes/{style_name}.xml'

            with open(theme_xml, 'w') as file:
                file.write('<!--?xml version="1.0" encoding="UTF-8"?-->\n')
                file.write('<resources>\n')
                labels = [self.window.label1, self.window.label2, self.window.label3, self.window.label4,
                          self.window.label5, self.window.label6, self.window.label7]
                names = ["primaryColor", "primaryLightColor", "secondaryColor", "secondaryLightColor",
                         "secondaryDarkColor", "primaryTextColor", "secondaryTextColor"]

                for i, label in enumerate(labels):
                    color = label.palette().color(label.backgroundRole())
                    file.write(f'  <color name="{names[i]}">{color.name()}</color>\n')

                file.write('</resources>\n')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ThemeCreateWindow()
    win.show()
    sys.exit(app.exec())
