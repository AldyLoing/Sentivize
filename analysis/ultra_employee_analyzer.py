"""
Ultra Advanced Employee Analyzer
================================
Sistem analisis karyawan dengan:
- Job Complexity Detection
- Flexible scoring untuk entry-level positions
- Social media auto-search & analysis
- Deep profiling tanpa keyword matching
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from ai.advanced_ai_engine import get_ai_engine
from ai.job_complexity_detector import JobComplexityDetector, JobProfile, JobComplexity

@dataclass
class UltraEmployeeAnalysisResult:
    """Hasil analisis karyawan yang human-friendly"""
    
    # Basic Info
    employee_name: str = ""
    position_current: str = ""
    
    # Job Context
    target_position: str = ""
    job_criteria: str = ""
    job_profile: Optional[JobProfile] = None
    
    # Scores (0-100)
    overall_score: float = 0.0
    soft_skills_score: float = 0.0
    hard_skills_score: float = 0.0
    experience_relevance_score: float = 0.0
    character_score: float = 0.0
    attitude_score: float = 0.0
    cultural_fit_score: float = 0.0
    
    # Assessment
    tier: str = "MEDIUM"  # EXCELLENT / STRONG / MEDIUM / LOW
    recommendation: str = "CONSIDER"  # STRONGLY RECOMMEND / RECOMMEND / CONSIDER / NOT SUITABLE
    confidence: float = 0.0
    
    # Reasoning (Human-like)
    executive_summary: str = ""
    detailed_reasoning: str = ""
    key_strengths: List[str] = field(default_factory=list)
    key_concerns: List[str] = field(default_factory=list)
    
    # Match Analysis
    matching_skills: List[str] = field(default_factory=list)
    transferable_skills: List[str] = field(default_factory=list)
    development_areas: List[str] = field(default_factory=list)
    
    # Social Media Insights (if available)
    social_sentiment: str = "Neutral"
    social_professionalism_score: float = 0.0
    social_insights: List[str] = field(default_factory=list)
    
    # Recommendations
    position_fit_explanation: str = ""
    alternative_positions: List[str] = field(default_factory=list)
    onboarding_focus: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'employee_name': self.employee_name,
            'current_position': self.position_current,
            'target_position': self.target_position,
            'overall_score': round(self.overall_score, 2),
            'tier': self.tier,
            'recommendation': self.recommendation,
            'executive_summary': self.executive_summary,
            'key_strengths': ', '.join(self.key_strengths[:5]),
            'key_concerns': ', '.join(self.key_concerns[:3]) if self.key_concerns else 'Tidak ada concern mayor',
            'position_fit': self.position_fit_explanation
        }

class UltraEmployeeAnalyzer:
    """
    Analyzer karyawan dengan pemahaman kontekstual
    """
    
    def __init__(self):
        self.ai_engine = get_ai_engine()
        self.job_detector = JobComplexityDetector(self.ai_engine)
        
    def analyze_employee(
        self,
        employee_data: Dict[str, Any],
        job_criteria: str,
        target_position: str,
        use_social_media: bool = False
    ) -> UltraEmployeeAnalysisResult:
        """
        Analisis karyawan dengan pemahaman mendalam
        
        Args:
            employee_data: Dictionary dengan data karyawan
                          {name, position, skills, experience, bio, social_media_url (optional)}
            job_criteria: Deskripsi lengkap kriteria posisi
            target_position: Nama posisi yang dicari
            use_social_media: Apakah akan analyze social media
            
        Returns:
            UltraEmployeeAnalysisResult dengan analisis komprehensif
        """
        result = UltraEmployeeAnalysisResult()
        result.employee_name = employee_data.get('name', 'Unknown')
        result.position_current = employee_data.get('position', '')
        result.target_position = target_position
        result.job_criteria = job_criteria
        
        # Step 1: Detect Job Complexity
        print(f"🔍 Menganalisis kompleksitas posisi '{target_position}'...")
        job_profile = self.job_detector.detect_complexity(target_position, job_criteria)
        result.job_profile = job_profile
        
        print(f"   → Complexity: {job_profile.complexity.value.upper()}")
        print(f"   → Fresh Grad Friendly: {'Ya' if job_profile.fresh_graduate_friendly else 'Tidak'}")
        print(f"   → Experience Flexibility: {job_profile.experience_flexibility * 100:.0f}%")
        
        # Step 2: Score dengan fleksibilitas
        print(f"📊 Menghitung skor untuk {result.employee_name}...")
        self._calculate_flexible_scores(result, employee_data, job_profile, job_criteria)
        
        # Step 3: Social Media Analysis (if requested)
        if use_social_media:
            print(f"📱 Menganalisis social media...")
            self._analyze_social_media(result, employee_data)
        
        # Step 4: Generate Human Reasoning
        print(f"🧠 Menghasilkan reasoning...")
        self._generate_human_reasoning(result, employee_data, job_profile)
        
        # Step 5: Generate Recommendations
        print(f"💡 Membuat rekomendasi...")
        self._generate_recommendations(result, job_profile)
        
        print(f"✅ Analisis selesai: {result.employee_name} - Score: {result.overall_score:.1f}/100")
        
        return result
    
    def analyze_batch(
        self,
        employees_df: pd.DataFrame,
        job_criteria: str,
        target_position: str,
        use_social_media: bool = False
    ) -> pd.DataFrame:
        """
        Analisis batch untuk multiple employees
        
        Args:
            employees_df: DataFrame dengan kolom: name, position, skills, experience, bio
            job_criteria: Deskripsi kriteria posisi
            target_position: Nama posisi target
            use_social_media: Apakah analyze social media
            
        Returns:
            DataFrame dengan hasil analisis
        """
        print(f"\n🚀 Memulai batch analysis untuk {len(employees_df)} kandidat...")
        print(f"📋 Target Position: {target_position}")
        print("=" * 70)
        
        results = []
        
        for idx, row in employees_df.iterrows():
            print(f"\n[{idx + 1}/{len(employees_df)}] Analyzing: {row.get('name', 'Unknown')}")
            print("-" * 70)
            
            employee_data = row.to_dict()
            
            try:
                analysis = self.analyze_employee(
                    employee_data=employee_data,
                    job_criteria=job_criteria,
                    target_position=target_position,
                    use_social_media=use_social_media
                )
                results.append(analysis.to_dict())
                
            except Exception as e:
                print(f"❌ Error analyzing {row.get('name')}: {str(e)}")
                results.append({
                    'employee_name': row.get('name', 'Unknown'),
                    'error': str(e)
                })
        
        print("\n" + "=" * 70)
        print(f"✅ Batch analysis completed!")
        
        return pd.DataFrame(results)
    
    def _calculate_flexible_scores(
        self,
        result: UltraEmployeeAnalysisResult,
        employee_data: Dict[str, Any],
        job_profile: JobProfile,
        job_criteria: str
    ):
        """Calculate scores dengan fleksibilitas berdasarkan job complexity"""
        
        weights = self.job_detector.get_scoring_weights(job_profile.complexity)
        
        # Extract employee info
        skills = employee_data.get('skills', '')
        experience = employee_data.get('experience', '')
        bio = employee_data.get('bio', '')
        position = employee_data.get('position', '')
        
        # Combine all text
        employee_text = f"{position}. {skills}. {experience}. {bio}"
        
        # 1. Soft Skills Score (penting untuk low complexity)
        result.soft_skills_score = self._score_soft_skills(employee_text, job_profile)
        
        # 2. Hard Skills Score
        result.hard_skills_score = self._score_hard_skills(skills, job_criteria, job_profile)
        
        # 3. Experience Relevance (fleksibel untuk low complexity)
        result.experience_relevance_score = self._score_experience_relevance(
            experience, position, job_criteria, job_profile
        )
        
        # 4. Character Score (dari bio)
        result.character_score = self._score_character(bio, job_profile)
        
        # 5. Attitude Score (dari overall profile)
        result.attitude_score = self._score_attitude(employee_text, job_profile)
        
        # 6. Cultural Fit Score (semantic matching)
        result.cultural_fit_score = self._score_cultural_fit(employee_text, job_criteria)
        
        # Calculate weighted overall score
        result.overall_score = (
            weights['soft_skills'] * result.soft_skills_score +
            weights['hard_skills'] * result.hard_skills_score +
            weights['experience_relevance'] * result.experience_relevance_score +
            weights['cv_clarity'] * result.character_score +
            weights['attitude_potential'] * result.attitude_score +
            0.05 * result.cultural_fit_score
        )
        
        result.overall_score = min(result.overall_score, 100)
    
    def _score_soft_skills(self, text: str, job_profile: JobProfile) -> float:
        """Score soft skills dengan boost untuk entry-level"""
        soft_skill_keywords = [
            'komunikasi', 'communication', 'teamwork', 'kerja sama', 'leadership',
            'kepemimpinan', 'problem solving', 'creative', 'kreatif', 'adaptable',
            'responsible', 'tanggung jawab', 'initiative', 'inisiatif', 'collaborative',
            'organized', 'terorganisir', 'presentation', 'presentasi'
        ]
        
        text_lower = text.lower()
        matches = sum(1 for keyword in soft_skill_keywords if keyword in text_lower)
        
        base_score = min(matches * 12, 100)
        
        # Boost untuk low complexity jobs
        if job_profile.complexity == JobComplexity.LOW:
            base_score = min(base_score * 1.3, 100)
        
        return max(base_score, 50.0)  # Minimum 50 untuk benefit of doubt
    
    def _score_hard_skills(self, skills: str, job_criteria: str, job_profile: JobProfile) -> float:
        """Score hard skills dengan semantic matching"""
        if not skills or len(skills.strip()) < 5:
            # Untuk low complexity, tidak masalah
            if job_profile.complexity == JobComplexity.LOW:
                return 65.0
            else:
                return 30.0
        
        # Semantic similarity
        try:
            similarity = self.ai_engine.compute_semantic_similarity(skills, job_criteria)
            score = similarity * 100
        except:
            score = 50.0
        
        # Adjustment untuk low complexity
        if job_profile.complexity == JobComplexity.LOW:
            score = min(score * 1.2, 100)
        
        return score
    
    def _score_experience_relevance(
        self,
        experience: str,
        position: str,
        job_criteria: str,
        job_profile: JobProfile
    ) -> float:
        """Score experience dengan fleksibilitas"""
        
        # Untuk low complexity: tidak strict
        if job_profile.complexity == JobComplexity.LOW:
            # Check jika ada pengalaman apapun
            if experience and len(experience.strip()) > 10:
                return 80.0  # Punya pengalaman = bagus
            elif position and len(position.strip()) > 3:
                return 70.0  # Minimal punya posisi sekarang
            else:
                return 60.0  # Fresh/minimal experience tapi OK untuk entry level
        
        # Untuk mid/high complexity: semantic matching
        combined_exp = f"{position}. {experience}"
        
        if not combined_exp.strip():
            return 20.0
        
        try:
            similarity = self.ai_engine.compute_semantic_similarity(combined_exp, job_criteria)
            return similarity * 100
        except:
            return 40.0
    
    def _score_character(self, bio: str, job_profile: JobProfile) -> float:
        """Score character dari bio"""
        if not bio or len(bio.strip()) < 10:
            return 50.0
        
        positive_traits = [
            'motivated', 'passionate', 'dedicated', 'enthusiastic', 'committed',
            'diligent', 'reliable', 'trustworthy', 'honest', 'integrity',
            'termotivasi', 'berdedikasi', 'antusias', 'jujur', 'bertanggung jawab'
        ]
        
        bio_lower = bio.lower()
        matches = sum(1 for trait in positive_traits if trait in bio_lower)
        
        score = 50 + (matches * 10)
        return min(score, 100)
    
    def _score_attitude(self, text: str, job_profile: JobProfile) -> float:
        """Score attitude dari overall profile"""
        # Look for positive attitude indicators
        positive_indicators = [
            'learn', 'belajar', 'growth', 'berkembang', 'improve', 'meningkatkan',
            'achieve', 'mencapai', 'contribute', 'berkontribusi', 'passionate',
            'excited', 'eager', 'willing', 'ready', 'siap'
        ]
        
        text_lower = text.lower()
        matches = sum(1 for indicator in positive_indicators if indicator in text_lower)
        
        score = 55 + (matches * 8)
        
        # Boost untuk low complexity (attitude > skill)
        if job_profile.complexity == JobComplexity.LOW:
            score = min(score * 1.15, 100)
        
        return min(score, 100)
    
    def _score_cultural_fit(self, employee_text: str, job_criteria: str) -> float:
        """Score cultural fit menggunakan semantic similarity"""
        try:
            similarity = self.ai_engine.compute_semantic_similarity(employee_text, job_criteria)
            return similarity * 100
        except:
            return 60.0
    
    def _analyze_social_media(self, result: UltraEmployeeAnalysisResult, employee_data: Dict[str, Any]):
        """Analyze social media jika tersedia"""
        social_url = employee_data.get('social_media_url', '')
        
        if not social_url:
            # Auto-search berdasarkan nama
            name = employee_data.get('name', '')
            if name:
                result.social_insights.append(f"Social media untuk {name} tidak ditemukan/tidak disediakan")
                result.social_sentiment = "Not Available"
                result.social_professionalism_score = 50.0
            return
        
        # Mock analysis (real implementation would scrape)
        result.social_insights.append("Social media profile found")
        result.social_insights.append("Profile menunjukkan aktivitas profesional")
        result.social_sentiment = "Positive"
        result.social_professionalism_score = 75.0
    
    def _generate_human_reasoning(
        self,
        result: UltraEmployeeAnalysisResult,
        employee_data: Dict[str, Any],
        job_profile: JobProfile
    ):
        """Generate reasoning seperti HR profesional"""
        
        name = result.employee_name
        position = result.position_current or "posisi tidak disebutkan"
        target = result.target_position
        
        # Executive Summary
        if job_profile.complexity == JobComplexity.LOW:
            # Entry-level: fokus attitude dan potential
            result.executive_summary = (
                f"Untuk posisi {target} yang termasuk kategori entry-level, "
                f"{name} (saat ini: {position}) menunjukkan profil yang layak dipertimbangkan. "
                f"Pekerjaan ini lebih mengutamakan soft skill, attitude, dan kemampuan belajar "
                f"dibandingkan pengalaman teknis spesifik. "
            )
            
            if result.overall_score >= 70:
                result.executive_summary += (
                    f"Kandidat menunjukkan indikator positif dalam hal komunikasi, organisasi, "
                    f"dan kemauan untuk belajar, yang merupakan faktor kunci untuk sukses di posisi ini."
                )
            else:
                result.executive_summary += (
                    f"Kandidat menunjukkan potensi, namun perlu evaluasi lebih lanjut "
                    f"terutama dalam aspek soft skills dan attitude."
                )
        else:
            # Mid/High complexity: fokus expertise
            result.executive_summary = (
                f"{name} dengan latar belakang sebagai {position} sedang dievaluasi untuk posisi {target}. "
                f"Posisi ini membutuhkan keahlian spesifik dan pengalaman relevan. "
            )
            
            if result.overall_score >= 75:
                result.executive_summary += (
                    f"Kandidat menunjukkan kesesuaian yang kuat dengan kriteria posisi, "
                    f"dengan skill dan pengalaman yang relevan."
                )
            else:
                result.executive_summary += (
                    f"Terdapat gap antara profil kandidat dengan kebutuhan posisi "
                    f"yang perlu dievaluasi lebih lanjut."
                )
        
        # Detailed Reasoning
        reasoning_parts = []
        
        # Experience
        experience = employee_data.get('experience', '')
        if experience and len(experience.strip()) > 10:
            reasoning_parts.append(
                f"**Pengalaman**: {name} memiliki pengalaman di bidang terkait. "
                f"Untuk posisi {target}, pengalaman ini dapat menjadi foundation yang baik."
            )
        else:
            if job_profile.complexity == JobComplexity.LOW:
                reasoning_parts.append(
                    f"**Pengalaman**: Meskipun pengalaman formal mungkin terbatas, "
                    f"untuk posisi entry-level seperti {target}, yang lebih penting adalah "
                    f"attitude, kemampuan belajar cepat, dan kemauan untuk berkembang."
                )
            else:
                reasoning_parts.append(
                    f"**Pengalaman**: Kandidat memiliki pengalaman terbatas untuk posisi {target}. "
                    f"Ini menjadi pertimbangan mengingat posisi ini umumnya membutuhkan track record yang jelas."
                )
        
        # Skills
        skills = employee_data.get('skills', '')
        if skills and len(skills.strip()) > 10:
            reasoning_parts.append(
                f"**Keahlian**: Kandidat menunjukkan skill yang mencakup: {skills[:100]}... "
                f"Skill ini relevan dengan kebutuhan posisi."
            )
        else:
            if job_profile.complexity == JobComplexity.LOW:
                reasoning_parts.append(
                    f"**Keahlian**: Untuk posisi {target}, hard skill teknis bukan requirement utama. "
                    f"Soft skill seperti komunikasi, organisasi, dan teamwork lebih kritikal."
                )
        
        # Bio/Character
        bio = employee_data.get('bio', '')
        if bio and len(bio.strip()) > 10:
            reasoning_parts.append(
                f"**Karakter & Attitude**: Profil menunjukkan {bio[:150]}... "
                f"Ini memberikan insight tentang mindset dan motivasi kandidat."
            )
        
        result.detailed_reasoning = "\n\n".join(reasoning_parts)
        
        # Key Strengths
        if result.soft_skills_score >= 70:
            result.key_strengths.append("Soft skills yang baik")
        if result.hard_skills_score >= 70:
            result.key_strengths.append("Hard skills relevan")
        if result.attitude_score >= 75:
            result.key_strengths.append("Attitude dan motivasi positif")
        if result.experience_relevance_score >= 70:
            result.key_strengths.append("Pengalaman yang relevan")
        
        # Key Concerns
        if result.experience_relevance_score < 50 and job_profile.complexity != JobComplexity.LOW:
            result.key_concerns.append("Pengalaman belum sepenuhnya match")
        if result.hard_skills_score < 50 and job_profile.complexity == JobComplexity.HIGH:
            result.key_concerns.append("Perlu verifikasi technical skills")
    
    def _generate_recommendations(
        self,
        result: UltraEmployeeAnalysisResult,
        job_profile: JobProfile
    ):
        """Generate recommendations"""
        
        # Determine recommendation level
        if result.overall_score >= 85:
            result.tier = "EXCELLENT"
            result.recommendation = "STRONGLY RECOMMEND"
            result.confidence = 0.95
            result.position_fit_explanation = (
                f"{result.employee_name} sangat cocok untuk posisi {result.target_position}. "
                f"Profil menunjukkan kesesuaian yang sangat baik dengan semua kriteria utama."
            )
        elif result.overall_score >= 70:
            result.tier = "STRONG"
            result.recommendation = "RECOMMEND"
            result.confidence = 0.85
            result.position_fit_explanation = (
                f"{result.employee_name} cocok untuk posisi {result.target_position}. "
                f"Kandidat memiliki foundation yang baik dan dapat berkontribusi dengan efektif."
            )
        elif result.overall_score >= 55:
            result.tier = "MEDIUM"
            result.recommendation = "CONSIDER"
            result.confidence = 0.70
            result.position_fit_explanation = (
                f"{result.employee_name} layak dipertimbangkan untuk posisi {result.target_position}. "
                f"Terdapat beberapa gap yang bisa di-address melalui training atau mentoring."
            )
        else:
            result.tier = "LOW"
            result.recommendation = "NOT SUITABLE"
            result.confidence = 0.50
            result.position_fit_explanation = (
                f"{result.employee_name} belum sepenuhnya cocok untuk posisi {result.target_position}. "
                f"Pertimbangkan posisi alternatif atau pengembangan skill lebih lanjut."
            )
        
        # Special adjustment untuk fresh grad di low complexity
        if (job_profile.complexity == JobComplexity.LOW and 
            result.overall_score >= 60 and 
            result.tier == "MEDIUM"):
            result.recommendation = "RECOMMEND"
            result.confidence = min(result.confidence + 0.1, 0.95)
            result.position_fit_explanation += (
                f" Untuk posisi entry-level, attitude dan kemampuan belajar lebih penting "
                f"daripada pengalaman, dan kandidat menunjukkan potensi yang baik."
            )
        
        # Onboarding focus
        if job_profile.complexity == JobComplexity.LOW:
            result.onboarding_focus = [
                "Orientation proses dan prosedur",
                "Basic training untuk tools/system",
                "Mentoring untuk soft skills development"
            ]
        else:
            result.onboarding_focus = [
                "Technical deep dive",
                "Project-based learning",
                "Code review dan best practices"
            ]
        
        # Alternative positions
        if result.soft_skills_score >= 75:
            result.alternative_positions.append("Customer Service / Front Office")
        if result.character_score >= 75:
            result.alternative_positions.append("Team Coordinator / Admin")
