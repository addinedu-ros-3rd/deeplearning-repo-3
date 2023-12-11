import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cv2, imutils
from PyQt5.QtCore import QThread, pyqtSignal
import time
import datetime

from_class = uic.loadUiType("opencv.ui")[0]


class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

    def run(self):
        count = 0
        while self.running == True:
            self.update.emit()
            time.sleep(0.05)

    def stop(self):
        self.running == False


class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.isCameraOn = False
        self.isRecStart = False
        self.btnRecord.hide()
        self.btnCapture.hide()

        self.pixmap = QPixmap()
        self.image = None

        self.camera = Camera(self)
        self.camera.deamon = True

        self.record =Camera(self)
        self.record.deamon = True 

        self.play = Camera(self)
        self.play.daemon = True

        self.btnOpen.clicked.connect(self.openFile)
        self.btnCamera.clicked.connect(self.clickCamera)
        self.camera.update.connect(self.updateCamera)
        self.btnRecord.clicked.connect(self.clickRecord)
        self.record.update.connect(self.updateRecording)
        self.btnCapture.clicked.connect(self.capture)
        self.btnOpenVideo.clicked.connect(self.openVideo)

        self.count = 0

    
    def capture(self):
        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.now + ".png"

        cv2.imwrite(filename, cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
    
    def updateRecording(self):
        self.writer.write(cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))
    
    def clickRecord(self):
        if self.isRecStart == False:
            self.btnRecord.setText("Rec Stop")
            self.isRecStart = True

            self.recordingStart()
            
        else:
            self.btnRecord.setText("Rec Start")
            self.isRecStart = False

            self.recordingStop()

    def recordingStart(self):
        self.record.running = True
        self.record.start()

        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.now + ".avi"
        self.fourcc = cv2.VideoWriter_fourcc(*'VP80')

        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (w, h))

    def recordingStop(self):
        self.record.running = False

        if self.isRecStart == True:
            self.writer.release()
    
    def clickCamera(self):
        if self.isCameraOn == False:
            self.isCameraOn = True
            self.btnCamera.setText("Camera Off")
            self.btnRecord.show()
            self.btnCapture.show()
            
            self.cameraStart()
        
        else:
            self.isCameraOn = False
            self.btnCamera.setText("Camera On")
            self.btnRecord.hide()
            self.btnCapture.hide()
            
            self.cameraStop()
            self.recordingStop()
    
    def cameraStart(self):
        self.camera.running = True
        self.camera.start()
        self.video = cv2.VideoCapture(0)

    def cameraStop(self):
        self.camera.running = False
        self.video.release()
    
    def updateCamera(self):
        retval, image = self.video.read()
        if retval:
            self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            h, w, c = self.image.shape
            qimage = QImage(self.image.data, w, h, w*c, QImage.Format_RGB888)

            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())

            self.label.setPixmap(self.pixmap)
    
    def openVideo(self):
        file = QFileDialog.getOpenFileName(filter="Video (*.*)")

        cap = cv2.VideoCapture(file[0])

        while(cap.isOpened()):
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            h, w, c = frame.shape
            qimage = QImage(frame.data, w, h, w*3, QImage.Format_RGB888)

            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())

            self.label.setPixmap(self.pixmap)
            
        cap.release()




        
    
    
    def openFile(self):
        file = QFileDialog.getOpenFileName(filter="Image (*.*)")

        image = cv2.imread(file[0])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        h, w, c = image.shape
        qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)

        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())

        self.label.setPixmap(self.pixmap)



        

    
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())