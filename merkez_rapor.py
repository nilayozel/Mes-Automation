import requests
import csv
from datetime import datetime

# Fabrika API'sinin adresi ve güvenlik anahtarı
API_URL = "http://127.0.0.1:5000/genel-merkez/uretim-raporu"
HEADERS = {"X-API-KEY": "OPPO-FACTORY-2026-SECRET"}

def raporu_getir_ve_excel_yap():
    try:
        # API'ye şifreli GET isteği gönderir
        yanit = requests.get(API_URL, headers=HEADERS)

        if yanit.status_code == 200:
            veri = yanit.json()
            urunler = veri['veriler']
            
            # Zaman damgalı benzersiz dosya adı oluşturur (Excel uyumlu CSV)
            zaman_etiketi = datetime.now().strftime("%Y%m%d_%H%M")
            dosya_adi = f"rapor_{zaman_etiketi}.csv"

            # Verileri CSV dosyasına satır satır yazar
            with open(dosya_adi, mode='w', newline='', encoding='utf-8-sig') as dosya:
                yazici = csv.writer(dosya)
                yazici.writerow(['ID', 'Seri No', 'Model', 'Durum', 'Rapor Tarihi']) # Sütun başlıkları
                
                for urun in urunler:
                    yazici.writerow([
                        urun['id'], 
                        urun['seri_no'], 
                        urun['model'], 
                        urun['durum'],
                        datetime.now().strftime("%Y-%m-%d %H:%M")
                    ])
            print(f"✅ İşlem Başarılı: {dosya_adi} oluşturuldu.")
        else:
            print(f"❌ Hata: Yetki sorunu veya sunucu yanıt vermiyor. Kod: {yanit.status_code}")

    except Exception as e:
        print(f"⚠️ Beklenmedik Hata: {e}")

if __name__ == "__main__":
    raporu_getir_ve_excel_yap()