# config.py

# --- Dosya Yolları ---
# YOLO modelinizin bulunduğu yol. 'models' klasörü içinde olduğunu varsayıyoruz.
# Kendi .pt dosyanızın adını buraya yazın (Örn: 'yolov8n.pt', 'best.pt' vb.).
YOLO_MODEL_PATH = 'models/best.pt' # Kendi model dosyanızın adını yazın

# Analiz edilecek videonun yolu. 'video_input' klasöründe olduğunu varsayıyoruz.
VIDEO_PATH = 'video_input/test_video.mp4' # Kendi video dosyanızın adını yazın


# --- Uygulama Mantığı Ayarları ---

# Ürün Fiyatları
# ÖNEMLİ: Buradaki anahtar isimler, YOLOv8 modelinizin tanıdığı sınıf
# isimleriyle (labels) BİREBİR AYNI olmalıdır.
# Modeliniz "tavuk_izgara" olarak tanıyorsa, buraya da "tavuk_izgara" yazmalısınız.
# Büyük/küçük harf ve alt çizgi gibi karakterler önemlidir.
FOOD_PRICES = {
    "makran": 120.00,       # Model sınıfı: "makran"
    "mercimek": 85.50,      # Model sınıfı: "mercimek"
    "tavuk_izgara": 280.00, # Model sınıfı: "tavuk_izgara"
    "asure": 95.00         # Model sınıfı: "asure"
   
}

# Garson QR Kod Eşleştirmesi
# ÖNEMLİ: Buradaki anahtar, QR kodun içinde yazan metindir.
# Değer ise arayüzde görünecek garson ismidir.
WAITER_QR_MAPPING = {
    "WAITER_ID_001": "Ahmet Yılmaz",
    "WAITER_ID_002": "Zeynep Kaya",
    "QR_GARSON_AYSE": "Ayşe Demir", # Örnek: QR kod içinde "QR_GARSON_AYSE" yazıyor.
    "HESAP_KAPAT_MASA1": "HESAP_KAPAT" # Hesap kapatma için özel bir kod
}