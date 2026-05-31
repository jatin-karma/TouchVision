"""
OpenCV preprocessing pipeline.
Converts raw camera frame → binary image suitable for YOLO dot detection.
Handles low-contrast embossed Braille (dots same color as paper).
"""

import cv2
import numpy as np


def preprocess(frame: np.ndarray) -> np.ndarray:
    """
    Full preprocessing pipeline for embossed Braille images.
    
    Args:
        frame: BGR image from camera (numpy array)
    
    Returns:
        Preprocessed BGR image ready for YOLO inference
    """
    # Step 1: Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Step 2: CLAHE — boosts local contrast (critical for embossed Braille)
    # Embossed dots have very low contrast; CLAHE makes them visible
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Step 3: Gaussian blur — removes camera noise
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)

    # Step 4: Adaptive threshold — handles uneven lighting across the paper
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=11,
        C=2
    )

    # Step 5: Morphological closing — fills gaps in dot circles
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Step 6: Convert back to BGR for YOLO (YOLO expects 3-channel input)
    result = cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)

    return result


def preprocess_for_display(frame: np.ndarray) -> np.ndarray:
    """
    Lighter preprocessing — just CLAHE enhancement for display purposes.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
