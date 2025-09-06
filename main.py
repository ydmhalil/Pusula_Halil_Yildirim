import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.decomposition import PCA


# Veri setini yükleme
df = pd.read_excel("C:\\Users\\PC\\Desktop\\Pusuala_Talent\\Talent_Academy_Case_DT_2025.xlsx")
    
# --- BASE VERİ SETİ DURUMU ---
print("\n--- Base Veri Seti İlk 5 Satır ---")
print(df.head())
print("\n--- Veri Seti Bilgisi (info) ---")
print(df.info())
print("\n--- Sayısal Sütunlar için Temel İstatistikler (describe) ---")
print(df.describe())
print("\n--- Eksik Değer Sayısı  ---")
print(df.isnull().sum())

    
# Yaş grubu değişkeni ekle
bins = [0, 18, 35, 50, 65, 100]
labels = ['Çocuk', 'Genç Yetişkin', 'Orta Yaş', 'Yaşlı', 'Emekli']
df['Yas_Grubu'] = pd.cut(df['Yas'], bins=bins, labels=labels, right=False)

# 1. EDA (Keşifçi Veri Analizi) Aşaması
def perform_advanced_eda(df_copy):
    """
    Veri setini daha derinlemesine inceleyen ve ilişkileri görselleştiren bir EDA fonksiyonu.
    """
    print("--- EDA: Veri Seti Yapısı ve İlişkiler ---")
    
    # 1.1 Yaş ve TedaviSuresi İlişkisi
    plt.figure(figsize=(12, 7))
    sns.scatterplot(x='Yas', y=df_copy['TedaviSuresi'].str.replace(' Seans', '').astype(float), data=df_copy)
    plt.title('Yaş ve Tedavi Süresi İlişkisi', fontsize=16)
    plt.xlabel('Yaş', fontsize=12)
    plt.ylabel('Tedavi Süresi (Seans)', fontsize=12)
    plt.show()

    # 1.2 Yaş Grupları ve Tedavi Süresi Dağılımı
    bins = [0, 18, 35, 50, 65, 100]
    labels = ['Çocuk', 'Genç Yetişkin', 'Orta Yaş', 'Yaşlı', 'Emekli']
    df_copy['Yas_Grubu'] = pd.cut(df_copy['Yas'], bins=bins, labels=labels, right=False)
    
    plt.figure(figsize=(12, 7))
    sns.boxplot(x='Yas_Grubu', y=df_copy['TedaviSuresi'].str.replace(' Seans', '').astype(float), data=df_copy)
    plt.title('Yaş Gruplarına Göre Tedavi Süresi', fontsize=16)
    plt.xlabel('Yaş Grubu', fontsize=12)
    plt.ylabel('Tedavi Süresi (Seans)', fontsize=12)
    plt.show()

    # 1.3 Kategorik Sütunların Korelasyon Isı Haritası
    # Sadece ilk 10 satır ile örnek bir gösterim
    categorical_df = df_copy[['Cinsiyet', 'KanGrubu', 'Bolum', 'TedaviAdi']].head(50)
    for col in categorical_df.columns:
        categorical_df[col] = pd.Categorical(categorical_df[col]).codes

    plt.figure(figsize=(10, 8))
    sns.heatmap(categorical_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Kategorik Sütunlar Arası Korelasyon (Örnek)', fontsize=16)
    plt.show()

    print("\n--- Gelişmiş Özellik Analizi Tamamlandı. ---\n")

# EDA'yı çalıştır
perform_advanced_eda(df.copy())

# ---------------------------------------------
# 2. Veri Ön İşleme Hattı (Pipeline) Aşaması
# ---------------------------------------------

# Hedef değişkeni temizleme
df['TedaviSuresi'] = df['TedaviSuresi'].str.replace(' Seans', '', regex=False).astype(int)

# Ek Özellik Mühendisliği (Pipeline dışında)
# Tedavi ve Tanıların eşleşip eşleşmediğini kontrol eden özellik
df['Tanilar_Tedavi_Eslesmesi'] = df.apply(
    lambda row: 1 if pd.notna(row['Tanilar']) and str(row['Tanilar']).lower() in str(row['TedaviAdi']).lower() else 0, axis=1
)

# Birden fazla tıbbi bölümle ilişkili olma sayısı
df['Bolum_Sayisi'] = df['Bolum'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) and x != '' else 0)

# Özel dönüştürücüler (önceki koddan aynen alındı)
class CustomDurationConverter(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.conversion_rates = {
            'Saniye': 1/60, 'Dakika': 1, 'Saat': 60
        }
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X_copy = X.copy()
        X_copy[['UygulamaSuresi_Numeric', 'UygulamaSuresi_Birim']] = X_copy['UygulamaSuresi'].str.split(' ', expand=True)
        X_copy['UygulamaSuresi_Numeric'] = pd.to_numeric(X_copy['UygulamaSuresi_Numeric']).fillna(0)
        X_copy['UygulamaSuresi_Numeric'] = X_copy.apply(
            lambda row: row['UygulamaSuresi_Numeric'] * self.conversion_rates.get(str(row['UygulamaSuresi_Birim']), 1), axis=1
        )
        return X_copy[['UygulamaSuresi_Numeric']]  # Sadece sayısal sütunu döndür

class MultiValueOneHotEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
        self.unique_values = {}
    def fit(self, X, y=None):
        for col in self.columns:
            all_values = X[col].dropna().str.split(',').explode().str.strip().unique()
            self.unique_values[col] = sorted(list(all_values))
        return self
    def transform(self, X):
        X_copy = X.copy()
        new_features = []
        for col in self.columns:
            # count sütunu
            count_col = X_copy[col].apply(lambda x: len(str(x).split(',')) if pd.notna(x) and x != '' else 0)
            count_col.name = f"{col}_count"
            new_features.append(count_col)
            # one-hot sütunları
            for val in self.unique_values[col]:
                onehot_col = X_copy[col].fillna('').str.contains(val, regex=False).astype(int)
                onehot_col.name = f"{col}_{val}"
                new_features.append(onehot_col)
        # Tüm yeni sütunları birleştir
        new_features_df = pd.concat(new_features, axis=1)
        # Orijinal çoklu değerli sütunları çıkar, yenileri ekle
        X_copy = X_copy.drop(columns=self.columns)
        X_copy = pd.concat([X_copy.reset_index(drop=True), new_features_df.reset_index(drop=True)], axis=1)
        return X_copy




# 1) Eksik değerleri doldurma

# Cinsiyet eksiklerini 'Bilinmiyor' ile doldur
df['Cinsiyet'] = df['Cinsiyet'].fillna('Bilinmiyor')
# Kan grubu eksiklerini doğrudan 'Bilinmiyor' yap
df['KanGrubu'] = df['KanGrubu'].fillna('Bilinmiyor')
# Tanilar: TedaviAdi'na göre doldur
df['Tanilar'] = df['Tanilar'].fillna(
        df.groupby(['TedaviAdi'])['Tanilar']
            .transform(lambda x: x.mode()[0] if not x.mode().empty else 'Bilinmiyor')
)
# Bolum: Tanilar'a göre doldur
df['Bolum'] = df['Bolum'].fillna(
        df.groupby(['Tanilar'])['Bolum']
            .transform(lambda x: x.mode()[0] if not x.mode().empty else 'Bilinmiyor')
)

# KronikHastalik: Aynı cinsiyet, bolum ve tanilar'a göre doldur
df['KronikHastalik'] = df['KronikHastalik'].fillna(
        df.groupby(['Cinsiyet', 'Bolum', 'Tanilar'])['KronikHastalik']
            .transform(lambda x: x.mode()[0] if not x.mode().empty else 'Yok')
)
# UygulamaYeri: Tanilar ve TedaviAdi'na göre doldur
df['UygulamaYerleri'] = df['UygulamaYerleri'].fillna(
        df.groupby(['Tanilar', 'TedaviAdi'])['UygulamaYerleri']
            .transform(lambda x: x.mode()[0] if not x.mode().empty else 'Bilinmiyor')
)
# Alerji eksiklerini yine 'Yok' ile doldur
df['Alerji'] = df['Alerji'].fillna('Yok')



# 2) Güçlü değişken çiftleri için etkileşim sütunları ekle
df['Cinsiyet_Bolum'] = df['Cinsiyet'].astype(str) + '_' + df['Bolum'].astype(str)
df['KanGrubu_Bolum'] = df['KanGrubu'].astype(str) + '_' + df['Bolum'].astype(str)
df['Bolum_TedaviAdi'] = df['Bolum'].astype(str) + '_' + df['TedaviAdi'].astype(str)

# 3) Aykırı ve tutarsız değerleri kontrol et ve sil
# Örnek: Yaş 0 veya 100'den büyük, TedaviSuresi 0 veya çok büyük olanlar
df = df[(df['Yas'] > 0) & (df['Yas'] < 100)]
df = df[(df['TedaviSuresi'] > 0) & (df['TedaviSuresi'] < 100)]

# 4) Hedef değişkenin dağılımını inceleme ve log-transform uygulama
plt.figure(figsize=(8,5))
sns.histplot(df['TedaviSuresi'], bins=30, kde=True)
plt.title('Tedavi Süresi Dağılımı (Orijinal)')
plt.show()

# Log-transform (log1p, sıfır ve negatifleri engeller)
df['TedaviSuresi_log'] = np.log1p(df['TedaviSuresi'])
plt.figure(figsize=(8,5))
sns.histplot(df['TedaviSuresi_log'], bins=30, kde=True)
plt.title('Tedavi Süresi Dağılımı (Log-Transform)')
plt.show()

# Pipeline bileşenlerini güncelleme
numerical_features = ['Yas', 'Tanilar_Tedavi_Eslesmesi', 'Bolum_Sayisi']
numerical_pipeline = Pipeline(steps=[
    ('imputer', IterativeImputer(max_iter=10, random_state=0)),
    ('scaler', StandardScaler())
])

categorical_features = ['Cinsiyet', 'KanGrubu', 'Uyruk', 'Bolum', 'TedaviAdi', 'Cinsiyet_Bolum', 'KanGrubu_Bolum', 'Bolum_TedaviAdi', 'Yas_Grubu']
categorical_pipeline = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

duration_pipeline = Pipeline(steps=[
    ('duration_converter', CustomDurationConverter())
])

multi_value_features = ['KronikHastalik', 'Alerji', 'Tanilar', 'UygulamaYerleri']
multi_value_pipeline = Pipeline(steps=[
    ('multi_value_encoder', MultiValueOneHotEncoder(multi_value_features)),
    ('pca', PCA(n_components=0.95))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_pipeline, numerical_features),
        ('cat', categorical_pipeline, categorical_features),
        ('duration', duration_pipeline, ['UygulamaSuresi']),
        ('multival', multi_value_pipeline, multi_value_features)
    ],
    remainder='drop'
)

# Nihai pipeline'ı veriye uygulama
X = df.drop(columns=['TedaviSuresi', 'TedaviSuresi_log', 'HastaNo'])
y = df['TedaviSuresi_log']

processed_data = preprocessor.fit_transform(X, y)

print("--- Veri ön işleme tamamlandı. ---")
print(f"Orijinal özellik sayısı: {X.shape[1]}")
print(f"İşlenmiş veri boyutu: {processed_data.shape}")