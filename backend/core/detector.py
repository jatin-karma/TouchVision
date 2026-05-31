"""
YOLOv8 Braille dot detector.
Loads best.pt and returns bounding boxes for detected dots.
"""

import cv2
import numpy as np
from ultralytics import YOLO
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MODEL_PATH, CONF_THRESHOLD, IOU_THRESHOLD, IMG_SIZE


class BrailleDetector:
    """
    Wraps YOLOv8 model for Braille dot detection.
    Handles model loading, inference, and result parsing.
    """

    def __init__(self, weights_path: str = None):
        path = weights_path or MODEL_PATH

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Model weights not found at: {path}\n"
                f"Please download best.pt from the Google Drive link in model/model_info.md"
            )

        self.model = YOLO(path)
        self.conf  = CONF_THRESHOLD
        self.iou   = IOU_THRESHOLD
        self.imgsz = IMG_SIZE
        print(f"✅ BrailleDetector loaded: {path}")

    def detect(self, frame: np.ndarray) -> tuple:
        """
        Run YOLOv8 inference on a preprocessed frame.

        Args:
            frame: BGR numpy array (preprocessed)

        Returns:
            boxes: list of [x1, y1, x2, y2] bounding boxes (dot locations)
            confs: list of confidence scores for each box
        """
        results = self.model(
            frame,
            conf=self.conf,
            iou=self.iou,
            imgsz=self.imgsz,
            augment=True,  # Enable Test-Time Augmentation for better accuracy
            verbose=False
        )[0]

        if results.boxes is None or len(results.boxes) == 0:
            return [], [], []

        boxes = results.boxes.xyxy.cpu().numpy().tolist()
        confs = results.boxes.conf.cpu().numpy().tolist()
        classes = results.boxes.cls.cpu().numpy().tolist()
        labels = [self.model.names[int(c)] for c in classes]

        return boxes, confs, labels

    def detect_with_annotated(self, frame: np.ndarray) -> tuple:
        """
        Run detection and return annotated frame for display.

        Returns:
            boxes, confs, annotated_frame (BGR)
        """
        results = self.model(
            frame,
            conf=self.conf,
            iou=self.iou,
            imgsz=self.imgsz,
            augment=True,  # Enable Test-Time Augmentation for better accuracy
            verbose=False
        )[0]

        boxes = []
        confs = []
        labels = []

        if results.boxes is not None and len(results.boxes) > 0:
            boxes = results.boxes.xyxy.cpu().numpy().tolist()
            confs = results.boxes.conf.cpu().numpy().tolist()
            classes = results.boxes.cls.cpu().numpy().tolist()
            labels = [self.model.names[int(c)] for c in classes]

        annotated = results.plot()
        return boxes, confs, labels, annotated
