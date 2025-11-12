"""
Enhanced CV Parser - Super Intelligent Extractor
Mendeteksi SEMUA informasi dengan akurasi tinggi
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import dateutil.parser as date_parser


class EnhancedCVParser:
    """Parser CV yang sangat canggih dengan multiple detection strategies"""
    
    def __init__(self):
        # Expanded patterns untuk deteksi maksimal
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'[\w\.-]+@[\w\.-]+\.\w+',
            r'Email\s*:\s*([^\s\n]+@[^\s\n]+)',
            r'E-mail\s*:\s*([^\s\n]+@[^\s\n]+)',
        ]
        
        self.phone_patterns = [
            r'\+?62\s*\d{2,3}\s*\d{3,4}\s*\d{3,4}\s*\d{0,4}',  # Indonesia
            r'\+?\d{1,4}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'(?:Phone|Tel|Mobile|HP|Telp|No\.?\s*HP)\s*:?\s*([\d\s\-\+\(\)]+)',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{4}[-.\s]\d{4}[-.\s]\d{4}',
        ]
        
        self.linkedin_patterns = [
            r'linkedin\.com/in/[\w\-]+',
            r'linkedin\.com/[\w\-/]+',
            r'(?:LinkedIn|Linkedin)\s*:?\s*([\w\-/\.]+)',
            r'in\.linkedin\.com/[\w\-]+',
        ]
        
        self.github_patterns = [
            r'github\.com/[\w\-]+',
            r'(?:GitHub|Github)\s*:?\s*([\w\-/\.]+)',
        ]
        
        self.location_patterns = [
            r'(?:Location|Alamat|Address)\s*:?\s*([^\n\|]+?)(?:\||$)',
            r'(?:Jakarta|Bandung|Surabaya|Yogyakarta|Bali|Medan|Semarang)[^\n]*',
            r'\b\d{5}\s+[A-Z][a-z]+,?\s+[A-Z]{2}\b',  # ZIP code + City, State
        ]
        
        # Name patterns - biasanya di awal CV
        self.name_patterns = [
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\s*$',  # Full name in title case
            r'(?:Name|Nama)\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
        ]
        
        # Date patterns - comprehensive
        self.date_patterns = [
            r'(\d{4})\s*[-–]\s*(\d{4})',
            r'(\d{4})\s*[-–]\s*(Present|Current|Now|Sekarang)',
            r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{4})',
            r'(\d{1,2})/(\d{4})',
            r'(\d{4})/(\d{1,2})',
        ]
        
        # Skills keywords - massive expansion
        self.tech_skills_keywords = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'golang',
            'rust', 'kotlin', 'swift', 'scala', 'perl', 'r', 'matlab', 'dart', 'lua', 'shell',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
            'fastapi', 'spring', 'laravel', 'rails', 'asp.net', 'jquery', 'bootstrap', 'tailwind',
            'webpack', 'babel', 'sass', 'less', 'next.js', 'nuxt.js', 'svelte', 'gatsby',
            
            # Mobile Development
            'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle', 'sql server',
            'sqlite', 'elasticsearch', 'dynamodb', 'couchdb', 'neo4j', 'mariadb', 'firebase',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions',
            'terraform', 'ansible', 'puppet', 'chef', 'circleci', 'travis ci', 'heroku',
            'digital ocean', 'cloudflare', 'netlify', 'vercel',
            
            # Data Science & AI
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
            'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'jupyter', 'nlp', 'opencv',
            'computer vision', 'neural networks', 'data analysis', 'data mining', 'big data',
            
            # Tools & Frameworks
            'git', 'svn', 'jira', 'confluence', 'slack', 'trello', 'asana', 'notion',
            'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator', 'postman', 'swagger',
            
            # Methodologies
            'agile', 'scrum', 'kanban', 'waterfall', 'devops', 'ci/cd', 'tdd', 'bdd',
            'microservices', 'rest api', 'graphql', 'soap', 'oauth', 'jwt',
            
            # Other Technical
            'linux', 'windows', 'macos', 'bash', 'powershell', 'vim', 'vscode', 'intellij',
            'eclipse', 'netbeans', 'apache', 'nginx', 'tomcat', 'iis',
        ]
        
        self.soft_skills_keywords = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
            'critical thinking', 'creativity', 'time management', 'organization',
            'adaptability', 'flexibility', 'collaboration', 'presentation', 'negotiation',
            'conflict resolution', 'decision making', 'strategic thinking', 'innovation',
            'mentoring', 'coaching', 'customer service', 'project management', 'planning',
        ]
        
        # Education degrees - expanded
        self.education_keywords = [
            'bachelor', 'master', 'phd', 'doctor', 'sarjana', 'magister', 'doktor',
            'diploma', 'associate', 's1', 's2', 's3', 'd3', 'd4',
            'b.sc', 'm.sc', 'b.a', 'm.a', 'b.tech', 'm.tech', 'mba', 'b.eng', 'm.eng',
            'undergraduate', 'graduate', 'postgraduate',
        ]
        
        # Job titles - comprehensive
        self.job_titles = [
            'engineer', 'developer', 'programmer', 'analyst', 'manager', 'director',
            'consultant', 'specialist', 'coordinator', 'administrator', 'architect',
            'designer', 'researcher', 'scientist', 'technician', 'lead', 'head',
            'chief', 'officer', 'executive', 'senior', 'junior', 'associate',
            'intern', 'trainee', 'assistant', 'supervisor', 'team lead',
        ]
        
        # Section headers - expanded
        self.section_headers = {
            'summary': ['summary', 'profile', 'about', 'objective', 'ringkasan', 'profil', 
                       'tentang', 'career objective', 'professional summary', 'personal statement'],
            'experience': ['experience', 'work history', 'employment', 'career history',
                          'pengalaman', 'riwayat kerja', 'pekerjaan', 'work experience',
                          'professional experience', 'employment history'],
            'education': ['education', 'academic', 'qualification', 'pendidikan', 'akademik',
                         'riwayat pendidikan', 'educational background', 'academic background'],
            'skills': ['skills', 'competencies', 'expertise', 'technical skills', 'kemampuan',
                      'keahlian', 'kompetensi', 'core competencies', 'areas of expertise'],
            'certifications': ['certifications', 'certificates', 'licenses', 'sertifikat',
                              'sertifikasi', 'lisensi', 'professional certifications'],
            'projects': ['projects', 'portfolio', 'proyek', 'portofolio', 'key projects',
                        'major projects', 'notable projects'],
            'awards': ['awards', 'achievements', 'honors', 'recognition', 'penghargaan',
                      'prestasi', 'accomplishments', 'honors and awards'],
            'languages': ['languages', 'bahasa', 'language proficiency', 'spoken languages'],
            'interests': ['interests', 'hobbies', 'activities', 'minat', 'hobi',
                         'personal interests', 'extracurricular'],
        }
    
    def extract_all_info(self, text: str) -> Dict:
        """
        Extract SEMUA informasi dari CV dengan multiple strategies
        """
        result = {
            'name': self.extract_name(text),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'linkedin': self.extract_linkedin(text),
            'github': self.extract_github(text),
            'location': self.extract_location(text),
            'summary': self.extract_summary(text),
            'experiences': self.extract_experiences(text),
            'education': self.extract_education(text),
            'skills': self.extract_skills(text),
            'certifications': self.extract_certifications(text),
            'projects': self.extract_projects(text),
            'awards': self.extract_awards(text),
            'languages': self.extract_languages(text),
        }
        
        return result
    
    def extract_name(self, text: str) -> str:
        """Extract nama kandidat - biasanya di baris pertama atau bagian atas"""
        lines = text.split('\n')
        
        # Strategy 1: Extract from email username (common pattern)
        email = self.extract_email(text)
        if email:
            username = email.split('@')[0]
            # Convert email username to name (loingaldy -> Loingaldy or Loing Aldy)
            if username:
                # Try to split camelCase or underscore
                parts = re.split(r'[_\.]', username)
                if len(parts) > 1:
                    name = ' '.join(part.capitalize() for part in parts if part)
                    if len(name) > 5:
                        return name
        
        # Strategy 2: First non-empty line yang terlihat seperti nama
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if not line:
                continue
            
            # Skip jika line terlalu panjang atau mengandung keywords umum
            if len(line) > 50 or len(line) < 5:
                continue
            
            skip_keywords = ['curriculum', 'vitae', 'resume', 'cv', 'email', 'phone', 'address', 
                           'tel', 'linkedin', 'github', 'http', 'www', '@']
            if any(kw in line.lower() for kw in skip_keywords):
                continue
            
            # Check if looks like a name (Title Case, 2-4 words)
            words = line.split()
            if 2 <= len(words) <= 4:
                if all(word[0].isupper() for word in words if word and word[0].isalpha()):
                    return line
        
        # Strategy 3: Look for Name: pattern
        for pattern in self.name_patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        # Strategy 4: First line that looks like proper name
        for line in lines[:5]:
            line = line.strip()
            if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+', line):
                # Extract only the name part
                name_match = re.match(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', line)
                if name_match:
                    return name_match.group(1)
        
        # Strategy 5: Look near LinkedIn URL
        linkedin = self.extract_linkedin(text)
        if linkedin and 'linkedin.com/in/' in linkedin:
            username = linkedin.split('linkedin.com/in/')[-1].strip('/').split('/')[-1]
            # Convert username to name
            parts = re.split(r'[-_]', username)
            if parts:
                name = ' '.join(part.capitalize() for part in parts if part)
                if len(name) > 5:
                    return name
        
        return "Unknown"
    
    def extract_email(self, text: str) -> str:
        """Extract email dengan multiple patterns"""
        for pattern in self.email_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Return first valid email
                for match in matches:
                    email = match if isinstance(match, str) else match[0]
                    if '@' in email and '.' in email:
                        return email.strip()
        return ""
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number dengan berbagai format"""
        for pattern in self.phone_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                phone = matches[0]
                if isinstance(phone, tuple):
                    phone = phone[0]
                # Clean up phone number
                phone = re.sub(r'\s+', ' ', str(phone)).strip()
                # Must have at least 7 digits
                digits = re.findall(r'\d', phone)
                if len(digits) >= 7:
                    return phone
        return ""
    
    def extract_linkedin(self, text: str) -> str:
        """Extract LinkedIn profile"""
        for pattern in self.linkedin_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                linkedin = matches[0]
                if isinstance(linkedin, tuple):
                    linkedin = linkedin[0]
                # Normalize URL
                if not linkedin.startswith('http'):
                    linkedin = 'https://' + linkedin.replace('www.', '')
                return linkedin.strip()
        return ""
    
    def extract_github(self, text: str) -> str:
        """Extract GitHub profile"""
        for pattern in self.github_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                github = matches[0]
                if isinstance(github, tuple):
                    github = github[0]
                if not github.startswith('http'):
                    github = 'https://' + github.replace('www.', '')
                return github.strip()
        return ""
    
    def extract_location(self, text: str) -> str:
        """Extract lokasi/alamat"""
        for pattern in self.location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                location = matches[0]
                if isinstance(location, tuple):
                    location = location[0]
                # Limit length and clean
                location = location.strip()
                if len(location) > 100:
                    # Take only first sentence or phrase
                    location = location[:100].split('.')[0].strip()
                if len(location) < 150:  # Reasonable length
                    return location
        
        # Fallback: Look for common Indonesian cities
        cities = ['Jakarta', 'Bandung', 'Surabaya', 'Yogyakarta', 'Bali', 'Medan', 
                 'Semarang', 'Makassar', 'Palembang', 'Denpasar', 'Manado']
        for city in cities:
            # Look for city at start of line or after location keywords
            pattern = rf'(?:Location|Alamat|Address|Domicile)?\s*:?\s*({city}[^\n,\.;]*(?:[,\.;])?)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                # Clean up: remove trailing punctuation and extra text
                location = re.sub(r'[,\.;]\s*$', '', location)
                # Limit to reasonable length
                if len(location) > 50:
                    location = location[:50].split(',')[0].strip()
                return location
            # Simple detection
            elif city in text:
                return city
        
        return ""
    
    def extract_summary(self, text: str) -> str:
        """Extract professional summary/objective"""
        # Find summary section
        for section_type, headers in self.section_headers.items():
            if section_type == 'summary':
                for header in headers:
                    pattern = rf'(?i){header}\s*:?\s*\n(.*?)(?=\n\s*\n|\n[A-Z][A-Za-z\s]+:|\Z)'
                    match = re.search(pattern, text, re.DOTALL)
                    if match:
                        summary = match.group(1).strip()
                        # Clean up
                        summary = re.sub(r'\s+', ' ', summary)
                        return summary[:500]  # Max 500 chars
        
        # Fallback: Get first paragraph after name
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if len(lines) > 3:
            # Skip first few lines (likely name/contact)
            for i in range(3, min(10, len(lines))):
                line = lines[i]
                if len(line) > 100:  # Likely a paragraph
                    return line[:500]
        
        return ""
    
    def extract_experiences(self, text: str) -> List[Dict]:
        """
        Extract work experiences dengan intelligent parsing
        """
        experiences = []
        
        # Find experience section
        exp_section = ""
        for header in self.section_headers['experience']:
            pattern = rf'(?i){header}\s*:?\s*\n(.*?)(?=\n\s*(?:' + '|'.join(self.section_headers['education']) + r')\s*:?|\Z)'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                exp_section = match.group(1)
                break
        
        if not exp_section:
            # Fallback: try to find by job titles
            job_pattern = '|'.join(self.job_titles)
            sections = re.split(rf'\n(?=(?:{job_pattern})\b)', text, flags=re.IGNORECASE)
            if len(sections) > 1:
                exp_section = '\n'.join(sections[1:])
        
        if not exp_section:
            return experiences
        
        # Split into individual experiences
        # Strategy 1: Split by date ranges at start of line
        entries = re.split(r'\n(?=\d{4}\s*[-–]\s*(?:\d{4}|Present|Current))', exp_section)
        
        # Strategy 2: Split by company/position patterns
        if len(entries) <= 1:
            # Look for patterns like: "Company Name | Position" or "Position at Company"
            entries = re.split(r'\n(?=[A-Z][A-Za-z\s&.,Inc]+\s*(?:\||at\s))', exp_section)
        
        for entry in entries:
            if len(entry.strip()) < 30:
                continue
            
            exp_data = self._parse_single_experience(entry)
            if exp_data['position'] or exp_data['company']:
                experiences.append(exp_data)
        
        return experiences
    
    def _parse_single_experience(self, entry: str) -> Dict:
        """Parse single work experience entry"""
        exp = {
            'company': '',
            'position': '',
            'duration': '',
            'start_date': '',
            'end_date': '',
            'years': 0,
            'responsibilities': [],
            'achievements': [],
            'technologies': [],
        }
        
        lines = [l.strip() for l in entry.split('\n') if l.strip()]
        if not lines:
            return exp
        
        # Extract dates
        for date_pattern in self.date_patterns:
            match = re.search(date_pattern, entry, re.IGNORECASE)
            if match:
                exp['duration'] = match.group(0)
                # Parse start and end dates
                try:
                    groups = match.groups()
                    if len(groups) >= 2:
                        exp['start_date'] = groups[0]
                        exp['end_date'] = groups[1] if groups[1] not in ['Present', 'Current', 'Now', 'Sekarang'] else 'Present'
                        
                        # Calculate years
                        start_year = int(re.search(r'\d{4}', exp['start_date']).group(0))
                        if exp['end_date'] == 'Present':
                            end_year = datetime.now().year
                        else:
                            end_year_match = re.search(r'\d{4}', exp['end_date'])
                            end_year = int(end_year_match.group(0)) if end_year_match else start_year
                        
                        exp['years'] = max(0, end_year - start_year)
                except:
                    pass
                break
        
        # Extract company and position
        # Look for patterns: "Position at Company" or "Company | Position"
        first_line = lines[0] if lines else ""
        
        if ' at ' in first_line:
            parts = first_line.split(' at ')
            exp['position'] = parts[0].strip()
            exp['company'] = parts[1].strip()
        elif '|' in first_line:
            parts = first_line.split('|')
            if len(parts) >= 2:
                # Usually: Company | Position or Position | Company
                # Check which part contains job title keywords
                if any(title in parts[0].lower() for title in self.job_titles):
                    exp['position'] = parts[0].strip()
                    exp['company'] = parts[1].strip()
                else:
                    exp['company'] = parts[0].strip()
                    exp['position'] = parts[1].strip()
        else:
            # Assume first line is position or company
            if any(title in first_line.lower() for title in self.job_titles):
                exp['position'] = first_line
                if len(lines) > 1:
                    exp['company'] = lines[1]
            else:
                exp['company'] = first_line
                if len(lines) > 1:
                    exp['position'] = lines[1]
        
        # Extract responsibilities and achievements
        for line in lines[2:]:
            # Skip date lines
            if re.search(r'\d{4}', line):
                continue
            
            # Bullet points or numbered items
            if re.match(r'^[\-\•\*\d\.]', line):
                clean_line = re.sub(r'^[\-\•\*\d\.]\s*', '', line)
                if len(clean_line) > 20:
                    exp['responsibilities'].append(clean_line)
            elif len(line) > 30:
                exp['responsibilities'].append(line)
        
        # Extract technologies mentioned
        for skill in self.tech_skills_keywords:
            if re.search(rf'\b{skill}\b', entry, re.IGNORECASE):
                if skill not in exp['technologies']:
                    exp['technologies'].append(skill)
        
        return exp
    
    def extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        education_list = []
        
        # Find education section
        edu_section = ""
        for header in self.section_headers['education']:
            pattern = rf'(?i){header}\s*:?\s*\n(.*?)(?=\n\s*(?:' + '|'.join(self.section_headers['skills']) + r')\s*:?|\Z)'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                edu_section = match.group(1)
                break
        
        if not edu_section:
            return education_list
        
        # Split by degree keywords or years
        entries = re.split(r'\n(?=(?:' + '|'.join(self.education_keywords) + r'))', edu_section, flags=re.IGNORECASE)
        
        if len(entries) <= 1:
            entries = re.split(r'\n(?=\d{4}\s*[-–])', edu_section)
        
        for entry in entries:
            if len(entry.strip()) < 20:
                continue
            
            edu_data = self._parse_single_education(entry)
            if edu_data['degree'] or edu_data['institution']:
                education_list.append(edu_data)
        
        return education_list
    
    def _parse_single_education(self, entry: str) -> Dict:
        """Parse single education entry"""
        edu = {
            'institution': '',
            'degree': '',
            'field': '',
            'year': '',
            'gpa': '',
        }
        
        lines = [l.strip() for l in entry.split('\n') if l.strip()]
        if not lines:
            return edu
        
        # Extract degree
        for keyword in self.education_keywords:
            if keyword.lower() in entry.lower():
                pattern = rf'(?i)({keyword}[^\n,\|]*)'
                match = re.search(pattern, entry)
                if match:
                    edu['degree'] = match.group(1).strip()
                    break
        
        # Extract institution (usually a proper noun)
        for line in lines:
            # Look for university/institut/college keywords
            if any(inst in line.lower() for inst in ['university', 'universitas', 'institut', 'college', 'school']):
                edu['institution'] = line
                break
        
        if not edu['institution']:
            # Assume first line or line with proper nouns
            for line in lines[:3]:
                if line[0].isupper() and len(line) > 5:
                    edu['institution'] = line
                    break
        
        # Extract year
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', entry)
        if years:
            edu['year'] = years[-1]  # Usually graduation year is last
        
        # Extract GPA
        gpa_match = re.search(r'GPA\s*:?\s*([\d\.]+)', entry, re.IGNORECASE)
        if gpa_match:
            edu['gpa'] = gpa_match.group(1)
        
        # Extract field of study
        common_fields = ['computer science', 'engineering', 'business', 'management', 
                        'information technology', 'mathematics', 'physics']
        for field in common_fields:
            if field in entry.lower():
                edu['field'] = field.title()
                break
        
        return edu
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract technical and soft skills"""
        skills = {
            'technical': [],
            'soft': [],
            'languages': [],
            'tools': [],
        }
        
        # Technical skills
        for skill in self.tech_skills_keywords:
            # Escape special regex characters
            skill_escaped = re.escape(skill)
            if re.search(rf'\b{skill_escaped}\b', text, re.IGNORECASE):
                # Capitalize properly
                skill_formatted = skill.upper() if len(skill) <= 4 else skill.title()
                if skill_formatted not in skills['technical']:
                    skills['technical'].append(skill_formatted)
        
        # Soft skills
        for skill in self.soft_skills_keywords:
            skill_escaped = re.escape(skill)
            if re.search(rf'\b{skill_escaped}\b', text, re.IGNORECASE):
                if skill.title() not in skills['soft']:
                    skills['soft'].append(skill.title())
        
        # Programming languages (subset of technical)
        prog_langs = ['Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'PHP', 
                     'Ruby', 'Go', 'Rust', 'Kotlin', 'Swift', 'Scala']
        skills['languages'] = [lang for lang in prog_langs if lang.lower() in text.lower()]
        
        return skills
    
    def extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certs = []
        
        # Find certification section
        for header in self.section_headers['certifications']:
            pattern = rf'(?i){header}\s*:?\s*\n(.*?)(?=\n\s*[A-Z][A-Za-z\s]+:|\Z)'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                cert_section = match.group(1)
                # Split by lines or bullet points
                lines = [l.strip() for l in cert_section.split('\n') if l.strip()]
                for line in lines:
                    # Remove bullet points
                    clean_line = re.sub(r'^[\-\•\*\d\.]\s*', '', line)
                    if len(clean_line) > 5:
                        certs.append(clean_line)
                break
        
        return certs
    
    def extract_projects(self, text: str) -> List[Dict]:
        """Extract projects"""
        projects = []
        
        # Find projects section
        for header in self.section_headers['projects']:
            pattern = rf'(?i){header}\s*:?\s*\n(.*?)(?=\n\s*[A-Z][A-Za-z\s]+:|\Z)'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                proj_section = match.group(1)
                # Split into individual projects
                entries = re.split(r'\n(?=[A-Z][^\n]{20,})', proj_section)
                
                for entry in entries:
                    if len(entry.strip()) < 30:
                        continue
                    
                    lines = [l.strip() for l in entry.split('\n') if l.strip()]
                    if lines:
                        project = {
                            'name': lines[0],
                            'description': ' '.join(lines[1:]) if len(lines) > 1 else '',
                        }
                        projects.append(project)
                break
        
        return projects
    
    def extract_awards(self, text: str) -> List[str]:
        """Extract awards and achievements"""
        awards = []
        
        for header in self.section_headers['awards']:
            pattern = rf'(?i){header}\s*:?\s*\n(.*?)(?=\n\s*[A-Z][A-Za-z\s]+:|\Z)'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                award_section = match.group(1)
                lines = [l.strip() for l in award_section.split('\n') if l.strip()]
                for line in lines:
                    clean_line = re.sub(r'^[\-\•\*\d\.]\s*', '', line)
                    if len(clean_line) > 5:
                        awards.append(clean_line)
                break
        
        return awards
    
    def extract_languages(self, text: str) -> List[Dict]:
        """Extract language proficiency"""
        languages = []
        
        # Common languages
        common_langs = {
            'English': ['english', 'inggris'],
            'Indonesian': ['indonesian', 'indonesia', 'bahasa indonesia'],
            'Mandarin': ['mandarin', 'chinese'],
            'Japanese': ['japanese', 'jepang'],
            'Korean': ['korean', 'korea'],
            'Spanish': ['spanish', 'spanyol'],
            'French': ['french', 'perancis'],
            'German': ['german', 'jerman'],
        }
        
        proficiency_keywords = ['native', 'fluent', 'advanced', 'intermediate', 'basic', 
                               'professional', 'conversational']
        
        for lang_name, keywords in common_langs.items():
            for keyword in keywords:
                if re.search(rf'\b{keyword}\b', text, re.IGNORECASE):
                    # Try to find proficiency level
                    pattern = rf'{keyword}\s*[-:,]?\s*({"|".join(proficiency_keywords)})?'
                    match = re.search(pattern, text, re.IGNORECASE)
                    level = match.group(1) if match and match.group(1) else 'Proficient'
                    
                    languages.append({
                        'language': lang_name,
                        'proficiency': level.title()
                    })
                    break
        
        return languages
    
    def calculate_experience_years(self, experiences: List[Dict]) -> float:
        """Calculate total years of experience"""
        total_years = 0
        for exp in experiences:
            total_years += exp.get('years', 0)
        return total_years
