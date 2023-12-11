import cv2
from ultralytics import YOLO
import supervision as sv
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
import mediapipe as mp
import numpy as np
import os
import random
import pickle
from torch.utils.data import random_split
import matplotlib.pyplot as plt
from IPython.display import clear_output
import gc
import time
from tqdm import tqdm
from torch.cuda import memory_allocated, empty_cache


class Trainer():
    def __init__(self, the_args):
        self.args = the_args
        self.set_cuda_device()
        self.set_dataset_variables()

    def set_cuda_device():
        if torch.cuda.is_available() == True:
            device = 'cuda:0'
            print("GPU is available")
        else:
            device = 'cpu'
            print('GPU is unavailable')
    
    def train(self):
        X_train_total, Y_train_total, X_valid_total, Y_valid_total = self.set_dataset()


    # Extract coordiates of key points and detected objects
    def show_skeleton(video_path , interval, attention_dot, draw_line, action, picking_ojb):
        input_list = []
        input_list_flip = []
        mp_pose = mp.solutions.pose
        # box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=1, text_scale=0.5)
        pose = mp_pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False, min_detection_confidence = 0.3)
        cv2.destroyAllWindows()
        
        cap = cv2.VideoCapture(video_path)
        if cap.isOpened():
            cnt = 0
            while True:
                ret, img = cap.read()
                if cnt == interval and ret == True:
                    cnt = 0
                    idx = 0
                    draw_line_dic = {}
                    xy_list = []
                    xy_list_flip = []
                    width, height = img.shape[1], img.shape[0]
                    scale_vector = np.array([width, height, width, height, 4.0])
                    
                    results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    
                    if not results.pose_landmarks: 
                        continue
                    
                    for x_and_y in results.pose_landmarks.landmark:
                        if idx in attention_dot:
                            xy_list.append(x_and_y.x)
                            xy_list.append(x_and_y.y)
                            xy_list_flip.append(1 - x_and_y.x)
                            xy_list_flip.append(x_and_y.y)
                            x, y = int(x_and_y.x * width), int(x_and_y.y * height)
                            draw_line_dic[idx] = [x, y]
                        idx += 1
                    
                    # yolo_result = model(img, agnostic_nms=True)[0]
                    # detections = sv.Detections.from_yolov8(yolo_result)
                    # labels = [f"{model.model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]
                    
                    # yolo_result = yolo_result.boxes.data.to('cpu').numpy()
                    # yolo_result = yolo_result[:, [0, 1, 2, 3, 5]]
                    # detection_list = yolo_result / scale_vector                                                  # Scaling the outputs of YOLO to the range (0, 1)
                    # detection_list_flip = flip(detection_list)
                    
                    # num_detection = len(detection_list)
                    # if num_detection < 22:                                                                                  # if the number of detected objeects is less than the 21
                    #     detection_list = np.vstack((detection_list, np.zeros((22 - num_detection, 5))))                     # pad with a zero vectors.
                    #     detection_list_flip = np.vstack((detection_list_flip, np.zeros((22 - num_detection, 5))))
                    
                    # detection_list = detection_list.reshape(-1).tolist()                                                    # convert to list type
                    # detection_list_flip = detection_list_flip.reshape(-1).tolist()     
                    
                    # xy_list += detection_list
                    # xy_list_flip += detection_list_flip

                    input_list.append(xy_list)
                    input_list_flip.append(xy_list_flip)
                    
                    for line in draw_line:
                        x1, y1 = draw_line_dic[line[0]][0], draw_line_dic[line[0]][1]
                        x2, y2 = draw_line_dic[line[1]][0], draw_line_dic[line[1]][1]
                        img = cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    # img = box_annotator.annotate(scene=img, detections=detections, labels=labels)
                    
                    if action == 0: 
                        action_text = 'nothing'
                    elif action == 1:
                        action_text = 'picking_up'
                    elif action == 2:
                        action_text = 'putting_down'
                    else: 
                        action_text = 'holding'

                    if picking_ojb == 0:
                        object_label = 'none'
                    elif picking_ojb == 1:
                        object_label = 'banana'
                    elif picking_ojb == 2:
                        object_label = 'apple'
                    else:
                        object_label = 'orange'
                    
                    status = action_text + ' ' + object_label
                    
                    cv2.putText(img, status, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                    cv2.imshow('Landmark Image', img)
                    cv2.waitKey(1)
                
                elif ret == False: break
                
                cnt += 1
        
        cap.release()
        cv2.destroyAllWindows()
        
        return input_list + input_list_flip
    

    def flip(original_array):
        # 0번째와 2번째 열의 값을 1에서 빼준 새로운 배열 생성
        modified_array = original_array.copy()  # 원본 배열을 변경하지 않기 위해 복사
        modified_array[:, [0, 2]] = 1 - modified_array[:, [0, 2]]

        return modified_array
    
