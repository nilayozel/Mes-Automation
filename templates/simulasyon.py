import requests
import random

# Veri girişi yapılacak hedef API adresi
URL = "http://127.0.0.1:5000/products"

# Fabrika simülasyonu için kullanılacak havuz veriler
modeller = ["Reno 11", "A60", "Find X8", "Reno 12 Pro", "A78", "Find N3"]
durumlar = ["SMT", "Montajda", "Paketleme", "Tamamlandi"]

print("🚀 500 adet veri simüle ediliyor...")

for i in range(1, 501):
    # Her döngüde benzersiz seri numaralı rastgele bir ürün oluşturur
    veri = {
        "seri_no": f"OPPO-PROD-{1000 + i}",
        "model": random.choice(modeller),
        "durum": random.choice(durumlar)
    }
    
    try:
        # Sunucuya POST isteği atarak kaydı gerçekleştirir
        response = requests.post(URL, json=veri)
        if response.status_code == 201 and i % 100 == 0:
            print(f"📈 {i} ürün bariyeri aşıldı...")
    except Exception as e:
        print(f"🚨 Bağlantı kesildi: {e}")
        break

print("🏁 Simülasyon bitti. Dashboard güncellendi!")