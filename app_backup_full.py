"""
Sentivize - Advanced AI-Powered HR Analytics
Deep contextual understanding with behavioral profiling and semantic reasoning
Version 2.0 - Advanced Mode Only
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Sentivize - Advanced AI HR Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application with advanced AI navigation"""
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🧠 Sentivize")
        st.caption("Advanced AI-Powered HR Analytics")
        st.markdown("---")
        
        # Module selection - Only Advanced Mode
        st.subheader("📍 Select Module")
        page = st.radio(
            "Choose Analysis Type:",
            ["👥 Employee Analysis", "📄 CV Analyzer"],
            help="Employee Analysis: Behavioral profiling & value alignment | CV Analyzer: Deep resume analysis & relevance scoring"
        )
        
        st.markdown("---")
        
        # Info about advanced features
        st.info("""
        **✨ Advanced AI Features:**
        - 🧠 Deep contextual understanding
        - 🎭 Behavioral profiling
        - 💡 Semantic reasoning
        - 🎯 Personality assessment
        - 🤝 Cultural fit analysis
        - 📊 Multi-dimensional scoring
        """)
        
        st.markdown("---")
        
        # System info
        st.caption("**System:** Advanced NLP Engine")
        st.caption("**Models:** BERT + Transformers")
        st.caption("**Version:** 2.0 Advanced")
    
    # Route to selected page - Always Advanced Mode
    if page == "👥 Employee Analysis":
        from advanced_employee_analyzer_page import render_advanced_employee_analysis_page
        render_advanced_employee_analysis_page()
    elif page == "📄 CV Analyzer":
        from advanced_cv_analyzer_page import render_advanced_cv_analyzer_page
        render_advanced_cv_analyzer_page()


if __name__ == "__main__":
    main()


def display_disclaimer():
    """Tampilkan disclaimer dan informasi penting"""
    with st.expander("⚠️ Disclaimer & Informasi Penting", expanded=False):
        st.warning("""
        **DISCLAIMER:**
        
        1. **Tujuan Analisis**: Aplikasi ini menganalisis data karyawan berdasarkan informasi publik 
           dan menghasilkan skor indikatif. Hasil analisis TIDAK boleh digunakan sebagai 
           satu-satunya dasar keputusan HR/rekrutmen.
        
        2. **Data & Privasi**: 
           - Analisis hanya menggunakan data yang Anda upload dan informasi publik dari internet
           - Pastikan Anda memiliki hak untuk memproses data karyawan yang diupload
           - Sistem dapat mencari profil sosial media publik berdasarkan nama
        
        3. **Scraping & Terms of Service**:
           - Web scraping dapat melanggar Terms of Service platform tertentu
           - Gunakan fitur scraping dengan bijak dan tanggung jawab
           - Pengguna bertanggung jawab mematuhi kebijakan data & privasi
        
        4. **Akurasi Model AI**:
           - Model AI memiliki keterbatasan dan dapat menghasilkan kesalahan
           - Sentiment dan relevance score bersifat probabilistik
           - Harap lakukan validasi manual untuk keputusan penting
        
        5. **Rate Limiting**: Pencarian web memiliki batasan. Jika terlalu banyak request, 
           proses dapat melambat atau gagal.
        """)


def display_instructions():
    """Tampilkan instruksi penggunaan"""
    with st.expander("📖 Cara Menggunakan Aplikasi", expanded=False):
        st.markdown("""
        ### Langkah-langkah:
        
        1. **Upload File Data Karyawan**
           - Format yang didukung: CSV, Excel (.xlsx, .xls), JSON
           - Pastikan file memiliki kolom nama (nama/name/nama lengkap)
           - Kolom opsional: jabatan, unit kerja, social media, deskripsi/bio
        
        2. **Masukkan Kata Kunci**
           - Kata kunci untuk mengukur relevansi kandidat
           - Contoh: "lingkungan", "teknologi", "kepemimpinan"
        
        3. **Pilih Opsi Analisis**
           - Mode Model: Mock (cepat) atau Transformers (akurat tapi lambat)
           - Scraping: Aktifkan jika ingin mengambil posting publik (memerlukan waktu lebih lama)
        
        4. **Jalankan Analisis**
           - Klik tombol "🚀 Mulai Analisis"
           - Tunggu hingga proses selesai (dapat memakan waktu beberapa menit)
        
        5. **Review Hasil**
           - Lihat tabel hasil dengan skor sentiment dan relevansi
           - Eksplorasi visualisasi data
           - Download hasil dalam format Excel
        
        ### Tips:
        - Untuk testing cepat, gunakan Mock Mode
        - Untuk hasil terbaik, gunakan Transformers Mode (download model diperlukan pertama kali)
        - Batasi jumlah kandidat (<50) untuk menghindari timeout
        """)


def render_sidebar():
    """Render sidebar dengan opsi konfigurasi"""
    with st.sidebar:
        st.title("⚙️ Konfigurasi")
        
        # Model selection
        st.subheader("Model AI")
        use_mock = st.checkbox(
            "Gunakan Mock Mode (Testing Cepat)",
            value=False,
            help="Mock mode menggunakan rule-based models untuk testing cepat tanpa download model besar"
        )
        
        if not use_mock:
            st.info("Mode Transformers: Menggunakan Hugging Face models untuk hasil terbaik. Download model diperlukan pada run pertama (~500MB).")
        else:
            st.info("Mock Mode: Menggunakan VADER sentiment + TF-IDF untuk testing cepat.")
        
        # Scraping option
        st.subheader("Web Scraping")
        enable_scraping = st.checkbox(
            "Ambil Posting Publik (Scraping)",
            value=False,
            help="Coba ekstrak teks dari profil sosial media. PERINGATAN: Dapat melanggar ToS platform."
        )
        
        if enable_scraping:
            st.warning("⚠️ Scraping diaktifkan. Pastikan Anda mematuhi kebijakan platform.")
        
        # Social media search
        st.subheader("Pencarian Sosial Media")
        st.info(f"""
        - Max hasil per kandidat: {config.MAX_SEARCH_RESULTS}
        - Max post per akun: {config.MAX_POSTS_PER_ACCOUNT}
        - Platform: LinkedIn, Instagram, Facebook, Twitter/X
        """)
        
        return use_mock, enable_scraping


def render_file_uploader():
    """Render file uploader dan return uploaded file"""
    st.subheader("📁 Upload File Data Karyawan")
    
    uploaded_file = st.file_uploader(
        "Pilih file (CSV, Excel, JSON)",
        type=config.SUPPORTED_FILE_TYPES,
        help="Upload file yang berisi data karyawan dengan minimal kolom nama"
    )
    
    if uploaded_file:
        st.success(f"✅ File '{uploaded_file.name}' berhasil diupload!")
        
        # Preview data with enhanced column detection info
        with st.expander("👁️ Preview Data & Deteksi Kolom", expanded=False):
            try:
                df = services.read_any_file(uploaded_file)
                
                # Show file info
                st.write(f"📊 **Informasi File:** {len(df)} baris, {len(df.columns)} kolom")
                
                # Detect columns
                cols = services.detect_columns(df)
                
                # Show detected columns with better formatting
                st.write("**🎯 Kolom Terdeteksi:**")
                col_status = []
                
                if cols['name_col']:
                    col_status.append(f"✅ **Nama:** `{cols['name_col']}`")
                else:
                    col_status.append(f"❌ **Nama:** Tidak terdeteksi (WAJIB!)")
                    
                if cols['position_col']:
                    col_status.append(f"✅ **Jabatan:** `{cols['position_col']}`")
                else:
                    col_status.append(f"⚪ **Jabatan:** Tidak terdeteksi (opsional)")
                    
                if cols['unit_col']:
                    col_status.append(f"✅ **Unit:** `{cols['unit_col']}`")
                else:
                    col_status.append(f"⚪ **Unit:** Tidak terdeteksi (opsional)")
                    
                if cols['social_col']:
                    col_status.append(f"✅ **Social Media:** `{cols['social_col']}`")
                    
                if cols['text_col']:
                    col_status.append(f"✅ **Teks/Deskripsi:** `{cols['text_col']}`")
                
                for status in col_status:
                    st.markdown(status)
                
                st.write("---")
                
                # Show data preview
                st.write("**📋 Preview Data:**")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Show all columns in expandable section
                with st.expander("📂 Lihat Semua Nama Kolom", expanded=False):
                    st.write(", ".join([f"`{col}`" for col in df.columns]))
                
                # Reset file pointer
                uploaded_file.seek(0)
                
            except Exception as e:
                st.error(f"❌ Error preview: {str(e)}")
                st.info("File akan tetap diproses saat analisis dimulai.")
    
    return uploaded_file


def render_keyword_input():
    """Render keyword input dan return keyword"""
    st.subheader("🔑 Kata Kunci atau Maksud Relevansi")
    
    st.markdown("""
    Masukkan **kata kunci**, **frasa**, atau **kalimat lengkap** untuk analisis relevansi.
    Sistem akan menganalisis kesamaan semantik dan konteks.
    """)
    
    # Examples in expander
    with st.expander("💡 Lihat Contoh Penggunaan", expanded=False):
        st.markdown("""
        **Single Keyword:**
        - `teknologi`
        - `kepemimpinan`
        - `hutan`
        
        **Phrase (2-3 kata):**
        - `konservasi hutan`
        - `teknologi digital`
        - `manajemen sumber daya`
        
        **Kalimat/Maksud:**
        - `pengalaman dalam pengelolaan hutan lestari`
        - `kemampuan memimpin tim dan berkomunikasi efektif`
        - `ahli dalam teknologi informasi dan transformasi digital`
        - `berpengalaman menangani masalah lingkungan dan keberlanjutan`
        
        **Tips:**
        - Gunakan kalimat untuk pencarian yang lebih spesifik
        - Sistem akan mencari kesamaan makna, bukan hanya kata exact
        - Semakin detail maksud, semakin akurat hasil analisis
        """)
    
    keyword = st.text_input(
        "Masukkan kata kunci, frasa, atau kalimat",
        placeholder="Contoh: pengalaman dalam pengelolaan dan konservasi hutan",
        help="Bisa berupa kata tunggal, frasa, atau kalimat lengkap yang menjelaskan maksud pencarian",
        max_chars=500
    )
    
    if keyword:
        # Detect type
        word_count = len(keyword.split())
        if word_count == 1:
            keyword_type = "Kata Kunci"
            icon = "🔤"
        elif word_count <= 3:
            keyword_type = "Frasa"
            icon = "📝"
        else:
            keyword_type = "Kalimat/Maksud"
            icon = "💬"
        
        st.info(f"{icon} **{keyword_type}:** {keyword} ({word_count} kata)")
        
        if word_count > 5:
            st.success("✨ Pencarian dengan kalimat lengkap akan menggunakan analisis semantik untuk kesamaan makna!")
    
    return keyword


def create_visualizations(results_df: pd.DataFrame):
    """Buat dan tampilkan visualisasi hasil analisis"""
    
    st.subheader("📊 Visualisasi Hasil")
    
    # Top 10 Candidates with Detailed Reasoning
    st.write("### 🏆 Top 10 Kandidat Berdasarkan Relevansi")
    st.write("Berikut adalah 10 kandidat teratas dengan alasan detail kenapa mereka masuk dalam daftar:")
    
    top_10 = results_df.head(10)
    
    # Display each candidate with reasoning
    for idx, row in top_10.iterrows():
        rank = idx + 1
        
        with st.expander(f"**#{rank}. {row['Name']}** - Relevance Score: {row['Relevance Score']:.3f}", expanded=(rank <= 3)):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📋 Alasan Masuk Top 10")
                st.markdown(row['Overall Reasoning'])
                
                st.markdown("---")
                st.markdown("#### 🔍 Detail Relevansi")
                st.write(row['Relevance Reasoning'])
                
            with col2:
                st.markdown("#### 📊 Metrics")
                st.metric("Relevance Score", f"{row['Relevance Score']:.3f}")
                st.metric("Sentiment", row['Sentiment Label'], f"{row['Sentiment Score']:.3f}")
                
                if row['Position'] != '-':
                    st.markdown(f"**Jabatan:** {row['Position']}")
                if row['Unit'] != '-':
                    st.markdown(f"**Unit:** {row['Unit']}")
                
                st.markdown(f"**Data Sources:** {row['Texts Analyzed']} teks")
    
    st.write("---")
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 bar chart
        st.write("**Grafik Top 10 Kandidat**")
        
        fig_relevance = px.bar(
            top_10,
            x='Relevance Score',
            y='Name',
            orientation='h',
            color='Relevance Score',
            color_continuous_scale='Viridis',
            title='Top 10 Kandidat - Relevance Score',
            hover_data=['Position', 'Sentiment Label']
        )
        fig_relevance.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_relevance, use_container_width=True)
    
    with col2:
        # Sentiment distribution
        st.write("**Distribusi Sentiment**")
        sentiment_counts = results_df['Sentiment Label'].value_counts()
        
        colors = {
            config.SENTIMENT_POSITIVE: '#28a745',
            config.SENTIMENT_NEUTRAL: '#ffc107',
            config.SENTIMENT_NEGATIVE: '#dc3545'
        }
        
        fig_sentiment = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            marker=dict(colors=[colors.get(label, '#6c757d') for label in sentiment_counts.index]),
            hole=0.4
        )])
        fig_sentiment.update_layout(
            title='Distribusi Sentiment Kandidat',
            height=400
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Scatter plot: Relevance vs Sentiment
    st.write("**Scatter Plot: Relevance Score vs Sentiment Score**")
    fig_scatter = px.scatter(
        results_df,
        x='Relevance Score',
        y='Sentiment Score',
        color='Sentiment Label',
        hover_data=['Name', 'Position'],
        color_discrete_map={
            config.SENTIMENT_POSITIVE: '#28a745',
            config.SENTIMENT_NEUTRAL: '#ffc107',
            config.SENTIMENT_NEGATIVE: '#dc3545'
        },
        title='Perbandingan Relevance dan Sentiment Score'
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Distribution of scores
    col3, col4 = st.columns(2)
    
    with col3:
        fig_hist_rel = px.histogram(
            results_df,
            x='Relevance Score',
            nbins=20,
            title='Distribusi Relevance Score'
        )
        fig_hist_rel.update_layout(height=300)
        st.plotly_chart(fig_hist_rel, use_container_width=True)
    
    with col4:
        fig_hist_sent = px.histogram(
            results_df,
            x='Sentiment Score',
            nbins=20,
            title='Distribusi Sentiment Score'
        )
        fig_hist_sent.update_layout(height=300)
        st.plotly_chart(fig_hist_sent, use_container_width=True)


def display_summary_stats(results_df: pd.DataFrame):
    """Tampilkan summary statistics"""
    st.subheader("📈 Ringkasan Statistik")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Kandidat",
            len(results_df)
        )
    
    with col2:
        avg_relevance = results_df['Relevance Score'].mean()
        st.metric(
            "Rata-rata Relevance",
            f"{avg_relevance:.3f}"
        )
    
    with col3:
        avg_sentiment = results_df['Sentiment Score'].mean()
        st.metric(
            "Rata-rata Sentiment",
            f"{avg_sentiment:.3f}"
        )
    
    with col4:
        with_social = len(results_df[results_df['Social Media Count'] > 0])
        st.metric(
            "Dengan Social Media",
            f"{with_social} ({with_social/len(results_df)*100:.1f}%)"
        )


def create_excel_download_link(results_df: pd.DataFrame) -> BytesIO:
    """Buat Excel file dalam memory untuk download"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Main results
        results_df.to_excel(writer, sheet_name='Hasil Analisis', index=False)
        
        # Summary
        summary_data = {
            'Metric': [
                'Total Kandidat',
                'Rata-rata Relevance Score',
                'Rata-rata Sentiment Score',
                'Jumlah Positive Sentiment',
                'Jumlah Negative Sentiment',
                'Jumlah Neutral Sentiment',
                'Kandidat dengan Social Media',
                'Kandidat tanpa Social Media'
            ],
            'Value': [
                len(results_df),
                round(results_df['Relevance Score'].mean(), 3),
                round(results_df['Sentiment Score'].mean(), 3),
                len(results_df[results_df['Sentiment Label'] == config.SENTIMENT_POSITIVE]),
                len(results_df[results_df['Sentiment Label'] == config.SENTIMENT_NEGATIVE]),
                len(results_df[results_df['Sentiment Label'] == config.SENTIMENT_NEUTRAL]),
                len(results_df[results_df['Social Media Count'] > 0]),
                len(results_df[results_df['Social Media Count'] == 0])
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    output.seek(0)
    return output


def main_original():
    """Original main application function - Employee Analysis"""
    
    # Header
    st.title("🔍 Sentivize - Analisis Karyawan dengan AI")
    st.markdown("*Aplikasi analisis data karyawan menggunakan sentiment analysis dan relevance scoring*")
    
    # Disclaimer
    display_disclaimer()
    
    # Instructions
    display_instructions()
    
    st.divider()
    
    # Sidebar configuration
    use_mock, enable_scraping = render_sidebar()
    
    # Main content
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # File uploader
        uploaded_file = render_file_uploader()
    
    with col_right:
        # Keyword input
        keyword = render_keyword_input()
    
    st.divider()
    
    # Analysis button
    if uploaded_file and keyword:
        if st.button("🚀 Mulai Analisis", type="primary", use_container_width=True):
            run_employee_analysis(uploaded_file, keyword, use_mock, enable_scraping)
    
    elif uploaded_file:
        st.info("👆 Masukkan kata kunci untuk memulai analisis")
    else:
        st.info("👆 Upload file data karyawan untuk memulai")
    
    # Display results if available
    if 'results_df' in st.session_state:
        display_employee_results()


def run_employee_analysis(uploaded_file, keyword, use_mock, enable_scraping):
    """Run employee analysis process"""
    
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Load data
        status_text.text("📂 Memuat data...")
        df = services.read_any_file(uploaded_file)
        progress_bar.progress(10)
        
        st.info(f"📊 Memproses {len(df)} kandidat dengan kata kunci: **{keyword}**")
        
        if enable_scraping:
            st.warning("⚠️ Scraping diaktifkan - proses akan memakan waktu lebih lama")
        
        # Define progress callback
        def update_progress(current, total):
            progress = 10 + int((current / total) * 80)
            progress_bar.progress(progress)
            status_text.text(f"🔄 Menganalisis kandidat {current}/{total}...")
        
        # Run analysis
        status_text.text("🤖 Memuat model AI...")
        results_df = analyzer.analyze_candidates(
            df=df,
            keyword=keyword,
            enable_scraping=enable_scraping,
            use_mock_models=use_mock,
            progress_callback=update_progress
        )
        
        progress_bar.progress(90)
        status_text.text("💾 Menyimpan hasil...")
        
        # Save to session state
        st.session_state['results_df'] = results_df
        st.session_state['keyword'] = keyword
        
        progress_bar.progress(100)
        status_text.text("✅ Analisis selesai!")
        
        st.success(f"🎉 Berhasil menganalisis {len(results_df)} kandidat!")
        
    except Exception as e:
        st.error(f"❌ Error saat analisis: {str(e)}")
        st.exception(e)
        return


def display_employee_results():
    """Display employee analysis results"""
    
    st.divider()
    st.header("📊 Hasil Analisis")
    
    results_df = st.session_state['results_df']
    keyword = st.session_state.get('keyword', '')
    
    # Summary stats
    display_summary_stats(results_df)
    
    st.divider()
    
    # Visualizations
    create_visualizations(results_df)
    
    st.divider()
    
    # Results table
    st.subheader("📋 Tabel Hasil Lengkap")
    
    # Display options
    col1, col2 = st.columns([3, 1])
    with col1:
        search_name = st.text_input("🔍 Cari nama kandidat", "")
    with col2:
        min_relevance = st.slider("Min Relevance Score", 0.0, 1.0, 0.0, 0.1)
    
    # Filter data
    filtered_df = results_df.copy()
    if search_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False, na=False)]
    if min_relevance > 0:
        filtered_df = filtered_df[filtered_df['Relevance Score'] >= min_relevance]
    
    st.write(f"Menampilkan {len(filtered_df)} dari {len(results_df)} kandidat")
    
    # Display dataframe
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Sentiment Score": st.column_config.ProgressColumn(
                "Sentiment Score",
                min_value=0,
                max_value=1
            ),
            "Relevance Score": st.column_config.ProgressColumn(
                "Relevance Score",
                min_value=0,
                max_value=1
            )
        }
    )
    
    st.divider()
    
    # Download button
    st.subheader("💾 Download Hasil")
    
    excel_file = create_excel_download_link(results_df)
    
    st.download_button(
        label="📥 Download Excel (hasil_analisis.xlsx)",
        data=excel_file,
        file_name=config.OUTPUT_FILENAME,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    
    st.success("✅ Klik tombol di atas untuk download hasil analisis dalam format Excel")


if __name__ == "__main__":
    main()
