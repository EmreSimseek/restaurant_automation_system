# src/report_generator.py

import pandas as pd
import matplotlib.pyplot as plt

class ReportGenerator:
    """Video sonunda sipariş ve performans raporlarını görselleştirir."""
    def generate(self, session_orders, performance_logs):
        if not session_orders:
            print("Rapor oluşturulacak sipariş verisi bulunamadı.")
            return

        order_df = pd.DataFrame(session_orders)
        perf_df = pd.DataFrame(performance_logs)

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(18, 12))
        fig.suptitle('Final Raporu', fontsize=20, fontweight='bold')

        # 1. Garson Bazlı Ciro
        waiter_revenue = order_df.groupby('garson')['fiyat'].sum()
        waiter_revenue.plot(kind='bar', ax=axes[0, 0], color='c', rot=0)
        axes[0, 0].set_title('Garson Bazlı Toplam Ciro')
        axes[0, 0].set_ylabel('Ciro (TL)')

        # 2. En Çok Satan Ürünler
        product_sales = order_df['urun'].value_counts()
        product_sales.plot(kind='pie', ax=axes[0, 1], autopct='%1.1f%%', startangle=90)
        axes[0, 1].set_title('Satılan Ürünlerin Dağılımı')
        axes[0, 1].set_ylabel('')

        # 3. Garsonların Baktığı Toplam Hesap Sayısı
        if not perf_df.empty and 'event' in perf_df.columns:
            closed_accounts = perf_df[perf_df['event'] == 'HESAP_KAPAMA']['waiter'].value_counts()
            closed_accounts.plot(kind='bar', ax=axes[1, 0], color='m', rot=0)
            axes[1, 0].set_title('Garsonların Kapattığı Hesap Sayısı')
            axes[1, 0].set_ylabel('Hesap Adedi')

        # 4. Gecikme Sayıları
        if not perf_df.empty and 'event' in perf_df.columns:
            late_responses = perf_df[perf_df['event'] == 'GECIKME']['waiter'].value_counts()
            late_responses.plot(kind='bar', ax=axes[1, 1], color='r', rot=0)
            axes[1, 1].set_title('Garson Gecikme Sayıları')
            axes[1, 1].set_ylabel('Gecikme Adedi')
        else:
            axes[1, 1].text(0.5, 0.5, 'Gecikme Kaydı Yok', ha='center', va='center', fontsize=12)


        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()