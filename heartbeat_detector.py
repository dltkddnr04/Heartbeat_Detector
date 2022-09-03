import sys
from function import (function)
from PyQt5.QtWidgets import (QApplication, QGridLayout, QWidget, QGroupBox, QComboBox, QLabel)
from PyQt5.QtGui import (QPixmap, QColor)
import PyQt5.QtWidgets as qtwid

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.camera_display(), 0, 0)
        grid.addWidget(self.program_settings(), 0, 1)
        self.setLayout(grid)
        self.resize(600, 300)
        self.setWindowTitle('Can you feel my heartbeat?')
        self.show()

    def camera_display(self):
        groupbox = QGroupBox()
        grid = QGridLayout()

        # show webcam's screen
        self.image_label = QLabel(self)
        grey = QPixmap(256, 256)
        grey.fill(QColor('darkGray'))
        self.image_label.setPixmap(grey)

        grid.addWidget(self.image_label, 0, 0)

        groupbox.setLayout(grid)
        return groupbox

    def program_settings(self):
        groupbox = QGroupBox('설정')
        grid = QGridLayout()

        self.select_camera = QComboBox(self)
        self.select_camera.addItem('1')
        self.select_camera.addItem('2')
        self.select_camera.addItem('3')
        self.select_camera.addItem('4')

        self.passthrough_start = qtwid.QPushButton("웹캠 패스스루 시작",self)
        self.info_graphic_start = qtwid.QPushButton("그래픽 출력 시작",self)

        grid.addWidget(self.select_camera, 0, 0, 1, 0)
        grid.addWidget(self.passthrough_start, 1, 0)
        grid.addWidget(self.info_graphic_start, 2, 0)
        

        groupbox.setLayout(grid)
        return groupbox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())