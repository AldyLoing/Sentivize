"""
Advanced AI Engine for Sentivize
=================================
Modul inti untuk AI analysis dengan capabilities:
- Semantic embeddings (sentence-transformers)
- Multi-layer sentiment analysis
- Contextual reasoning
- Deep profile generation
- Human-like insight generation
"""

import torch
from sentence_transformers import SentenceTransformer, util
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    pipeline
)
import numpy as np
from typing import List, Dict, Any, Tuple, Optional, Union
import warnings
warnings.filterwarnings('ignore')


class AdvancedAIEngine:
    """
    Engine AI paling canggih untuk Sentivize.
    Menggabungkan embeddings, sentiment, dan reasoning.
    """
    
    def __init__(self, device: str = None, lite_mode: bool = False):
        """
        Initialize AI Engine dengan semua model yang dibutuhkan.
        
        Args:
            device: 'cuda', 'cpu', atau None (auto-detect)
            lite_mode: If True, load minimal models (for low memory systems)
        """
        # Auto-detect device
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
        
        self.lite_mode = lite_mode
        
        if lite_mode:
            print(f"🔧 Initializing Advanced AI Engine in LITE MODE (minimal models)...")
        else:
            print(f"🔧 Initializing Advanced AI Engine on {self.device}...")
        
        # Initialize models with error handling
        self.embedding_model = None
        self.sentiment_tokenizer = None
        self.sentiment_model = None
        self.ner_pipeline = None
        self.zero_shot_classifier = None
        
        try:
            if not lite_mode:
                # 1. Semantic Embeddings Model (untuk semantic search)
                print("📥 Loading semantic embeddings model...")
                self.embedding_model = SentenceTransformer(
                    'paraphrase-multilingual-mpnet-base-v2',
                    device=self.device
                )
                
                # 2. Sentiment Analysis Model (multilingual)
                print("📥 Loading sentiment analysis model...")
                self.sentiment_model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
                self.sentiment_tokenizer = AutoTokenizer.from_pretrained(
                    self.sentiment_model_name
                )
                self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(
                    self.sentiment_model_name
                ).to(self.device)
                
                # 3. NER Model untuk extraction (opsional, bisa digunakan untuk CV parsing)
                print("📥 Loading NER model for entity extraction...")
                try:
                    self.ner_pipeline = pipeline(
                        "ner",
                        model="Davlan/xlm-roberta-base-ner-hrl",
                        aggregation_strategy="simple",
                        device=0 if self.device == 'cuda' else -1
                    )
                except Exception as e:
                    print(f"⚠️ NER model loading failed: {e}. Using fallback.")
                    self.ner_pipeline = None
                
                # 4. Zero-shot classification untuk category detection
                print("📥 Loading zero-shot classifier...")
                try:
                    self.zero_shot_classifier = pipeline(
                        "zero-shot-classification",
                        model="facebook/bart-large-mnli",
                        device=0 if self.device == 'cuda' else -1
                    )
                except Exception as e:
                    print(f"⚠️ Zero-shot classifier loading failed: {e}")
                    self.zero_shot_classifier = None
                
                print("✅ Advanced AI Engine initialized successfully!")
            else:
                print("✅ Advanced AI Engine initialized in LITE MODE (models will load on-demand)")
                
        except OSError as e:
            if "paging file" in str(e).lower() or "1455" in str(e):
                print("⚠️ Memory error detected - switching to LITE MODE")
                self.lite_mode = True
                self.embedding_model = None
                self.sentiment_tokenizer = None
                self.sentiment_model = None
                self.ner_pipeline = None
                self.zero_shot_classifier = None
            else:
                raise
        except Exception as e:
            print(f"⚠️ Error loading models: {e}")
            raise
        
    def compute_semantic_similarity(
        self, 
        query: str, 
        documents: List[str],
        return_scores: bool = True
    ) -> Union[List[float], List[Tuple[str, float]]]:
        """
        Hitung semantic similarity antara query dengan banyak dokumen.
        Menggunakan embeddings yang sangat powerful.
        
        Args:
            query: Kalimat pencarian/kriteria
            documents: List dokumen untuk dibandingkan
            return_scores: Return scores only atau (doc, score) pairs
            
        Returns:
            List of similarity scores (0-1) atau list of (document, score)
        """
        # Fallback for lite mode
        if self.lite_mode or self.embedding_model is None:
            print("⚠️ Semantic similarity unavailable (LITE MODE) - using keyword matching")
            scores = []
            query_lower = query.lower()
            for doc in documents:
                doc_lower = doc.lower()
                # Simple keyword overlap
                query_words = set(query_lower.split())
                doc_words = set(doc_lower.split())
                overlap = len(query_words & doc_words)
                score = min(overlap / max(len(query_words), 1), 1.0)
                scores.append(score)
            
            if return_scores:
                return scores
            else:
                return list(zip(documents, scores))
        
        # Encode query
        query_embedding = self.embedding_model.encode(
            query, 
            convert_to_tensor=True,
            show_progress_bar=False
        )
        
        # Encode documents
        doc_embeddings = self.embedding_model.encode(
            documents,
            convert_to_tensor=True,
            show_progress_bar=False
        )
        
        # Compute cosine similarity
        similarities = util.cos_sim(query_embedding, doc_embeddings)[0]
        scores = similarities.cpu().numpy().tolist()
        
        if return_scores:
            return scores
        else:
            return list(zip(documents, scores))
    
    def analyze_sentiment_multilayer(
        self, 
        text: str,
        aspects: List[str] = None
    ) -> Dict[str, Any]:
        """
        Analisis sentiment dengan banyak layer dan aspek.
        
        Args:
            text: Teks untuk dianalisis
            aspects: Aspek-aspek yang ingin dianalisis (leadership, teamwork, etc)
            
        Returns:
            Dict dengan sentiment scores untuk berbagai aspek
        """
        if not text or len(text.strip()) == 0:
            return {
                'overall_sentiment': 'NEUTRAL',
                'overall_score': 0.5,
                'confidence': 0.0,
                'aspects': {}
            }
        
        # Truncate text jika terlalu panjang
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
        
        # 1. Overall sentiment
        inputs = self.sentiment_tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.sentiment_model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)[0]
            
        # Labels: negative, neutral, positive
        labels = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']
        scores = probs.cpu().numpy()
        predicted_label = labels[np.argmax(scores)]
        confidence = float(np.max(scores))
        
        # Normalize score to 0-1 (negative=0, neutral=0.5, positive=1)
        if predicted_label == 'NEGATIVE':
            overall_score = float(scores[0]) * 0.0 + float(scores[1]) * 0.5
        elif predicted_label == 'NEUTRAL':
            overall_score = 0.5
        else:  # POSITIVE
            overall_score = float(scores[1]) * 0.5 + float(scores[2]) * 1.0
        
        result = {
            'overall_sentiment': predicted_label,
            'overall_score': overall_score,
            'confidence': confidence,
            'raw_scores': {
                'negative': float(scores[0]),
                'neutral': float(scores[1]),
                'positive': float(scores[2])
            }
        }
        
        # 2. Aspect-based sentiment (jika ada aspects)
        if aspects:
            result['aspects'] = {}
            for aspect in aspects:
                # Cari kalimat yang relevan dengan aspect
                aspect_text = self._extract_aspect_context(text, aspect)
                if aspect_text:
                    aspect_inputs = self.sentiment_tokenizer(
                        aspect_text,
                        return_tensors="pt",
                        truncation=True,
                        max_length=512
                    ).to(self.device)
                    
                    with torch.no_grad():
                        aspect_outputs = self.sentiment_model(**aspect_inputs)
                        aspect_probs = torch.softmax(aspect_outputs.logits, dim=1)[0]
                    
                    aspect_scores = aspect_probs.cpu().numpy()
                    aspect_label = labels[np.argmax(aspect_scores)]
                    
                    result['aspects'][aspect] = {
                        'sentiment': aspect_label,
                        'score': float(np.max(aspect_scores)),
                        'context': aspect_text[:100] + '...' if len(aspect_text) > 100 else aspect_text
                    }
        
        return result
    
    def _extract_aspect_context(self, text: str, aspect: str) -> str:
        """
        Extract kalimat yang relevan dengan aspek tertentu.
        """
        sentences = text.split('.')
        relevant_sentences = []
        
        # Cari kalimat yang mengandung kata kunci terkait aspect
        aspect_keywords = {
            'leadership': ['lead', 'leader', 'manage', 'team', 'memimpin', 'kepemimpinan'],
            'teamwork': ['team', 'kolaborasi', 'kerja sama', 'bersama', 'collaborate'],
            'communication': ['komunikasi', 'presentasi', 'berbicara', 'menulis', 'communication'],
            'technical': ['teknis', 'teknologi', 'programming', 'code', 'sistem'],
            'professional': ['profesional', 'kerja', 'karir', 'professional', 'work']
        }
        
        keywords = aspect_keywords.get(aspect.lower(), [aspect.lower()])
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                relevant_sentences.append(sentence.strip())
        
        return '. '.join(relevant_sentences) if relevant_sentences else text[:200]
    
    def generate_deep_profile(
        self, 
        candidate_data: Dict[str, Any],
        criteria: str = None
    ) -> Dict[str, Any]:
        """
        Generate profil mendalam kandidat dengan AI reasoning.
        
        Args:
            candidate_data: Data kandidat (nama, jabatan, skills, bio, dll)
            criteria: Kriteria pencarian (opsional)
            
        Returns:
            Dict dengan profil lengkap termasuk strengths, weaknesses, dll
        """
        # Gabungkan semua teks kandidat
        text_parts = []
        
        if candidate_data.get('position'):
            text_parts.append(f"Posisi: {candidate_data['position']}")
        if candidate_data.get('department'):
            text_parts.append(f"Departemen: {candidate_data['department']}")
        if candidate_data.get('experience'):
            text_parts.append(f"Pengalaman: {candidate_data['experience']}")
        if candidate_data.get('skills'):
            text_parts.append(f"Skills: {candidate_data['skills']}")
        if candidate_data.get('bio'):
            text_parts.append(f"Bio: {candidate_data['bio']}")
        if candidate_data.get('projects'):
            text_parts.append(f"Projects: {candidate_data['projects']}")
        
        full_text = '. '.join(text_parts)
        
        # 1. Sentiment Analysis
        sentiment = self.analyze_sentiment_multilayer(
            full_text,
            aspects=['leadership', 'teamwork', 'communication', 'professional']
        )
        
        # 2. Strengths Detection
        strengths = self._detect_strengths(candidate_data, full_text)
        
        # 3. Weaknesses Detection (gap analysis)
        weaknesses = self._detect_weaknesses(candidate_data, criteria)
        
        # 4. Career Potential
        career_potential = self._assess_career_potential(candidate_data, sentiment)
        
        # 5. Communication Style
        communication_style = self._analyze_communication_style(full_text, sentiment)
        
        # 6. Risk Assessment
        risks = self._assess_risks(candidate_data, sentiment)
        
        # 7. Soft Skills
        soft_skills = self._detect_soft_skills(full_text)
        
        # 8. Hard Skills
        hard_skills = self._extract_hard_skills(candidate_data)
        
        profile = {
            'candidate_name': candidate_data.get('name', 'Unknown'),
            'position': candidate_data.get('position', 'N/A'),
            'strengths': strengths,
            'weaknesses': weaknesses,
            'career_potential': career_potential,
            'communication_style': communication_style,
            'soft_skills': soft_skills,
            'hard_skills': hard_skills,
            'risks': risks,
            'sentiment_profile': sentiment,
            'overall_assessment': self._generate_overall_assessment(
                strengths, weaknesses, career_potential, sentiment
            )
        }
        
        return profile
    
    def _detect_strengths(self, data: Dict, text: str) -> List[str]:
        """Deteksi kekuatan kandidat dari data dan teks."""
        strengths = []
        
        # Analisis dari posisi
        position = data.get('position', '').lower()
        if any(word in position for word in ['senior', 'lead', 'manager', 'director']):
            strengths.append("Pengalaman leadership di level senior")
        if any(word in position for word in ['expert', 'specialist', 'architect']):
            strengths.append("Keahlian spesialis di bidangnya")
        
        # Analisis dari skills
        skills = data.get('skills', '').lower()
        if skills:
            if len(skills.split(',')) > 5:
                strengths.append("Memiliki skill set yang beragam")
            if any(word in skills for word in ['python', 'java', 'ai', 'machine learning']):
                strengths.append("Keahlian teknis di teknologi modern")
        
        # Analisis dari bio/text
        if any(word in text.lower() for word in ['award', 'achievement', 'prestasi', 'penghargaan']):
            strengths.append("Memiliki track record pencapaian")
        
        if any(word in text.lower() for word in ['team', 'kolaborasi', 'collaborate']):
            strengths.append("Pengalaman kerja tim yang baik")
        
        if not strengths:
            strengths.append("Kandidat dengan latar belakang solid")
        
        return strengths[:5]  # Max 5 strengths
    
    def _detect_weaknesses(self, data: Dict, criteria: str) -> List[str]:
        """Deteksi kelemahan atau gap kandidat."""
        weaknesses = []
        
        # Analisis gap dari criteria (jika ada)
        if criteria:
            text = ' '.join([
                str(data.get('position', '')),
                str(data.get('skills', '')),
                str(data.get('bio', ''))
            ])
            
            relevance = self.compute_semantic_similarity(criteria, [text])[0]
            if relevance < 0.5:
                weaknesses.append("Relevansi dengan kriteria perlu ditingkatkan")
        
        # Cek kelengkapan data
        if not data.get('skills'):
            weaknesses.append("Informasi skills perlu dilengkapi")
        
        if not data.get('experience') and not data.get('bio'):
            weaknesses.append("Informasi pengalaman kerja kurang detail")
        
        # Default jika tidak ada weakness terdeteksi
        if not weaknesses:
            weaknesses.append("Tidak ada kelemahan signifikan terdeteksi")
        
        return weaknesses[:3]  # Max 3 weaknesses
    
    def _assess_career_potential(self, data: Dict, sentiment: Dict) -> Dict[str, Any]:
        """Penilaian potensi karier kandidat."""
        position = data.get('position', '').lower()
        
        # Estimate seniority level
        if any(word in position for word in ['junior', 'staff', 'entry']):
            level = 'Junior'
            growth_potential = 'High'
        elif any(word in position for word in ['senior', 'lead']):
            level = 'Senior'
            growth_potential = 'Medium to High'
        elif any(word in position for word in ['manager', 'head', 'director']):
            level = 'Management'
            growth_potential = 'Leadership Track'
        else:
            level = 'Mid-level'
            growth_potential = 'Medium'
        
        # Faktor sentiment
        if sentiment['overall_score'] > 0.7:
            attitude = 'Sangat positif dan proaktif'
        elif sentiment['overall_score'] > 0.5:
            attitude = 'Positif dan stabil'
        else:
            attitude = 'Perlu pengembangan soft skills'
        
        return {
            'current_level': level,
            'growth_potential': growth_potential,
            'attitude': attitude,
            'recommendation': f"Kandidat dengan potensi {growth_potential.lower()} untuk berkembang"
        }
    
    def _analyze_communication_style(self, text: str, sentiment: Dict) -> str:
        """Analisis gaya komunikasi dari teks."""
        text_lower = text.lower()
        
        # Analisis dari panjang dan struktur teks
        if len(text) < 100:
            style = "Komunikasi singkat dan to-the-point"
        elif len(text) > 500:
            style = "Komunikasi detail dan elaboratif"
        else:
            style = "Komunikasi seimbang dan efektif"
        
        # Tambahkan tone dari sentiment
        if sentiment['overall_score'] > 0.7:
            style += ", dengan tone yang sangat positif dan profesional"
        elif sentiment['overall_score'] > 0.5:
            style += ", dengan tone yang profesional"
        else:
            style += ", dengan tone yang perlu lebih dikembangkan"
        
        return style
    
    def _assess_risks(self, data: Dict, sentiment: Dict) -> List[str]:
        """Identifikasi risiko atau red flags."""
        risks = []
        
        # Cek sentiment negatif
        if sentiment['overall_score'] < 0.4:
            risks.append("⚠️ Indikasi sentiment negatif dalam profil")
        
        # Cek kelengkapan data
        missing_fields = []
        for field in ['position', 'skills', 'experience', 'bio']:
            if not data.get(field):
                missing_fields.append(field)
        
        if len(missing_fields) > 2:
            risks.append("⚠️ Data profil kurang lengkap")
        
        # Default: no major risks
        if not risks:
            risks.append("✅ Tidak ada red flag signifikan")
        
        return risks
    
    def _detect_soft_skills(self, text: str) -> List[str]:
        """Deteksi soft skills dari teks."""
        soft_skills = []
        text_lower = text.lower()
        
        skill_keywords = {
            'Leadership': ['lead', 'leader', 'memimpin', 'kepemimpinan', 'manage'],
            'Communication': ['komunikasi', 'presentasi', 'berbicara', 'communication'],
            'Teamwork': ['team', 'kolaborasi', 'kerja sama', 'collaborate'],
            'Problem Solving': ['problem', 'solving', 'solusi', 'menyelesaikan'],
            'Adaptability': ['adaptasi', 'fleksibel', 'flexible', 'adapt'],
            'Critical Thinking': ['analisis', 'berpikir', 'kritis', 'analytical']
        }
        
        for skill, keywords in skill_keywords.items():
            if any(kw in text_lower for kw in keywords):
                soft_skills.append(skill)
        
        return soft_skills[:5] if soft_skills else ['Teamwork', 'Communication']
    
    def _extract_hard_skills(self, data: Dict) -> List[str]:
        """Extract hard skills dari data kandidat."""
        skills_text = data.get('skills', '')
        if not skills_text:
            return ['Tidak ada informasi hard skills']
        
        # Split by comma and clean
        skills = [s.strip() for s in skills_text.split(',')]
        return skills[:10]  # Max 10 hard skills
    
    def _generate_overall_assessment(
        self, 
        strengths: List[str],
        weaknesses: List[str],
        career_potential: Dict,
        sentiment: Dict
    ) -> str:
        """Generate kesimpulan keseluruhan dengan bahasa manusiawi."""
        
        # Mulai dengan strengths
        assessment = f"Kandidat ini menunjukkan {len(strengths)} kekuatan utama. "
        
        # Tambahkan career potential
        assessment += f"Berada di level {career_potential['current_level']} dengan potensi "
        assessment += f"{career_potential['growth_potential'].lower()}. "
        
        # Sentiment
        if sentiment['overall_score'] > 0.7:
            assessment += "Memiliki attitude yang sangat positif dan profesional. "
        elif sentiment['overall_score'] > 0.5:
            assessment += "Menunjukkan sikap profesional yang baik. "
        
        # Weaknesses (jika ada yang signifikan)
        if len(weaknesses) > 0 and "Tidak ada kelemahan" not in weaknesses[0]:
            assessment += f"Perlu perhatian pada {len(weaknesses)} area untuk pengembangan lebih lanjut. "
        
        # Kesimpulan
        if sentiment['overall_score'] > 0.6 and len(strengths) >= 3:
            assessment += "Secara keseluruhan, kandidat yang sangat potensial untuk dipertimbangkan."
        elif sentiment['overall_score'] > 0.5:
            assessment += "Secara keseluruhan, kandidat yang layak untuk dipertimbangkan lebih lanjut."
        else:
            assessment += "Perlu evaluasi lebih mendalam untuk memastikan kesesuaian."
        
        return assessment
    
    def classify_text_categories(
        self, 
        text: str, 
        candidate_labels: List[str]
    ) -> Dict[str, float]:
        """
        Klasifikasi teks ke dalam kategori menggunakan zero-shot learning.
        Berguna untuk mendeteksi expertise, industry domain, dll.
        
        Args:
            text: Teks untuk diklasifikasi
            candidate_labels: List kategori yang mungkin
            
        Returns:
            Dict {kategori: confidence_score}
        """
        if not self.zero_shot_classifier:
            # Fallback: keyword-based
            results = {}
            text_lower = text.lower()
            for label in candidate_labels:
                if label.lower() in text_lower:
                    results[label] = 0.8
                else:
                    results[label] = 0.1
            return results
        
        try:
            result = self.zero_shot_classifier(
                text,
                candidate_labels,
                multi_label=True
            )
            return dict(zip(result['labels'], result['scores']))
        except Exception as e:
            print(f"⚠️ Zero-shot classification error: {e}")
            return {label: 0.0 for label in candidate_labels}
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities dari teks (nama, organisasi, lokasi, dll).
        
        Args:
            text: Teks untuk di-extract
            
        Returns:
            List of entities dengan type dan confidence
        """
        if not self.ner_pipeline:
            return []
        
        try:
            entities = self.ner_pipeline(text)
            return [
                {
                    'text': ent['word'],
                    'type': ent['entity_group'],
                    'score': ent['score']
                }
                for ent in entities
            ]
        except Exception as e:
            print(f"⚠️ NER extraction error: {e}")
            return []
    
    def batch_analyze_relevance(
        self,
        query: str,
        candidates: List[Dict[str, Any]],
        text_field: str = 'text'
    ) -> List[Dict[str, Any]]:
        """
        Analisis relevansi banyak kandidat sekaligus terhadap query.
        Optimized untuk batch processing.
        
        Args:
            query: Kriteria pencarian
            candidates: List of candidate dicts
            text_field: Field name yang berisi teks untuk analisis
            
        Returns:
            List of candidates dengan tambahan relevance_score
        """
        # Extract texts
        texts = [c.get(text_field, '') for c in candidates]
        
        # Compute similarities
        similarities = self.compute_semantic_similarity(query, texts)
        
        # Add scores to candidates
        results = []
        for candidate, score in zip(candidates, similarities):
            candidate_copy = candidate.copy()
            candidate_copy['relevance_score'] = float(score)
            results.append(candidate_copy)
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results


# Singleton instance untuk reuse
_engine_instance = None

def get_ai_engine(device: str = None, lite_mode: bool = None) -> AdvancedAIEngine:
    """
    Get singleton instance of AI Engine.
    Prevents loading models multiple times.
    
    Args:
        device: 'cuda', 'cpu', atau None
        lite_mode: If True, use minimal models (for low memory), None = auto from config
    """
    global _engine_instance
    if _engine_instance is None:
        # Check config for lite mode if not specified
        if lite_mode is None:
            from config import AI_LITE_MODE
            lite_mode = AI_LITE_MODE
            if lite_mode:
                print("✅ AI_LITE_MODE enabled from config (using minimal models)")
        
        try:
            _engine_instance = AdvancedAIEngine(device=device, lite_mode=lite_mode)
        except OSError as e:
            if "paging file" in str(e).lower() or "1455" in str(e):
                print("⚠️ Memory error - forcing LITE MODE")
                _engine_instance = AdvancedAIEngine(device=device, lite_mode=True)
            else:
                raise
        except Exception as e:
            print(f"⚠️ Error initializing AI Engine: {e}")
            print("⚠️ Falling back to LITE MODE")
            _engine_instance = AdvancedAIEngine(device=device, lite_mode=True)
    return _engine_instance
