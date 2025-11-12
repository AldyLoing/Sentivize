"""
CV/Resume Analyzer Module - Analisis CV berdasarkan kriteria custom
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple
import PyPDF2
import docx
import re
from pathlib import Path
import config
from ai_analyzer import get_analyzer


class CVAnalyzer:
    """
    Class untuk menganalisis CV/Resume berdasarkan kriteria
    """
    
    def __init__(self, use_mock_models: bool = False):
        """Initialize CV analyzer dengan AI models"""
        self.analyzer = get_analyzer(use_mock_models=use_mock_models)
        self.use_mock = use_mock_models
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """
        Extract text dari PDF file
        
        Args:
            pdf_file: File object (UploadedFile atau path)
            
        Returns:
            str: Extracted text
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_parts = []
            
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            return "\n".join(text_parts)
        except Exception as e:
            print(f"Error extracting PDF: {str(e)}")
            return ""
    
    def extract_text_from_docx(self, docx_file) -> str:
        """
        Extract text dari DOCX file
        
        Args:
            docx_file: File object
            
        Returns:
            str: Extracted text
        """
        try:
            doc = docx.Document(docx_file)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            return "\n".join(text_parts)
        except Exception as e:
            print(f"Error extracting DOCX: {str(e)}")
            return ""
    
    def extract_text_from_txt(self, txt_file) -> str:
        """
        Extract text dari TXT file
        
        Args:
            txt_file: File object
            
        Returns:
            str: Extracted text
        """
        try:
            return txt_file.read().decode('utf-8')
        except UnicodeDecodeError:
            try:
                txt_file.seek(0)
                return txt_file.read().decode('latin-1')
            except Exception as e:
                print(f"Error extracting TXT: {str(e)}")
                return ""
    
    def extract_cv_text(self, uploaded_file) -> Tuple[str, str]:
        """
        Extract text dari CV file (PDF, DOCX, atau TXT)
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Tuple[str, str]: (extracted_text, file_type)
        """
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            text = self.extract_text_from_pdf(uploaded_file)
            return text, 'PDF'
        elif file_extension == 'docx':
            text = self.extract_text_from_docx(uploaded_file)
            return text, 'DOCX'
        elif file_extension == 'txt':
            text = self.extract_text_from_txt(uploaded_file)
            return text, 'TXT'
        else:
            raise ValueError(f"Format file tidak didukung: {file_extension}")
    
    def extract_cv_sections(self, text: str) -> Dict[str, str]:
        """
        Extract common CV sections (nama, email, phone, pendidikan, pengalaman, skills)
        
        Args:
            text: CV text
            
        Returns:
            Dict dengan sections
        """
        sections = {
            'nama': '',
            'email': '',
            'phone': '',
            'pendidikan': '',
            'pengalaman': '',
            'skills': '',
            'full_text': text
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            sections['email'] = emails[0]
        
        # Extract phone
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            sections['phone'] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
        
        # Extract name (assume first non-empty line with reasonable length)
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if 5 < len(line) < 50 and not re.search(email_pattern, line):
                # Likely a name
                if not any(keyword in line.lower() for keyword in ['curriculum', 'vitae', 'resume', 'cv']):
                    sections['nama'] = line
                    break
        
        # Extract sections by keywords
        text_lower = text.lower()
        
        # Pendidikan section
        pendidikan_keywords = ['pendidikan', 'education', 'riwayat pendidikan', 'educational background']
        for keyword in pendidikan_keywords:
            if keyword in text_lower:
                start_idx = text_lower.find(keyword)
                # Find next section or end
                next_section_keywords = ['pengalaman', 'experience', 'skills', 'kemampuan', 'sertifikat']
                end_idx = len(text)
                for next_kw in next_section_keywords:
                    next_idx = text_lower.find(next_kw, start_idx + len(keyword))
                    if next_idx != -1 and next_idx < end_idx:
                        end_idx = next_idx
                
                sections['pendidikan'] = text[start_idx:end_idx].strip()
                break
        
        # Pengalaman section
        pengalaman_keywords = ['pengalaman', 'experience', 'work experience', 'riwayat pekerjaan', 'work history']
        for keyword in pengalaman_keywords:
            if keyword in text_lower:
                start_idx = text_lower.find(keyword)
                next_section_keywords = ['pendidikan', 'education', 'skills', 'kemampuan', 'sertifikat']
                end_idx = len(text)
                for next_kw in next_section_keywords:
                    next_idx = text_lower.find(next_kw, start_idx + len(keyword))
                    if next_idx != -1 and next_idx < end_idx:
                        end_idx = next_idx
                
                sections['pengalaman'] = text[start_idx:end_idx].strip()
                break
        
        # Skills section
        skills_keywords = ['skills', 'kemampuan', 'keahlian', 'competencies', 'technical skills']
        for keyword in skills_keywords:
            if keyword in text_lower:
                start_idx = text_lower.find(keyword)
                next_section_keywords = ['pendidikan', 'education', 'pengalaman', 'experience', 'sertifikat']
                end_idx = len(text)
                for next_kw in next_section_keywords:
                    next_idx = text_lower.find(next_kw, start_idx + len(keyword))
                    if next_idx != -1 and next_idx < end_idx:
                        end_idx = next_idx
                
                sections['skills'] = text[start_idx:end_idx].strip()
                break
        
        return sections
    
    def analyze_cv_against_criteria(
        self, 
        cv_text: str, 
        criteria: str,
        cv_sections: Optional[Dict[str, str]] = None
    ) -> Dict:
        """
        Analisis CV berdasarkan kriteria yang diberikan
        
        Args:
            cv_text: Full CV text
            criteria: Kriteria pencarian (kata kunci atau kalimat)
            cv_sections: Optional extracted sections
            
        Returns:
            Dict hasil analisis
        """
        # Calculate relevance dengan reasoning
        relevance_score, relevance_reasoning = self.analyzer.calculate_relevance_with_reasoning(
            texts=[cv_text],
            keyword=criteria,
            name=cv_sections.get('nama', 'Unknown') if cv_sections else 'Unknown',
            position=None,
            unit=None
        )
        
        # Analyze sentiment dari CV tone
        sentiment_label, sentiment_score = self.analyzer.analyze_sentiment([cv_text[:2000]])  # First 2000 chars
        
        # Extract matched keywords/phrases
        matches = self._find_criteria_matches(cv_text, criteria)
        
        # Calculate section-wise scores
        section_scores = {}
        if cv_sections:
            for section_name, section_text in cv_sections.items():
                if section_name not in ['nama', 'email', 'phone', 'full_text'] and section_text:
                    section_score = self.analyzer.calculate_relevance([section_text], criteria)
                    section_scores[section_name] = round(section_score, 3)
        
        return {
            'relevance_score': round(relevance_score, 3),
            'relevance_reasoning': relevance_reasoning,
            'sentiment_label': sentiment_label,
            'sentiment_score': round(sentiment_score, 3),
            'matches': matches,
            'section_scores': section_scores,
            'nama': cv_sections.get('nama', 'Unknown') if cv_sections else 'Unknown',
            'email': cv_sections.get('email', '-') if cv_sections else '-',
            'phone': cv_sections.get('phone', '-') if cv_sections else '-'
        }
    
    def _find_criteria_matches(self, text: str, criteria: str) -> Dict[str, List[str]]:
        """
        Find where criteria appears in text
        
        Args:
            text: CV text
            criteria: Search criteria
            
        Returns:
            Dict dengan matched phrases dan contexts
        """
        text_lower = text.lower()
        criteria_lower = criteria.lower()
        
        matches = {
            'exact_phrases': [],
            'related_words': [],
            'contexts': []
        }
        
        # Find exact phrase matches
        if criteria_lower in text_lower:
            # Find all occurrences with context
            start = 0
            while True:
                idx = text_lower.find(criteria_lower, start)
                if idx == -1:
                    break
                
                # Get context (50 chars before and after)
                context_start = max(0, idx - 50)
                context_end = min(len(text), idx + len(criteria) + 50)
                context = text[context_start:context_end].strip()
                
                matches['exact_phrases'].append(criteria)
                matches['contexts'].append(f"...{context}...")
                
                start = idx + 1
        
        # Find individual words
        words = criteria_lower.split()
        for word in words:
            if len(word) > 3:  # Skip short words
                if word in text_lower and word not in matches['related_words']:
                    matches['related_words'].append(word)
        
        return matches
    
    def analyze_multiple_cvs(
        self,
        cv_files: List,
        criteria: str,
        progress_callback=None
    ) -> pd.DataFrame:
        """
        Analyze multiple CV files against criteria
        
        Args:
            cv_files: List of uploaded files
            criteria: Search criteria
            progress_callback: Progress callback function
            
        Returns:
            DataFrame with analysis results
        """
        results = []
        total = len(cv_files)
        
        for idx, cv_file in enumerate(cv_files):
            try:
                if progress_callback:
                    progress_callback(idx + 1, total)
                
                # Extract text
                cv_text, file_type = self.extract_cv_text(cv_file)
                
                if not cv_text or len(cv_text) < 50:
                    print(f"⚠️ File {cv_file.name}: Text terlalu pendek atau kosong")
                    continue
                
                # Extract sections
                cv_sections = self.extract_cv_sections(cv_text)
                
                # Analyze
                analysis = self.analyze_cv_against_criteria(cv_text, criteria, cv_sections)
                
                # Compile result
                result = {
                    'File Name': cv_file.name,
                    'File Type': file_type,
                    'Nama Kandidat': analysis['nama'],
                    'Email': analysis['email'],
                    'Phone': analysis['phone'],
                    'Relevance Score': analysis['relevance_score'],
                    'Relevance Reasoning': analysis['relevance_reasoning'],
                    'Sentiment Label': analysis['sentiment_label'],
                    'Sentiment Score': analysis['sentiment_score'],
                    'Exact Matches': len(analysis['matches']['exact_phrases']),
                    'Related Words': ', '.join(analysis['matches']['related_words'][:10]),
                    'Match Contexts': ' | '.join(analysis['matches']['contexts'][:3]),
                    'CV Length': len(cv_text),
                    **{f'Score_{k.title()}': v for k, v in analysis['section_scores'].items()}
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"❌ Error processing {cv_file.name}: {str(e)}")
                continue
        
        if not results:
            raise ValueError("Tidak ada CV yang berhasil dianalisis!")
        
        # Create DataFrame and sort by relevance
        df = pd.DataFrame(results)
        df = df.sort_values('Relevance Score', ascending=False).reset_index(drop=True)
        
        return df


def get_cv_analyzer(use_mock_models: bool = False) -> CVAnalyzer:
    """
    Get CV analyzer instance
    
    Args:
        use_mock_models: Whether to use mock models
        
    Returns:
        CVAnalyzer instance
    """
    return CVAnalyzer(use_mock_models=use_mock_models)
