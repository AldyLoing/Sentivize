"""
Sentivize Ultra - Advanced AI HR Analytics System
==================================================
Version 3.0 - Ultra Advanced Edition

Fitur Utama:
- Job Complexity Detection
- Flexible Scoring untuk Entry-Level
- CV Preview sebelum Analisis
- Human-like Reasoning
- Fresh Graduate Friendly
"""

import streamlit as st
import warnings
warnings.filterwarnings('ignore')

# Import pages
from ultra_employee_analyzer_page import render_ultra_employee_analyzer_page
from ultra_cv_analyzer_page import render_ultra_cv_analyzer_page


def main():
    """Main application"""
    
    # Page config
    st.set_page_config(
        page_title="Sentivize Ultra - AI HR Analytics",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        .version-badge {
            text-align: center;
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 12px 24px;
            background-color: #f0f2f6;
            border-radius: 8px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #667eea;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
        st.markdown("# Sentivize Ultra")
        st.markdown("### 🚀 AI HR Analytics")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigasi",
            ["🏠 Home", "👥 Employee Analyzer", "📄 CV Analyzer", "ℹ️ About"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Version info
        st.markdown("**Version:** 3.0 Ultra")
        st.markdown("**Status:** 🟢 Active")
        
        st.markdown("---")
        
        # Quick info
        st.markdown("### ⚡ Fitur Baru")
        st.markdown("""
        - ✅ Job Complexity Detector
        - ✅ CV Preview
        - ✅ Flexible Scoring
        - ✅ Fresh Grad Friendly
        - ✅ Human Reasoning
        """)
        
        st.markdown("---")
        st.caption("© 2024 Sentivize Ultra")
    
    # Main content
    if page == "🏠 Home":
        render_home_page()
    elif page == "👥 Employee Analyzer":
        render_ultra_employee_analyzer_page()
    elif page == "📄 CV Analyzer":
        render_ultra_cv_analyzer_page()
    elif page == "ℹ️ About":
        render_about_page()


def render_home_page():
    """Render home page"""
    
    st.markdown('<h1 class="main-header">Sentivize Ultra</h1>', unsafe_allow_html=True)
    st.markdown('<p class="version-badge">Advanced AI-Powered HR Analytics System v3.0</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Hero section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Smart Detection")
        st.markdown("""
        Sistem otomatis mendeteksi kompleksitas pekerjaan:
        - Entry-Level (Admin, CS, Kasir)
        - Mid-Level (Coordinator, Specialist)
        - Senior-Level (Engineer, Manager)
        """)
    
    with col2:
        st.markdown("### 🧠 Intelligent Scoring")
        st.markdown("""
        Scoring fleksibel berdasarkan job type:
        - Fresh graduate friendly untuk entry-level
        - Soft skills prioritas untuk admin/CS
        - Hard skills untuk technical positions
        """)
    
    with col3:
        st.markdown("### 💬 Human-like Reasoning")
        st.markdown("""
        Output seperti konsultasi HR:
        - Penjelasan kontekstual
        - Rekomendasi manusiawi
        - Insight mendalam
        """)
    
    st.markdown("---")
    
    # Features section
    st.markdown("## 🚀 Fitur Utama")
    
    tab1, tab2 = st.tabs(["👥 Employee Analyzer", "📄 CV Analyzer"])
    
    with tab1:
        st.markdown("""
        ### Ultra Employee Analyzer
        
        **Kemampuan:**
        
        1. **Job Complexity Detection** 🎯
           - Otomatis detect entry/mid/senior level
           - Adjust scoring weights accordingly
           - Fresh graduate friendly untuk entry-level
        
        2. **Flexible Scoring** 📊
           - Soft skills > Hard skills untuk entry-level
           - Experience flexibility untuk fresh grad
           - Organizational experience dihargai
        
        3. **Deep Analysis** 🔬
           - Semantic similarity dengan AI
           - Character & attitude assessment
           - Cultural fit evaluation
        
        4. **Batch Processing** ⚡
           - Analyze 100+ kandidat sekaligus
           - Export ke Excel/CSV
           - Ranking otomatis
        
        **Contoh Output:**
        
        > "Untuk posisi Admin yang termasuk entry-level, Aldy Loing sangat layak dipertimbangkan. 
        > Meskipun belum memiliki pengalaman admin langsung, profil menunjukkan kemampuan organisasi, 
        > dokumentasi yang baik, dan attitude positif. Pengalaman organisasi dapat menjadi foundation 
        > yang baik untuk posisi ini."
        
        **Cocok untuk:**
        - Screening kandidat internal
        - Talent mapping
        - Career development planning
        """)
    
    with tab2:
        st.markdown("""
        ### Ultra CV Analyzer
        
        **Kemampuan:**
        
        1. **CV Preview** 👁️
           - Extract data sebelum analisis
           - Tampilkan nama, email, skills, experience
           - Validasi kelengkapan CV
        
        2. **Advanced Parsing** 📄
           - Support PDF, DOCX, TXT
           - Extract education, experience, projects
           - Detect programming languages & tools
        
        3. **Intelligent Analysis** 🧠
           - Semantic matching dengan job description
           - Detect implicit skills dari experience
           - Identify leadership patterns
           - Problem-solving evidence
        
        4. **Comprehensive Scoring** 📊
           - Relevance score
           - Soft & hard skills score
           - Experience depth score
           - CV clarity score
           - Potential score
        
        **Contoh Output:**
        
        > "Kandidat fresh graduate dengan 3 project dan pengalaman organisasi yang kuat. 
        > Untuk posisi entry-level Admin, profil ini sangat cocok. CV menunjukkan kemampuan 
        > dokumentasi, organisasi, dan komunikasi yang baik. Pengalaman sebagai Bendahara Organisasi 
        > menunjukkan responsibility dan attention to detail."
        
        **Cocok untuk:**
        - Screening CV kandidat eksternal
        - ATS-level parsing
        - Resume quality check
        """)
    
    st.markdown("---")
    
    # How it works
    st.markdown("## 🔄 Cara Kerja")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 1️⃣ Input")
        st.markdown("Upload CV atau data kandidat + job description")
    
    with col2:
        st.markdown("### 2️⃣ Detect")
        st.markdown("AI detect job complexity & candidate level")
    
    with col3:
        st.markdown("### 3️⃣ Analyze")
        st.markdown("Deep analysis dengan semantic AI")
    
    with col4:
        st.markdown("### 4️⃣ Result")
        st.markdown("Reasoning manusiawi + rekomendasi")
    
    st.markdown("---")
    
    # Why Sentivize Ultra
    st.markdown("## ⭐ Mengapa Sentivize Ultra?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ Keunggulan
        
        - **No Keyword Matching**: Pure AI semantic understanding
        - **Fresh Grad Friendly**: Tidak diskriminatif terhadap fresh graduate
        - **Context-Aware**: Memahami perbedaan entry-level vs senior
        - **Human-like**: Output seperti konsultasi HR profesional
        - **Fast & Accurate**: Proses cepat dengan akurasi tinggi
        - **Batch Ready**: Support massive screening
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Use Cases
        
        - **Recruitment**: Screening CV kandidat eksternal
        - **Internal Hiring**: Analisis karyawan untuk promosi
        - **Talent Mapping**: Identifikasi skill gap
        - **Career Planning**: Rekomendasi posisi yang cocok
        - **Training Needs**: Deteksi area development
        - **Succession Planning**: Find potential leaders
        """)
    
    st.markdown("---")
    
    # CTA
    st.markdown("## 🚀 Mulai Sekarang")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👥 Analyze Employee", type="primary", use_container_width=True):
            st.session_state.page = "👥 Employee Analyzer"
            st.rerun()
    
    with col2:
        if st.button("📄 Analyze CV", type="primary", use_container_width=True):
            st.session_state.page = "📄 CV Analyzer"
            st.rerun()
    
    with col3:
        if st.button("ℹ️ Learn More", use_container_width=True):
            st.session_state.page = "ℹ️ About"
            st.rerun()


def render_about_page():
    """Render about page"""
    
    st.title("ℹ️ About Sentivize Ultra")
    
    st.markdown("""
    ## 🎯 Tentang Sistem
    
    **Sentivize Ultra** adalah sistem AI HR Analytics yang dirancang khusus untuk memahami 
    kandidat secara **kontekstual dan manusiawi**, bukan hanya berdasarkan keyword matching.
    
    ### 🧠 Filosofi Desain
    
    Sistem ini dibangun dengan prinsip:
    
    1. **Fairness**: Fresh graduate tidak otomatis ditolak untuk entry-level jobs
    2. **Context-Aware**: Perbedaan evaluasi untuk admin vs engineer
    3. **Human-like**: Reasoning seperti HR profesional, bukan robot
    4. **Comprehensive**: Analisis mendalam, bukan surface-level
    5. **Actionable**: Rekomendasi yang bisa dieksekusi
    
    ### 🔬 Teknologi
    
    **AI Models:**
    - Sentence Transformers (Semantic Embeddings)
    - XLM-RoBERTa (Multilingual Sentiment)
    - Custom Job Complexity Detector
    - Advanced CV Parser
    
    **Frameworks:**
    - PyTorch & Transformers
    - Streamlit (UI)
    - Pandas (Data Processing)
    - pdfplumber & python-docx (CV Parsing)
    
    ### 📊 Metode Scoring
    
    **Entry-Level Jobs (Admin, CS, Kasir):**
    - Soft Skills: 35%
    - Hard Skills: 15%
    - Experience: 15%
    - Organizational Exp: 15%
    - CV Clarity: 10%
    - Attitude/Potential: 10%
    
    **High-Level Jobs (Engineer, Manager):**
    - Soft Skills: 10%
    - Hard Skills: 40%
    - Experience: 30%
    - Organizational Exp: 5%
    - CV Clarity: 5%
    - Attitude/Potential: 10%
    
    ### 🎓 Contoh Kasus
    
    **Kasus 1: Fresh Graduate untuk Admin**
    
    *Tanpa Sentivize Ultra:*
    - ❌ Ditolak karena "no experience"
    - ❌ CV tidak match keyword "admin experience"
    
    *Dengan Sentivize Ultra:*
    - ✅ Detect sebagai entry-level job
    - ✅ Nilai pengalaman organisasi
    - ✅ Fokus soft skills & attitude
    - ✅ Result: "Sangat layak, CV menunjukkan organizational skills dan attitude positif"
    
    **Kasus 2: Senior untuk Software Engineer**
    
    *Tanpa Sentivize Ultra:*
    - ⚠️ Hanya cek keyword programming language
    
    *Dengan Sentivize Ultra:*
    - ✅ Detect sebagai high-complexity job
    - ✅ Deep dive technical skills
    - ✅ Analyze project portfolio
    - ✅ Verify experience depth
    - ✅ Result: Comprehensive technical assessment
    
    ### 📈 Version History
    
    - **v1.0** (2024-01): Basic sentiment analysis
    - **v2.0** (2024-02): Advanced AI with semantic search
    - **v3.0** (2024-03): Ultra edition with job complexity detection & CV preview
    
    ### 👥 Team
    
    Developed with ❤️ by AI Copilot Team
    
    ### 📧 Contact
    
    Untuk pertanyaan atau feedback, silakan hubungi tim development.
    
    ### 🔒 Privacy
    
    Semua data diproses secara lokal. Tidak ada data yang dikirim ke server eksternal.
    AI models dijalankan on-premise untuk menjaga kerahasiaan data kandidat.
    """)
    
    st.markdown("---")
    
    st.success("""
    **🎉 Terima kasih telah menggunakan Sentivize Ultra!**
    
    Sistem ini dirancang untuk membantu HR membuat keputusan yang lebih adil, 
    akurat, dan berbasis data dalam proses recruitment dan talent management.
    """)


if __name__ == "__main__":
    main()
