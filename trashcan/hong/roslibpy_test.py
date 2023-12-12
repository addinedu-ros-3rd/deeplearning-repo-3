# bridge 이용 : terminal에서
# ros2 launch rosbridge_server rosbridge_websocket_launch.xml
# ros2 launch rosbridge_server rosbridge_websocket_launch.xml port:=9091
# source ros_ws/install/local_setup.bash
# ros2 run auto_store_package auto_store_subscriber
# 진행 후 실행

# https://velog.io/@choonsik_mom/ROS2-python-%EA%B8%B0%EC%B4%88-%EC%97%AC%EB%9F%AC-topic%EC%9D%84-%EA%B5%AC%EB%8F%85%ED%95%98%EC%97%AC-csv-%ED%8C%8C%EC%9D%BC-%EB%A7%8C%EB%93%A4%EA%B8%B0


import roslibpy
import cv2
import base64
import logging
import time
from cv_bridge import CvBridge
import sys


def main():
    bridge = CvBridge() 

    fmt = '%(asctime)s %(levelname)8s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)
    log = logging.getLogger(__name__)

    client = roslibpy.Ros(host='localhost', port=9090) 
    client.run()

    # publisher = roslibpy.Topic(client, '/camera/image/compressed', 'sensor_msgs/CompressedImage')
    publisher = roslibpy.Topic(client, '/camera1/image/compressed', 'sensor_msgs/CompressedImage')
    publisher.advertise()


    cam = cv2.VideoCapture(1)

    try:
        while client.is_connected:
            ret, frame = cam.read()

            if not(frame is None):
                cv2.imshow("frame1", frame)
                resized = cv2.resize(frame, (320, 320))
                _, buffer = cv2.imencode('.jpeg', resized)
                encoded = base64.b64encode(buffer).decode('ascii')
                publisher.publish(dict(format='jpeg', data=encoded))
            key = cv2.waitKey(100)
            if key == ord('q'):
                raise
            # time.sleep(0.1)

    except Exception as e:
        print("An error occurred:", type(e).__name__, "–", e)
    finally:
        cv2.destroyAllWindows()
        cam.release()
        publisher.unadvertise()
        client.terminate()
        sys.exit()

if __name__ == "__main__":
    main()