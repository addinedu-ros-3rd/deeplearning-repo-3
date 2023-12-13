import roslibpy
import base64
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal


class ImageReceiver(QThread):
    update = pyqtSignal(np.ndarray)

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.running = True

        self.client = roslibpy.Ros(host='localhost', port=9090) 
        self.client.run()
        
        self.listener = roslibpy.Topic(self.client, '/ImgNData', 'auto_store_package_msgs/msg/ImgNData')

    def receive(self, msg):
        decode = base64.b64decode(msg['img_data'])
        img_buf = np.frombuffer(decode, dtype=np.uint8)
        img = np.reshape(img_buf, (msg['img_height'], msg['img_width'], msg['img_channel']))
        
        self.update.emit(img)
        
        
    def run(self):
        while self.client.is_connected:
            self.listener.subscribe(self.receive)

    def stop(self):
        self.running = False
        self.listener.unsubscribe()
        self.client.terminate()