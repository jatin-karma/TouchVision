"""
YOLOv8 Model Training Script for Braille Dot Detection.
This script trains a YOLOv8 detector on the custom Braille dataset.
"""

from ultralytics import YOLO
import os

# Load a slightly larger pretrained YOLOv8 model for better accuracy
model = YOLO("yolov8m.pt")

# Get dataset path
dataset_path = os.path.join(os.path.dirname(__file__), "..", "dataset", "data.yaml")

# Train the model with advanced hyperparameters
results = model.train(
    data=dataset_path,
    epochs=300,            # Increased epochs for better convergence
    imgsz=1024,            # Increased resolution to detect tiny braille dots better
    batch=8,               # Lowered batch size to prevent OOM with larger imgsz
    patience=50,           # Early stopping patience
    device=0,              # GPU device ID
    project="runs/detect",
    name="braille_dot_detector",
    exist_ok=True,
    
    # Custom Augmentations tailored for Braille (Lighting & Rotation)
    degrees=10.0,          # Slight rotations (paper might not be perfectly straight)
    hsv_v=0.6,             # Significant brightness variation (crucial for embossed shadows)
    hsv_s=0.5,             # Saturation variation
    perspective=0.0005,    # Slight perspective warping (camera tilt)
    fliplr=0.0,            # DISABLED: Never flip left-right (Braille is not symmetric!)
    flipud=0.0,            # DISABLED: Never flip up-down
    mosaic=1.0,            # Mosaic augmentation (combines 4 images into 1)
)

# Evaluate on validation set
metrics = model.val()

# Run inference on test set
results = model.predict(source="path/to/test/images", save=True)

print("✅ Training completed!")
print(f"Best model: runs/detect/braille_dot_detector/weights/best.pt")
