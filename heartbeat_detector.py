import sys
from function import (function)
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QGroupBox, QComboBox, QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import PyQt5.QtWidgets as qtwid
import numpy as np
import cv2

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.camrea_id = 0

    def run(self):
        # capture from web cam
        cap = function.get_camera(self.camrea_id)
        while self._run_flag:
            pre_process_frame = function.get_camera_frame(cap)
            processed_frame = function.process_monitor_frame(pre_process_frame)
            self.change_pixmap_signal.emit(processed_frame)
        # shut down capture system
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


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

        self.disply_width = 256
        self.display_height = 256
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

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

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())