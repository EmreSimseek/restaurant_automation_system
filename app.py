# app.py

from flask import Flask, render_template, Response, jsonify
import cv2
from collections import Counter
from ultralytics import YOLO
import time

# --- Config Dosyasını Güvenli Bir Şekilde Yükle ---
try:
    from config import VIDEO_PATH, YOLO_MODEL_PATH, FOOD_PRICES, WAITER_CLASS_NAME, RESET_CLASS_NAME
except ImportError:
    print("❌ HATA: config.py dosyası bulunamadı veya içindeki değişkenler eksik!")
    print("-> Lütfen YOLO_MODEL_PATH, VIDEO_PATH, FOOD_PRICES, WAITER_CLASS_NAME, RESET_CLASS_NAME değişkenlerinin tanımlı olduğundan emin olun.")
    exit()

# --- Sipariş Yönetim Sınıfı ---
class OrderManager:
    def __init__(self):
        """Sınıf başlatıldığında oturumu temiz bir şekilde hazırlar."""
        self.reset_session()
        
    def reset_session(self):
        """Oturumu sıfırlar, her şeyi başlangıç durumuna getirir."""
        print("🔄 OTURUM SIFIRLANDI. Yeni sipariş için garson bekleniyor.")
        self.is_session_active = False
        self.items_on_table = Counter()
        self.session_orders = []
        self.total_bill = 0.0
        self.status_message = "GARSON BEKLENİYOR..."
        self.last_activity_time = time.time()

    def update_from_yolo(self, detected_class_names):
        """Sadece YOLO'dan gelen sınıf isim listesine göre durumu günceller."""
        current_time = time.time()

        # 1. Oturumu Sıfırlama Komutunu Kontrol Et
        if RESET_CLASS_NAME in detected_class_names:
            if self.is_session_active:
                self.reset_session()
            return

        # 2. Oturumu Başlatma Komutunu (Garsonu) Kontrol Et
        # Oturum henüz aktif değilse ve garson tespit edildiyse, oturumu başlat.
        if not self.is_session_active and WAITER_CLASS_NAME in detected_class_names:
            print(f"✅ OTURUM BAŞLATILDI ({WAITER_CLASS_NAME} tespit edildi).")
            self.is_session_active = True
            self.status_message = "SİPARİŞLERİNİZ BEKLENİYOR"
            self.last_activity_time = current_time
        
        # Oturum aktif değilse, sipariş işlemlerine geçme.
        if not self.is_session_active:
            return

        # 3. Yemekleri Ayıkla ve Yeni Eklenenleri Bul
        current_foods = Counter([name for name in detected_class_names if name in FOOD_PRICES])
        newly_added_foods = current_foods - self.items_on_table
        
        if newly_added_foods:
            food_names = ", ".join(newly_added_foods.keys()).upper()
            self.status_message = f"YENİ SİPARİŞ: {food_names}"
            self.last_activity_time = current_time
            
            for food_name, count in newly_added_foods.items():
                for _ in range(count):
                    self._add_order(food_name)
            
            # Masanın son durumunu hafızaya al ki aynı yemek tekrar eklenmesin.
            self.items_on_table = current_foods
        
        # 4. Son aktiviteden bu yana belirli bir süre geçtiyse, durumu "izleniyor" yap.
        elif current_time - self.last_activity_time > 5:
             self.status_message = "MASA İZLENİYOR"

    def _add_order(self, food_name):
        """Bir yemeği sipariş listesine ve hesaba ekler."""
        price = FOOD_PRICES.get(food_name, 0.0)
        self.total_bill += price
        self.session_orders.append({'urun': food_name, 'fiyat': price})
        print(f" SİPARİŞ EKLENDİ: {food_name.upper()} | Fiyat: {price:.2f} TL | Yeni Toplam: {self.total_bill:.2f} TL")

    def get_summary_data(self):
        """Arayüze gönderilecek tüm veriyi tek bir yerden toplar."""
        return {
            "session_orders": self.session_orders,
            "total_bill": self.total_bill,
            "status_message": self.status_message
        }

# --- Flask Uygulaması ve Video Akışı ---
app = Flask(__name__)
yolo_model = YOLO(YOLO_MODEL_PATH)
order_manager = OrderManager()
cap = cv2.VideoCapture(VIDEO_PATH)

def generate_frames():
    """Video akışını oluşturur, YOLO tespitlerini yapar ve siparişleri yönetir."""
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        results = yolo_model(frame, verbose=False, conf=0.5)[0]
        detected_class_names = [yolo_model.names[int(c)] for c in results.boxes.cls]
        
        order_manager.update_from_yolo(detected_class_names)
        
        # Görüntü üzerine kutu ve etiketleri çiz
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = yolo_model.names[int(box.cls[0])]
            # Garson ve Hesap kartını farklı renkte göster
            color = (255, 0, 255) if label in [WAITER_CLASS_NAME, RESET_CLASS_NAME] else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# --- Flask Rotaları ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_data')
def get_data():
    """Frontend'in anlık verileri çekmesi için ana API noktası."""
    # Ham veriyi al
    data = order_manager.get_summary_data()
    
    # Frontend için veriyi özetle (aynı yemekleri grupla)
    summary = {}
    for order in data["session_orders"]:
        item = order['urun']
        if item not in summary:
            summary[item] = {'count': 0, 'price': 0.0}
        summary[item]['count'] += 1
        summary[item]['price'] += order['fiyat']

    # Özetlenmiş veriyi gönder
    return jsonify({
        "order_summary": summary,
        "total_bill": data["total_bill"],
        "status_message": data["status_message"]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)