"""
CV Preview Extractor Module
Ekstraksi dan preview data CV sebelum analisis lengkap
dengan AI-powered intelligent extraction
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import pdfplumber
from docx import Document


@dataclass
class CVPreview:
    """Preview data hasil ekstraksi CV dengan AI enhancement"""
    # Basic Info
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    
    # Education
    education_summary: List[str] = field(default_factory=list)
    highest_education: str = ""
    
    # Skills
    hard_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    programming_languages: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    implicit_skills: List[str] = field(default_factory=list)  # AI-detected implicit skills
    
    # Experience
    work_experiences: List[Dict[str, str]] = field(default_factory=list)  # {title, company, duration}
    organizational_experiences: List[Dict[str, str]] = field(default_factory=list)
    projects: List[Dict[str, str]] = field(default_factory=list)
    
    # Analysis
    candidate_level: str = "Unknown"  # fresh_graduate / junior / mid / senior
    candidate_type: str = "Unknown"  # Generalist / Specialist / Career Shifter
    estimated_job_complexity: str = "mid"  # low / mid / high
    total_work_experience_months: int = 0
    total_years_display: str = "0 tahun"
    
    # Career Pattern Analysis (AI-powered)
    career_summary: str = ""  # 3-5 kalimat ringkasan karier
    career_trajectory: str = ""  # Growing / Stable / Shifting
    main_focus_area: str = ""  # Bidang utama karier
    
    # Initial Assessment
    initial_conclusion: str = ""
    strengths: List[str] = field(default_factory=list)
    growth_indicators: List[str] = field(default_factory=list)
    
    # Flags
    is_fresh_graduate: bool = False
    is_career_shifter: bool = False
    has_leadership_experience: bool = False
    has_technical_background: bool = False
    
    # Raw text for further processing
    raw_text: str = ""
    
    def get_display_summary(self) -> str:
        """Generate display summary untuk UI preview"""
        summary_parts = []
        
        summary_parts.append(f"👤 **{self.full_name or 'Nama tidak terdeteksi'}**")
        
        if self.email or self.phone:
            contact = []
            if self.email:
                contact.append(f"📧 {self.email}")
            if self.phone:
                contact.append(f"📱 {self.phone}")
            summary_parts.append(" | ".join(contact))
        
        if self.highest_education:
            summary_parts.append(f"🎓 **Pendidikan:** {self.highest_education}")
        
        summary_parts.append(f"💼 **Level:** {self.candidate_level}")
        summary_parts.append(f"📊 **Pengalaman:** {self.total_years_display}")
        
        if self.main_focus_area:
            summary_parts.append(f"🎯 **Fokus:** {self.main_focus_area}")
        
        # Top skills
        top_skills = []
        if self.programming_languages:
            top_skills.extend(self.programming_languages[:3])
        if self.hard_skills and len(top_skills) < 5:
            top_skills.extend(self.hard_skills[:5-len(top_skills)])
        
        if top_skills:
            summary_parts.append(f"⚡ **Skill Utama:** {', '.join(top_skills)}")
        
        # Flags
        flags = []
        if self.is_fresh_graduate:
            flags.append("🌱 Fresh Graduate")
        if self.is_career_shifter:
            flags.append("🔄 Career Shifter")
        if self.has_leadership_experience:
            flags.append("👔 Leadership Experience")
        if self.has_technical_background:
            flags.append("💻 Technical Background")
        
        if flags:
            summary_parts.append(" | ".join(flags))
        
        return "\n\n".join(summary_parts)

class CVPreviewExtractor:
    """
    Ekstraksi cepat dan akurat dari CV untuk preview sebelum analisis
    dengan AI-powered intelligent extraction
    """
    
    def __init__(self, use_ai: bool = True):
        """
        Initialize extractor
        
        Args:
            use_ai: Gunakan AI untuk enhance extraction (default: True)
        """
        self.use_ai = use_ai
        
        # Lazy load AI engine
        self._ai_engine = None
        
        # Regex patterns untuk ekstraksi
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}')
        self.linkedin_pattern = re.compile(r'linkedin\.com/in/[\w-]+')
        self.github_pattern = re.compile(r'github\.com/[\w-]+')
        
        # Common soft skills
        self.soft_skills_keywords = [
            'komunikasi', 'communication', 'leadership', 'kepemimpinan', 'teamwork', 
            'kerja sama', 'problem solving', 'critical thinking', 'adaptability',
            'time management', 'organizational', 'presentation', 'negotiation',
            'interpersonal', 'creativity', 'initiative', 'responsibility', 'tanggung jawab'
        ]
        
        # Programming languages dan tools
        self.programming_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby',
            'go', 'rust', 'kotlin', 'swift', 'sql', 'html', 'css', 'r', 'matlab'
        ]
        
        self.tools_keywords = [
            'git', 'docker', 'kubernetes', 'aws', 'azure', 'react', 'vue', 'angular',
            'node.js', 'django', 'flask', 'spring', 'tensorflow', 'pytorch', 'pandas',
            'excel', 'powerpoint', 'word', 'tableau', 'power bi', 'figma', 'photoshop'
        ]
        
        # Education keywords
        self.education_keywords = ['universitas', 'university', 'institut', 'institute', 
                                   'sekolah', 'school', 'sarjana', 'bachelor', 'master',
                                   's1', 's2', 's3', 'diploma', 'd3', 'd4']
        
        # Experience keywords
        self.experience_keywords = ['pengalaman', 'experience', 'worked', 'bekerja', 
                                    'position', 'posisi', 'role', 'peran']
    
    @property
    def ai_engine(self):
        """Lazy load AI engine"""
        if self._ai_engine is None and self.use_ai:
            try:
                from ai.openrouter_engine import get_openrouter_engine
                self._ai_engine = get_openrouter_engine()
            except Exception as e:
                print(f"⚠️ AI Engine not available: {e}")
                self.use_ai = False
        return self._ai_engine
        
    def extract_from_file(self, file_path: str, file_type: str = 'pdf') -> CVPreview:
        """
        Ekstraksi CV dari file PDF atau DOCX
        
        Args:
            file_path: Path ke file CV
            file_type: 'pdf' atau 'docx'
            
        Returns:
            CVPreview object dengan data terektraksi
        """
        # Extract text
        if file_type.lower() == 'pdf':
            text = self._extract_text_from_pdf(file_path)
        elif file_type.lower() in ['docx', 'doc']:
            text = self._extract_text_from_docx(file_path)
        else:
            text = self._extract_text_from_txt(file_path)
        
        return self.extract_from_text(text)
    
    def extract_from_text(self, text: str) -> CVPreview:
        """
        Ekstraksi CV dari raw text
        
        Args:
            text: Raw text dari CV
            
        Returns:
            CVPreview object dengan data terektraksi
        """
        preview = CVPreview(raw_text=text)
        
        # Extract basic info
        preview.full_name = self._extract_name(text)
        preview.email = self._extract_email(text)
        preview.phone = self._extract_phone(text)
        preview.linkedin = self._extract_linkedin(text)
        preview.github = self._extract_github(text)
        
        # Extract education
        preview.education_summary = self._extract_education(text)
        
        # Extract skills
        preview.hard_skills, preview.soft_skills = self._extract_skills(text)
        preview.programming_languages = self._extract_programming_languages(text)
        preview.tools = self._extract_tools(text)
        
        # Extract experiences
        preview.work_experiences = self._extract_work_experience(text)
        preview.organizational_experiences = self._extract_organizational_experience(text)
        preview.projects = self._extract_projects(text)
        
        # Calculate experience
        preview.total_work_experience_months = self._calculate_total_experience(
            preview.work_experiences, preview.organizational_experiences
        )
        
        # Determine candidate level
        preview.candidate_level = self._determine_candidate_level(
            preview.total_work_experience_months,
            preview.work_experiences,
            preview.education_summary
        )
        
        # Set flags
        preview.is_fresh_graduate = preview.total_work_experience_months < 12
        preview.is_career_shifter = self._detect_career_shifter(preview.work_experiences)
        preview.has_leadership_experience = self._has_leadership_exp(preview.work_experiences)
        preview.has_technical_background = len(preview.programming_languages) > 0 or len(preview.tools) > 2
        
        # Estimate job complexity suitability
        preview.estimated_job_complexity = self._estimate_job_complexity_fit(preview)
        
        # Display years
        years = preview.total_work_experience_months / 12
        preview.total_years_display = f"{years:.1f} tahun" if years > 0 else "Fresh Graduate"
        
        # Determine highest education
        preview.highest_education = self._determine_highest_education(preview.education_summary)
        
        # AI Enhancement (jika enabled)
        if self.use_ai and self.ai_engine:
            preview = self._enhance_with_ai(preview)
        else:
            # Fallback manual analysis
            preview.initial_conclusion = self._generate_initial_conclusion(preview)
            preview.strengths = self._identify_strengths(preview)
            preview.career_summary = self._generate_manual_career_summary(preview)
            preview.main_focus_area = self._detect_main_focus(preview)
        
        return preview
    
    def _enhance_with_ai(self, preview: CVPreview) -> CVPreview:
        """Enhance preview dengan AI reasoning"""
        try:
            # Generate career summary dengan AI
            if len(preview.raw_text) > 100:
                preview.career_summary = self.ai_engine.generate_career_summary(
                    preview.raw_text,
                    max_sentences=5
                )
            
            # Extract implicit skills dengan AI
            if len(preview.raw_text) > 100:
                skills_result = self.ai_engine.extract_skills_intelligent(preview.raw_text)
                preview.implicit_skills = skills_result.get('implicit_skills', [])[:5]
                
                # Merge dengan existing skills jika ada yang terlewat
                ai_hard_skills = skills_result.get('hard_skills', [])
                for skill in ai_hard_skills:
                    if skill not in preview.hard_skills and len(preview.hard_skills) < 15:
                        preview.hard_skills.append(skill)
            
            # Generate conclusion dan strengths
            preview.initial_conclusion = self._generate_ai_conclusion(preview)
            preview.strengths = self._identify_strengths_ai(preview)
            preview.main_focus_area = self._detect_main_focus(preview)
            preview.career_trajectory = self._analyze_career_trajectory(preview)
            
        except Exception as e:
            print(f"⚠️ AI enhancement failed: {e}. Using fallback.")
            preview.initial_conclusion = self._generate_initial_conclusion(preview)
            preview.strengths = self._identify_strengths(preview)
            preview.career_summary = self._generate_manual_career_summary(preview)
        
        return preview
    
    def _generate_ai_conclusion(self, preview: CVPreview) -> str:
        """Generate conclusion dengan context awareness"""
        conclusion_parts = []
        
        # Level dan experience
        if preview.is_fresh_graduate:
            if len(preview.projects) > 0 or len(preview.organizational_experiences) > 0:
                conclusion_parts.append(
                    f"✅ Kandidat **fresh graduate aktif** dengan "
                    f"{len(preview.projects)} project dan {len(preview.organizational_experiences)} pengalaman organisasi."
                )
            else:
                conclusion_parts.append("✅ Kandidat **fresh graduate**. Cocok untuk posisi entry-level dengan training.")
        else:
            years = preview.total_work_experience_months / 12
            conclusion_parts.append(
                f"✅ Kandidat **{preview.candidate_level}** dengan pengalaman **{years:.1f} tahun**."
            )
        
        # Technical background
        if preview.has_technical_background:
            tech_skills = preview.programming_languages + preview.tools
            conclusion_parts.append(
                f"💻 Background teknis dengan keahlian: **{', '.join(tech_skills[:3])}**."
            )
        
        # Career pattern
        if preview.is_career_shifter:
            conclusion_parts.append("🔄 Terdeteksi sebagai **career shifter** dengan pengalaman lintas industri.")
        
        # Leadership
        if preview.has_leadership_experience:
            conclusion_parts.append("👔 Memiliki **pengalaman leadership/managerial**.")
        
        # Suitable for
        if preview.estimated_job_complexity == "Low-Mid":
            conclusion_parts.append("📋 **Cocok untuk:** Posisi entry to mid-level dengan fokus learning & development.")
        elif preview.estimated_job_complexity == "Mid":
            conclusion_parts.append("📋 **Cocok untuk:** Posisi mid-level yang membutuhkan kombinasi skill & experience.")
        else:
            conclusion_parts.append("📋 **Cocok untuk:** Posisi specialist/senior dengan tanggung jawab tinggi.")
        
        return " ".join(conclusion_parts)
    
    def _identify_strengths_ai(self, preview: CVPreview) -> List[str]:
        """Identify strengths dengan AI awareness"""
        strengths = []
        
        # Technical strengths
        if len(preview.programming_languages) > 3:
            strengths.append(f"💻 Multi-language programmer ({', '.join(preview.programming_languages[:3])})")
        elif len(preview.programming_languages) > 0:
            strengths.append(f"💻 Programming: {', '.join(preview.programming_languages)}")
        
        # Tools mastery
        if len(preview.tools) > 5:
            strengths.append(f"🛠️ Wide range of tools ({len(preview.tools)} tools)")
        
        # Experience
        if preview.total_work_experience_months > 60:
            years = preview.total_work_experience_months // 12
            strengths.append(f"⭐ {years}+ years professional experience")
        elif preview.total_work_experience_months > 24:
            strengths.append("📈 Solid mid-level experience")
        
        # Projects & initiatives
        if len(preview.projects) > 3:
            strengths.append(f"🚀 Strong project portfolio ({len(preview.projects)} projects)")
        elif len(preview.projects) > 0:
            strengths.append(f"🚀 Project experience ({len(preview.projects)} projects)")
        
        # Organizational experience (valuable untuk fresh grad)
        if preview.is_fresh_graduate and len(preview.organizational_experiences) > 0:
            strengths.append(f"🌟 Active in organizations ({len(preview.organizational_experiences)})")
        
        # Leadership
        if preview.has_leadership_experience:
            strengths.append("👔 Leadership & management experience")
        
        # Soft skills diversity
        if len(preview.soft_skills) > 5:
            strengths.append(f"🤝 Well-rounded soft skills ({len(preview.soft_skills)} skills)")
        
        # Online presence
        if preview.linkedin and preview.github:
            strengths.append("🌐 Professional online presence (LinkedIn + GitHub)")
        elif preview.linkedin:
            strengths.append("🌐 LinkedIn profile available")
        
        # Implicit skills (AI-detected)
        if preview.implicit_skills and len(preview.implicit_skills) > 0:
            strengths.append(f"🎯 Implicit skills: {', '.join(preview.implicit_skills[:2])}")
        
        return strengths[:7]  # Max 7 strengths
    
    def _generate_manual_career_summary(self, preview: CVPreview) -> str:
        """Generate career summary tanpa AI (fallback)"""
        parts = []
        
        # Education
        if preview.highest_education:
            parts.append(f"Lulusan {preview.highest_education}")
        
        # Experience level
        if preview.is_fresh_graduate:
            parts.append("dengan antusiasme tinggi untuk memulai karier profesional")
        else:
            years = preview.total_work_experience_months / 12
            parts.append(f"dengan {years:.1f} tahun pengalaman kerja")
        
        # Main area
        if preview.has_technical_background:
            if preview.programming_languages:
                parts.append(f"di bidang teknologi, khususnya {', '.join(preview.programming_languages[:2])}")
        
        # Closing
        if preview.is_fresh_graduate:
            parts.append(". Memiliki potensi untuk berkembang dengan guidance yang tepat.")
        else:
            parts.append(". Kandidat siap untuk memberikan kontribusi immediate.")
        
        return " ".join(parts)
    
    def _detect_main_focus(self, preview: CVPreview) -> str:
        """Deteksi fokus utama karier"""
        # Dari job titles
        all_titles = [exp.get('title', '').lower() for exp in preview.work_experiences]
        title_text = ' '.join(all_titles)
        
        # Technical roles
        if any(keyword in title_text for keyword in ['developer', 'engineer', 'programmer', 'software']):
            return "Software Development"
        elif any(keyword in title_text for keyword in ['data', 'analyst', 'analytics']):
            return "Data & Analytics"
        elif any(keyword in title_text for keyword in ['design', 'ui', 'ux', 'graphic']):
            return "Design"
        elif any(keyword in title_text for keyword in ['manager', 'lead', 'head', 'director']):
            return "Management & Leadership"
        elif any(keyword in title_text for keyword in ['marketing', 'sales', 'business']):
            return "Business & Marketing"
        elif any(keyword in title_text for keyword in ['admin', 'administrative', 'officer']):
            return "Administration & Operations"
        elif any(keyword in title_text for keyword in ['finance', 'accounting', 'financial']):
            return "Finance & Accounting"
        
        # From skills
        if len(preview.programming_languages) > 2:
            return "Technology"
        elif len(preview.soft_skills) > len(preview.hard_skills):
            return "People & Operations"
        else:
            return "General / Multi-disciplinary"
    
    def _analyze_career_trajectory(self, preview: CVPreview) -> str:
        """Analyze career trajectory pattern"""
        if len(preview.work_experiences) == 0:
            return "Starting"
        
        # Check for progression in titles
        titles = [exp.get('title', '').lower() for exp in preview.work_experiences]
        
        has_junior = any('junior' in t or 'staff' in t for t in titles)
        has_senior = any('senior' in t or 'lead' in t or 'manager' in t for t in titles)
        
        if has_junior and has_senior:
            return "Growing (Junior → Senior)"
        elif has_senior:
            return "Established (Senior Level)"
        elif has_junior:
            return "Developing (Early Career)"
        elif len(preview.work_experiences) > 3:
            return "Stable (Multiple Experiences)"
        else:
            return "Building Foundation"
    
    def _detect_career_shifter(self, work_exp: List[Dict]) -> bool:
        """Deteksi apakah career shifter"""
        if len(work_exp) < 2:
            return False
        
        # Extract industries/roles
        titles = [exp.get('title', '').lower() for exp in work_exp]
        
        # Check for vastly different roles
        tech_roles = ['developer', 'engineer', 'programmer', 'it']
        business_roles = ['sales', 'marketing', 'business']
        admin_roles = ['admin', 'officer', 'coordinator']
        
        has_tech = any(any(role in title for role in tech_roles) for title in titles)
        has_business = any(any(role in title for role in business_roles) for title in titles)
        has_admin = any(any(role in title for role in admin_roles) for title in titles)
        
        # Career shifter if has roles in 2+ different categories
        category_count = sum([has_tech, has_business, has_admin])
        return category_count >= 2
    
    def _has_leadership_exp(self, work_exp: List[Dict]) -> bool:
        """Check apakah punya leadership experience"""
        leadership_keywords = ['manager', 'lead', 'head', 'director', 'supervisor', 
                              'coordinator', 'chief', 'kepala', 'koordinator']
        
        for exp in work_exp:
            title = exp.get('title', '').lower()
            if any(keyword in title for keyword in leadership_keywords):
                return True
        
        return False
    
    def _determine_highest_education(self, education_list: List[str]) -> str:
        """Determine highest education level dengan deteksi yang lebih akurat"""
        if not education_list:
            return "Tidak terdeteksi"
        
        edu_text = ' '.join(education_list).lower()
        
        # Deteksi dengan word boundary untuk menghindari false positive
        # Prioritas dari tertinggi ke terendah
        
        # S3 / Doktor (harus benar-benar S3, bukan bagian dari CSS3)
        if re.search(r'\bs3\b|\bdoktor\b|\bphd\b|\bdoctoral\b', edu_text):
            return "S3 / Doktor"
        
        # S2 / Master
        elif re.search(r'\bs2\b|\bmaster\b|\bmagister\b|\bm\.?sc\b|\bm\.?a\b', edu_text):
            return "S2 / Master"
        
        # S1 / Sarjana (paling umum untuk fresh graduate)
        elif re.search(r'\bs1\b|\bsarjana\b|\bbachelor\b|\bb\.?sc\b|\bb\.?a\b|\bgpa\b', edu_text):
            return "S1 / Sarjana"
        
        # D4
        elif re.search(r'\bd4\b|diploma 4|diploma iv', edu_text):
            return "D4"
        
        # D3
        elif re.search(r'\bd3\b|diploma 3|diploma iii|diploma', edu_text):
            return "D3"
        
        # SMA / SMK
        elif re.search(r'\bsma\b|\bsmk\b|high school|senior high', edu_text):
            return "SMA / SMK"
        
        # Try to extract university name (kemungkinan S1)
        for edu in education_list:
            if 'universitas' in edu.lower() or 'university' in edu.lower():
                return "S1 / Sarjana"
        
        return education_list[0][:50]  # Return first education entry
        
        return preview
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text dari PDF"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            text = f"Error extracting PDF: {str(e)}"
        return text
    
    def _extract_text_from_docx(self, file_path: str) -> str:
        """Extract text dari DOCX"""
        text = ""
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            text = f"Error extracting DOCX: {str(e)}"
        return text
    
    def _extract_text_from_txt(self, file_path: str) -> str:
        """Extract text dari TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                return f"Error extracting TXT: {str(e)}"
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Ekstraksi nama dari 3 baris pertama CV"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Nama biasanya di baris pertama atau kedua
        for line in lines[:3]:
            # Skip jika line terlalu panjang atau mengandung email/phone
            if len(line) > 50 or '@' in line or re.search(r'\d{3,}', line):
                continue
            # Check jika line hanya mengandung huruf dan spasi
            if re.match(r'^[A-Za-z\s.]+$', line) and len(line.split()) >= 2:
                return line
        
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Ekstraksi email"""
        match = self.email_pattern.search(text)
        return match.group(0) if match else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Ekstraksi nomor telepon"""
        match = self.phone_pattern.search(text)
        if match:
            phone = match.group(0)
            # Clean up
            phone = re.sub(r'[\s\-\(\)]', '', phone)
            return phone
        return None
    
    def _extract_linkedin(self, text: str) -> Optional[str]:
        """Ekstraksi LinkedIn URL"""
        match = self.linkedin_pattern.search(text.lower())
        return f"https://{match.group(0)}" if match else None
    
    def _extract_github(self, text: str) -> Optional[str]:
        """Ekstraksi GitHub URL"""
        match = self.github_pattern.search(text.lower())
        return f"https://{match.group(0)}" if match else None
    
    def _extract_education(self, text: str) -> List[str]:
        """Ekstraksi pendidikan dengan filter lebih ketat"""
        education = []
        lines = text.split('\n')
        
        # Keywords yang BUKAN education (untuk filter)
        non_education_keywords = ['html', 'css', 'javascript', 'python', 'java', 'php', 'api', 
                                  'cloud', 'devops', 'database', 'framework', 'library',
                                  'development', 'programming', 'technical', 'skill', 'bootstrap',
                                  'tailwind', 'vercel', 'railway', 'github', 'restful']
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Skip jika mengandung technical keywords (ini skill, bukan education)
            if any(tech_keyword in line_lower for tech_keyword in non_education_keywords):
                continue
            
            # Cari line yang mengandung education keywords
            if any(keyword in line_lower for keyword in self.education_keywords):
                # Ambil line tersebut dan beberapa line setelahnya
                education_lines = []
                for j in range(i, min(i+3, len(lines))):
                    line_text = lines[j].strip()
                    # Skip jika mengandung technical keywords
                    if line_text and not any(tech in line_text.lower() for tech in non_education_keywords):
                        education_lines.append(line_text)
                
                education_block = ' '.join(education_lines)
                if education_block and len(education_block) > 10:
                    education.append(education_block[:200])  # Limit length
        
        return education[:3]  # Max 3 entries
    
    def _extract_skills(self, text: str) -> Tuple[List[str], List[str]]:
        """Ekstraksi hard skills dan soft skills"""
        text_lower = text.lower()
        
        # Soft skills
        soft_skills = []
        for skill in self.soft_skills_keywords:
            if skill.lower() in text_lower:
                soft_skills.append(skill.title())
        
        # Hard skills - cari section skills
        hard_skills = []
        lines = text.split('\n')
        in_skills_section = False
        
        for line in lines:
            line_lower = line.lower()
            if 'skill' in line_lower or 'keahlian' in line_lower or 'kemampuan' in line_lower:
                in_skills_section = True
                continue
            
            if in_skills_section:
                # Stop jika ketemu section lain
                if any(keyword in line_lower for keyword in ['experience', 'pengalaman', 'education', 'pendidikan', 'project']):
                    break
                
                # Extract skills dari line
                if line.strip() and not line.strip().startswith(('•', '-', '*')):
                    # Pisah berdasarkan delimiter
                    skills_in_line = re.split(r'[,;|]', line)
                    for skill in skills_in_line:
                        skill = skill.strip()
                        if skill and len(skill) > 2 and len(skill) < 50:
                            hard_skills.append(skill)
        
        return list(set(hard_skills))[:15], list(set(soft_skills))[:10]
    
    def _extract_programming_languages(self, text: str) -> List[str]:
        """Ekstraksi bahasa pemrograman"""
        text_lower = text.lower()
        found_languages = []
        
        for lang in self.programming_keywords:
            if lang.lower() in text_lower:
                found_languages.append(lang.title())
        
        return list(set(found_languages))
    
    def _extract_tools(self, text: str) -> List[str]:
        """Ekstraksi tools dan technologies"""
        text_lower = text.lower()
        found_tools = []
        
        for tool in self.tools_keywords:
            if tool.lower() in text_lower:
                # Preserve original casing for acronyms
                if tool.isupper():
                    found_tools.append(tool)
                else:
                    found_tools.append(tool.title())
        
        return list(set(found_tools))
    
    def _extract_work_experience(self, text: str) -> List[Dict[str, str]]:
        """Ekstraksi pengalaman kerja"""
        experiences = []
        lines = text.split('\n')
        
        in_experience_section = False
        current_experience = {}
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Detect experience section
            if any(keyword in line_lower for keyword in ['pengalaman kerja', 'work experience', 'professional experience']):
                in_experience_section = True
                continue
            
            # Stop jika ketemu section lain
            if in_experience_section and any(keyword in line_lower for keyword in ['education', 'pendidikan', 'skill', 'project', 'organization']):
                if current_experience:
                    experiences.append(current_experience)
                break
            
            if in_experience_section and line.strip():
                # Coba detect job title dan company
                if '|' in line or '-' in line or 'at' in line_lower:
                    if current_experience:
                        experiences.append(current_experience)
                    
                    # Parse experience entry
                    parts = re.split(r'\||–|—|-|\sat\s', line)
                    current_experience = {
                        'title': parts[0].strip() if len(parts) > 0 else '',
                        'company': parts[1].strip() if len(parts) > 1 else '',
                        'duration': self._extract_duration_from_line(line)
                    }
        
        if current_experience:
            experiences.append(current_experience)
        
        return experiences[:5]  # Max 5 entries
    
    def _extract_organizational_experience(self, text: str) -> List[Dict[str, str]]:
        """Ekstraksi pengalaman organisasi dengan deteksi lebih akurat"""
        experiences = []
        lines = text.split('\n')
        
        in_org_section = False
        skip_next_lines = 0  # Track berapa baris yang harus di-skip (deskripsi)
        
        # Skip keywords untuk filter non-org content
        skip_keywords = ['project', 'skill', 'html', 'css', 'javascript', 'python', 
                        'development', 'api', 'database', 'cloud']
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            line_stripped = line.strip()
            
            # Skip line jika ini adalah deskripsi dari entry sebelumnya
            if skip_next_lines > 0:
                skip_next_lines -= 1
                continue
            
            # Detect organizational section header
            if any(keyword in line_lower for keyword in ['organisasi', 'organization', 'volunteer', 'extracurricular', 'aktivitas']):
                # Pastikan ini header, bukan bagian dari deskripsi
                if len(line_stripped) < 50 and not any(skip in line_lower for skip in skip_keywords):
                    in_org_section = True
                    continue
            
            if in_org_section:
                # Stop jika ketemu section lain (header section)
                if (any(keyword in line_lower for keyword in ['pendidikan', 'education', 'skill', 'keahlian', 
                                                               'pengalaman kerja', 'work experience', 'project'])
                    and len(line_stripped) < 50):
                    break
                
                # Skip baris kosong
                if not line_stripped:
                    continue
                
                # Skip jika technical content
                if any(skip in line_lower for skip in skip_keywords):
                    continue
                
                # Check if this looks like ORGANIZATION TITLE/ROLE (bukan deskripsi)
                is_title_line = (
                    # Ada dash yang menunjukkan format "Role - Organization" atau "Role – Organization Date"
                    (' - ' in line_stripped or ' – ' in line_stripped or ' — ' in line_stripped) or
                    # Huruf pertama kapital dan tidak terlalu panjang
                    (line_stripped[0].isupper() and len(line_stripped) < 150) or
                    # Ada bulan/tahun
                    re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)\s+\d{4}', line_stripped, re.IGNORECASE)
                )
                
                # Check if bukan deskripsi (yang dimulai dengan lowercase atau kata kerja)
                is_not_description = not (
                    line_stripped.lower().startswith(('led ', 'managed', 'organized', 'coordinated', 'and ', 'with '))
                )
                
                if is_title_line and is_not_description and len(line_stripped) > 10:
                    # Ini adalah ORG TITLE/ROLE baru
                    # Parse role dan organization name
                    if '-' in line_stripped or '–' in line_stripped or '—' in line_stripped:
                        parts = re.split(r'\s*[-–—]\s*', line_stripped, maxsplit=1)
                        role = parts[0].strip()
                        org_name = parts[1].strip() if len(parts) > 1 else parts[0].strip()
                    else:
                        role = 'Member'
                        org_name = line_stripped
                    
                    # Ambil deskripsi dari 1-2 baris berikutnya (optional)
                    for j in range(1, 3):
                        if i + j < len(lines):
                            desc_line = lines[i + j].strip()
                            # Stop jika ketemu title baru atau section header
                            if desc_line and not (
                                (' - ' in desc_line or ' – ' in desc_line) or
                                any(kw in desc_line.lower() for kw in ['education', 'skill', 'organization:', 'project'])
                            ):
                                skip_next_lines += 1
                            else:
                                break
                    
                    experiences.append({
                        'organization': org_name[:100],
                        'role': role[:100],
                        'duration': self._extract_duration_from_line(line_stripped)
                    })
                    
                    # Limit untuk menghindari noise
                    if len(experiences) >= 5:
                        break
        
        return experiences[:5]
    
    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Ekstraksi project dengan deteksi lebih akurat"""
        projects = []
        lines = text.split('\n')
        
        in_project_section = False
        skip_next_lines = 0  # Track berapa baris yang harus di-skip (deskripsi)
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            line_stripped = line.strip()
            
            # Skip line jika ini adalah deskripsi dari entry sebelumnya
            if skip_next_lines > 0:
                skip_next_lines -= 1
                continue
            
            # Detect project section header
            if ('project' in line_lower or 'proyek' in line_lower) and len(line_stripped) < 50:
                in_project_section = True
                continue
            
            if in_project_section:
                # Stop jika ketemu section lain (header)
                if (any(keyword in line_lower for keyword in ['pendidikan', 'education', 'skill', 'keahlian',
                                                               'organisasi', 'organization', 'pengalaman kerja', 'work experience'])
                    and len(line_stripped) < 50):
                    break
                
                # Skip baris kosong
                if not line_stripped:
                    continue
                
                # Check if this looks like a PROJECT TITLE (bukan deskripsi)
                # Title biasanya: punya huruf kapital di awal, ada dash/date, atau < 100 char
                is_title_line = (
                    # Ada dash yang menunjukkan format "Title - Date" atau "Title – Date"
                    (' - ' in line_stripped or ' – ' in line_stripped or ' — ' in line_stripped) or
                    # Huruf pertama kapital dan tidak terlalu panjang (< 150 char)
                    (line_stripped[0].isupper() and len(line_stripped) < 150) or
                    # Ada bulan/tahun di akhir (Nov 2025, Dec 2024, dll)
                    re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)\s+\d{4}', line_stripped, re.IGNORECASE)
                )
                
                # Check if bukan deskripsi teknis (yang dimulai dengan lowercase atau kata "Developed")
                is_not_description = not (
                    line_stripped.lower().startswith(('developed', 'built', 'created', 'implemented', 'and ', 'using ', 'with '))
                )
                
                if is_title_line and is_not_description and len(line_stripped) > 15:
                    # Ini adalah PROJECT TITLE baru
                    # Ambil deskripsi dari 1-2 baris berikutnya
                    description_parts = []
                    for j in range(1, 3):
                        if i + j < len(lines):
                            desc_line = lines[i + j].strip()
                            # Stop jika ketemu title baru atau section header
                            if desc_line and not (
                                (' - ' in desc_line or ' – ' in desc_line) or
                                any(kw in desc_line.lower() for kw in ['education', 'skill', 'organization', 'project:'])
                            ):
                                description_parts.append(desc_line)
                                skip_next_lines += 1
                            else:
                                break
                    
                    projects.append({
                        'title': line_stripped[:100],
                        'description': ' '.join(description_parts)[:300]
                    })
                    
                    # Limit untuk menghindari noise
                    if len(projects) >= 5:
                        break
        
        return projects[:5]
    
    def _extract_duration_from_line(self, line: str) -> str:
        """Extract duration dari line text"""
        # Pattern untuk tahun (2020-2023, Jan 2020 - Dec 2023, dll)
        year_patterns = [
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*–\s*(\d{4})',
            r'(\w+\s+\d{4})\s*-\s*(\w+\s+\d{4})',
            r'(\d{4})\s*-\s*(present|now|sekarang)',
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return ""
    
    def _calculate_total_experience(self, work_exp: List[Dict], org_exp: List[Dict]) -> int:
        """Hitung total pengalaman dalam bulan"""
        total_months = 0
        
        # Count work experience (full weight)
        for exp in work_exp:
            duration = exp.get('duration', '')
            months = self._parse_duration_to_months(duration)
            total_months += months
        
        # Count organizational experience (50% weight untuk fresh grad friendly)
        for exp in org_exp:
            duration = exp.get('duration', '')
            months = self._parse_duration_to_months(duration)
            total_months += months * 0.5
        
        return int(total_months)
    
    def _parse_duration_to_months(self, duration_str: str) -> int:
        """Parse duration string ke jumlah bulan"""
        if not duration_str:
            return 0
        
        # Extract years
        year_match = re.search(r'(\d{4})\s*-\s*(\d{4})', duration_str)
        if year_match:
            start_year = int(year_match.group(1))
            end_year = int(year_match.group(2))
            return (end_year - start_year) * 12
        
        # Check for "present" or "now"
        if re.search(r'present|now|sekarang', duration_str, re.IGNORECASE):
            year_match = re.search(r'(\d{4})', duration_str)
            if year_match:
                start_year = int(year_match.group(1))
                current_year = datetime.now().year
                return (current_year - start_year) * 12
        
        return 12  # Default 1 year
    
    def _determine_candidate_level(self, total_months: int, work_exp: List[Dict], education: List[str]) -> str:
        """Determine level kandidat"""
        if total_months < 12:
            return "Fresh Graduate"
        elif total_months < 36:
            return "Junior (1-3 tahun)"
        elif total_months < 72:
            return "Mid Level (3-6 tahun)"
        else:
            return "Senior (6+ tahun)"
    
    def _estimate_job_complexity_fit(self, preview: CVPreview) -> str:
        """Estimasi kompleksitas pekerjaan yang cocok"""
        # Hitung indikator
        has_technical_skills = len(preview.programming_languages) > 2 or len(preview.tools) > 3
        has_experience = preview.total_work_experience_months > 12
        has_leadership = any('lead' in exp.get('title', '').lower() or 'manager' in exp.get('title', '').lower() 
                            for exp in preview.work_experiences)
        
        if has_technical_skills and has_experience and has_leadership:
            return "High"
        elif has_technical_skills or has_experience:
            return "Mid"
        else:
            return "Low-Mid"
    
    def _generate_initial_conclusion(self, preview: CVPreview) -> str:
        """Generate kesimpulan awal"""
        if preview.candidate_level == "Fresh Graduate":
            if len(preview.projects) > 0 or len(preview.organizational_experiences) > 0:
                return "Kandidat fresh graduate dengan pengalaman organisasi/project. Cocok untuk posisi entry-level yang membutuhkan kemampuan belajar cepat."
            else:
                return "Kandidat fresh graduate. Cocok untuk posisi entry-level dengan training."
        elif "Junior" in preview.candidate_level:
            return "Kandidat junior dengan pengalaman kerja awal. Cocok untuk posisi yang membutuhkan kombinasi teori dan praktik."
        elif "Mid" in preview.candidate_level:
            return "Kandidat mid-level dengan pengalaman substansial. Cocok untuk posisi yang membutuhkan kemandirian dan expertise."
        else:
            return "Kandidat senior dengan pengalaman luas. Cocok untuk posisi leadership atau specialist."
    
    def _identify_strengths(self, preview: CVPreview) -> List[str]:
        """Identifikasi kekuatan kandidat"""
        strengths = []
        
        if len(preview.programming_languages) > 3:
            strengths.append(f"Menguasai multiple bahasa pemrograman ({len(preview.programming_languages)} bahasa)")
        
        if len(preview.projects) > 2:
            strengths.append(f"Pengalaman project yang baik ({len(preview.projects)} project)")
        
        if preview.total_work_experience_months > 24:
            years = preview.total_work_experience_months // 12
            strengths.append(f"Pengalaman kerja {years} tahun")
        
        if len(preview.soft_skills) > 5:
            strengths.append("Soft skills yang lengkap")
        
        if preview.linkedin and preview.github:
            strengths.append("Memiliki professional online presence")
        
        if len(preview.organizational_experiences) > 0:
            strengths.append("Pengalaman organisasi/volunteer")
        
        return strengths[:5]
