"""
CV Preview Extractor Module
Ekstraksi dan preview data CV sebelum analisis lengkap
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import pdfplumber
from docx import Document

@dataclass
class CVPreview:
    """Preview data hasil ekstraksi CV"""
    # Basic Info
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    
    # Education
    education_summary: List[str] = field(default_factory=list)
    
    # Skills
    hard_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    programming_languages: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    
    # Experience
    work_experiences: List[Dict[str, str]] = field(default_factory=list)  # {title, company, duration}
    organizational_experiences: List[Dict[str, str]] = field(default_factory=list)
    projects: List[Dict[str, str]] = field(default_factory=list)
    
    # Analysis
    candidate_level: str = "Unknown"  # fresh_graduate / junior / mid / senior
    estimated_job_complexity: str = "mid"  # low / mid / high
    total_work_experience_months: int = 0
    
    # Initial Assessment
    initial_conclusion: str = ""
    strengths: List[str] = field(default_factory=list)
    
    # Raw text for further processing
    raw_text: str = ""

class CVPreviewExtractor:
    """
    Ekstraksi cepat dan akurat dari CV untuk preview sebelum analisis
    """
    
    def __init__(self):
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
        
        # Estimate job complexity suitability
        preview.estimated_job_complexity = self._estimate_job_complexity_fit(preview)
        
        # Generate initial conclusion
        preview.initial_conclusion = self._generate_initial_conclusion(preview)
        preview.strengths = self._identify_strengths(preview)
        
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
        """Ekstraksi pendidikan"""
        education = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            # Cari line yang mengandung education keywords
            if any(keyword in line_lower for keyword in self.education_keywords):
                # Ambil line tersebut dan beberapa line setelahnya
                education_block = ' '.join([l.strip() for l in lines[i:min(i+3, len(lines))] if l.strip()])
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
        """Ekstraksi pengalaman organisasi"""
        experiences = []
        lines = text.split('\n')
        
        in_org_section = False
        
        for line in lines:
            line_lower = line.lower()
            
            # Detect organizational section
            if any(keyword in line_lower for keyword in ['organisasi', 'organization', 'volunteer', 'extracurricular']):
                in_org_section = True
                continue
            
            if in_org_section:
                # Stop jika ketemu section lain
                if any(keyword in line_lower for keyword in ['education', 'pendidikan', 'skill', 'experience', 'pengalaman kerja']):
                    break
                
                if line.strip() and len(line.strip()) > 10:
                    experiences.append({
                        'organization': line.strip()[:100],
                        'role': 'Member/Volunteer',
                        'duration': self._extract_duration_from_line(line)
                    })
        
        return experiences[:5]
    
    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Ekstraksi project"""
        projects = []
        lines = text.split('\n')
        
        in_project_section = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Detect project section
            if 'project' in line_lower or 'proyek' in line_lower:
                in_project_section = True
                continue
            
            if in_project_section:
                # Stop jika ketemu section lain
                if any(keyword in line_lower for keyword in ['education', 'pendidikan', 'skill', 'experience']):
                    break
                
                if line.strip() and len(line.strip()) > 10:
                    # Get project description from next few lines
                    description_lines = []
                    for j in range(i+1, min(i+3, len(lines))):
                        if lines[j].strip():
                            description_lines.append(lines[j].strip())
                    
                    projects.append({
                        'title': line.strip()[:100],
                        'description': ' '.join(description_lines[:2])[:200]
                    })
        
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
