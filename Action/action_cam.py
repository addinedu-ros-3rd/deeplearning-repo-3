import numpy as np
import cv2
import torch
from torch.utils.data import Dataset, DataLoader
import supervision as sv


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
    

class ActionCam():
    def __init__(self, attention_dot, draw_line, length, pose, lstm_model, cnn_model, yolo, transform, device):
        self.attention_dot = attention_dot
        self.draw_line = draw_line
        self.length = length
        self.device = device

        self.pose = pose
        self.lstm_model = lstm_model
        self.cnn_model = cnn_model
        self.yolo = yolo

        self.transform = transform
        self.input_list = []
        self.status = None
        
        self.keys = ["person", "action", "fruit_type", "fruit_quantity"]
        self.values = [0, 0, 5, 0]
        self.output_data = dict(zip(self.keys, self.values))

        self.box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=1, text_scale=0.5)


    def predict(self, img):
        width, height = img.shape[1], img.shape[0]
        
        results = self.pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        yolo_result = self.yolo(img, agnostic_nms=True, verbose=False)[0]
        detections = sv.Detections.from_yolov8(yolo_result)
        
        if 3 in detections.class_id:
            self.output_data['person'] = 1
        else:
            self.output_data['person'] = 0
            
        labels = [f"{self.yolo.model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]

        if not results.pose_landmarks: 
            return img, self.output_data
        else:
            xy_list = []
            idx = 0
            draw_line_dic = {}
            
            for x_and_y in results.pose_landmarks.landmark:
                if idx in self.attention_dot:
                    xy_list.append(x_and_y.x)
                    xy_list.append(x_and_y.y)
                    x, y = int(x_and_y.x * width), int(x_and_y.y * height)
                    draw_line_dic[idx] = [x, y]
                idx += 1

            self.input_list.append(xy_list)
            
            for line in self.draw_line:
                x1, y1 = draw_line_dic[line[0]][0], draw_line_dic[line[0]][1]
                x2, y2 = draw_line_dic[line[1]][0], draw_line_dic[line[1]][1]
                img = cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

            if len(self.input_list) == self.length:
                dataset = []
                dataset.append({'key' : 0, 'value' : self.input_list})
                dataset = MyDataset(dataset)
                dataset = DataLoader(dataset)
                self.input_list = []
                self.output_data['fruit_type'] = 5
                for data, label in dataset:
                    data = data.to(self.device)
                    with torch.no_grad():
                        result = self.lstm_model(data)
                        _, act_out = torch.max(result, 1)
                        
                        if act_out.item() == 0:
                            action_text = 'nothing'
                            self.status = action_text

                        elif act_out.item() == 1:
                            action_text = 'picking_up'
                            self.status = action_text

                        elif act_out.item() == 2:
                            action_text = 'putting_down'
                            self.status = action_text                            

                        else:
                            action_text = 'holding'
                            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            input_tensor = self.transform(frame_rgb).unsqueeze(0)
                            
                            # CNN Model에 입력 전달
                            with torch.no_grad():
                                outputs = self.cnn_model(input_tensor)

                            # 예측 결과 확인
                            _, predicted_class = torch.max(outputs, 1)
                            
                            if predicted_class == 0:
                                object_label = 'apple'
                            elif predicted_class == 1:
                                object_label = 'banana'
                            else:
                                object_label = 'orange'

                            self.output_data['fruit_type'] = predicted_class.item()
                            self.output_data['fruit_quantity'] = 1
                            
                            self.status = action_text + ' ' + object_label
                        
                        self.output_data['action'] = act_out.item()
                        if self.output_data['person'] == 0:
                                self.keys = ["person", "action", "fruit_type", "fruit_quantity"]
                                self.values = [0, 0, 5, 0]
                                self.output_data = dict(zip(self.keys, self.values))
                        
                        print()

            img = self.box_annotator.annotate(scene=img, detections=detections, labels=labels)           
            cv2.putText(img, self.status, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            return img, self.output_data

    