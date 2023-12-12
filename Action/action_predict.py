import torch
import mediapipe as mp
import numpy as np
from Action.models import action_lstm

def main():
    
    
    if torch.cuda.is_available() == True:
        device = 'cuda:0'
        print("GPU is available")
    else:
        device = 'cpu'
        print('GPU is unavailable')  



# prediction 실행문
def prediction():
    input_size = 28
    hidden_size = 128
    num_layers = 2
    num_class = 4
    net = action_lstm.ActionLSTM(input_size, hidden_size, num_layers, num_class)
    net = torch.load('./model_saved/ActionLSTM/best_action.pt')

    net.eval()
    out_img_list = []
    dataset = []
    status = 'None'
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False, min_detection_confidence = 0.3)
    box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=1, text_scale=0.5)

    # 모델 정의
    model = models.mobilenet_v3_small()
    num_classes = 3  # 여기에 모델을 학습할 때 사용한 클래스 수를 지정하세요.
    # model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.classifier[-1] = nn.Linear(model.classifier[-1].in_features, num_classes)

    # 저장된 가중치 로드
    weights_path = "mobilenetv3_weights_2.pt"  # 미리 저장한 가중치 파일의 경로
    model.load_state_dict(torch.load(weights_path))
    model.eval()

    # 입력 이미지 전처리
    transform = transforms.Compose([
        transforms.ToPILImage(),  # OpenCV 이미지를 PIL 이미지로 변환
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])


    # model = YOLO('best.pt')

    # attention_dot = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,                          # 25 key points
    #                  14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    # draw_line = [[0, 1], [1, 2], [2, 3], [3, 7], [0, 4], [4, 5], [5, 6], [6, 8], [9, 10],   # face
    #              [11, 12], [11, 23], [12, 24], [23, 24],                                    # body
    #              [11, 13], [13, 15], [15, 17], [17, 19], [15, 21],                          # right arm
    #              [12, 14], [14, 16], [16, 18], [18, 20], [16, 22]]                          # left arm

    attention_dot = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    draw_line = [[11, 12], [11, 23], [12, 24], [23, 24],
                [11, 13], [13, 15], [15, 17], [17, 19], [15, 21],
                [12, 14], [14, 16], [16, 18], [18, 20], [16, 22]]

    print("시퀀스 데이터 분석 중...")

    input_list = []
    for img in tqdm(img_list):
        width, height = img.shape[1], img.shape[0]
        scale_vector = np.array([width, height, width, height, 4.0])
        
        results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks: continue
        xy_list = []
        idx = 0
        draw_line_dic = {}
        
        # detected_idx = 0
        # yolo_result = model(img, agnostic_nms=True)[0]
        # detections = sv.Detections.from_yolov8(yolo_result)

        # labels = [f"{model.model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]
        
        for x_and_y in results.pose_landmarks.landmark:
            if idx in attention_dot:
                xy_list.append(x_and_y.x)
                xy_list.append(x_and_y.y)
                x, y = int(x_and_y.x * width), int(x_and_y.y * height)
                draw_line_dic[idx] = [x, y]
            idx += 1
        
        # yolo_result = model(img, agnostic_nms=True)[0]
        # detections = sv.Detections.from_yolov8(yolo_result)
        # labels = [f"{model.model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]
        
        # yolo_result = yolo_result.boxes.data.to('cpu').numpy()
        # yolo_result = yolo_result[:, [0, 1, 2, 3, 5]]
        # detection_list = yolo_result / scale_vector                                                  # Scaling the outputs of YOLO to the range (0, 1)

        # num_detection = len(detection_list)
        # if num_detection < 22:                                                                                  # if the number of detected objeects is less than the 21
        #     detection_list = np.vstack((detection_list, np.zeros((22 - num_detection, 5))))                     # pad with a zero vectors.
        
        # detection_list = detection_list.reshape(-1).tolist()                                                    # convert to list type     
        
        # xy_list += detection_list

        input_list.append(xy_list)
        
        for line in draw_line:
            x1, y1 = draw_line_dic[line[0]][0], draw_line_dic[line[0]][1]
            x2, y2 = draw_line_dic[line[1]][0], draw_line_dic[line[1]][1]
            img = cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        # img = box_annotator.annotate(scene=img, detections=detections, labels=labels)
        
        product = ''
        if len(input_list) == length:
            dataset = []
            dataset.append({'key' : 0, 'value' : input_list})
            dataset = MyDataset(dataset)
            dataset = DataLoader(dataset)
            input_list = []
            for data, label in dataset:
                data = data.to(device)
                with torch.no_grad():
                    result = net(data)
                    _, act_out = torch.max(result, 1)
                    
                    # if obj_out.item() == 0:
                    #     object_label = 'none'
                    # elif obj_out.item() == 1:
                    #     object_label = 'banana'
                    # elif obj_out.item() == 2:
                    #     object_label = 'apple'
                    # else:
                    #     object_label = 'orange'
                    
                    if act_out.item() == 0:
                        action_text = 'nothing'
                        status = action_text
                    elif act_out.item() == 1:
                        action_text = 'picking_up'
                        status = action_text
                    elif act_out.item() == 2:
                        action_text = 'putting_down'
                        status = action_text
                    else:
                        action_text = 'holding'
                        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        input_tensor = transform(frame_rgb).unsqueeze(0)
                        # 모델에 입력 전달
                        with torch.no_grad():
                            outputs = model(input_tensor)

                        # 예측 결과 확인
                        _, predicted_class = torch.max(outputs, 1)
                        if predicted_class == 0:
                            object_label = 'apple'
                        elif predicted_class == 1:
                            object_label = 'banana'
                        else:
                            object_label = 'orange'
                        
                        # print(f"Predicted class: {predicted_class.item()}")
                        status = action_text + ' ' + object_label

                        
        
        cv2.putText(img, status, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        
        out_img_list.append(img)

    