from ultralytics import YOLO
import supervision as sv
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader
import mediapipe as mp
import numpy as np
import os
import random
from torch.utils.data import random_split
import matplotlib.pyplot as plt
from IPython.display import clear_output
import gc
import time
from tqdm import tqdm
from torch.cuda import memory_allocated, empty_cache
import cv2
import json

mp_pose = mp.solutions.pose
length = 50
interval = 1

attention_dot = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
draw_line = [[11, 12], [11, 23], [12, 24], [23, 24],
             [11, 13], [13, 15], [15, 17], [17, 19], [15, 21],
             [12, 14], [14, 16], [16, 18], [18, 20], [16, 22]]

class MyDataset(Dataset):
    def __init__(self, seq_list):
        self.X = []
        self.y = []
        for dic in seq_list:
            self.y.append(dic['key'])
            self.X.append(dic['value'])
        
    def __getitem__(self, index):
        data = self.X[index]
        label = self.y[index]
        return torch.Tensor(np.array(data)), torch.tensor(np.array(int(label)))
    
    def __len__(self):
        return len(self.X)



class skeleton_LSTM(nn.Module):
    def __init__(self, input_dim):
        super(skeleton_LSTM, self).__init__()
        self.lstm1 = nn.LSTM(input_size=input_dim, hidden_size=128, num_layers=1, batch_first=True)
        self.lstm2 = nn.LSTM(input_size=128, hidden_size=256, num_layers=1, batch_first=True)
        self.lstm3 = nn.LSTM(input_size=256, hidden_size=512, num_layers=1, batch_first=True)
        self.dropout1 = nn.Dropout(0.1)
        self.lstm4 = nn.LSTM(input_size=512, hidden_size=256, num_layers=1, batch_first=True)
        self.lstm5 = nn.LSTM(input_size=256, hidden_size=128, num_layers=1, batch_first=True)
        self.lstm6 = nn.LSTM(input_size=128, hidden_size=64, num_layers=1, batch_first=True)
        self.dropout2 = nn.Dropout(0.1)
        self.lstm7 = nn.LSTM(input_size=64, hidden_size=32, num_layers=1, batch_first=True)
        self.fc = nn.Linear(32, 4)

    def forward(self, x):
        x, _ = self.lstm1(x)
        x, _ = self.lstm2(x)
        x, _ = self.lstm3(x)
        x = self.dropout1(x)
        x, _ = self.lstm4(x)
        x, _ = self.lstm5(x)
        x, _ = self.lstm6(x)
        x = self.dropout2(x)
        x, _ = self.lstm7(x)
        x = self.fc(x[:, -1, :])
        
        return x
    
    
def get_hand_centers(results):
    # img = img_list[0]
    # pose = mp_pose.Pose(static_image_mode=True, model_complexity=1,
    #                     enable_segmentation = False, min_detection_confidence=0.3)

    # results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    rh_x_sum, rh_y_sum, lh_x_sum, lh_y_sum = 0, 0, 0, 0

    hand_centers = []

    for k in range(15, 23):
        if k == 15 or k == 17 or k == 19 or k == 21:
        # if k == 15:
            lh_x_sum += results.pose_landmarks.landmark[k].x
            lh_y_sum += results.pose_landmarks.landmark[k].y
        
        
        elif k == 16 or k == 18 or k == 20 or k == 22:
        # elif k == 16:
            rh_x_sum += results.pose_landmarks.landmark[k].x
            rh_y_sum += results.pose_landmarks.landmark[k].y
            
    lh_x_avg, lh_y_avg = lh_x_sum/4, lh_y_sum/4
    rh_x_avg, rh_y_avg = rh_x_sum/4, rh_y_sum/4     
        
    hand_centers.append([lh_x_avg, lh_y_avg])
    hand_centers.append([rh_x_avg, rh_y_avg])
    
    # print(hand_centers)
    return hand_centers

# 두 점 사이의 유클리디언 거리를 계산하는 함수
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def main():
    if torch.cuda.is_available() == True:
        device = 'cuda:0'
        print("GPU is available")
    else:
        device = 'cpu'
        print('GPU is unavailable')   
    
    net = skeleton_LSTM(32).to(device)
    
    net = torch.load('../checkpoint/action_pt/best_action.pt')
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1)

    model = YOLO('../checkpoint/yolo_pt/best.pt')
    
    net.eval()
    out_img_list = []
    dataset = []
    status = ''
    action = 0
    fruit_type = 5
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=1,
                        enable_segmentation = False, min_detection_confidence=0.3)
    
    xy_list_list = []
    # file_path = '../log/test5.json'
    seq = {}
    seq_index = 0
    
    
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return
    while True:
        ret, img = cap.read()
        if ret:
            results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            if not results.pose_landmarks: continue
            test_dict = {}
            xy_list = []
            idx = 0
            person = 0
            
            fruit_quantity = 0
            draw_line_dic = {}

            yolo_result = model(img, agnostic_nms=True)[0]
            hand_centers = get_hand_centers(results)
            
            detections = sv.Detections.from_yolov8(yolo_result)
            
            if 3 in detections.class_id:
                person = 1
                
            labels = [f"{model.model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]
            
            object_centers = []
            class_ids = []
            
            # if len(detections.xyxy) == 0:
            #     detected_obj = [0.0, 0.0, 0.0, 0.0]
            # else:
            #     detected_obj = list(detections.xyxy[0] / 640)
            
            for i in range(len(detections.xyxy)):
                x_center = ((detections.xyxy[i][0] + detections.xyxy[i][2]) / 2) / 640
                y_center = ((detections.xyxy[i][1] + detections.xyxy[i][3]) / 2) / 640
                object_centers.append((x_center, y_center))
                class_ids.append(detections.class_id[i])
            
            min_distance = 100000
            holding_object = ''
            dist_list = []
            
            # 유클리디언 거리 계산 및 최소 거리와 해당 물체 이름 출력
            for i in range(len(detections.xyxy)):    
                
                # Holding left hand
                if hand_centers[0][1] <= 0.5 and object_centers[i][1] <= 0.8 and (class_ids[i] not in [3, 4]):
                    distance = calculate_distance(object_centers[i], hand_centers[0])        
                    if distance < min_distance:
                        min_distance = distance
                        fruit_type = class_ids[i]
                        holding_object = model.model.names[class_ids[i]]
                        fruit_quantity = 1
                        
                # Holding right hand
                if hand_centers[1][1] <= 0.5 and object_centers[i][1] <= 0.8 and (class_ids[i] not in [3, 4]):
                    distance = calculate_distance(object_centers[i], hand_centers[1])        
                    if distance < min_distance:
                        min_distance = distance
                        fruit_type = class_ids[i]
                        holding_object = model.model.names[class_ids[i]]
                        fruit_quantity = 1
                
                # if hand_centers[0][1] <= 0.5 and object_centers[i][1] <= 0.8 and class_ids[i] not in [3, 4]:
                #         holding_object = model.model.names[class_ids[i]]
                
                
                # if hand_centers[1][1] <= 0.5 and object_centers[i][1] <= 0.8 and class_ids[i] not in [3, 4]:
                #         holding_object = model.model.names[class_ids[i]]
        
            min_distance = round(min_distance, 3)
            for x_and_y in results.pose_landmarks.landmark:
                if idx in attention_dot:
                    xy_list.append(x_and_y.x)
                    xy_list.append(x_and_y.y)
                    x, y = int(x_and_y.x * 640), int(x_and_y.y * 640)
                    draw_line_dic[idx] = [x, y]
                idx += 1
            
            if len(detections.xyxy) == 0:
                detected_obj = [0.0, 0.0, 0.0, 0.0]
            else:
                detected_obj = list(detections.xyxy[0] / 640)
            
            xy_list += detected_obj
            xy_list_list.append(xy_list)
            
            for line in draw_line:
                x1, y1 = draw_line_dic[line[0]][0], draw_line_dic[line[0]][1]
                x2, y2 = draw_line_dic[line[1]][0], draw_line_dic[line[1]][1]
                img = cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 4)

            img = box_annotator.annotate(
                            scene=img, 
                            detections=detections, 
                            labels=labels
                        )
            if len(xy_list_list) == length:
                dataset = []
                dataset.append({'key' : 0, 'value' : xy_list_list})
                dataset = MyDataset(dataset)
                dataset = DataLoader(dataset)
                xy_list_list = []
                for data, label in dataset:
                    data = data.to(device)
                    with torch.no_grad():
                        result = net(data)
                        _, output = torch.max(result, 1)
                        if output.item() == 0:
                            # status = f'Nothing {holding_object}, min_dist: {min_distance}'
                            status = 'Nothing' 
                            fruit_type = 5
                            action = 0

                        elif output.item() == 1:  
                            status = 'Picking_up'
                            fruit_type = 5
                            action = 1
                            
                        elif output.item() == 2:
                            status = 'Putting_down'
                            fruit_type = 5
                            action = 2
                        elif output.item() == 3:
                            # if holding_object != '':
                            #     # status = f'Holding {holding_object}, min_dist: {min_distance}'
                            #     status = f'Holding {holding_object}'
                            # else: 
                            #     status = 'Holding'
                            
                            status = 'Holding ' + holding_object 
                            action = 3

            # 보정 완료: person, action, fruit_type, fruit_quantity
            test_dict['person'] = int(person)
            test_dict['action'] = int(action)
            test_dict['fruit_type'] = int(fruit_type)
            test_dict['fruit_quantity'] = int(fruit_quantity)
            # print(test_dict)
            
            # cv2.putText(img, status, (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 2)
            cv2.putText(img, f'{status}', (0, 25), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 0), 1)
            # out_img_list.append(img)
            seq[seq_index] = test_dict
            seq_index += 1
            
            cv2.imshow('camera', img)
            
        key = cv2.waitKey(1)
        if key == 27:
            break  
    
    with open('../log/action_5_log.json', 'w') as f:
        json.dump(seq, f, ensure_ascii=False, indent=4)            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()