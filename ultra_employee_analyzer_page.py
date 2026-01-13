"""
Ultra Advanced Employee Analyzer Page
======================================
Batch Analysis dengan 3 tab terpisah: Upload & Preview, Analisis, Hasil
UPGRADED dengan OpenRouter AI integration
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io

from analysis.ultra_employee_analyzer import UltraEmployeeAnalyzer
from utils.human_friendly_formatter import HumanFriendlyFormatter

# Load environment variables
from utils.env_loader import load_env, validate_api_keys
load_env()


def render_ultra_employee_analyzer_page():
    """Render halaman Employee Analyzer untuk Batch Analysis dengan 3 tab"""
    
    st.title("👥 Ultra Employee Analyzer - Batch Analysis")
    st.markdown("### Analisis Multiple Kandidat Sekaligus dengan AI Super Pintar")
    st.markdown("---")
    
    # Info banner
    with st.expander("ℹ️ **Fitur AI Reasoning (NEW)**", expanded=False):
        st.markdown("""
        **Upgrade Terbaru:**
        - 🤖 **OpenRouter AI** untuk semantic reasoning mendalam
        - 📊 **Batch Analysis** untuk banyak kandidat sekaligus
        - 🎯 Deteksi kompleksitas pekerjaan otomatis (Entry/Mid/Senior)
        - 🌱 Scoring fleksibel untuk posisi entry-level
        - 🆓 Fresh graduate friendly evaluation
        - 💭 Reasoning kontekstual seperti HR profesional
        - 📱 Social media auto-search (optional)
        
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
    
    # Initialize analyzer
    if 'employee_analyzer' not in st.session_state:
        with st.spinner("⚙️ Initializing AI Engine..."):
            st.session_state.employee_analyzer = UltraEmployeeAnalyzer()
    
    analyzer = st.session_state.employee_analyzer
    
    # Tabs - 3 tab seperti CV Analyzer
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Preview", "🔍 Analisis", "📊 Hasil"])
    
    # ======================
    # TAB 1: Upload & Preview
    # ======================
    with tab1:
        st.markdown("## 📤 Upload Data Kandidat")
        st.markdown("Upload file Excel atau CSV berisi data multiple kandidat untuk batch analysis")
        
        # File format guide
        st.markdown("---")
        st.markdown("### 📋 Format File yang Diperlukan")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **File Excel/CSV dengan kolom:**
            - `name`: Nama kandidat (Required)
            - `position`: Posisi saat ini (Required)
            - `skills`: Keahlian (Required)
            - `experience`: Pengalaman (Required)
            - `bio`: Profil singkat (Required)
            - `social_media_url`: URL social media (Optional)
            """)
        
        with col2:
            st.markdown("**Contoh Format:**")
            example_df = pd.DataFrame({
                'name': ['John Doe', 'Jane Smith'],
                'position': ['Admin', 'Customer Service'],
                'skills': ['MS Office, Komunikasi', 'Customer Service, Problem Solving'],
                'experience': ['2 tahun admin', '1 tahun CS'],
                'bio': ['Fresh graduate termotivasi', 'Berpengalaman di retail']
            })
            st.dataframe(example_df, use_container_width=True)
        
        st.markdown("---")
        
        # File uploader
        st.markdown("### 📤 Upload File")
        
        uploaded_file = st.file_uploader(
            "Upload Excel atau CSV",
            type=['xlsx', 'xls', 'csv'],
            help="Upload file dengan format yang sesuai",
            key="emp_batch_upload"
        )
        
        if uploaded_file is not None:
            try:
                # Read file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ File berhasil di-upload: **{uploaded_file.name}**")
                st.info(f"📊 Total kandidat: **{len(df)}** orang")
                
                # Validate columns
                required_cols = ['name', 'position', 'skills', 'experience', 'bio']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"❌ Kolom yang hilang: **{', '.join(missing_cols)}**")
                    st.warning("Pastikan file memiliki semua kolom required: name, position, skills, experience, bio")
                else:
                    # Store in session state
                    st.session_state.emp_batch_data = df
                    st.session_state.emp_batch_filename = uploaded_file.name
                    
                    st.markdown("---")
                    st.markdown("### 👁️ Preview Data")
                    
                    # Display full data with pagination
                    st.markdown(f"**Menampilkan {min(10, len(df))} dari {len(df)} kandidat:**")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    if len(df) > 10:
                        st.caption(f"ℹ️ {len(df) - 10} kandidat lainnya akan diproses saat analisis")
                    
                    # Summary statistics
                    st.markdown("---")
                    st.markdown("### 📊 Summary Statistik")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Kandidat", len(df))
                    
                    with col2:
                        unique_positions = df['position'].nunique()
                        st.metric("Unique Positions", unique_positions)
                    
                    with col3:
                        has_skills = df['skills'].notna().sum()
                        st.metric("Dengan Skills", has_skills)
                    
                    with col4:
                        has_exp = df['experience'].notna().sum()
                        st.metric("Dengan Experience", has_exp)
                    
                    # Action buttons
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("🔄 Upload File Baru", key="emp_upload_new"):
                            for key in ['emp_batch_data', 'emp_batch_filename', 'emp_batch_results']:
                                if key in st.session_state:
                                    del st.session_state[key]
                            st.rerun()
                    
                    with col2:
                        if st.button("➡️ Lanjut ke Analisis", type="primary", key="emp_goto_analysis"):
                            st.info("👉 Silakan ke tab **Analisis** untuk input job description dan mulai batch analysis")
            
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                st.exception(e)
        
        else:
            st.info("📁 Silakan upload file Excel atau CSV untuk memulai batch analysis")
    
    # ======================
    # TAB 2: Analisis
    # ======================
    with tab2:
        st.markdown("## 🔍 Batch Analysis")
        
        # Check if data is loaded
        if 'emp_batch_data' not in st.session_state:
            st.warning("⚠️ Silakan upload file data kandidat terlebih dahulu di tab **Upload & Preview**")
            return
        
        df = st.session_state.emp_batch_data
        st.success(f"✅ Data loaded: **{st.session_state.emp_batch_filename}** ({len(df)} kandidat)")
        
        st.markdown("---")
        
        # Job Description Section
        st.markdown("### 📋 Job Requirements")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            emp_job_title = st.text_input(
                "Judul Posisi",
                placeholder="Contoh: Admin, Customer Service, Data Analyst",
                help="Masukkan nama posisi yang dicari",
                key="emp_job_title"
            )
        
        with col2:
            st.markdown("**Contoh:**")
            st.caption("- Admin")
            st.caption("- Kasir")
            st.caption("- Customer Service")
        
        emp_job_criteria = st.text_area(
            "Kriteria Pekerjaan",
            height=200,
            placeholder="""Masukkan deskripsi lengkap kriteria, requirements, responsibilities.

Contoh untuk Admin:
- Mengelola administrasi kantor
- Membuat laporan harian/bulanan
- Komunikasi dengan tim
- Data entry dan filing

Skills Required:
- MS Office (Excel, Word, PowerPoint)
- Komunikasi baik
- Detail-oriented
- Organisasi yang rapi

Attitude:
- Rajin dan bertanggung jawab
- Proaktif
- Bisa bekerja dalam tim""",
            help="Semakin detail, semakin akurat analisisnya. Sistem akan otomatis detect kompleksitas pekerjaan.",
            key="emp_job_criteria"
        )
        
        st.markdown("---")
        
        # Options
        st.markdown("### ⚙️ Opsi Analisis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            emp_use_social = st.checkbox(
                "🌐 Analisis Social Media",
                value=False,
                help="Analisis profile social media kandidat (jika tersedia)",
                key="emp_use_social"
            )
        
        with col2:
            st.info(f"📊 Total kandidat yang akan dianalisis: **{len(df)}**")
        
        # Analyze button
        st.markdown("---")
        
        if st.button("🚀 Mulai Batch Analysis", type="primary", disabled=not (emp_job_title and emp_job_criteria), key="emp_start_analysis"):
            with st.spinner(f"🧠 Analyzing {len(df)} kandidat... Mohon tunggu, ini mungkin memakan waktu beberapa menit..."):
                
                # Progress indicator
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text(f"⏳ Memulai analisis untuk {len(df)} kandidat...")
                    
                    # Run batch analysis
                    results_df = analyzer.analyze_batch(
                        employees_df=df,
                        job_criteria=emp_job_criteria,
                        target_position=emp_job_title,
                        use_social_media=emp_use_social
                    )
                    
                    # Complete progress
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis completed!")
                    
                    # Store results
                    st.session_state.emp_batch_results = results_df
                    st.session_state.emp_result_job_title = emp_job_title
                    st.session_state.emp_result_job_criteria = emp_job_criteria
                    
                    st.success("✅ Batch analysis selesai!")
                    st.info("👉 Lihat hasil lengkap di tab **Hasil**")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    st.exception(e)
        
        if not emp_job_title:
            st.warning("⚠️ Masukkan judul posisi")
        if not emp_job_criteria:
            st.warning("⚠️ Masukkan kriteria pekerjaan")
    
    # ======================
    # TAB 3: Hasil
    # ======================
    with tab3:
        st.markdown("## 📊 Hasil Batch Analysis")
        
        if 'emp_batch_results' not in st.session_state:
            st.info("ℹ️ Belum ada hasil analisis. Silakan upload data dan jalankan batch analysis terlebih dahulu.")
            return
        
        results_df = st.session_state.emp_batch_results
        job_title = st.session_state.get('emp_result_job_title', 'N/A')
        
        # Header
        st.markdown(f"### 🎯 Target Position: **{job_title}**")
        st.markdown(f"**Total Kandidat Dianalisis:** {len(results_df)}")
        
        st.markdown("---")
        
        # Summary Statistics
        st.markdown("### 📈 Summary Statistik")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Kandidat", len(results_df))
        
        with col2:
            if 'tier' in results_df.columns:
                excellent = len(results_df[results_df['tier'] == 'EXCELLENT'])
                st.metric("⭐ Excellent", excellent)
        
        with col3:
            if 'tier' in results_df.columns:
                strong = len(results_df[results_df['tier'] == 'STRONG'])
                st.metric("💪 Strong", strong)
        
        with col4:
            if 'overall_score' in results_df.columns:
                avg_score = results_df['overall_score'].mean()
                st.metric("📊 Avg Score", f"{avg_score:.1f}")
        
        st.markdown("---")
        
        # Tier Distribution
        if 'tier' in results_df.columns:
            st.markdown("### 🎯 Distribusi Tier")
            
            tier_counts = results_df['tier'].value_counts()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                for tier in ['EXCELLENT', 'STRONG', 'MEDIUM', 'LOW']:
                    if tier in tier_counts.index:
                        count = tier_counts[tier]
                        percentage = (count / len(results_df)) * 100
                        st.progress(percentage / 100)
                        st.caption(f"**{tier}**: {count} kandidat ({percentage:.1f}%)")
            
            with col2:
                st.markdown("**Legend:**")
                st.markdown("⭐ **EXCELLENT**: Top tier")
                st.markdown("💪 **STRONG**: Sangat baik")
                st.markdown("🟢 **MEDIUM**: Baik")
                st.markdown("🟡 **LOW**: Perlu peningkatan")
        
        st.markdown("---")
        
        # Results Table
        st.markdown("### 📋 Tabel Hasil Detail")
        
        # Sort options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            sort_by = st.selectbox(
                "Sortir berdasarkan:",
                ['overall_score', 'tier', 'employee_name'],
                format_func=lambda x: {
                    'overall_score': '📊 Overall Score',
                    'tier': '🎯 Tier',
                    'employee_name': '👤 Nama'
                }.get(x, x),
                key="emp_sort_by"
            )
        
        with col2:
            sort_order = st.radio(
                "Urutan:",
                ['desc', 'asc'],
                format_func=lambda x: '⬇️ Descending' if x == 'desc' else '⬆️ Ascending',
                key="emp_sort_order"
            )
        
        # Sort dataframe
        sorted_df = results_df.sort_values(
            by=sort_by,
            ascending=(sort_order == 'asc')
        )
        
        # Display table
        st.dataframe(
            sorted_df,
            use_container_width=True,
            height=400
        )
        
        st.markdown("---")
        
        # Top Candidates
        if 'overall_score' in results_df.columns:
            st.markdown("### 🏆 Top 5 Kandidat")
            
            top_5 = results_df.nlargest(5, 'overall_score')
            
            for idx, (_, row) in enumerate(top_5.iterrows(), 1):
                with st.expander(f"#{idx} - {row.get('employee_name', 'N/A')} - Score: {row.get('overall_score', 0):.1f}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Tier:** {row.get('tier', 'N/A')}")
                        st.markdown(f"**Recommendation:** {row.get('recommendation', 'N/A')}")
                        st.markdown(f"**Overall Score:** {row.get('overall_score', 0):.1f}/100")
                    
                    with col2:
                        st.markdown(f"**Current Position:** {row.get('current_position', 'N/A')}")
                        if 'executive_summary' in row:
                            summary = str(row.get('executive_summary', 'N/A'))
                            st.markdown(f"**Summary:** {summary[:150]}...")
        
        st.markdown("---")
        
        # All Candidates Detail View
        st.markdown("### 👥 Detail Per Kandidat (Klik untuk lihat detail lengkap)")
        
        # Sort options untuk detail view
        view_sorted_df = sorted_df  # Gunakan data yang sudah di-sort
        
        for idx, (_, row) in enumerate(view_sorted_df.iterrows(), 1):
            # Emoji tier
            tier_emoji = {
                'EXCELLENT': '⭐',
                'STRONG': '💪',
                'MEDIUM': '🟢',
                'LOW': '🟡'
            }.get(row.get('tier', ''), '🔵')
            
            # Expander dengan info ringkas
            expander_title = f"{tier_emoji} {row.get('employee_name', 'N/A')} - {row.get('tier', 'N/A')} - Score: {row.get('overall_score', 0):.1f}/100"
            
            with st.expander(expander_title):
                # Header Info
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📊 Overall Score", f"{row.get('overall_score', 0):.1f}/100")
                
                with col2:
                    st.metric("🎯 Tier", row.get('tier', 'N/A'))
                
                with col3:
                    st.metric("💼 Recommendation", row.get('recommendation', 'N/A'))
                
                st.markdown("---")
                
                # Detailed Information
                detail_col1, detail_col2 = st.columns([1, 1])
                
                with detail_col1:
                    st.markdown("#### 📋 Informasi Kandidat")
                    st.markdown(f"**Posisi Saat Ini:** {row.get('current_position', 'N/A')}")
                    st.markdown(f"**Skills:** {row.get('skills', 'N/A')}")
                    st.markdown(f"**Experience:** {row.get('experience', 'N/A')}")
                    
                    if 'bio' in row and pd.notna(row.get('bio')):
                        st.markdown(f"**Bio:** {row.get('bio', 'N/A')}")
                
                with detail_col2:
                    st.markdown("#### 🎯 Breakdown Score")
                    if 'skills_match' in row:
                        st.markdown(f"**Skills Match:** {row.get('skills_match', 0):.1f}/100")
                    if 'experience_score' in row:
                        st.markdown(f"**Experience:** {row.get('experience_score', 0):.1f}/100")
                    if 'cultural_fit' in row:
                        st.markdown(f"**Cultural Fit:** {row.get('cultural_fit', 0):.1f}/100")
                    if 'growth_potential' in row:
                        st.markdown(f"**Growth Potential:** {row.get('growth_potential', 0):.1f}/100")
                
                # Executive Summary
                if 'executive_summary' in row and pd.notna(row.get('executive_summary')):
                    st.markdown("---")
                    st.markdown("#### 📝 Executive Summary")
                    st.info(row.get('executive_summary', 'N/A'))
                
                # Reasoning (jika ada)
                if 'reasoning' in row and pd.notna(row.get('reasoning')):
                    st.markdown("---")
                    st.markdown("#### 💭 AI Reasoning")
                    with st.container():
                        st.markdown(row.get('reasoning', 'N/A'))
                
                # Additional details (red flags, strengths, gaps)
                if any(col in row for col in ['strengths', 'gaps', 'red_flags']):
                    st.markdown("---")
                    detail_col1, detail_col2, detail_col3 = st.columns(3)
                    
                    with detail_col1:
                        if 'strengths' in row and pd.notna(row.get('strengths')):
                            st.markdown("#### ✅ Strengths")
                            st.success(row.get('strengths', 'N/A'))
                    
                    with detail_col2:
                        if 'gaps' in row and pd.notna(row.get('gaps')):
                            st.markdown("#### ⚠️ Gaps")
                            st.warning(row.get('gaps', 'N/A'))
                    
                    with detail_col3:
                        if 'red_flags' in row and pd.notna(row.get('red_flags')):
                            st.markdown("#### 🚩 Red Flags")
                            st.error(row.get('red_flags', 'N/A'))
        
        st.markdown("---")
        
        # Export Options
        st.markdown("### 💾 Export Hasil")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"batch_analysis_{job_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="emp_download_csv"
            )
        
        with col2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                results_df.to_excel(writer, index=False, sheet_name='Analysis Results')
            
            st.download_button(
                label="📥 Download Excel",
                data=output.getvalue(),
                file_name=f"batch_analysis_{job_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="emp_download_excel"
            )
        
        with col3:
            if 'overall_score' in results_df.columns:
                top_candidates = results_df.nlargest(10, 'overall_score')
                csv_top = top_candidates.to_csv(index=False)
                st.download_button(
                    label="📥 Top 10 CSV",
                    data=csv_top,
                    file_name=f"top10_{job_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="emp_download_top10"
                )
        
        # Actions
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Analisis Batch Baru", key="emp_new_batch"):
                for key in ['emp_batch_data', 'emp_batch_filename', 'emp_batch_results', 'emp_result_job_title', 'emp_result_job_criteria']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("📝 Analisis dengan Job Description Berbeda", key="emp_different_job"):
                if 'emp_batch_results' in st.session_state:
                    del st.session_state.emp_batch_results
                st.info("👉 Kembali ke tab **Analisis** untuk menggunakan data yang sama dengan job description berbeda")


if __name__ == "__main__":
    render_ultra_employee_analyzer_page()
