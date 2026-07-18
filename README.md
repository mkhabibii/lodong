# Proyek UAS Data Mining - Deteksi Lowongan Kerja Palsu

Proyek ini dibuat untuk memenuhi tugas UAS mata kuliah **Data Mining** di Universitas Alma Ata. Di sini, kita mengembangkan model machine learning untuk membedakan mana lowongan kerja yang asli dan mana yang terindikasi palsu (fraudulent). Model terbaik yang kita dapatkan kemudian dipasang ke aplikasi web interaktif menggunakan Streamlit supaya mudah dicoba langsung.

Di branch `reborn` ini, kami telah menerapkan perbaikan metodologi yang ketat: menggunakan **Train-Test Split sebelum balancing**, membandingkan 9 skenario eksperimen dengan **5-Fold Stratified Cross-Validation**, serta menggunakan objek **Pipeline terpadu** untuk penyederhanaan deployment.

---

## Latar Belakang
Banyaknya kasus penipuan berkedok lowongan kerja online sangat merugikan para pencari kerja. Lewat proyek ini, kita ingin membuat sistem yang bisa mendeteksi lowongan palsu secara instan hanya dengan melihat kelengkapan informasi dari postingan lowongan tersebut, tanpa perlu ribet menggunakan analisis teks (NLP) yang berat.

---

## Data Understanding
Kita menggunakan dataset berisi **17.880 data lowongan kerja**. Namun, ada satu masalah besar:
*   **Lowongan Asli**: 17.014 data (95.16%)
*   **Lowongan Palsu**: 866 data (4.84%)

Datanya **sangat jomplang (tidak seimbang)**. Kalau kita langsung buat model dari data ini, modelnya pasti akan malas mikir dan selalu menebak 'Asli' karena peluang benarnya 95%. Maka dari itu, kita harus menyeimbangkan datanya terlebih dahulu pada tahap persiapan.

### Pola Menarik yang Ditemukan
*   Lowongan palsu rata-rata tidak memiliki logo perusahaan dan tidak menuliskan profil perusahaan.
*   Deskripsi pekerjaan pada lowongan palsu cenderung sangat pendek dan asal-asalan.

---

## Data Preparation & Feature Engineering
Untuk membekali model dengan pola struktural kelengkapan postingan lowongan kerja tanpa NLP, kami merekayasa fitur-fitur berikut:
1.  `has_company_profile`, `has_requirements`, `has_benefits` (Keberadaan teks info)
2.  `has_salary_range` (Keberadaan rentang gaji)
3.  `has_department` (Keberadaan departemen)
4.  `description_length`, `requirements_length`, `benefits_length`, `company_profile_length`, `title_length` (Panjang karakter teks)
5.  `completeness_score` (Rasio kelengkapan informasi, range 0.0 - 1.0)
6.  `missing_count` (Jumlah informasi kosong)

Proses pemisahan data latih (80%) dan data uji (20%) dilakukan **sebelum** balancing secara stratifikasi. Hal ini menjaga agar data uji tetap menggambarkan distribusi asli yang timpang (~95:5) demi validitas evaluasi.

---

## Hasil Percobaan Model (Modeling & Evaluation)
Kami melatih 3 algoritma dengan 3 skenario penanganan data jomplang pada training set (total 9 eksperimen) dan mengevaluasinya menggunakan 5-Fold Stratified Cross-Validation:

| Model | Strategi Imbalance | Precision (Fake) | Recall (Fake) | F1-Score (Fake) | PR-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Logistic Regression** | Original | 71.02% | 30.60% | 42.53% | 0.5578 |
| | Class Weight | 26.12% | 87.41% | 40.22% | 0.4740 |
| | Undersampling | 22.84% | 86.95% | 36.17% | 0.4229 |
| **Decision Tree** | Original | 67.61% | 68.83% | 68.12% | 0.4805 |
| | Class Weight | 66.58% | 71.24% | 68.82% | 0.4895 |
| | Undersampling | 22.72% | 88.34% | 36.13% | 0.2064 |
| **Random Forest** | Original | 97.31% | 62.24% | 75.90% | 0.8904 |
| | Class Weight | 97.36% | 61.67% | 75.46% | 0.8809 |
| | **Undersampling (Selected)** | **32.61%** | **92.38%** | **48.20%** | **0.7703** |

### Mengapa Random Forest dengan Undersampling?
Kami memilih **Random Forest dengan strategi Undersampling (Strategy C)** karena memberikan tingkat **Recall (sensitivitas) tertinggi sebesar 92.38%** pada data training. Nilai Recall yang tinggi sangat penting bagi sistem keamanan lowongan kerja agar tidak ada korban penipuan yang lolos.

### Evaluasi Final pada Data Uji Asli (Test Set)
Model final yang telah dituning menunjukkan performa luar biasa pada data uji riil yang imbalanced:
*   **Akurasi Keseluruhan** : **90.18%**
*   **Precision (Fake)** : **32.27%**
*   **Recall (Fake)** : **93.64%** (Model berhasil menangkap 93.64% lowongan palsu pada populasi riil)
*   **F1-Score (Fake)** : **48.00%**
*   **PR-AUC** : **78.11%**

---

## Cara Menjalankan Aplikasi

### 1. Install Library
Ketik perintah ini di Terminal / CMD untuk menginstal pustaka yang dibutuhkan:
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
Jalankan perintah berikut:
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

### Struktur File Proyek
*   `notebooks/Klasifikasi_Lowongan_Asli_Palsu.ipynb` - File notebook pengerjaan analisis lengkap dari awal sampai akhir.
*   `models/model_pipeline.joblib` - Objek Pipeline Scikit-Learn tunggal berisi preprocessor dan model klasifikasi.
*   `app.py` - File utama untuk menjalankan web Streamlit.
*   `frontend/` - Folder komponen UI modular (views, styles).
*   `implementasi.md` - Laporan tertulis hasil pengerjaan CRISP-DM.
*   `requirements.txt` - Daftar dependensi pustaka Python.
