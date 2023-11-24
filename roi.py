import os
import cv2
import numpy as np
from datetime import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Camera import Camera

# 미리 video 폴더 생성 안해두면 안됨
file_folder = os.path.dirname(os.path.abspath(__file__))
from_class = uic.loadUiType(os.path.join(os.path.dirname(file_folder) +\
                            "/camera.ui"))[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
    
        self.image = None
        self.img_modified = None
        self.pixmap = QPixmap()

        self.camera = Camera(self)
        self.camera.daemon = True
        self.isCameraOn = False
        self.video = None

        self.text = ""
        self.lineEdit.setText(self.text)

        self.btnCam.clicked.connect(self.clickCamera)
        self.camera.update.connect(self.updateCamera)
        self.btnCapture.clicked.connect(self.clickCapture)


    # Camera Events
    def clickCamera(self):
        if self.isCameraOn == False:
            self.btnCam.setText("Camera off")
            self.btnCam.setStyleSheet("background-color: red")
            self.isCameraOn = True
            self.btnCapture.setText("Capture")

            self.cameraStart()

        else:
            self.btnCam.setText('Camera on')
            self.btnCam.setStyleSheet("")

            self.isCannyPressed = False
            self.btnCanny.setStyleSheet("")

            self.isCameraOn = False
            self.btnCapture.setText("Save")

            self.cameraStop()

            self.btnRec.setText('Rec on')
            self.recordingStop()

    def cameraStart(self):
        self.camera.running = True
        self.camera.start()
        self.video = cv2.VideoCapture(-1)

    def cameraStop(self):
        self.camera.running = False
        if self.video != None:
            self.video.release()
        # self.label.clear()

    def updateCamera(self):
        retval, self.image = self.video.read()

        if retval:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.img_modified = self.image

            self.plotImg()

    def clickCapture(self):
        if type(self.image) != np.ndarray:
            self.resetCanny()
            self.resetHSV()
            self.resetRGB()

            retval, self.image = cv2.VideoCapture(-1).read() 
            if retval:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                self.img_modified = self.image
                self.plotImg()

            else:
                return



    #
    def plotImg(self):
        h, w, c = self.img_modified.shape

        qimage = QImage(self.img_modified.data, w, h, w*c, QImage.Format_RGB888)

        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height(),
                                        Qt.KeepAspectRatio)

        self.label.setPixmap(self.pixmap)
