"""
Social Media Analyzer
====================
Modul untuk lookup dan analisis social media kandidat.
- Auto-search berdasarkan nama
- Profile extraction
- Content analysis
- Personality insights
"""

import re
from typing import List, Dict, Any, Optional
import warnings
warnings.filterwarnings('ignore')

try:
    from duckduckgo_search import DDGS
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False
    print("⚠️ duckduckgo_search not available. Social media search disabled.")

try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPING_AVAILABLE = True
except ImportError:
    SCRAPING_AVAILABLE = False
    print("⚠️ requests/beautifulsoup4 not available. Social media scraping disabled.")

from ai.advanced_ai_engine import get_ai_engine


class SocialMediaAnalyzer:
    """
    Analyzer untuk social media kandidat.
    """
    
    def __init__(self, ai_engine=None):
        """Initialize analyzer."""
        self.ai_engine = ai_engine or get_ai_engine()
        self.platforms = ['linkedin', 'twitter', 'instagram', 'facebook']
        print("✅ Social Media Analyzer initialized")
    
    def search_social_media(
        self,
        candidate_name: str,
        additional_info: str = ""
    ) -> Dict[str, str]:
        """
        Cari social media accounts berdasarkan nama kandidat.
        
        Args:
            candidate_name: Nama kandidat
            additional_info: Info tambahan (company, location, dll)
            
        Returns:
            Dict dengan platform -> URL
        """
        if not SEARCH_AVAILABLE:
            return {}
        
        print(f"🔍 Searching social media for: {candidate_name}")
        
        results = {}
        
        for platform in self.platforms:
            query = f"{candidate_name} {platform}"
            if additional_info:
                query += f" {additional_info}"
            
            try:
                # Search using DuckDuckGo
                with DDGS() as ddgs:
                    search_results = list(ddgs.text(query, max_results=3))
                    
                    for result in search_results:
                        url = result.get('href', '')
                        if platform in url.lower():
                            results[platform] = url
                            break
            except Exception as e:
                print(f"⚠️ Search error for {platform}: {e}")
        
        return results
    
    def extract_profile_info(
        self,
        social_media_url: str
    ) -> Dict[str, Any]:
        """
        Extract informasi dari social media profile.
        (Simplified - real implementation needs platform-specific APIs)
        
        Args:
            social_media_url: URL social media
            
        Returns:
            Dict dengan profile info
        """
        if not SCRAPING_AVAILABLE:
            return {'error': 'Scraping not available'}
        
        try:
            # Determine platform
            platform = self._detect_platform(social_media_url)
            
            # Fetch page (with proper headers)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(social_media_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return {'error': f'HTTP {response.status_code}'}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract based on platform
            if platform == 'linkedin':
                return self._extract_linkedin_info(soup)
            elif platform == 'twitter':
                return self._extract_twitter_info(soup)
            else:
                return self._extract_generic_info(soup)
        
        except Exception as e:
            print(f"⚠️ Profile extraction error: {e}")
            return {'error': str(e)}
    
    def _detect_platform(self, url: str) -> str:
        """Detect social media platform from URL."""
        url_lower = url.lower()
        for platform in self.platforms:
            if platform in url_lower:
                return platform
        return 'unknown'
    
    def _extract_linkedin_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract info dari LinkedIn (simplified)."""
        # Note: LinkedIn heavily uses JavaScript, scraping is limited
        # Real implementation should use LinkedIn API
        
        info = {
            'platform': 'linkedin',
            'bio': '',
            'headline': '',
            'location': '',
            'posts': []
        }
        
        # Try to extract headline
        headline_tag = soup.find('h2', class_=re.compile('.*headline.*'))
        if headline_tag:
            info['headline'] = headline_tag.get_text(strip=True)
        
        # Try to extract bio/summary
        summary_tag = soup.find('div', class_=re.compile('.*summary.*'))
        if summary_tag:
            info['bio'] = summary_tag.get_text(strip=True)[:500]
        
        return info
    
    def _extract_twitter_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract info dari Twitter (simplified)."""
        info = {
            'platform': 'twitter',
            'bio': '',
            'tweets': []
        }
        
        # Try to extract bio
        bio_tag = soup.find('div', attrs={'data-testid': 'UserDescription'})
        if bio_tag:
            info['bio'] = bio_tag.get_text(strip=True)
        
        return info
    
    def _extract_generic_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Generic extraction for unknown platforms."""
        # Extract all text
        text = soup.get_text(separator=' ', strip=True)
        
        return {
            'platform': 'generic',
            'text_content': text[:1000],  # First 1000 chars
        }
    
    def analyze_social_content(
        self,
        profile_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analisis konten social media dengan AI.
        
        Args:
            profile_info: Info dari extract_profile_info
            
        Returns:
            Dict dengan sentiment, personality insights, dll
        """
        # Build text untuk analisis
        text_parts = []
        
        if profile_info.get('bio'):
            text_parts.append(profile_info['bio'])
        if profile_info.get('headline'):
            text_parts.append(profile_info['headline'])
        if profile_info.get('text_content'):
            text_parts.append(profile_info['text_content'])
        
        full_text = ' '.join(text_parts)
        
        if not full_text:
            return {
                'sentiment': 'NEUTRAL',
                'sentiment_score': 0.5,
                'insights': 'Tidak ada konten untuk dianalisis'
            }
        
        # Sentiment analysis
        sentiment_result = self.ai_engine.analyze_sentiment_multilayer(
            full_text,
            aspects=['professional', 'communication']
        )
        
        # Personality detection (simplified)
        personality = self._detect_personality_traits(full_text)
        
        # Detect dominant themes
        themes = self._detect_themes(full_text)
        
        return {
            'sentiment': sentiment_result['overall_sentiment'],
            'sentiment_score': sentiment_result['overall_score'],
            'sentiment_confidence': sentiment_result['confidence'],
            'personality_traits': personality,
            'dominant_themes': themes,
            'professional_tone': sentiment_result['aspects'].get('professional', {}),
            'insights': self._generate_insights(sentiment_result, personality, themes)
        }
    
    def _detect_personality_traits(self, text: str) -> List[str]:
        """Detect personality traits dari teks."""
        traits = []
        text_lower = text.lower()
        
        trait_keywords = {
            'Analytical': ['analyze', 'data', 'research', 'study', 'investigate'],
            'Creative': ['creative', 'design', 'innovative', 'idea', 'art'],
            'Leadership': ['lead', 'manage', 'team', 'director', 'guide'],
            'Collaborative': ['collaborate', 'team', 'together', 'partnership'],
            'Detail-oriented': ['detail', 'precise', 'accurate', 'thorough'],
            'Strategic': ['strategy', 'plan', 'vision', 'goal', 'objective'],
            'Results-driven': ['achieve', 'result', 'success', 'accomplish', 'deliver']
        }
        
        for trait, keywords in trait_keywords.items():
            if sum(1 for kw in keywords if kw in text_lower) >= 2:
                traits.append(trait)
        
        return traits[:5]
    
    def _detect_themes(self, text: str) -> List[str]:
        """Detect dominant themes dari konten."""
        themes = []
        text_lower = text.lower()
        
        theme_keywords = {
            'Technology': ['tech', 'software', 'digital', 'AI', 'data'],
            'Business': ['business', 'strategy', 'market', 'growth', 'revenue'],
            'Leadership': ['lead', 'management', 'team', 'people', 'culture'],
            'Innovation': ['innovation', 'creative', 'new', 'future', 'transform'],
            'Education': ['learn', 'education', 'teaching', 'knowledge', 'training'],
            'Social Impact': ['impact', 'community', 'social', 'help', 'change']
        }
        
        theme_scores = {}
        for theme, keywords in theme_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                theme_scores[theme] = score
        
        # Sort by score
        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
        themes = [theme for theme, score in sorted_themes[:3]]
        
        return themes
    
    def _generate_insights(
        self,
        sentiment: Dict,
        personality: List[str],
        themes: List[str]
    ) -> str:
        """Generate human-readable insights."""
        insights = []
        
        # Sentiment insight
        if sentiment['overall_score'] > 0.7:
            insights.append("Menunjukkan sikap sangat positif dan proaktif di social media.")
        elif sentiment['overall_score'] > 0.5:
            insights.append("Memiliki presence profesional yang baik di social media.")
        else:
            insights.append("Tone komunikasi cenderung netral atau konservatif.")
        
        # Personality insight
        if personality:
            insights.append(f"Personality traits: {', '.join(personality[:3])}.")
        
        # Theme insight
        if themes:
            insights.append(f"Fokus utama: {', '.join(themes)}.")
        
        return ' '.join(insights)
    
    def batch_analyze_social_media(
        self,
        candidates: List[Dict[str, str]],
        progress_callback=None
    ) -> List[Dict[str, Any]]:
        """
        Batch analysis untuk multiple kandidat.
        
        Args:
            candidates: List of {'name': ..., 'company': ..., etc}
            progress_callback: Progress callback
            
        Returns:
            List of analysis results
        """
        results = []
        total = len(candidates)
        
        for idx, candidate in enumerate(candidates):
            if progress_callback:
                progress_callback(idx + 1, total, f"Analyzing {candidate.get('name', 'Unknown')}...")
            
            name = candidate.get('name', '')
            additional_info = candidate.get('company', '') or candidate.get('position', '')
            
            # Search social media
            social_urls = self.search_social_media(name, additional_info)
            
            # Analyze each platform
            analyses = {}
            for platform, url in social_urls.items():
                profile_info = self.extract_profile_info(url)
                if 'error' not in profile_info:
                    analysis = self.analyze_social_content(profile_info)
                    analyses[platform] = analysis
            
            results.append({
                'candidate_name': name,
                'social_media_urls': social_urls,
                'analyses': analyses,
                'overall_social_sentiment': self._aggregate_sentiment(analyses)
            })
        
        return results
    
    def _aggregate_sentiment(self, analyses: Dict[str, Dict]) -> Dict[str, Any]:
        """Aggregate sentiment dari multiple platforms."""
        if not analyses:
            return {'sentiment': 'NEUTRAL', 'score': 0.5}
        
        scores = [a['sentiment_score'] for a in analyses.values() if 'sentiment_score' in a]
        
        if not scores:
            return {'sentiment': 'NEUTRAL', 'score': 0.5}
        
        avg_score = sum(scores) / len(scores)
        
        if avg_score > 0.7:
            sentiment = 'POSITIVE'
        elif avg_score > 0.4:
            sentiment = 'NEUTRAL'
        else:
            sentiment = 'NEGATIVE'
        
        return {
            'sentiment': sentiment,
            'score': avg_score,
            'platforms_analyzed': len(analyses)
        }


def analyze_candidate_social_media(
    candidate_name: str,
    additional_info: str = ""
) -> Dict[str, Any]:
    """
    Helper function untuk analisis social media satu kandidat.
    
    Args:
        candidate_name: Nama kandidat
        additional_info: Info tambahan (company, position, dll)
        
    Returns:
        Analysis result
    """
    analyzer = SocialMediaAnalyzer()
    
    # Search
    social_urls = analyzer.search_social_media(candidate_name, additional_info)
    
    # Analyze
    analyses = {}
    for platform, url in social_urls.items():
        profile_info = analyzer.extract_profile_info(url)
        if 'error' not in profile_info:
            analysis = analyzer.analyze_social_content(profile_info)
            analyses[platform] = analysis
    
    return {
        'candidate_name': candidate_name,
        'social_media_urls': social_urls,
        'analyses': analyses,
        'overall_sentiment': analyzer._aggregate_sentiment(analyses)
    }
