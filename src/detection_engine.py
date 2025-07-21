# src/detection_engine.py

from ultralytics import YOLO
from pyzbar.pyzbar import decode
from collections import Counter

class DetectionEngine:
    """Tüm bilgisayarlı görü işlemlerini yöneten sınıf."""
    def __init__(self, model_path):
        try:
            self.yolo_model = YOLO(model_path)
        except Exception as e:
            raise Exception(f"YOLO modeli yüklenemedi: {e}")

    def process_frame(self, frame):
        """Tek bir video karesini işler, nesneleri ve QR kodları tespit eder."""
        results = self.yolo_model(frame, verbose=False)[0]
        detected_items = Counter(self.yolo_model.names[int(c)] for c in results.boxes.cls)
        qr_data_list = [obj.data.decode('utf-8') for obj in decode(frame)]
        return detected_items, qr_data_list