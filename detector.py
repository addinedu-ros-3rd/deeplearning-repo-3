import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
from supervision.geometry.core import Rect


class Detector:

    def __init__(self, model, frame_width, frame_height):
        self.model = model
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.colors = sv.ColorPalette.default()

        self.roi_points = []
        with open("save.txt", "r") as f:
            for line in f.readlines():
                l = line.split()
                cls, points = l[0], l[1:]
                tmp = np.array(list(map(np.float32, points)))
                tmp = tmp.reshape((4, 2))
                tmp = tmp * [frame_width, frame_height]
                tmp = tmp.astype(np.int32)

                self.roi_points.append(tmp)

        self.zones = [
            sv.PolygonZone(
                polygon=points,
                frame_resolution_wh=(frame_width, frame_height)
            ) for points in self.roi_points
        ]
        self.zone_annotators = [
            sv.PolygonZoneAnnotator(
                zone=zone, 
                color=self.colors.by_idx(i),
                thickness=2,
                text_thickness=1,
                text_scale=0.5
            ) for i, zone in enumerate(self.zones)
        ]
        self.zone_annotator_points = [
            np.mean(points, axis=0).astype(int) for points in self.roi_points 
        ]

        self.box_annotators = [
            sv.BoxAnnotator(
                color=self.colors.by_idx(i),
                thickness=1,
                text_thickness=1,
                text_scale=0.5
            ) for i in range(len(self.roi_points))
        ]

        # 0:person 49:orange 47:apple 46:banana
        self.item_dict = {
            46: "Banana",
            47: "Apple",
            49: "Orange"
        }



    def detect_fruit_in_box(self, frame = None):
        if (self.model is None) or (frame is None):
            raise ValueError("model 또는 frame이 없습니다.")

        results = self.model(frame)[0]
        detections = sv.Detections.from_yolov8(results)
        detections = detections[detections.confidence > 0.5]

        for zone, zone_annotator, zone_annot_point, box_annotator in zip(self.zones, self.zone_annotators, self.zone_annotator_points, self.box_annotators):
            mask = zone.trigger(detections=detections)
            detections_in_mask = detections[mask]

            frame = box_annotator.annotate(scene=frame, detections=detections_in_mask)
            frame = zone_annotator.annotate(scene=frame)

            for i, id in enumerate(self.item_dict.keys()):
                detections_id = detections_in_mask[detections_in_mask.class_id == id]

                text = f"{self.item_dict[id]}: {len(detections_id.class_id)}"

                frame = self.draw_text(frame, i, text, zone_annot_point, zone_annotator.color.as_bgr())
            
        return frame

    
    
    def draw_text(self, frame, idx, text, position, background_color):
        text_font = cv2.FONT_HERSHEY_SIMPLEX
        text_scale = 1
        text_thickness = 2
        text_interval = 25

        text_width, text_height = cv2.getTextSize(
            text=text,
            fontFace=text_font,
            fontScale=text_scale,
            thickness=text_thickness,
        )[0]

        text_rect = Rect(
            x=position[0] - text_width // 2,
            y=(position[1] + text_interval*idx) - text_height // 2,
            width=text_width,
            height=text_height,
        )

        cv2.rectangle(
            frame,
            text_rect.top_left.as_xy_int_tuple(),
            text_rect.bottom_right.as_xy_int_tuple(),
            background_color,
            -1,
        )

        cv2.putText(frame,
                    text,
                    (position[0] - text_width // 2,
                        position[1] + text_height // 2 + text_interval*idx),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=text_scale,
                    color=(0,0,0),
                    thickness=text_thickness
        )

        return frame