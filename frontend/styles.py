import streamlit as st

def inject_custom_css():
    """Injects custom premium CSS styles into the Streamlit app to match the visual design."""
    st.markdown("""
    <div id="page-loader">
        <div class="loader-ring"></div>
        <div class="loader-logo">LODONG</div>
    </div>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        /* Page Loader Styling */
        #page-loader {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: #0b0f19 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            z-index: 99999999 !important;
            opacity: 1;
            visibility: visible;
            gap: 20px !important;
            
            /* Pure CSS Loader Fadeout Animation */
            animation: fade-out-loader 0.5s ease-out forwards !important;
            animation-delay: 0.4s !important;
            pointer-events: none !important;
        }

        @keyframes fade-out-loader {
            0% {
                opacity: 1;
                visibility: visible;
            }
            99% {
                opacity: 0;
                visibility: visible;
            }
            100% {
                opacity: 0;
                visibility: hidden;
            }
        }
        
        .loader-logo {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            letter-spacing: 2px !important;
            background: linear-gradient(135deg, #ffffff 0%, #6366f1 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            animation: text-pulse 1.8s infinite ease-in-out !important;
        }
        
        .loader-ring {
            width: 60px !important;
            height: 60px !important;
            border: 3px solid rgba(99, 102, 241, 0.1) !important;
            border-radius: 50% !important;
            border-top-color: #6366f1 !important;
            animation: spin 1s linear infinite !important;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg) !important; }
        }
        
        @keyframes text-pulse {
            0%, 100% { opacity: 0.6 !important; transform: scale(0.98) !important; }
            50% { opacity: 1 !important; transform: scale(1.02) !important; }
        }
        
        /* General Page Overrides */
        html, body, [class*="css"]  {
            font-family: 'Plus Jakarta Sans', sans-serif;
            overflow-x: hidden !important;
        }
        
        .stApp, section.main, .main, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            background: radial-gradient(circle at top, #1c2966 0%, #0b0f19 65%) no-repeat fixed;
            background-color: #0b0f19;
            color: #f1f5f9;
            overflow-x: hidden !important;
        }
        
        .block-container {
            display: flex !important;
            flex-direction: column !important;
            min-height: calc(100vh - 120px) !important;
            padding-top: 100px !important;
        }
        
        /* Page Titles & Subtitles */
        .main-title {
            font-size: 2.8rem;
            font-weight: 800 !important;
            line-height: 1.2;
            color: #ffffff;
            text-align: center !important;
            margin: 0 auto 15px auto !important;
            display: block !important;
        }
        .subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
            max-width: 750px;
            margin: 0 auto 40px auto !important;
            line-height: 1.6;
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
            background: rgba(13, 17, 28, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 50px;
            padding: 10px 24px;
            max-width: 1000px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
            z-index: 9999;
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: calc(100% - 40px);
        }
        .nav-logo {
            font-weight: 800;
            font-size: 1.3rem;
            color: #ffffff;
            letter-spacing: 1px;
            text-decoration: none !important;
        }
        .nav-links {
            display: flex;
            gap: 30px;
            align-items: center;
        }
        .nav-link {
            color: #94a3b8;
            font-weight: 500;
            font-size: 0.95rem;
            text-decoration: none !important;
            transition: color 0.3s ease;
        }
        .nav-link:hover, .nav-link.active {
            color: #ffffff;
        }
        .nav-btn {
            background-color: #ffffff;
            color: #0b0f19 !important;
            font-weight: 600;
            font-size: 0.9rem;
            padding: 8px 20px;
            border-radius: 20px;
            text-decoration: none !important;
            transition: all 0.3s ease;
        }
        .nav-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
        }
        
        /* Hero Section */
        .hero-container {
            text-align: center;
            padding: 60px 20px 80px 20px;
            background: transparent;
            margin-bottom: 50px;
        }
        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.2;
            color: #ffffff;
            max-width: 800px;
            margin: 0 auto 20px auto !important;
            text-align: center !important;
        }
        .hero-title span {
            color: #6366f1;
            background: linear-gradient(45deg, #a5b4fc, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto 35px auto !important;
            line-height: 1.6;
            text-align: center !important;
        }
        .hero-btn {
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
            color: #ffffff !important;
            font-weight: 600;
            padding: 14px 30px;
            border-radius: 30px;
            font-size: 1.05rem;
            text-decoration: none !important;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        }
        .hero-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(99, 102, 241, 0.6);
        }
        
        /* Sponsors Area */
        .sponsors-title {
            text-align: center;
            color: #64748b;
            font-size: 0.8rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 25px;
        }
        .sponsors-grid {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 50px;
            flex-wrap: wrap;
            margin-bottom: 80px;
            opacity: 0.75;
        }
        .sponsor-item {
            color: #94a3b8;
            font-size: 1.1rem;
            font-weight: 700;
            letter-spacing: 1px;
        }
        
        /* About Us Section */
        .about-section {
            display: flex;
            align-items: center;
            gap: 60px;
            margin-bottom: 100px;
            padding: 0 10px;
        }
        .about-image-container {
            flex: 1;
            display: flex;
            justify-content: center;
        }
        .about-globe {
            width: 320px;
            height: 320px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, rgba(11,15,25,0) 70%);
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 50px rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(99, 102, 241, 0.1);
        }
        .about-content {
            flex: 1.2;
        }
        .about-tag {
            color: #6366f1;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .about-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 20px;
        }
        .about-text {
            color: #94a3b8;
            line-height: 1.7;
            margin-bottom: 30px;
        }
        .about-stats {
            display: flex;
            gap: 50px;
        }
        .stat-item h3 {
            font-size: 2.2rem;
            font-weight: 800;
            color: #6366f1;
            margin: 0 0 5px 0;
        }
        .stat-item p {
            color: #94a3b8;
            margin: 0;
            font-size: 0.9rem;
        }
        
        /* Optimization Section */
        .opt-section {
            text-align: center;
            margin-bottom: 100px;
        }
        .opt-tag {
            color: #6366f1;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .opt-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 40px;
        }
        .opt-title span {
            color: #6366f1;
        }
        /* Horizontal Scroll Features Container */
        .features-scroll-container {
            display: flex !important;
            gap: 24px;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch;
            padding: 20px 10px 30px 10px;
            scroll-snap-type: x mandatory;
            scrollbar-width: thin;
            scrollbar-color: rgba(255, 255, 255, 0.1) transparent;
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 auto;
            text-align: left;
            box-sizing: border-box;
        }
        
        .features-scroll-container::-webkit-scrollbar {
            height: 6px;
        }
        .features-scroll-container::-webkit-scrollbar-track {
            background: transparent;
        }
        .features-scroll-container::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        .features-scroll-container::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        
        .feature-scroll-card {
            flex: 0 0 320px; /* Fixed width for horizontal layout */
            border-radius: 24px;
            padding: 35px 30px;
            background: linear-gradient(135deg, rgba(16, 20, 38, 0.6) 0%, rgba(13, 17, 28, 0.85) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            scroll-snap-align: start;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            min-height: 280px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        
        .feature-scroll-card:hover {
            transform: translateY(-5px);
            border-color: rgba(99, 102, 241, 0.25);
            box-shadow: 0 15px 30px rgba(99, 102, 241, 0.12);
        }
        
        .bento-tag {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
        }
        
        .bento-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.3;
            margin: 0 0 12px 0;
        }
        
        .bento-desc {
            color: #94a3b8;
            font-size: 0.9rem;
            line-height: 1.6;
            margin: 0;
        }
        
        .bento-nodes {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }
        
        .bento-node {
            padding: 5px 12px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 20px;
            font-size: 0.75rem;
            color: #cbd5e1;
            font-weight: 500;
        }
        
        /* Comparison Section */
        .comp-section {
            text-align: center;
            margin-bottom: 100px;
        }
        .comp-tag {
            color: #6366f1;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .comp-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 50px;
        }
        .comp-title span {
            color: #6366f1;
        }
        
        /* Comparison Table Grid Layout */
        .comp-grid {
            display: grid;
            grid-template-columns: 1.2fr 1fr 1fr 1fr;
            gap: 20px;
            max-width: 1000px;
            margin: 0 auto;
            text-align: left;
        }
        .comp-headers-col {
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            padding: 20px 0;
        }
        .comp-header-label {
            color: #94a3b8;
            font-weight: 600;
            font-size: 0.95rem;
            height: 50px;
            display: flex;
            align-items: center;
        }
        .comp-card {
            border-radius: 20px;
            padding: 25px 20px;
            text-align: center;
            display: flex;
            flex-direction: column;
            gap: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        .comp-card.lodong-card {
            background: #0f1530;
            border: 2px solid #6366f1;
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.15);
        }
        .comp-card.white-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .comp-card-title {
            font-weight: 800;
            font-size: 1.1rem;
            margin-bottom: 10px;
        }
        .lodong-card .comp-card-title {
            color: #6366f1;
        }
        .comp-check-row {
            height: 50px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .icon-check {
            color: #10b981;
            font-size: 1.4rem;
            font-weight: 700;
        }
        .icon-cross {
            color: #f43f5e;
            font-size: 1.4rem;
            font-weight: 700;
        }
        
        /* Bottom CTA Section */
        .cta-banner {
            background: linear-gradient(rgba(11, 15, 25, 0.4), rgba(11, 15, 25, 0.8)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80');
            background-size: cover;
            background-position: center;
            border-radius: 50px 50px 0 0;
            text-align: center;
            margin-bottom: 100px;
            padding-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.5);
        }
        .cta-title {
            font-size: 2.5rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 15px;
            text-align: center;
        }
        .cta-subtitle {
            color: #cbd5e1;
            font-size: 1.1rem;
            max-width: 500px;
            margin: 0 auto 15px auto !important;
            line-height: 1.6;
            text-align: center;
        }
        
        /* Footer Styling */
        .custom-footer {
            background-color: #060911;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding: 30px 40px;
            text-align: center;
            margin-top: auto !important; /* Pushes the footer to the bottom */
            margin-left: -100px; /* Counteracting Streamlit padding */
            margin-right: -100px;
        }
        .footer-grid {
            display: grid;
            grid-template-columns: 1.5fr 1fr 1fr 1.2fr;
            gap: 40px;
            max-width: 1100px;
            margin: 0 auto 50px auto;
        }
        .footer-brand h3 {
            font-size: 1.4rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0 0 15px 0;
        }
        .footer-brand p {
            color: #64748b;
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        .footer-socials {
            display: flex;
            gap: 15px;
        }
        .social-icon {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.05);
            color: #94a3b8;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }
        .social-icon:hover {
            background: #6366f1;
            color: #ffffff;
        }
        .footer-col h4 {
            font-size: 0.95rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #ffffff;
            margin: 0 0 20px 0;
        }
        .footer-links {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .footer-link {
            color: #64748b;
            text-decoration: none !important;
            font-size: 0.9rem;
            transition: color 0.3s ease;
        }
        .footer-link:hover {
            color: #ffffff;
        }
        .footer-contact h4 {
            font-size: 0.95rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #ffffff;
            margin: 0 0 20px 0;
        }
        .footer-email {
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            text-decoration: none !important;
            margin-bottom: 8px;
            display: block;
        }
        .footer-contact p {
            color: #64748b;
            font-size: 0.85rem;
            margin: 0;
        }
        .footer-copyright {
            text-align: center;
            color: #475569;
            font-size: 0.8rem;
            border-top: 1px solid rgba(255, 255, 255, 0.03);
            padding-top: 30px;
            max-width: 1100px;
            margin: 0 auto;
        }
        
        /* Prediction Form Layout CSS Overrides */
        .block-container [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"]:has(.glass-card-marker) {
            background: rgba(13, 17, 28, 0.45) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 24px !important;
            padding: 40px !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            margin-bottom: 30px !important;
        }
        
        .form-card-title {
            font-size: 1.6rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            margin-top: 0 !important;
            margin-bottom: 30px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
            padding-bottom: 15px !important;
            letter-spacing: 0.5px !important;
        }

        /* Form Subsections */
        .form-section-title {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            color: #6366f1 !important;
            margin-top: 0 !important;
            margin-bottom: 25px !important;
            letter-spacing: 0.5px !important;
            text-transform: uppercase !important;
            border-left: 3px solid #6366f1 !important;
            padding-left: 10px !important;
        }
        
        .form-divider {
            height: 1px !important;
            background: rgba(255, 255, 255, 0.08) !important;
            margin: 30px 0 !important;
        }

        /* Prediction Results Cards */
        .result-card-real {
            background: rgba(16, 185, 129, 0.08) !important;
            border: 1px solid rgba(16, 185, 129, 0.2) !important;
            border-radius: 20px !important;
            padding: 30px !important;
            margin-top: 35px !important;
            text-align: center !important;
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.1) !important;
        }
        
        .result-card-fake {
            background: rgba(244, 63, 94, 0.08) !important;
            border: 1px solid rgba(244, 63, 94, 0.2) !important;
            border-radius: 20px !important;
            padding: 30px !important;
            margin-top: 35px !important;
            text-align: center !important;
            box-shadow: 0 8px 25px rgba(244, 63, 94, 0.1) !important;
        }

        /* Streamlit Button Override */
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            padding: 14px 30px !important;
            border-radius: 30px !important;
            font-size: 1.05rem !important;
            border: none !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
            color: #ffffff !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }

        /* Custom Streamlit Spinner Override */
        div[data-testid="stSpinner"] {
            background: rgba(13, 17, 28, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 20px !important;
            padding: 30px !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            gap: 20px !important;
            margin: 40px auto !important;
            max-width: 500px !important;
            animation: pulse-glow 2s infinite ease-in-out !important;
        }
        
        div[data-testid="stSpinner"] svg {
            width: 50px !important;
            height: 50px !important;
            color: #6366f1 !important;
            animation: rotate-spinner 1.5s linear infinite !important;
        }
        
        div[data-testid="stSpinner"] > div {
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            color: #ffffff !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            letter-spacing: 0.5px !important;
        }
        
        @keyframes rotate-spinner {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes pulse-glow {
            0%, 100% {
                border-color: rgba(255, 255, 255, 0.08);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            }
            50% {
                border-color: rgba(99, 102, 241, 0.3);
                box-shadow: 0 15px 35px rgba(99, 102, 241, 0.15);
            }
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
                display: none !important; /* Hide CTA button on mobile navbar to fit links */
            }
            
            /* 2. Hero & Titles Mobile Typography */
            .hero-title {
                font-size: 2.2rem !important;
                line-height: 1.3 !important;
            }
            .hero-subtitle {
                font-size: 0.95rem !important;
                padding: 0 10px !important;
            }
            .main-title {
                font-size: 1.8rem !important;
            }
            .subtitle {
                font-size: 0.95rem !important;
                margin: 0 auto 30px auto !important;
            }
            
            /* 3. Form Card Mobile Padding Adjustment */
            .block-container [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"]:has(.glass-card-marker) {
                padding: 24px 20px !important;
                border-radius: 20px !important;
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
        }
    </style>
    """, unsafe_allow_html=True)

def render_navbar(active_page="beranda"):
    """Renders the custom top navigation bar."""
    home_active = "active" if active_page == "beranda" else ""
    predict_active = "active" if active_page == "prediksi" else ""
    tentang_active = "active" if active_page == "tentang" else ""
    
    st.markdown(f"""<div class="custom-navbar">
<a href="?page=beranda" target="_self" class="nav-logo">LODONG</a>
<div class="nav-links">
<a href="?page=beranda" target="_self" class="nav-link {home_active}">Beranda</a>
<a href="?page=prediksi" target="_self" class="nav-link {predict_active}">Prediksi</a>
<a href="?page=tentang" target="_self" class="nav-link {tentang_active}">Tentang</a>
</div>
<a href="?page=prediksi" target="_self" class="nav-btn">Coba Prediksi</a>
</div>""", unsafe_allow_html=True)

def render_footer():
    """Renders the custom simplified footer containing only copyright and github repo link."""
    st.markdown("""<div class="custom-footer">
<p style="margin: 0; color: #64748b; font-size: 0.9rem; font-family: 'Plus Jakarta Sans', sans-serif;">
© 2026 LODONG AI. Seluruh hak cipta dilindungi undang-undang.
<span style="margin: 0 10px; color: #334155;">|</span>
<a href="https://github.com/mkhabibii/lodong" target="_blank" style="color: #6366f1; text-decoration: none; font-weight: 500;">GitHub Repository</a>
</p>
</div>""", unsafe_allow_html=True)
