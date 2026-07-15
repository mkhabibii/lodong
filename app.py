import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import time

# Set page configuration
st.set_page_config(
    page_title="Pendeteksi Lowongan Palsu",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Glassmorphism, Premium Dark Mode, and transitions
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #15103c 100%);
        color: #f1f5f9;
    }
    
    /* Title and Header */
    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .main-title {
        background: linear-gradient(45deg, #a5b4fc, #818cf8, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Card Glassmorphism UI */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }
    
    /* Result styling */
    .result-card-real {
        background: rgba(16, 185, 129, 0.12);
        border: 2px solid #10b981;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.25);
        backdrop-filter: blur(8px);
        animation: pulse-green 2s infinite alternate;
    }
    
    .result-card-fake {
        background: rgba(244, 63, 94, 0.12);
        border: 2px solid #f43f5e;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 0 25px rgba(244, 63, 94, 0.25);
        backdrop-filter: blur(8px);
        animation: pulse-red 2s infinite alternate;
    }
    
    @keyframes pulse-green {
        0% { box-shadow: 0 0 15px rgba(16, 185, 129, 0.15); }
        100% { box-shadow: 0 0 30px rgba(16, 185, 129, 0.35); }
    }
    
    @keyframes pulse-red {
        0% { box-shadow: 0 0 15px rgba(244, 63, 94, 0.15); }
        100% { box-shadow: 0 0 30px rgba(244, 63, 94, 0.35); }
    }
    
    /* Button Customization */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        color: white !important;
        border: none !important;
        padding: 14px 28px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
        background: linear-gradient(135deg, #5a52e6 0%, #7376f2 100%) !important;
    }
    
    /* Sidebar Styling */
    .css-163412f {
        background-color: #0d0f1a !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load model and encoders safely
@st.cache_resource
def load_prediction_assets():
    model_path = 'models/model_random_forest.joblib'
    encoders_path = 'models/encoder_kategori.joblib'
    
    if os.path.exists(model_path) and os.path.exists(encoders_path):
        model = joblib.load(model_path)
        encoders = joblib.load(encoders_path)
        return model, encoders, True
    return None, None, False


model, encoders, is_loaded = load_prediction_assets()

# --- KAMUS TRANSLASI DROPDOWN KE BAHASA INDONESIA ---
# 1. Tipe Pekerjaan (Employment Type)
emp_translation = {
    'Full-time': 'Penuh Waktu (Full-time)',
    'Part-time': 'Paruh Waktu (Part-time)',
    'Contract': 'Kontrak (Contract)',
    'Temporary': 'Sementara (Temporary)',
    'Other': 'Lainnya (Other)',
    'Unspecified': 'Tidak Ditentukan (Unspecified)'
}
reverse_emp = {v: k for k, v in emp_translation.items()}

# 2. Pengalaman Kerja Minimal
exp_translation = {
    'Entry level': 'Tingkat Pemula (Entry Level)',
    'Associate': 'Asosiasi (Associate)',
    'Mid-Senior level': 'Menengah-Atas (Mid-Senior)',
    'Director': 'Direktur (Director)',
    'Executive': 'Eksekutif (Executive)',
    'Internship': 'Magang (Internship)',
    'Not Applicable': 'Tidak Terkait (Not Applicable)',
    'Unspecified': 'Tidak Ditentukan (Unspecified)'
}
reverse_exp = {v: k for k, v in exp_translation.items()}

# 3. Pendidikan Minimal
edu_translation = {
    'High School or equivalent': 'SMA / Sederajat (High School)',
    'Bachelor\'s Degree': 'S1 / Sarjana (Bachelor\'s)',
    'Master\'s Degree': 'S2 / Magister (Master\'s)',
    'Doctorate': 'S3 / Doktor (Doctorate)',
    'Associate Degree': 'D3 / Diploma (Associate)',
    'Vocational': 'Vokasi / SMK (Vocational)',
    'Certification': 'Sertifikasi (Certification)',
    'Some College Coursework Completed': 'Kuliah Belum Lulus',
    'Unspecified': 'Tidak Ditentukan (Unspecified)'
}
reverse_edu = {v: k for k, v in edu_translation.items()}

# 4. Negara Lokasi Kerja
country_translation = {
    'AE': 'Uni Emirat Arab (AE)',
    'AL': 'Albania (AL)',
    'AM': 'Armenia (AM)',
    'AR': 'Argentina (AR)',
    'AT': 'Austria (AT)',
    'AU': 'Australia (AU)',
    'BD': 'Bangladesh (BD)',
    'BE': 'Belgia (BE)',
    'BG': 'Bulgaria (BG)',
    'BH': 'Bahrain (BH)',
    'BR': 'Brasil (BR)',
    'BY': 'Belarus (BY)',
    'CA': 'Kanada (CA)',
    'CH': 'Swiss (CH)',
    'CL': 'Chile (CL)',
    'CM': 'Kamerun (CM)',
    'CN': 'Tiongkok (CN)',
    'CO': 'Kolombia (CO)',
    'CY': 'Siprus (CY)',
    'CZ': 'Ceko (CZ)',
    'DE': 'Jerman (DE)',
    'DK': 'Denmark (DK)',
    'EE': 'Estonia (EE)',
    'EG': 'Mesir (EG)',
    'ES': 'Spanyol (ES)',
    'FI': 'Finlandia (FI)',
    'FR': 'Prancis (FR)',
    'GB': 'Inggris (GB)',
    'GH': 'Ghana (GH)',
    'GR': 'Yunani (GR)',
    'HK': 'Hong Kong (HK)',
    'HR': 'Kroasia (HR)',
    'HU': 'Hongaria (HU)',
    'ID': 'Indonesia (ID)',
    'IE': 'Irlandia (IE)',
    'IL': 'Israel (IL)',
    'IN': 'India (IN)',
    'IQ': 'Irak (IQ)',
    'IS': 'Islandia (IS)',
    'IT': 'Italia (IT)',
    'JM': 'Jamaika (JM)',
    'JP': 'Jepang (JP)',
    'KE': 'Kenya (KE)',
    'KH': 'Kamboja (KH)',
    'KR': 'Korea Selatan (KR)',
    'KW': 'Kuwait (KW)',
    'KZ': 'Kazakhstan (KZ)',
    'LK': 'Sri Lanka (LK)',
    'LT': 'Lituania (LT)',
    'LU': 'Luksemburg (LU)',
    'LV': 'Latvia (LV)',
    'MA': 'Maroko (MA)',
    'MT': 'Malta (MT)',
    'MU': 'Mauritius (MU)',
    'MX': 'Meksiko (MX)',
    'MY': 'Malaysia (MY)',
    'NG': 'Nigeria (NG)',
    'NI': 'Nikaragua (NI)',
    'NL': 'Belanda (NL)',
    'NO': 'Norwegia (NO)',
    'NZ': 'Selandia Baru (NZ)',
    'PA': 'Panama (PA)',
    'PE': 'Peru (PE)',
    'PH': 'Filipina (PH)',
    'PK': 'Pakistan (PK)',
    'PL': 'Polandia (PL)',
    'PT': 'Portugal (PT)',
    'QA': 'Qatar (QA)',
    'RO': 'Rumania (RO)',
    'RS': 'Serbia (RS)',
    'RU': 'Rusia (RU)',
    'SA': 'Arab Saudi (SA)',
    'SD': 'Sudan (SD)',
    'SE': 'Swedia (SE)',
    'SG': 'Singapura (SG)',
    'SI': 'Slovenia (SI)',
    'SK': 'Slovakia (SK)',
    'SV': 'El Salvador (SV)',
    'TH': 'Thailand (TH)',
    'TN': 'Tunisia (TN)',
    'TR': 'Turki (TR)',
    'TT': 'Trinidad & Tobago (TT)',
    'TW': 'Taiwan (TW)',
    'UA': 'Ukraina (UA)',
    'UG': 'Uganda (UG)',
    'US': 'Amerika Serikat (US)',
    'VI': 'Kepulauan Virgin (VI)',
    'VN': 'Vietnam (VN)',
    'ZA': 'Afrika Selatan (ZA)',
    'ZM': 'Zambia (ZM)',
    'Unspecified': 'Tidak Ditentukan (Unspecified)'
}
def get_country_display(code):
    return country_translation.get(code, f"{code} ({code})")


# --- SIDEBAR AREA ---
with st.sidebar:
    st.image("https://img.icons8.com/color/120/cyber-security.png", width=70)
    st.markdown("### **Pendeteksi Lowongan Palsu**")
    st.markdown("Aplikasi web data mining untuk memprediksi apakah suatu lowongan pekerjaan terindikasi **Palsu (Fraudulent)** atau **Asli (Real)**.")
    
    st.markdown("---")
    st.markdown("#### **Spesifikasi Model:**")
    st.markdown("- **Model**: Klasifikasi Random Forest")
    st.markdown("- **Metode**: Klasifikasi Tabular (Non-NLP)")
    st.markdown("- **Kelebihan**: Menggunakan rekayasa fitur kelengkapan profil perusahaan dan panjang karakter teks untuk deteksi cepat.")
    st.markdown("---")
    st.markdown("Dibuat untuk UAS Kelas Data Mining © Alma Ata Yogyakarta")

# --- MAIN AREA ---
st.markdown('<div class="main-title">🔍 Deteksi Lowongan Kerja Palsu</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analisis instan keandalan lowongan kerja berdasarkan pola struktural dan kelengkapan informasi</div>', unsafe_allow_html=True)

if not is_loaded:
    st.warning("⚠️ Berkas Model dan Encoder tidak ditemukan di folder `models/`. Harap selesaikan pelatihan model pada file notebook terlebih dahulu untuk menghasilkan berkas `model_random_forest.joblib` dan `encoder_kategori.joblib`.")
else:
    # We create the input form using columns
    with st.container():
        st.markdown('<div class="glass-card"><h4>📝 Formulir Karakteristik Lowongan</h4>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### **Kategori & Karakteristik Struktural**")
            
            # Categories loaded dynamically from label encoders
            country_options = list(encoders['country'].classes_)
            country_display_options = [get_country_display(c) for c in country_options]
            selected_country_display = st.selectbox(
                "Negara Lokasi Kerja", 
                options=country_display_options, 
                index=country_options.index('US') if 'US' in country_options else 0
            )
            # Map back to raw code
            country = next(k for k, v in country_translation.items() if v == selected_country_display) if selected_country_display in country_translation.values() else selected_country_display.split(' ')[-1].replace('(', '').replace(')', '')
            
            emp_options = list(encoders['employment_type'].classes_)
            emp_display_options = [emp_translation.get(e, e) for e in emp_options]
            selected_emp_display = st.selectbox(
                "Jenis Pekerjaan (Employment Type)", 
                options=emp_display_options, 
                index=emp_display_options.index(emp_translation['Full-time']) if 'Full-time' in emp_options else 0
            )
            employment_type = reverse_emp.get(selected_emp_display, selected_emp_display)
            
            exp_options = list(encoders['required_experience'].classes_)
            exp_display_options = [exp_translation.get(e, e) for e in exp_options]
            selected_exp_display = st.selectbox("Pengalaman Kerja Minimal", options=exp_display_options)
            required_experience = reverse_exp.get(selected_exp_display, selected_exp_display)
            
            edu_options = list(encoders['required_education'].classes_)
            edu_display_options = [edu_translation.get(e, e) for e in edu_options]
            selected_edu_display = st.selectbox("Pendidikan Minimal", options=edu_display_options)
            required_education = reverse_edu.get(selected_edu_display, selected_edu_display)
            
            ind_options = list(encoders['industry'].classes_)
            industry = st.selectbox("Kategori Industri", options=ind_options)
            
            func_options = list(encoders['function'].classes_)
            function = st.selectbox("Fungsi / Bidang Pekerjaan", options=func_options)
            
        with col2:
            st.markdown("##### **Fasilitas & Kelengkapan Profil**")
            
            # Checkbox columns
            sub_col1, sub_col2, sub_col3 = st.columns(3)
            with sub_col1:
                telecommuting = st.checkbox("Mendukung Remote / WFH", value=False)
            with sub_col2:
                has_company_logo = st.checkbox("Memiliki Logo Perusahaan", value=False)
            with sub_col3:
                has_questions = st.checkbox("Memiliki Pertanyaan Screening", value=False)
                
            # Text completeness flags
            sub_col4, sub_col5, sub_col6 = st.columns(3)
            with sub_col4:
                has_company_profile = st.checkbox("Memiliki Profil Perusahaan", value=False)
            with sub_col5:
                has_requirements = st.checkbox("Memiliki Persyaratan Kerja", value=False)
            with sub_col6:
                has_benefits = st.checkbox("Memiliki Fasilitas / Benefit", value=False)
                
            st.markdown("---")
            st.markdown("##### **Estimasi Panjang Karakter Informasi**")
            
            description_length = st.slider("Panjang Karakter Deskripsi Pekerjaan", min_value=0, max_value=5000, value=0, step=50)
            requirements_length = st.slider("Panjang Karakter Persyaratan Kerja", min_value=0, max_value=4000, value=0, step=50, disabled=not has_requirements)
            benefits_length = st.slider("Panjang Karakter Benefit Pekerjaan", min_value=0, max_value=3000, value=0, step=50, disabled=not has_benefits)
            company_profile_length = st.slider("Panjang Karakter Profil Perusahaan", min_value=0, max_value=4000, value=0, step=50, disabled=not has_company_profile)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Trigger button
        predict_btn = st.button("🔍 Menganalisis Keaslian Lowongan")
        
        if predict_btn:
            with st.spinner("Menganalisis pola karakteristik lowongan kerja..."):
                time.sleep(1.0) # Simulation for premium feel
                
                # Transform inputs using label encoders
                encoded_country = encoders['country'].transform([country])[0]
                encoded_employment = encoders['employment_type'].transform([employment_type])[0]
                encoded_experience = encoders['required_experience'].transform([required_experience])[0]
                encoded_education = encoders['required_education'].transform([required_education])[0]
                encoded_industry = encoders['industry'].transform([industry])[0]
                encoded_function = encoders['function'].transform([function])[0]
                
                # Format into input DataFrame with EXACT order and names as training columns
                input_df = pd.DataFrame([{
                    'telecommuting': 1 if telecommuting else 0,
                    'has_company_logo': 1 if has_company_logo else 0,
                    'has_questions': 1 if has_questions else 0,
                    'employment_type': encoded_employment,
                    'required_experience': encoded_experience,
                    'required_education': encoded_education,
                    'industry': encoded_industry,
                    'function': encoded_function,
                    'country': encoded_country,
                    'has_company_profile': 1 if has_company_profile else 0,
                    'has_requirements': 1 if has_requirements else 0,
                    'has_benefits': 1 if has_benefits else 0,
                    'description_length': description_length,
                    'requirements_length': requirements_length,
                    'benefits_length': benefits_length,
                    'company_profile_length': company_profile_length
                }])
                
                # Predict
                prediction = model.predict(input_df)[0]
                probabilities = model.predict_proba(input_df)[0]
                
                st.markdown("### **Hasil Analisis Model:**")
                if prediction == 0:
                    real_prob = probabilities[0] * 100
                    st.markdown(f"""
                    <div class="result-card-real">
                        <img src="https://img.icons8.com/color/96/ok--v1.png" width="60" style="margin-bottom: 10px;">
                        <h3 style="color: #10b981; margin: 0;">LOWONGAN KERJA INI VALID / ASLI</h3>
                        <p style="margin: 8px 0 0 0; color: #e2e8f0; font-size: 1.1rem;">
                            Model memprediksi dengan tingkat keyakinan <strong>{real_prob:.2f}%</strong> bahwa lowongan ini aman dan terpercaya.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    fake_prob = probabilities[1] * 100
                    st.markdown(f"""
                    <div class="result-card-fake">
                        <img src="https://img.icons8.com/color/96/cancel--v1.png" width="60" style="margin-bottom: 10px;">
                        <h3 style="color: #f43f5e; margin: 0;">PERINGATAN: LOWONGAN KERJA TERINDIKASI PALSU / FRAUD</h3>
                        <p style="margin: 8px 0 0 0; color: #e2e8f0; font-size: 1.1rem;">
                            Model memprediksi dengan tingkat keyakinan <strong>{fake_prob:.2f}%</strong> bahwa lowongan ini memiliki kecocokan pola penipuan.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)