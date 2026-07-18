import streamlit as st

def show_landing_page():
    """Renders the high-fidelity mock layout landing page matching the user's custom screenshot specification."""
    
    # 1. Hero Section
    st.markdown("""<div class="hero-container">
<h1 class="hero-title">Cek Keaslian Lowongan Kerja dalam Sekali Klik</h1>
<p class="hero-subtitle">Sistem kami mendeteksi potensi keaslian berdasarkan karakteristik informasi lowongan menggunakan Machine Learning untuk membantu Anda melakukan validasi mandiri sebelum memutuskan untuk melamar.</p>
<div class="hero-btns">
    <a href="?page=prediksi" target="_self" class="hero-btn-primary">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="margin-right: 4px;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
        Mulai Analisis
    </a>
    <a href="?page=prediksi" target="_self" class="hero-btn-secondary">
        Pelajari Metodologi
    </a>
</div>
</div>""", unsafe_allow_html=True)

    # 2. Features Section (Karakteristik yang Dianalisis)
    st.markdown("""<div style="text-align: center; margin-bottom: 50px;">
<h2 class="main-title">Karakteristik yang Dianalisis</h2>
<p class="subtitle">Model kami mengevaluasi berbagai fitur dari input lowongan kerja untuk menemukan pola indikasi keaslian.</p>
</div>
<div class="features-grid-3">
    <!-- Card 1 -->
    <div class="feature-card-item">
        <div class="feature-card-icon-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
        </div>
        <h3 class="feature-card-title">Analisis Struktural</h3>
        <p class="feature-card-desc">Memeriksa kesesuaian antara lokasi, industri, tingkat pendidikan minimum, dan pengalaman kerja.</p>
    </div>
    <!-- Card 2 -->
    <div class="feature-card-item">
        <div class="feature-card-icon-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        </div>
        <h3 class="feature-card-title">Kelengkapan Informasi</h3>
        <p class="feature-card-desc">Mengevaluasi kredibilitas lowongan dari kelengkapan profil perusahaan, keberadaan logo, dan kejelasan benefit.</p>
    </div>
    <!-- Card 3 -->
    <div class="feature-card-item">
        <div class="feature-card-icon-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
        </div>
        <h3 class="feature-card-title">Pola Kedalaman Teks</h3>
        <p class="feature-card-desc">Menganalisis indikasi keaslian dari panjang teks deskripsi pekerjaan serta persyaratan kerja yang dicantumkan.</p>
    </div>
</div>""", unsafe_allow_html=True)

    # 3. How It Works Section
    col1, col2 = st.columns([1.1, 0.9])
    
    with col1:
        st.markdown("""<div style="text-align: left; padding: 20px 0;">
<p style="font-size: 0.8rem; font-weight: 700; color: #14a800; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 10px 0;">PROSES KLASIFIKASI AI</p>
<h2 style="font-size: 2rem; font-weight: 600; color: #1a1c1c; margin: 0 0 35px 0;">Bagaimana AI Kami Bekerja?</h2>
<div class="process-list">
    <div class="process-step">
        <div class="process-dot"></div>
        <div class="process-content">
            <h4>1. Input Karakteristik</h4>
            <p>Pengguna memasukkan detail informasi lowongan kerja pada form yang tersedia sesuai dengan data yang ditemukan.</p>
        </div>
    </div>
    <div class="process-step">
        <div class="process-dot"></div>
        <div class="process-content">
            <h4>2. Klasifikasi Model</h4>
            <p>Algoritma Random Forest mempelajari kombinasi fitur untuk mendeteksi pola indikasi penipuan dari data historis.</p>
        </div>
    </div>
    <div class="process-step">
        <div class="process-dot"></div>
        <div class="process-content">
            <h4>3. Penjelasan & Rekomendasi</h4>
            <p>Sistem memberikan skor indikasi akhir beserta penjelasan dan saran tindakan verifikasi lanjutan untuk keamanan Anda.</p>
        </div>
    </div>
</div>
</div>""", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""<div class="mock-sim-container">
<div class="mock-sim-card">
    <div class="mock-sim-header">
        <span>● KLASIFIKASI MODEL...</span>
        <span>Random Forest Engine</span>
    </div>
    <div class="mock-sim-progress-block">
        <div class="mock-sim-label-row">
            <span>Keyakinan Model</span>
            <span style="color: #14a800;">96%</span>
        </div>
        <div class="mock-sim-bar-container">
            <div class="mock-sim-bar-fill" style="width: 96%;"></div>
        </div>
    </div>
    <div class="mock-sim-progress-block">
        <div class="mock-sim-label-row">
            <span>Skor Indikasi</span>
            <span style="color: #14a800;">Positif Sah</span>
        </div>
        <div class="mock-sim-bar-container">
            <div class="mock-sim-bar-fill" style="width: 85%;"></div>
        </div>
    </div>
    <div class="mock-result-pill">
        <p>Hasil Prediksi</p>
        <h3>TERPERCAYA</h3>
    </div>
</div>
</div>""", unsafe_allow_html=True)

    # 4. Green Stats Band
    st.markdown("""<div class="green-stats-band">
    <div class="stat-band-item">
        <h3>17,000+</h3>
        <p>Data Historis</p>
    </div>
    <div class="stat-band-item">
        <h3>Evaluasi</h3>
        <p>Terbimbing</p>
    </div>
    <div class="stat-band-item">
        <h3>Akurat</h3>
        <p>Skor Indikasi Awal</p>
    </div>
</div>""", unsafe_allow_html=True)

    # 5. Call to Action Box
    st.markdown("""<div class="cta-card-box">
    <h2 class="cta-card-title">Mulai Analisis Mandiri</h2>
    <p class="cta-card-desc">Gunakan instrumen identifikasi berbasis data untuk membantu Anda mengenali karakteristik lowongan kerja sebelum memberikan data pribadi.</p>
    <a href="?page=prediksi" target="_self" class="hero-btn-primary">
        Input Data Sekarang
    </a>
</div>""", unsafe_allow_html=True)
