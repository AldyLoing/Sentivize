"""
Ultra Advanced CV Analyzer
==========================
Sistem analisis CV dengan kecerdasan AI tingkat tinggi:
- Job Complexity Detection
- Flexible scoring untuk entry-level jobs
- Deep contextual reasoning
- Human-like understanding
- Fresh graduate friendly evaluation
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import warnings
warnings.filterwarnings('ignore')

from ai.advanced_ai_engine import get_ai_engine
from ai.job_complexity_detector import JobComplexityDetector, JobProfile, JobComplexity
from ai.cv_preview_extractor import CVPreviewExtractor, CVPreview

@dataclass
class UltraCVAnalysisResult:
    """Hasil analisis CV yang komprehensif dan human-friendly"""
    
    # Basic Info
    candidate_name: str = ""
    preview: Optional[CVPreview] = None
    
    # Job Context
    job_profile: Optional[JobProfile] = None
    job_title: str = ""
    job_description: str = ""
    
    # Scoring (0-100)
    overall_score: float = 0.0
    relevance_score: float = 0.0
    soft_skill_score: float = 0.0
    hard_skill_score: float = 0.0
    experience_score: float = 0.0
    cv_clarity_score: float = 0.0
    potential_score: float = 0.0
    
    # Assessment
    candidate_tier: str = "MEDIUM"  # EXCELLENT / STRONG / MEDIUM / LOW
    is_suitable: bool = True
    confidence_level: float = 0.0
    
    # Human Reasoning
    executive_summary: str = ""
    detailed_reasoning: str = ""
    key_strengths: List[str] = field(default_factory=list)
    key_weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    # Insights
    leadership_patterns: List[str] = field(default_factory=list)
    problem_solving_evidence: List[str] = field(default_factory=list)
    initiative_examples: List[str] = field(default_factory=list)
    implicit_skills: List[str] = field(default_factory=list)  # Skills tidak ditulis eksplisit
    
    # Career Development
    career_progression: str = ""
    growth_potential: str = ""
    
    # Match Details
    matching_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    transferable_experience: List[str] = field(default_factory=list)
    
    # Recommendations
    position_recommendations: List[Dict[str, str]] = field(default_factory=list)
    interview_focus_areas: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for export"""
        return {
            'candidate_name': self.candidate_name,
            'job_title': self.job_title,
            'overall_score': round(self.overall_score, 2),
            'relevance_score': round(self.relevance_score, 2),
            'soft_skill_score': round(self.soft_skill_score, 2),
            'hard_skill_score': round(self.hard_skill_score, 2),
            'experience_score': round(self.experience_score, 2),
            'cv_clarity_score': round(self.cv_clarity_score, 2),
            'potential_score': round(self.potential_score, 2),
            'candidate_tier': self.candidate_tier,
            'is_suitable': 'COCOK' if self.is_suitable else 'KURANG COCOK',
            'executive_summary': self.executive_summary,
            'key_strengths': ', '.join(self.key_strengths[:5]),
            'key_weaknesses': ', '.join(self.key_weaknesses[:3]),
            'recommendations': ', '.join(self.recommendations[:3])
        }

class UltraCVAnalyzer:
    """
    Analyzer super canggih dengan pemahaman kontekstual seperti HR profesional
    """
    
    def __init__(self):
        self.ai_engine = get_ai_engine()
        self.job_detector = JobComplexityDetector(self.ai_engine)
        self.preview_extractor = CVPreviewExtractor()
        
    def analyze_cv(
        self,
        cv_file_path: str,
        job_title: str,
        job_description: str,
        file_type: str = 'pdf'
    ) -> UltraCVAnalysisResult:
        """
        Analisis CV dengan pemahaman mendalam
        
        Args:
            cv_file_path: Path ke file CV
            job_title: Judul posisi yang dicari
            job_description: Deskripsi pekerjaan lengkap
            file_type: Tipe file (pdf/docx/txt)
            
        Returns:
            UltraCVAnalysisResult dengan analisis komprehensif
        """
        result = UltraCVAnalysisResult()
        result.job_title = job_title
        result.job_description = job_description
        
        # Step 1: Extract CV Preview
        print("📄 Mengekstrak data CV...")
        preview = self.preview_extractor.extract_from_file(cv_file_path, file_type)
        result.preview = preview
        result.candidate_name = preview.full_name or "Kandidat"
        
        # Step 2: Detect Job Complexity
        print("🔍 Menganalisis kompleksitas pekerjaan...")
        job_profile = self.job_detector.detect_complexity(job_title, job_description)
        result.job_profile = job_profile
        
        # Step 3: Score CV berdasarkan Job Complexity
        print("📊 Menghitung skor dengan konteks pekerjaan...")
        self._calculate_flexible_scores(result, preview, job_profile, job_description)
        
        # Step 4: Generate Deep Reasoning
        print("🧠 Menghasilkan reasoning kontekstual...")
        self._generate_human_reasoning(result, preview, job_profile)
        
        # Step 5: Extract Implicit Skills & Patterns
        print("🔎 Mengidentifikasi skill implisit dan pola...")
        self._extract_implicit_skills(result, preview)
        self._identify_patterns(result, preview)
        
        # Step 6: Generate Recommendations
        print("💡 Membuat rekomendasi...")
        self._generate_recommendations(result, preview, job_profile)
        
        # Step 7: Determine Suitability
        self._determine_suitability(result, job_profile)
        
        print(f"✅ Analisis selesai: {result.candidate_name} - Score: {result.overall_score:.1f}/100")
        
        return result
    
    def _calculate_flexible_scores(
        self,
        result: UltraCVAnalysisResult,
        preview: CVPreview,
        job_profile: JobProfile,
        job_desc: str
    ):
        """
        Calculate scores dengan fleksibilitas berdasarkan job complexity
        """
        weights = self.job_detector.get_scoring_weights(job_profile.complexity)
        
        # 1. Soft Skills Score (penting untuk low complexity)
        result.soft_skill_score = self._score_soft_skills(preview, job_profile)
        
        # 2. Hard Skills Score
        result.hard_skill_score = self._score_hard_skills(preview, job_desc, job_profile)
        
        # 3. Experience Score (fleksibel untuk low complexity)
        result.experience_score = self._score_experience(preview, job_profile)
        
        # 4. CV Clarity Score
        result.cv_clarity_score = self._score_cv_clarity(preview)
        
        # 5. Potential Score (tinggi untuk fresh grad di low complexity)
        result.potential_score = self._score_potential(preview, job_profile)
        
        # 6. Relevance Score (semantic matching dengan AI)
        result.relevance_score = self._score_semantic_relevance(preview, job_desc)
        
        # Calculate weighted overall score
        result.overall_score = (
            weights['soft_skills'] * result.soft_skill_score +
            weights['hard_skills'] * result.hard_skill_score +
            weights['experience_relevance'] * result.experience_score +
            weights['cv_clarity'] * result.cv_clarity_score +
            weights['attitude_potential'] * result.potential_score +
            weights['organizational_experience'] * min(len(preview.organizational_experiences) * 10, 100)
        )
        
        result.overall_score = min(result.overall_score, 100)
        
    def _score_soft_skills(self, preview: CVPreview, job_profile: JobProfile) -> float:
        """Score soft skills dengan boost untuk entry-level"""
        base_score = min(len(preview.soft_skills) * 8, 100)
        
        # Boost untuk organizational experience
        if len(preview.organizational_experiences) > 0:
            base_score = min(base_score + 15, 100)
        
        # Extra boost untuk low complexity jobs
        if job_profile.complexity == JobComplexity.LOW:
            base_score = min(base_score * 1.2, 100)
        
        return base_score
    
    def _score_hard_skills(self, preview: CVPreview, job_desc: str, job_profile: JobProfile) -> float:
        """Score hard skills dengan semantic matching"""
        if not preview.hard_skills and not preview.programming_languages:
            # Untuk low complexity, tidak masalah jika tidak ada hard skill teknis
            if job_profile.complexity == JobComplexity.LOW:
                return 70.0  # Base score wajar
            else:
                return 30.0
        
        # Count relevant skills
        all_skills = preview.hard_skills + preview.programming_languages + preview.tools
        skill_count = len(all_skills)
        
        # Semantic similarity dengan job description
        if all_skills:
            skills_text = ', '.join(all_skills)
            try:
                similarity = self.ai_engine.compute_semantic_similarity(skills_text, job_desc)
                semantic_score = float(similarity) * 100
            except:
                semantic_score = 50.0
        else:
            semantic_score = 40.0
        
        # Combine
        count_score = min(float(skill_count) * 5, 70)
        final_score = (float(count_score) * 0.4) + (float(semantic_score) * 0.6)
        
        return min(final_score, 100)
    
    def _score_experience(self, preview: CVPreview, job_profile: JobProfile) -> float:
        """Score experience dengan fleksibilitas untuk entry-level"""
        months = preview.total_work_experience_months
        
        # Untuk low complexity jobs
        if job_profile.complexity == JobComplexity.LOW:
            # Fresh grad tidak masalah
            if months == 0:
                # Cek organizational experience sebagai pengganti
                if len(preview.organizational_experiences) > 0:
                    return 75.0  # Bagus untuk entry level
                else:
                    return 65.0  # Masih acceptable
            elif months < 12:
                return 85.0
            else:
                return 90.0
        
        # Untuk mid/high complexity
        else:
            if months == 0:
                return 20.0
            elif months < 12:
                return 40.0
            elif months < 36:
                return 65.0
            elif months < 60:
                return 85.0
            else:
                return 95.0
    
    def _score_cv_clarity(self, preview: CVPreview) -> float:
        """Score struktur dan kejelasan CV"""
        score = 50.0  # Base
        
        # Ada kontak lengkap
        if preview.email:
            score += 10
        if preview.phone:
            score += 10
        
        # Ada section education
        if preview.education_summary:
            score += 10
        
        # Ada skills
        if preview.hard_skills or preview.soft_skills:
            score += 10
        
        # Ada professional links
        if preview.linkedin or preview.github:
            score += 10
        
        return min(score, 100)
    
    def _score_potential(self, preview: CVPreview, job_profile: JobProfile) -> float:
        """Score potensi kandidat (penting untuk fresh grad)"""
        score = 50.0
        
        # Projects show initiative
        if len(preview.projects) > 0:
            score += 20
        
        # Organizational experience shows soft skills
        if len(preview.organizational_experiences) > 0:
            score += 20
        
        # Multiple skills show learning ability
        if len(preview.hard_skills) + len(preview.soft_skills) > 8:
            score += 15
        
        # CV clarity shows attention to detail
        if preview.email and preview.phone and preview.education_summary:
            score += 10
        
        # Boost untuk fresh grad di low complexity
        if job_profile.complexity == JobComplexity.LOW and preview.candidate_level == "Fresh Graduate":
            score = min(score * 1.15, 100)
        
        return min(score, 100)
    
    def _score_semantic_relevance(self, preview: CVPreview, job_desc: str) -> float:
        """Score relevansi menggunakan semantic similarity AI"""
        if not job_desc or len(job_desc.strip()) < 20:
            return 50.0
        
        # Combine semua info kandidat
        candidate_text = f"""
        Skills: {', '.join(preview.hard_skills + preview.soft_skills)}
        Experience: {' | '.join([exp.get('title', '') + ' at ' + exp.get('company', '') for exp in preview.work_experiences])}
        Education: {' | '.join(preview.education_summary)}
        Projects: {' | '.join([proj.get('title', '') for proj in preview.projects])}
        """
        
        try:
            similarity = self.ai_engine.compute_semantic_similarity(candidate_text, job_desc)
            return similarity * 100
        except Exception as e:
            print(f"⚠️ Semantic similarity gagal: {e}")
            return 50.0
    
    def _generate_human_reasoning(
        self,
        result: UltraCVAnalysisResult,
        preview: CVPreview,
        job_profile: JobProfile
    ):
        """Generate reasoning seperti HR profesional"""
        
        # Executive Summary
        if job_profile.complexity == JobComplexity.LOW:
            if preview.candidate_level == "Fresh Graduate":
                result.executive_summary = (
                    f"Untuk posisi {result.job_title} yang termasuk kategori entry-level, "
                    f"{result.candidate_name} menunjukkan profil yang layak dipertimbangkan. "
                    f"Meskipun belum memiliki pengalaman kerja langsung, CV menunjukkan "
                    f"struktur yang baik, kemampuan dokumentasi, dan indikator soft skill yang positif."
                )
            else:
                result.executive_summary = (
                    f"{result.candidate_name} memiliki profil yang cocok untuk posisi {result.job_title}. "
                    f"Dengan pengalaman {preview.total_work_experience_months // 12} tahun dan skill yang relevan, "
                    f"kandidat menunjukkan kesiapan untuk peran ini."
                )
        else:
            if preview.candidate_level == "Fresh Graduate":
                result.executive_summary = (
                    f"Posisi {result.job_title} membutuhkan keahlian spesifik. "
                    f"{result.candidate_name} adalah fresh graduate dengan "
                    f"{len(preview.projects)} project dan {len(preview.hard_skills)} skill teknis. "
                    f"Perlu evaluasi mendalam pada technical skills dan project relevance."
                )
            else:
                result.executive_summary = (
                    f"{result.candidate_name} memiliki {preview.total_work_experience_months // 12} tahun pengalaman "
                    f"dengan keahlian di {', '.join(preview.hard_skills[:3]) if preview.hard_skills else 'berbagai area'}. "
                    f"Profil menunjukkan kesesuaian yang baik untuk posisi {result.job_title}."
                )
        
        # Detailed Reasoning
        reasoning_parts = []
        
        # Experience reasoning
        if preview.total_work_experience_months > 0:
            years = preview.total_work_experience_months // 12
            reasoning_parts.append(
                f"**Pengalaman Kerja**: Kandidat memiliki {years} tahun pengalaman profesional. "
            )
            if preview.work_experiences:
                latest_job = preview.work_experiences[0]
                reasoning_parts.append(
                    f"Posisi terakhir sebagai {latest_job.get('title', 'N/A')} menunjukkan relevansi dengan kebutuhan posisi."
                )
        else:
            if job_profile.complexity == JobComplexity.LOW:
                reasoning_parts.append(
                    f"**Pengalaman Kerja**: Meskipun belum memiliki pengalaman kerja formal, "
                    f"untuk posisi entry-level seperti {result.job_title}, yang lebih penting adalah "
                    f"attitude, kemampuan belajar, dan organizational skills."
                )
            else:
                reasoning_parts.append(
                    f"**Pengalaman Kerja**: Kandidat belum memiliki pengalaman kerja profesional. "
                    f"Ini menjadi pertimbangan mengingat posisi {result.job_title} umumnya membutuhkan pengalaman relevan."
                )
        
        # Skills reasoning
        if preview.hard_skills or preview.programming_languages:
            skills_list = preview.hard_skills + preview.programming_languages
            reasoning_parts.append(
                f"**Keahlian Teknis**: Kandidat menguasai {len(skills_list)} skill teknis termasuk "
                f"{', '.join(skills_list[:3])}. Ini menunjukkan fondasi teknis yang baik."
            )
        
        if preview.soft_skills:
            reasoning_parts.append(
                f"**Soft Skills**: CV menunjukkan {len(preview.soft_skills)} soft skill penting seperti "
                f"{', '.join(preview.soft_skills[:3])}, yang krusial untuk kolaborasi dan adaptasi."
            )
        
        # Organizational experience
        if preview.organizational_experiences:
            reasoning_parts.append(
                f"**Pengalaman Organisasi**: Kandidat aktif dalam {len(preview.organizational_experiences)} organisasi/volunteer. "
                f"Ini menunjukkan leadership potential, teamwork, dan social responsibility."
            )
        
        # Projects
        if preview.projects:
            reasoning_parts.append(
                f"**Project Experience**: Memiliki {len(preview.projects)} project yang menunjukkan "
                f"inisiatif, problem-solving ability, dan hands-on experience."
            )
        
        result.detailed_reasoning = "\n\n".join(reasoning_parts)
        
    def _extract_implicit_skills(self, result: UltraCVAnalysisResult, preview: CVPreview):
        """Identifikasi skill yang tidak ditulis eksplisit tapi tersirat dari pengalaman"""
        implicit_skills = []
        
        # Dari work experience
        for exp in preview.work_experiences:
            title = exp.get('title', '').lower()
            
            if any(word in title for word in ['lead', 'manager', 'head', 'supervisor']):
                implicit_skills.append("Leadership & People Management")
            
            if any(word in title for word in ['senior', 'principal', 'expert']):
                implicit_skills.append("Deep Domain Expertise")
            
            if any(word in title for word in ['coordinator', 'organizer']):
                implicit_skills.append("Project Coordination")
        
        # Dari projects
        if len(preview.projects) > 2:
            implicit_skills.append("Self-Initiative & Continuous Learning")
        
        # Dari organizational experience
        if len(preview.organizational_experiences) > 1:
            implicit_skills.append("Community Engagement & Social Skills")
        
        # Dari programming languages
        if len(preview.programming_languages) > 3:
            implicit_skills.append("Multi-Technology Adaptability")
        
        result.implicit_skills = list(set(implicit_skills))
    
    def _identify_patterns(self, result: UltraCVAnalysisResult, preview: CVPreview):
        """Identifikasi pola leadership, problem-solving, initiative"""
        
        # Leadership patterns
        for exp in preview.work_experiences:
            title = exp.get('title', '').lower()
            if any(word in title for word in ['lead', 'manager', 'head', 'coordinator', 'chief']):
                result.leadership_patterns.append(
                    f"Posisi {exp.get('title')} menunjukkan tanggung jawab kepemimpinan"
                )
        
        for org in preview.organizational_experiences:
            org_text = org.get('organization', '').lower()
            if any(word in org_text for word in ['ketua', 'leader', 'president', 'chairman']):
                result.leadership_patterns.append(
                    f"Pengalaman kepemimpinan di {org.get('organization')}"
                )
        
        # Problem-solving evidence
        if len(preview.projects) > 0:
            result.problem_solving_evidence.append(
                f"{len(preview.projects)} project menunjukkan kemampuan problem-solving praktis"
            )
        
        # Initiative examples
        if len(preview.programming_languages) > 0 or len(preview.tools) > 0:
            result.initiative_examples.append(
                "Menguasai multiple teknologi menunjukkan inisiatif belajar mandiri"
            )
        
        if preview.github:
            result.initiative_examples.append(
                "Memiliki GitHub profile menunjukkan kontribusi ke open source atau portfolio digital"
            )
    
    def _generate_recommendations(
        self,
        result: UltraCVAnalysisResult,
        preview: CVPreview,
        job_profile: JobProfile
    ):
        """Generate rekomendasi aksi"""
        
        # Key Strengths
        result.key_strengths = preview.strengths.copy()
        
        if not result.key_strengths:
            if len(preview.hard_skills) > 3:
                result.key_strengths.append("Memiliki diverse technical skills")
            if len(preview.soft_skills) > 3:
                result.key_strengths.append("Soft skills yang lengkap")
            if preview.total_work_experience_months > 24:
                result.key_strengths.append("Pengalaman kerja yang substansial")
        
        # Key Weaknesses (constructive)
        if preview.total_work_experience_months == 0:
            if job_profile.complexity != JobComplexity.LOW:
                result.key_weaknesses.append("Belum memiliki pengalaman kerja profesional")
        
        if not preview.programming_languages and job_profile.complexity == JobComplexity.HIGH:
            result.key_weaknesses.append("Kurang menunjukkan technical skills spesifik")
        
        if not preview.projects and preview.candidate_level == "Fresh Graduate":
            result.key_weaknesses.append("Portofolio project bisa diperkuat")
        
        # Recommendations
        if result.overall_score >= 75:
            result.recommendations.append("RECOMMEND untuk interview")
            result.recommendations.append("Kandidat menunjukkan kesesuaian yang baik")
        elif result.overall_score >= 60:
            result.recommendations.append("CONSIDER untuk interview dengan evaluasi tambahan")
            result.recommendations.append("Kandidat potensial dengan beberapa gap yang bisa di-address")
        else:
            result.recommendations.append("Kandidat belum sesuai dengan kebutuhan posisi saat ini")
            result.recommendations.append("Pertimbangkan untuk posisi lain yang lebih sesuai")
        
        # Interview focus areas
        if job_profile.complexity == JobComplexity.LOW:
            result.interview_focus_areas = [
                "Attitude dan kemampuan belajar",
                "Communication skills",
                "Situational questions untuk soft skills"
            ]
        else:
            result.interview_focus_areas = [
                "Technical deep dive",
                "Problem-solving scenarios",
                "Past project discussions"
            ]
        
        # Position recommendations
        if result.overall_score >= 70:
            result.position_recommendations.append({
                'position': result.job_title,
                'fit': 'STRONG FIT',
                'reason': 'Profil sesuai dengan kebutuhan posisi'
            })
        
        # Alternative positions berdasarkan skills
        if preview.programming_languages and 'python' in [lang.lower() for lang in preview.programming_languages]:
            result.position_recommendations.append({
                'position': 'Python Developer / Data Analyst',
                'fit': 'POTENTIAL FIT',
                'reason': 'Memiliki Python skills'
            })
    
    def _determine_suitability(self, result: UltraCVAnalysisResult, job_profile: JobProfile):
        """Tentukan apakah kandidat cocok"""
        
        # Tier determination
        if result.overall_score >= 85:
            result.candidate_tier = "EXCELLENT"
            result.is_suitable = True
            result.confidence_level = 0.95
        elif result.overall_score >= 70:
            result.candidate_tier = "STRONG"
            result.is_suitable = True
            result.confidence_level = 0.85
        elif result.overall_score >= 55:
            result.candidate_tier = "MEDIUM"
            result.is_suitable = True
            result.confidence_level = 0.70
        else:
            result.candidate_tier = "LOW"
            result.is_suitable = False
            result.confidence_level = 0.50
        
        # Special case: Fresh grad untuk low complexity
        if (job_profile.complexity == JobComplexity.LOW and 
            result.preview and 
            result.preview.candidate_level == "Fresh Graduate"):
            # Be more lenient
            if result.overall_score >= 60:
                result.is_suitable = True
                result.candidate_tier = "STRONG" if result.overall_score >= 70 else "MEDIUM"
                result.confidence_level = min(result.confidence_level + 0.1, 0.95)
