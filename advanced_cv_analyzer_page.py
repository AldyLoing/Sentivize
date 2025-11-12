"""
Advanced CV Analyzer Page - UI untuk deep CV analysis
"""

import streamlit as st
import pandas as pd
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
from typing import List

from advanced_cv_analyzer import get_advanced_cv_analyzer


def render_advanced_cv_analyzer_page():
    """Render advanced CV analyzer page dengan visualisasi rich"""
    
    st.title("📄 Advanced CV/Resume Analyzer")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0;">🧠 AI-Powered Deep CV Analysis</h3>
        <p style="margin: 5px 0 0 0;">Sistem AI yang memahami CV secara kontekstual dan semantik - 
        bukan hanya membaca teks, tapi benar-benar memahami maknanya seperti HR profesional.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Konfigurasi Analyzer")
        
        use_mock = st.checkbox(
            "🚀 Mock Mode (Fast)",
            value=True,
            help="Mock mode: cepat, tidak perlu download model besar. Transformers mode: akurasi tertinggi dengan AI models."
        )
        
        st.markdown("---")
        
        if not use_mock:
            st.info("🎯 **Transformers Mode**\n\nMenggunakan BERT, sentence transformers, dan NER models untuk analisis mendalam.")
        else:
            st.success("⚡ **Mock Mode**\n\nMenggunakan TF-IDF dan rule-based NLP untuk analisis cepat.")
        
        st.markdown("---")
        
        # Analysis options
        st.subheader("🎛️ Opsi Analisis")
        
        enable_deep_parsing = st.checkbox(
            "Deep Parsing",
            value=True,
            help="Extract dan parse CV sections secara detail"
        )
        
        enable_personality = st.checkbox(
            "Personality Assessment",
            value=True,
            help="Assess soft skills dan traits dari CV content"
        )
        
        enable_fit_analysis = st.checkbox(
            "Cultural Fit Analysis",
            value=True,
            help="Analisis kesesuaian budaya dan nilai"
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📁 Upload CV/Resume")
        st.markdown("""
        **Supported Formats:** PDF, DOCX, TXT  
        💡 **Tip:** Upload multiple files untuk batch analysis
        """)
    
    with col2:
        st.metric(
            "Analysis Depth",
            "Deep" if not use_mock else "Standard",
            delta="AI-Powered" if not use_mock else "Fast Mode"
        )
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Drop CV files here",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Upload one or more CV files",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")
        
        with st.expander("📋 Uploaded Files", expanded=False):
            file_df = pd.DataFrame([
                {
                    'Filename': f.name,
                    'Type': f.type,
                    'Size (KB)': f"{f.size / 1024:.1f}"
                }
                for f in uploaded_files
            ])
            st.dataframe(file_df, use_container_width=True)
    
    # Criteria input
    st.subheader("🎯 Job Requirements / Criteria")
    
    # Provide templates
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👨‍💻 Software Engineer", use_container_width=True):
            st.session_state.criteria = "3+ years experience in web development, proficient in Python and JavaScript, experience with React and Django, strong problem-solving skills, bachelor's degree in Computer Science"
    
    with col2:
        if st.button("📊 Data Analyst", use_container_width=True):
            st.session_state.criteria = "2+ years experience in data analysis, proficient in SQL and Python, experience with data visualization tools (Tableau/PowerBI), strong analytical skills, bachelor's degree in Statistics or related field"
    
    with col3:
        if st.button("🎨 UI/UX Designer", use_container_width=True):
            st.session_state.criteria = "3+ years in UI/UX design, expert in Figma and Adobe Creative Suite, portfolio demonstrating mobile and web design, understanding of design systems, bachelor's degree in Design"
    
    criteria = st.text_area(
        "Enter job requirements or ideal candidate criteria",
        value=st.session_state.get('criteria', ''),
        placeholder="Example: 3+ years experience in software development, proficient in Python and React, bachelor's degree in Computer Science, strong problem-solving and communication skills",
        height=120,
        help="Describe the ideal candidate: skills, experience, education, and soft skills"
    )
    
    st.session_state.criteria = criteria
    
    # Advanced criteria (collapsible)
    with st.expander("🔧 Advanced Criteria (Optional)", expanded=False):
        st.markdown("**Break down specific requirements:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            required_skills = st.text_input(
                "Required Technical Skills",
                placeholder="Python, SQL, React, etc."
            )
            
            min_experience = st.slider(
                "Minimum Years of Experience",
                0, 15, 2
            )
        
        with col2:
            required_education = st.text_input(
                "Education Requirements",
                placeholder="Bachelor in Computer Science"
            )
            
            seniority_level = st.selectbox(
                "Seniority Level",
                ["Any", "Entry-Level", "Mid-Level", "Senior", "Executive"]
            )
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        analyze_button = st.button(
            "🚀 Analyze CVs",
            type="primary",
            use_container_width=True,
            disabled=not (uploaded_files and criteria)
        )
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    with col3:
        if st.button("💡 Tips", use_container_width=True):
            st.session_state.show_tips = not st.session_state.get('show_tips', False)
    
    # Show tips if requested
    if st.session_state.get('show_tips', False):
        st.info("""
        **💡 Tips for Best Results:**
        
        1. **Criteria Quality:** Be specific and detailed in your job requirements
        2. **CV Format:** Ensure CVs are text-readable (not scanned images)
        3. **Batch Analysis:** Analyze 5-10 CVs at once for comparison
        4. **Transformers Mode:** Use for final selection (slower but more accurate)
        5. **Mock Mode:** Use for quick screening (faster, good accuracy)
        """)
    
    # Analysis execution
    if analyze_button:
        if not uploaded_files:
            st.error("❌ Please upload at least one CV file")
        elif not criteria:
            st.error("❌ Please enter job requirements/criteria")
        else:
            run_advanced_cv_analysis(
                uploaded_files,
                criteria,
                use_mock,
                enable_deep_parsing,
                enable_personality,
                enable_fit_analysis
            )


def run_advanced_cv_analysis(
    files: List,
    criteria: str,
    use_mock: bool,
    enable_deep_parsing: bool,
    enable_personality: bool,
    enable_fit_analysis: bool
):
    """Run the advanced CV analysis"""
    
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize analyzer
        status_text.text("🔧 Initializing AI analyzer...")
        analyzer = get_advanced_cv_analyzer(use_mock_models=use_mock)
        progress_bar.progress(10)
        
        results = []
        total_files = len(files)
        
        for idx, cv_file in enumerate(files):
            status_text.text(f"📄 Analyzing {cv_file.name} ({idx+1}/{total_files})...")
            
            try:
                # Extract text
                if cv_file.name.endswith('.pdf'):
                    cv_text = analyzer.parser.extract_text_from_pdf(cv_file)
                elif cv_file.name.endswith('.docx'):
                    cv_text = analyzer.parser.extract_text_from_docx(cv_file)
                else:
                    cv_text = cv_file.read().decode('utf-8')
                
                if not cv_text or len(cv_text) < 50:
                    st.warning(f"⚠️ {cv_file.name}: CV text too short or empty")
                    continue
                
                # Perform deep analysis
                analysis_result = analyzer.analyze_cv_deep(
                    cv_text=cv_text,
                    criteria=criteria
                )
                
                results.append({
                    'filename': cv_file.name,
                    'result': analysis_result
                })
                
                progress_bar.progress(10 + int((idx + 1) / total_files * 80))
                
            except Exception as e:
                st.error(f"❌ Error analyzing {cv_file.name}: {str(e)}")
                continue
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        if not results:
            st.error("❌ No CVs were successfully analyzed")
            return
        
        # Display results
        display_analysis_results(results, criteria)
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


def display_analysis_results(results: List[dict], criteria: str):
    """Display comprehensive analysis results - User-Friendly Format"""
    
    st.success(f"✅ Berhasil menganalisis {len(results)} CV")
    
    # Create summary dataframe
    summary_data = []
    for item in results:
        filename = item['filename']
        result = item['result']
        
        summary_data.append({
            'Filename': filename,
            'Candidate': result.cv_profile.candidate_name,
            'Relevance Score': result.relevance_score,  # Keep as float for gradient
            'Confidence': result.confidence_score,  # Keep as float
            'Experience': f"{result.cv_profile.total_experience_years} yrs",
            'Seniority': result.cv_profile.seniority_level,
            'Email': result.cv_profile.contact_info.get('email', '-'),
            'Phone': result.cv_profile.contact_info.get('phone', '-')
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Summary table with formatted display
    st.subheader("📊 Summary Table")
    
    # Create styled dataframe
    styled_df = summary_df.style.background_gradient(
        subset=['Relevance Score', 'Confidence'],
        cmap='RdYlGn'
    ).format({
        'Relevance Score': '{:.1%}',
        'Confidence': '{:.1%}'
    })
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Visualization
    st.subheader("📈 Relevance Score Comparison")
    
    # Create chart data
    chart_data = []
    for item in results:
        chart_data.append({
            'Candidate': item['result'].cv_profile.candidate_name,
            'Relevance Score': item['result'].relevance_score,
            'Confidence': item['result'].confidence_score
        })
    
    chart_df = pd.DataFrame(chart_data)
    
    # Horizontal bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=chart_df['Candidate'],
        x=chart_df['Relevance Score'],
        orientation='h',
        name='Relevance Score',
        marker=dict(
            color=chart_df['Relevance Score'],
            colorscale='RdYlGn',
            showscale=True
        ),
        text=[f"{score:.1%}" for score in chart_df['Relevance Score']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Candidate Relevance Ranking",
        xaxis_title="Relevance Score",
        yaxis_title="Candidate",
        height=max(300, len(results) * 60),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analysis for each candidate - User-Friendly Format
    st.markdown("---")
    st.subheader("� Hasil Analisis Detail per CV")
    st.caption("Klik nama kandidat untuk melihat analisis lengkap")
    
    for idx, item in enumerate(results):
        filename = item['filename']
        result = item['result']
        profile = result.cv_profile
        
        # Use user-friendly display
        display_user_friendly_cv_report(result, filename, idx+1, criteria)


def display_user_friendly_cv_report(result, filename: str, number: int, criteria: str):
    """Display user-friendly CV analysis report with emojis and simple language"""
    
    profile = result.cv_profile
    
    # Calculate match percentage
    match_score = int(result.relevance_score * 100)
    
    # Determine emoji and label based on score
    if match_score >= 80:
        score_emoji = "🌟"
        score_label = "Sangat Cocok"
        decision_text = "Strong Hire - Kandidat sangat direkomendasikan!"
    elif match_score >= 65:
        score_emoji = "✅"
        score_label = "Cocok"
        decision_text = "Hire - Kandidat direkomendasikan untuk interview lanjutan"
    elif match_score >= 50:
        score_emoji = "💡"
        score_label = "Cukup Potensial"
        decision_text = "Consider - Pertimbangkan dengan interview mendalam"
    else:
        score_emoji = "⚠️"
        score_label = "Kurang Sesuai"
        decision_text = "Pass - Belum sesuai dengan kriteria saat ini"
    
    # Create attractive expander
    with st.expander(
        f"{score_emoji} {number}. {profile.candidate_name} | Kecocokan: {match_score}%",
        expanded=(number <= 3)  # Auto-expand top 3
    ):
        # Header with gradient
        # Get current role from work experience
        current_role = "Kandidat"
        if profile.work_experiences and len(profile.work_experiences) > 0:
            current_role = profile.work_experiences[0].position
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
            <h2 style="margin: 0;">📄 {profile.candidate_name}</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">
                {current_role} | {profile.total_experience_years} tahun pengalaman
            </p>
            <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 14px;">
                📁 {filename}
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
                <div style="color: #666;">Kesesuaian</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            exp_emoji = "🏆" if profile.total_experience_years >= 5 else ("💼" if profile.total_experience_years >= 2 else "🌱")
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: #f0f2f6; border-radius: 10px;">
                <div style="font-size: 32px;">{exp_emoji}</div>
                <div style="font-size: 24px; font-weight: bold; color: #667eea;">{profile.total_experience_years}</div>
                <div style="color: #666;">Tahun Pengalaman</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            confidence_score = int(result.confidence_score * 100)
            conf_emoji = "💯" if confidence_score >= 80 else ("👍" if confidence_score >= 60 else "🤔")
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: #f0f2f6; border-radius: 10px;">
                <div style="font-size: 32px;">{conf_emoji}</div>
                <div style="font-size: 24px; font-weight: bold; color: #667eea;">{confidence_score}%</div>
                <div style="color: #666;">Confidence</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 💡 Ringkasan
        st.markdown("### 💡 Ringkasan Kandidat")
        
        # Generate simple summary
        summary_parts = []
        
        if profile.professional_summary:
            summary_parts.append(profile.professional_summary[:200] + "...")
        else:
            summary_parts.append(f"{profile.candidate_name} adalah kandidat dengan {profile.total_experience_years} tahun pengalaman sebagai {current_role}.")
        
        # Add education info
        if profile.education and len(profile.education) > 0:
            edu_level = profile.education[0].degree if profile.education[0].degree else "Sarjana"
            summary_parts.append(f"Pendidikan terakhir: {edu_level}.")
        
        # Add skill summary
        technical_skills = profile.skills.get('technical', [])
        if technical_skills:
            top_skills = technical_skills[:5]
            summary_parts.append(f"Keahlian utama meliputi {', '.join(top_skills)}.")
        
        st.markdown(" ".join(summary_parts))
        
        st.markdown("---")
        
        # ✅ Kekuatan
        st.markdown("### ✅ Kekuatan Kandidat")
        
        strengths = []
        
        # Experience strength
        if profile.total_experience_years >= 5:
            strengths.append(f"✅ Pengalaman profesional yang solid ({profile.total_experience_years} tahun)")
        elif profile.total_experience_years >= 2:
            strengths.append(f"✅ Pengalaman yang memadai ({profile.total_experience_years} tahun)")
        
        # Skills match
        skill_score = result.relevance_breakdown.get('skills', 0) if hasattr(result, 'relevance_breakdown') else 0
        if skill_score >= 0.7:
            strengths.append(f"✅ Keahlian teknis sangat sesuai dengan kebutuhan ({int(skill_score*100)}% match)")
        elif skill_score >= 0.5:
            strengths.append(f"✅ Keahlian teknis cukup sesuai ({int(skill_score*100)}% match)")
        
        # Education
        if profile.education and len(profile.education) > 0:
            edu_degree = profile.education[0].degree.lower() if profile.education[0].degree else ""
            if any(degree in edu_degree for degree in ['master', 's2', 'phd', 's3', 'magister', 'doktor']):
                strengths.append(f"✅ Pendidikan tinggi: {profile.education[0].degree}")
        
        # Soft skills from analysis
        soft_skills = profile.skills.get('soft', [])
        if soft_skills:
            strengths.append(f"✅ Soft skills: {', '.join(soft_skills[:3])}")
        
        # Industry experience
        if hasattr(result, 'industry_fit_score') and result.industry_fit_score >= 0.7:
            strengths.append("✅ Pengalaman industri yang relevan")
        
        # Show strengths or default
        if strengths:
            for strength in strengths[:5]:
                st.markdown(f"- {strength}")
        else:
            st.markdown("- ✅ CV terstruktur dengan baik dan mudah dibaca")
            st.markdown("- ✅ Informasi kontak lengkap")
        
        st.markdown("---")
        
        # ⚠️ Perlu Ditingkatkan
        st.markdown("### ⚠️ Area yang Perlu Diperhatikan")
        
        concerns = []
        
        # Experience concerns
        if profile.total_experience_years < 2:
            concerns.append("⚠️ Pengalaman profesional masih terbatas")
        
        # Skill gaps
        if skill_score < 0.5:
            concerns.append("⚠️ Beberapa keahlian penting belum tercantum dalam CV")
        
        # Missing information
        if not profile.contact_info.get('email'):
            concerns.append("⚠️ Email tidak ditemukan di CV")
        
        if not profile.professional_summary:
            concerns.append("⚠️ Tidak ada ringkasan profesional di CV")
        
        # Confidence concerns
        if result.confidence_score < 0.6:
            concerns.append("⚠️ Informasi di CV kurang detail untuk analisis mendalam")
        
        # Show concerns or default
        if concerns:
            for concern in concerns[:5]:
                st.markdown(f"- {concern}")
        else:
            st.markdown("- Tidak ada area kritis yang perlu perhatian khusus")
            st.markdown("- CV cukup komprehensif dan informatif")
        
        st.markdown("---")
        
        # 🎯 Rekomendasi
        st.markdown("### 🎯 Rekomendasi Tindakan")
        
        st.markdown(f"""
        <div style="background: {'#d4edda' if match_score >= 65 else '#fff3cd' if match_score >= 50 else '#f8d7da'}; 
                    padding: 15px; border-radius: 8px; border-left: 4px solid {'#28a745' if match_score >= 65 else '#ffc107' if match_score >= 50 else '#dc3545'};">
            <strong>📊 Keputusan: {decision_text}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")  # Spacing
        
        # Actionable recommendations
        recommendations = []
        
        if match_score >= 80:
            recommendations.append("🌟 **Prioritas Tinggi** - Undang untuk interview segera")
            recommendations.append("📞 **Contact ASAP** - Kandidat potensial strong hire")
            recommendations.append("💼 **Persiapkan Offer** - Diskusikan kompensasi dan benefit")
        elif match_score >= 65:
            recommendations.append("✅ **Lanjutkan ke Tahap Interview** - Kandidat memenuhi kriteria")
            recommendations.append("📋 **Verify Skills** - Konfirmasi keahlian teknis saat interview")
            recommendations.append("🎯 **Assess Cultural Fit** - Evaluasi kesesuaian dengan tim")
        elif match_score >= 50:
            recommendations.append("💡 **Consider dengan Interview Mendalam** - Gali potensi lebih jauh")
            recommendations.append("📚 **Tanyakan tentang Gap** - Diskusikan area yang kurang")
            recommendations.append("🔄 **Pertimbangkan Posisi Alternatif** - Mungkin cocok di posisi lain")
        else:
            recommendations.append("⚠️ **Belum Sesuai** - Tidak memenuhi kriteria minimum saat ini")
            recommendations.append("📁 **Keep in Database** - Simpan untuk peluang future")
            recommendations.append("🔍 **Cari Kandidat Lain** - Fokus pada CV dengan match lebih tinggi")
        
        for rec in recommendations:
            st.markdown(f"- {rec}")
        
        st.markdown("---")
        
        # 📊 Detail Teknis (Collapsible)
        with st.expander("📊 Lihat Detail Teknis & Scoring"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📈 Breakdown Skor:**")
                st.markdown(f"- Overall Relevance: {result.relevance_score*100:.1f}%")
                st.markdown(f"- Confidence Level: {result.confidence_score*100:.1f}%")
                if skill_score > 0:
                    st.markdown(f"- Skill Match: {skill_score*100:.1f}%")
                exp_score = result.relevance_breakdown.get('experience', 0) if hasattr(result, 'relevance_breakdown') else 0
                if exp_score > 0:
                    st.markdown(f"- Experience Score: {exp_score*100:.1f}%")
            
            with col2:
                st.markdown("**📞 Informasi Kontak:**")
                st.markdown(f"- Email: {profile.contact_info.get('email', 'N/A')}")
                st.markdown(f"- Phone: {profile.contact_info.get('phone', 'N/A')}")
                st.markdown(f"- LinkedIn: {profile.contact_info.get('linkedin', 'N/A')}")
                st.markdown(f"- Location: {profile.contact_info.get('location', 'N/A')}")
            
            # Skills breakdown
            technical_skills = profile.skills.get('technical', [])
            if technical_skills:
                st.markdown("**💻 Keahlian Teknis:**")
                skills_text = ", ".join(technical_skills[:15])
                st.markdown(f"_{skills_text}_")
            
            # Experience timeline
            if profile.work_experiences and len(profile.work_experiences) > 0:
                st.markdown("**💼 Pengalaman Kerja:**")
                for i, exp in enumerate(profile.work_experiences[:3], 1):
                    exp_text = f"{exp.position} at {exp.company}" if hasattr(exp, 'company') else exp.position
                    if hasattr(exp, 'duration'):
                        exp_text += f" ({exp.duration})"
                    st.markdown(f"{i}. {exp_text}")


def display_old_cv_detailed_view(result, filename):
    """Old detailed CV view for technical reference"""
    profile = result.cv_profile
    
    with st.expander(f"📄 {profile.candidate_name} ({filename})", expanded=False):
            
            # Top metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Relevance", f"{result.relevance_score:.1%}")
            with col2:
                st.metric("Confidence", f"{result.confidence_score:.1%}")
            with col3:
                st.metric("Experience", f"{profile.total_experience_years} yrs")
            with col4:
                st.metric("Seniority", profile.seniority_level.split('-')[0])
            
            # Tabs for different sections
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "👤 Profile", "💪 Strengths", "📊 Breakdown", "🎯 Assessment", "📞 Contact"
            ])
            
            with tab1:
                st.markdown("### Candidate Profile")
                
                # Professional summary
                if profile.professional_summary:
                    st.markdown("**Professional Summary:**")
                    st.info(profile.professional_summary[:300] + "..." if len(profile.professional_summary) > 300 else profile.professional_summary)
                
                # Work experience
                if profile.work_experiences:
                    st.markdown("**Work Experience:**")
                    for exp in profile.work_experiences[:3]:
                        st.markdown(f"""
                        **{exp.position}** at **{exp.company}**  
                        📅 {exp.duration} ({exp.years} years)
                        """)
                        
                        if exp.responsibilities:
                            st.markdown("*Key Responsibilities:*")
                            for resp in exp.responsibilities[:3]:
                                st.markdown(f"- {resp[:100]}...")
                
                # Education
                if profile.education:
                    st.markdown("**Education:**")
                    for edu in profile.education[:2]:
                        gpa_str = f" | GPA: {edu.gpa}" if edu.gpa else ""
                        year_str = f" ({edu.graduation_year})" if edu.graduation_year else ""
                        st.markdown(f"- **{edu.degree}** - {edu.field_of_study}{year_str}{gpa_str}")
                
                # Skills
                st.markdown("**Skills:**")
                
                skills_col1, skills_col2 = st.columns(2)
                
                with skills_col1:
                    if profile.skills['technical']:
                        st.markdown("*Technical:*")
                        st.markdown(", ".join(profile.skills['technical'][:10]))
                
                with skills_col2:
                    if profile.skills['soft']:
                        st.markdown("*Soft Skills:*")
                        st.markdown(", ".join(profile.skills['soft'][:8]))
            
            with tab2:
                st.markdown("### Key Strengths")
                
                if result.strengths:
                    for i, strength in enumerate(result.strengths, 1):
                        st.markdown(f"**{i}. {strength.category}** (Score: {strength.score:.0%})")
                        st.markdown(f"*{strength.reasoning}*")
                        
                        if strength.evidence:
                            with st.expander("📋 Evidence"):
                                for evidence in strength.evidence[:5]:
                                    st.markdown(f"- {evidence}")
                        
                        st.markdown("---")
                else:
                    st.info("No specific strengths identified")
                
                # Potential areas
                if result.potential_areas:
                    st.markdown("### ⚠️ Areas for Consideration")
                    for area in result.potential_areas:
                        st.warning(f"**{area.category}:** {area.reasoning}")
            
            with tab3:
                st.markdown("### Relevance Breakdown")
                
                # Breakdown chart
                if result.relevance_breakdown:
                    breakdown_df = pd.DataFrame([
                        {'Component': k.replace('_', ' ').title(), 'Score': v}
                        for k, v in result.relevance_breakdown.items()
                    ])
                    
                    fig_breakdown = px.bar(
                        breakdown_df,
                        x='Component',
                        y='Score',
                        title='Relevance Score Components',
                        color='Score',
                        color_continuous_scale='RdYlGn'
                    )
                    
                    fig_breakdown.update_layout(height=300)
                    st.plotly_chart(fig_breakdown, use_container_width=True)
                
                # Soft skills radar
                if result.soft_skills_assessment:
                    st.markdown("**Soft Skills Assessment:**")
                    
                    fig_radar = go.Figure()
                    
                    categories = list(result.soft_skills_assessment.keys())
                    values = list(result.soft_skills_assessment.values())
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values,
                        theta=[c.replace('_', ' ').title() for c in categories],
                        fill='toself',
                        name='Soft Skills'
                    ))
                    
                    fig_radar.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                        showlegend=False,
                        height=400
                    )
                    
                    st.plotly_chart(fig_radar, use_container_width=True)
            
            with tab4:
                st.markdown("### Professional Assessment")
                
                # Professional assessment text
                st.markdown(result.professional_assessment)
                
                # Fit analysis
                if result.fit_analysis:
                    st.markdown("---")
                    st.markdown("**🎯 Fit Analysis:**")
                    
                    fit = result.fit_analysis
                    
                    if 'seniority_match' in fit:
                        st.markdown(f"**Seniority Match:** {fit['seniority_match']}")
                    
                    if 'cultural_indicators' in fit and fit['cultural_indicators']:
                        st.markdown(f"**Cultural Fit Indicators:** {', '.join(fit['cultural_indicators'])}")
                    
                    if 'experience_depth' in fit:
                        exp_depth = fit['experience_depth']
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Responsibility Level", exp_depth.get('responsibility_level', 'N/A').title())
                        with col2:
                            st.metric("Technical Depth", exp_depth.get('technical_depth', 'N/A').title())
                        with col3:
                            st.metric("Impact Indicators", len(exp_depth.get('impact_indicators', [])))
                
                # Recommendation
                st.markdown("---")
                st.markdown("### 📝 Recommendation")
                st.markdown(result.overall_recommendation)
            
            with tab5:
                st.markdown("### Contact Information")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Name:** {profile.candidate_name}")
                    st.markdown(f"**Email:** {profile.contact_info.get('email', 'Not provided')}")
                    st.markdown(f"**Phone:** {profile.contact_info.get('phone', 'Not provided')}")
                
                with col2:
                    if profile.contact_info.get('linkedin'):
                        st.markdown(f"**LinkedIn:** {profile.contact_info['linkedin']}")
                    if profile.contact_info.get('github'):
                        st.markdown(f"**GitHub:** {profile.contact_info['github']}")
                
                # Certifications
                if profile.certifications:
                    st.markdown("**Certifications:**")
                    for cert in profile.certifications[:5]:
                        st.markdown(f"- {cert}")
                
                # Awards
                if profile.awards:
                    st.markdown("**Awards:**")
                    for award in profile.awards[:5]:
                        st.markdown(f"- {award}")
    
    # Download results
    st.markdown("---")
    st.subheader("📥 Download Results")
    
    # Create Excel export
    excel_buffer = create_excel_export(results, criteria)
    
    st.download_button(
        label="📥 Download Detailed Analysis (Excel)",
        data=excel_buffer,
        file_name="cv_analysis_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def create_excel_export(results: List[dict], criteria: str) -> BytesIO:
    """Create Excel file with comprehensive results"""
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = []
        for item in results:
            result = item['result']
            profile = result.cv_profile
            
            summary_data.append({
                'Filename': item['filename'],
                'Candidate Name': profile.candidate_name,
                'Email': profile.contact_info.get('email', ''),
                'Phone': profile.contact_info.get('phone', ''),
                'Relevance Score': result.relevance_score,
                'Confidence Score': result.confidence_score,
                'Experience (Years)': profile.total_experience_years,
                'Seniority Level': profile.seniority_level,
                'Recommendation': result.overall_recommendation[:200],
                'LinkedIn': profile.contact_info.get('linkedin', ''),
                'GitHub': profile.contact_info.get('github', '')
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Detailed analysis sheet
        detailed_data = []
        for item in results:
            result = item['result']
            profile = result.cv_profile
            
            detailed_data.append({
                'Candidate': profile.candidate_name,
                'Professional Assessment': result.professional_assessment,
                'Relevance Reasoning': result.relevance_reasoning,
                'Top Strength 1': result.strengths[0].reasoning if result.strengths else '',
                'Top Strength 2': result.strengths[1].reasoning if len(result.strengths) > 1 else '',
                'Top Strength 3': result.strengths[2].reasoning if len(result.strengths) > 2 else '',
                'Skills (Technical)': ', '.join(profile.skills['technical'][:20]),
                'Skills (Soft)': ', '.join(profile.skills['soft'][:15]),
                'Education': '; '.join([f"{edu.degree} - {edu.institution}" for edu in profile.education[:3]]),
                'Certifications': '; '.join(profile.certifications[:10])
            })
        
        detailed_df = pd.DataFrame(detailed_data)
        detailed_df.to_excel(writer, sheet_name='Detailed Analysis', index=False)
        
        # Add criteria sheet
        criteria_df = pd.DataFrame([{'Job Requirements': criteria}])
        criteria_df.to_excel(writer, sheet_name='Criteria', index=False)
    
    output.seek(0)
    return output
