# bridge 이용 : terminal에서
# ros2 launch rosbridge_server rosbridge_websocket_launch.xml
# ros2 launch rosbridge_server rosbridge_websocket_launch.xml port:=9091
# source ros_ws/install/local_setup.bash
# ros2 run auto_store_package auto_store_subscriber
# 진행 후 실행


import roslibpy
import base64
import json
import cv2
import torch
import os
import copy

from torchvision import transforms, models
import torch.nn as nn
import mediapipe as mp
from ultralytics import YOLO

from Action.action_cam import ActionCam
from Action.models.action_lstm import ActionLSTM
from Stand.utils.Detector import Detector


def save_video(cam_type, video_name, img_list, frame_width, frame_height):
    if not os.path.exists("./output_video"):
        os.makedirs("./output_video")

    if cam_type == 'action':
        filename = './output_video/action_'+ video_name +'.avi'
    else:
        filename = './output_video/stand_'+ video_name +'.avi'
    
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    fps = 30
    frameSize = (frame_width, frame_height)
    isColor = True
    
    out = cv2.VideoWriter(filename, fourcc, fps, frameSize, isColor)
    for out_ in img_list:
        out.write(out_)
    
    out.release()


def main(video_path = './test_sample/test_data_0.avi'):
    client = roslibpy.Ros(host='localhost', port=9090) 
    client.run()

    publisher = roslibpy.Topic(client, '/ImgNData', 'auto_store_package_msgs/msg/ImgNData')
    publisher.advertise()

    cv2.destroyAllWindows()
    cap = cv2.VideoCapture(video_path)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    resized_height, resized_width = 320, 320
    
    # video_name = video_path.split('/')[-1]

    attention_dot = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    draw_line = [[11, 12], [11, 23], [12, 24], [23, 24],
                [11, 13], [13, 15], [15, 17], [17, 19], [15, 21],
                [12, 14], [14, 16], [16, 18], [18, 20], [16, 22]]

    length = 50    
    input_size = 28
    hidden_size = 128
    num_layers = 2
    action_num_class = 4

    if torch.cuda.is_available() == True:
        device = 'cuda:0'
        print("GPU is available")
    else:
        device = 'cpu'
        print('GPU is unavailable')

    # Pose Estimation : Mediapipe 
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False, min_detection_confidence = 0.3)

    # Action Recognition : LSTM
    lstm = ActionLSTM(input_size, hidden_size, num_layers, action_num_class, device)
    lstm = torch.load('./model_saved/ActionLSTM/best_action.pt')
    lstm.eval()

    # CNN : MobileNet-V3
    # mobilenet = models.mobilenet_v3_small()
    # num_classes = 3
    # mobilenet.classifier[-1] = nn.Linear(mobilenet.classifier[-1].in_features, num_classes)
    # weights_path = './model_saved/MobileNetV3/mobilenetv3_weights_2.pt'
    # mobilenet.load_state_dict(torch.load(weights_path))
    # mobilenet.eval()
    mobilenet = models.resnet18(pretrained=True)
    num_classes = 3
    mobilenet.fc = nn.Linear(mobilenet.fc.in_features, num_classes)
    weights_path = './model_saved/MobileNetV3/resnet18_weights.pt'
    mobilenet.load_state_dict(torch.load(weights_path))
    mobilenet.eval()

    yolo = YOLO('./model_saved/YOLO/yolo_best.pt')

    # 입력 이미지 전처리
    transform = transforms.Compose([
        transforms.ToPILImage(),        # OpenCV 이미지를 PIL 이미지로 변환
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    Action = ActionCam(attention_dot, draw_line, length, pose, lstm, mobilenet, yolo, transform, device)
    roi_txt = os.path.abspath("./Stand/save_roi.txt")
    detector = Detector(yolo, frame_width, frame_height, roi_txt)
    
    # action_out_img_list = []
    # stand_out_img_list = []
    action_output_frame = None
    if cap.isOpened():
        while True:
            ret, img = cap.read()

            # img = cv2.flip(img, 1)
            # img = cv2.flip(img, 0)

            if ret:
                # if cnt == interval:
                action_img = copy.deepcopy(img)
                stand_img = copy.deepcopy(img)

                action_output_frame, action_output_data = Action.predict(action_img)
                stand_output_frame, stand_output_data = detector.detect_fruit_in_box(stand_img)
                
                # ToDo : 출력문을 통신 보내는 코드로 바꾸기
                print("Action-Cam:", action_output_data)
                print("Stand-Cam:", stand_output_data)
                print()

                # # Output Frames 저장
                # action_out_img_list.append(action_output_frame)
                # stand_out_img_list.append(stand_output_frame)
                
                cv2.imshow("Action Cam", cv2.resize(action_output_frame, (int(frame_width * 0.6), int(frame_height * 0.6))))
                cv2.imshow("Stand Cam", cv2.resize(stand_output_frame, (int(frame_width * 0.6), int(frame_height * 0.6))))
                
                resized = cv2.resize(action_output_frame, (resized_height, resized_width))
                encoded = base64.b64encode(resized).decode('ascii')


                publisher.publish(roslibpy.Message({'img_data': encoded,
                                                    'img_height': resized.shape[0],
                                                    'img_width': resized.shape[1],
                                                    'img_channel': resized.shape[2],
                                                    'action_data': json.dumps(action_output_data),
                                                    'stand_data': json.dumps(stand_output_data)}))
                cv2.waitKey(1)
            
            else:
                break
    
    cap.release()
    cv2.destroyAllWindows()

    # save_video('action', video_name[:-4], action_out_img_list, frame_width, frame_height)
    # save_video('stand', video_name[:-4], stand_out_img_list, frame_width, frame_height)



if __name__ == "__main__":
    main()