import cv2
import argparse

from ultralytics import YOLO
import supervision as sv
import numpy as np


ZONE_POLYGON = np.array([
    [0, 0],
    [1, 0],
    [1, 1],
    [0, 1]
])

roi_coordinates = [
    [(100, 200), (400, 600)],  # 첫 번째 roi 좌표 (x1, y1), (x2, y2)
    [(500, 200), (800, 600)],  # 두 번째 roi 좌표 (x1, y1), (x2, y2)
    [(900, 200), (1200, 600)]   # 세 번째 roi 좌표 (x1, y1), (x2, y2)
]

# 0:person 49:orange 47:apple 46:banana
item_dict = {46: "Banana",
             47: "Apple",
             49: "Orange"}

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("yolov8l.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone, 
        color=sv.Color.red(),
        thickness=2,
        text_thickness=4,
        text_scale=2
    )

    while True:
        ret, frame = cap.read()

        if ret:
            # 각각의 roi를 생성하고 detecting
            for idx, (start, end) in enumerate(roi_coordinates):
                x1, y1 = start
                x2, y2 = end

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                roi = frame[y1:y2, x1:x2]  # 주의: y1:y2, x1:x2로 수정
                roi = np.ascontiguousarray(roi)

                result = model(roi, agnostic_nms=True)[0]

                detections = sv.Detections.from_yolov8(result)
                selected_classes = item_dict.keys()
                # detections = detections[np.isin(detections.class_id, selected_classes)]
                
                detect_dict = {k: 0 for k in selected_classes}

                for detect in detections:
                    # print(detect)
                    xyxy, conf, id, _ = detect

                    if id in selected_classes:
                        detect_dict[id] += 1
                
                # labels = [
                #     f"{model.model.names[class_id]} {confidence:0.2f}"
                #     for _, confidence, class_id, _
                #     in detections
                # ]

                # roi 영역에 탐지된 물체 수 계산
                num_detections = sum(detect_dict.values())

                # roi 영역에 탐지된 물체 수 표시
                cv2.putText(frame, f"Detections: {num_detections}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                # print("-------------")
                print(f"Box {idx} : ")
                for idx, sc in enumerate(selected_classes):
                    # print(f"{sc} : {detect_dict[sc]}")
                    cv2.putText(frame, f"{item_dict[sc]}: {detect_dict[sc]}", (x1, y1 - (20 * (idx+1))),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                # print("-------------")
                
                # 원본 프레임에 roi 영역과 탐지된 물체 표시
                frame[y1:y2, x1:x2] = roi
            
            # zone.trigger(detections=detections)
            # frame = zone_annotator.annotate(scene=frame)      
            
            cv2.imshow("yolov8", frame)

            if (cv2.waitKey(30) == 27):
                break


if __name__ == "__main__":
    main()