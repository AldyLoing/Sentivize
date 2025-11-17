"""
Job Complexity Detector Module
Otomatis mengelompokkan pekerjaan berdasarkan kompleksitas dan kebutuhan skill
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class JobComplexity(Enum):
    LOW = "low"
    MID = "mid"
    HIGH = "high"

@dataclass
class JobProfile:
    """Profile hasil analisis kompleksitas pekerjaan"""
    title: str
    complexity: JobComplexity
    confidence: float
    reasoning: str
    key_requirements: List[str]
    soft_skill_weight: float  # 0-1, tinggi untuk low complexity
    hard_skill_weight: float  # 0-1, tinggi untuk high complexity
    experience_flexibility: float  # 0-1, tinggi untuk low complexity
    fresh_graduate_friendly: bool

class JobComplexityDetector:
    """
    Detector pintar untuk menganalisis kompleksitas pekerjaan
    menggunakan semantic understanding dan keyword patterns
    """
    
    def __init__(self, ai_engine=None):
        self.ai_engine = ai_engine
        
        # Low-complexity job patterns
        self.low_complexity_patterns = {
            'admin': ['admin', 'administrasi', 'administrative', 'clerk', 'office'],
            'customer_service': ['customer service', 'cs', 'front office', 'receptionist', 'frontliner'],
            'retail': ['kasir', 'cashier', 'toko', 'retail', 'sales assistant', 'pramuniaga'],
            'data_entry': ['data entry', 'input data', 'data clerk'],
            'warehouse': ['gudang', 'warehouse', 'packer', 'picker', 'stock'],
            'support': ['support', 'helpdesk', 'assistant'],
            'general': ['umum', 'general', 'junior', 'trainee', 'staff']
        }
        
        # High-complexity job patterns
        self.high_complexity_patterns = {
            'engineering': ['engineer', 'developer', 'programmer', 'software', 'hardware', 'technical lead'],
            'it': ['it', 'system', 'network', 'database', 'devops', 'cloud', 'architect'],
            'management': ['manager', 'head', 'director', 'supervisor', 'leader', 'koordinator'],
            'finance': ['finance', 'accounting', 'auditor', 'financial', 'treasurer'],
            'specialist': ['specialist', 'expert', 'consultant', 'analyst', 'researcher'],
            'medical': ['doctor', 'nurse', 'medical', 'healthcare', 'pharmacist'],
            'legal': ['lawyer', 'legal', 'attorney', 'counsel'],
            'design': ['designer', 'architect', 'ui', 'ux', 'graphic', 'creative director']
        }
        
        # Mid-complexity adalah default untuk yang tidak masuk kategori low/high
        
    def detect_complexity(self, job_title: str, job_description: str = "") -> JobProfile:
        """
        Analisis kompleksitas pekerjaan berdasarkan judul dan deskripsi
        
        Args:
            job_title: Judul posisi pekerjaan
            job_description: Deskripsi pekerjaan (opsional)
            
        Returns:
            JobProfile dengan analisis lengkap
        """
        job_text = f"{job_title} {job_description}".lower()
        
        # Cek low complexity
        low_score, low_matches = self._calculate_pattern_score(job_text, self.low_complexity_patterns)
        
        # Cek high complexity
        high_score, high_matches = self._calculate_pattern_score(job_text, self.high_complexity_patterns)
        
        # Determine complexity
        if low_score > 0.5 and low_score > high_score:
            complexity = JobComplexity.LOW
            confidence = low_score
            reasoning = self._generate_low_complexity_reasoning(job_title, low_matches)
            soft_skill_weight = 0.65  # Soft skill sangat penting
            hard_skill_weight = 0.35
            experience_flexibility = 0.85  # Sangat fleksibel
            fresh_graduate_friendly = True
            key_requirements = ["Komunikasi baik", "Attitude positif", "Kemampuan belajar", "Organisasi"]
            
        elif high_score > 0.5:
            complexity = JobComplexity.HIGH
            confidence = high_score
            reasoning = self._generate_high_complexity_reasoning(job_title, high_matches)
            soft_skill_weight = 0.30
            hard_skill_weight = 0.70  # Hard skill dominan
            experience_flexibility = 0.30  # Butuh pengalaman spesifik
            fresh_graduate_friendly = False
            key_requirements = ["Skill teknis spesifik", "Pengalaman relevan", "Problem solving", "Keahlian mendalam"]
            
        else:
            complexity = JobComplexity.MID
            confidence = 0.7
            reasoning = self._generate_mid_complexity_reasoning(job_title)
            soft_skill_weight = 0.45
            hard_skill_weight = 0.55
            experience_flexibility = 0.60
            fresh_graduate_friendly = True  # Tergantung skill
            key_requirements = ["Kombinasi soft & hard skill", "Pengalaman relevan", "Kemampuan adaptasi"]
        
        return JobProfile(
            title=job_title,
            complexity=complexity,
            confidence=confidence,
            reasoning=reasoning,
            key_requirements=key_requirements,
            soft_skill_weight=soft_skill_weight,
            hard_skill_weight=hard_skill_weight,
            experience_flexibility=experience_flexibility,
            fresh_graduate_friendly=fresh_graduate_friendly
        )
    
    def _calculate_pattern_score(self, text: str, patterns: Dict[str, List[str]]) -> Tuple[float, List[str]]:
        """Calculate how well text matches pattern categories"""
        matches = []
        total_score = 0
        
        for category, keywords in patterns.items():
            for keyword in keywords:
                if keyword in text:
                    matches.append(keyword)
                    total_score += 1
        
        # Normalize score
        max_possible = len(patterns)
        normalized_score = min(total_score / max_possible, 1.0) if max_possible > 0 else 0
        
        return normalized_score, matches
    
    def _generate_low_complexity_reasoning(self, job_title: str, matches: List[str]) -> str:
        """Generate reasoning untuk low complexity jobs"""
        return (
            f"Posisi '{job_title}' terdeteksi sebagai pekerjaan entry-level/low-complexity. "
            f"Pekerjaan ini lebih mengutamakan soft skill seperti komunikasi, attitude, dan kemampuan belajar. "
            f"Fresh graduate dan kandidat tanpa pengalaman langsung tetap layak dipertimbangkan jika menunjukkan "
            f"kemampuan organisasi, dokumentasi, dan kemauan belajar yang baik. "
            f"Pengalaman organisasi atau proyek pribadi dapat dianggap sebagai nilai tambah yang relevan."
        )
    
    def _generate_high_complexity_reasoning(self, job_title: str, matches: List[str]) -> str:
        """Generate reasoning untuk high complexity jobs"""
        return (
            f"Posisi '{job_title}' terdeteksi sebagai pekerjaan spesialisasi/high-complexity. "
            f"Pekerjaan ini membutuhkan keahlian teknis spesifik dan pengalaman relevan yang kuat. "
            f"Kandidat diharapkan memiliki track record dalam bidang terkait, portfolio yang jelas, "
            f"dan kemampuan problem-solving yang mendalam. Fresh graduate perlu menunjukkan proyek "
            f"atau pengalaman magang yang sangat relevan untuk dipertimbangkan."
        )
    
    def _generate_mid_complexity_reasoning(self, job_title: str) -> str:
        """Generate reasoning untuk mid complexity jobs"""
        return (
            f"Posisi '{job_title}' terdeteksi sebagai pekerjaan mid-complexity. "
            f"Pekerjaan ini membutuhkan kombinasi antara soft skill dan hard skill yang seimbang. "
            f"Kandidat dengan pengalaman relevan akan lebih diutamakan, namun fresh graduate dengan "
            f"skill yang kuat dan pengalaman organisasi/proyek tetap dapat dipertimbangkan. "
            f"Kemampuan adaptasi dan pembelajaran cepat menjadi nilai tambah penting."
        )
    
    def get_scoring_weights(self, complexity: JobComplexity) -> Dict[str, float]:
        """
        Return scoring weights berdasarkan kompleksitas pekerjaan
        untuk digunakan dalam analisis kandidat
        """
        if complexity == JobComplexity.LOW:
            return {
                'soft_skills': 0.35,
                'hard_skills': 0.15,
                'experience_relevance': 0.15,
                'organizational_experience': 0.15,
                'cv_clarity': 0.10,
                'attitude_potential': 0.10
            }
        elif complexity == JobComplexity.HIGH:
            return {
                'soft_skills': 0.10,
                'hard_skills': 0.40,
                'experience_relevance': 0.30,
                'organizational_experience': 0.05,
                'cv_clarity': 0.05,
                'attitude_potential': 0.10
            }
        else:  # MID
            return {
                'soft_skills': 0.25,
                'hard_skills': 0.30,
                'experience_relevance': 0.25,
                'organizational_experience': 0.10,
                'cv_clarity': 0.05,
                'attitude_potential': 0.05
            }
    
    def should_be_flexible(self, complexity: JobComplexity) -> bool:
        """Return True jika evaluasi harus fleksibel untuk fresh graduate"""
        return complexity == JobComplexity.LOW
