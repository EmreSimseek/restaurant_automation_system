# src/display_panel.py

import cv2
import numpy as np
from collections import Counter
from config import Config
from src.table_manager import TableManager

class DisplayPanel:
    """Anlık bilgileri profesyonel bir arayüzle ekrana çizer."""
    def draw(self, frame, manager: TableManager):
        self._draw_background(frame)
        self._draw_header(frame)
        self._draw_table_status(frame, manager)
        self._draw_waiter_info(frame, manager)
        self._draw_order_summary(frame, manager)

    def _draw_background(self, frame):
        panel_area = frame[0:frame.shape[0], Config.PANEL_START_X:frame.shape[1]]
        black_rect = np.zeros(panel_area.shape, dtype=np.uint8)
        res = cv2.addWeighted(panel_area, 0.4, black_rect, 0.6, 1.0)
        frame[0:frame.shape[0], Config.PANEL_START_X:frame.shape[1]] = res

    def _draw_header(self, frame):
        self._put_text(frame, "YONETIM PANELI", (Config.PANEL_START_X + 20, 40), 0.8, Config.COLOR_YELLOW)

    def _draw_table_status(self, frame, manager: TableManager):
        state_color_map = {
            "EMPTY": Config.COLOR_GREEN, "WAITING_FOR_WAITER": Config.COLOR_YELLOW,
            "BEING_SERVED": Config.COLOR_BLUE, "NEEDS_ATTENTION": Config.COLOR_RED
        }
        color = state_color_map.get(manager.state, Config.COLOR_WHITE)
        self._put_text(frame, f"Masa Durumu: {manager.state}", (Config.PANEL_START_X + 20, 80), color=color, thick=2)
    
    def _draw_waiter_info(self, frame, manager: TableManager):
        waiter = manager.active_waiter or manager.last_waiter_id or "Yok"
        text = f"Servis Yapan: {waiter}"
        self._put_text(frame, text, (Config.PANEL_START_X + 20, 110))

    def _draw_order_summary(self, frame, manager: TableManager):
        self._put_text(frame, "Hesap Ozeti:", (Config.PANEL_START_X + 20, 160), color=Config.COLOR_YELLOW)
        y_pos = 190
        
        current_orders = Counter(item['urun'] for item in manager.session_orders)
        if manager.state == "EMPTY": # Hesap kapandıysa, sipariş listesini boşalt
            current_orders.clear()

        for item, count in current_orders.items():
            price = Config.FOOD_PRICES.get(item, 0)
            text = f"- {item} (x{count}) = {price * count:.2f} TL"
            self._put_text(frame, text, (Config.PANEL_START_X + 30, y_pos), 0.55)
            y_pos += 30
        
        cv2.line(frame, (Config.PANEL_START_X, y_pos + 10), (frame.shape[1], y_pos + 10), Config.COLOR_YELLOW, 1)
        bill_text = f"TOPLAM: {manager.current_bill:.2f} TL"
        self._put_text(frame, bill_text, (Config.PANEL_START_X + 20, y_pos + 40), 0.9, Config.COLOR_GREEN)

    def _put_text(self, frame, text, org, scale=0.6, color=Config.COLOR_WHITE, thick=1):
        cv2.putText(frame, text, org, cv2.FONT_HERSHEY_DUPLEX, scale, color, thick, cv2.LINE_AA)