"""
Advanced Employee Analyzer Page - UI untuk deep behavioral analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

import services
from advanced_employee_analyzer import get_advanced_employee_analyzer


def render_advanced_employee_analysis_page():
    """Render advanced employee analysis page"""
    
    st.title("👥 Advanced Employee Analysis")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0;">🧠 Deep Behavioral & Values Analysis</h3>
        <p style="margin: 5px 0 0 0;">AI yang memahami karakter, kepribadian, dan nilai personal dari aktivitas digital - 
        seperti psikolog profesional menganalisis behavior patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Analysis Configuration")
        
        use_mock = st.checkbox(
            "🚀 Mock Mode (Fast)",
            value=True,
            help="Mock mode untuk testing cepat. Transformers mode untuk akurasi maksimal."
        )
        
        st.markdown("---")
        
        enable_scraping = st.checkbox(
            "🌐 Enable Social Media Scraping",
            value=False,
            help="Coba scrape posting dari social media (may be slow)"
        )
        
        enable_behavioral = st.checkbox(
            "🧠 Deep Behavioral Analysis",
            value=True,
            help="Analisis mendalam perilaku, personality traits, dan values"
        )
        
        enable_clustering = st.checkbox(
            "📊 Candidate Clustering",
            value=True,
            help="Kelompokkan kandidat berdasarkan similarity values/traits"
        )
        
        st.markdown("---")
        
        if not use_mock:
            st.info("🎯 **Transformers Mode**\n\nMenggunakan advanced NLP: NER, Topic Modeling, Semantic Understanding")
        else:
            st.success("⚡ **Mock Mode**\n\nRule-based analysis dengan TF-IDF dan VADER sentiment")
    
    # File upload
    st.subheader("📁 Upload Employee Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Supported Formats:** CSV, Excel (xlsx/xls), JSON  
        **Required Column:** Nama / Name  
        **Optional Columns:** Jabatan, Unit, Social Media, Bio
        """)
    
    with col2:
        # Sample data download
        if st.button("📥 Download Sample Data", use_container_width=True):
            sample_df = pd.DataFrame([
                {
                    'Nama': 'John Doe',
                    'Jabatan': 'Software Engineer',
                    'Unit': 'Engineering',
                    'Social Media': 'https://linkedin.com/in/johndoe',
                    'Bio': 'Passionate about clean code and sustainable technology'
                },
                {
                    'Nama': 'Jane Smith',
                    'Jabatan': 'Product Manager',
                    'Unit': 'Product',
                    'Social Media': 'https://linkedin.com/in/janesmith',
                    'Bio': 'Leading product innovation with customer-first mindset'
                }
            ])
            
            buffer = BytesIO()
            sample_df.to_csv(buffer, index=False)
            buffer.seek(0)
            
            st.download_button(
                "Download",
                buffer,
                "sample_employee_data.csv",
                "text/csv",
                use_container_width=True
            )
    
    uploaded_file = st.file_uploader(
        "Upload employee data file",
        type=['csv', 'xlsx', 'xls', 'json'],
        help="File with employee information"
    )
    
    if uploaded_file:
        try:
            df = services.read_any_file(uploaded_file)
            st.success(f"✅ File loaded: {len(df)} employees")
            
            with st.expander("👀 Preview Data", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            df = None
    else:
        df = None
    
    # Keyword/Theme input
    st.subheader("🎯 Value/Theme to Analyze")
    
    # Quick theme templates
    st.markdown("**Quick Templates:**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🌱 Environmental", use_container_width=True):
            st.session_state.employee_keyword = "lingkungan hidup, sustainability, green energy, konservasi, eco-friendly"
    
    with col2:
        if st.button("🚀 Innovation", use_container_width=True):
            st.session_state.employee_keyword = "innovation, technology, digital transformation, creativity, future-thinking"
    
    with col3:
        if st.button("👥 Leadership", use_container_width=True):
            st.session_state.employee_keyword = "leadership, team management, mentoring, strategic thinking, decision making"
    
    with col4:
        if st.button("🤝 Social", use_container_width=True):
            st.session_state.employee_keyword = "community, social responsibility, volunteering, helping others, collaboration"
    
    keyword = st.text_input(
        "Enter value/theme to search for",
        value=st.session_state.get('employee_keyword', ''),
        placeholder="Example: lingkungan hidup, sustainability, peduli alam",
        help="Enter values, themes, or keywords you want to analyze in candidates"
    )
    
    st.session_state.employee_keyword = keyword
    
    # Analysis button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        analyze_button = st.button(
            "🚀 Start Deep Analysis",
            type="primary",
            use_container_width=True,
            disabled=not (df is not None and keyword)
        )
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # Run analysis
    if analyze_button:
        if df is None:
            st.error("❌ Please upload employee data file")
        elif not keyword:
            st.error("❌ Please enter value/theme to analyze")
        else:
            run_advanced_employee_analysis(
                df=df,
                keyword=keyword,
                use_mock=use_mock,
                enable_scraping=enable_scraping,
                enable_behavioral=enable_behavioral,
                enable_clustering=enable_clustering
            )


def run_advanced_employee_analysis(
    df: pd.DataFrame,
    keyword: str,
    use_mock: bool,
    enable_scraping: bool,
    enable_behavioral: bool,
    enable_clustering: bool
):
    """Execute advanced employee analysis"""
    
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize analyzer
        status_text.text("🔧 Initializing advanced AI analyzer...")
        analyzer = get_advanced_employee_analyzer(use_mock_models=use_mock)
        progress_bar.progress(5)
        
        # Detect columns
        columns = services.detect_columns(df)
        
        if not columns['name_col']:
            st.error("❌ Column 'Nama' atau 'Name' tidak ditemukan!")
            return
        
        results = []
        total_employees = len(df)
        
        for idx, row in df.iterrows():
            status_text.text(f"👤 Analyzing employee {idx+1}/{total_employees}...")
            
            try:
                # Extract basic info
                name = str(row[columns['name_col']]).strip()
                if not name or name == 'nan':
                    continue
                
                position = None
                if columns['position_col']:
                    position = str(row[columns['position_col']]).strip()
                    if position == 'nan':
                        position = None
                
                unit = None
                if columns['unit_col']:
                    unit = str(row[columns['unit_col']]).strip()
                    if unit == 'nan':
                        unit = None
                
                # Get social links
                social_links = []
                if columns['social_col']:
                    social_text = str(row[columns['social_col']])
                    social_links = services.extract_social_links_from_text(social_text)
                
                # If no links and scraping enabled, search
                if not social_links and enable_scraping:
                    social_links = services.find_social_media_links(name, max_results=2)
                
                # Collect texts
                texts = []
                
                # Bio/text column
                if columns['text_col']:
                    text_content = str(row[columns['text_col']])
                    if text_content and text_content != 'nan':
                        texts.append(services.clean_text(text_content))
                
                # Scrape if enabled and has links
                if enable_scraping and social_links:
                    for link in social_links[:2]:
                        try:
                            posts = services.scrape_social_posts(link, max_posts=5)
                            texts.extend(posts)
                        except:
                            pass
                
                # Perform advanced analysis
                analysis_result = analyzer.analyze_employee_comprehensive(
                    name=name,
                    position=position,
                    unit=unit,
                    texts=texts,
                    social_links=social_links,
                    keyword=keyword,
                    enable_behavioral_analysis=enable_behavioral
                )
                
                results.append(analysis_result)
                
                progress_bar.progress(5 + int((idx + 1) / total_employees * 85))
                
            except Exception as e:
                st.warning(f"⚠️ Error analyzing {name}: {str(e)}")
                continue
        
        progress_bar.progress(90)
        
        if not results:
            st.error("❌ No employees were successfully analyzed")
            return
        
        # Clustering (if enabled)
        clusters = None
        if enable_clustering and len(results) > 2:
            status_text.text("📊 Performing candidate clustering...")
            clusters = perform_clustering(results)
            progress_bar.progress(95)
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        # Display results
        display_advanced_employee_results(results, keyword, clusters)
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


def perform_clustering(results: list) -> dict:
    """Perform clustering based on value alignment"""
    from sklearn.cluster import KMeans
    import numpy as np
    
    # Extract features for clustering
    features = []
    names = []
    
    for result in results:
        if result.behavioral_profile and result.behavioral_profile.value_alignment:
            values = list(result.behavioral_profile.value_alignment.values())
            features.append(values)
            names.append(result.name)
    
    if len(features) < 3:
        return None
    
    # Perform K-means clustering
    n_clusters = min(3, len(features) // 2)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    
    cluster_labels = kmeans.fit_predict(features)
    
    clusters = {}
    for i in range(n_clusters):
        cluster_members = [names[j] for j in range(len(names)) if cluster_labels[j] == i]
        clusters[f"Cluster {i+1}"] = cluster_members
    
    return clusters


def display_advanced_employee_results(results: list, keyword: str, clusters: dict):
    """Display comprehensive employee analysis results - User-friendly format"""
    
    st.success(f"✅ Berhasil menganalisis {len(results)} karyawan")
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    avg_relevance = sum(r.relevance_score for r in results) / len(results)
    avg_sentiment = sum(r.sentiment_score for r in results) / len(results)
    avg_potential = sum(r.potential_score for r in results) / len(results)
    
    highly_relevant = sum(1 for r in results if r.relevance_score >= 0.7)
    
    with col1:
        st.metric("📊 Rata-rata Kecocokan", f"{avg_relevance*100:.0f}%")
    with col2:
        st.metric("😊 Sentimen Positif", f"{avg_sentiment*100:.0f}%")
    with col3:
        st.metric("⭐ Potensi Rata-rata", f"{avg_potential:.0f}/100")
    with col4:
        st.metric("🎯 Sangat Cocok", f"{highly_relevant}/{len(results)}")
    
    # Create summary dataframe
    summary_data = []
    for result in results:
        summary_data.append({
            'Name': result.name,
            'Position': result.position or '-',
            'Unit': result.unit or '-',
            'Relevance Score': result.relevance_score,
            'Sentiment': result.sentiment_label,
            'Sentiment Score': result.sentiment_score,
            'Potential Score': result.potential_score,
            'Confidence': result.confidence,
            'Social Links': len(result.social_links),
            'Recommendation': result.recommendation.split('\n')[0][:50] + '...'
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.sort_values('Relevance Score', ascending=False).reset_index(drop=True)
    
    # Summary table
    st.subheader("📊 Summary Rankings")
    st.dataframe(
        summary_df.style.background_gradient(
            subset=['Relevance Score', 'Potential Score'],
            cmap='RdYlGn'
        ),
        use_container_width=True
    )
    
    # Visualizations
    st.subheader("📈 Data Visualizations")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Rankings", "🎭 Sentiments", "⭐ Potential", "🌐 Clusters"])
    
    with tab1:
        # Relevance ranking chart
        fig_ranking = go.Figure()
        
        fig_ranking.add_trace(go.Bar(
            y=summary_df['Name'],
            x=summary_df['Relevance Score'],
            orientation='h',
            marker=dict(
                color=summary_df['Relevance Score'],
                colorscale='RdYlGn',
                showscale=True
            ),
            text=[f"{score:.1%}" for score in summary_df['Relevance Score']],
            textposition='auto'
        ))
        
        fig_ranking.update_layout(
            title=f"Employee Relevance to '{keyword}'",
            xaxis_title="Relevance Score",
            yaxis_title="Employee",
            height=max(400, len(results) * 40)
        )
        
        st.plotly_chart(fig_ranking, use_container_width=True, key="ranking_chart")
    
    with tab2:
        # Sentiment distribution
        sentiment_counts = summary_df['Sentiment'].value_counts()
        
        fig_sentiment = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title='Sentiment Distribution',
            color=sentiment_counts.index,
            color_discrete_map={
                'POSITIVE': '#00cc44',
                'NEUTRAL': '#ffaa00',
                'NEGATIVE': '#ff4444'
            }
        )
        
        st.plotly_chart(fig_sentiment, use_container_width=True, key="sentiment_pie_chart")
    
    with tab3:
        # Scatter: Relevance vs Potential
        fig_scatter = px.scatter(
            summary_df,
            x='Relevance Score',
            y='Potential Score',
            size='Confidence',
            color='Sentiment',
            hover_name='Name',
            title='Relevance vs Potential Score',
            labels={'Relevance Score': 'Relevance', 'Potential Score': 'Potential'},
            color_discrete_map={
                'POSITIVE': '#00cc44',
                'NEUTRAL': '#ffaa00',
                'NEGATIVE': '#ff4444'
            }
        )
        
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True, key="potential_scatter_chart")
    
    with tab4:
        if clusters:
            st.markdown("**Candidate Clusters Based on Value Alignment:**")
            
            for cluster_name, members in clusters.items():
                with st.expander(f"{cluster_name} ({len(members)} members)", expanded=True):
                    st.markdown("**Members:**")
                    for member in members:
                        st.markdown(f"- {member}")
        else:
            st.info("Clustering not performed (enable in settings or need more candidates)")
    
    # Detailed individual analysis - User-Friendly Format
    st.markdown("---")
    st.subheader("� Hasil Analisis Detail per Karyawan")
    st.caption("Klik nama karyawan untuk melihat analisis lengkap")
    
    for idx, result in enumerate(results):
        # Create user-friendly individual report
        display_user_friendly_employee_report(result, keyword, idx+1)


def display_user_friendly_employee_report(result, keyword: str, number: int):
    """Display user-friendly employee analysis report with emojis and simple language"""
    
    # Calculate match percentage
    match_score = int(result.relevance_score * 100)
    
    # Determine emoji based on score
    if match_score >= 80:
        score_emoji = "🌟"
        score_label = "Sangat Cocok"
    elif match_score >= 60:
        score_emoji = "✅"
        score_label = "Cocok"
    elif match_score >= 40:
        score_emoji = "💡"
        score_label = "Cukup Cocok"
    else:
        score_emoji = "⚠️"
        score_label = "Kurang Cocok"
    
    # Create expander with attractive title
    with st.expander(
        f"{score_emoji} {number}. {result.name} - {result.position or 'Karyawan'} | Kecocokan: {match_score}%",
        expanded=(number <= 3)  # Auto-expand top 3
    ):
        # Header section with clean design
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
            <h2 style="margin: 0;">👤 {result.name}</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">
                {result.position or 'Karyawan'} 
                {f'| {result.unit}' if result.unit else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: #f0f2f6; border-radius: 10px;">
                <div style="font-size: 32px;">{score_emoji}</div>
                <div style="font-size: 24px; font-weight: bold; color: #667eea;">{match_score}%</div>
                <div style="color: #666;">Skor Kecocokan</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            sentiment_emoji = "😊" if result.sentiment_label == "POSITIVE" else ("😐" if result.sentiment_label == "NEUTRAL" else "😟")
            sentiment_indo = "Positif" if result.sentiment_label == "POSITIVE" else ("Netral" if result.sentiment_label == "NEUTRAL" else "Negatif")
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: #f0f2f6; border-radius: 10px;">
                <div style="font-size: 32px;">{sentiment_emoji}</div>
                <div style="font-size: 18px; font-weight: bold; color: #667eea;">{sentiment_indo}</div>
                <div style="color: #666;">Sentimen</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            potential_score = int(result.potential_score)
            potential_emoji = "⭐" if potential_score >= 75 else ("💫" if potential_score >= 50 else "✨")
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: #f0f2f6; border-radius: 10px;">
                <div style="font-size: 32px;">{potential_emoji}</div>
                <div style="font-size: 24px; font-weight: bold; color: #667eea;">{potential_score}/100</div>
                <div style="color: #666;">Potensi</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 💡 Ringkasan
        st.markdown(f"""
        ### 💡 Ringkasan Singkat
        
        {result.character_assessment}
        """)
        
        st.markdown("---")
        
        # ✅ Kekuatan
        st.markdown("### ✅ Kekuatan Utama")
        
        # Extract strengths from behavioral profile or generate from data
        strengths = []
        if result.behavioral_profile and result.behavioral_profile.green_flags:
            strengths = result.behavioral_profile.green_flags[:3]
        else:
            # Generate basic strengths
            if match_score >= 70:
                strengths.append(f"Menunjukkan ketertarikan yang kuat terhadap {keyword}")
            if result.sentiment_label == "POSITIVE":
                strengths.append("Memiliki sikap positif dan antusiasme tinggi")
            if result.potential_score >= 70:
                strengths.append("Potensi pengembangan yang baik")
        
        if strengths:
            for strength in strengths:
                st.markdown(f"- ✅ {strength}")
        else:
            st.markdown("- Data aktivitas terbatas untuk analisis mendalam")
        
        st.markdown("---")
        
        # ⚠️ Perlu Ditingkatkan
        st.markdown("### ⚠️ Area yang Perlu Ditingkatkan")
        
        concerns = []
        if result.behavioral_profile and result.behavioral_profile.red_flags:
            concerns = result.behavioral_profile.red_flags[:3]
        else:
            # Generate basic concerns
            if match_score < 50:
                concerns.append(f"Konten terkait {keyword} masih terbatas")
            if len(result.social_links) == 0:
                concerns.append("Tidak ditemukan aktivitas media sosial untuk analisis")
            if result.confidence < 0.6:
                concerns.append("Data yang tersedia terbatas untuk analisis akurat")
        
        if concerns:
            for concern in concerns:
                st.markdown(f"- ⚠️ {concern}")
        else:
            st.markdown("- Tidak ada area kritis yang perlu perhatian khusus")
        
        st.markdown("---")
        
        # 🎯 Rekomendasi
        st.markdown("### 🎯 Rekomendasi")
        
        # Generate simple, actionable recommendations
        recommendations = []
        
        if match_score >= 80:
            recommendations.append(f"🌟 **Sangat direkomendasikan** untuk proyek atau posisi terkait {keyword}")
            recommendations.append("💼 Cocok untuk peran leadership atau ambassador program")
        elif match_score >= 60:
            recommendations.append(f"✅ **Direkomendasikan** untuk terlibat dalam inisiatif {keyword}")
            recommendations.append("📚 Berikan pelatihan lanjutan untuk memaksimalkan potensi")
        elif match_score >= 40:
            recommendations.append(f"💡 **Potensial** - Perlu pendampingan dan pengembangan terkait {keyword}")
            recommendations.append("🎓 Sediakan program mentoring dan learning resources")
        else:
            recommendations.append(f"⚠️ **Kurang sesuai** untuk fokus {keyword} saat ini")
            recommendations.append(f"🔄 Pertimbangkan penempatan di area lain yang lebih sesuai dengan minatnya")
        
        for rec in recommendations:
            st.markdown(f"- {rec}")
        
        st.markdown("---")
        
        # 📊 Detail Tambahan (Collapsible)
        with st.expander("📊 Lihat Detail Teknis"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📈 Skor Detail:**")
                st.markdown(f"- Relevansi: {result.relevance_score*100:.1f}%")
                st.markdown(f"- Sentimen: {result.sentiment_score*100:.1f}%")
                st.markdown(f"- Potensi: {result.potential_score:.1f}/100")
                st.markdown(f"- Confidence: {result.confidence*100:.1f}%")
            
            with col2:
                st.markdown("**🔗 Informasi:**")
                st.markdown(f"- Jabatan: {result.position or 'N/A'}")
                st.markdown(f"- Unit: {result.unit or 'N/A'}")
                st.markdown(f"- Social Links: {len(result.social_links)}")
            
            # Value themes if available
            if result.value_themes:
                st.markdown("**💎 Tema Nilai yang Teridentifikasi:**")
                for theme, score in result.value_themes[:5]:
                    st.progress(score, text=f"{theme.title()}: {score*100:.0f}%")


def display_old_detailed_analysis(result, idx):
    """Old detailed view for reference"""
    with st.expander("🔍 Advanced Technical View", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Relevance", f"{result.relevance_score:.1%}")
        with col2:
            st.metric("Sentiment", result.sentiment_label, f"{result.sentiment_score:.1%}")
        with col3:
            st.metric("Potential", f"{result.potential_score:.1%}")
        with col4:
            st.metric("Confidence", f"{result.confidence:.1%}")
            
            # Tabs for different sections
            tab1, tab2, tab3, tab4 = st.tabs([
                "🎯 Assessment", "🧠 Behavioral", "💎 Values", "📊 Details"
            ])
            
            with tab1:
                st.markdown("### Character Assessment")
                st.markdown(result.character_assessment)
                
                st.markdown("---")
                st.markdown("### Recommendation")
                st.markdown(result.recommendation)
            
            with tab2:
                if result.behavioral_profile:
                    profile = result.behavioral_profile
                    
                    st.markdown("### Personality Traits")
                    
                    # Traits radar chart
                    if profile.personality.traits:
                        fig_traits = go.Figure()
                        
                        categories = [k.replace('_', ' ').title() for k in profile.personality.traits.keys()]
                        values = list(profile.personality.traits.values())
                        
                        fig_traits.add_trace(go.Scatterpolar(
                            r=values,
                            theta=categories,
                            fill='toself',
                            name='Traits'
                        ))
                        
                        fig_traits.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                            showlegend=False,
                            height=400
                        )
                        
                        st.plotly_chart(fig_traits, use_container_width=True, key=f"traits_radar_{idx}")
                    
                    # Behavior patterns
                    if profile.personality.behavior_patterns:
                        st.markdown("**Behavior Patterns:**")
                        for pattern in profile.personality.behavior_patterns:
                            st.markdown(f"- {pattern}")
                    
                    # Communication style
                    st.markdown(f"**Communication Style:** {profile.personality.communication_style.title()}")
                    st.markdown(f"**Professional Tone:** {profile.personality.professional_tone.title()}")
                    st.markdown(f"**Social Presence:** {profile.personality.social_presence.title()}")
                    
                    # Professional maturity
                    st.markdown("---")
                    st.markdown("### Professional Maturity")
                    st.progress(profile.professional_maturity)
                    st.markdown(f"Score: {profile.professional_maturity:.0%}")
                    
                    # Flags
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if profile.green_flags:
                            st.markdown("**✅ Positive Indicators:**")
                            for flag in profile.green_flags:
                                st.success(flag)
                    
                    with col2:
                        if profile.red_flags:
                            st.markdown("**⚠️ Areas of Concern:**")
                            for flag in profile.red_flags:
                                st.warning(flag)
                
                else:
                    st.info("Behavioral analysis not available (insufficient data)")
            
            with tab3:
                if result.behavioral_profile:
                    st.markdown("### Value Alignment")
                    
                    # Value alignment bar chart
                    value_df = pd.DataFrame([
                        {'Value': k.replace('_', ' ').title(), 'Score': v}
                        for k, v in result.behavioral_profile.value_alignment.items()
                    ]).sort_values('Score', ascending=False)
                    
                    fig_values = px.bar(
                        value_df,
                        x='Value',
                        y='Score',
                        title='Value Alignment Scores',
                        color='Score',
                        color_continuous_scale='Viridis'
                    )
                    
                    fig_values.update_layout(height=400)
                    st.plotly_chart(fig_values, use_container_width=True, key=f"values_bar_{idx}")
                    
                    # Value themes
                    if result.value_themes:
                        st.markdown("**Key Themes/Interests:**")
                        for theme, score in result.value_themes:
                            st.markdown(f"- {theme.title()} ({score:.0%})")
                
                else:
                    st.info("Value analysis not available")
            
            with tab4:
                st.markdown("### Analysis Details")
                
                st.markdown(f"**Relevance Reasoning:**")
                st.info(result.relevance_reasoning)
                
                if result.social_links:
                    st.markdown("**Social Media Links:**")
                    for link in result.social_links:
                        st.markdown(f"- {link}")
                else:
                    st.markdown("**Social Media:** Not available")
                
                # Posting patterns
                if result.behavioral_profile:
                    st.markdown("**Posting Patterns:**")
                    patterns = result.behavioral_profile.posting_patterns
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Posts", patterns.get('total_posts', 0))
                    with col2:
                        st.metric("Avg Length", patterns.get('avg_length', 0))
                    with col3:
                        st.metric("Diversity", f"{patterns.get('content_diversity', 0):.0%}")
    
    # Download results
    st.markdown("---")
    st.subheader("📥 Export Results")
    
    excel_buffer = create_employee_excel_export(results, keyword)
    
    st.download_button(
        label="📥 Download Complete Analysis (Excel)",
        data=excel_buffer,
        file_name="employee_analysis_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def create_employee_excel_export(results: list, keyword: str) -> BytesIO:
    """Create Excel export with all results"""
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = []
        for result in results:
            summary_data.append({
                'Name': result.name,
                'Position': result.position or '-',
                'Unit': result.unit or '-',
                'Relevance Score': result.relevance_score,
                'Sentiment Label': result.sentiment_label,
                'Sentiment Score': result.sentiment_score,
                'Potential Score': result.potential_score,
                'Confidence': result.confidence,
                'Social Links Count': len(result.social_links),
                'Recommendation': result.recommendation[:200]
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Detailed analysis
        detailed_data = []
        for result in results:
            detailed_data.append({
                'Name': result.name,
                'Character Assessment': result.character_assessment,
                'Relevance Reasoning': result.relevance_reasoning,
                'Recommendation': result.recommendation,
                'Social Links': ', '.join(result.social_links) if result.social_links else 'N/A'
            })
        
        detailed_df = pd.DataFrame(detailed_data)
        detailed_df.to_excel(writer, sheet_name='Detailed', index=False)
        
        # Keyword sheet
        keyword_df = pd.DataFrame([{'Search Keyword/Theme': keyword}])
        keyword_df.to_excel(writer, sheet_name='Criteria', index=False)
    
    output.seek(0)
    return output
