# 🍽️ Restoran Akıllı Masa Otomasyonu

Web tabanlı sistem ile masaya servis edilen ürünleri **gerçek zamanlı tespit** eder, **sipariş** ve **hesap** işlemlerini otomatik yönetir.

---

## 🚀 Ana Özellikler

- **Canlı Nesne Tespiti**  
  YOLOv8 ile yemek ve içecekleri (makarna, mercimek, tavuk ızgara, aşure vb.) anlık olarak tanır.

- **Otomatik Sipariş & Hesap**  
  Tespit edilen ürünleri sipariş listesine ekler, toplam hesabı otomatik hesaplar.

- **QR Kodla Garson Tanıma**  
  Garsonun QR kodu okunduğunda sipariş işlemi başlatılır.

- **Hesap Kapatma**  
  “HESAP_KAPAT” QR kodu veya manuel işlem ile masa sıfırlanır.

- **Web Arayüzü**  
  Canlı video, sipariş listesi, garson durumu ve toplam hesap bilgisi kullanıcıya gösterilir.

---

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python, Flask  
- **Görüntü İşleme:** OpenCV, YOLOv8 (Ultralytics)  
- **QR Kod Okuma:** Pyzbar  
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

---

## 📁 Proje Yapısı

restoran_otomasyonu/
├── app.py # Ana Flask uygulaması
├── config.py # Yapılandırmalar (model yolu, fiyatlar, QR kodlar)
├── README.md # Bu belge
│
├── templates/
│ └── index.html # Web arayüzü
│
├── models/
│ └── best.pt # YOLOv8 eğitilmiş model
│
└── video_input/
└── test_video.mp4 # Örnek video girişi

yaml
Copy
Edit

---

## ⚙️ Kurulum ve Çalıştırma

### 1. Gereksinimlerin Kurulumu

Aşağıdaki komut ile gerekli kütüphaneleri kurun:

```bash
pip install flask ultralytics opencv-python pyzbar numpy
2. Yapılandırma
config.py dosyasını düzenleyin:

YOLO_MODEL_PATH: .pt model dosyasının yolu

VIDEO_PATH: Giriş videosunun yolu

FOOD_PRICES: Ürün adları ve fiyatları

WAITER_QR_MAPPING: QR metinleri (garsonlar ve "HESAP_KAPAT")

3. Uygulamayı Başlatma
Ana dizinde şu komutu çalıştırın:

bash
Copy
Edit
python app.py
Tarayıcıdan erişim adresleri:

Yerel: http://127.0.0.1:5001

Ağ üzeri: http://<IP_ADRESİNİZ>:5001

🔮 Gelecekteki Geliştirmeler
Veritabanı Desteği (SQLite/PostgreSQL)

Çoklu Masa Yönetimi

Satış ve Sipariş Raporları

Garson Girişi / Şifre Doğrulama
