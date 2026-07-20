# Proyek UAS Data Mining - Deteksi Lowongan Kerja Palsu

Proyek ini dibuat untuk memenuhi tugas UAS mata kuliah **Data Mining** di Universitas Alma Ata. Di sini, kami mengembangkan model machine learning untuk membedakan mana lowongan kerja yang asli dan mana yang terindikasi palsu (fraudulent). Model terbaik yang kami dapatkan kemudian dipasang ke aplikasi web interaktif menggunakan Streamlit supaya mudah dicoba langsung.

---

## Latar Belakang

Banyaknya kasus penipuan berkedok lowongan kerja online sangat merugikan para pencari kerja. Lewat proyek ini, kami ingin membuat sistem yang bisa mendeteksi lowongan palsu secara instan hanya dengan melihat kelengkapan informasi dari postingan lowongan tersebut, tanpa menggunakan analisis teks (NLP) yang berat.

---

## Data Understanding

Kami menggunakan dataset berisi **17.880 data lowongan kerja**. Namun, ada satu masalah besar:

- **Lowongan Asli**: 17.014 data (95.16%)
- **Lowongan Palsu**: 866 data (4.84%)

Datanya **sangat jomplang (tidak seimbang)**. Kalau kami langsung buat model dari data ini, modelnya pasti akan malas mikir dan selalu menebak 'Asli' karena peluang benarnya 95%. Maka dari itu, kami harus menyeimbangkan datanya terlebih dahulu pada tahap persiapan.

### Pola Menarik yang Ditemukan

- Lowongan palsu rata-rata tidak memiliki logo perusahaan dan tidak menuliskan profil perusahaan.
- Deskripsi pekerjaan pada lowongan palsu cenderung sangat pendek dan asal-asalan.

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

| Model                   | Strategi Imbalance           | Precision (Fake) | Recall (Fake) | F1-Score (Fake) |   PR-AUC   |
| :---------------------- | :--------------------------- | :--------------: | :-----------: | :-------------: | :--------: |
| **Logistic Regression** | Original                     |      71.02%      |    30.60%     |     42.53%      |   0.5578   |
|                         | Class Weight                 |      26.12%      |    87.41%     |     40.22%      |   0.4740   |
|                         | Undersampling                |      22.84%      |    86.95%     |     36.17%      |   0.4229   |
| **Decision Tree**       | Original                     |      67.61%      |    68.83%     |     68.12%      |   0.4805   |
|                         | Class Weight                 |      66.58%      |    71.24%     |     68.82%      |   0.4895   |
|                         | Undersampling                |      22.72%      |    88.34%     |     36.13%      |   0.2064   |
| **Random Forest**       | Original                     |      97.31%      |    62.24%     |     75.90%      |   0.8904   |
|                         | Class Weight                 |      97.36%      |    61.67%     |     75.46%      |   0.8809   |
|                         | **Undersampling (Selected)** |    **32.61%**    |  **92.38%**   |   **48.20%**    | **0.7703** |

### Mengapa Random Forest dengan Undersampling?

Kami memilih **Random Forest dengan strategi Undersampling (Strategy C)** karena memberikan tingkat **Recall (sensitivitas) tertinggi sebesar 92.38%** pada data training. Nilai Recall yang tinggi sangat penting bagi sistem keamanan lowongan kerja agar tidak ada korban penipuan yang lolos.

### Evaluasi Final pada Data Uji Asli (Test Set)

Model final yang telah dituning menunjukkan performa luar biasa pada data uji riil yang imbalanced:

- **Akurasi Keseluruhan** : **90.18%**
- **Precision (Fake)** : **32.27%**
- **Recall (Fake)** : **93.64%** (Model berhasil menangkap 93.64% lowongan palsu pada populasi riil)
- **F1-Score (Fake)** : **48.00%**
- **PR-AUC** : **78.11%**

---

## Fitur Explainable AI (XAI) dengan Gemini

Untuk memberikan transparansi yang lebih baik kepada pengguna, aplikasi web **LODONG** terintegrasi dengan teknologi **XAI (Explainable AI)** menggunakan **Google Gemini 3.1 Flash Lite**.

### Peran XAI di Lodong

Model klasifikasi machine learning (Random Forest) hanya mengeluarkan angka probabilitas/label keputusan (misalnya: _75% kemungkinan palsu_). Bagi pengguna awam, angka ini sering kali sulit dipahami. XAI berfungsi untuk menerjemahkan logika matematika model tersebut menjadi kalimat penjelasan alami bahasa Indonesia yang logis mengenai faktor risiko apa saja yang membuat lowongan tersebut dinilai asli atau palsu.

### Output XAI pada Aplikasi

Setelah pengguna menekan tombol **Analisis Lowongan**, model akan mengklasifikasikan data dan Gemini AI akan secara dinamis menyusun penjelasan 4–5 kalimat berdasarkan data masukan berikut:

1.  **Judul Pekerjaan**: Menganalisis nama profesi yang dicari secara kontekstual.
2.  **Kelengkapan Profil & Logo**: Menilai validitas kehadiran logo resmi dan sejarah singkat perusahaan.
3.  **Panjang Deskripsi & Persyaratan**: Mengindikasikan kerawanan dari teks deskripsi/persyaratan kerja yang terlalu singkat.
4.  **Rentang Gaji & Benefit**: Mendeteksi ada/tidaknya kompensasi bagi pelamar.
5.  **Skor Kelengkapan Informasi**: Memberikan persentase kelayakan kelengkapan loker.
6.  **Tips Keamanan**: Di akhir analisis, Gemini akan menyusun 3 poin tips keamanan praktis yang spesifik bagi pelamar kerja.

### Cara Konfigurasi API Key Gemini

Untuk menggunakan fitur ini di lokal:

1. Buat berkas rahasia bernama `.streamlit/secrets.toml` di direktori root proyek.
2. Masukkan API Key Google Gemini Anda ke dalam berkas tersebut:
   ```toml
   GEMINI_API_KEY = "API_KEY_GOOGLE_AI_STUDIO_ANDA"
   ```
   _(Berkas ini aman dan tidak akan ter-push ke GitHub karena sudah terdaftar di `.gitignore`)._

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

- `notebooks/Klasifikasi_Lowongan_Asli_Palsu.ipynb` - File notebook pengerjaan analisis lengkap dari awal sampai akhir.
- `models/model_pipeline.joblib` - Objek Pipeline Scikit-Learn tunggal berisi preprocessor dan model klasifikasi.
- `app.py` - File utama untuk menjalankan web Streamlit.
- `frontend/` - Folder komponen UI modular (views, styles).
- `implementasi.md` - Laporan tertulis hasil pengerjaan CRISP-DM.
- `requirements.txt` - Daftar dependensi pustaka Python.
