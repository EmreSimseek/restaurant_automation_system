# config.py

# --- Dosya Yolları ---
# Modelinizin ve videonuzun yollarını buraya yazın.
YOLO_MODEL_PATH = 'models/best.pt'
VIDEO_PATH = 'video_input/test_video.mp4'


# --- Ürün Fiyatları ---
# ÖNEMLİ: Buradaki anahtar isimler, YOLO modelinizin tanıdığı yemek sınıflarının
# isimleri (labels) ile BİREBİR AYNI olmalıdır.
FOOD_PRICES = {
    "makarna": 40.00,
    "mercimek": 60.00,
    "tavuk_izgara": 150.00,
    "asure": 50.00
    # Modelinizin tanıdığı diğer YEMEK sınıflarını buraya ekleyebilirsiniz.
}


# --- Özel Sınıf İsimleri ---
# YOLO modelinizde garsonu/oturumu başlatan sınıfın adı.
WAITER_CLASS_NAME = "qr1"

# YOLO modelinizde hesabı/oturumu kapatan sınıfın adı.
RESET_CLASS_NAME = "hesap"