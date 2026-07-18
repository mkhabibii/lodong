# Rencana Revisi Notebook Klasifikasi Lowongan Kerja Asli dan Palsu

## 1. Tujuan Dokumen

Dokumen ini berisi hasil evaluasi dan rancangan revisi terhadap notebook
**`Klasifikasi_Lowongan_Asli_Palsu.ipynb`**.

Revisi difokuskan pada peningkatan **validitas metodologi machine
learning**, **kualitas evaluasi model**, dan **kesiapan model untuk
deployment**, dengan tetap mempertahankan batasan proyek:

> **Proyek tidak menggunakan Natural Language Processing (NLP).**

Artinya, revisi **tidak mencakup** TF-IDF, Bag of Words, analisis kata
kunci, Word2Vec, embedding, BERT, atau teknik pemahaman semantik teks
lainnya.

Fitur teks tetap digunakan hanya sebagai **fitur struktural**, misalnya:

-   panjang deskripsi;
-   panjang profil perusahaan;
-   panjang persyaratan;
-   panjang benefit;
-   keberadaan atau ketiadaan suatu informasi.

------------------------------------------------------------------------

# 2. Ringkasan Kondisi Notebook Saat Ini

Notebook saat ini telah memiliki alur CRISP-DM yang cukup jelas, yaitu:

1.  Data Understanding
2.  Exploratory Data Analysis (EDA)
3.  Data Preparation
4.  Modeling
5.  Evaluation
6.  Deployment
7.  Kesimpulan

Model yang dibandingkan adalah:

-   Logistic Regression;
-   Decision Tree;
-   Random Forest.

Dataset asli memiliki distribusi kelas yang tidak seimbang:

-   **Real / Asli:** sekitar 95,16%;
-   **Fake / Palsu:** sekitar 4,84%.

Pada notebook saat ini, ketidakseimbangan kelas ditangani dengan
**Random Undersampling sebelum Train-Test Split**, sehingga data
menjadi:

-   866 data asli;
-   866 data palsu;
-   total 1.732 data.

Setelah itu, dataset seimbang tersebut baru dibagi menjadi training set
dan testing set.

Random Forest kemudian memperoleh hasil sekitar:

-   Accuracy: 91,93%;
-   Precision Fake: 91,43%;
-   Recall Fake: 92,49%;
-   F1-Score Fake: 91,95%.

Hasil tersebut terlihat tinggi, tetapi masih terdapat beberapa hal
metodologis yang perlu diperbaiki agar performa model lebih valid dan
lebih mencerminkan kondisi ketika model menerima data baru dari
pengguna.

------------------------------------------------------------------------

# 3. Revisi Utama yang Perlu Dilakukan

## 3.1. Train-Test Split Harus Dilakukan Sebelum Penanganan Class Imbalance

### Kondisi Saat Ini

Alur notebook saat ini adalah:

``` text
Dataset Asli
    ↓
Feature Engineering
    ↓
Encoding
    ↓
Random Undersampling
    ↓
Dataset menjadi 50:50
    ↓
Train-Test Split
    ↓
Training dan Evaluation
```

Dengan skema tersebut, bukan hanya training set yang menjadi seimbang,
tetapi **testing set juga ikut menjadi seimbang 50:50**.

### Masalah

Testing set seharusnya digunakan sebagai simulasi data baru yang belum
pernah dilihat oleh model. Karena distribusi asli dataset adalah sekitar
95% lowongan asli dan 5% lowongan palsu, testing set yang dibuat 50:50
tidak lagi merepresentasikan kondisi asli dataset.

Akibatnya, hasil seperti F1-Score 91,95% belum dapat langsung dianggap
sebagai performa model pada kondisi data yang realistis.

### Revisi

Urutan yang lebih tepat:

``` text
Dataset Asli
    ↓
Feature Engineering
    ↓
Pisahkan X dan y
    ↓
Train-Test Split dengan stratify
    ↓
┌──────────────────────┬──────────────────────┐
│ Training Set         │ Testing Set          │
│                      │                      │
│ Boleh dilakukan      │ Tidak di-resampling  │
│ penanganan imbalance │ Tetap distribusi asli│
└──────────────────────┴──────────────────────┘
```

Contoh:

``` python
X = df_prepared.drop(columns=["fraudulent"])
y = df_prepared["fraudulent"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

### Alasan

Dengan cara ini:

-   model hanya belajar dari training set;
-   strategi balancing hanya memengaruhi proses training;
-   testing set tetap merepresentasikan distribusi asli;
-   evaluasi menjadi lebih realistis;
-   hasil model lebih dapat dipercaya untuk deployment.

### Prioritas

**WAJIB DIPERBAIKI.**

------------------------------------------------------------------------

# 4. Jangan Langsung Menggunakan Satu Strategi Class Imbalance

## Kondisi Saat Ini

Notebook langsung menggunakan:

``` text
Random Undersampling
```

dan membuang sebagian besar data lowongan asli.

Dari sekitar 17.014 lowongan asli, hanya 866 yang dipertahankan.

Artinya, sekitar 16 ribu data lowongan asli tidak digunakan untuk
training.

## Masalah

Data lowongan asli memiliki variasi yang sangat besar.

Contohnya, lowongan asli dapat memiliki kondisi seperti:

``` text
Logo perusahaan      : Tidak ada
Profil perusahaan    : Tidak ada
Benefit               : Tidak ada
Persyaratan           : Ada
Deskripsi             : Ada
Status                : ASLI
```

Lowongan seperti ini penting untuk dipelajari oleh model.

Jika sebagian besar data asli dibuang secara acak, model berpotensi
kehilangan contoh-contoh penting yang menunjukkan bahwa:

> Tidak adanya logo, profil perusahaan, benefit, atau informasi tertentu
> tidak otomatis berarti sebuah lowongan palsu.

Hal ini penting karena fitur seperti `has_company_logo`,
`has_company_profile`, dan fitur kelengkapan lainnya hanyalah
**indikator**, bukan aturan mutlak.

## Revisi yang Direkomendasikan

Gunakan tiga strategi eksperimen:

  Kode   Data Training           Penanganan Imbalance
  ------ ----------------------- ---------------------------
  A      Seluruh training data   Tanpa balancing
  B      Seluruh training data   `class_weight="balanced"`
  C      Training data saja      Random Undersampling

### Eksperimen A --- Original Data

Tujuan:

-   menjadi baseline;
-   mengetahui performa model tanpa intervensi class imbalance.

### Eksperimen B --- Class Weight

Tujuan:

-   mempertahankan seluruh data training;
-   memberikan penalti lebih besar terhadap kesalahan pada kelas
    minoritas.

Contoh:

``` python
RandomForestClassifier(
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
```

Strategi ini penting karena model tetap dapat mempelajari seluruh
variasi lowongan asli.

### Eksperimen C --- Random Undersampling

Tujuan:

-   menjadi pembanding terhadap metode yang digunakan pada notebook
    lama;
-   mengetahui apakah pengurangan kelas mayoritas benar-benar
    meningkatkan performa.

Namun, undersampling hanya dilakukan pada:

``` text
X_train dan y_train
```

bukan pada seluruh dataset.

## Mengapa Tidak Langsung Menambahkan Random Oversampling dan SMOTE?

Untuk scope proyek saat ini, tiga strategi sudah cukup kuat dan lebih
mudah dijelaskan.

SMOTE juga perlu digunakan dengan hati-hati pada data yang memiliki
kombinasi fitur:

-   biner;
-   kategorikal;
-   numerik.

Karena itu, Random Oversampling dan SMOTE dapat dijadikan **pengembangan
lanjutan**, bukan revisi utama.

### Prioritas

**SANGAT DIREKOMENDASIKAN.**

------------------------------------------------------------------------

# 5. Rancangan Eksperimen Model

Notebook menggunakan tiga algoritma:

1.  Logistic Regression;
2.  Decision Tree;
3.  Random Forest.

Ketiga algoritma tetap dapat dipertahankan.

Masing-masing model diuji dengan tiga strategi imbalance.

Dengan demikian:

``` text
3 Algoritma × 3 Strategi = 9 Eksperimen
```

Rancangan:

  Model                 Original   Class Weight   Undersampling
  --------------------- ---------- -------------- ---------------
  Logistic Regression   Ya         Ya             Ya
  Decision Tree         Ya         Ya             Ya
  Random Forest         Ya         Ya             Ya

Hasil dapat dirangkum dalam tabel:

  Model                 Strategi          Precision Fake   Recall Fake   F1 Fake   PR-AUC
  --------------------- --------------- ---------------- ------------- --------- --------
  Logistic Regression   Original                     ...           ...       ...      ...
  Logistic Regression   Class Weight                 ...           ...       ...      ...
  Logistic Regression   Undersampling                ...           ...       ...      ...
  Decision Tree         Original                     ...           ...       ...      ...
  Decision Tree         Class Weight                 ...           ...       ...      ...
  Decision Tree         Undersampling                ...           ...       ...      ...
  Random Forest         Original                     ...           ...       ...      ...
  Random Forest         Class Weight                 ...           ...       ...      ...
  Random Forest         Undersampling                ...           ...       ...      ...

Tujuan eksperimen bukan mencari skor paling tinggi secara sembarangan,
tetapi mencari model yang paling baik dalam menjaga keseimbangan antara:

-   mendeteksi lowongan palsu;
-   tidak terlalu sering menuduh lowongan asli sebagai palsu.

------------------------------------------------------------------------

# 6. Revisi Encoding Fitur Kategorikal

## Kondisi Saat Ini

Notebook menggunakan:

``` python
LabelEncoder
```

untuk:

-   `country`;
-   `employment_type`;
-   `required_experience`;
-   `required_education`;
-   `industry`;
-   `function`.

## Masalah

`LabelEncoder` menghasilkan representasi seperti:

``` text
Engineering = 0
Finance     = 1
Healthcare  = 2
IT          = 3
```

Padahal kategori tersebut tidak memiliki hubungan urutan matematis.

Untuk model berbasis pohon, dampaknya dapat lebih kecil dibandingkan
model linier, tetapi tetap kurang ideal.

Untuk Logistic Regression, angka kategori dapat diperlakukan sebagai
nilai numerik yang memiliki urutan.

## Revisi

Gunakan:

``` python
OneHotEncoder(
    handle_unknown="ignore"
)
```

melalui:

``` python
ColumnTransformer
```

Contoh konsep:

``` python
categorical_features = [
    "country",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)
```

## Keuntungan

-   kategori tidak dianggap memiliki urutan;
-   lebih tepat untuk Logistic Regression;
-   kategori baru saat deployment tidak langsung menyebabkan error;
-   preprocessing dapat disatukan dengan model.

### Prioritas

**DIREKOMENDASIKAN.**

------------------------------------------------------------------------

# 7. Gunakan Pipeline untuk Mencegah Ketidakkonsistenan

## Kondisi Saat Ini

Notebook menyimpan:

``` text
encoder_kategori.joblib
model_random_forest.joblib
```

secara terpisah.

Hal ini membuat aplikasi harus memastikan sendiri bahwa:

1.  feature engineering sama;
2.  missing value ditangani dengan cara yang sama;
3.  encoding sama;
4.  urutan kolom sama;
5.  model menerima struktur input yang sama.

## Risiko

Jika preprocessing pada aplikasi Streamlit berbeda sedikit saja dari
preprocessing notebook, prediksi dapat:

-   error;
-   salah urutan fitur;
-   menghasilkan prediksi yang tidak konsisten.

## Revisi

Gabungkan preprocessing dan model menggunakan:

``` python
Pipeline
```

Contoh konsep:

``` python
model_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])
```

Kemudian:

``` python
model_pipeline.fit(X_train, y_train)
```

dan simpan:

``` python
joblib.dump(
    model_pipeline,
    "../models/model_pipeline.joblib"
)
```

Pada deployment:

``` python
model = joblib.load(
    "../models/model_pipeline.joblib"
)

prediction = model.predict(input_data)
```

### Prioritas

**SANGAT DIREKOMENDASIKAN UNTUK DEPLOYMENT.**

------------------------------------------------------------------------

# 8. Feature Engineering Tetap Non-NLP

Revisi tidak mengubah scope proyek menjadi NLP.

Fitur yang sudah digunakan dan tetap dipertahankan:

## Fitur Biner

``` text
telecommuting
has_company_logo
has_questions
has_company_profile
has_requirements
has_benefits
```

## Fitur Numerik Struktural

``` text
description_length
requirements_length
benefits_length
company_profile_length
```

## Fitur Kategorikal

``` text
country
employment_type
required_experience
required_education
industry
function
```

Pendekatan ini tetap termasuk machine learning tabular karena model
tidak membaca atau memahami makna teks.

------------------------------------------------------------------------

# 9. Fitur Tambahan yang Masih Sesuai Scope Non-NLP

Beberapa informasi yang sudah dianalisis pada EDA dapat dipertimbangkan
menjadi fitur model.

Namun, fitur baru sebaiknya diuji dan tidak otomatis dianggap
meningkatkan model.

## 9.1. `has_salary_range`

Saat ini `salary_range` dibuang karena sekitar 84% data kosong.

Daripada menggunakan isi rentang gaji, cukup gunakan keberadaan
informasinya:

``` python
df_prepared["has_salary_range"] = (
    df["salary_range"]
    .notna()
    .astype(int)
)
```

Fitur ini tidak menganalisis isi teks dan masih sesuai scope non-NLP.

------------------------------------------------------------------------

## 9.2. `has_department`

Karena `department` memiliki missing value tinggi dan cardinality besar,
isi kategorinya tidak harus digunakan.

Namun, keberadaan informasinya dapat diuji:

``` python
df_prepared["has_department"] = (
    df["department"]
    .notna()
    .astype(int)
)
```

------------------------------------------------------------------------

## 9.3. `title_length`

Walaupun `title` tidak digunakan sebagai kategori dan tidak dianalisis
secara NLP, panjang judul masih dapat digunakan:

``` python
df_prepared["title_length"] = (
    df["title"]
    .fillna("")
    .str.len()
)
```

------------------------------------------------------------------------

## 9.4. `completeness_score`

Notebook sudah menganalisis kelengkapan informasi pada tahap EDA.

Fitur tersebut dapat diuji sebagai fitur model:

``` python
info_columns = [
    "company_profile",
    "salary_range",
    "requirements",
    "benefits",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function"
]

df_prepared["completeness_score"] = (
    df[info_columns]
    .notna()
    .mean(axis=1)
)
```

------------------------------------------------------------------------

## 9.5. `missing_count`

``` python
df_prepared["missing_count"] = (
    df[info_columns]
    .isna()
    .sum(axis=1)
)
```

Fitur ini dapat membantu model memahami tingkat kelengkapan postingan
tanpa menyimpulkan bahwa data yang tidak lengkap pasti palsu.

------------------------------------------------------------------------

# 10. Catatan Penting tentang Fitur Logo, Profil, dan Kelengkapan

Notebook perlu memperjelas interpretasi fitur.

Pernyataan seperti:

> Lowongan tanpa logo adalah lowongan palsu.

tidak boleh digunakan.

Yang lebih tepat:

> Tidak adanya logo perusahaan merupakan salah satu karakteristik yang
> pada dataset memiliki hubungan dengan peningkatan risiko lowongan
> palsu, tetapi fitur tersebut bukan penentu tunggal.

Hal yang sama berlaku untuk:

-   tidak adanya profil perusahaan;
-   benefit kosong;
-   persyaratan kosong;
-   deskripsi pendek.

Model seharusnya belajar dari **kombinasi banyak fitur**.

Contoh:

``` text
Tidak ada logo
+ tidak ada profil perusahaan
+ deskripsi pendek
+ informasi kategori tertentu
+ karakteristik lainnya
        ↓
      Model
        ↓
Probabilitas kelas Fake
```

Karena itu, mempertahankan lebih banyak data asli penting agar model
juga mempelajari contoh:

``` text
Tidak ada logo
+ informasi tidak lengkap
+ tetapi sebenarnya ASLI
```

------------------------------------------------------------------------

# 11. Perbaikan Evaluasi Model

## Kondisi Saat Ini

Metrik yang digunakan:

-   Accuracy;
-   Precision;
-   Recall;
-   F1-Score;
-   Confusion Matrix.

Metrik tersebut tetap digunakan.

Namun, karena dataset asli tidak seimbang, evaluasi perlu diperkuat.

## Metrik Utama yang Direkomendasikan

### 1. Precision Fake

Menjawab:

> Dari semua lowongan yang diprediksi palsu, berapa banyak yang
> benar-benar palsu?

Precision penting untuk mengurangi kasus:

``` text
Lowongan ASLI
    ↓
Diprediksi PALSU
```

------------------------------------------------------------------------

### 2. Recall Fake

Menjawab:

> Dari seluruh lowongan palsu, berapa banyak yang berhasil ditemukan?

Recall penting untuk mengurangi kasus:

``` text
Lowongan PALSU
    ↓
Diprediksi ASLI
```

------------------------------------------------------------------------

### 3. F1-Score Fake

Digunakan untuk melihat keseimbangan antara precision dan recall.

F1-Score tetap cocok menjadi salah satu metrik utama.

------------------------------------------------------------------------

### 4. PR-AUC / Average Precision

PR-AUC direkomendasikan karena kelas positif atau lowongan palsu hanya
sekitar 4,84% dari dataset.

Contoh:

``` python
from sklearn.metrics import average_precision_score

y_prob = model.predict_proba(X_test)[:, 1]

pr_auc = average_precision_score(
    y_test,
    y_prob
)
```

------------------------------------------------------------------------

### 5. Confusion Matrix

Tetap digunakan untuk melihat:

-   True Negative;
-   False Positive;
-   False Negative;
-   True Positive.

Confusion Matrix sangat penting untuk memahami jenis kesalahan model.

------------------------------------------------------------------------

# 12. Accuracy Tidak Boleh Menjadi Metrik Utama

Karena sekitar 95% data adalah lowongan asli, model sederhana yang
selalu memprediksi:

``` text
ASLI
```

dapat memperoleh accuracy sekitar 95%.

Namun, model tersebut gagal mendeteksi seluruh lowongan palsu.

Karena itu, hasil model tidak boleh dipilih hanya berdasarkan:

``` text
Accuracy tertinggi
```

Prioritas evaluasi:

``` text
1. F1-Score Fake
2. Recall Fake
3. Precision Fake
4. PR-AUC
5. Confusion Matrix
6. Accuracy sebagai informasi tambahan
```

Urutan akhir dapat disesuaikan dengan tujuan bisnis, tetapi keputusan
harus mempertimbangkan false positive dan false negative.

------------------------------------------------------------------------

# 13. Tambahkan Baseline Model

Sebelum membandingkan model utama, disarankan menambahkan:

``` python
DummyClassifier
```

Tujuannya adalah mengetahui apakah model machine learning benar-benar
lebih baik daripada strategi prediksi sederhana.

Contoh:

``` python
from sklearn.dummy import DummyClassifier

dummy_model = DummyClassifier(
    strategy="most_frequent"
)
```

Baseline membantu memperkuat analisis penelitian.

### Prioritas

**OPSIONAL TETAPI DIREKOMENDASIKAN.**

------------------------------------------------------------------------

# 14. Tambahkan Cross-Validation

## Kondisi Saat Ini

Model dinilai berdasarkan satu kali Train-Test Split dengan:

``` python
random_state=42
```

Hasil model dapat dipengaruhi oleh pembagian data tertentu.

## Revisi

Gunakan:

``` python
StratifiedKFold
```

pada training set.

Contoh:

``` python
from sklearn.model_selection import StratifiedKFold

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)
```

Cross-validation digunakan untuk:

-   membandingkan model;
-   membandingkan strategi imbalance;
-   mengetahui kestabilan performa.

Testing set final tetap disimpan dan tidak digunakan berulang kali untuk
memilih model.

### Alur

``` text
Training Set
    ↓
5-Fold Cross-Validation
    ↓
Bandingkan Model dan Strategi
    ↓
Pilih Kandidat Terbaik
    ↓
Latih Final Model
    ↓
Evaluasi Sekali pada Test Set
```

### Prioritas

**SANGAT DIREKOMENDASIKAN.**

------------------------------------------------------------------------

# 15. Hyperparameter Tuning Dilakukan Setelah Model Terbaik Ditemukan

Notebook saat ini menggunakan konfigurasi Random Forest yang masih
sederhana:

``` python
RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)
```

Jangan langsung melakukan tuning terhadap semua model dan semua strategi
karena akan membuat eksperimen terlalu besar.

Urutan yang disarankan:

``` text
1. Bandingkan 3 model × 3 strategi
2. Pilih kombinasi terbaik
3. Lakukan tuning hanya pada kandidat terbaik
4. Evaluasi final
```

Contoh parameter Random Forest yang dapat diuji:

``` text
n_estimators
max_depth
min_samples_split
min_samples_leaf
max_features
```

Gunakan:

``` python
RandomizedSearchCV
```

agar lebih efisien dibandingkan mencoba seluruh kombinasi.

### Prioritas

**DILAKUKAN SETELAH METODOLOGI UTAMA DIPERBAIKI.**

------------------------------------------------------------------------

# 16. Revisi Interpretasi Feature Importance

## Kondisi Saat Ini

Notebook menyatakan bahwa feature importance:

> membuktikan hipotesis awal bahwa lowongan palsu biasanya dibuat
> asal-asalan tanpa profil perusahaan yang jelas dan tanpa logo.

Pernyataan tersebut terlalu kuat.

Feature importance tidak membuktikan hubungan sebab-akibat.

## Revisi Narasi

Gunakan:

> Hasil feature importance menunjukkan bahwa `has_company_logo`,
> `company_profile_length`, dan `description_length` merupakan fitur
> yang berkontribusi terhadap keputusan model. Temuan ini mendukung
> hasil EDA bahwa karakteristik kelengkapan dan struktur informasi
> memiliki hubungan dengan klasifikasi lowongan asli dan palsu. Namun,
> fitur-fitur tersebut tidak dapat digunakan secara individual sebagai
> penentu bahwa suatu lowongan pasti asli atau palsu.

Gunakan istilah:

``` text
mendukung temuan
```

bukan:

``` text
membuktikan
```

------------------------------------------------------------------------

# 17. Revisi Klaim Hasil Model

## Kondisi Saat Ini

Notebook menyimpulkan bahwa Random Forest memiliki performa sangat baik
berdasarkan testing set yang sebelumnya sudah diseimbangkan menjadi
50:50.

## Masalah

Hasil tersebut tetap dapat dilaporkan sebagai hasil eksperimen lama,
tetapi belum dapat dianggap sebagai performa final pada distribusi asli.

## Revisi

Setelah metodologi diperbaiki, kesimpulan harus didasarkan pada:

-   testing set yang tidak di-resampling;
-   distribusi kelas asli;
-   model dan strategi imbalance terbaik;
-   precision, recall, F1, PR-AUC, dan confusion matrix.

Jangan menganggap penurunan F1 sebagai kegagalan.

Contoh:

``` text
Eksperimen lama:
F1 = 91,95% pada test set 50:50

Eksperimen revisi:
F1 = 80% pada test set distribusi asli
```

Hasil kedua dapat lebih valid dan lebih realistis untuk deployment.

------------------------------------------------------------------------

# 18. Revisi Kesimpulan tentang Lowongan Tidak Lengkap

Notebook perlu menghindari kesimpulan:

``` text
Tidak ada logo → palsu
Tidak ada profil → palsu
Deskripsi pendek → palsu
```

Kesimpulan yang lebih tepat:

> Berdasarkan dataset, lowongan palsu cenderung memiliki tingkat
> kelengkapan informasi yang lebih rendah dibandingkan lowongan asli.
> Namun, ketidaklengkapan informasi tidak dapat digunakan sebagai aturan
> tunggal karena sebagian lowongan asli juga dapat tidak mencantumkan
> logo, profil perusahaan, benefit, atau informasi lainnya. Oleh karena
> itu, model melakukan prediksi berdasarkan kombinasi berbagai fitur.

------------------------------------------------------------------------

# 19. Rancangan Alur Notebook Setelah Revisi

## Tahap 1 --- Data Understanding

Tetap mempertahankan:

-   informasi dataset;
-   tipe data;
-   missing value;
-   duplicate;
-   distribusi target;
-   analisis fitur biner;
-   analisis kategorikal;
-   analisis kelengkapan;
-   analisis panjang teks.

------------------------------------------------------------------------

## Tahap 2 --- Feature Engineering Non-NLP

Buat fitur:

``` text
country

has_company_profile
has_requirements
has_benefits
has_salary_range
has_department

description_length
requirements_length
benefits_length
company_profile_length
title_length

completeness_score
missing_count
```

Fitur tambahan bersifat kandidat dan perlu diuji.

------------------------------------------------------------------------

## Tahap 3 --- Pisahkan Fitur dan Target

``` python
X = df_prepared.drop(columns=["fraudulent"])
y = df_prepared["fraudulent"]
```

------------------------------------------------------------------------

## Tahap 4 --- Train-Test Split

``` python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

Testing set tidak diubah distribusinya.

------------------------------------------------------------------------

## Tahap 5 --- Preprocessing

``` text
Categorical Features
        ↓
OneHotEncoder(handle_unknown="ignore")

Numerical/Binary Features
        ↓
Passthrough
```

Untuk Logistic Regression, scaling dapat diterapkan pada fitur numerik
jika diperlukan melalui pipeline yang sesuai.

------------------------------------------------------------------------

## Tahap 6 --- Eksperimen Class Imbalance

``` text
Training Set
    │
    ├── A. Original
    │
    ├── B. Class Weight
    │
    └── C. Random Undersampling
```

Random Undersampling hanya dilakukan pada training data atau di dalam
pipeline CV yang aman.

------------------------------------------------------------------------

## Tahap 7 --- Modeling

``` text
3 Strategi
    ×
3 Algoritma
```

Algoritma:

``` text
Logistic Regression
Decision Tree
Random Forest
```

Total:

``` text
9 eksperimen
```

------------------------------------------------------------------------

## Tahap 8 --- Cross-Validation

Gunakan 5-fold Stratified Cross-Validation pada training set untuk
membandingkan kombinasi model.

------------------------------------------------------------------------

## Tahap 9 --- Pemilihan Model

Model dipilih berdasarkan kombinasi:

-   F1 Fake;
-   Recall Fake;
-   Precision Fake;
-   PR-AUC;
-   kestabilan cross-validation;
-   confusion matrix;
-   kebutuhan aplikasi.

------------------------------------------------------------------------

## Tahap 10 --- Hyperparameter Tuning

Dilakukan hanya terhadap kandidat terbaik.

------------------------------------------------------------------------

## Tahap 11 --- Final Evaluation

Model final diuji satu kali pada testing set asli.

Laporkan:

``` text
Accuracy
Precision Fake
Recall Fake
F1-Score Fake
PR-AUC
Confusion Matrix
```

------------------------------------------------------------------------

## Tahap 12 --- Deployment

Simpan preprocessing dan model sebagai satu pipeline jika memungkinkan.

Output aplikasi sebaiknya tidak memberikan klaim absolut.

Contoh:

``` text
Risiko Lowongan Palsu: 68%

Model mendeteksi beberapa karakteristik yang memiliki
kemiripan dengan pola lowongan palsu pada data pelatihan.

Catatan:
Hasil ini merupakan prediksi machine learning dan bukan
jaminan bahwa lowongan tersebut pasti asli atau palsu.
```

------------------------------------------------------------------------

# 20. Diagram Rancangan Akhir

``` text
DATASET ASLI
      │
      ▼
DATA UNDERSTANDING & EDA
      │
      ▼
FEATURE ENGINEERING NON-NLP
      │
      ▼
TRAIN-TEST SPLIT
      │
      ├──────────────────────────────► TEST SET ASLI
      │                                Tidak di-resampling
      ▼
TRAINING SET
      │
      ├── Original
      ├── Class Weight
      └── Random Undersampling
              │
              ▼
      PREPROCESSING PIPELINE
              │
              ▼
      3 ALGORITMA
      ├── Logistic Regression
      ├── Decision Tree
      └── Random Forest
              │
              ▼
      STRATIFIED CROSS-VALIDATION
              │
              ▼
      BANDINGKAN 9 EKSPERIMEN
              │
              ▼
      PILIH KANDIDAT TERBAIK
              │
              ▼
      HYPERPARAMETER TUNING
              │
              ▼
      FINAL MODEL
              │
              ▼
      EVALUASI PADA TEST SET ASLI
              │
              ▼
          DEPLOYMENT
```

------------------------------------------------------------------------

# 21. Urutan Prioritas Revisi

## Prioritas 1 --- Wajib

1.  Lakukan Train-Test Split sebelum balancing.
2.  Jangan melakukan undersampling pada testing set.
3.  Pertahankan testing set dengan distribusi asli.
4.  Bandingkan minimal Original, Class Weight, dan Random Undersampling.
5.  Revisi interpretasi bahwa ketidaklengkapan informasi bukan berarti
    otomatis palsu.

## Prioritas 2 --- Sangat Direkomendasikan

6.  Ganti `LabelEncoder` dengan `OneHotEncoder`.
7.  Gunakan `ColumnTransformer` dan `Pipeline`.
8.  Tambahkan Stratified Cross-Validation.
9.  Tambahkan PR-AUC.
10. Pilih model berdasarkan keseimbangan precision dan recall, bukan
    accuracy saja.

## Prioritas 3 --- Peningkatan

11. Tambahkan fitur non-NLP seperti `has_salary_range`, `title_length`,
    dan `completeness_score`.
12. Tambahkan Dummy Classifier sebagai baseline.
13. Lakukan hyperparameter tuning hanya pada model terbaik.
14. Analisis threshold prediksi jika diperlukan.
15. Perbaiki tampilan hasil prediksi pada aplikasi agar tidak terlalu
    absolut.

------------------------------------------------------------------------

# 22. Kesimpulan Revisi

Notebook saat ini sudah memiliki dasar yang baik, terutama pada:

-   alur CRISP-DM;
-   EDA;
-   pemahaman class imbalance;
-   feature engineering non-NLP;
-   perbandingan beberapa algoritma;
-   penggunaan metrik precision, recall, dan F1-score.

Masalah utama bukan terletak pada pilihan Random Forest atau pada
batasan tanpa NLP.

Masalah utama adalah **metodologi evaluasi**, khususnya karena Random
Undersampling dilakukan sebelum Train-Test Split sehingga testing set
ikut menjadi seimbang 50:50.

Revisi paling penting adalah:

> **Pisahkan training dan testing terlebih dahulu, pertahankan testing
> set dalam distribusi asli, lalu lakukan eksperimen penanganan class
> imbalance hanya pada training set.**

Untuk scope proyek ini, rancangan:

``` text
3 algoritma × 3 strategi imbalance = 9 eksperimen
```

sudah cukup kuat dan tidak berlebihan.

Strategi yang dibandingkan:

``` text
1. Original Data
2. Class Weight
3. Random Undersampling
```

Model akhir tidak ditentukan dari awal.

Walaupun Random Forest dengan `class_weight="balanced"` merupakan
kandidat yang masuk akal, keputusan akhir harus berdasarkan hasil
eksperimen.

Tujuan utama revisi bukan sekadar meningkatkan angka F1-Score, tetapi
menghasilkan model yang:

-   lebih valid secara metodologis;
-   lebih stabil;
-   lebih realistis ketika menerima input pengguna;
-   tidak menganggap ketidaklengkapan informasi sebagai bukti mutlak
    lowongan palsu;
-   tetap konsisten dengan batasan proyek tanpa NLP.
