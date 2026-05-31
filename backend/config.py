import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "best.pt")

# Detection settings
CONF_THRESHOLD = 0.35       # minimum confidence for a dot detection
IOU_THRESHOLD  = 0.45       # NMS IoU threshold
IMG_SIZE       = 640         # YOLO input image size

# Cell grouping settings
ROW_TOLERANCE  = 15          # pixels — dots within this Y-distance = same row
COL_TOLERANCE  = 20          # pixels — dots within this X-distance = same column
CELL_GAP_RATIO = 2.5         # gap between cells vs gap between dots in same cell

# TTS settings
TTS_RATE   = 150             # words per minute
TTS_VOLUME = 1.0

# API settings
HOST = "0.0.0.0"
PORT = 8000
CORS_ORIGINS = [
	"http://localhost:5173",
	"http://127.0.0.1:5173",
	"http://localhost:5174",
	"http://127.0.0.1:5174",
]
