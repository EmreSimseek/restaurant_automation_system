# src/table_manager.py

import time
from collections import Counter
from config import Config
from src.database_handler import DatabaseHandler # DB sınıfını import et

class TableManager:
    def __init__(self, db_handler: DatabaseHandler):
        self.db = db_handler # DatabaseHandler nesnesini al
        self.state = "EMPTY"
        self.active_waiter = None
        self.items_on_table = Counter()
        self.current_bill = 0.0
        self.customer_arrival_time = None
        self.last_waiter_id = None
        
        # Artık bu listelere gerek yok, veriler doğrudan DB'ye gidecek.
        # self.session_orders = []
        # self.performance_logs = []

    def update(self, detected_items, qr_data_list):
        # ... (Bu metodun geri kalanı aynı kalır) ...
        pass

    def _add_new_order(self, item_name):
        price = Config.FOOD_PRICES.get(item_name, 0.0)
        self.current_bill += price
        # Veriyi listeye eklemek yerine, doğrudan veritabanına yaz:
        self.db.add_order(self.active_waiter, item_name, price)
        print(f"SİPARİŞ (DB'ye yazıldı): {item_name} - Garson: {self.active_waiter}")

    def _waiter_arrived(self):
        response_time = time.time() - self.customer_arrival_time
        # Performans olayını doğrudan veritabanına logla:
        self.db.log_performance_event(
            self.active_waiter, 
            "ZAMANINDA_MUDALE", 
            f"{response_time:.2f} sn'de geldi."
        )
        self.state = "BEING_SERVED"
        print(f"BİLGİ: Garson {self.active_waiter} masaya geldi.")

    def _reset_table(self):
        print(f"HESAP KAPANDI: Toplam Tutar = {self.current_bill:.2f} TL")
        if self.last_waiter_id:
            # Hesap kapama olayını logla:
            self.db.log_performance_event(
                self.last_waiter_id, 
                "HESAP_KAPAMA", 
                f"Hesap: {self.current_bill:.2f} TL"
            )
        # Anlık durumları sıfırla
        self.state = "EMPTY"
        self.active_waiter = None
        self.items_on_table = Counter()
        self.current_bill = 0.0
        self.customer_arrival_time = None

    # Diğer metodlar (_customer_arrived vb.) aynı kalır, sadece print mesajları içerirler.