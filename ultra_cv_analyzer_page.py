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
            st.success(f"✅ OpenRouter API: Active")
        else:
            st.warning("⚠️ OpenRouter API: Not configured (akan menggunakan fallback scoring)")
            st.caption("Set OPENROUTER_API_KEY di file .env untuk mengaktifkan AI reasoning")
    
    # Initialize analyzer
    if 'cv_analyzer' not in st.session_state:
        with st.spinner("⚙️ Initializing AI Engine..."):
            st.session_state.cv_analyzer = UltraCVAnalyzer()
    
    analyzer = st.session_state.cv_analyzer
    
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
                    # Run analysis
                    result = analyzer.analyze_cv(
                        cv_file_path=st.session_state.cv_file_path,
                        job_title=job_title,
                        job_description=job_description,
                        file_type=st.session_state.cv_file_type
                    )
                    
                    # Store result
                    st.session_state.cv_analysis_result = result
                    
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
