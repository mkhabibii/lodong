import streamlit as st
import pandas as pd
import numpy as np
import time

# TRANSLASI DROPDOWN KE BAHASA INDONESIA ---
emp_translation = {
    'Full-time': 'Penuh Waktu (Full-time)',
    'Part-time': 'Paruh Waktu (Part-time)',
    'Contract': 'Kontrak (Contract)',
    'Temporary': 'Sementara (Temporary)',
    'Other': 'Lainnya (Other)',
    'Unspecified': 'Tidak Ditentukan (Unspecified)'
}

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

def show_predictor_page(pipeline):
    """Renders the prediction page using the pipeline models and custom UI styling."""
    
    st.title("Deteksi Lowongan Kerja Palsu", anchor=False)
    st.markdown('<div class="subtitle">Analisis instan keandalan lowongan kerja berdasarkan pola struktural dan kelengkapan informasi</div>', unsafe_allow_html=True)
    
    # Extract options dynamically from pipeline preprocessor categories
    categories = pipeline.named_steps['preprocessor'].named_transformers_['cat'].categories_
    country_options = list(categories[0])
    emp_options = list(categories[1])
    exp_options = list(categories[2])
    edu_options = list(categories[3])
    ind_options = list(categories[4])
    func_options = list(categories[5])

    # We create the input form using containers
    with st.container():
        st.markdown('<div class="glass-card-marker"></div>', unsafe_allow_html=True)
        
        # Opsi A: Metode Hybrid Autocomplete / Text Selectbox + Manual Input
        popular_titles = sorted([
            "Software Engineer", "English Teacher Abroad", "Customer Service Associate",
            "Account Manager", "Web Developer", "Project Manager", "Administrative Assistant",
            "Product Manager", "Office Manager", "Marketing Manager", "Sales Representative",
            "iOS Developer", "Senior Software Engineer", "Web Designer", "Account Executive",
            "Customer Service Team Lead", "Front End Developer", "Sales Manager",
            "Software Developer", "Android Developer", "Data Scientist", "Data Analyst",
            "Financial Analyst", "Recruiter", "Human Resources Manager"
        ])
        
        # Selectbox dengan fitur pencarian bawaan Streamlit
        selected_title_option = st.selectbox(
            "Judul Pekerjaan (Job Title) - Pilih Populer atau Ketik Baru",
            options=["Lainnya (Ketik Manual)..."] + popular_titles,
            index=0,
            help="Gunakan fitur pencarian pada pilihan untuk mencari judul pekerjaan populer. Jika tidak ada di daftar, pilih 'Lainnya (Ketik Manual)...' untuk mengetik judul pekerjaan baru."
        )
        
        # Kondisi input manual jika memilih "Lainnya"
        if selected_title_option == "Lainnya (Ketik Manual)...":
            title_input = st.text_input(
                "Masukkan Judul Pekerjaan Secara Manual",
                value="",
                placeholder="Contoh: Staff Administrasi Kantor / Backend Developer"
            )
        else:
            title_input = selected_title_option
            
        title_length = len(title_input)
        
        st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown('<div class="form-section-title">Kategori & Karakteristik Struktural</div>', unsafe_allow_html=True)
            
            # Country Display
            country_display_options = [get_country_display(c) for c in country_options]
            selected_country_display = st.selectbox(
                "Negara Lokasi Kerja", 
                options=country_display_options, 
                index=country_display_options.index(get_country_display('US')) if get_country_display('US') in country_display_options else 0
            )
            selected_country = country_options[country_display_options.index(selected_country_display)]
            
            # Employment Type
            emp_display_options = [emp_translation.get(e, e) for e in emp_options]
            selected_emp_display = st.selectbox(
                "Jenis Pekerjaan (Employment Type)", 
                options=emp_display_options, 
                index=emp_display_options.index(emp_translation.get('Full-time', 'Full-time')) if 'Full-time' in emp_options else 0
            )
            selected_employment = emp_options[emp_display_options.index(selected_emp_display)]
            
            # Required Experience
            exp_display_options = [exp_translation.get(e, e) for e in exp_options]
            selected_exp_display = st.selectbox(
                "Pengalaman Kerja Minimal", 
                options=exp_display_options, 
                index=exp_display_options.index(exp_translation.get('Unspecified', 'Unspecified')) if 'Unspecified' in exp_options else 0
            )
            selected_experience = exp_options[exp_display_options.index(selected_exp_display)]
            
            # Required Education
            edu_display_options = [edu_translation.get(e, e) for e in edu_options]
            selected_edu_display = st.selectbox(
                "Pendidikan Minimal", 
                options=edu_display_options, 
                index=edu_display_options.index(edu_translation.get('Unspecified', 'Unspecified')) if 'Unspecified' in edu_options else 0
            )
            selected_education = edu_options[edu_display_options.index(selected_edu_display)]
            
            # Industry & Function
            selected_industry = st.selectbox(
                "Kategori Industri", 
                options=ind_options, 
                index=ind_options.index('Unspecified') if 'Unspecified' in ind_options else 0
            )
            selected_function = st.selectbox(
                "Fungsi / Bidang Pekerjaan", 
                options=func_options, 
                index=func_options.index('Unspecified') if 'Unspecified' in func_options else 0
            )
            
        with col2:
            st.markdown('<div class="form-section-title">Fasilitas & Kelengkapan Profil</div>', unsafe_allow_html=True)
            
            # Checkbox columns: 2 columns of 4 checkboxes for balanced UI look
            check_col1, check_col2 = st.columns(2)
            with check_col1:
                telecommuting = st.checkbox("Mendukung Remote / WFH", value=False)
                has_company_logo = st.checkbox("Memiliki Logo Perusahaan", value=False)
                has_questions = st.checkbox("Memiliki Pertanyaan Screening", value=False)
                has_department = st.checkbox("Ada Departemen Tertera", value=False)
            with check_col2:
                has_company_profile = st.checkbox("Memiliki Profil Perusahaan", value=False)
                has_requirements = st.checkbox("Memiliki Persyaratan Kerja", value=False)
                has_benefits = st.checkbox("Memiliki Fasilitas / Benefit", value=False)
                has_salary_range = st.checkbox("Ada Gaji Tertera", value=False)
                
            st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="form-section-title">Estimasi Panjang Karakter Informasi</div>', unsafe_allow_html=True)
            
            description_length = st.slider("Panjang Karakter Deskripsi Pekerjaan", min_value=0, max_value=5000, value=0, step=50)
            requirements_length = st.slider("Panjang Karakter Persyaratan Kerja", min_value=0, max_value=4000, value=0, step=50, disabled=not has_requirements)
            benefits_length = st.slider("Panjang Karakter Benefit Pekerjaan", min_value=0, max_value=3000, value=0, step=50, disabled=not has_benefits)
            company_profile_length = st.slider("Panjang Karakter Profil Perusahaan", min_value=0, max_value=4000, value=0, step=50, disabled=not has_company_profile)
            
            # Failsafes: reset lengths if checkboxes are unchecked
            if not has_company_profile:
                company_profile_length = 0
            if not has_requirements:
                requirements_length = 0
            if not has_benefits:
                benefits_length = 0
        
        st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)
        
        # Calculate completeness score and missing count dynamically
        info_presence = [
            1 if has_company_profile else 0,
            1 if has_salary_range else 0,
            1 if has_requirements else 0,
            1 if has_benefits else 0,
            1 if selected_employment != 'Unspecified' else 0,
            1 if selected_experience != 'Unspecified' else 0,
            1 if selected_education != 'Unspecified' else 0,
            1 if selected_industry != 'Unspecified' else 0,
            1 if selected_function != 'Unspecified' else 0
        ]
        completeness_score = sum(info_presence) / 9.0
        missing_count = 9 - sum(info_presence)

        # Trigger button
        predict_btn = st.button("Menganalisis Keaslian Lowongan")
        
        if predict_btn:
            with st.spinner("Menganalisis pola karakteristik lowongan kerja..."):
                time.sleep(1.0) # Simulation for premium feel
                
                # Format into input DataFrame with EXACT order and names as training columns
                input_df = pd.DataFrame([{
                    'telecommuting': 1 if telecommuting else 0,
                    'has_company_logo': 1 if has_company_logo else 0,
                    'has_questions': 1 if has_questions else 0,
                    'employment_type': selected_employment,
                    'required_experience': selected_experience,
                    'required_education': selected_education,
                    'industry': selected_industry,
                    'function': selected_function,
                    'country': selected_country,
                    'has_company_profile': 1 if has_company_profile else 0,
                    'has_requirements': 1 if has_requirements else 0,
                    'has_benefits': 1 if has_benefits else 0,
                    'has_salary_range': 1 if has_salary_range else 0,
                    'has_department': 1 if has_department else 0,
                    'description_length': description_length,
                    'requirements_length': requirements_length,
                    'benefits_length': benefits_length,
                    'company_profile_length': company_profile_length,
                    'title_length': title_length,
                    'completeness_score': completeness_score,
                    'missing_count': missing_count
                }])
                
                # Predict
                prediction = pipeline.predict(input_df)[0]
                probabilities = pipeline.predict_proba(input_df)[0]
                
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
<h3 style="color: #ba1a1a; margin: 0 0 10px 0; font-weight: 700;">PERINGATAN ! LOWONGAN KERJA TERINDIKASI PALSU / FRAUD</h3>
<p style="margin: 0; color: #3e4a38; font-size: 1.1rem;">
Model memprediksi dengan tingkat keyakinan <strong>{fake_prob:.2f}%</strong> bahwa lowongan ini memiliki kecocokan pola penipuan.
</p>
</div>""", unsafe_allow_html=True)
