"""
Sentiment Analyzer - Enhanced sentiment analysis dengan multiple engines
Mendukung VADER, TextBlob, dan Transformers untuk analisis sentimen mendalam
"""

from typing import Dict, List, Optional, Tuple
import re
from dataclasses import dataclass


@dataclass
class SentimentResult:
    """Hasil analisis sentimen"""
    label: str  # positive, negative, neutral
    score: float  # 0-100
    confidence: float  # 0-100
    details: Dict[str, float]
    engine: str


class SentimentAnalyzer:
    """
    Multi-engine sentiment analyzer
    
    Engines:
    - VADER: Rule-based, fast, good for social media
    - TextBlob: Pattern-based, good for general text
    - Transformers: ML-based, most accurate (optional)
    """
    
    def __init__(self, use_transformers: bool = False):
        """
        Initialize sentiment analyzer
        
        Args:
            use_transformers: Use transformer models (slower but more accurate)
        """
        self.use_transformers = use_transformers
        
        # Initialize engines
        self.vader_analyzer = None
        self.transformer_pipeline = None
        
        self._load_engines()
    
    def _load_engines(self):
        """Load sentiment analysis engines"""
        # VADER (always available)
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.vader_analyzer = SentimentIntensityAnalyzer()
        except ImportError:
            print("⚠️ VADER not available. Install: pip install vaderSentiment")
        
        # Transformers (optional)
        if self.use_transformers:
            try:
                from transformers import pipeline
                self.transformer_pipeline = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=-1  # CPU
                )
            except ImportError:
                print("⚠️ Transformers not available. Install: pip install transformers torch")
    
    def analyze(
        self,
        text: str,
        engine: str = "vader",
        context: Optional[str] = None
    ) -> SentimentResult:
        """
        Analyze sentiment dari text
        
        Args:
            text: Text untuk dianalisis
            engine: Engine to use (vader, textblob, transformer, auto)
            context: Context untuk contextual analysis
        
        Returns:
            SentimentResult
        """
        if not text or not text.strip():
            return SentimentResult(
                label="neutral",
                score=50.0,
                confidence=0.0,
                details={},
                engine="none"
            )
        
        # Clean text
        text_clean = self._preprocess_text(text)
        
        # Route to appropriate engine
        if engine == "vader" or engine == "auto":
            return self._analyze_vader(text_clean)
        elif engine == "textblob":
            return self._analyze_textblob(text_clean)
        elif engine == "transformer":
            return self._analyze_transformer(text_clean)
        else:
            # Fallback to VADER
            return self._analyze_vader(text_clean)
    
    def analyze_batch(
        self,
        texts: List[str],
        engine: str = "vader"
    ) -> List[SentimentResult]:
        """Analyze multiple texts"""
        return [self.analyze(text, engine=engine) for text in texts]
    
    def analyze_multi_engine(self, text: str) -> Dict[str, SentimentResult]:
        """
        Analyze dengan multiple engines dan aggregate
        
        Returns:
            Dict dengan results dari setiap engine + ensemble result
        """
        results = {}
        
        # VADER
        if self.vader_analyzer:
            results['vader'] = self._analyze_vader(text)
        
        # TextBlob
        try:
            results['textblob'] = self._analyze_textblob(text)
        except:
            pass
        
        # Transformer
        if self.use_transformers and self.transformer_pipeline:
            try:
                results['transformer'] = self._analyze_transformer(text)
            except:
                pass
        
        # Ensemble (average)
        if results:
            avg_score = sum(r.score for r in results.values()) / len(results)
            avg_confidence = sum(r.confidence for r in results.values()) / len(results)
            
            # Determine label based on average
            if avg_score > 60:
                label = "positive"
            elif avg_score < 40:
                label = "negative"
            else:
                label = "neutral"
            
            results['ensemble'] = SentimentResult(
                label=label,
                score=avg_score,
                confidence=avg_confidence,
                details={k: v.score for k, v in results.items()},
                engine="ensemble"
            )
        
        return results
    
    def _analyze_vader(self, text: str) -> SentimentResult:
        """Analyze using VADER"""
        if not self.vader_analyzer:
            return self._fallback_result()
        
        scores = self.vader_analyzer.polarity_scores(text)
        
        # Convert VADER scores (-1 to 1) to 0-100 scale
        compound = scores['compound']
        score_normalized = ((compound + 1) / 2) * 100  # -1,1 -> 0,100
        
        # Determine label
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        
        # Confidence based on magnitude
        confidence = abs(compound) * 100
        
        return SentimentResult(
            label=label,
            score=score_normalized,
            confidence=confidence,
            details={
                'positive': scores['pos'] * 100,
                'negative': scores['neg'] * 100,
                'neutral': scores['neu'] * 100,
                'compound': compound
            },
            engine="vader"
        )
    
    def _analyze_textblob(self, text: str) -> SentimentResult:
        """Analyze using TextBlob"""
        try:
            from textblob import TextBlob
            
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Convert to 0-100 scale
            score_normalized = ((polarity + 1) / 2) * 100
            
            # Determine label
            if polarity > 0.1:
                label = "positive"
            elif polarity < -0.1:
                label = "negative"
            else:
                label = "neutral"
            
            # Confidence based on subjectivity (more subjective = more confident)
            confidence = subjectivity * 100
            
            return SentimentResult(
                label=label,
                score=score_normalized,
                confidence=confidence,
                details={
                    'polarity': polarity,
                    'subjectivity': subjectivity
                },
                engine="textblob"
            )
            
        except ImportError:
            return self._fallback_result()
    
    def _analyze_transformer(self, text: str) -> SentimentResult:
        """Analyze using Transformer model"""
        if not self.transformer_pipeline:
            return self._fallback_result()
        
        try:
            # Truncate long text
            text_truncated = text[:512]
            
            result = self.transformer_pipeline(text_truncated)[0]
            
            label_raw = result['label'].lower()
            confidence_raw = result['score'] * 100
            
            # Map label
            if 'pos' in label_raw:
                label = "positive"
                score = 50 + (confidence_raw / 2)
            elif 'neg' in label_raw:
                label = "negative"
                score = 50 - (confidence_raw / 2)
            else:
                label = "neutral"
                score = 50.0
            
            return SentimentResult(
                label=label,
                score=score,
                confidence=confidence_raw,
                details={
                    'raw_label': result['label'],
                    'raw_score': result['score']
                },
                engine="transformer"
            )
            
        except Exception as e:
            print(f"⚠️ Transformer analysis failed: {e}")
            return self._fallback_result()
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text untuk sentiment analysis"""
        if not text:
            return ""
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove mentions and hashtags (but keep text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip
        text = text.strip()
        
        return text
    
    def _fallback_result(self) -> SentimentResult:
        """Fallback result when engine not available"""
        return SentimentResult(
            label="neutral",
            score=50.0,
            confidence=0.0,
            details={},
            engine="fallback"
        )
    
    def get_emotion_profile(self, text: str) -> Dict[str, float]:
        """
        Get emotion profile dari text (basic version)
        
        Returns:
            Dict dengan emotion scores
        """
        # Simple emotion keywords
        emotions = {
            'joy': ['happy', 'joy', 'excited', 'love', 'wonderful', 'amazing', 'great', 
                   'senang', 'gembira', 'bahagia', 'suka', 'hebat'],
            'sadness': ['sad', 'unhappy', 'depressed', 'disappointed', 'hurt',
                       'sedih', 'kecewa', 'sakit', 'hancur'],
            'anger': ['angry', 'mad', 'furious', 'hate', 'annoyed', 'frustrated',
                     'marah', 'kesal', 'benci', 'frustrasi'],
            'fear': ['afraid', 'scared', 'worry', 'anxious', 'nervous', 'panic',
                    'takut', 'khawatir', 'cemas', 'panik'],
            'surprise': ['surprise', 'shock', 'wow', 'amazing', 'unexpected',
                        'terkejut', 'kaget', 'wow', 'mengejutkan'],
            'trust': ['trust', 'reliable', 'honest', 'confident', 'believe',
                     'percaya', 'yakin', 'jujur', 'handal']
        }
        
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in emotions.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            emotion_scores[emotion] = min(score * 10, 100)  # Cap at 100
        
        return emotion_scores
    
    def analyze_tone(self, text: str) -> Dict[str, any]:
        """
        Analyze tone dari text (professional, casual, formal, etc.)
        
        Returns:
            Dict dengan tone analysis
        """
        text_lower = text.lower()
        
        # Indicators
        formal_indicators = ['therefore', 'however', 'furthermore', 'consequently',
                           'oleh karena itu', 'namun', 'selanjutnya', 'dengan demikian']
        casual_indicators = ['yeah', 'yup', 'cool', 'awesome', 'lol', 'btw',
                           'ya', 'sip', 'oke', 'wkwk', 'haha']
        professional_indicators = ['responsibility', 'accountability', 'strategic',
                                  'tanggung jawab', 'akuntabilitas', 'strategis']
        
        formal_count = sum(1 for ind in formal_indicators if ind in text_lower)
        casual_count = sum(1 for ind in casual_indicators if ind in text_lower)
        professional_count = sum(1 for ind in professional_indicators if ind in text_lower)
        
        # Calculate scores
        total = max(formal_count + casual_count + professional_count, 1)
        
        return {
            'formal': (formal_count / total) * 100,
            'casual': (casual_count / total) * 100,
            'professional': (professional_count / total) * 100,
            'primary_tone': max(
                [('formal', formal_count), ('casual', casual_count), 
                 ('professional', professional_count)],
                key=lambda x: x[1]
            )[0]
        }


# Helper functions
def quick_sentiment(text: str, engine: str = "vader") -> str:
    """Quick sentiment analysis - returns label only"""
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze(text, engine=engine)
    return result.label


def sentiment_score(text: str, engine: str = "vader") -> float:
    """Quick sentiment score - returns score only"""
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze(text, engine=engine)
    return result.score


def analyze_text_sentiment(text: str, detailed: bool = False) -> Dict:
    """
    Convenience function untuk sentiment analysis
    
    Args:
        text: Text to analyze
        detailed: Return detailed analysis
    
    Returns:
        Dict dengan sentiment info
    """
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze(text)
    
    if detailed:
        emotion_profile = analyzer.get_emotion_profile(text)
        tone_analysis = analyzer.analyze_tone(text)
        
        return {
            'sentiment': result.label,
            'score': result.score,
            'confidence': result.confidence,
            'details': result.details,
            'emotions': emotion_profile,
            'tone': tone_analysis
        }
    else:
        return {
            'sentiment': result.label,
            'score': result.score,
            'confidence': result.confidence
        }


if __name__ == "__main__":
    # Example usage
    print("😊 Sentiment Analyzer - Testing")
    print("=" * 60)
    
    # Test samples
    samples = [
        "I absolutely love this product! It's amazing and exceeded my expectations!",
        "This is terrible. I'm very disappointed and frustrated.",
        "The weather is okay today. Nothing special.",
        "Saya sangat senang dengan hasil kerja tim. Luar biasa!",
        "Kecewa dengan pelayanan. Tidak sesuai harapan."
    ]
    
    analyzer = SentimentAnalyzer()
    
    for i, text in enumerate(samples, 1):
        print(f"\n{i}. Text: {text}")
        result = analyzer.analyze(text)
        print(f"   Sentiment: {result.label} | Score: {result.score:.1f} | Confidence: {result.confidence:.1f}%")
        
        # Detailed analysis
        if i <= 2:  # Show details for first 2
            emotions = analyzer.get_emotion_profile(text)
            tone = analyzer.analyze_tone(text)
            print(f"   Emotions: {emotions}")
            print(f"   Tone: {tone['primary_tone']}")
    
    print("\n✅ Sentiment Analyzer test completed!")
