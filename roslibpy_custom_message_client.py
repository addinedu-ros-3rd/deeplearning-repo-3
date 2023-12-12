import roslibpy
import cv2
import base64
import logging
import sys
import numpy as np

def receive(msg):
    # print(msg['img_data'])
    decode = base64.b64decode(msg['img_data'])
    img_buf = np.frombuffer(decode, dtype=np.uint8)
    img = np.reshape(img_buf, (msg['img_height'], msg['img_width'], msg['img_channel']))
    
    cv2.imshow('ros_img1', img)
    print("action_data : ", msg['action_data'])
    print("stand_data : ", msg['stand_data'])

    key = cv2.waitKey(10)
    if key == ord('q'):
        raise
    
def main():

    fmt = '%(asctime)s %(levelname)8s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)
    log = logging.getLogger(__name__)

    client = roslibpy.Ros(host='localhost', port=9090) 
    client.run()
    
    listener = roslibpy.Topic(client, '/ImgNData', 'auto_store_package_msgs/msg/ImgNData')

    try:
        while client.is_connected:
            listener.subscribe(receive)

    except Exception as e:
        print("An error occurred:", type(e).__name__, "–", e)
    finally:
        cv2.destroyAllWindows()
        listener.unsubscribe()
        client.terminate()
        sys.exit()

if __name__ == "__main__":
    main()