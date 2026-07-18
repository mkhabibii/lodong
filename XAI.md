# 💡 Dokumentasi Implementasi Explainable AI (XAI) menggunakan Gemini 1.5 Flash

Dokumen ini menjelaskan langkah-langkah praktis untuk mengintegrasikan model bahasa besar (LLM) **Gemini 1.5 Flash** ke dalam aplikasi **Pendeteksi Lowongan Palsu**. Tujuannya adalah memberikan penjelasan alami (XAI) mengapa model Random Forest memprediksi suatu lowongan sebagai "Asli" atau "Palsu".

---

## 🛠️ Prasyarat & Persiapan

### 1. Dapatkan API Key Gratis
1. Buka [Google AI Studio](https://aistudio.google.com/).
2. Login menggunakan akun Google Anda.
3. Klik tombol **"Get API Key"** lalu buat kunci API baru.
4. Salin API Key tersebut dan simpan dengan aman.

### 2. Instal Library Pustaka Python
Jalankan perintah berikut di terminal Anda untuk menginstal pustaka generator resmi dari Google:
```bash
pip install google-generativeai
```
*(Jangan lupa tambahkan `google-generativeai` ke dalam file `requirements.txt` Anda).*

---

## 📝 Perubahan Kode pada `app.py`

Berikut adalah blok kode yang perlu ditambahkan atau dimodifikasi pada file `app.py` Anda:

### Langkah A: Import Library & Inisialisasi API
Tambahkan kode berikut di bagian paling atas file `app.py` (bersama import library lainnya):

```python
import google.generativeai as genai

# Konfigurasi API Key (Disarankan menggunakan Environment Variable demi keamanan)
# Anda bisa menyimpan API key langsung di kode untuk uji coba lokal, 
# atau menggunakan os.environ.get("GEMINI_API_KEY")
GEMINI_API_KEY = "MASUKKAN_API_KEY_GOOGLE_AI_STUDIO_ANDA_DI_SINI"

if GEMINI_API_KEY and GEMINI_API_KEY != "MASUKKAN_API_KEY_GOOGLE_AI_STUDIO_ANDA_DI_SINI":
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_ready = True
else:
    gemini_ready = False
```

---

### Langkah B: Buat Fungsi Pembuat Penjelasan (Helper Function)
Tambahkan fungsi di bawah ini sebelum bagian blok kode `# --- MAIN AREA ---`:

```python
def generate_xai_explanation(prediction, probability, input_data):
    """
    Fungsi untuk mengirim data karakteristik ke Gemini 1.5 Flash 
    dan mendapatkan penjelasan bahasa Indonesia yang logis (XAI).
    """
    if not gemini_ready:
        return "⚠️ API Key Gemini belum dikonfigurasi. Penjelasan otomatis tidak dapat dimuat."
        
    try:
        # Tentukan label teks prediksi
        label_prediksi = "PALSU (Terdikasi Penipuan)" if prediction == 1 else "ASLI (Valid)"
        persen_keyakinan = f"{probability:.2f}%"
        
        # Buat ringkasan kelengkapan informasi sebagai bukti
        bukti_list = []
        if input_data['has_company_logo'] == 0:
            bukti_list.append("- Postingan tidak mencantumkan logo perusahaan.")
        else:
            bukti_list.append("- Postingan mencantumkan logo resmi perusahaan.")
            
        if input_data['has_company_profile'] == 0:
            bukti_list.append("- Profil/sejarah singkat perusahaan dikosongkan.")
        else:
            bukti_list.append(f"- Profil perusahaan dicantumkan sepanjang {input_data['company_profile_length']} karakter.")
            
        if input_data['description_length'] < 300:
            bukti_list.append(f"- Teks deskripsi pekerjaan sangat singkat (hanya {input_data['description_length']} karakter).")
        else:
            bukti_list.append(f"- Deskripsi pekerjaan ditulis cukup lengkap ({input_data['description_length']} karakter).")
            
        if input_data['has_requirements'] == 0:
            bukti_list.append("- Persyaratan kerja untuk pelamar dikosongkan.")
        else:
            bukti_list.append(f"- Persyaratan kerja ditulis sepanjang {input_data['requirements_length']} karakter.")
            
        bukti_str = "\\n".join(bukti_list)
        
        # Susun Prompt untuk dikirim ke Gemini
        prompt = f\"\"\"
        Kamu adalah asisten ahli keamanan informasi dan analisis lowongan kerja. 
        Tolong jelaskan secara singkat dan logis kepada pencari kerja mengapa sistem klasifikasi 
        kami memprediksi lowongan ini sebagai {label_prediksi} dengan tingkat keyakinan {persen_keyakinan} 
        berdasarkan bukti karakteristik berikut:
        {bukti_str}
        
        Aturan Penulisan:
        1. Tulis penjelasan dalam 3-4 kalimat saja menggunakan bahasa Indonesia yang ramah, santai namun tetap profesional (human-written style).
        2. Jangan terdengar seperti robot atau template AI yang kaku.
        3. Di akhir kalimat, berikan 1 tips keamanan singkat yang relevan bagi pelamar kerja.
        \"\"\"
        
        # Panggil model Gemini 1.5 Flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Gagal memuat penjelasan AI: {str(e)}"
```

---

### Langkah C: Integrasikan Fungsi pada Tombol Prediksi Streamlit
Pada file `app.py`, di dalam blok `if predict_btn:` (tepat di bawah visualisasi hasil prediksi merah/hijau), tambahkan rendering untuk penjelasan AI:

```python
                # Panggil fungsi XAI di bawah rendering hasil prediksi
                st.markdown("---")
                st.markdown("### 💡 **Analisis Karakteristik (AI Explanation):**")
                
                with st.spinner("AI sedang menganalisis karakteristik lowongan..."):
                    # Buat dict input_data dari nilai masukan pengguna
                    data_bukti = {
                        'has_company_logo': 1 if has_company_logo else 0,
                        'has_company_profile': 1 if has_company_profile else 0,
                        'description_length': description_length,
                        'has_requirements': 1 if has_requirements else 0,
                        'requirements_length': requirements_length,
                        'company_profile_length': company_profile_length
                    }
                    
                    # Dapatkan probabilitas yang sesuai
                    prob_nilai = probabilities[1] * 100 if prediction == 1 else probabilities[0] * 100
                    
                    # Tampilkan penjelasan hasil interpretasi Gemini
                    penjelasan_ai = generate_xai_explanation(prediction, prob_nilai, data_bukti)
                    
                    # Tampilkan dalam box Glassmorphic khusus
                    st.info(penjelasan_ai)
```

---

## 📈 Keuntungan Fitur Ini bagi Tugas Akhir UAS Anda
*   **Nilai Orisinalitas Tinggi**: Menunjukkan Anda mengerti tren terkini di mana machine learning dikombinasikan dengan generative AI untuk kebutuhan interpretasi model.
*   **Edukasi Pengguna Nyata**: Aplikasi tidak hanya memberi label "Palsu/Asli", tetapi mendidik calon pelamar kerja untuk jeli melihat ciri-ciri lowongan kosong sebelum melamar.
