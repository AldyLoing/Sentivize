"""
Advanced Employee Analyzer - Deep Social Media & Behavioral Analysis
Analisis mendalam perilaku, nilai personal, dan kepribadian berdasarkan aktivitas digital
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import re

from advanced_ai_core import (
    AdvancedNLPEngine,
    ContextualReasoningEngine,
    PersonalityProfile,
    get_advanced_nlp_engine,
    get_reasoning_engine,
    AnalysisInsight
)
import services
import config


@dataclass
class BehavioralProfile:
    """Profile perilaku digital kandidat"""
    personality: PersonalityProfile
    value_alignment: Dict[str, float]  # environmental, social, professional, etc.
    posting_patterns: Dict[str, Any]
    sentiment_distribution: Dict[str, int]
    engagement_metrics: Dict[str, float]
    professional_maturity: float
    red_flags: List[str]
    green_flags: List[str]


@dataclass
class EmployeeAnalysisResult:
    """Hasil analisis karyawan yang comprehensive"""
    name: str
    position: Optional[str]
    unit: Optional[str]
    social_links: List[str]
    behavioral_profile: Optional[BehavioralProfile]
    relevance_score: float
    relevance_reasoning: str
    sentiment_label: str
    sentiment_score: float
    value_themes: List[Tuple[str, float]]
    character_assessment: str
    potential_score: float
    recommendation: str
    confidence: float


class AdvancedEmployeeAnalyzer:
    """
    Advanced analyzer untuk analisis karyawan dengan deep understanding
    """
    
    def __init__(self, use_mock_models: bool = False):
        self.nlp_engine = get_advanced_nlp_engine(use_mock_models=use_mock_models)
        self.reasoning_engine = get_reasoning_engine(self.nlp_engine)
        self.use_mock = use_mock_models
    
    def analyze_employee_comprehensive(
        self,
        name: str,
        position: Optional[str],
        unit: Optional[str],
        texts: List[str],
        social_links: List[str],
        keyword: str,
        enable_behavioral_analysis: bool = True
    ) -> EmployeeAnalysisResult:
        """
        Comprehensive analysis dengan behavioral profiling
        
        Args:
            name: Nama kandidat
            position: Jabatan
            unit: Unit kerja
            texts: List of texts (posting, bio, dll)
            social_links: Social media links
            keyword: Keyword untuk relevance
            enable_behavioral_analysis: Enable deep behavioral analysis
            
        Returns:
            EmployeeAnalysisResult
        """
        
        # 1. Basic sentiment analysis
        from ai_analyzer import get_analyzer
        basic_analyzer = get_analyzer(use_mock_models=self.use_mock)
        
        sentiment_label, sentiment_score = basic_analyzer.analyze_sentiment(texts)
        
        # 2. Advanced relevance with deep reasoning
        relevance_score, relevance_reasoning = self._calculate_advanced_relevance(
            texts, keyword, name, position, unit
        )
        
        # 3. Behavioral profiling (if enabled and texts available)
        behavioral_profile = None
        if enable_behavioral_analysis and texts:
            behavioral_profile = self._create_behavioral_profile(texts, name)
        
        # 4. Value theme extraction
        value_themes = self._extract_value_themes(texts)
        
        # 5. Character assessment
        character_assessment = self._generate_character_assessment(
            name, texts, behavioral_profile, sentiment_label, value_themes
        )
        
        # 6. Potential score
        potential_score = self._calculate_potential_score(
            relevance_score, sentiment_score, behavioral_profile, value_themes
        )
        
        # 7. Recommendation
        recommendation = self._generate_recommendation(
            relevance_score, potential_score, behavioral_profile
        )
        
        # 8. Confidence
        confidence = self._calculate_analysis_confidence(
            texts, social_links, behavioral_profile
        )
        
        return EmployeeAnalysisResult(
            name=name,
            position=position,
            unit=unit,
            social_links=social_links,
            behavioral_profile=behavioral_profile,
            relevance_score=relevance_score,
            relevance_reasoning=relevance_reasoning,
            sentiment_label=sentiment_label,
            sentiment_score=sentiment_score,
            value_themes=value_themes,
            character_assessment=character_assessment,
            potential_score=potential_score,
            recommendation=recommendation,
            confidence=confidence
        )
    
    def _calculate_advanced_relevance(
        self,
        texts: List[str],
        keyword: str,
        name: str,
        position: Optional[str],
        unit: Optional[str]
    ) -> Tuple[float, str]:
        """
        Calculate relevance dengan contextual reasoning
        """
        if not texts or not keyword:
            return 0.0, "Tidak ada data untuk analisis"
        
        # Combine texts
        combined_text = " ".join(texts)
        
        # Calculate base semantic similarity
        base_similarity = self.nlp_engine.calculate_semantic_similarity(
            combined_text, keyword
        )
        
        # Extract entities from texts and keyword
        text_entities = self.nlp_engine.extract_entities(combined_text)
        keyword_entities = self.nlp_engine.extract_entities(keyword)
        
        # Calculate entity match bonus
        entity_bonus = 0.0
        entity_matches = []
        
        # Check skill matches
        text_skills = set([s.lower() for s in text_entities.get('skills', [])])
        keyword_skills = set([s.lower() for s in keyword_entities.get('skills', [])])
        
        skill_matches = text_skills & keyword_skills
        if skill_matches:
            entity_bonus += 0.1 * min(len(skill_matches), 3)
            entity_matches.extend([f"Skill: {s}" for s in list(skill_matches)[:3]])
        
        # Check organization matches
        text_orgs = set([o.lower() for o in text_entities.get('organizations', [])])
        keyword_orgs = set([o.lower() for o in keyword_entities.get('organizations', [])])
        
        org_matches = text_orgs & keyword_orgs
        if org_matches:
            entity_bonus += 0.05 * len(org_matches)
            entity_matches.extend([f"Organisasi: {o}" for o in list(org_matches)[:2]])
        
        # Extract topics
        text_topics = self.nlp_engine.extract_semantic_topics(combined_text, num_topics=5)
        keyword_topics = self.nlp_engine.extract_semantic_topics(keyword, num_topics=3)
        
        # Topic overlap
        topic_bonus = 0.0
        topic_matches = []
        
        for text_topic, text_score in text_topics:
            for keyword_topic, keyword_score in keyword_topics:
                # Simple word overlap
                text_words = set(text_topic.lower().split())
                keyword_words = set(keyword_topic.lower().split())
                overlap = len(text_words & keyword_words)
                
                if overlap >= 1:
                    topic_bonus += 0.05
                    topic_matches.append(text_topic)
                    break
        
        # Calculate final score
        final_score = base_similarity + entity_bonus + topic_bonus
        final_score = min(1.0, max(0.0, final_score))
        
        # Generate reasoning
        reasoning_parts = []
        
        reasoning_parts.append(f"Skor similaritas semantik: {base_similarity:.2%}")
        
        if entity_matches:
            reasoning_parts.append(f"Entitas yang cocok: {', '.join(entity_matches[:5])}")
        
        if topic_matches:
            reasoning_parts.append(f"Tema relevan: {', '.join(topic_matches[:3])}")
        
        if position:
            reasoning_parts.append(f"Posisi: {position}")
        
        if unit:
            reasoning_parts.append(f"Unit: {unit}")
        
        # Check for exact keyword matches
        keyword_lower = keyword.lower()
        exact_matches = sum(1 for text in texts if keyword_lower in text.lower())
        if exact_matches > 0:
            reasoning_parts.append(f"Kata kunci muncul eksplisit {exact_matches}x")
        
        reasoning = " | ".join(reasoning_parts)
        
        return round(final_score, 3), reasoning
    
    def _create_behavioral_profile(
        self,
        texts: List[str],
        name: str
    ) -> BehavioralProfile:
        """
        Create comprehensive behavioral profile
        """
        
        # 1. Personality profile
        personality = self.reasoning_engine.infer_personality_traits(texts)
        
        # 2. Value alignment
        value_alignment = self._assess_value_alignment(texts)
        
        # 3. Posting patterns
        posting_patterns = self._analyze_posting_patterns(texts)
        
        # 4. Sentiment distribution
        sentiment_distribution = self._analyze_sentiment_distribution(texts)
        
        # 5. Engagement metrics
        engagement_metrics = self._calculate_engagement_metrics(texts)
        
        # 6. Professional maturity
        professional_maturity = self._assess_professional_maturity(texts)
        
        # 7. Red flags & Green flags
        red_flags = self._identify_red_flags(texts)
        green_flags = self._identify_green_flags(texts)
        
        return BehavioralProfile(
            personality=personality,
            value_alignment=value_alignment,
            posting_patterns=posting_patterns,
            sentiment_distribution=sentiment_distribution,
            engagement_metrics=engagement_metrics,
            professional_maturity=professional_maturity,
            red_flags=red_flags,
            green_flags=green_flags
        )
    
    def _assess_value_alignment(self, texts: List[str]) -> Dict[str, float]:
        """
        Assess alignment dengan berbagai values
        """
        combined_text = " ".join(texts).lower()
        
        value_dimensions = {
            'environmental': [
                'lingkungan', 'environment', 'sustainability', 'green', 'climate',
                'conservation', 'eco', 'renewable', 'recycle', 'pollution'
            ],
            'social_responsibility': [
                'social', 'community', 'volunteer', 'charity', 'donation', 'help',
                'sosial', 'komunitas', 'sukarelawan', 'donasi', 'membantu'
            ],
            'innovation': [
                'innovation', 'innovative', 'technology', 'digital', 'future',
                'inovasi', 'inovatif', 'teknologi', 'digital', 'masa depan'
            ],
            'education': [
                'education', 'learning', 'teaching', 'knowledge', 'training',
                'pendidikan', 'pembelajaran', 'mengajar', 'pengetahuan', 'pelatihan'
            ],
            'diversity_inclusion': [
                'diversity', 'inclusion', 'equality', 'inclusive', 'diverse',
                'keberagaman', 'inklusif', 'kesetaraan'
            ],
            'professionalism': [
                'professional', 'career', 'business', 'industry', 'work',
                'profesional', 'karir', 'bisnis', 'industri', 'kerja'
            ],
            'leadership': [
                'leadership', 'lead', 'manage', 'team', 'mentor',
                'kepemimpinan', 'memimpin', 'mengelola', 'tim', 'mentor'
            ],
            'creativity': [
                'creative', 'creativity', 'design', 'art', 'innovation',
                'kreatif', 'kreativitas', 'desain', 'seni', 'inovasi'
            ]
        }
        
        value_scores = {}
        
        for value_name, keywords in value_dimensions.items():
            # Count occurrences
            occurrences = sum(combined_text.count(keyword) for keyword in keywords)
            
            # Normalize to 0-1 scale
            score = min(1.0, occurrences / 10.0)
            value_scores[value_name] = round(score, 2)
        
        return value_scores
    
    def _analyze_posting_patterns(self, texts: List[str]) -> Dict[str, Any]:
        """
        Analyze posting patterns and behavior
        """
        patterns = {
            'total_posts': len(texts),
            'avg_length': 0,
            'content_diversity': 0.0,
            'interaction_style': 'informative'  # informative, conversational, promotional
        }
        
        if not texts:
            return patterns
        
        # Average length
        lengths = [len(text) for text in texts]
        patterns['avg_length'] = int(sum(lengths) / len(lengths))
        
        # Content diversity (based on unique words)
        all_words = []
        for text in texts:
            words = text.lower().split()
            all_words.extend(words)
        
        if all_words:
            unique_ratio = len(set(all_words)) / len(all_words)
            patterns['content_diversity'] = round(unique_ratio, 2)
        
        # Interaction style
        combined_text = " ".join(texts).lower()
        
        question_marks = sum(text.count('?') for text in texts)
        exclamation_marks = sum(text.count('!') for text in texts)
        promotional_words = sum(1 for word in ['buy', 'sale', 'discount', 'offer', 'promo'] if word in combined_text)
        
        if question_marks > len(texts):
            patterns['interaction_style'] = 'conversational'
        elif promotional_words > 3:
            patterns['interaction_style'] = 'promotional'
        else:
            patterns['interaction_style'] = 'informative'
        
        return patterns
    
    def _analyze_sentiment_distribution(self, texts: List[str]) -> Dict[str, int]:
        """
        Analyze distribution of sentiments across posts
        """
        from ai_analyzer import get_analyzer
        analyzer = get_analyzer(use_mock_models=self.use_mock)
        
        distribution = {
            'POSITIVE': 0,
            'NEGATIVE': 0,
            'NEUTRAL': 0
        }
        
        for text in texts[:10]:  # Analyze up to 10 posts
            if not text or len(text.strip()) < 10:
                continue
            
            sentiment_label, _ = analyzer.analyze_sentiment([text])
            distribution[sentiment_label] += 1
        
        return distribution
    
    def _calculate_engagement_metrics(self, texts: List[str]) -> Dict[str, float]:
        """
        Calculate engagement quality metrics
        """
        metrics = {
            'content_quality': 0.0,
            'thoughtfulness': 0.0,
            'clarity': 0.0
        }
        
        if not texts:
            return metrics
        
        combined_text = " ".join(texts)
        
        # Content quality (based on length and structure)
        avg_length = sum(len(t) for t in texts) / len(texts)
        if avg_length > 200:
            metrics['content_quality'] = 0.8
        elif avg_length > 100:
            metrics['content_quality'] = 0.6
        else:
            metrics['content_quality'] = 0.4
        
        # Thoughtfulness (based on depth indicators)
        depth_indicators = [
            'because', 'therefore', 'however', 'although', 'moreover',
            'karena', 'oleh karena itu', 'namun', 'meskipun', 'selain itu'
        ]
        
        depth_count = sum(combined_text.lower().count(indicator) for indicator in depth_indicators)
        metrics['thoughtfulness'] = min(1.0, depth_count / 5.0)
        
        # Clarity (based on structure)
        sentences = combined_text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        # Optimal sentence length: 15-25 words
        if 15 <= avg_sentence_length <= 25:
            metrics['clarity'] = 0.9
        elif 10 <= avg_sentence_length <= 30:
            metrics['clarity'] = 0.7
        else:
            metrics['clarity'] = 0.5
        
        return {k: round(v, 2) for k, v in metrics.items()}
    
    def _assess_professional_maturity(self, texts: List[str]) -> float:
        """
        Assess professional maturity dari posting behavior
        """
        if not texts:
            return 0.5
        
        combined_text = " ".join(texts).lower()
        
        maturity_score = 0.5  # Base score
        
        # Positive indicators
        positive_indicators = [
            'professional', 'industry', 'career', 'experience', 'learning',
            'development', 'achievement', 'responsible', 'strategy', 'goal',
            'profesional', 'industri', 'karir', 'pengalaman', 'pembelajaran'
        ]
        
        positive_count = sum(combined_text.count(indicator) for indicator in positive_indicators)
        maturity_score += min(0.3, positive_count / 20.0)
        
        # Negative indicators
        negative_indicators = [
            'lol', 'haha', 'omg', 'wtf', 'drama', 'gossip', 'hate',
            'stupid', 'idiot', 'sucks', 'complain'
        ]
        
        negative_count = sum(combined_text.count(indicator) for indicator in negative_indicators)
        maturity_score -= min(0.3, negative_count / 10.0)
        
        # Grammar/spelling quality (rough estimate)
        # Check for excessive punctuation
        excessive_punctuation = re.findall(r'[!?]{2,}', combined_text)
        if len(excessive_punctuation) > 5:
            maturity_score -= 0.1
        
        # Check for CAPS LOCK abuse
        caps_words = re.findall(r'\b[A-Z]{3,}\b', " ".join(texts))
        if len(caps_words) > len(texts):
            maturity_score -= 0.1
        
        return round(max(0.0, min(1.0, maturity_score)), 2)
    
    def _identify_red_flags(self, texts: List[str]) -> List[str]:
        """
        Identify potential red flags dalam behavior
        """
        red_flags = []
        
        if not texts:
            return red_flags
        
        combined_text = " ".join(texts).lower()
        
        # Negativity
        negative_keywords = ['hate', 'angry', 'stupid', 'idiot', 'terrible', 'worst', 'sucks']
        negative_count = sum(combined_text.count(kw) for kw in negative_keywords)
        if negative_count > 3:
            red_flags.append(f"Konten negatif berlebihan ({negative_count} instances)")
        
        # Unprofessional language
        unprofessional_keywords = ['wtf', 'damn', 'shit', 'fuck', 'hell']
        unprofessional_count = sum(combined_text.count(kw) for kw in unprofessional_keywords)
        if unprofessional_count > 0:
            red_flags.append("Bahasa kurang profesional terdeteksi")
        
        # Controversial topics (politics, religion)
        controversial_keywords = ['politik', 'political', 'religion', 'agama', 'partai']
        controversial_count = sum(combined_text.count(kw) for kw in controversial_keywords)
        if controversial_count > 5:
            red_flags.append("Banyak konten kontroversial (politik/agama)")
        
        # Complaint pattern
        complaint_keywords = ['complain', 'keluh', 'mengeluh', 'frustrated', 'frustasi']
        complaint_count = sum(combined_text.count(kw) for kw in complaint_keywords)
        if complaint_count > 3:
            red_flags.append("Pola mengeluh yang tinggi")
        
        # Excessive self-promotion
        promo_keywords = ['buy', 'sale', 'discount', 'promo', 'limited offer', 'click here']
        promo_count = sum(combined_text.count(kw) for kw in promo_keywords)
        if promo_count > len(texts) * 0.3:
            red_flags.append("Terlalu banyak promosi/spam")
        
        return red_flags
    
    def _identify_green_flags(self, texts: List[str]) -> List[str]:
        """
        Identify positive indicators dalam behavior
        """
        green_flags = []
        
        if not texts:
            return green_flags
        
        combined_text = " ".join(texts).lower()
        
        # Thought leadership
        leadership_keywords = ['insight', 'analysis', 'perspective', 'learned', 'sharing', 'experience']
        leadership_count = sum(combined_text.count(kw) for kw in leadership_keywords)
        if leadership_count > 5:
            green_flags.append("Menunjukkan thought leadership")
        
        # Helping others
        helping_keywords = ['help', 'assist', 'support', 'guide', 'mentor', 'membantu', 'mendukung']
        helping_count = sum(combined_text.count(kw) for kw in helping_keywords)
        if helping_count > 3:
            green_flags.append("Aktif membantu komunitas")
        
        # Continuous learning
        learning_keywords = ['learn', 'course', 'training', 'certification', 'studying', 'belajar', 'pelatihan']
        learning_count = sum(combined_text.count(kw) for kw in learning_keywords)
        if learning_count > 3:
            green_flags.append("Komitmen pada pembelajaran berkelanjutan")
        
        # Professional engagement
        professional_keywords = ['industry', 'conference', 'seminar', 'workshop', 'networking', 'professional']
        professional_count = sum(combined_text.count(kw) for kw in professional_keywords)
        if professional_count > 3:
            green_flags.append("Aktif dalam pengembangan profesional")
        
        # Positive impact
        impact_keywords = ['achieve', 'success', 'improve', 'grow', 'develop', 'impact', 'contribute']
        impact_count = sum(combined_text.count(kw) for kw in impact_keywords)
        if impact_count > 5:
            green_flags.append("Fokus pada dampak dan pencapaian")
        
        # Collaboration
        collab_keywords = ['collaborate', 'team', 'together', 'partnership', 'collective', 'kolaborasi']
        collab_count = sum(combined_text.count(kw) for kw in collab_keywords)
        if collab_count > 3:
            green_flags.append("Kuat dalam kolaborasi dan kerja tim")
        
        return green_flags
    
    def _extract_value_themes(self, texts: List[str]) -> List[Tuple[str, float]]:
        """
        Extract main value/interest themes
        """
        if not texts:
            return []
        
        combined_text = " ".join(texts)
        
        # Use NLP engine to extract topics
        topics = self.nlp_engine.extract_semantic_topics(combined_text, num_topics=5)
        
        return topics
    
    def _generate_character_assessment(
        self,
        name: str,
        texts: List[str],
        behavioral_profile: Optional[BehavioralProfile],
        sentiment_label: str,
        value_themes: List[Tuple[str, float]]
    ) -> str:
        """
        Generate comprehensive character assessment
        """
        assessment_parts = []
        
        assessment_parts.append(f"**Profil Karakter: {name}**\n\n")
        
        if not texts:
            return assessment_parts[0] + "Data tidak cukup untuk analisis karakter mendalam."
        
        # Personality traits
        if behavioral_profile and behavioral_profile.personality:
            personality = behavioral_profile.personality
            assessment_parts.append("**Kepribadian:**\n")
            
            # Top 3 traits
            sorted_traits = sorted(
                personality.traits.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            
            for trait, score in sorted_traits:
                if score > 0.5:
                    trait_desc = trait.replace('_', ' ').title()
                    if score >= 0.75:
                        level = "Sangat Tinggi"
                    elif score >= 0.6:
                        level = "Tinggi"
                    else:
                        level = "Moderat"
                    assessment_parts.append(f"- {trait_desc}: {level} ({score:.0%})\n")
            
            assessment_parts.append(f"\n**Pola Perilaku:**\n")
            for pattern in personality.behavior_patterns[:3]:
                assessment_parts.append(f"- {pattern}\n")
            
            assessment_parts.append(f"\n**Karakteristik Komunikasi:**\n")
            assessment_parts.append(f"- Keaktifan: {personality.social_presence.title()}\n")
            assessment_parts.append(f"- Tone: {personality.professional_tone.title()}\n")
            assessment_parts.append(f"- Style: {personality.communication_style.title()}\n")
        
        # Value alignment
        if behavioral_profile and behavioral_profile.value_alignment:
            assessment_parts.append(f"\n**Nilai & Minat:**\n")
            
            sorted_values = sorted(
                behavioral_profile.value_alignment.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            
            for value, score in sorted_values:
                if score > 0.3:
                    value_desc = value.replace('_', ' ').title()
                    assessment_parts.append(f"- {value_desc}: {score:.0%}\n")
        
        # Value themes
        if value_themes:
            assessment_parts.append(f"\n**Tema Utama:**\n")
            for theme, score in value_themes[:3]:
                if score > 0.1:
                    assessment_parts.append(f"- {theme.title()}\n")
        
        # Professional maturity
        if behavioral_profile:
            assessment_parts.append(f"\n**Profesionalisme:** {behavioral_profile.professional_maturity:.0%}\n")
        
        # Overall sentiment
        sentiment_desc = {
            'POSITIVE': 'Positif dan optimis',
            'NEGATIVE': 'Kritis dan analitis',
            'NEUTRAL': 'Seimbang dan objektif'
        }
        assessment_parts.append(f"\n**Sentimen Umum:** {sentiment_desc.get(sentiment_label, sentiment_label)}\n")
        
        # Flags
        if behavioral_profile:
            if behavioral_profile.green_flags:
                assessment_parts.append(f"\n**✅ Indikator Positif:**\n")
                for flag in behavioral_profile.green_flags[:3]:
                    assessment_parts.append(f"- {flag}\n")
            
            if behavioral_profile.red_flags:
                assessment_parts.append(f"\n**⚠️ Perhatian:**\n")
                for flag in behavioral_profile.red_flags[:3]:
                    assessment_parts.append(f"- {flag}\n")
        
        return "".join(assessment_parts)
    
    def _calculate_potential_score(
        self,
        relevance_score: float,
        sentiment_score: float,
        behavioral_profile: Optional[BehavioralProfile],
        value_themes: List[Tuple[str, float]]
    ) -> float:
        """
        Calculate overall potential score
        """
        # Base: relevance and sentiment
        base_score = (relevance_score * 0.5) + (sentiment_score * 0.2)
        
        # Behavioral bonus
        behavioral_bonus = 0.0
        if behavioral_profile:
            # Professional maturity
            behavioral_bonus += behavioral_profile.professional_maturity * 0.15
            
            # Green flags bonus
            if behavioral_profile.green_flags:
                behavioral_bonus += min(0.1, len(behavioral_profile.green_flags) * 0.02)
            
            # Red flags penalty
            if behavioral_profile.red_flags:
                behavioral_bonus -= min(0.1, len(behavioral_profile.red_flags) * 0.02)
        
        # Value alignment bonus
        value_bonus = 0.0
        if value_themes:
            # Higher score if has clear value themes
            avg_theme_score = sum(score for _, score in value_themes[:3]) / 3
            value_bonus = avg_theme_score * 0.05
        
        total_score = base_score + behavioral_bonus + value_bonus
        return round(max(0.0, min(1.0, total_score)), 3)
    
    def _generate_recommendation(
        self,
        relevance_score: float,
        potential_score: float,
        behavioral_profile: Optional[BehavioralProfile]
    ) -> str:
        """
        Generate hiring/selection recommendation
        """
        if potential_score >= 0.75:
            recommendation = "**HIGHLY RECOMMENDED** ✅\n"
            recommendation += "Kandidat menunjukkan potensi tinggi dengan profil yang sangat sesuai."
        elif potential_score >= 0.6:
            recommendation = "**RECOMMENDED** 👍\n"
            recommendation += "Kandidat memiliki potensi baik dan layak dipertimbangkan."
        elif potential_score >= 0.45:
            recommendation = "**CONSIDER** 💭\n"
            recommendation += "Kandidat memiliki potensi moderat, perlu evaluasi lebih lanjut."
        else:
            recommendation = "**REVIEW REQUIRED** ⚠️\n"
            recommendation += "Kandidat memerlukan evaluasi mendalam sebelum keputusan."
        
        # Add key points
        if behavioral_profile:
            if behavioral_profile.green_flags:
                recommendation += f"\n\n**Kekuatan:** {len(behavioral_profile.green_flags)} indikator positif"
            
            if behavioral_profile.red_flags:
                recommendation += f"\n**Perhatian:** {len(behavioral_profile.red_flags)} area yang perlu diperhatikan"
        
        recommendation += f"\n\n**Skor Relevansi:** {relevance_score:.0%}"
        recommendation += f"\n**Skor Potensi:** {potential_score:.0%}"
        
        return recommendation
    
    def _calculate_analysis_confidence(
        self,
        texts: List[str],
        social_links: List[str],
        behavioral_profile: Optional[BehavioralProfile]
    ) -> float:
        """
        Calculate confidence level of analysis
        """
        confidence = 0.3  # Base confidence
        
        # Data availability
        if texts:
            confidence += min(0.3, len(texts) * 0.05)
        
        if social_links:
            confidence += min(0.2, len(social_links) * 0.1)
        
        # Text quality
        if texts:
            total_length = sum(len(t) for t in texts)
            if total_length > 1000:
                confidence += 0.2
            elif total_length > 500:
                confidence += 0.1
        
        # Behavioral profile completeness
        if behavioral_profile:
            confidence += 0.1
        
        return round(min(1.0, confidence), 2)


def get_advanced_employee_analyzer(use_mock_models: bool = False) -> AdvancedEmployeeAnalyzer:
    """Get advanced employee analyzer instance"""
    return AdvancedEmployeeAnalyzer(use_mock_models=use_mock_models)
