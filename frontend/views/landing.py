import streamlit as st

def show_landing_page():
    """Renders the custom designed Landing Page with zero leading whitespace in HTML blocks to prevent Markdown code block rendering bugs."""
    
    #Hero Section
    st.markdown("""<div class="hero-container">
<h1 class="hero-title">Kenali Lowongan Kerja<br><span>Palsu</span> Sebelum Terlambat</h1>
<p class="hero-subtitle">LODONG mengandalkan deteksi lowongan secara real-time. Deteksi kecocokan untuk meminimalisir adanya penipuan sebelum terjadi.</p>
<a href="?page=prediksi" target="_self" class="hero-btn">
Mulai Test Sekarang <span>→</span>
</a>
</div>""", unsafe_allow_html=True)
    
    #About Us Section
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("""<div class="about-image-container">
<div class="about-globe">
<!-- Glowing Animated Globe SVG -->
<svg width="200" height="200" viewBox="0 0 100 100" style="animation: rotate 15s linear infinite;">
<style>
@keyframes rotate { 100% { transform: rotate(360deg); } }
</style>
<circle cx="50" cy="50" r="40" stroke="#6366f1" stroke-width="1" fill="none" opacity="0.3" stroke-dasharray="4 4" />
<circle cx="50" cy="50" r="35" stroke="#312e81" stroke-width="1.5" fill="none" />
<!-- Grid Lines -->
<path d="M 15 50 Q 50 20 85 50" stroke="#6366f1" stroke-width="0.8" fill="none" opacity="0.5" />
<path d="M 15 50 Q 50 80 85 50" stroke="#6366f1" stroke-width="0.8" fill="none" opacity="0.5" />
<path d="M 50 15 Q 20 50 50 85" stroke="#6366f1" stroke-width="0.8" fill="none" opacity="0.5" />
<path d="M 50 15 Q 80 50 50 85" stroke="#6366f1" stroke-width="0.8" fill="none" opacity="0.5" />
<line x1="10" y1="50" x2="90" y2="50" stroke="#312e81" stroke-width="1" opacity="0.8" />
<line x1="50" y1="10" x2="50" y2="90" stroke="#312e81" stroke-width="1" opacity="0.8" />
<!-- Glowing dots -->
<circle cx="28" cy="30" r="2" fill="#818cf8" />
<circle cx="72" cy="70" r="2.5" fill="#a5b4fc" />
<circle cx="50" cy="20" r="1.5" fill="#818cf8" />
<circle cx="45" cy="75" r="2" fill="#6366f1" />
</svg>
</div>
</div>""", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""<div class="about-content">
<div class="about-tag">Tentang Kami</div>
<h2 class="about-title">LODONG</h2>
<p class="about-text">LODONG adalah platform cerdas berbasis Machine Learning (algoritma Random Forest) yang didedikasikan untuk mendeteksi keabsahan postingan lowongan pekerjaan secara instan. Kami mengevaluasi integritas informasi, ketersediaan logo, kelengkapan profil perusahaan, dan panjang deskripsi struktural untuk melindungimu dari risiko penipuan berkedok rekrutmen kerja.</p>
</div>""", unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
        
    # Optimization Section
    st.markdown("""<div class="opt-section">
<div class="opt-tag">Fitur Lodong</div>
<div class="features-scroll-container">
<!-- Card 1 -->
<div class="feature-scroll-card">
<div class="bento-tag" style="color: #818cf8;">Klasifikasi Real-Time</div>
<h3 class="bento-title">Klasifikasi Instan</h3>
<p class="bento-desc">Memprediksi validitas lowongan pekerjaan hanya dalam beberapa detik menggunakan analisis parameter struktural tanpa pemrosesan NLP yang berat.</p>
<div class="bento-nodes" style="margin-top: auto;">
<div class="bento-node" style="border-color: rgba(129, 140, 248, 0.2); color: #818cf8;">Real-Time</div>
<div class="bento-node" style="border-color: rgba(129, 140, 248, 0.2); color: #818cf8;">Instan</div>
</div>
</div>
<!-- Card 2 -->
<div class="feature-scroll-card">
<div class="bento-tag" style="color: #fbbf24;">Kecerdasan Buatan</div>
<h3 class="bento-title">Deteksi Cerdas</h3>
<p class="bento-desc">Model dilatih secara khusus dengan algoritma Random Forest untuk mendeteksi pola penipuan secara akurat berdasarkan ketidaklengkapan data.</p>
<div class="bento-nodes" style="margin-top: auto;">
<div class="bento-node" style="border-color: rgba(251, 191, 36, 0.2); color: #fbbf24;">Random Forest</div>
<div class="bento-node" style="border-color: rgba(251, 191, 36, 0.2); color: #fbbf24;">Ensemble</div>
</div>
</div>
<!-- Card 3 -->
<div class="feature-scroll-card">
<div class="bento-tag" style="color: #a78bfa;">Validasi Informasi</div>
<h3 class="bento-title">Analisis Kelengkapan</h3>
<p class="bento-desc">Menguji kelengkapan data penting seperti ketersediaan logo, profil deskripsi perusahaan, dan keberadaan screening questions.</p>
<div class="bento-nodes" style="margin-top: auto;">
<div class="bento-node" style="border-color: rgba(167, 139, 250, 0.2); color: #a78bfa;">Profil Logo</div>
<div class="bento-node" style="border-color: rgba(167, 139, 250, 0.2); color: #a78bfa;">Screening</div>
</div>
</div>
<!-- Card 4 -->
<div class="feature-scroll-card">
<div class="bento-tag" style="color: #10b981;">Aksesibilitas Tinggi</div>
<h3 class="bento-title">Desain UI Responsif</h3>
<p class="bento-desc">Antarmuka web interaktif yang modern, bersih, dan dioptimalkan secara khusus untuk kenyamanan para pencari kerja di berbagai perangkat.</p>
<div class="bento-nodes" style="margin-top: auto;">
<div class="bento-node" style="border-color: rgba(16, 185, 129, 0.2); color: #10b981;">Glassmorphism</div>
<div class="bento-node" style="border-color: rgba(16, 185, 129, 0.2); color: #10b981;">Responsive</div>
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)


