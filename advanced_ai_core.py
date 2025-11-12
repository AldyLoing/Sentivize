"""
Advanced AI Core - Deep Learning & NLP Engine untuk Analisis HR
Sistem AI yang memahami konteks, makna, dan relasi data secara mendalam
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Any
import re
from dataclasses import dataclass
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


@dataclass
class AnalysisInsight:
    """Struktur data untuk insight analisis"""
    category: str
    score: float
    evidence: List[str]
    reasoning: str
    confidence: float


@dataclass
class PersonalityProfile:
    """Profile kepribadian kandidat"""
    traits: Dict[str, float]  # leadership, creativity, analytical, etc.
    behavior_patterns: List[str]
    social_presence: str  # active, moderate, passive
    professional_tone: str  # formal, casual, balanced
    key_interests: List[str]
    communication_style: str


class AdvancedNLPEngine:
    """
    Advanced NLP Engine dengan kemampuan:
    - Named Entity Recognition (NER)
    - Topic Modeling
    - Semantic Understanding
    - Contextual Reasoning
    """
    
    def __init__(self, use_mock_models: bool = False):
        self.use_mock_models = use_mock_models
        self.ner_model = None
        self.topic_model = None
        self.sentence_transformer = None
        self.zero_shot_classifier = None
        
        if not use_mock_models:
            self._load_advanced_models()
        else:
            self._load_mock_engines()
    
    def _load_advanced_models(self):
        """Load advanced transformer models"""
        try:
            from transformers import pipeline, AutoTokenizer, AutoModel
            from sentence_transformers import SentenceTransformer
            import torch
            
            print("🚀 Loading Advanced AI Models...")
            
            # 1. Sentence Transformer untuk semantic similarity
            try:
                self.sentence_transformer = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
                print("✓ Loaded Sentence Transformer (mpnet)")
            except:
                self.sentence_transformer = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                print("✓ Loaded Sentence Transformer (MiniLM)")
            
            # 2. Zero-shot classifier untuk topic classification
            try:
                self.zero_shot_classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=-1
                )
                print("✓ Loaded Zero-Shot Classifier")
            except Exception as e:
                print(f"⚠️ Zero-shot classifier not available: {e}")
            
            # 3. NER Model untuk entity extraction
            try:
                self.ner_model = pipeline(
                    "ner",
                    model="dslim/bert-base-NER",
                    aggregation_strategy="simple",
                    device=-1
                )
                print("✓ Loaded NER Model")
            except Exception as e:
                print(f"⚠️ NER model not available: {e}")
            
            print("✅ Advanced AI Models Ready!")
            
        except Exception as e:
            print(f"⚠️ Error loading advanced models: {e}")
            print("Falling back to mock engines...")
            self.use_mock_models = True
            self._load_mock_engines()
    
    def _load_mock_engines(self):
        """Load mock/lightweight engines"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            from sklearn.decomposition import LatentDirichletAllocation
            
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 3),
                stop_words='english'
            )
            self.lda_model = None  # Will be fit on demand
            
            print("✓ Loaded Mock NLP Engines (TF-IDF + LDA)")
            
        except Exception as e:
            print(f"Error loading mock engines: {e}")
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities: organizations, locations, skills, etc.
        
        Args:
            text: Input text
            
        Returns:
            Dict dengan entities yang terdeteksi
        """
        entities = {
            'organizations': [],
            'locations': [],
            'persons': [],
            'skills': [],
            'education': [],
            'certifications': []
        }
        
        if not text or len(text.strip()) == 0:
            return entities
        
        if not self.use_mock_models and self.ner_model:
            return self._extract_entities_advanced(text)
        else:
            return self._extract_entities_rule_based(text)
    
    def _extract_entities_advanced(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using NER model"""
        try:
            ner_results = self.ner_model(text[:2000])  # Limit text length
            
            entities = {
                'organizations': [],
                'locations': [],
                'persons': [],
                'skills': [],
                'education': [],
                'certifications': []
            }
            
            for entity in ner_results:
                entity_type = entity['entity_group']
                entity_text = entity['word']
                
                if entity_type == 'ORG':
                    entities['organizations'].append(entity_text)
                elif entity_type == 'LOC':
                    entities['locations'].append(entity_text)
                elif entity_type == 'PER':
                    entities['persons'].append(entity_text)
            
            # Complement with rule-based extraction
            rule_entities = self._extract_entities_rule_based(text)
            entities['skills'] = rule_entities['skills']
            entities['education'] = rule_entities['education']
            entities['certifications'] = rule_entities['certifications']
            
            return entities
            
        except Exception as e:
            print(f"Error in advanced entity extraction: {e}")
            return self._extract_entities_rule_based(text)
    
    def _extract_entities_rule_based(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using rule-based patterns"""
        entities = {
            'organizations': [],
            'locations': [],
            'persons': [],
            'skills': [],
            'education': [],
            'certifications': []
        }
        
        text_lower = text.lower()
        
        # Skills patterns (comprehensive list)
        skill_keywords = [
            # Programming
            'python', 'java', 'javascript', 'typescript', 'c\\+\\+', 'c#', 'php', 'ruby', 'go', 'rust',
            'react', 'vue', 'angular', 'node\\.?js', 'django', 'flask', 'spring', 'laravel',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'ci/cd',
            
            # Data Science / ML
            'machine learning', 'deep learning', 'ai', 'artificial intelligence',
            'data science', 'data analysis', 'data analyst', 'data engineer',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
            'nlp', 'computer vision', 'neural network',
            
            # Business / Soft Skills
            'leadership', 'management', 'project management', 'agile', 'scrum',
            'communication', 'teamwork', 'problem solving', 'critical thinking',
            'strategic planning', 'business development', 'sales', 'marketing',
            'digital marketing', 'seo', 'sem', 'social media',
            
            # Design
            'ui/ux', 'ui design', 'ux design', 'graphic design', 'web design',
            'figma', 'adobe', 'photoshop', 'illustrator', 'sketch',
            
            # Languages
            'bahasa inggris', 'english', 'mandarin', 'japanese', 'bilingual', 'multilingual'
        ]
        
        for skill in skill_keywords:
            pattern = r'\b' + skill + r'\b'
            if re.search(pattern, text_lower):
                skill_formatted = skill.replace('\\', '').replace('.', '').replace('?', '')
                if skill_formatted not in entities['skills']:
                    entities['skills'].append(skill_formatted.title())
        
        # Education patterns
        education_patterns = [
            r'\b(S[1-3]|D[1-4]|bachelor|master|phd|doctoral|sarjana|magister|doktor)\b',
            r'\b(universitas|university|institut|institute|politeknik|polytechnic)\s+\w+',
            r'\b(IPK|GPA)\s*:?\s*[\d.]+',
        ]
        
        for pattern in education_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                edu_text = match.group(0)
                if edu_text not in entities['education']:
                    entities['education'].append(edu_text)
        
        # Certification patterns
        cert_keywords = [
            'certified', 'certification', 'sertifikat', 'sertifikasi',
            'pmp', 'cissp', 'aws certified', 'google certified', 'microsoft certified',
            'oracle certified', 'cisco certified', 'comptia'
        ]
        
        for keyword in cert_keywords:
            pattern = r'\b' + keyword + r'[^.!?\n]{0,50}'
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                cert_text = match.group(0).strip()
                if cert_text and cert_text not in entities['certifications']:
                    entities['certifications'].append(cert_text.title())
        
        # Organizations (companies)
        org_indicators = ['PT', 'CV', 'Corp', 'Corporation', 'Inc', 'Ltd', 'Tbk', 'Company']
        for indicator in org_indicators:
            pattern = r'\b' + indicator + r'\s+[\w\s]+\b'
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                org_text = match.group(0).strip()
                if org_text not in entities['organizations']:
                    entities['organizations'].append(org_text)
        
        # Locations (cities in Indonesia and major world cities)
        locations = [
            'Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang', 'Makassar', 'Palembang',
            'Singapore', 'Malaysia', 'Bangkok', 'Manila', 'Hong Kong',
            'New York', 'London', 'Sydney', 'Tokyo', 'Shanghai'
        ]
        
        for location in locations:
            if location.lower() in text_lower:
                if location not in entities['locations']:
                    entities['locations'].append(location)
        
        return entities
    
    def extract_semantic_topics(self, text: str, num_topics: int = 5) -> List[Tuple[str, float]]:
        """
        Extract main topics dari text menggunakan topic modeling
        
        Args:
            text: Input text
            num_topics: Number of topics to extract
            
        Returns:
            List of (topic_label, score) tuples
        """
        if not text or len(text.strip()) < 50:
            return []
        
        if not self.use_mock_models and self.zero_shot_classifier:
            return self._extract_topics_zero_shot(text)
        else:
            return self._extract_topics_tfidf(text, num_topics)
    
    def _extract_topics_zero_shot(self, text: str) -> List[Tuple[str, float]]:
        """Extract topics using zero-shot classification"""
        try:
            candidate_labels = [
                "teknologi dan programming",
                "kepemimpinan dan manajemen",
                "data science dan AI",
                "bisnis dan marketing",
                "desain dan kreativitas",
                "komunikasi dan kolaborasi",
                "pendidikan dan pembelajaran",
                "lingkungan dan keberlanjutan",
                "kesehatan dan wellness",
                "sosial dan kemasyarakatan"
            ]
            
            result = self.zero_shot_classifier(
                text[:1000],  # Limit text
                candidate_labels,
                multi_label=True
            )
            
            topics = list(zip(result['labels'], result['scores']))
            return topics[:5]  # Top 5 topics
            
        except Exception as e:
            print(f"Error in zero-shot topic extraction: {e}")
            return self._extract_topics_tfidf(text, 5)
    
    def _extract_topics_tfidf(self, text: str, num_topics: int) -> List[Tuple[str, float]]:
        """Extract topics using TF-IDF (mock approach)"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            
            # Create sentences
            sentences = text.split('.')
            sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
            
            if len(sentences) < 3:
                return []
            
            vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Get top terms
            feature_names = vectorizer.get_feature_names_out()
            avg_tfidf = tfidf_matrix.mean(axis=0).A1
            
            top_indices = avg_tfidf.argsort()[-num_topics:][::-1]
            topics = [(feature_names[i], float(avg_tfidf[i])) for i in top_indices]
            
            return topics
            
        except Exception as e:
            print(f"Error in TF-IDF topic extraction: {e}")
            return []
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity antara dua teks
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            float: Similarity score (0-1)
        """
        if not text1 or not text2:
            return 0.0
        
        if not self.use_mock_models and self.sentence_transformer:
            return self._calculate_similarity_transformers(text1, text2)
        else:
            return self._calculate_similarity_tfidf(text1, text2)
    
    def _calculate_similarity_transformers(self, text1: str, text2: str) -> float:
        """Calculate similarity using sentence transformers"""
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            
            embeddings = self.sentence_transformer.encode([text1[:512], text2[:512]])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            
            return float(max(0.0, min(1.0, similarity)))
            
        except Exception as e:
            print(f"Error in transformer similarity: {e}")
            return self._calculate_similarity_tfidf(text1, text2)
    
    def _calculate_similarity_tfidf(self, text1: str, text2: str) -> float:
        """Calculate similarity using TF-IDF"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            vectorizer = TfidfVectorizer()
            tfidf = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            
            return float(max(0.0, min(1.0, similarity)))
            
        except Exception as e:
            print(f"Error in TF-IDF similarity: {e}")
            return 0.0


class ContextualReasoningEngine:
    """
    Engine untuk contextual reasoning - memahami makna tersirat dan konteks
    """
    
    def __init__(self, nlp_engine: AdvancedNLPEngine):
        self.nlp_engine = nlp_engine
    
    def analyze_experience_depth(self, text: str) -> Dict[str, Any]:
        """
        Analisis kedalaman pengalaman dari text
        
        Returns:
            Dict dengan duration, responsibility_level, impact, dll
        """
        analysis = {
            'years_of_experience': 0,
            'responsibility_level': 'entry',  # entry, mid, senior, lead, executive
            'impact_indicators': [],
            'leadership_indicators': [],
            'technical_depth': 'basic',  # basic, intermediate, advanced, expert
            'reasoning': ''
        }
        
        text_lower = text.lower()
        
        # Extract years of experience
        year_patterns = [
            r'(\d+)\s*tahun',
            r'(\d+)\s*years?',
            r'(\d+)\+\s*years?',
            r'(\d{4})\s*-\s*(\d{4})',  # Date ranges
            r'(\d{4})\s*-\s*(present|now|sekarang)',
        ]
        
        years_found = []
        for pattern in year_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                if len(match.groups()) == 1:
                    years_found.append(int(match.group(1)))
                elif len(match.groups()) == 2:
                    try:
                        start = int(match.group(1))
                        end = match.group(2)
                        if end.isdigit():
                            years_found.append(int(end) - start)
                        else:
                            years_found.append(datetime.now().year - start)
                    except:
                        pass
        
        if years_found:
            analysis['years_of_experience'] = max(years_found)
        
        # Responsibility level indicators
        level_keywords = {
            'executive': ['ceo', 'cto', 'cfo', 'coo', 'vp', 'vice president', 'director', 'direktur'],
            'lead': ['lead', 'head of', 'principal', 'kepala', 'manager', 'manajer'],
            'senior': ['senior', 'sr.', 'staff', 'specialist', 'expert', 'architect'],
            'mid': ['associate', 'engineer', 'analyst', 'developer', 'designer'],
            'entry': ['junior', 'jr.', 'assistant', 'intern', 'trainee']
        }
        
        for level, keywords in level_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                analysis['responsibility_level'] = level
                break
        
        # Impact indicators
        impact_keywords = [
            'led team', 'memimpin tim', 'managed', 'mengelola',
            'increased', 'meningkatkan', 'improved', 'memperbaiki',
            'reduced cost', 'mengurangi biaya', 'saved', 'menghemat',
            'launched', 'meluncurkan', 'built', 'membangun',
            'scaled', 'mengembangkan', 'optimized', 'mengoptimalkan',
            'revenue', 'pendapatan', 'profit', 'keuntungan',
            'growth', 'pertumbuhan', 'success', 'sukses'
        ]
        
        for keyword in impact_keywords:
            if keyword in text_lower:
                # Find context around keyword
                pattern = r'.{0,50}' + re.escape(keyword) + r'.{0,50}'
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    context = match.group(0).strip()
                    if context not in analysis['impact_indicators']:
                        analysis['impact_indicators'].append(context)
        
        # Leadership indicators
        leadership_keywords = [
            'led', 'memimpin', 'managed', 'mengelola', 'supervised', 'mengawasi',
            'mentored', 'membimbing', 'coached', 'melatih',
            'team of', 'tim sebanyak', 'cross-functional', 'lintas departemen',
            'stakeholder', 'pemangku kepentingan', 'client', 'klien'
        ]
        
        for keyword in leadership_keywords:
            if keyword in text_lower:
                pattern = r'.{0,50}' + re.escape(keyword) + r'.{0,50}'
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    context = match.group(0).strip()
                    if context not in analysis['leadership_indicators']:
                        analysis['leadership_indicators'].append(context)
        
        # Technical depth assessment
        technical_indicators = {
            'expert': ['expert', 'ahli', 'specialist', 'spesialis', 'architect', 'arsitek', 'deep knowledge'],
            'advanced': ['advanced', 'lanjut', 'proficient', 'mahir', 'extensive experience', 'pengalaman luas'],
            'intermediate': ['intermediate', 'menengah', 'working knowledge', 'familiar', 'experienced'],
            'basic': ['basic', 'dasar', 'fundamental', 'beginner', 'learning']
        }
        
        for level, keywords in technical_indicators.items():
            if any(keyword in text_lower for keyword in keywords):
                analysis['technical_depth'] = level
                break
        
        # Generate reasoning
        reasoning_parts = []
        
        if analysis['years_of_experience'] > 0:
            reasoning_parts.append(f"Pengalaman {analysis['years_of_experience']} tahun")
        
        reasoning_parts.append(f"Level: {analysis['responsibility_level']}")
        
        if analysis['leadership_indicators']:
            reasoning_parts.append(f"Indikasi kepemimpinan: {len(analysis['leadership_indicators'])} bukti")
        
        if analysis['impact_indicators']:
            reasoning_parts.append(f"Dampak terukur: {len(analysis['impact_indicators'])} indikator")
        
        reasoning_parts.append(f"Kedalaman teknis: {analysis['technical_depth']}")
        
        analysis['reasoning'] = " | ".join(reasoning_parts)
        
        return analysis
    
    def infer_personality_traits(self, texts: List[str]) -> PersonalityProfile:
        """
        Infer personality traits dari text (posting, bio, dll)
        
        Args:
            texts: List of texts dari kandidat
            
        Returns:
            PersonalityProfile object
        """
        combined_text = " ".join(texts).lower()
        
        traits = {}
        behavior_patterns = []
        key_interests = []
        
        # Leadership trait
        leadership_signals = [
            'lead', 'manage', 'team', 'project', 'delegate', 'motivate',
            'memimpin', 'mengelola', 'tim', 'proyek'
        ]
        leadership_score = sum(1 for signal in leadership_signals if signal in combined_text)
        traits['leadership'] = min(1.0, leadership_score / 5)
        
        # Analytical trait
        analytical_signals = [
            'data', 'analysis', 'research', 'study', 'investigate', 'metrics',
            'analisis', 'riset', 'penelitian', 'metrik'
        ]
        analytical_score = sum(1 for signal in analytical_signals if signal in combined_text)
        traits['analytical'] = min(1.0, analytical_score / 5)
        
        # Creative trait
        creative_signals = [
            'design', 'creative', 'innovative', 'idea', 'imagination', 'art',
            'desain', 'kreatif', 'inovasi', 'ide', 'seni'
        ]
        creative_score = sum(1 for signal in creative_signals if signal in combined_text)
        traits['creativity'] = min(1.0, creative_score / 5)
        
        # Social trait
        social_signals = [
            'community', 'social', 'people', 'collaborate', 'share', 'help',
            'komunitas', 'sosial', 'kolaborasi', 'berbagi', 'membantu'
        ]
        social_score = sum(1 for signal in social_signals if signal in combined_text)
        traits['social'] = min(1.0, social_score / 5)
        
        # Technical trait
        technical_signals = [
            'code', 'programming', 'software', 'system', 'technical', 'engineer',
            'kode', 'pemrograman', 'perangkat lunak', 'sistem', 'teknis'
        ]
        technical_score = sum(1 for signal in technical_signals if signal in combined_text)
        traits['technical'] = min(1.0, technical_score / 5)
        
        # Professional trait
        professional_signals = [
            'professional', 'career', 'business', 'work', 'industry', 'corporate',
            'profesional', 'karir', 'bisnis', 'kerja', 'industri'
        ]
        professional_score = sum(1 for signal in professional_signals if signal in combined_text)
        traits['professionalism'] = min(1.0, professional_score / 5)
        
        # Determine social presence
        text_volume = len(combined_text)
        if text_volume > 2000:
            social_presence = "active"
        elif text_volume > 500:
            social_presence = "moderate"
        else:
            social_presence = "passive"
        
        # Determine professional tone
        formal_words = ['professional', 'business', 'corporate', 'industry', 'strategy']
        casual_words = ['fun', 'cool', 'awesome', 'lol', 'haha', 'emoji']
        
        formal_count = sum(1 for word in formal_words if word in combined_text)
        casual_count = sum(1 for word in casual_words if word in combined_text)
        
        if formal_count > casual_count * 2:
            professional_tone = "formal"
        elif casual_count > formal_count * 2:
            professional_tone = "casual"
        else:
            professional_tone = "balanced"
        
        # Determine communication style
        question_marks = combined_text.count('?')
        exclamation_marks = combined_text.count('!')
        
        if question_marks > len(texts):
            communication_style = "inquisitive"
        elif exclamation_marks > len(texts):
            communication_style = "enthusiastic"
        else:
            communication_style = "informative"
        
        # Identify key interests
        interest_topics = self.nlp_engine.extract_semantic_topics(combined_text, num_topics=5)
        key_interests = [topic for topic, score in interest_topics if score > 0.1]
        
        # Identify behavior patterns
        if traits['leadership'] > 0.5:
            behavior_patterns.append("Menunjukkan kualitas kepemimpinan")
        if traits['analytical'] > 0.5:
            behavior_patterns.append("Berpikir analitis dan data-driven")
        if traits['creativity'] > 0.5:
            behavior_patterns.append("Kreatif dan inovatif")
        if traits['social'] > 0.5:
            behavior_patterns.append("Aktif dalam komunitas dan kolaborasi")
        if traits['technical'] > 0.5:
            behavior_patterns.append("Memiliki keahlian teknis yang kuat")
        if traits['professionalism'] > 0.7:
            behavior_patterns.append("Sangat profesional dalam komunikasi")
        
        return PersonalityProfile(
            traits=traits,
            behavior_patterns=behavior_patterns,
            social_presence=social_presence,
            professional_tone=professional_tone,
            key_interests=key_interests,
            communication_style=communication_style
        )


def get_advanced_nlp_engine(use_mock_models: bool = False) -> AdvancedNLPEngine:
    """Get NLP engine instance"""
    return AdvancedNLPEngine(use_mock_models=use_mock_models)


def get_reasoning_engine(nlp_engine: AdvancedNLPEngine) -> ContextualReasoningEngine:
    """Get reasoning engine instance"""
    return ContextualReasoningEngine(nlp_engine=nlp_engine)
