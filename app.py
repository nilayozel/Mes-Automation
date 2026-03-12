from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- 1. VERİTABANI AYARLARI ---
# Projenin çalıştığı klasör yolunu belirler
basedir = os.path.abspath(os.path.dirname(__file__))
# SQLite veritabanı dosyasının yolunu tanımlar (mes_database.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mes_database.db')
# Gereksiz bellek kullanımını önlemek için takip özelliğini kapatır
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Flask uygulaması ile SQLAlchemy veritabanı motorunu birbirine bağlar
db = SQLAlchemy(app)

# --- 2. SQL TABLO MODELİ ---
# Veritabanında 'urun' tablosunu ve sütunlarını oluşturur (ORM yapısı)
class Urun(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Her kayıt için otomatik artan benzersiz kimlik
    seri_no = db.Column(db.String(50), unique=True, nullable=False) # Ürünün benzersiz seri numarası
    model = db.Column(db.String(100), nullable=False) # Cihaz modeli (Reno 11, A60 vb.)
    durum = db.Column(db.String(100), default="Yeni Giris") # Üretim aşaması (SMT, Paketleme vb.)

# --- 3. VERİTABANINI OLUŞTURMA ---
with app.app_context():
    # Tanımlanan modelleri kullanarak fiziksel .db dosyasını oluşturur
    db.create_all()
    # Eğer tablo tamamen boşsa, sistemi test etmek için 3 örnek veri ekler
    if not Urun.query.first():
        db.session.add(Urun(seri_no="OPPO-001", model="Reno 11", durum="Tamamlandi"))
        db.session.add(Urun(seri_no="OPPO-002", model="A60", durum="Montajda"))
        db.session.add(Urun(seri_no="OPPO-003", model="Find X8", durum="Yeni Giris"))
        db.session.commit() # Değişiklikleri veritabanına kaydeder

# API güvenliği için kullanılan statik anahtar (Örn: Genel Merkez erişimi için)
GIZLI_API_KEY = "OPPO-FACTORY-2026-SECRET"

# --- 4. API ENDPOINT (GENEL MERKEZ İÇİN) ---
@app.route('/genel-merkez/uretim-raporu', methods=['GET'])
def get_factory_report():
    # Gelen isteğin başlığındaki (Headers) API anahtarını kontrol eder
    gelen_anahtar = request.headers.get('X-API-KEY')
    if gelen_anahtar == GIZLI_API_KEY:
        # Yetki onaylandıysa SQL'deki tüm ürünleri çekip JSON listesine dönüştürür
        urunler = Urun.query.all()
        veri_listesi = [{"id": u.id, "seri_no": u.seri_no, "model": u.model, "durum": u.durum} for u in urunler]
        
        return jsonify({
            "fabrika_adi": "Istanbul MES Merkezi",
            "veriler": veri_listesi,
            "mesaj": "Veri erişimi onaylandı."
        }), 200
    # Anahtar yanlışsa erişimi reddeder
    return jsonify({"hata": "Yetkisiz Erişim"}), 401

# --- 5. YENİ ÜRÜN EKLEME (POST) ---
@app.route('/products', methods=['POST'])
def add_product():
    # İstekten gelen JSON verisini Python sözlüğüne çevirir
    veri = request.get_json()
    
    # Gelen verilere göre yeni bir veritabanı objesi oluşturur
    yeni_urun = Urun(
        seri_no=veri['seri_no'],
        model=veri['model'],
        durum=veri.get('durum', 'Yeni Giris')
    )
    
    try:
        db.session.add(yeni_urun) # Veriyi ekle
        db.session.commit() # Veritabanına işle
        return jsonify({"mesaj": f"{yeni_urun.seri_no} başarıyla SQL'e kaydedildi!"}), 201
    except Exception as e:
        db.session.rollback() # Hata olursa (Örn: Aynı seri no) işlemi iptal et
        return jsonify({"hata": "Veri kaydedilemedi. Seri numarası benzersiz olmalı!"}), 400

# --- 6. ÜRÜN GÜNCELLEME (PATCH) ---
@app.route('/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    # Belirtilen ID'ye sahip ürünü arar
    urun = Urun.query.get(product_id)
    if not urun:
        return jsonify({"hata": "Ürün bulunamadı!"}), 404
    
    # Sadece 'durum' alanını günceller (Üretim aşaması değişikliği)
    veri = request.get_json()
    if 'durum' in veri:
        urun.durum = veri['durum']
    
    db.session.commit()
    return jsonify({"mesaj": f"ID: {product_id} güncellendi.", "yeni_durum": urun.durum}), 200 

# --- 7. ÜRÜN SİLME (DELETE) ---
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    urun = Urun.query.get(product_id)
    if not urun:
        return jsonify({"hata": "Ürün bulunamadı!"}), 404
    
    try:
        db.session.delete(urun) # Kaydı sil
        db.session.commit()
        return jsonify({"mesaj": f"ID {product_id} olan ürün başarıyla silindi."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"hata": "Ürün silinemedi!"}), 500
        
# --- 8. DASHBOARD (GÖRSEL ARAYÜZ) ---
@app.route('/dashboard')
def dashboard():
    # Tüm tabloyu çeker ve durumlarına göre sayısal analiz yapar
    urunler = Urun.query.all()
    toplam = len(urunler)
    tamamlanan = len([u for u in urunler if u.durum == 'Tamamlandi'])
    montajda = len([u for u in urunler if u.durum == 'Montajda'])
    paketleme = len([u for u in urunler if u.durum == 'Paketleme'])
    smt = len([u for u in urunler if u.durum == 'SMT'])
    
    # Analiz sonuçlarını HTML şablonuna (dashboard.html) gönderir
    return render_template('dashboard.html', 
                           toplam=toplam, 
                           tamamlanan=tamamlanan, 
                           montajda=montajda, 
                           paketleme=paketleme, 
                           smt=smt)

if __name__ == '__main__':
    # Sunucuyu geliştirici modunda (canlı yenileme aktif) başlatır
    app.run(debug=True)