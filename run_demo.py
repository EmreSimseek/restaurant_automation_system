# run_demo.py

import cv2
from config import Config
from src.detection_engine import DetectionEngine
from src.table_manager import TableManager
from src.display_panel import DisplayPanel
from src.report_generator import ReportGenerator
from src.database_handler import DatabaseHandler
def main():
    print("Restoran Yönetim Sistemi başlatılıyor...")
    
    cfg = Config()
    db = DatabaseHandler(db_file=cfg.DATABASE_PATH)  
    engine = DetectionEngine(model_path=cfg.YOLO_MODEL_PATH)
    table = TableManager(db_handler=db)
    panel = DisplayPanel()
    reporter = ReportGenerator()

    cap = cv2.VideoCapture(cfg.VIDEO_PATH)
    if not cap.isOpened():
        print(f"HATA: Video dosyası açılamadı! -> {cfg.VIDEO_PATH}")
        return
    print("Video analizi başlıyor... Çıkmak için 'q' tuşuna basın.")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 1. Tespit
        detected_items, qr_data = engine.process_frame(frame)
        
        # 2. Mantık
        table.update(detected_items, qr_data)
        
        # 3. Görselleştirme
        panel.draw(frame, table)
        
        # 4. Gösterim
        cv2.imshow(cfg.WINDOW_NAME, frame)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    print("\nAnaliz tamamlandı. Final raporu oluşturuluyor...")
    reporter.generate(table.session_orders, table.performance_logs)
    print("Program başarıyla sonlandı.")

if __name__ == '__main__':
    main()