import streamlit as st
import pandas as pd
import numpy as np
import time

# --- KAMUS TRANSLASI DROPDOWN KE BAHASA INDONESIA ---
emp_translation = {
    'Full-time': 'Penuh Waktu (Full-time)',
    'Part-time': 'Paruh Waktu (Part-time)',
    'Contract': 'Kontrak (Contract)',
    'Temporary': 'Sementara (Temporary)',
    'Other': 'Lainnya (Other)',
    'Unspecified': 'Tidak Ditentukan (Unspecified)'
}
reverse_emp = {v: k for k, v in emp_translation.items()}

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

edu_translation = {
    'High School or equivalent': 'SMA / Sederajat (High School)',
    "Bachelor's Degree": "S1 / Sarjana (Bachelor's)",
    "Master's Degree": "S2 / Magister (Master's)",
    'Doctorate': 'S3 / Doktor (Doctorate)',
    'Associate Degree': 'D3 / Diploma (Associate)',
    'Vocational': 'Vokasi / SMK (Vocational)',
    'Certification': 'Sertifikasi (Certification)',
    'Some College Coursework Completed': 'Kuliah Belum Lulus',
    'Unspecified': 'Tidak Ditentukan (Unspecified)'
}
reverse_edu = {v: k for k, v in edu_translation.items()}

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

def show_predictor_page(model, encoders):
    """Renders the prediction page using the original Streamlit form layout."""
    
    st.title("Deteksi Lowongan Kerja Palsu", anchor=False)
    st.markdown('<div class="subtitle">Analisis instan keandalan lowongan kerja berdasarkan pola struktural dan kelengkapan informasi</div>', unsafe_allow_html=True)
    
    # We create the input form using columns
    with st.container():
        st.markdown('<div class="glass-card-marker"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown('<div class="form-section-title">Kategori & Karakteristik Struktural</div>', unsafe_allow_html=True)
            
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
            st.markdown('<div class="form-section-title">Fasilitas & Kelengkapan Profil</div>', unsafe_allow_html=True)
            
            # Checkbox columns (2 columns of 3 checkboxes each for a cleaner, un-wrapped look)
            check_col1, check_col2 = st.columns(2)
            with check_col1:
                telecommuting = st.checkbox("Mendukung Remote / WFH", value=False)
                has_company_logo = st.checkbox("Memiliki Logo Perusahaan", value=False)
                has_questions = st.checkbox("Memiliki Pertanyaan Screening", value=False)
            with check_col2:
                has_company_profile = st.checkbox("Memiliki Profil Perusahaan", value=False)
                has_requirements = st.checkbox("Memiliki Persyaratan Kerja", value=False)
                has_benefits = st.checkbox("Memiliki Fasilitas / Benefit", value=False)
                
            st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="form-section-title">Estimasi Panjang Karakter Informasi</div>', unsafe_allow_html=True)
            
            description_length = st.slider("Panjang Karakter Deskripsi Pekerjaan", min_value=0, max_value=5000, value=0, step=50)
            requirements_length = st.slider("Panjang Karakter Persyaratan Kerja", min_value=0, max_value=4000, value=0, step=50, disabled=not has_requirements)
            benefits_length = st.slider("Panjang Karakter Benefit Pekerjaan", min_value=0, max_value=3000, value=0, step=50, disabled=not has_benefits)
            company_profile_length = st.slider("Panjang Karakter Profil Perusahaan", min_value=0, max_value=4000, value=0, step=50, disabled=not has_company_profile)
        
        # Trigger button
        predict_btn = st.button("Menganalisis Keaslian Lowongan")
        
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
                
                st.markdown("### Hasil Analisis Model:")
                if prediction == 0:
                    real_prob = probabilities[0] * 100
                    st.markdown(f"""<div class="result-card-real">
<h3 style="color: #0a6e00; margin: 0 0 10px 0; font-weight: 700;">LOWONGAN KERJA INI VALID / ASLI</h3>
<p style="margin: 0; color: #3e4a38; font-size: 1.1rem;">
Model memprediksi dengan tingkat keyakinan <strong>{real_prob:.2f}%</strong> bahwa lowongan ini aman dan terpercaya.
</p>
</div>""", unsafe_allow_html=True)
                else:
                    fake_prob = probabilities[1] * 100
                    st.markdown(f"""<div class="result-card-fake">
<h3 style="color: #ba1a1a; margin: 0 0 10px 0; font-weight: 700;">PERINGATAN: LOWONGAN KERJA TERINDIKASI PALSU / FRAUD</h3>
<p style="margin: 0; color: #3e4a38; font-size: 1.1rem;">
Model memprediksi dengan tingkat keyakinan <strong>{fake_prob:.2f}%</strong> bahwa lowongan ini memiliki kecocokan pola penipuan.
</p>
</div>""", unsafe_allow_html=True)
