import roslibpy
import cv2
import base64
import logging
import sys
import numpy as np

def receive(msg):
    # print(msg['img_data'])
    buf = base64.b64decode(msg['img_data'])
    # print(buf)
    img_arr = np.frombuffer(buf, dtype=np.uint8)
    img = np.reshape(img_arr, (msg['img_height'], msg['img_width'], msg['img_channel']))
    cv2.imshow('ros_img1', img)
    print("action_data : ", msg['action_data'])
    print("stand_data : ", msg['stand_data'])
    
def main():

    fmt = '%(asctime)s %(levelname)8s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)
    log = logging.getLogger(__name__)

    client = roslibpy.Ros(host='localhost', port=9090) 
    client.run()

    try:
        while client.is_connected:
            listener = roslibpy.Topic(client, '/ImgNData', 'auto_store_package_msgs/msg/ImgNData')
            listener.subscribe(receive)

            key = cv2.waitKey(10)
            if key == ord('q'):
                raise

    except Exception as e:
        print("An error occurred:", type(e).__name__, "–", e)
    finally:
        cv2.destroyAllWindows()
        client.terminate()
        sys.exit()

if __name__ == "__main__":
    main()