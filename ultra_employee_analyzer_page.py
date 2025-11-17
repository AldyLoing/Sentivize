"""
Ultra Advanced Employee Analyzer Page
======================================
UI page dengan flexible scoring untuk entry-level jobs
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io

from analysis.ultra_employee_analyzer import UltraEmployeeAnalyzer
from utils.human_friendly_formatter import HumanFriendlyFormatter


def render_ultra_employee_analyzer_page():
    """Render halaman Employee Analyzer dengan job complexity detection"""
    
    st.title("👥 Ultra Employee Analyzer")
    st.markdown("### Analisis Karyawan dengan AI Super Pintar")
    st.markdown("---")
    
    # Info banner
    st.info("""
    **Fitur Baru:**
    - ✅ Deteksi kompleksitas pekerjaan otomatis (Entry/Mid/Senior)
    - ✅ Scoring fleksibel untuk posisi entry-level
    - ✅ Fresh graduate friendly evaluation
    - ✅ Reasoning kontekstual seperti HR profesional
    - ✅ Social media auto-search (optional)
    """)
    
    # Initialize analyzer
    if 'employee_analyzer' not in st.session_state:
        with st.spinner("⚙️ Initializing AI Engine..."):
            st.session_state.employee_analyzer = UltraEmployeeAnalyzer()
    
    analyzer = st.session_state.employee_analyzer
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["👤 Single Analysis", "📊 Batch Analysis", "ℹ️ Help"])
    
    # ======================
    # TAB 1: Single Analysis
    # ======================
    with tab1:
        st.markdown("## 🎯 Analisis Single Kandidat")
        
        # Job Description Section
        st.markdown("### 📋 Job Requirements")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            job_title = st.text_input(
                "Judul Posisi",
                placeholder="Contoh: Admin, Customer Service, Software Engineer",
                help="Masukkan nama posisi yang dicari"
            )
        
        with col2:
            st.markdown("**Contoh:**")
            st.caption("- Admin")
            st.caption("- Kasir")
            st.caption("- Data Analyst")
        
        job_criteria = st.text_area(
            "Kriteria Pekerjaan",
            height=150,
            placeholder="Masukkan deskripsi lengkap kriteria, requirements, responsibilities.\n\nContoh untuk Admin:\n- Mengelola administrasi kantor\n- Membuat laporan\n- Komunikasi dengan tim\n- Skill: MS Office, komunikasi baik, detail-oriented\n- Attitude: rajin, bertanggung jawab, proaktif",
            help="Semakin detail, semakin akurat analisisnya. Sistem akan otomatis detect kompleksitas pekerjaan."
        )
        
        st.markdown("---")
        
        # Candidate Data Section
        st.markdown("### 👤 Data Kandidat")
        
        col1, col2 = st.columns(2)
        
        with col1:
            candidate_name = st.text_input("Nama Lengkap", placeholder="Contoh: John Doe")
            candidate_position = st.text_input("Posisi Saat Ini", placeholder="Contoh: Staff Admin")
        
        with col2:
            use_social_media = st.checkbox("Analisis Social Media (Optional)", value=False)
            social_media_url = st.text_input(
                "Social Media URL (Optional)",
                placeholder="https://linkedin.com/in/username",
                disabled=not use_social_media
            )
        
        candidate_skills = st.text_area(
            "Skills & Keahlian",
            height=100,
            placeholder="Masukkan skill yang dimiliki kandidat.\nContoh: MS Office (Excel, Word, PowerPoint), komunikasi, data entry, customer service"
        )
        
        candidate_experience = st.text_area(
            "Pengalaman",
            height=100,
            placeholder="Masukkan pengalaman kerja atau organisasi.\nContoh: Admin di PT ABC (2 tahun), Bendahara OSIS (2020-2021)"
        )
        
        candidate_bio = st.text_area(
            "Bio / Profil Singkat",
            height=100,
            placeholder="Masukkan deskripsi singkat tentang kandidat.\nContoh: Fresh graduate yang termotivasi untuk belajar, memiliki pengalaman organisasi sebagai koordinator event"
        )
        
        # Analyze button
        st.markdown("---")
        
        if st.button("🚀 Mulai Analisis", type="primary", disabled=not (job_title and job_criteria and candidate_name)):
            with st.spinner("🧠 AI sedang menganalisis kandidat..."):
                try:
                    # Prepare employee data
                    employee_data = {
                        'name': candidate_name,
                        'position': candidate_position,
                        'skills': candidate_skills,
                        'experience': candidate_experience,
                        'bio': candidate_bio,
                        'social_media_url': social_media_url if use_social_media else ''
                    }
                    
                    # Run analysis
                    result = analyzer.analyze_employee(
                        employee_data=employee_data,
                        job_criteria=job_criteria,
                        target_position=job_title,
                        use_social_media=use_social_media
                    )
                    
                    # Store result
                    st.session_state.single_analysis_result = result
                    
                    st.success("✅ Analisis selesai!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    st.exception(e)
        
        # Display Results
        if 'single_analysis_result' in st.session_state:
            st.markdown("---")
            st.markdown("## 📊 Hasil Analisis")
            
            result = st.session_state.single_analysis_result
            formatter = HumanFriendlyFormatter()
            
            # Job Complexity Info
            if result.job_profile:
                st.markdown("### 🎯 Analisis Kompleksitas Pekerjaan")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    complexity_color = {
                        'low': '🟢',
                        'mid': '🟡',
                        'high': '🔴'
                    }
                    st.metric(
                        "Complexity",
                        f"{complexity_color.get(result.job_profile.complexity.value, '⚪')} {result.job_profile.complexity.value.upper()}"
                    )
                
                with col2:
                    st.metric(
                        "Fresh Grad OK?",
                        "✅ YES" if result.job_profile.fresh_graduate_friendly else "⚠️ NO"
                    )
                
                with col3:
                    st.metric(
                        "Soft Skill Weight",
                        f"{result.job_profile.soft_skill_weight * 100:.0f}%"
                    )
                
                with col4:
                    st.metric(
                        "Flexibility",
                        f"{result.job_profile.experience_flexibility * 100:.0f}%"
                    )
                
                st.info(f"**Reasoning:** {result.job_profile.reasoning}")
                
                st.markdown("---")
            
            # Main Analysis
            formatter.format_employee_analysis_card(result)
            
            # Export
            st.markdown("---")
            st.markdown("### 💾 Export Hasil")
            
            export_data = result.to_dict()
            df_export = pd.DataFrame([export_data])
            
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"employee_analysis_{result.employee_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # ======================
    # TAB 2: Batch Analysis
    # ======================
    with tab2:
        st.markdown("## 📊 Batch Analysis")
        st.markdown("Analisis multiple kandidat sekaligus dari file Excel/CSV")
        
        # Job Description
        st.markdown("### 📋 Job Requirements")
        
        batch_job_title = st.text_input(
            "Judul Posisi (Batch)",
            placeholder="Contoh: Admin",
            key="batch_job_title"
        )
        
        batch_job_criteria = st.text_area(
            "Kriteria Pekerjaan (Batch)",
            height=150,
            placeholder="Masukkan kriteria lengkap...",
            key="batch_job_criteria"
        )
        
        st.markdown("---")
        
        # File Upload
        st.markdown("### 📤 Upload Data Kandidat")
        
        st.markdown("""
        **Format file yang diperlukan:**
        
        File Excel/CSV dengan kolom:
        - `name`: Nama kandidat
        - `position`: Posisi saat ini
        - `skills`: Keahlian
        - `experience`: Pengalaman
        - `bio`: Profil singkat
        - `social_media_url` (optional): URL social media
        """)
        
        uploaded_file = st.file_uploader(
            "Upload Excel atau CSV",
            type=['xlsx', 'xls', 'csv'],
            help="Upload file dengan format yang sesuai"
        )
        
        if uploaded_file is not None:
            try:
                # Read file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ File loaded: {len(df)} kandidat")
                
                # Display preview
                st.markdown("**Preview Data:**")
                st.dataframe(df.head())
                
                # Validate columns
                required_cols = ['name', 'position', 'skills', 'experience', 'bio']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"❌ Kolom yang hilang: {', '.join(missing_cols)}")
                    st.info("Pastikan file memiliki kolom: name, position, skills, experience, bio")
                else:
                    # Social media option
                    use_social_batch = st.checkbox(
                        "Analisis Social Media untuk semua kandidat",
                        value=False,
                        key="batch_social"
                    )
                    
                    # Analyze button
                    if st.button("🚀 Mulai Batch Analysis", type="primary", disabled=not (batch_job_title and batch_job_criteria)):
                        with st.spinner(f"🧠 Analyzing {len(df)} kandidat... Mohon tunggu..."):
                            try:
                                # Run batch analysis
                                results_df = analyzer.analyze_batch(
                                    employees_df=df,
                                    job_criteria=batch_job_criteria,
                                    target_position=batch_job_title,
                                    use_social_media=use_social_batch
                                )
                                
                                st.session_state.batch_results = results_df
                                
                                st.success("✅ Batch analysis selesai!")
                                st.balloons()
                                
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                                st.exception(e)
            
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        # Display Batch Results
        if 'batch_results' in st.session_state:
            st.markdown("---")
            st.markdown("## 📊 Hasil Batch Analysis")
            
            results_df = st.session_state.batch_results
            
            # Summary stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Kandidat", len(results_df))
            
            with col2:
                excellent = len(results_df[results_df['tier'] == 'EXCELLENT'])
                st.metric("Excellent", excellent)
            
            with col3:
                strong = len(results_df[results_df['tier'] == 'STRONG'])
                st.metric("Strong", strong)
            
            with col4:
                avg_score = results_df['overall_score'].mean()
                st.metric("Avg Score", f"{avg_score:.1f}")
            
            # Display table
            st.markdown("### 📋 Tabel Hasil")
            st.dataframe(
                results_df.sort_values('overall_score', ascending=False),
                use_container_width=True
            )
            
            # Export
            st.markdown("---")
            st.markdown("### 💾 Export Hasil")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Excel export
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    results_df.to_excel(writer, index=False, sheet_name='Analysis Results')
                
                st.download_button(
                    label="📥 Download as Excel",
                    data=output.getvalue(),
                    file_name=f"batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    # ======================
    # TAB 3: Help
    # ======================
    with tab3:
        st.markdown("## ℹ️ Panduan Penggunaan")
        
        st.markdown("""
        ### 🎯 Cara Kerja Sistem
        
        Sistem ini menggunakan AI super canggih untuk menganalisis kandidat dengan cara yang **fleksibel dan realistis**:
        
        #### 1️⃣ Deteksi Kompleksitas Pekerjaan Otomatis
        
        Sistem akan otomatis mendeteksi apakah pekerjaan termasuk:
        - **Low Complexity (Entry-Level)**: Admin, Kasir, CS, Data Entry, Front Office, dll.
        - **Mid Complexity**: Staff dengan skill spesifik, coordinator, dll.
        - **High Complexity**: Engineer, Manager, Specialist, dll.
        
        #### 2️⃣ Scoring Fleksibel
        
        **Untuk Pekerjaan Entry-Level:**
        - ✅ Fresh graduate TIDAK otomatis ditolak
        - ✅ Soft skill (komunikasi, attitude) lebih penting dari hard skill
        - ✅ Pengalaman organisasi dihargai setara pengalaman kerja ringan
        - ✅ Fokus pada potensi dan kemampuan belajar
        
        **Untuk Pekerjaan High-Level:**
        - ⚠️ Pengalaman relevan sangat penting
        - ⚠️ Hard skill teknis dominan
        - ⚠️ Fresh graduate harus punya project/portfolio kuat
        
        #### 3️⃣ Reasoning Manusiawi
        
        Sistem memberikan penjelasan seperti HR profesional:
        
        > "Untuk posisi Admin yang termasuk entry-level, kandidat ini sangat layak. 
        > Meskipun belum memiliki pengalaman admin langsung, CV menunjukkan kemampuan 
        > organisasi yang baik, dokumentasi yang rapi, dan attitude yang positif."
        
        #### 4️⃣ Tidak Ada Keyword Matching Kaku
        
        Sistem menggunakan **semantic understanding**:
        - Memahami konteks, bukan hanya keyword
        - Mengenali skill implisit dari pengalaman
        - Mendeteksi pola kepemimpinan, problem-solving, inisiatif
        
        ### 💡 Tips Penggunaan
        
        1. **Job Description**: Semakin detail, semakin akurat
        2. **Entry-Level Jobs**: Jangan khawatir dengan fresh graduate
        3. **Data Kandidat**: Input sebanyak mungkin informasi
        4. **Batch Analysis**: Gunakan untuk screening awal banyak kandidat
        
        ### 📞 Troubleshooting
        
        **Q: Fresh graduate mendapat score rendah untuk posisi admin?**
        A: Pastikan job title mengandung kata seperti "admin", "staff", "entry", "junior". 
        Sistem akan otomatis detect sebagai low-complexity dan scoring akan fleksibel.
        
        **Q: Bagaimana jika tidak ada social media?**
        A: Tidak masalah. Social media bersifat optional dan tidak mempengaruhi score utama.
        
        **Q: Candidate level seperti apa yang cocok untuk entry-level?**
        A: Fresh graduate, Junior (0-2 tahun), bahkan yang hanya punya pengalaman organisasi.
        """)


if __name__ == "__main__":
    render_ultra_employee_analyzer_page()
