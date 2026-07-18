import streamlit as st
import base64
import os

def inject_custom_css():
    """Injects custom premium CSS styles into the Streamlit app to match the visual design."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* General Page Overrides */
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            overflow-x: hidden !important;
        }
        
        .stApp, section.main, .main, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            background: #ffffff !important;
            background-color: #ffffff !important;
            color: #001e00 !important;
            overflow-x: hidden !important;
        }
        
        .block-container {
            display: flex !important;
            flex-direction: column !important;
            min-height: calc(100vh - 120px) !important;
            padding-top: 100px !important;
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        
        /* Page Titles & Subtitles */
        h1, .main-title {
            font-family: 'Inter', sans-serif !important;
            font-size: 32px !important;
            font-weight: 600 !important;
            line-height: 40px !important;
            letter-spacing: -0.01em !important;
            color: #001e00 !important;
            text-align: center !important;
            margin: 0 auto 15px auto !important;
            display: block !important;
        }
        .subtitle {
            font-family: 'Inter', sans-serif !important;
            color: #3e4a38 !important;
            font-size: 16px !important;
            font-weight: 400 !important;
            line-height: 24px !important;
            max-width: 750px !important;
            margin: 0 auto 40px auto !important;
            text-align: center !important;
            display: block !important;
        }
        
        /* Hide Default Streamlit UI Elements */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        header {
            visibility: hidden !important;
            height: 0px !important;
        }
        footer {
            visibility: hidden !important;
            height: 0px !important;
        }
        .stDeployButton {
            display: none !important;
        }
        
        /* Navbar Styling */
        .custom-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;
            border-bottom: 1px solid #e4ebe4;
            padding: 15px 40px;
            max-width: 1200px;
            z-index: 9999;
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
        }
        .nav-logo {
            font-weight: 800;
            font-size: 1.3rem;
            color: #14a800 !important;
            letter-spacing: 0.5px;
            text-decoration: none !important;
        }
        .nav-links {
            display: flex;
            gap: 30px;
            align-items: center;
        }
        .nav-link {
            color: #1a1c1c !important;
            font-weight: 500;
            font-size: 0.95rem;
            text-decoration: none !important;
            transition: color 0.2s ease;
        }
        .nav-link:hover, .nav-link.active {
            color: #14a800 !important;
            border-bottom: 2px solid #14a800;
            padding-bottom: 4px;
        }
        .nav-btn {
            background-color: #14a800;
            color: #ffffff !important;
            font-weight: 600;
            font-size: 0.9rem;
            padding: 8px 20px;
            border-radius: 8px;
            text-decoration: none !important;
            transition: all 0.2s ease;
        }
        .nav-btn:hover {
            background-color: #0a6e00;
        }
        
        /* Hero Section */
        .hero-container {
            text-align: center;
            padding: 60px 20px 80px 20px;
            background: transparent;
            margin-bottom: 40px;
        }
        .badge-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background-color: rgba(20, 168, 0, 0.08);
            color: #0a6e00;
            border-radius: 20px;
            padding: 6px 14px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 25px;
            border: 1px solid rgba(20, 168, 0, 0.15);
        }
        .hero-title {
            font-family: 'Inter', sans-serif !important;
            font-size: 40px !important;
            font-weight: 600 !important;
            line-height: 48px !important;
            letter-spacing: -0.02em !important;
            color: #1a1c1c !important;
            max-width: 800px;
            margin: 0 auto 20px auto !important;
            text-align: center !important;
        }
        .hero-subtitle {
            color: #3e4a38 !important;
            font-size: 16px !important;
            font-weight: 400 !important;
            line-height: 24px !important;
            max-width: 650px;
            margin: 0 auto 35px auto !important;
            text-align: center !important;
        }
        .hero-btns {
            display: flex;
            justify-content: center;
            gap: 16px;
            margin-top: 30px;
        }
        .hero-btn-primary {
            background: #14a800 !important;
            color: #ffffff !important;
            font-weight: 600;
            padding: 12px 28px;
            border-radius: 8px;
            font-size: 1rem;
            text-decoration: none !important;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: background-color 0.2s ease;
        }
        .hero-btn-primary:hover {
            background-color: #0a6e00 !important;
        }
        .hero-btn-secondary {
            background: #ffffff !important;
            color: #1a1c1c !important;
            border: 1px solid #e4ebe4 !important;
            font-weight: 600;
            padding: 12px 28px;
            border-radius: 8px;
            font-size: 1rem;
            text-decoration: none !important;
            display: inline-flex;
            align-items: center;
            transition: background-color 0.2s ease;
        }
        .hero-btn-secondary:hover {
            background-color: #f9f9f9 !important;
            border-color: #dadada !important;
        }
        
        /* Features Area "Karakteristik yang Dianalisis" */
        .features-grid-3 {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 24px;
            max-width: 1200px;
            margin: 0 auto 80px auto;
            text-align: left;
        }
        .feature-card-item {
            background: #ffffff;
            border: 1px solid #e4ebe4;
            border-radius: 12px;
            padding: 30px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            transition: border-color 0.2s ease;
        }
        .feature-card-item:hover {
            border-color: #bdcbb3;
        }
        .feature-card-icon-box {
            width: 40px;
            height: 40px;
            background: rgba(20, 168, 0, 0.06);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #14a800;
        }
        .feature-card-title {
            font-family: 'Inter', sans-serif !important;
            font-size: 20px !important;
            font-weight: 600 !important;
            color: #1a1c1c !important;
            margin: 0 !important;
        }
        .feature-card-desc {
            color: #3e4a38;
            font-size: 14px;
            line-height: 20px;
            margin: 0 !important;
        }
        
        /* Bagaimana AI Kami Bekerja? */
        .how-it-works-section {
            display: flex;
            gap: 60px;
            margin: 80px 0;
            align-items: center;
            text-align: left;
        }
        .process-list {
            display: flex;
            flex-direction: column;
            gap: 30px;
            flex: 1.1;
        }
        .process-step {
            display: flex;
            gap: 16px;
            align-items: flex-start;
        }
        .process-dot {
            width: 12px;
            height: 12px;
            background-color: #14a800;
            border-radius: 50%;
            margin-top: 6px;
            flex-shrink: 0;
        }
        .process-content h4 {
            font-size: 1.15rem;
            font-weight: 700;
            color: #1a1c1c;
            margin: 0 0 6px 0;
        }
        .process-content p {
            color: #3e4a38;
            font-size: 0.95rem;
            margin: 0;
            line-height: 1.5;
        }
        
        /* Mock Simulation Card */
        .mock-sim-container {
            flex: 0.9;
            display: flex;
            justify-content: center;
        }
        .mock-sim-card {
            background: #ffffff;
            border: 1px solid #e4ebe4;
            border-radius: 12px;
            padding: 24px;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 10px 30px rgba(0, 30, 0, 0.02);
            text-align: left;
        }
        .mock-sim-header {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            font-weight: 700;
            color: #6e7b67;
            border-bottom: 1px solid #e4ebe4;
            padding-bottom: 12px;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .mock-sim-progress-block {
            margin-bottom: 20px;
        }
        .mock-sim-label-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            font-weight: 700;
            color: #1a1c1c;
            margin-bottom: 8px;
        }
        .mock-sim-bar-container {
            height: 8px;
            background-color: #f3f3f3;
            border-radius: 4px;
            overflow: hidden;
        }
        .mock-sim-bar-fill {
            height: 100%;
            background-color: #14a800;
            border-radius: 4px;
        }
        .mock-result-pill {
            background-color: rgba(20, 168, 0, 0.08);
            border: 1px solid rgba(20, 168, 0, 0.15);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            margin-top: 30px;
        }
        .mock-result-pill p {
            margin: 0;
            font-size: 0.75rem;
            font-weight: 700;
            color: #14a800;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .mock-result-pill h3 {
            margin: 4px 0 0 0;
            font-size: 1.6rem;
            font-weight: 800;
            color: #14a800;
            letter-spacing: 0.5px;
        }
        
        /* Green Stats Band */
        .green-stats-band {
            background-color: #14a800;
            color: #ffffff;
            border-radius: 12px;
            padding: 40px 20px;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 40px;
            text-align: center;
            margin: 60px 0 80px 0;
        }
        .stat-band-item h3 {
            font-size: 2.5rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0 0 5px 0;
            line-height: 1.1;
        }
        .stat-band-item p {
            font-size: 0.8rem;
            font-weight: 700;
            color: #aad19c;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Call to Action Section */
        .cta-card-box {
            background-color: #f3f3f3;
            border: 1px solid #e4ebe4;
            border-radius: 16px;
            padding: 60px 30px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-bottom: 80px;
        }
        .cta-card-icon-box {
            width: 48px;
            height: 48px;
            background-color: #0a6e00;
            color: #ffffff;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 24px;
        }
        .cta-card-title {
            font-size: 1.8rem;
            font-weight: 600;
            color: #1a1c1c;
            margin-bottom: 12px;
        }
        .cta-card-desc {
            font-size: 1rem;
            color: #3e4a38;
            max-width: 600px;
            line-height: 1.6;
            margin-bottom: 30px;
        }
        
        /* Premium Flat Card Definition */
        .glass-card {
            background: #ffffff !important;
            border: 1px solid #e4ebe4 !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: none !important;
            color: #001e00 !important;
            margin-bottom: 25px !important;
            transition: border-color 0.2s ease !important;
        }
        .glass-card:hover {
            border-color: #bdcbb3 !important;
        }
        
        /* Prediction Form Layout CSS Overrides */
        .block-container [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"]:has(.glass-card-marker) {
            background: #ffffff !important;
            border: 1px solid #e4ebe4 !important;
            border-radius: 16px !important;
            padding: 40px !important;
            box-shadow: none !important;
            margin-bottom: 30px !important;
        }
        
        .form-card-title {
            font-family: 'Inter', sans-serif !important;
            font-size: 24px !important;
            font-weight: 600 !important;
            line-height: 32px !important;
            color: #001e00 !important;
            margin-top: 0 !important;
            margin-bottom: 30px !important;
            border-bottom: 1px solid #e4ebe4 !important;
            padding-bottom: 15px !important;
        }

        /* Form Subsections */
        .form-section-title {
            font-family: 'Inter', sans-serif !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            color: #14a800 !important;
            margin-top: 0 !important;
            margin-bottom: 25px !important;
            text-transform: uppercase !important;
            border-left: 3px solid #14a800 !important;
            padding-left: 10px !important;
        }
        
        .form-divider {
            height: 1px !important;
            background: #e4ebe4 !important;
            margin: 30px 0 !important;
        }

        /* Prediction Results Cards */
        .result-card-real {
            background: rgba(20, 168, 0, 0.04) !important;
            border: 1px solid rgba(20, 168, 0, 0.15) !important;
            border-radius: 8px !important;
            padding: 30px !important;
            margin-top: 35px !important;
            text-align: center !important;
            box-shadow: none !important;
        }
        
        .result-card-fake {
            background: rgba(186, 26, 26, 0.04) !important;
            border: 1px solid rgba(186, 26, 26, 0.15) !important;
            border-radius: 8px !important;
            padding: 30px !important;
            margin-top: 35px !important;
            text-align: center !important;
            box-shadow: none !important;
        }

        /* Streamlit Button Override */
        .stButton > button {
            background: #14a800 !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            padding: 14px 30px !important;
            border-radius: 8px !important;
            font-size: 1.05rem !important;
            border: none !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            background-color: #0a6e00 !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }

        /* Custom Streamlit Spinner Override */
        div[data-testid="stSpinner"] {
            background: #ffffff !important;
            border: 1px solid #e4ebe4 !important;
            border-radius: 8px !important;
            padding: 30px !important;
            box-shadow: none !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            gap: 20px !important;
            margin: 40px auto !important;
            max-width: 500px !important;
        }
        
        div[data-testid="stSpinner"] svg {
            width: 50px !important;
            height: 50px !important;
            color: #14a800 !important;
            animation: rotate-spinner 1.5s linear infinite !important;
        }
        
        div[data-testid="stSpinner"] > div {
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            color: #001e00 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        @keyframes rotate-spinner {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Mobile Responsive Overrides */
        @media (max-width: 600px) {
            /* 1. Navbar Mobile Optimization */
            .custom-navbar {
                padding: 10px 16px !important;
                top: 15px !important;
                width: calc(100% - 30px) !important;
            }
            .nav-logo {
                font-size: 1.15rem !important;
            }
            .nav-links {
                gap: 15px !important;
            }
            .nav-link {
                font-size: 0.85rem !important;
            }
            .nav-btn {
                display: none !important;
            }
            
            /* 2. Hero & Titles Mobile Typography */
            .hero-title {
                font-size: 28px !important;
                line-height: 36px !important;
            }
            .hero-subtitle {
                font-size: 0.95rem !important;
                padding: 0 10px !important;
            }
            .main-title {
                font-size: 24px !important;
            }
            .subtitle {
                font-size: 0.95rem !important;
                margin: 0 auto 30px auto !important;
            }
            
            /* 3. Form Card Mobile Padding Adjustment */
            .block-container [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"]:has(.glass-card-marker) {
                padding: 24px 20px !important;
                border-radius: 16px !important;
            }
            .form-card-title {
                font-size: 1.3rem !important;
                margin-bottom: 20px !important;
            }
            
            /* 4. CTA Banner Typography */
            .cta-title {
                font-size: 1.8rem !important;
            }
            .cta-subtitle {
                font-size: 0.95rem !important;
                max-width: 100% !important;
            }
            
            /* 5. Block Container Padding (Account for navbar height) */
            .block-container {
                padding-top: 85px !important;
            }

            /* Landing Layout Responsive Overrides */
            .features-grid-3 {
                grid-template-columns: 1fr !important;
            }
            .how-it-works-section {
                flex-direction: column !important;
                gap: 30px !important;
            }
            .green-stats-band {
                grid-template-columns: 1fr !important;
                gap: 30px !important;
            }
            .mock-sim-card {
                max-width: 100% !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def get_logo_base64():
    """Reads the logo.png from root and returns its base64 string."""
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception:
            return ""
    return ""

def render_navbar(active_page="beranda"):
    """Renders the custom top navigation bar."""
    home_active = "active" if active_page == "beranda" else ""
    predict_active = "active" if active_page == "prediksi" else ""
    tentang_active = "active" if active_page == "tentang" else ""
    
    logo_base64 = get_logo_base64()
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" height="28" style="vertical-align: middle; max-height: 28px; display: block;"/>'
    else:
        logo_html = 'LODONG'
        
    st.markdown(f"""<div class="custom-navbar">
<a href="?page=beranda" target="_self" class="nav-logo" style="display: flex; align-items: center; text-decoration: none !important;">{logo_html}</a>
<div class="nav-links">
<a href="?page=beranda" target="_self" class="nav-link {home_active}">Beranda</a>
<a href="?page=prediksi" target="_self" class="nav-link {predict_active}">Prediksi</a>
<a href="?page=tentang" target="_self" class="nav-link {tentang_active}">Tentang</a>
</div>
<a href="?page=prediksi" target="_self" class="nav-btn">Cek Loker</a>
</div>""", unsafe_allow_html=True)

def render_footer():
    """Renders the custom simplified footer containing only copyright and github repo link."""
    logo_base64 = get_logo_base64()
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" height="20" style="vertical-align: middle; max-height: 20px; display: block;"/>'
    else:
        logo_html = '<span style="font-weight: 800; color: #14a800; font-family: \'Inter\', sans-serif;">LODONG</span>'
        
    st.markdown(f"""<div class="custom-footer" style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 50px auto 0 auto; padding: 20px 40px; border-top: 1px solid #e4ebe4; background: #ffffff;">
<div style="display: flex; align-items: center; gap: 10px;">
    {logo_html}
    <span style="color: #bdcbb3;">|</span>
    <span style="margin: 0; color: #6e7b67; font-size: 0.9rem; font-family: 'Inter', sans-serif;">Copyright Team LODONG 2026</span>
</div>
<a href="#" style="color: #6e7b67; text-decoration: none; font-size: 0.9rem; font-family: 'Inter', sans-serif;">Kebijakan Privasi</a>
</div>""", unsafe_allow_html=True)
