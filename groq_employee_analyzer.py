"""
Groq-Enhanced Employee Analyzer
Integrates Groq AI reasoning dengan existing advanced analyzer
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import os

from groq_ai_reasoner import GroqAIReasoner, get_groq_reasoner
from sentiment_analyzer import SentimentAnalyzer, analyze_text_sentiment
from advanced_employee_analyzer import (
    AdvancedEmployeeAnalyzer,
    EmployeeAnalysisResult,
    BehavioralProfile
)


class GroqEmployeeAnalyzer:
    """
    Employee Analyzer enhanced dengan Groq AI
    
    Combines:
    - Groq AI untuk deep reasoning dan personality assessment
    - Advanced NLP untuk entity extraction dan topic modeling
    - Multi-engine sentiment analysis
    """
    
    def __init__(
        self,
        groq_api_key: Optional[str] = None,
        use_mock_models: bool = False,
        enable_groq: bool = True
    ):
        """
        Initialize Groq-enhanced analyzer
        
        Args:
            groq_api_key: Groq API key
            use_mock_models: Use mock models untuk NLP (fast mode)
            enable_groq: Enable Groq AI reasoning (disable untuk fallback mode)
        """
        self.enable_groq = enable_groq
        self.use_mock = use_mock_models
        
        # Initialize Groq reasoner (if enabled and API key available)
        self.groq_reasoner = None
        if enable_groq:
            try:
                self.groq_reasoner = get_groq_reasoner(api_key=groq_api_key)
                print("✅ Groq AI Reasoner initialized")
            except Exception as e:
                print(f"⚠️ Groq AI not available: {e}")
                print("   Falling back to traditional NLP...")
                self.enable_groq = False
        
        # Initialize sentiment analyzer
        self.sentiment_analyzer = SentimentAnalyzer(use_transformers=not use_mock_models)
        
        # Initialize traditional advanced analyzer (fallback)
        self.traditional_analyzer = AdvancedEmployeeAnalyzer(use_mock_models=use_mock_models)
    
    def analyze_employee(
        self,
        name: str,
        position: Optional[str] = None,
        unit: Optional[str] = None,
        bio: Optional[str] = None,
        social_posts: Optional[List[str]] = None,
        social_links: Optional[List[str]] = None,
        keyword: Optional[str] = None,
        company_values: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive employee analysis dengan Groq AI
        
        Args:
            name: Nama karyawan/kandidat
            position: Jabatan
            unit: Unit kerja
            bio: Bio/deskripsi personal
            social_posts: List social media posts
            social_links: Social media links
            keyword: Keyword untuk relevance matching
            company_values: Company values untuk cultural fit
        
        Returns:
            Dict dengan comprehensive analysis results
        """
        
        # Prepare data
        texts = []
        if bio:
            texts.append(bio)
        if social_posts:
            texts.extend(social_posts)
        
        if not texts:
            return self._empty_result(name, "Tidak ada data untuk dianalisis")
        
        # 1. Sentiment Analysis (multi-engine)
        combined_text = " ".join(texts)
        sentiment_results = self.sentiment_analyzer.analyze_multi_engine(combined_text)
        primary_sentiment = sentiment_results.get('ensemble', sentiment_results.get('vader'))
        
        emotion_profile = self.sentiment_analyzer.get_emotion_profile(combined_text)
        tone_analysis = self.sentiment_analyzer.analyze_tone(combined_text)
        
        # 2. Groq AI Deep Analysis (if available)
        groq_analysis = None
        personality_assessment = None
        cultural_fit = None
        
        if self.enable_groq and self.groq_reasoner:
            try:
                # Build employee data for Groq
                employee_data = {
                    "name": name,
                    "position": position,
                    "unit": unit,
                    "bio": bio,
                    "social_posts": social_posts[:10] if social_posts else [],  # Limit to 10 posts
                    "social_links": social_links
                }
                
                # Deep behavioral analysis
                groq_response = self.groq_reasoner.analyze_employee(
                    employee_data=employee_data,
                    focus_areas=["personality", "values", "behavior", "professional_fit"]
                )
                
                groq_analysis = groq_response.metadata.get('parsed_result', {})
                
                # Personality assessment
                personality_assessment = self.groq_reasoner.assess_personality(
                    text_data=combined_text[:2000],  # Limit untuk API
                    context="professional"
                )
                
                # Cultural fit (if company values provided)
                if company_values:
                    candidate_profile = {
                        "name": name,
                        "values": groq_analysis.get('core_values', []),
                        "traits": groq_analysis.get('personality_traits', {}),
                        "behavior": groq_analysis.get('behavioral_patterns', [])
                    }
                    
                    cultural_fit = self.groq_reasoner.evaluate_cultural_fit(
                        candidate_profile=candidate_profile,
                        company_values=company_values
                    )
                
            except Exception as e:
                print(f"⚠️ Groq analysis error: {e}")
                groq_analysis = {"error": str(e)}
        
        # 3. Traditional NLP Analysis (for topics, entities, etc.)
        traditional_result = self.traditional_analyzer.analyze_employee_comprehensive(
            name=name,
            position=position,
            unit=unit,
            texts=texts,
            social_links=social_links or [],
            keyword=keyword or "",
            enable_behavioral_analysis=True
        )
        
        # 4. Relevance Scoring (with keyword if provided)
        relevance_score = 0.0
        relevance_reasoning = ""
        
        if keyword:
            relevance_score = traditional_result.relevance_score
            relevance_reasoning = traditional_result.relevance_reasoning
        
        # 5. Aggregate scores
        overall_score = self._calculate_overall_score(
            sentiment_score=primary_sentiment.score,
            relevance_score=relevance_score,
            groq_score=groq_analysis.get('overall_score', 70) if groq_analysis else 70,
            potential_score=traditional_result.potential_score
        )
        
        # 6. Generate insights
        key_insights = self._generate_insights(
            name=name,
            sentiment=primary_sentiment,
            groq_analysis=groq_analysis,
            personality=personality_assessment,
            traditional=traditional_result
        )
        
        # 7. Generate recommendation
        recommendation = self._generate_comprehensive_recommendation(
            overall_score=overall_score,
            groq_analysis=groq_analysis,
            cultural_fit=cultural_fit,
            traditional=traditional_result
        )
        
        # Build comprehensive result
        result = {
            "candidate_info": {
                "name": name,
                "position": position,
                "unit": unit,
                "social_links": social_links or []
            },
            
            "scores": {
                "overall_score": overall_score,
                "sentiment_score": primary_sentiment.score,
                "relevance_score": relevance_score,
                "potential_score": traditional_result.potential_score,
                "confidence": traditional_result.confidence
            },
            
            "sentiment_analysis": {
                "primary_sentiment": primary_sentiment.label,
                "sentiment_score": primary_sentiment.score,
                "sentiment_confidence": primary_sentiment.confidence,
                "emotions": emotion_profile,
                "tone": tone_analysis,
                "sentiment_engines": {
                    k: {"label": v.label, "score": v.score}
                    for k, v in sentiment_results.items()
                }
            },
            
            "personality_profile": personality_assessment if personality_assessment else {
                "source": "traditional",
                "traits": traditional_result.behavioral_profile.personality.traits
                if traditional_result.behavioral_profile else {}
            },
            
            "groq_analysis": groq_analysis if groq_analysis else {
                "available": False,
                "note": "Groq AI tidak aktif atau tidak tersedia"
            },
            
            "cultural_fit": cultural_fit if cultural_fit else None,
            
            "value_themes": [
                {"theme": theme, "score": score}
                for theme, score in traditional_result.value_themes
            ],
            
            "behavioral_insights": {
                "character_assessment": traditional_result.character_assessment,
                "behavioral_patterns": (
                    traditional_result.behavioral_profile.behavioral_profile.behavior_patterns
                    if traditional_result.behavioral_profile else []
                ),
                "red_flags": (
                    traditional_result.behavioral_profile.red_flags
                    if traditional_result.behavioral_profile else []
                ),
                "green_flags": (
                    traditional_result.behavioral_profile.green_flags
                    if traditional_result.behavioral_profile else []
                )
            },
            
            "key_insights": key_insights,
            
            "recommendation": recommendation,
            
            "metadata": {
                "groq_enabled": self.enable_groq,
                "groq_available": self.groq_reasoner is not None,
                "analysis_mode": "groq_enhanced" if self.enable_groq else "traditional",
                "text_analyzed": len(texts),
                "total_characters": len(combined_text)
            }
        }
        
        return result
    
    def _calculate_overall_score(
        self,
        sentiment_score: float,
        relevance_score: float,
        groq_score: float,
        potential_score: float
    ) -> float:
        """Calculate weighted overall score"""
        
        # Weights
        weights = {
            'sentiment': 0.25,
            'relevance': 0.25,
            'groq': 0.30,
            'potential': 0.20
        }
        
        # Normalize scores to 0-100
        scores = {
            'sentiment': sentiment_score,
            'relevance': relevance_score * 100,
            'groq': groq_score,
            'potential': potential_score
        }
        
        # Weighted average
        overall = sum(scores[k] * weights[k] for k in weights.keys())
        
        return round(overall, 2)
    
    def _generate_insights(
        self,
        name: str,
        sentiment: Any,
        groq_analysis: Optional[Dict],
        personality: Optional[Dict],
        traditional: EmployeeAnalysisResult
    ) -> List[str]:
        """Generate key insights dari analysis"""
        
        insights = []
        
        # Sentiment insight
        if sentiment.label == "positive":
            insights.append(f"🌟 {name} menunjukkan sikap positif dan optimis dalam komunikasi digital")
        elif sentiment.label == "negative":
            insights.append(f"⚠️ {name} cenderung mengekspresikan sentimen negatif - perlu investigasi lebih lanjut")
        
        # Groq insights
        if groq_analysis and 'key_insights' in groq_analysis:
            insights.extend(groq_analysis['key_insights'][:3])  # Top 3
        
        # Personality insights
        if personality and 'key_characteristics' in personality:
            chars = personality['key_characteristics'][:2]
            if chars:
                insights.append(f"🧠 Karakteristik utama: {', '.join(chars)}")
        
        # Value themes
        if traditional.value_themes:
            top_value = traditional.value_themes[0][0]
            insights.append(f"💎 Value dominan: {top_value}")
        
        return insights[:5]  # Limit to 5 insights
    
    def _generate_comprehensive_recommendation(
        self,
        overall_score: float,
        groq_analysis: Optional[Dict],
        cultural_fit: Optional[Dict],
        traditional: EmployeeAnalysisResult
    ) -> Dict[str, Any]:
        """Generate comprehensive hiring recommendation"""
        
        # Determine decision
        if overall_score >= 80:
            decision = "🌟 Strong Hire"
            level = "excellent"
        elif overall_score >= 65:
            decision = "✅ Hire"
            level = "good"
        elif overall_score >= 50:
            decision = "🤔 Consider"
            level = "moderate"
        else:
            decision = "❌ Pass"
            level = "poor"
        
        # Reasoning
        reasoning_parts = []
        
        if overall_score >= 70:
            reasoning_parts.append("Kandidat menunjukkan profil yang kuat secara keseluruhan")
        
        if groq_analysis and groq_analysis.get('overall_score', 0) >= 75:
            reasoning_parts.append("AI assessment menunjukkan personality dan behavioral fit yang baik")
        
        if cultural_fit and cultural_fit.get('cultural_fit_score', 0) >= 70:
            reasoning_parts.append("Cultural fit sangat baik dengan organizational values")
        
        reasoning = ". ".join(reasoning_parts) if reasoning_parts else traditional.recommendation
        
        # Next steps
        next_steps = []
        
        if level in ["excellent", "good"]:
            next_steps = [
                "Lanjutkan ke tahap interview",
                "Konfirmasi technical competencies",
                "Reference check"
            ]
        elif level == "moderate":
            next_steps = [
                "Deep dive interview untuk validate concerns",
                "Assess specific competency gaps",
                "Consider untuk role yang lebih sesuai"
            ]
        else:
            next_steps = [
                "Archive application",
                "Keep in talent pool untuk future opportunities"
            ]
        
        return {
            "decision": decision,
            "level": level,
            "overall_score": overall_score,
            "reasoning": reasoning,
            "next_steps": next_steps,
            "confidence": traditional.confidence
        }
    
    def _empty_result(self, name: str, reason: str) -> Dict[str, Any]:
        """Return empty result structure"""
        return {
            "candidate_info": {"name": name},
            "scores": {"overall_score": 0},
            "error": reason,
            "recommendation": {
                "decision": "⚠️ Insufficient Data",
                "reasoning": reason
            }
        }


# Helper function
def get_groq_employee_analyzer(
    groq_api_key: Optional[str] = None,
    use_mock_models: bool = True,
    enable_groq: bool = True
) -> GroqEmployeeAnalyzer:
    """Get configured Groq Employee Analyzer"""
    return GroqEmployeeAnalyzer(
        groq_api_key=groq_api_key,
        use_mock_models=use_mock_models,
        enable_groq=enable_groq
    )


if __name__ == "__main__":
    print("🚀 Groq Employee Analyzer - Testing")
    print("=" * 60)
    
    # Test with sample data
    analyzer = get_groq_employee_analyzer(
        use_mock_models=True,
        enable_groq=False  # Test without Groq first
    )
    
    result = analyzer.analyze_employee(
        name="John Doe",
        position="Software Engineer",
        bio="Passionate about clean code and sustainable technology. Love building scalable systems.",
        social_posts=[
            "Just shipped a new microservice architecture! Team collaboration was key.",
            "Learning Rust - loving the memory safety guarantees.",
            "Weekend hackathon was amazing - built an AI-powered code reviewer."
        ],
        keyword="software development",
        company_values=["innovation", "collaboration", "excellence"]
    )
    
    print(f"\n✅ Analysis completed!")
    print(f"Overall Score: {result['scores']['overall_score']}")
    print(f"Sentiment: {result['sentiment_analysis']['primary_sentiment']}")
    print(f"Recommendation: {result['recommendation']['decision']}")
    print(f"\nKey Insights:")
    for insight in result['key_insights']:
        print(f"  - {insight}")
