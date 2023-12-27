import roslibpy
import base64
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import time

class ImageReceiver(QThread):
    update = pyqtSignal(np.ndarray)

    def __init__(self, host='localhost', port=9090, sec=0, parent=None):
    # def __init__(self):
        super().__init__()
        self.running = False

        self.client = roslibpy.Ros(host=host, port=port)
        self.client.run()
        
        self.listener = roslibpy.Topic(self.client, '/ImgNData', 'auto_store_package_msgs/msg/ImgNData')
        # while self.client.is_connected:
        #     self.listener.subscribe(self.receive)
        
        self.before_time = time.time()
        

    def receive(self, msg):
        decode = base64.b64decode(msg['img_data'])
        img_buf = np.frombuffer(decode, dtype=np.uint8)
        img = np.reshape(img_buf, (msg['img_height'], msg['img_width'], msg['img_channel']))
        self.update.emit(img)
        # cv2.imshow(img)
        # print(time.time() - self.before_time)
        # self.before_time = time.time()
        
        
    def run(self):
        while self.client.is_connected and self.running:
            self.listener.subscribe(self.receive)

    def stop(self):
        self.running = False
        self.listener.unsubscribe()
        self.client.terminate()