# bridge 이용 : terminal에서
# ros2 launch rosbridge_server rosbridge_websocket_launch.xml
# ros2 launch rosbridge_server rosbridge_websocket_launch.xml port:=9091
# source ros_ws/install/local_setup.bash
# ros2 run auto_store_package auto_store_subscriber
# 진행 후 실행


import roslibpy
import cv2
import base64
import logging
import sys
import json

def main():

    fmt = '%(asctime)s %(levelname)8s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)
    log = logging.getLogger(__name__)

    client = roslibpy.Ros(host='localhost', port=9090) 
    client.run()

    publisher = roslibpy.Topic(client, '/ImgNData', 'auto_store_package_msgs/msg/ImgNData')
    publisher.advertise()


    cam = cv2.VideoCapture(1)
    resized_height, resized_width = 320, 320

    try:
        while client.is_connected:
            ret, frame = cam.read()

            if not(frame is None):
                cv2.imshow("frame1", frame)
                resized = cv2.resize(frame, (resized_height, resized_width))
                encoded = base64.b64encode(resized).decode('ascii')

                stand_data = {
                    "1": {
                        "Banana": 0,
                        "Apple": 0,
                        "Orange": 0},
                    "2": {
                        "Banana": 0,
                        "Apple": 0,
                        "Orange": 0},
                    "3": {
                        "Banana": 0,
                        "Apple": 0,
                        "Orange": 0}
                }
                action_data = {
                    "person": 0,
                    "action": 0,
                    "fruit_type": 5,
                    "fruit_quantity": 0
                }

                publisher.publish(roslibpy.Message({'img_data': encoded,
                                                    'img_height': resized.shape[0],
                                                    'img_width': resized.shape[1],
                                                    'img_channel': resized.shape[2],
                                                    'action_data': json.dumps(action_data),
                                                    'stand_data': json.dumps(stand_data)}))

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