"""
Ultra Advanced CV Analyzer Page
================================
UI page dengan CV Preview sebelum analisis
UPGRADED dengan OpenRouter AI integration
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import tempfile

from analysis.ultra_cv_analyzer import UltraCVAnalyzer
from utils.human_friendly_formatter import HumanFriendlyFormatter

# Load environment variables
from utils.env_loader import load_env, validate_api_keys
load_env()

# NEW: Digital Footprint Analysis (additive module)
try:
    from services.digital_footprint_analyzer import get_digital_footprint_analyzer
    DIGITAL_FOOTPRINT_ENABLED = True
except ImportError:
    DIGITAL_FOOTPRINT_ENABLED = False
    print("⚠️ Digital Footprint module not available (optional)")

# NEW: Social Media Intelligence (additive module)
try:
    from services.social_media_intelligence_rapidapi import get_social_media_intelligence
    SOCIAL_MEDIA_INTEL_ENABLED = True
except ImportError:
    SOCIAL_MEDIA_INTEL_ENABLED = False
    print("⚠️ Social Media Intelligence module not available (optional)")


def render_ultra_cv_analyzer_page():
    """Render halaman CV Analyzer dengan Preview"""
    
    st.title("🔍 Ultra CV/Resume Analyzer")
    st.markdown("### Analisis CV dengan AI Super Canggih + Preview")
    st.markdown("---")
    
    # Info banner
    with st.expander("ℹ️ **Fitur AI Reasoning (NEW)**", expanded=False):
        st.markdown("""
        **Upgrade Terbaru:**
        - 🤖 **OpenRouter AI** untuk semantic reasoning mendalam
        - ✅ Preview data CV sebelum analisis
        - 🎯 Deteksi kompleksitas pekerjaan otomatis
        - 🌱 Scoring fleksibel untuk fresh graduate
        - 💭 Reasoning kontekstual seperti HR profesional
        - 🔍 Identifikasi skill implisit dan pola karier
        
        **AI Model:** deepseek-chat (FREE)
        """)
        
        # Check API key status
        api_status = validate_api_keys()
        if api_status['openrouter']['configured']:
            st.info(f"ℹ️ OpenRouter API: Configured (mungkin expired/invalid - fallback aktif)")
            st.caption("Jika muncul error 401, dapatkan API key baru di https://openrouter.ai/keys")
        else:
            st.warning("⚠️ OpenRouter API: Not configured (menggunakan fallback scoring)")
            st.caption("Set OPENROUTER_API_KEY di file .env untuk AI reasoning - atau biarkan fallback")
    
    # Initialize analyzer with error handling
    if 'cv_analyzer' not in st.session_state:
        with st.spinner("⚙️ Initializing AI Engine..."):
            try:
                st.session_state.cv_analyzer = UltraCVAnalyzer()
                st.session_state.analyzer_error = None
            except OSError as e:
                if "paging file" in str(e).lower() or "1455" in str(e):
                    st.session_state.analyzer_error = "memory"
                    st.error("""
                    ⚠️ **Memory Error: Paging File Too Small**
                    
                    Sistem tidak dapat load AI models karena Windows paging file terlalu kecil.
                    
                    **Solusi Cepat:**
                    1. Tutup aplikasi berat lainnya
                    2. Restart Streamlit
                    3. Atau tingkatkan virtual memory Windows
                    
                    **Sementara ini, sistem akan berjalan dengan mode minimal (tanpa AI advanced features).**
                    """)
                    st.session_state.cv_analyzer = None
                else:
                    st.session_state.analyzer_error = "unknown"
                    st.error(f"❌ Error initializing analyzer: {str(e)}")
                    st.session_state.cv_analyzer = None
            except Exception as e:
                st.session_state.analyzer_error = "unknown"
                st.error(f"❌ Error initializing analyzer: {str(e)}")
                st.session_state.cv_analyzer = None
    
    # Check if analyzer is available
    if st.session_state.get('analyzer_error') == 'memory':
        st.warning("⚠️ AI Engine tidak tersedia (memory error). Upload CV tetap bisa dilakukan, tapi analisis mendalam tidak tersedia.")
        return
    
    analyzer = st.session_state.cv_analyzer
    
    if analyzer is None:
        st.error("❌ Analyzer tidak tersedia. Silakan restart aplikasi atau hubungi administrator.")
        return
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📄 Upload & Preview", "🔍 Analisis", "📊 Hasil"])
    
    # ======================
    # TAB 1: Upload & Preview
    # ======================
    with tab1:
        st.markdown("## 📤 Upload CV")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Upload CV (PDF, DOCX, atau TXT)",
                type=['pdf', 'docx', 'doc', 'txt'],
                help="Upload CV kandidat dalam format PDF, DOCX, atau TXT"
            )
        
        with col2:
            st.markdown("**Format yang didukung:**")
            st.markdown("- 📕 PDF")
            st.markdown("- 📘 DOCX/DOC")
            st.markdown("- 📄 TXT")
        
        # Manual Social Media URLs Input (Optional)
        st.markdown("---")
        with st.expander("🔗 Tambah Link Social Media Manual (Opsional)"):
            st.caption("💡 Jika sistem tidak menemukan secara otomatis, Anda bisa input manual di sini")
            
            col1, col2 = st.columns(2)
            
            with col1:
                manual_linkedin = st.text_input(
                    "💼 LinkedIn URL",
                    placeholder="https://linkedin.com/in/username",
                    help="Contoh: https://linkedin.com/in/johndoe"
                )
                manual_instagram = st.text_input(
                    "📷 Instagram Username",
                    placeholder="@username atau username",
                    help="Contoh: @johndoe atau johndoe"
                )
                manual_twitter = st.text_input(
                    "🐦 Twitter/X Username",
                    placeholder="@username atau username",
                    help="Contoh: @johndoe atau johndoe"
                )
            
            with col2:
                manual_facebook = st.text_input(
                    "👥 Facebook URL atau Username",
                    placeholder="https://facebook.com/username",
                    help="Contoh: https://facebook.com/johndoe atau johndoe"
                )
                manual_tiktok = st.text_input(
                    "🎵 TikTok Username",
                    placeholder="@username atau username",
                    help="Contoh: @johndoe atau johndoe"
                )
                manual_youtube = st.text_input(
                    "▶️ YouTube Channel URL",
                    placeholder="https://youtube.com/@username",
                    help="Contoh: https://youtube.com/@johndoe"
                )
            
            # Store manual inputs in session state
            if 'manual_social_media' not in st.session_state:
                st.session_state.manual_social_media = {}
            
            st.session_state.manual_social_media = {
                'linkedin': [manual_linkedin.strip()] if manual_linkedin.strip() else [],
                'facebook': [manual_facebook.strip()] if manual_facebook.strip() else [],
                'instagram': [manual_instagram.strip().replace('@', '')] if manual_instagram.strip() else [],
                'twitter': [manual_twitter.strip().replace('@', '')] if manual_twitter.strip() else [],
                'tiktok': [manual_tiktok.strip().replace('@', '')] if manual_tiktok.strip() else [],
                'youtube': [manual_youtube.strip()] if manual_youtube.strip() else []
            }
            
            # Show summary if any manual input provided
            manual_count = sum(1 for links in st.session_state.manual_social_media.values() if links)
            if manual_count > 0:
                st.success(f"✅ {manual_count} link social media manual ditambahkan")
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Extract file type
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension == 'doc':
                file_extension = 'docx'
            
            # Preview Button
            if st.button("👁️ Preview & Extract Data", type="primary"):
                with st.spinner("📄 Mengekstrak data dari CV..."):
                    try:
                        # Extract preview
                        preview = analyzer.preview_extractor.extract_from_file(
                            tmp_file_path,
                            file_extension
                        )
                        
                        # Store in session state
                        st.session_state.cv_preview = preview
                        st.session_state.cv_file_path = tmp_file_path
                        st.session_state.cv_file_type = file_extension
                        
                        st.success("✅ Data berhasil diekstraksi!")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ Error extracting CV: {str(e)}")
                        st.exception(e)
        
        # Display Preview if available
        if 'cv_preview' in st.session_state:
            st.markdown("---")
            st.markdown("### 👁️ Preview Data CV")
            
            preview = st.session_state.cv_preview
            
            # Use the new display_summary method
            st.markdown(preview.get_display_summary())
            
            # Additional details in expander
            with st.expander("📋 Detail Lengkap Preview"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if preview.education_summary:
                        st.markdown("**🎓 Pendidikan:**")
                        for edu in preview.education_summary[:3]:
                            st.caption(f"- {edu}")
                    
                    if preview.work_experiences:
                        st.markdown("**💼 Pengalaman Kerja:**")
                        for exp in preview.work_experiences[:3]:
                            st.caption(f"- {exp.get('title', '')} @ {exp.get('company', '')}")
                
                with col2:
                    if preview.projects:
                        st.markdown("**🚀 Project:**")
                        for proj in preview.projects[:3]:
                            st.caption(f"- {proj.get('title', '')}")
                    
                    if preview.organizational_experiences:
                        st.markdown("**🌟 Organisasi:**")
                        for org in preview.organizational_experiences[:3]:
                            st.caption(f"- {org.get('organization', '')}")
                
                # Career summary (jika ada AI)
                if preview.career_summary:
                    st.markdown("---")
                    st.markdown("**💭 AI Career Summary:**")
                    st.info(preview.career_summary)
            
            # Strengths display
            if preview.strengths:
                st.markdown("**💪 Kekuatan yang Terdeteksi:**")
                cols = st.columns(min(len(preview.strengths), 3))
                for idx, strength in enumerate(preview.strengths[:6]):
                    with cols[idx % 3]:
                        st.success(f"✅ {strength}")
            
            # NEW: Digital Footprint Preview (additive, non-breaking)
            if DIGITAL_FOOTPRINT_ENABLED:
                st.markdown("---")
                st.markdown("### 🌐 Preview Jejak Digital")
                st.caption("Deteksi otomatis dari CV - akan dianalisis jika tersedia")
                
                try:
                    footprint_analyzer = get_digital_footprint_analyzer()
                    cv_text = preview.raw_text if hasattr(preview, 'raw_text') else ""
                    candidate_name = preview.full_name or "Unknown"
                    
                    profiles = footprint_analyzer.extract_digital_profiles(cv_text, candidate_name)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        github_status = profiles['github']['status']
                        if github_status == 'detected':
                            st.success(f"✅ GitHub: {profiles['github']['username']}")
                        else:
                            st.info("ℹ️ GitHub: Not Found")
                    
                    with col2:
                        linkedin_status = profiles['linkedin']['status']
                        if linkedin_status == 'detected':
                            st.success("✅ LinkedIn: Detected")
                        else:
                            st.info("ℹ️ LinkedIn: Not Found")
                    
                    with col3:
                        if profiles['candidate_name'] != "Unknown":
                            st.info(f"📰 Google News: {profiles['candidate_name']}")
                        else:
                            st.info("📰 Google News: Pending")
                    
                    # Store for later analysis
                    st.session_state.cv_digital_profiles = profiles
                    
                    st.caption("💡 Data ini akan digunakan untuk analisis jejak digital (optional)")
                    
                except Exception as e:
                    st.caption(f"⚠️ Digital footprint preview error: {str(e)}")
            
            formatter = HumanFriendlyFormatter()
            
            # Action buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Upload CV Baru"):
                    # Clear session state
                    if 'cv_preview' in st.session_state:
                        del st.session_state.cv_preview
                    if 'cv_file_path' in st.session_state:
                        del st.session_state.cv_file_path
                    if 'cv_analysis_result' in st.session_state:
                        del st.session_state.cv_analysis_result
                    st.rerun()
            
            with col2:
                if st.button("➡️ Lanjut ke Analisis", type="primary"):
                    st.info("👉 Silakan ke tab **Analisis** untuk input job description")
            
            with col3:
                st.markdown("")  # Spacer
    
    # ======================
    # TAB 2: Analisis
    # ======================
    with tab2:
        st.markdown("## 🎯 Input Job Description")
        
        if 'cv_preview' not in st.session_state:
            st.warning("⚠️ Silakan upload dan preview CV terlebih dahulu di tab **Upload & Preview**")
            return
        
        st.success(f"✅ CV sudah di-load: **{st.session_state.cv_preview.full_name or 'Kandidat'}**")
        
        # Job input
        col1, col2 = st.columns([2, 1])
        
        with col1:
            job_title = st.text_input(
                "Judul Posisi",
                placeholder="Contoh: Admin, Customer Service, Software Engineer",
                help="Masukkan nama posisi yang dicari"
            )
        
        with col2:
            st.markdown("**Contoh Posisi:**")
            st.caption("- Admin")
            st.caption("- Customer Service")
            st.caption("- Software Engineer")
        
        job_description = st.text_area(
            "Deskripsi Pekerjaan (Job Description)",
            height=200,
            placeholder="Masukkan deskripsi lengkap pekerjaan, requirements, responsibilities, dll.\n\nContoh:\n- Mengelola administrasi kantor\n- Membuat laporan\n- Komunikasi dengan tim\n- Skill: MS Office, komunikasi baik, detail-oriented",
            help="Semakin detail, semakin akurat analisisnya"
        )
        
        # Analyze button
        if st.button("🚀 Mulai Analisis", type="primary", disabled=not job_title or not job_description):
            with st.spinner("🧠 AI sedang menganalisis CV secara mendalam..."):
                try:
                    # EXISTING: Run main CV analysis (TIDAK DIUBAH)
                    result = analyzer.analyze_cv(
                        cv_file_path=st.session_state.cv_file_path,
                        job_title=job_title,
                        job_description=job_description,
                        file_type=st.session_state.cv_file_type
                    )
                    
                    # Store main result (EXISTING)
                    st.session_state.cv_analysis_result = result
                    
                    # NEW: Digital Footprint Analysis (additive, tidak wajib)
                    if DIGITAL_FOOTPRINT_ENABLED and 'cv_digital_profiles' in st.session_state:
                        with st.spinner("🌐 Menganalisis jejak digital (optional)..."):
                            try:
                                footprint_analyzer = get_digital_footprint_analyzer()
                                preview = st.session_state.cv_preview
                                cv_text = preview.raw_text if hasattr(preview, 'raw_text') else ""
                                candidate_name = preview.full_name or "Unknown"
                                
                                digital_footprint = footprint_analyzer.analyze_complete_footprint(
                                    cv_text=cv_text,
                                    candidate_name=candidate_name,
                                    job_description=job_description
                                )
                                
                                # Store SEPARATELY (tidak override hasil lama)
                                st.session_state.cv_digital_footprint = digital_footprint
                                st.success("✅ Digital footprint analysis completed")
                                
                            except Exception as df_error:
                                # SAFE: Jika gagal, analisis utama tetap jalan
                                st.warning(f"⚠️ Digital footprint analysis skipped: {str(df_error)}")
                                st.session_state.cv_digital_footprint = None
                    
                    # NEW: Social Media Intelligence (additive, tidak wajib)
                    if SOCIAL_MEDIA_INTEL_ENABLED:
                        with st.spinner("📱 Menganalisis social media intelligence (optional)..."):
                            try:
                                social_intel = get_social_media_intelligence()
                                preview = st.session_state.cv_preview
                                candidate_name = preview.full_name or "Unknown"
                                cv_text = preview.raw_text if hasattr(preview, 'raw_text') else ""
                                
                                # Extract organization safely
                                org_name = ''
                                if preview.organizational_experiences:
                                    first_org = preview.organizational_experiences[0]
                                    if isinstance(first_org, dict):
                                        org_name = first_org.get('organization', '')
                                    elif isinstance(first_org, str):
                                        org_name = first_org
                                
                                # Get manual social media inputs
                                manual_inputs = st.session_state.get('manual_social_media', {})
                                
                                social_media_result = social_intel.analyze_complete_social_footprint(
                                    candidate_name=candidate_name,
                                    cv_text=cv_text,
                                    cv_data={
                                        'organization': org_name
                                    },
                                    manual_links=manual_inputs
                                )
                                
                                # Store SEPARATELY
                                st.session_state.cv_social_media_intel = social_media_result
                                
                                # Count manual inputs
                                manual_count = sum(1 for links in manual_inputs.values() if links)
                                confirmed_count = sum(1 for p in social_media_result.get('platforms', {}).values() 
                                                    if p.get('status') == 'confirmed')
                                
                                if manual_count > 0:
                                    st.success(f"✅ Social media intelligence completed ({manual_count} manual input used)")
                                else:
                                    st.success("✅ Social media intelligence completed")
                                
                                st.info(f"🎯 Found {confirmed_count} confirmed social media accounts")
                                
                            except Exception as sm_error:
                                # SAFE: Jika gagal, analisis utama tetap jalan
                                st.warning(f"⚠️ Social media intelligence skipped: {str(sm_error)}")
                                st.session_state.cv_social_media_intel = None
                    
                    st.success("✅ Analisis selesai!")
                    st.info("👉 Lihat hasil lengkap di tab **Hasil**")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    st.exception(e)
        
        if not job_title:
            st.warning("⚠️ Masukkan judul posisi")
        if not job_description:
            st.warning("⚠️ Masukkan deskripsi pekerjaan")
    
    # ======================
    # TAB 3: Hasil
    # ======================
    with tab3:
        st.markdown("## 📊 Hasil Analisis")
        
        if 'cv_analysis_result' not in st.session_state:
            st.info("ℹ️ Belum ada hasil analisis. Silakan upload CV dan jalankan analisis terlebih dahulu.")
            return
        
        result = st.session_state.cv_analysis_result
        
        # Display hasil
        formatter = HumanFriendlyFormatter()
        
        # Header
        st.markdown(f"## 👤 {result.candidate_name}")
        st.markdown(f"**Target Position:** {result.job_title}")
        
        # Job Complexity Info
        if result.job_profile:
            st.markdown("---")
            st.markdown("### 🎯 Analisis Kompleksitas Pekerjaan")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Complexity Level",
                    result.job_profile.complexity.value.upper()
                )
            
            with col2:
                st.metric(
                    "Fresh Grad Friendly",
                    "YES" if result.job_profile.fresh_graduate_friendly else "NO"
                )
            
            with col3:
                st.metric(
                    "Flexibility",
                    f"{result.job_profile.experience_flexibility * 100:.0f}%"
                )
            
            st.info(f"**Reasoning:** {result.job_profile.reasoning}")
        
        st.markdown("---")
        
        # Main Analysis
        formatter.format_cv_analysis_card(result)
        
        # Advanced Insights
        st.markdown("---")
        st.markdown("### 🔬 Advanced Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if result.implicit_skills:
                st.markdown("#### 💡 Skill Implisit")
                st.caption("Skill yang tidak ditulis eksplisit tapi terdeteksi dari pengalaman")
                for skill in result.implicit_skills:
                    st.markdown(f"- {skill}")
        
        with col2:
            if result.leadership_patterns:
                st.markdown("#### 👑 Pola Leadership")
                for pattern in result.leadership_patterns:
                    st.markdown(f"- {pattern}")
        
        if result.problem_solving_evidence:
            st.markdown("#### 🧩 Bukti Problem-Solving")
            for evidence in result.problem_solving_evidence:
                st.markdown(f"- {evidence}")
        
        if result.initiative_examples:
            st.markdown("#### ⚡ Contoh Inisiatif")
            for example in result.initiative_examples:
                st.markdown(f"- {example}")
        
        # Position Recommendations
        if result.position_recommendations:
            st.markdown("---")
            st.markdown("### 📍 Rekomendasi Posisi")
            
            for pos_rec in result.position_recommendations:
                # Handle both dict and string format
                if isinstance(pos_rec, dict):
                    position = pos_rec.get('position', 'Unknown Position')
                    reason = pos_rec.get('reason', 'Sesuai dengan profil kandidat')
                    st.info(f"**{position}** - {reason}")
                else:
                    # If it's just a string (position name)
                    st.info(f"**{pos_rec}** - Direkomendasikan berdasarkan profil kandidat")
        
        # Interview Focus
        if result.interview_focus_areas:
            st.markdown("---")
            st.markdown("### 🎤 Fokus Interview")
            
            for focus in result.interview_focus_areas:
                st.markdown(f"- {focus}")
        
        # NEW: Digital Footprint Insights (additive section)
        if DIGITAL_FOOTPRINT_ENABLED and 'cv_digital_footprint' in st.session_state:
            digital_footprint = st.session_state.cv_digital_footprint
            
            if digital_footprint and digital_footprint.get('analysis_status') == 'completed':
                st.markdown("---")
                st.markdown("### 🌐 Digital Footprint Insights")
                st.caption("Analisis tambahan berdasarkan jejak digital kandidat")
                
                # Generate human-friendly summary
                try:
                    footprint_analyzer = get_digital_footprint_analyzer()
                    summary = footprint_analyzer.generate_human_friendly_summary(digital_footprint)
                    st.markdown(summary)
                    
                    # Detailed breakdown in expander
                    with st.expander("🔍 Detail Analisis Jejak Digital"):
                        sources = digital_footprint.get('sources', {})
                        
                        # GitHub detail
                        if sources.get('github', {}).get('available'):
                            github = sources['github']
                            st.markdown("#### 🔧 GitHub Analysis")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Public Repos", github['profile']['public_repos'])
                            with col2:
                                st.metric("Total Stars", github['activity']['total_stars_received'])
                            with col3:
                                st.metric("Followers", github['profile']['followers'])
                            
                            if github['activity']['top_languages']:
                                st.markdown("**Top Languages:**")
                                for lang_data in github['activity']['top_languages'][:5]:
                                    st.caption(f"- {lang_data['language']}: {lang_data['count']} repos")
                        
                        # LinkedIn detail
                        if sources.get('linkedin', {}).get('available'):
                            linkedin = sources['linkedin']
                            st.markdown("#### 💼 LinkedIn Analysis")
                            st.info(linkedin.get('message', 'LinkedIn profile available'))
                            if 'limitation' in linkedin:
                                st.caption(f"⚠️ {linkedin['limitation']}")
                        
                        # Google News detail with AI Analysis
                        if sources.get('google_news'):
                            news = sources['google_news']
                            st.markdown("#### 📰 Google News Search (AI Analyzed)")
                            
                            if news.get('status') == 'found':
                                # Get AI-analyzed results
                                analyzed_results = news.get('analyzed_results', {})
                                
                                if analyzed_results:
                                    confirmed_list = analyzed_results.get('confirmed', [])
                                    conditional_list = analyzed_results.get('conditional', [])
                                    
                                    st.success(f"✅ Ditemukan {news.get('total_results', 0)} berita (AI: {len(confirmed_list)} relevan, {len(conditional_list)} perlu review)")
                                else:
                                    st.success(f"✅ Ditemukan {news.get('total_results', 0)} berita")
                                
                                # NEW: AI-Analyzed Results (human-friendly)
                                if analyzed_results:
                                    st.markdown("---")
                                    st.markdown("### 📌 Google News Insight (AI Analysis)")
                                    
                                    # ✅ Confirmed News
                                    confirmed = analyzed_results.get('confirmed', [])
                                    if confirmed:
                                        st.markdown("#### ✅ Berita Relevan & Terkonfirmasi")
                                        st.caption(f"Ditemukan {len(confirmed)} berita dengan relevansi tinggi")
                                        
                                        for idx, article in enumerate(confirmed, 1):
                                            with st.container():
                                                st.markdown(f"**{idx}. 📰 {article.get('title')}**")
                                                
                                                col1, col2 = st.columns([1, 1])
                                                with col1:
                                                    st.caption(f"🏢 **Sumber:** {article.get('source', 'Unknown')}")
                                                    if article.get('date'):
                                                        st.caption(f"📅 **Tanggal:** {article['date']}")
                                                
                                                with col2:
                                                    if article.get('link'):
                                                        st.caption(f"🔗 [Baca Artikel Lengkap]({article['link']})")
                                                
                                                # Summary
                                                if article.get('summary'):
                                                    st.info(f"📝 {article['summary']}")
                                                
                                                # Relevance Reasons
                                                if article.get('reasons'):
                                                    st.success("**🎯 Alasan Relevansi:**")
                                                    for reason in article['reasons']:
                                                        st.caption(f"• {reason}")
                                                
                                                st.markdown("---")
                                    
                                    # ⚠️ Conditional News
                                    conditional = analyzed_results.get('conditional', [])
                                    if conditional:
                                        st.markdown("#### ⚠️ Berita Relevan Bersyarat (Perlu Pertimbangan)")
                                        st.caption(f"Ditemukan {len(conditional)} berita dengan konteks mendekati CV")
                                        
                                        for idx, article in enumerate(conditional, 1):
                                            with st.container():
                                                st.markdown(f"**{idx}. 📰 {article.get('title')}**")
                                                
                                                col1, col2 = st.columns([1, 1])
                                                with col1:
                                                    st.caption(f"🏢 **Sumber:** {article.get('source', 'Unknown')}")
                                                    if article.get('date'):
                                                        st.caption(f"📅 **Tanggal:** {article['date']}")
                                                
                                                with col2:
                                                    if article.get('link'):
                                                        st.caption(f"🔗 [Baca Artikel Lengkap]({article['link']})")
                                                
                                                # Note
                                                if article.get('note'):
                                                    st.warning(f"💡 **Catatan AI:** {article['note']}")
                                                
                                                # Reasons
                                                if article.get('reasons'):
                                                    st.info("**Indikator Relevansi:**")
                                                    for reason in article['reasons']:
                                                        st.caption(f"• {reason}")
                                                
                                                st.markdown("---")
                                    
                                    # No relevant news found
                                    if not confirmed and not conditional:
                                        st.info("🔍 Tidak ditemukan publikasi berita yang relevan atau mendekati secara kontekstual dengan data CV kandidat.")
                                
                                else:
                                    # Fallback: Show raw results if analyzed_results not available
                                    st.markdown("**Berita yang ditemukan:**")
                                    for idx, article in enumerate(news.get('results', [])[:5], 1):
                                        with st.container():
                                            st.markdown(f"**{idx}. {article.get('title', 'No title')}**")
                                            if article.get('date'):
                                                st.caption(f"📅 {article['date']}")
                                            if article.get('link'):
                                                st.caption(f"🔗 [Baca artikel]({article['link']})")
                                            if article.get('query'):
                                                st.caption(f"🔍 Query: {article['query']}")
                                            st.markdown("---")
                            
                            elif news.get('status') == 'not_found':
                                st.info(news.get('message', 'Tidak ditemukan berita'))
                                
                                if news.get('query_variations'):
                                    st.caption(f"**Pencarian dengan:** {', '.join(news['query_variations'])}")
                                
                                if news.get('contexts_used'):
                                    st.caption(f"**Konteks yang dicari:** {', '.join(news['contexts_used'])}")
                            
                            else:
                                st.info(news.get('message', 'News search completed'))
                
                except Exception as e:
                    import traceback
                    st.error(f"Error displaying digital footprint: {str(e)}")
                    with st.expander("Debug Info"):
                        st.code(traceback.format_exc())
        
        # NEW: Social Media Intelligence Section (additive)
        if SOCIAL_MEDIA_INTEL_ENABLED and 'cv_social_media_intel' in st.session_state:
            social_intel_result = st.session_state.cv_social_media_intel
            
            if social_intel_result and social_intel_result.get('status') != 'skipped':
                st.markdown("---")
                st.markdown("### 📱 Social Media Intelligence")
                st.caption("Analisis tambahan jejak digital kandidat di social media")
                
                try:
                    social_intel = get_social_media_intelligence()
                    report = social_intel.generate_human_friendly_report(social_intel_result)
                    st.markdown(report)
                    
                    # Detailed view in expander
                    with st.expander("🔍 Detail Social Media Analysis"):
                        platforms = social_intel_result.get('platforms', {})
                        
                        for platform_name, platform_data in platforms.items():
                            st.markdown(f"#### {platform_name.title()}")
                            st.json(platform_data)
                
                except Exception as e:
                    st.warning(f"⚠️ Social media intelligence display error: {str(e)}")
        
        # Export option
        st.markdown("---")
        st.markdown("### 💾 Export Hasil")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export as dictionary
            export_data = result.to_dict()
            df_export = pd.DataFrame([export_data])
            
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"cv_analysis_{result.candidate_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            excel_buffer = pd.io.excel.ExcelWriter(f'temp_export.xlsx', engine='openpyxl')
            df_export.to_excel(excel_buffer, index=False, sheet_name='Analysis')
            excel_buffer.close()
            
            st.info("💡 Hasil analisis dapat di-export ke CSV")
        
        # Actions
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Analisis CV Baru"):
                # Clear all session state
                for key in ['cv_preview', 'cv_file_path', 'cv_analysis_result']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("📝 Analisis dengan Job Description Berbeda"):
                # Keep CV, clear analysis
                if 'cv_analysis_result' in st.session_state:
                    del st.session_state.cv_analysis_result
                st.info("👉 Kembali ke tab **Analisis**")


if __name__ == "__main__":
    render_ultra_cv_analyzer_page()
