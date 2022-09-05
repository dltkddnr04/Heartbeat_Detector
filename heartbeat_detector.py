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
        self.setWindowTitle('Heartbeat Detector')
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

        grid.addWidget(self.camera_settings(), 0, 0)
        grid.addWidget(self.status_widget(), 1, 0)
        grid.addWidget(self.passthrough_settings(), 2, 0)
        
        groupbox.setLayout(grid)
        return groupbox

    def camera_settings(self):
        groupbox = QGroupBox('카메라 선택')
        grid = QGridLayout()

        self.select_camera = QComboBox(self)
        self.select_camera.addItem('1')
        self.select_camera.addItem('2')
        self.select_camera.addItem('3')
        self.select_camera.addItem('4')

        grid.addWidget(self.select_camera, 1, 0)
        groupbox.setLayout(grid)
        return groupbox

    def status_widget(self):
        groupbox = QGroupBox('상태')
        grid = QGridLayout()

        self.tracking_status = QLabel('트래킹 상태 {}'.format('🔴'))
        self.heartbeat_rate = QLabel('심박수 {}bpm'.format(0))

        grid.addWidget(self.tracking_status, 0, 0)
        grid.addWidget(self.heartbeat_rate, 1, 0)

        groupbox.setLayout(grid)
        return groupbox

    def passthrough_settings(self):
        groupbox = QGroupBox('패스스루')
        grid = QGridLayout()

        self.passthrough_button = qtwid.QPushButton("웹캠 출력 시작",self)
        self.info_graphic_button = qtwid.QPushButton("그래픽 출력 시작",self)

        grid.addWidget(self.passthrough_button, 1, 0)
        grid.addWidget(self.info_graphic_button, 2, 0)

        self.passthrough_button.clicked.connect(self.passthrough_start)
        self.info_graphic_button.clicked.connect(self.info_graphic_start)

        groupbox.setLayout(grid)
        return groupbox

    def passthrough_start(self):
        self.passthrough_button.setText("웹캠 출력 중지")
        self.passthrough_button.clicked.connect(self.passthrough_stop)
        return

    def info_graphic_start(self):
        self.info_graphic_button.setText("그래픽 출력 중지")
        self.info_graphic_button.clicked.connect(self.info_graphic_stop)
        return

    def passthrough_stop(self):
        self.passthrough_button.setText("웹캠 출력 시작")
        self.passthrough_button.clicked.connect(self.passthrough_start)
        return

    def info_graphic_stop(self):
        self.info_graphic_button.setText("그래픽 출력 시작")
        self.info_graphic_button.clicked.connect(self.info_graphic_start)
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())