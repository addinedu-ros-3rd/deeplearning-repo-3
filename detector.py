import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np


class Detector:

    def __init__(self, model, frame_width, frame_height, args):
        self.model = model
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.colors = sv.ColorPalette.default()

        self.ZONE_POLYGON = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ])

        self.roi_points = []
        with open("save.txt", "r") as f:
            for line in f.readlines():
                l = line.split()
                cls, points = l[0], l[1:]
                tmp = np.array(list(map(np.float32, points))).astype(np.int32)
                tmp = tmp.reshape((4, 2))

                self.roi_points.append(tmp)


        self.zones = [
            sv.PolygonZone(
                polygon=points,
                frame_resolution_wh=tuple(args.webcam_resolution)
            ) for points in self.roi_points
        ]
        self.zone_annotators = [
            sv.PolygonZoneAnnotator(
                zone=zone, 
                color=self.colors.by_idx(i),
                thickness=2,
                text_thickness=4,
                text_scale=2
            ) for i, zone in enumerate(self.zones)
        ]

        self.box_annotators = [
            sv.BoxAnnotator(
                color=self.colors.by_idx(i),
                thickness=2,
                text_thickness=2,
                text_scale=1
            ) for i in range(len(self.roi_points))
        ]

        # 0:person 49:orange 47:apple 46:banana
        self.item_dict = {46: "Banana",
                    47: "Apple",
                    49: "Orange"}



    def detect_fruit_in_box(self, frame = None):
        if (self.model is None) or (frame is None):
            raise ValueError("model 또는 frame이 없습니다.")

        results = self.model(frame)[0]
        detections = sv.Detections.from_yolov8(results)
        # detections = detections[detections.confidence > 0.5]

        for zone, zone_annotator, box_annotator in zip(self.zones, self.zone_annotators, self.box_annotators):
            mask = zone.trigger(detections=detections)
            detections_filtered = detections[mask]
            frame = box_annotator.annotate(scene=frame, detections=detections_filtered, skip_label=True)
            frame = zone_annotator.annotate(scene=frame)

        return frame