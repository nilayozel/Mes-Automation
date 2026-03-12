# 🏭 OPPO MES: End-to-End Production Tracking & Analytical Reporting System

Bu proje, bir akıllı telefon üretim hattındaki süreçleri (SMT, Montaj, Paketleme) uçtan uca takip eden, verileri SQL veritabanında saklayan ve anlık olarak görselleştiren bir **Üretim Yürütme Sistemi (MES)** prototipidir.

![OPPO MES Dashboard](https://github.com/nilayozel/Mes-Automation/blob/main/dashboard.png) 

## 🎯 Projenin Amacı
Üretim sahasından gelen verileri manuel takipten kurtarıp, dijital bir ekosisteme taşımak amaçlanmıştır. Bu sistem sayesinde:
* **Anlık İzlenebilirlik:** Üretimdeki darboğazlar canlı grafiklerle izlenir.
* **Veri Güvenliği:** Veriler ilişkisel bir SQL (SQLite) yapısında depolanır.
* **Veri Analitiği & Raporlama:** **`merkez_rapor.py`** üzerinden tüm üretim geçmişi dışa aktarılabilir (CSV/Excel). Bu verilerle Verimlilik (OEE) ve Kalite analizleri yapılabilir.
* **Entegrasyon:** Genel merkez gibi dış birimler için API Key tabanlı güvenli raporlama sunulur.

---

## 🛠️ Kullanılan Teknolojiler & Kütüphaneler

Sistemin mimarisi aşağıdaki teknolojiler üzerine kurulmuştur:
* **Backend:** Python & Flask (API ve Sunucu yönetimi)
* **Database:** SQLAlchemy & SQLite (İlişkisel Veritabanı Yönetimi)
* **Frontend:** HTML5, Bootstrap 5 (Responsive Arayüz Tasarımı)
* **Visualization:** Chart.js (Dinamik Pasta Grafik)
* **Tools:** Python Requests (Veri Simülasyonu ve API Testi)

---

## 🚀 Kurulum ve Çalıştırma Rehberi (Yeni Başlayanlar İçin)

Aşağıdaki adımları sırayla takip ederek sistemi kendi bilgisayarınızda saniyeler içinde ayağa kaldırabilirsiniz:

### 1. Projeyi Bilgisayarınıza İndirin
```bash
git clone [https://github.com/NilayOzel/Mes-Automation.git](https://github.com/NilayOzel/Mes-Automation.git)
cd Mes-Automation
```

### 2. Gerekli Kütüphaneleri Yükleyin
Sistemin çalışması için gereken tüm araçları tek komutla kurun:
```bash
pip install -r requirements.txt
```

### 3. Ana Sunucuyu Başlatın (Backend)
Bu komut veritabanını otomatik olarak oluşturacak ve fabrikayı "çalışır" duruma getirecektir:
```bash
python app.py
```
Terminalde Running on http://127.0.0.1:5000 mesajını gördüğünüzde her şey hazır demektir.

### 4. Veri Simülasyonunu Çalıştırın
Dashboard'un dolması ve sistemin yük altındaki performansını görmek için 500 adet örnek ürünü sisteme gönderin:
(Yeni bir terminal penceresi açıp klasöre giderek çalıştırın)
```bash
python simulasyon.py
```

---

## 📊 Dashboard'u Görüntüleme
Her şey çalışırken tarayıcınızı açın ve şu adrese gidin:
👉 **[http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard)**

Bu sayfada üretim hattındaki SMT, Montaj ve Paketleme aşamalarındaki ürün dağılımını canlı olarak izleyebilirsiniz.

---

## 📂 Dosya Yapısı ve Görevleri

Proje klasöründeki dosyaların görevleri aşağıda detaylandırılmıştır:

* **`app.py`**: Projenin ana kontrol merkezidir. Flask sunucusunu ayağa kaldırır, SQLite veritabanı bağlantısını kurar ve API uç noktalarını (Endpoints) yönetir.
* **`simulasyon.py`**: Üretim hattından anlık veri akışı geliyormuş gibi sisteme rastgele 500 adet ürün kaydı gönderen test scriptidir.
* **`merkez_rapor.py`**:  **Projenin analitik bacağıdır.** API üzerinden fabrikanın güncel verilerini çeker ve yönetimsel analizler için zaman damgalı bir **Excel (CSV)** raporu üretir.
* **`templates/dashboard.html`**: Kullanıcıların canlı veriyi pasta grafiği (Pie Chart) üzerinden izlediği, Bootstrap destekli görsel arayüz dosyasıdır.
* **`requirements.txt`**: Projenin herhangi bir bilgisayarda sorunsuz çalışması için gerekli kütüphane listesini içerir.

---


## 📧 İletişim ve Geliştirici
Bu proje, veri odaklı üretim sistemleri ve otomasyon üzerine bir çalışma olarak **Nilay Özel** tarafından geliştirilmiştir.

* **LinkedIn:** [linkedin.com/in/nilayozel](https://www.linkedin.com/in/nilay-özel-2927a7210/)
* **GitHub:** [@NilayOzel](https://github.com/nilayozel)

---
*Bu proje açık kaynaklıdır ve geliştirilmeye açıktır. Katkıda bulunmak isterseniz bir Pull Request gönderebilirsiniz.*
