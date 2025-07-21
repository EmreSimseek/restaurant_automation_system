# Restoran Akıllı Masa Otomasyonu
Bu proje, bir restoran masasına servis edilen ürünleri kamera aracılığıyla gerçek zamanlı olarak tespit eden, siparişleri ve hesabı otomatik olarak yöneten bir web tabanlı otomasyon sistemidir. Sistem, YOLOv8 ile nesne tespiti, Pyzbar ile QR kod okuma ve Flask ile web arayüzü sunma teknolojilerini kullanır.
<!-- Buraya kendi arayüzünüzün bir ekran görüntüsünü ekleyebilirsiniz. -->
🚀 Özellikler
Gerçek Zamanlı Nesne Tespiti: Masaya konulan yiyecek ve içecekleri (makran, mercimek, tavuk_izgara, asure vb.) canlı video akışından tanır.
Otomatik Sipariş ve Hesap Yönetimi: Tespit edilen her yeni ürünü otomatik olarak sipariş listesine ve hesaba ekler.
Garson Tanıma: Garsonun taşıdığı bir QR kodu okuyarak sipariş işlemini başlatır.
Hesap Sıfırlama: Özel bir "Hesap Kapat" QR kodu ile veya manuel olarak masa hesabını sıfırlar.
Web Arayüzü: Tüm bilgileri (canlı video, garson durumu, sipariş listesi, toplam hesap) anlık olarak gösteren modern ve kullanıcı dostu bir arayüz sunar.
🛠️ Kullanılan Teknolojiler
Backend: Python, Flask
Görüntü İşleme: OpenCV, Ultralytics YOLOv8
QR Kod Okuma: Pyzbar
Frontend: HTML5, CSS3, JavaScript
📂 Proje Yapısı
Generated code
restoran_otomasyonu/
├── app.py             # Ana Flask uygulaması ve mantık
├── config.py          # Yapılandırma dosyası (dosya yolları, fiyatlar, QR kodlar)
├── README.md          # Bu dosya
│
├── templates/
│   └── index.html     # Web arayüzü
│
├── models/
│   └── best.pt        # Eğitilmiş YOLOv8 modeli
│
└── video_input/
    └── test_video.mp4 # Analiz edilecek örnek video
Use code with caution.
⚙️ Kurulum ve Çalıştırma
1. Gerekli Kütüphanelerin Kurulumu
Projeyi çalıştırmadan önce aşağıdaki Python kütüphanelerini kurmanız gerekmektedir.
Generated bash
pip install flask ultralytics opencv-python pyzbar numpy
Use code with caution.
Bash
2. Yapılandırma (config.py)
Projenin düzgün çalışması için config.py dosyasını kendi ayarlarınıza göre düzenleyin:
YOLO_MODEL_PATH: Eğittiğiniz .pt model dosyasının yolunu belirtin.
VIDEO_PATH: Analiz edilecek videonun yolunu belirtin.
FOOD_PRICES: YOLO modelinizin tanıdığı sınıflarla eşleşen ürün isimlerini ve fiyatlarını girin.
WAITER_QR_MAPPING: Garsonları ve diğer işlemleri (örn: HESAP_KAPAT) tetikleyecek QR kod metinlerini tanımlayın.
3. Projeyi Başlatma
Terminali projenin ana dizininde açın ve aşağıdaki komutu çalıştırın:
Generated bash
python app.py
Use code with caution.
Bash
Sunucu başladıktan sonra web tarayıcınızdan aşağıdaki adreslere erişebilirsiniz:
Ana Arayüz: http://127.0.0.1:5001
Ağdaki Diğer Cihazlardan Erişim: http://<bilgisayarınızın_yerel_ip_adresi>:5001
🔮 Gelecek Geliştirmeler
Veritabanı Entegrasyonu (SQLite/PostgreSQL): Siparişleri kalıcı olarak saklamak.
Çoklu Masa Desteği: Her masayı ayrı bir QR kod ile tanımlayarak birden fazla masayı aynı anda yönetmek.
Gelişmiş Raporlama: Belirli tarih aralıkları için satış raporları oluşturma.
Kullanıcı Doğrulama: Garsonların sisteme bir şifre ile giriş yapması.
