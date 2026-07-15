# Proyek UAS Data Mining - Deteksi Lowongan Kerja Palsu

Proyek ini dibuat untuk memenuhi tugas UAS mata kuliah **Data Mining** di Universitas Alma Ata. Di sini, kita mengembangkan model machine learning untuk membedakan mana lowongan kerja yang asli dan mana yang terindikasi palsu. Model terbaik yang kita dapatkan kemudian dipasang ke aplikasi web interaktif menggunakan Streamlit supaya mudah dicoba langsung.

---

## Latar Belakang
Banyaknya kasus penipuan berkedok lowongan kerja online sangat merugikan para pencari kerja. Lewat proyek ini, kita ingin membuat sistem yang bisa mendeteksi lowongan palsu secara instan hanya dengan melihat kelengkapan informasi dari postingan lowongan tersebut, tanpa perlu ribet menggunakan analisis teks (NLP) yang berat.

---

## Data Understanding
Kita menggunakan dataset berisi **17.880 data lowongan kerja**. Namun, ada satu masalah besar:
*   **Lowongan Asli**: 17.014 data (95.16%)
*   **Lowongan Palsu**: 866 data (4.84%)

Datanya **sangat jomplang (tidak seimbang)**. Kalau kita langsung buat model dari data ini, modelnya pasti akan malas mikir dan selalu menebak 'Asli' karena peluang benarnya 95%. Maka dari itu, kita harus menyeimbangkan datanya terlebih dahulu pada tahap persiapan.

### Pola Menarik yang Ditemukan:
*   Lowongan palsu rata-rata **tidak memiliki logo perusahaan** dan **tidak menuliskan profil perusahaan**.
*   Deskripsi pekerjaan pada lowongan palsu cenderung **sangat pendek dan asal-asalan**.

---

## Data Preparation
Langkah-langkah yang kita lakukan di berkas notebook:
1.  **Buang Kolom Tidak Penting**: Kolom seperti job_id, title (karena terlalu acak), serta salary_range dan department (karena isinya banyak yang kosong) kita hapus.
2.  **Ubah Teks Jadi Angka & Ukuran**: 
    *   Kita ambil kode negara saja dari lokasi lowongan.
    *   Teks deskripsi, profil, persyaratan, dan benefit kita ukur panjang karakternya. Kita juga buat penanda (0 jika kosong, 1 jika ada isinya).
3.  **Mengatasi Data Jomplang (Random Undersampling)**:
    *   Kita ambil seluruh **866 data lowongan palsu**.
    *   Lalu, kita ambil acak **866 data lowongan asli** untuk mendampinginya.
    *   Sekarang data kita pas 50:50 dengan total **1.732 data** yang siap dilatih.

---

## Hasil Percobaan Model ( Modeling & Evaluation )
Kita bagi data menjadi 80% untuk latihan model (1.385 data) dan 20% untuk pengujian (347 data). Kita coba melatih dan membandingkan 3 algoritma:

*   **Random Forest** (Akurasi: 91.93%, F1-Score: 91.95%, Recall: 92.49%) -> **Pilihan Terbaik**
*   **Decision Tree** (Akurasi: 87.90%, F1-Score: 88.00%)
*   **Logistic Regression** (Akurasi: 77.81%, F1-Score: 77.01%)

### Mengapa Random Forest?
Model Random Forest terbukti paling pintar. Nilai **Recall-nya mencapai 92.49%**, yang berarti model ini bisa mendeteksi 92% lowongan palsu yang diuji. Di dunia nyata, kepekaan mendeteksi lowongan palsu adalah hal terpenting agar tidak ada korban penipuan yang lolos.

Tiga fitur yang paling mempengaruhi keputusan model adalah:
1. Ada tidaknya logo perusahaan (has_company_logo)
2. Panjang tulisan profil perusahaan (company_profile_length)
3. Panjang deskripsi pekerjaan (description_length)

---

## Cara Menjalankan Aplikasi
Aplikasi web ini sudah dipasang tampilan web gelap (*dark mode*) yang interaktif.

### 1. Install Library
Ketik perintah ini di Terminal / CMD untuk menginstal pustaka yang dibutuhkan :
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
Jalankan perintah berikut :
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

### Struktur File Proyek
*   `notebooks/Klasifikasi_Lowongan_Asli_Palsu.ipynb` - File notebook pengerjaan analisis lengkap dari awal sampai akhir.
*   `models/` - Folder penyimpanan model (`model_random_forest.joblib`) dan encoder kategori (`encoder_kategori.joblib`).
*   `app.py` - File utama untuk menjalankan web Streamlit.
*   `implementasi.md` - Laporan tertulis hasil pengerjaan CRISP-DM.
*   `design.md` - Panduan prompting visual UI untuk teman developer.
*   `requirements.txt` - Daftar dependensi pustaka Python.
