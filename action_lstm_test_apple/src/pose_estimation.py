# 카툰 필터 카메라

import sys
import math
import cv2
import numpy as np
import pandas as pd
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
from IPython.display import HTML


# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose

# Setting up the Pose function.
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils 

col_name_ls = []
for i in range(11, 17):
    print(mp_pose.PoseLandmark(i).name + "_x")
    col_name_ls.append(mp_pose.PoseLandmark(i).name + "_x")
    col_name_ls.append(mp_pose.PoseLandmark(i).name + "_y")
    col_name_ls.append("label")
    # col_name_ls.append(mp_pose.PoseLandmark(i).name + "_z")

data_dict = dict.fromkeys(col_name_ls)
for key in data_dict.keys():
    data_dict[key] = []
print(col_name_ls)


def detectPose(image, pose, display=True):
    # Create a copy of the input image.
    output_image = image.copy()
    
    # Convert the image from BGR into RGB format.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Perform the Pose Detection.
    results = pose.process(imageRGB)
    
    # Retrieve the height and width of the input image.
    height, width, _ = image.shape
    
    # Initialize a list to store the detected landmarks.
    landmarks = []
    
    # Check if any landmarks are detected.
    if results.pose_landmarks:
    
        # Draw Pose landmarks on the output image.
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)
        
        # Iterate over the detected landmarks.
        for landmark in results.pose_landmarks.landmark:
            
            # Append the landmark into the list.
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))
    
    
    return output_image, landmarks





cap = cv2.VideoCapture('../data/running.webm')

if not cap.isOpened():
    print('video open failed!')
    sys.exit()

cam_mode = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    mp_drawing.draw_landmarks(image=frame, landmark_list=results.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)

    if key == 27:
        break
    elif key == 49:
        for i in range(11, 17):
            data_dict[mp_pose.PoseLandmark(i).name + "_x"].append(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x)
            data_dict[mp_pose.PoseLandmark(i).name + "_y"].append(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y)
        data_dict['label'].append("Right_Up")

    elif key == 50:
        for i in range(11, 17):
            data_dict[mp_pose.PoseLandmark(i).name + "_x"].append(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x)
            data_dict[mp_pose.PoseLandmark(i).name + "_y"].append(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y)
        data_dict['label'].append("Left_Up")

    elif key == 51:
        for i in range(11, 17):
            data_dict[mp_pose.PoseLandmark(i).name + "_x"].append(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x)
            data_dict[mp_pose.PoseLandmark(i).name + "_y"].append(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y)
        data_dict['label'].append("Both_Up")

    elif key == 52:
        for i in range(11, 17):
            data_dict[mp_pose.PoseLandmark(i).name + "_x"].append(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x)
            data_dict[mp_pose.PoseLandmark(i).name + "_y"].append(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y)
        data_dict['label'].append("Both_Down")
    
train_df = pd.DataFrame.from_dict(data_dict)
train_df.to_csv("train_data.csv", index = False)

cap.release()
cv2.destroyAllWindows()