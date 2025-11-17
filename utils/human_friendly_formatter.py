"""
Human-Friendly Output Formatters
=================================
Format output AI agar mudah dipahami orang awam seperti konsultasi HR
"""

from typing import Dict, List, Any
import streamlit as st


class HumanFriendlyFormatter:
    """Format output menjadi human-readable"""
    
    @staticmethod
    def format_score(score: float) -> str:
        """Format score menjadi kategori verbal"""
        if score >= 90:
            return "🌟 Sangat Baik (Excellent)"
        elif score >= 80:
            return "⭐ Baik Sekali (Very Good)"
        elif score >= 70:
            return "✅ Baik (Good)"
        elif score >= 60:
            return "👍 Cukup Baik (Fair)"
        elif score >= 50:
            return "⚠️ Cukup (Adequate)"
        else:
            return "❌ Kurang (Needs Improvement)"
    
    @staticmethod
    def format_percentage(value: float) -> str:
        """Format percentage dengan visual"""
        percentage = int(value)
        filled = int(percentage / 10)
        empty = 10 - filled
        bar = "█" * filled + "░" * empty
        return f"{bar} {percentage}%"
    
    @staticmethod
    def format_tier(tier: str) -> str:
        """Format tier dengan emoji"""
        tier_map = {
            'EXCELLENT': '🏆 EXCELLENT - Kandidat Terbaik',
            'STRONG': '⭐ STRONG - Kandidat Kuat',
            'MEDIUM': '👤 MEDIUM - Kandidat Potensial',
            'LOW': '⚠️ LOW - Perlu Evaluasi Lebih Lanjut'
        }
        return tier_map.get(tier, tier)
    
    @staticmethod
    def format_complexity(complexity: str) -> str:
        """Format job complexity"""
        complexity_map = {
            'low': '🟢 Entry-Level (Mudah Dipelajari)',
            'mid': '🟡 Mid-Level (Butuh Pengalaman)',
            'high': '🔴 Senior-Level (Butuh Expertise)'
        }
        return complexity_map.get(complexity.lower(), complexity)
    
    @staticmethod
    def format_recommendation(recommendation: str) -> str:
        """Format recommendation dengan emoji"""
        rec_map = {
            'STRONGLY RECOMMEND': '✅ SANGAT DIREKOMENDASIKAN - Segera lanjut ke interview',
            'RECOMMEND': '👍 DIREKOMENDASIKAN - Kandidat layak untuk interview',
            'CONSIDER': '🤔 PERTIMBANGKAN - Perlu evaluasi tambahan',
            'NOT SUITABLE': '❌ TIDAK COCOK - Pertimbangkan posisi lain'
        }
        return rec_map.get(recommendation, recommendation)
    
    @staticmethod
    def format_cv_analysis_card(result: Any) -> None:
        """Display CV analysis result dalam format card"""
        st.markdown("### 📊 Ringkasan Analisis")
        
        # Summary Box
        st.info(result.executive_summary)
        
        # Score Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Overall Score",
                value=f"{result.overall_score:.1f}/100",
                delta=f"{HumanFriendlyFormatter.format_score(result.overall_score)}"
            )
        
        with col2:
            st.metric(
                label="Candidate Tier",
                value=result.candidate_tier,
                delta="✅ Suitable" if result.is_suitable else "⚠️ Review Needed"
            )
        
        with col3:
            st.metric(
                label="Confidence",
                value=f"{result.confidence_level * 100:.0f}%",
                delta=f"{'High' if result.confidence_level > 0.8 else 'Medium' if result.confidence_level > 0.6 else 'Low'}"
            )
        
        # Detailed Scores
        st.markdown("### 📈 Detail Skor")
        
        scores = {
            'Relevansi': result.relevance_score,
            'Soft Skills': result.soft_skill_score,
            'Hard Skills': result.hard_skill_score,
            'Pengalaman': result.experience_score,
            'Kejelasan CV': result.cv_clarity_score,
            'Potensi': result.potential_score
        }
        
        for label, score in scores.items():
            st.markdown(f"**{label}**: {HumanFriendlyFormatter.format_percentage(score)}")
            st.progress(score / 100)
        
        # Strengths & Weaknesses
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Kelebihan")
            if result.key_strengths:
                for strength in result.key_strengths:
                    st.markdown(f"- {strength}")
            else:
                st.markdown("*Tidak ada kelebihan khusus tercatat*")
        
        with col2:
            st.markdown("### ⚠️ Area Pengembangan")
            if result.key_weaknesses:
                for weakness in result.key_weaknesses:
                    st.markdown(f"- {weakness}")
            else:
                st.markdown("*Tidak ada concern mayor*")
        
        # Reasoning
        st.markdown("### 🧠 Analisis Mendalam")
        st.markdown(result.detailed_reasoning)
        
        # Recommendations
        st.markdown("### 💡 Rekomendasi")
        if result.recommendations:
            for rec in result.recommendations:
                if "RECOMMEND" in rec.upper():
                    st.success(rec)
                elif "CONSIDER" in rec.upper():
                    st.warning(rec)
                else:
                    st.info(rec)
    
    @staticmethod
    def format_employee_analysis_card(result: Any) -> None:
        """Display employee analysis result dalam format card"""
        st.markdown("### 📊 Ringkasan Analisis Karyawan")
        
        # Summary Box
        st.info(result.executive_summary)
        
        # Score Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Overall Score",
                value=f"{result.overall_score:.1f}/100"
            )
        
        with col2:
            st.metric(
                label="Tier",
                value=result.tier
            )
        
        with col3:
            st.metric(
                label="Recommendation",
                value=result.recommendation.split()[0]
            )
        
        with col4:
            st.metric(
                label="Confidence",
                value=f"{result.confidence * 100:.0f}%"
            )
        
        # Detailed Scores
        st.markdown("### 📈 Detail Skor")
        
        scores = {
            'Soft Skills': result.soft_skills_score,
            'Hard Skills': result.hard_skills_score,
            'Experience': result.experience_relevance_score,
            'Character': result.character_score,
            'Attitude': result.attitude_score,
            'Cultural Fit': result.cultural_fit_score
        }
        
        for label, score in scores.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(score / 100)
            with col2:
                st.markdown(f"**{score:.0f}%**")
            st.caption(label)
        
        # Position Fit
        st.markdown("### 🎯 Kesesuaian Posisi")
        if "cocok" in result.position_fit_explanation.lower():
            st.success(result.position_fit_explanation)
        elif "layak" in result.position_fit_explanation.lower():
            st.info(result.position_fit_explanation)
        else:
            st.warning(result.position_fit_explanation)
        
        # Strengths & Concerns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Kelebihan Utama")
            if result.key_strengths:
                for strength in result.key_strengths:
                    st.markdown(f"- ✓ {strength}")
            else:
                st.markdown("*Evaluasi lebih lanjut diperlukan*")
        
        with col2:
            st.markdown("### ⚠️ Perhatian")
            if result.key_concerns:
                for concern in result.key_concerns:
                    st.markdown(f"- ⚠️ {concern}")
            else:
                st.markdown("*Tidak ada concern mayor*")
        
        # Detailed Reasoning
        st.markdown("### 🧠 Analisis Mendalam")
        st.markdown(result.detailed_reasoning)
        
        # Recommendations
        if result.alternative_positions:
            st.markdown("### 🔄 Posisi Alternatif")
            for pos in result.alternative_positions:
                st.markdown(f"- {pos}")
        
        if result.onboarding_focus:
            st.markdown("### 📚 Fokus Onboarding")
            for focus in result.onboarding_focus:
                st.markdown(f"- {focus}")
    
    @staticmethod
    def format_preview_card(preview: Any) -> None:
        """Display CV preview sebelum analisis"""
        st.markdown("## 👁️ Preview Data CV")
        st.markdown("*Data yang berhasil diekstraksi dari CV*")
        st.markdown("---")
        
        # Basic Info
        st.markdown("### 📇 Informasi Kontak")
        
        info_data = {
            'Nama': preview.full_name or "Tidak terdeteksi",
            'Email': preview.email or "Tidak terdeteksi",
            'Telepon': preview.phone or "Tidak terdeteksi",
            'LinkedIn': preview.linkedin or "Tidak tersedia",
            'GitHub': preview.github or "Tidak tersedia"
        }
        
        col1, col2 = st.columns(2)
        items = list(info_data.items())
        
        for i, (key, value) in enumerate(items):
            if i % 2 == 0:
                with col1:
                    st.markdown(f"**{key}**: {value}")
            else:
                with col2:
                    st.markdown(f"**{key}**: {value}")
        
        st.markdown("---")
        
        # Education
        st.markdown("### 🎓 Pendidikan")
        if preview.education_summary:
            for edu in preview.education_summary:
                st.markdown(f"- {edu}")
        else:
            st.markdown("*Informasi pendidikan tidak terdeteksi*")
        
        st.markdown("---")
        
        # Skills
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💼 Hard Skills")
            if preview.hard_skills:
                for skill in preview.hard_skills[:10]:  # Limit 10
                    st.markdown(f"- {skill}")
                if len(preview.hard_skills) > 10:
                    st.caption(f"... dan {len(preview.hard_skills) - 10} lainnya")
            else:
                st.markdown("*Tidak terdeteksi*")
        
        with col2:
            st.markdown("### 🤝 Soft Skills")
            if preview.soft_skills:
                for skill in preview.soft_skills[:10]:
                    st.markdown(f"- {skill}")
                if len(preview.soft_skills) > 10:
                    st.caption(f"... dan {len(preview.soft_skills) - 10} lainnya")
            else:
                st.markdown("*Tidak terdeteksi*")
        
        st.markdown("---")
        
        # Programming & Tools
        if preview.programming_languages or preview.tools:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 💻 Bahasa Pemrograman")
                if preview.programming_languages:
                    st.markdown(", ".join(preview.programming_languages))
                else:
                    st.markdown("*Tidak terdeteksi*")
            
            with col2:
                st.markdown("### 🛠️ Tools & Technologies")
                if preview.tools:
                    st.markdown(", ".join(preview.tools))
                else:
                    st.markdown("*Tidak terdeteksi*")
            
            st.markdown("---")
        
        # Experience
        st.markdown("### 💼 Pengalaman Kerja")
        if preview.work_experiences:
            for exp in preview.work_experiences:
                title = exp.get('title', 'N/A')
                company = exp.get('company', 'N/A')
                duration = exp.get('duration', '')
                st.markdown(f"- **{title}** at {company} {f'({duration})' if duration else ''}")
        else:
            st.markdown("*Belum ada pengalaman kerja formal*")
        
        # Organizational Experience
        if preview.organizational_experiences:
            st.markdown("### 🏛️ Pengalaman Organisasi")
            for org in preview.organizational_experiences:
                org_name = org.get('organization', 'N/A')
                st.markdown(f"- {org_name}")
        
        # Projects
        if preview.projects:
            st.markdown("### 🚀 Project")
            for proj in preview.projects:
                title = proj.get('title', 'N/A')
                desc = proj.get('description', '')
                st.markdown(f"- **{title}**")
                if desc:
                    st.caption(desc)
        
        st.markdown("---")
        
        # Analysis Summary
        st.markdown("### 📊 Ringkasan Awal")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Level Kandidat",
                value=preview.candidate_level
            )
        
        with col2:
            st.metric(
                label="Total Pengalaman",
                value=f"{preview.total_work_experience_months} bulan"
            )
        
        with col3:
            st.metric(
                label="Cocok untuk Job",
                value=preview.estimated_job_complexity
            )
        
        # Initial Conclusion
        st.markdown("### 💬 Kesimpulan Awal")
        st.info(preview.initial_conclusion)
        
        # Strengths
        if preview.strengths:
            st.markdown("### ⭐ Highlight")
            for strength in preview.strengths:
                st.success(f"✓ {strength}")
