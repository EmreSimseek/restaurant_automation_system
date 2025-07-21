# app.py

import cv2
import time
from collections import Counter

from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO
from pyzbar.pyzbar import decode

# --- Ayarlar ve Sınıflar ---

# config.py dosyasından gerekli ayarları çekiyoruz.
# Bu dosyanın app.py ile aynı dizinde olduğundan emin olun.
from config import VIDEO_PATH, YOLO_MODEL_PATH, FOOD_PRICES, WAITER_QR_MAPPING

# OrderManager (Sipariş Mantığı Sınıfı)
class OrderManager:
    """Masa ile ilgili tüm durumu yöneten sınıf."""
    def __init__(self):
        self.active_waiter = None
        self.items_on_table = Counter()
        self.session_orders = []
        self.total_bill = 0.0
        self.is_waiter_identified = False

    def update(self, detected_items, qr_data_list):
        """Her video karesinden gelen yeni verilerle durumu günceller."""
        # Henüz garson tanımlanmadıysa, QR kodlarını kontrol et
        if not self.is_waiter_identified:
            for qr_data in qr_data_list:
                if qr_data in WAITER_QR_MAPPING:
                    waiter_action = WAITER_QR_MAPPING[qr_data]
                    
                    if waiter_action == "HESAP_KAPAT":
                        print("BİLGİ: 'HESAP_KAPAT' QR kodu okundu. Oturum sıfırlanıyor.")
                        self.reset_session()
                    else:
                        self.active_waiter = waiter_action
                        self.is_waiter_identified = True
                        print(f"BİLGİ: Garson Tanımlandı -> {self.active_waiter}")
                    break
        
        # Garson tanımlandıktan sonra masaya eklenen ürünleri işle
        if self.is_waiter_identified:
            # Masaya yeni eklenen ürünleri bul (mevcut durumdan farkı)
            newly_added_items = detected_items - self.items_on_table
            if newly_added_items:
                for item, count in newly_added_items.items():
                    # Counter farkı kadar ürün ekle
                    for _ in range(count):
                        self._add_order(item)
                # Masadaki ürün listesini tam olarak yeni tespit edilenle eşitle
                self.items_on_table = detected_items.copy()

    def _add_order(self, item_name):
        """Listeye ve hesaba yeni bir sipariş ekler."""
        price = FOOD_PRICES.get(item_name, 0.0)
        self.total_bill += price
        self.session_orders.append({'urun': item_name, 'fiyat': price})
        print(f"SİPARİŞ EKLENDİ: {item_name} ({price:.2f} TL) | GÜNCEL HESAP: {self.total_bill:.2f} TL")

    def reset_session(self):
        """Tüm siparişleri, hesabı ve garsonu sıfırlar."""
        self.active_waiter = None
        self.items_on_table.clear()
        self.session_orders.clear()
        self.total_bill = 0.0
        self.is_waiter_identified = False
        print("BİLGİ: Oturum başarıyla sıfırlandı.")

    def get_full_status(self):
        """Frontend'e göndermek için tam durumu (garson, siparişler, toplam) oluşturur."""
        summary = {}
        for order in self.session_orders:
            item = order['urun']
            if item not in summary:
                summary[item] = {'count': 0, 'price': 0.0}
            summary[item]['count'] += 1
            summary[item]['price'] += order['fiyat']
        
        return {
            "active_waiter": self.active_waiter,
            "order_summary": summary,
            "total_bill": self.total_bill
        }

# --- Global Değişkenler ve Flask Uygulaması ---

app = Flask(__name__)

# Global nesneleri başlat
yolo_model = YOLO(YOLO_MODEL_PATH)
order_manager = OrderManager()
# Videoyu açarken hata kontrolü eklemek iyi bir pratiktir
try:
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise IOError(f"Video dosyası açılamadı: {VIDEO_PATH}")
except Exception as e:
    print(f"HATA: {e}")
    exit()


def generate_frames():
    """
    Video karesini okur, işler ve bir JPEG dizisine dönüştürür.
    Bu fonksiyon bir 'generator' olarak çalışarak video akışı sağlar.
    """
    while True:
        success, frame = cap.read()
        if not success:
            print("Video sonuna gelindi, başa sarılıyor...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        # --- Görüntü İşleme ve Mantık ---
        # 1. YOLO ile nesne tespiti yap
        results = yolo_model(frame, verbose=False)[0]
        detected_items = Counter(yolo_model.names[int(c)] for c in results.boxes.cls)
        
        # 2. Pyzbar ile QR kod tespiti yap
        qr_objects = decode(frame)
        qr_data_list = [obj.data.decode('utf-8') for obj in qr_objects]
        
        # 3. Sipariş yöneticisini yeni verilerle güncelle
        order_manager.update(detected_items, qr_data_list)
        
        # 4. Görüntü üzerine anlık bilgileri çiz (Görselleştirme için)
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = yolo_model.names[int(box.cls[0])]
            confidence = box.conf[0]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} ({confidence:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # QR kodlarını da çerçeve içine al
        for qr in qr_objects:
            (x, y, w, h) = qr.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.putText(frame, qr.data.decode('utf-8'), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # 5. Kareyi web'de gösterilecek formata çevir
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        
        # 'yield' ile kareyi bir HTTP response parçası olarak gönder
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        # Sunucuyu yormamak için küçük bir bekleme süresi eklenebilir
        # time.sleep(0.05) 

# --- Flask Rotaları (URL Endpoints) ---

@app.route('/')
def index():
    """Ana sayfayı (index.html) render eder."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video akışını sağlayan rota."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_data')
def get_data():
    """
    JavaScript'in anlık verileri (hesap, garson vb.) çekmesi için API endpoint'i.
    JSON formatında veri döndürür.
    """
    return jsonify(order_manager.get_full_status())

@app.route('/reset')
def reset():
    """Hesabı manuel olarak sıfırlamak için bir API endpoint'i (Test için kullanışlı)."""
    order_manager.reset_session()
    return jsonify({"status": "success", "message": "Oturum sıfırlandı."})


if __name__ == '__main__':
    # Flask sunucusunu başlatır.
    # host='0.0.0.0' ağdaki diğer cihazların da erişebilmesini sağlar.
    app.run(debug=True, host='0.0.0.0', port=5001)