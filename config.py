# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YOLO_MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")

class Config:
    # --- Dosya ve Model Yolları ---
    VIDEO_PATH = "video_input/test_video1.mp4"
    YOLO_MODEL_PATH = "models/best.pt"
    DATABASE_PATH = "restoran_veritabani.db" # Veritabanı dosyasının adı ve yolu

    # --- Ürün ve Fiyat Bilgileri ---
    FOOD_PRICES = {
        'corba': 40.0,
        'tavuk_izgara': 150.0,
        'makarna': 50.0,
        'asure': 60.0,
        
    }

    # --- QR Kod Tanımlamaları ---
    WAITER_QR_MAPPING = {
        "garson_ali_qr_id_123": "Garson Ali",
        "garson_veli_qr_id_456": "Garson Veli"
    }
    CUSTOMER_ARRIVED_QR = "musteri_geldi"
    RESET_TABLE_QR = "hesap_kapat"

    # --- Garson Performans Ayarları ---
    WAITER_RESPONSE_TIMEOUT_SECONDS = 10

    # --- Görüntü ve Panel Ayarları ---
    WINDOW_NAME = "Restoran Yönetim Sistemi"
    PANEL_START_X = 880
    
    # Renkler (BGR formatında)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (255, 150, 0)
    COLOR_YELLOW = (0, 255, 255)
    COLOR_RED = (0, 0, 255)