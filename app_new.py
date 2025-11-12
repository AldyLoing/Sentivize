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
