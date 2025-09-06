# EDA ve Veri Ön İşleme Özeti

## 1. Keşifçi Veri Analizi (EDA) Bulguları

- **Veri seti boyutu:** 2235 gözlem, 13 ana değişken
- **Eksik değerler:**
  - Cinsiyet, KanGrubu, KronikHastalik, Bolum, Alerji, Tanilar ve UygulamaYerleri değişkenlerinde eksikler mevcut.
  - Özellikle Alerji ve KanGrubu'nda eksik oranı yüksek.
- **Kategorik değişkenler:**
  - Cinsiyet, KanGrubu, Uyruk, Bolum, TedaviAdi gibi değişkenler çeşitli kategoriler içeriyor.
- **Çoklu değerli değişkenler:**
  - KronikHastalik, Alerji, Tanilar, UygulamaYerleri gibi değişkenler birden fazla değeri virgül ile ayırarak tutabiliyor.
- **Hedef değişken:**
  - TedaviSuresi, orijinalde string (örn. "12 Seans"), sayısala çevrildi ve log-transform uygulandı.
- **Yaş grupları:**
  - Yaş değişkeni, Çocuk, Genç Yetişkin, Orta Yaş, Yaşlı, Emekli olarak gruplandırıldı.

## 2. Veri Ön İşleme Adımları

1. **Eksik Değer Doldurma:**
   - Cinsiyet: Eksikler "Bilinmiyor" ile dolduruldu.
   - KanGrubu: Eksikler "Bilinmiyor" ile dolduruldu.
   - Tanilar: Eksikler, aynı TedaviAdi'na sahip satırların mod değeriyle dolduruldu.
   - Bolum: Eksikler, aynı Tanilar'a sahip satırların mod değeriyle dolduruldu.
   - KronikHastalik: Eksikler, aynı Cinsiyet, Bolum ve Tanilar'a göre dolduruldu.
   - UygulamaYerleri: Eksikler, aynı Tanilar ve TedaviAdi'na göre dolduruldu.
   - Alerji: Eksikler "Yok" ile dolduruldu.

2. **Özellik Mühendisliği:**
   - Tedavi ve Tanıların eşleşip eşleşmediğini gösteren binary değişken oluşturuldu.
   - Birden fazla bölümle ilişkili olma sayısı çıkarıldı.
   - Cinsiyet_Bolum, KanGrubu_Bolum, Bolum_TedaviAdi gibi etkileşim değişkenleri eklendi.
   - Yaş grubu kategorik değişken olarak eklendi.

3. **Hedef Değişken Dönüşümü:**
   - TedaviSuresi sayısala çevrildi ve log1p ile log-transform uygulandı.

4. **Pipeline ile Ön İşleme:**
   - Sayısal değişkenler: IterativeImputer ile eksik doldurma, StandardScaler ile ölçekleme.
   - Kategorik değişkenler: OneHotEncoder ile kodlama.
   - Süre değişkeni: CustomDurationConverter ile dakikaya çevrildi.
   - Çoklu değerli değişkenler: MultiValueOneHotEncoder ile one-hot kodlama ve PCA ile boyut indirgeme.

## 3. Sonuç
- Tüm eksik değerler uygun şekilde dolduruldu.
- Sayısal ve kategorik değişkenler modellemeye uygun hale getirildi.
- Veri seti, makine öğrenmesi modelleri için hazır ve temiz bir formata dönüştürüldü.

---
