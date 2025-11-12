"""
CV Analyzer Page - UI untuk analisis CV/Resume
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from cv_analyzer import get_cv_analyzer
import plotly.express as px


def render_cv_analyzer_page():
    """Render halaman CV Analyzer"""
    
    st.title("📄 CV/Resume Analyzer")
    st.markdown("""
    Analisis CV/Resume berdasarkan kriteria yang Anda tentukan.
    Upload satu atau beberapa CV, tentukan kriteria, dan sistem akan memberikan scoring + reasoning detail.
    """)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Konfigurasi CV Analyzer")
        
        use_mock = st.checkbox(
            "Gunakan Mock Mode (Testing Cepat)",
            value=True,
            help="Mock mode lebih cepat dan tidak perlu download model besar"
        )
        
        if not use_mock:
            st.info("Mode Transformers: Menggunakan AI models untuk hasil terbaik")
        else:
            st.info("Mock Mode: Menggunakan TF-IDF untuk testing cepat")
    
    # File uploader
    st.subheader("📁 Upload CV/Resume")
    st.markdown("""
    **Format yang Didukung:** PDF, DOCX, TXT
    
    💡 **Tips:**
    - Upload multiple files untuk analisis batch
    - Pastikan CV dalam format yang readable (tidak scan image)
    - File size maksimal: 200MB per file
    """)
    
    uploaded_files = st.file_uploader(
        "Upload CV/Resume Files",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Upload satu atau beberapa CV untuk dianalisis"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file berhasil diupload")
        
        # Show file list
        with st.expander("📋 Daftar File", expanded=False):
            file_info = []
            for f in uploaded_files:
                file_info.append({
                    'Nama File': f.name,
                    'Type': f.type,
                    'Size (KB)': f.size / 1024
                })
            st.dataframe(pd.DataFrame(file_info), use_container_width=True)
    
    # Criteria input
    st.subheader("🎯 Kriteria Pencarian")
    st.markdown("""
    Masukkan **kata kunci**, **frasa**, atau **kalimat lengkap** yang menjelaskan kriteria kandidat ideal Anda.
    """)
    
    with st.expander("💡 Contoh Kriteria", expanded=False):
        st.markdown("""
        **Single Keyword:**
        - `Python`
        - `Leadership`
        - `Marketing`
        
        **Phrase:**
        - `machine learning engineer`
        - `digital marketing specialist`
        - `full stack developer`
        
        **Kalimat/Deskripsi Lengkap:**
        - `pengalaman minimal 3 tahun dalam pengembangan aplikasi web menggunakan Python dan React`
        - `kemampuan memimpin tim dan mengelola project dengan metodologi agile`
        - `background pendidikan S1 Teknik Informatika dengan IPK minimal 3.5`
        - `mahir dalam data analysis menggunakan Python, SQL, dan Tableau`
        - `berpengalaman dalam digital marketing, SEO, dan social media management`
        
        **Kriteria Kombinasi:**
        - `S1 Teknik Informatika, mahir Python dan SQL, pengalaman minimal 2 tahun sebagai data analyst`
        - `lulusan top university, memiliki sertifikasi project management, bahasa Inggris fluent`
        """)
    
    criteria = st.text_area(
        "Masukkan kriteria pencarian",
        placeholder="Contoh: pengalaman minimal 3 tahun dalam pengembangan aplikasi web, mahir Python dan JavaScript, memiliki portofolio project yang kuat",
        height=100,
        max_chars=1000,
        help="Bisa berupa kata kunci tunggal, frasa, atau deskripsi lengkap kandidat ideal"
    )
    
    if criteria:
        word_count = len(criteria.split())
        if word_count == 1:
            st.info(f"🔤 **Kata Kunci:** {criteria}")
        elif word_count <= 5:
            st.info(f"📝 **Frasa:** {criteria} ({word_count} kata)")
        else:
            st.info(f"💬 **Deskripsi Lengkap:** {word_count} kata")
            st.success("✨ Sistem akan menggunakan analisis semantik untuk kesamaan makna!")
    
    # Analyze button
    st.markdown("---")
    
    if st.button("🚀 Mulai Analisis CV", type="primary", disabled=not (uploaded_files and criteria)):
        if not uploaded_files:
            st.error("❌ Silakan upload CV terlebih dahulu")
        elif not criteria:
            st.error("❌ Silakan masukkan kriteria pencarian")
        else:
            analyze_cvs(uploaded_files, criteria, use_mock)


def analyze_cvs(uploaded_files, criteria, use_mock):
    """Proses analisis CV"""
    
    with st.spinner("🔄 Sedang menganalisis CV..."):
        try:
            # Initialize analyzer
            cv_analyzer = get_cv_analyzer(use_mock_models=use_mock)
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(current, total):
                progress = current / total
                progress_bar.progress(progress)
                status_text.text(f"Memproses CV {current}/{total}...")
            
            # Analyze CVs
            results_df = cv_analyzer.analyze_multiple_cvs(
                uploaded_files,
                criteria,
                progress_callback=update_progress
            )
            
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"✅ Analisis selesai! {len(results_df)} CV berhasil dianalisis")
            
            # Display results
            display_cv_results(results_df, criteria)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            import traceback
            with st.expander("🔍 Detail Error"):
                st.code(traceback.format_exc())


def display_cv_results(results_df: pd.DataFrame, criteria: str):
    """Display hasil analisis CV"""
    
    st.markdown("---")
    st.header("📊 Hasil Analisis CV")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total CV", len(results_df))
    
    with col2:
        avg_score = results_df['Relevance Score'].mean()
        st.metric("Avg Relevance", f"{avg_score:.3f}")
    
    with col3:
        top_score = results_df['Relevance Score'].max()
        st.metric("Top Score", f"{top_score:.3f}")
    
    with col4:
        qualified = len(results_df[results_df['Relevance Score'] >= 0.6])
        st.metric("Qualified (≥0.6)", qualified)
    
    # Detailed Results
    st.subheader("📋 Hasil Analisis CV")
    st.markdown(f"**Kriteria:** {criteria}")
    st.markdown(f"**Total CV Dianalisis:** {len(results_df)}")
    
    for idx, row in results_df.iterrows():
        
        # Determine relevance level
        score = row['Relevance Score']
        if score >= 0.7:
            level_icon = "✅"
            level_text = "Sangat Cocok"
            level_color = "green"
        elif score >= 0.5:
            level_icon = "⚠️"
            level_text = "Cukup Cocok"
            level_color = "orange"
        else:
            level_icon = "⚪"
            level_text = "Kurang Cocok"
            level_color = "gray"
        
        with st.expander(
            f"{level_icon} **{row['Nama Kandidat']}** ({row['File Name']}) - Score: {score:.3f}",
            expanded=(idx == 0)  # Expand first result only
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"### {level_icon} {level_text} (Score: {score:.3f})")
                
                st.markdown("#### 📋 Alasan & Analisis")
                st.write(row['Relevance Reasoning'])
                
                if row['Exact Matches'] > 0:
                    st.markdown(f"**🎯 Exact Matches:** {row['Exact Matches']} kali")
                
                if row['Related Words']:
                    st.markdown(f"**🔗 Related Keywords:** {row['Related Words']}")
                
                if row['Match Contexts']:
                    st.markdown("**📝 Context dari CV:**")
                    contexts = row['Match Contexts'].split(' | ')
                    for ctx in contexts[:3]:
                        st.info(ctx)
                
                # Section scores
                section_cols = [col for col in row.index if col.startswith('Score_')]
                if section_cols:
                    st.markdown("**📊 Score per Section:**")
                    section_data = []
                    for col in section_cols:
                        section_name = col.replace('Score_', '')
                        section_score = row[col]
                        if pd.notna(section_score):
                            section_data.append({
                                'Section': section_name,
                                'Score': section_score
                            })
                    
                    if section_data:
                        section_df = pd.DataFrame(section_data)
                        fig = px.bar(
                            section_df,
                            x='Score',
                            y='Section',
                            orientation='h',
                            color='Score',
                            color_continuous_scale='Viridis'
                        )
                        fig.update_layout(height=200, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Metrics")
                st.metric("Relevance Score", f"{row['Relevance Score']:.3f}")
                st.metric("Sentiment", row['Sentiment Label'], f"{row['Sentiment Score']:.3f}")
                
                st.markdown("### 📞 Contact Info")
                st.write(f"**Nama:** {row['Nama Kandidat']}")
                st.write(f"**Email:** {row['Email']}")
                st.write(f"**Phone:** {row['Phone']}")
                
                st.markdown("### 📄 File Info")
                st.write(f"**Type:** {row['File Type']}")
                st.write(f"**Length:** {row['CV Length']} chars")
    
    # Visualizations
    st.markdown("---")
    st.subheader("📈 Visualisasi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution
        fig = px.histogram(
            results_df,
            x='Relevance Score',
            nbins=20,
            title='Distribusi Relevance Score',
            labels={'Relevance Score': 'Score', 'count': 'Jumlah CV'}
        )
        fig.add_vline(x=0.6, line_dash="dash", line_color="red", annotation_text="Threshold")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sentiment distribution
        sentiment_counts = results_df['Sentiment Label'].value_counts()
        fig = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title='Distribusi Sentiment',
            color_discrete_map={
                'POSITIVE': '#28a745',
                'NEUTRAL': '#ffc107',
                'NEGATIVE': '#dc3545'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Full results table
    st.markdown("---")
    st.subheader("📋 Tabel Lengkap Semua CV")
    
    # Select columns to display
    display_columns = [
        'File Name', 'Nama Kandidat', 'Email', 'Phone',
        'Relevance Score', 'Sentiment Label', 'Exact Matches',
        'Related Words', 'CV Length'
    ]
    
    st.dataframe(
        results_df[display_columns].style.background_gradient(
            subset=['Relevance Score'],
            cmap='RdYlGn',
            vmin=0,
            vmax=1
        ),
        use_container_width=True
    )
    
    # Download button
    st.markdown("---")
    st.subheader("📥 Download Hasil")
    
    # Create Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        results_df.to_excel(writer, sheet_name='CV Analysis', index=False)
    
    excel_data = output.getvalue()
    
    st.download_button(
        label="📥 Download Excel",
        data=excel_data,
        file_name="cv_analysis_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


if __name__ == "__main__":
    render_cv_analyzer_page()
