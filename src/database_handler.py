# src/database_handler.py
import sqlite3
import datetime
from config import Config

DB_FILE = "restoran_veritabani.db" # Ana klasörde oluşacak

class DatabaseHandler:
    def __init__(self, db_file=DB_FILE):
        """Veritabanı bağlantısını kurar."""
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def setup_tables(self):
        """Gerekli tabloları (eğer yoksa) oluşturur."""
        # Siparişlerin detaylı kaydı
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS siparisler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                garson_adi TEXT NOT NULL,
                urun_adi TEXT NOT NULL,
                fiyat REAL NOT NULL,
                tarih TIMESTAMP NOT NULL
            )
        ''')
        # Garson performans olaylarının kaydı
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS performans_loglari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                garson_adi TEXT NOT NULL,
                olay_tipi TEXT NOT NULL, -- 'GECIKME', 'ZAMANINDA_MUDALE', 'HESAP_KAPAMA'
                detay TEXT,
                tarih TIMESTAMP NOT NULL
            )
        ''')
        self.conn.commit()

    def add_order(self, garson_adi, urun_adi, fiyat):
        """Veritabanına yeni bir sipariş ekler."""
        timestamp = datetime.datetime.now()
        self.cursor.execute(
            "INSERT INTO siparisler (garson_adi, urun_adi, fiyat, tarih) VALUES (?, ?, ?, ?)",
            (garson_adi, urun_adi, fiyat, timestamp)
        )
        self.conn.commit()

    def log_performance_event(self, garson_adi, olay_tipi, detay=""):
        """Veritabanına bir performans olayı kaydeder."""
        timestamp = datetime.datetime.now()
        self.cursor.execute(
            "INSERT INTO performans_loglari (garson_adi, olay_tipi, detay, tarih) VALUES (?, ?, ?, ?)",
            (garson_adi, olay_tipi, detay, timestamp)
        )
        self.conn.commit()

    def get_all_orders_as_dataframe(self):
        """Tüm siparişleri bir pandas DataFrame olarak döndürür."""
        import pandas as pd
        return pd.read_sql_query("SELECT * FROM siparisler", self.conn)

    def get_all_performance_logs_as_dataframe(self):
        """Tüm performans loglarını bir pandas DataFrame olarak döndürür."""
        import pandas as pd
        return pd.read_sql_query("SELECT * FROM performans_loglari", self.conn)

    def close_connection(self):
        """Veritabanı bağlantısını kapatır."""
        self.conn.close()