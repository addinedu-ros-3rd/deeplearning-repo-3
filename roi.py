import os, sys
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
from_class = uic.loadUiType(os.path.join(file_folder +\
                            "/camera.ui"))[0]


class Polygon:
    def __init__(self, points):
        self.points = points



class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
        self.image = None
        self.img_modified = None
        self.pixmap = QPixmap()

        self.camera = Camera(self)
        self.camera.daemon = True
        self.isCameraOn = False

        self.polyList = []


        self.camera.update.connect(self.updateCamera)
        self.btnCapture.clicked.connect(self.clickCapture)

        self.label.mousePressEvent = self.getPixel
        self.pol = []

        self.cap = cv2.VideoCapture(1)
        print("Loading cam", end='')
        while not self.cap.isOpened():
            print(".")


    def addPolygon(self):
        w, h = self.label.width(), self.label.height()
        painter = QPainter(self.img_modified)

        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.VerPattern))

        points = [QPoint(w-50, h-50), QPoint(w+50, h-50),
                  QPoint(w+50, h+50), QPoint(w-50, h+50)]
        
        painter.drawPolygon(QPolygon(points))
        
        self.plotImg()
        self.polyList.append(Polygon)


    def getPixel(self, event):
        x = event.pos().x()
        y = event.pos().y()

        # self.pol.append(QPoint(int(x),int(y)))

        # print(x,y, self.pol)

        self.statusBar().showMessage("x: " + str(x) + ", y: " + str(y))


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

            self.isCameraOn = False
            self.btnCapture.setText("Save")

            self.cameraStop()

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
        retval, self.image = self.cap.read()
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())