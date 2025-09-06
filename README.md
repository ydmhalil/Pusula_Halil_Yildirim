# Pusuala Talent Veri Hazırlama Pipeline'ı

**Ad:** Halil  
**Soyad:** Yıldırım  
**E-posta:** ydmhalil@gmail.com

---

## Genel Bakış
Bu proje, "Talent Academy Case DT 2025" veri seti için sağlam bir veri hazırlama ve ön işleme pipeline'ı sunar. Pipeline; gelişmiş veri temizleme, özellik mühendisliği, eksik değer doldurma, kategorik ve çoklu değerli değişkenlerin kodlanması ve aykırı değer işlemlerini içerir. Kod, sağlık/rehabilitasyon verileri için tasarlanmıştır ve makine öğrenmesi süreçlerinde kullanılmaya hazırdır.

## Proje Yapısı
- `main.py`: Verinin yüklenmesi, EDA, özellik mühendisliği ve ön işleme pipeline'ı için ana script.
- `Talent_Academy_Case_DT_2025.xlsx`: Ham veri dosyası (repo içinde yoktur).
- `requirements.txt`: Python bağımlılıkları.


## Nasıl Çalıştırılır?
1. Bu repoyu kendi bilgisayarınıza klonlayın.
2. Ham veri dosyasını (`Talent_Academy_Case_DT_2025.xlsx`) proje ana dizinine yerleştirin.
3. (Opsiyonel) Bir Python sanal ortamı oluşturup aktive edin:
   ```bash
   python -m venv PusulaVenv
   PusulaVenv\Scripts\activate  # Windows
   # source PusulaVenv/bin/activate  # Linux/Mac
   ```
4. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
5. Ana scripti çalıştırın:
   ```bash
   python main.py
   ```

## Çıktılar
- Script, EDA özetlerini ekrana basar ve işlenmiş veriyi bellekte tutar (isteğe bağlı olarak CSV olarak kaydedilebilir).
- Hedef değişkenin dağılımı (orijinal ve log-transform) için grafikler gösterilir.

## Notlar
- Pipeline, eksik değerler, aykırı değerler ve karmaşık kategorik/çoklu değerli değişkenleri otomatik olarak işler.

---

