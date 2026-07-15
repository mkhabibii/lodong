import streamlit as st
import joblib
import os

# Import custom frontend modules
from frontend.styles import inject_custom_css, render_navbar, render_footer
from frontend.views.landing import show_landing_page
from frontend.views.predictor import show_predictor_page
from frontend.views.dashboard import show_dashboard_page

# Set page configuration
st.set_page_config(
    page_title="LODONG - Kenali Lowongan Kerja Palsu",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject custom styling to hide default Streamlit layout and apply new styles
inject_custom_css()

# Helper function to load model and encoders safely and cache them
@st.cache_resource
def load_prediction_assets():
    model_path = 'models/model_random_forest.joblib'
    encoders_path = 'models/encoder_kategori.joblib'
    
    if os.path.exists(model_path) and os.path.exists(encoders_path):
        model = joblib.load(model_path)
        encoders = joblib.load(encoders_path)
        return model, encoders, True
    return None, None, False

# Load model and encoders
model, encoders, is_loaded = load_prediction_assets()

# Read active page from URL query parameters (default is "beranda")
active_page = st.query_params.get("page", "beranda")

# Render Custom Navbar
render_navbar(active_page)

# Render View Content
if active_page == "beranda":
    show_landing_page()
elif active_page == "prediksi":
    if not is_loaded:
        st.warning("⚠️ Berkas Model dan Encoder tidak ditemukan di folder `models/`. Harap selesaikan pelatihan model pada file notebook terlebih dahulu untuk menghasilkan berkas `model_random_forest.joblib` dan `encoder_kategori.joblib`.")
    else:
        show_predictor_page(model, encoders)
elif active_page == "dashboard":
    show_dashboard_page()
elif active_page == "tentang":
    # Custom About Page View
    st.markdown('<div class="main-title">Tentang LODONG (Loker Bodong) </div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Pelajari latar belakang pengembangan platform dan bagaimana kecerdasan buatan membantu menekan angka kejahatan siber rekrutmen.</div>', unsafe_allow_html=True)
    
    st.markdown("""<div style="background: rgba(13, 17, 28, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; padding: 40px; max-width: 800px; margin: 0 auto 50px auto; line-height: 1.8; color: #cbd5e1;">
<h3 style="color: #ffffff; font-weight: 700; margin-top: 0; margin-bottom: 20px;">Latar Belakang Proyek</h3>
<p>Banyaknya kasus penipuan berkedok lowongan kerja online sangat merugikan para pencari kerja. Lewat proyek UAS Data Mining ini (Universitas Alma Ata Yogyakarta), kami mengembangkan sistem yang bisa mendeteksi lowongan palsu secara instan hanya dengan melihat kelengkapan informasi dari postingan lowongan tersebut, tanpa perlu menggunakan analisis teks (NLP) yang berat.</p>
<h3 style="color: #ffffff; font-weight: 700; margin-top: 30px; margin-bottom: 20px;">Mengapa Random Forest?</h3>
<p>Model Random Forest terbukti paling pintar dalam uji coba eksperimen. Nilai <strong>Recall-nya mencapai 92.49%</strong>, yang berarti model ini bisa mendeteksi 92% lowongan palsu yang diuji. Di dunia nyata, kepekaan mendeteksi lowongan palsu adalah hal terpenting agar tidak ada korban penipuan yang lolos.</p>
<h3 style="color: #ffffff; font-weight: 700; margin-top: 30px; margin-bottom: 20px;">Tim Pengembang</h3>
<p>Dibuat dan dikembangkan oleh Muhammad Khoerul Habibi, Kholil Mustofa dan Faiz Faturrahman.</p>
</div>""", unsafe_allow_html=True)

# Render Custom Footer
render_footer()