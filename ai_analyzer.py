"""
AI Analyzer module - Sentiment analysis dan relevance calculation menggunakan AI models
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
import config
import warnings
warnings.filterwarnings('ignore')


class AIAnalyzer:
    """
    Class untuk mengelola model AI dan melakukan analisis sentiment & relevance
    """
    
    def __init__(self, use_mock_models: bool = False):
        """
        Initialize AI models
        
        Args:
            use_mock_models: Jika True, gunakan rule-based models untuk testing cepat
        """
        self.use_mock_models = use_mock_models
        self.sentiment_pipeline = None
        self.embedding_model = None
        
        if not use_mock_models:
            self._load_transformers_models()
        else:
            self._load_mock_models()
    
    def _load_transformers_models(self):
        """Load Hugging Face Transformers models"""
        try:
            from transformers import pipeline
            from sentence_transformers import SentenceTransformer
            import torch
            
            print("Loading AI models... This may take a few minutes on first run.")
            
            # Coba load model Indonesia dulu
            try:
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model=config.SENTIMENT_MODEL,
                    device=-1  # CPU only
                )
                print(f"✓ Loaded sentiment model: {config.SENTIMENT_MODEL}")
            except Exception as e:
                print(f"Failed to load {config.SENTIMENT_MODEL}, trying fallback...")
                # Fallback ke multilingual model
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model=config.SENTIMENT_MODEL_FALLBACK,
                    device=-1
                )
                print(f"✓ Loaded fallback sentiment model: {config.SENTIMENT_MODEL_FALLBACK}")
            
            # Load embedding model
            self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
            print(f"✓ Loaded embedding model: {config.EMBEDDING_MODEL}")
            
        except Exception as e:
            print(f"Error loading transformers models: {str(e)}")
            print("Falling back to mock models...")
            self.use_mock_models = True
            self._load_mock_models()
    
    def _load_mock_models(self):
        """Load simple rule-based models untuk testing"""
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            self.vectorizer = TfidfVectorizer()
            print("✓ Loaded mock models (VADER + TF-IDF)")
            
        except Exception as e:
            print(f"Error loading mock models: {str(e)}")
            # Fallback ke simple rules
            self.sentiment_analyzer = None
            self.vectorizer = None
    
    def analyze_sentiment(self, texts: List[str]) -> Tuple[str, float]:
        """
        Analisis sentiment dari list teks
        
        Args:
            texts: List teks untuk dianalisis
            
        Returns:
            Tuple[str, float]: (sentiment_label, sentiment_score)
                sentiment_label: "POSITIVE", "NEGATIVE", atau "NEUTRAL"
                sentiment_score: float antara 0-1
        """
        if not texts or all(not t for t in texts):
            return config.SENTIMENT_NEUTRAL, 0.5
        
        # Filter empty texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if not texts:
            return config.SENTIMENT_NEUTRAL, 0.5
        
        if not self.use_mock_models and self.sentiment_pipeline:
            return self._analyze_sentiment_transformers(texts)
        else:
            return self._analyze_sentiment_mock(texts)
    
    def _analyze_sentiment_transformers(self, texts: List[str]) -> Tuple[str, float]:
        """Sentiment analysis menggunakan Transformers"""
        try:
            scores = []
            labels = []
            
            for text in texts[:config.MAX_POSTS_PER_ACCOUNT]:
                # Truncate text
                text = text[:config.MAX_TEXT_LENGTH]
                
                result = self.sentiment_pipeline(text)[0]
                label = result['label'].upper()
                score = result['score']
                
                # Normalize label
                if 'POS' in label or '4' in label or '5' in label:
                    labels.append(config.SENTIMENT_POSITIVE)
                    scores.append(score)
                elif 'NEG' in label or '1' in label or '2' in label:
                    labels.append(config.SENTIMENT_NEGATIVE)
                    scores.append(1 - score)  # Invert negative score
                else:
                    labels.append(config.SENTIMENT_NEUTRAL)
                    scores.append(0.5)
            
            # Aggregate results
            if not scores:
                return config.SENTIMENT_NEUTRAL, 0.5
            
            avg_score = np.mean(scores)
            
            # Determine overall label
            positive_count = labels.count(config.SENTIMENT_POSITIVE)
            negative_count = labels.count(config.SENTIMENT_NEGATIVE)
            
            if positive_count > negative_count:
                final_label = config.SENTIMENT_POSITIVE
            elif negative_count > positive_count:
                final_label = config.SENTIMENT_NEGATIVE
            else:
                final_label = config.SENTIMENT_NEUTRAL
            
            return final_label, float(avg_score)
            
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return config.SENTIMENT_NEUTRAL, 0.5
    
    def _analyze_sentiment_mock(self, texts: List[str]) -> Tuple[str, float]:
        """Sentiment analysis menggunakan VADER (mock)"""
        try:
            if self.sentiment_analyzer:
                scores = []
                for text in texts[:config.MAX_POSTS_PER_ACCOUNT]:
                    vs = self.sentiment_analyzer.polarity_scores(text)
                    compound = vs['compound']
                    scores.append(compound)
                
                avg_compound = np.mean(scores)
                
                # Convert compound score (-1 to 1) to 0-1 scale
                normalized_score = (avg_compound + 1) / 2
                
                if avg_compound >= 0.05:
                    label = config.SENTIMENT_POSITIVE
                elif avg_compound <= -0.05:
                    label = config.SENTIMENT_NEGATIVE
                else:
                    label = config.SENTIMENT_NEUTRAL
                
                return label, float(normalized_score)
            else:
                # Very simple rule-based
                combined_text = " ".join(texts).lower()
                positive_words = ['baik', 'bagus', 'hebat', 'excellent', 'good', 'great', 
                                'sukses', 'positif', 'senang', 'happy']
                negative_words = ['buruk', 'jelek', 'bad', 'poor', 'negatif', 'sedih', 
                                'sad', 'gagal', 'fail']
                
                pos_count = sum(1 for word in positive_words if word in combined_text)
                neg_count = sum(1 for word in negative_words if word in combined_text)
                
                if pos_count > neg_count:
                    return config.SENTIMENT_POSITIVE, 0.7
                elif neg_count > pos_count:
                    return config.SENTIMENT_NEGATIVE, 0.3
                else:
                    return config.SENTIMENT_NEUTRAL, 0.5
                    
        except Exception as e:
            print(f"Error in mock sentiment analysis: {str(e)}")
            return config.SENTIMENT_NEUTRAL, 0.5
    
    def calculate_relevance(self, texts: List[str], keyword: str) -> float:
        """
        Hitung relevansi teks terhadap keyword menggunakan semantic similarity
        
        Args:
            texts: List teks untuk dianalisis
            keyword: Kata kunci target
            
        Returns:
            float: Relevance score antara 0-1
        """
        if not texts or not keyword or all(not t for t in texts):
            return 0.0
        
        # Filter empty texts
        texts = [t for t in texts if t and len(t.strip()) > 0]
        if not texts:
            return 0.0
        
        if not self.use_mock_models and self.embedding_model:
            return self._calculate_relevance_transformers(texts, keyword)
        else:
            return self._calculate_relevance_mock(texts, keyword)
    
    def calculate_relevance_with_reasoning(
        self, 
        texts: List[str], 
        keyword: str,
        name: str,
        position: Optional[str],
        unit: Optional[str]
    ) -> Tuple[float, str]:
        """
        Hitung relevansi dengan alasan detail
        
        Args:
            texts: List teks untuk dianalisis
            keyword: Kata kunci target
            name: Nama kandidat
            position: Jabatan kandidat
            unit: Unit kerja kandidat
            
        Returns:
            Tuple[float, str]: (relevance_score, reasoning)
        """
        # Calculate base relevance
        relevance_score = self.calculate_relevance(texts, keyword)
        
        # Generate reasoning
        reasoning_parts = []
        
        # Analyze keyword/phrase presence in different contexts
        keyword_lower = keyword.lower()
        combined_text = " ".join(texts).lower() if texts else ""
        
        # Extract keywords/phrases (support multi-word phrases)
        keyword_phrases = self._extract_keyword_phrases(keyword_lower)
        
        # Check in position
        position_match = False
        position_matches = []
        if position and position != '-':
            position_lower = position.lower()
            for phrase in keyword_phrases:
                if phrase in position_lower:
                    position_matches.append(phrase)
                    position_match = True
            
            if position_matches:
                if len(position_matches) == 1:
                    reasoning_parts.append(f"Kata kunci '{position_matches[0]}' ditemukan di jabatan: {position}")
                else:
                    reasoning_parts.append(f"Kata kunci '{', '.join(position_matches)}' ditemukan di jabatan: {position}")
        
        # Check in unit
        unit_match = False
        unit_matches = []
        if unit and unit != '-':
            unit_lower = unit.lower()
            for phrase in keyword_phrases:
                if phrase in unit_lower:
                    unit_matches.append(phrase)
                    unit_match = True
            
            if unit_matches:
                if len(unit_matches) == 1:
                    reasoning_parts.append(f"Kata kunci '{unit_matches[0]}' ditemukan di unit: {unit}")
                else:
                    reasoning_parts.append(f"Kata kunci '{', '.join(unit_matches)}' ditemukan di unit: {unit}")
        
        # Check in texts - support phrase and sentence matching
        if combined_text:
            # Count exact phrase matches
            phrase_matches = {}
            for phrase in keyword_phrases:
                count = combined_text.count(phrase)
                if count > 0:
                    phrase_matches[phrase] = count
            
            if phrase_matches:
                if len(phrase_matches) == 1:
                    phrase, count = list(phrase_matches.items())[0]
                    reasoning_parts.append(f"'{phrase}' muncul {count}x dalam konten")
                else:
                    match_descriptions = [f"'{phrase}' ({count}x)" for phrase, count in phrase_matches.items()]
                    reasoning_parts.append(f"Ditemukan: {', '.join(match_descriptions)}")
            
            # Check for individual words if no phrase matches
            if not phrase_matches:
                related_found = []
                keyword_words = keyword_lower.split()
                word_counts = {}
                for word in keyword_words:
                    if len(word) > 3:  # Skip common short words
                        count = combined_text.count(word)
                        if count > 0:
                            word_counts[word] = count
                            related_found.append(word)
                
                if related_found:
                    if len(related_found) == 1:
                        word = related_found[0]
                        reasoning_parts.append(f"Kata '{word}' ditemukan {word_counts[word]}x dalam konten")
                    else:
                        word_descriptions = [f"'{w}' ({word_counts[w]}x)" for w in related_found]
                        reasoning_parts.append(f"Kata terkait: {', '.join(word_descriptions)}")
        
        # Add semantic reasoning for high scores without explicit matches
        if relevance_score >= 0.7:
            if not reasoning_parts:
                reasoning_parts.append("Konten sangat relevan berdasarkan analisis semantik (kesamaan makna tinggi)")
            else:
                reasoning_parts.append("Analisis semantik menunjukkan kesamaan makna yang tinggi")
        elif relevance_score >= 0.5:
            if not reasoning_parts:
                reasoning_parts.append("Konten memiliki relevansi sedang berdasarkan kesamaan konteks")
            elif relevance_score >= 0.6:
                reasoning_parts.append("Kesamaan konteks dan makna cukup kuat")
        elif relevance_score >= 0.3:
            if not reasoning_parts:
                reasoning_parts.append("Relevansi terbatas, namun ada beberapa kesamaan topik atau konteks")
        else:
            if not reasoning_parts:
                if self._is_sentence_or_phrase(keyword):
                    reasoning_parts.append(f"Konten kurang relevan dengan maksud '{keyword}'")
                else:
                    reasoning_parts.append(f"Konten kurang relevan dengan kata kunci '{keyword}'")
        
        # Combine reasoning
        if reasoning_parts:
            reasoning = ". ".join(reasoning_parts) + "."
        else:
            reasoning = f"Tidak ditemukan konten yang relevan dengan '{keyword}'."
        
        return relevance_score, reasoning
    
    def _extract_keyword_phrases(self, keyword: str) -> List[str]:
        """
        Extract phrases dari keyword (support multi-word phrases)
        Returns list of phrases/words to search for
        """
        phrases = []
        
        # Add full keyword as a phrase
        phrases.append(keyword.strip())
        
        # Extract n-grams (2-5 words) if keyword is a sentence
        words = keyword.split()
        if len(words) >= 2:
            # Add bigrams
            for i in range(len(words) - 1):
                bigram = f"{words[i]} {words[i+1]}"
                if bigram not in phrases:
                    phrases.append(bigram)
            
            # Add trigrams if sentence is long enough
            if len(words) >= 3:
                for i in range(len(words) - 2):
                    trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
                    if trigram not in phrases:
                        phrases.append(trigram)
        
        return phrases
    
    def _is_sentence_or_phrase(self, keyword: str) -> bool:
        """Check if keyword is a sentence/phrase (has multiple words)"""
        return len(keyword.split()) > 2
    
    def _calculate_relevance_transformers(self, texts: List[str], keyword: str) -> float:
        """Calculate relevance menggunakan sentence-transformers"""
        try:
            # Truncate texts
            texts = [t[:config.MAX_TEXT_LENGTH] for t in texts[:config.MAX_POSTS_PER_ACCOUNT]]
            
            # Encode texts and keyword
            text_embeddings = self.embedding_model.encode(texts)
            keyword_embedding = self.embedding_model.encode([keyword])
            
            # Calculate cosine similarities
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(text_embeddings, keyword_embedding)
            
            # Average similarity
            avg_similarity = np.mean(similarities)
            
            # Normalize to 0-1 (cosine similarity is already -1 to 1, but usually 0 to 1)
            relevance_score = float(max(0, min(1, avg_similarity)))
            
            return relevance_score
            
        except Exception as e:
            print(f"Error in relevance calculation: {str(e)}")
            return 0.0
    
    def _calculate_relevance_mock(self, texts: List[str], keyword: str) -> float:
        """Calculate relevance menggunakan TF-IDF (mock) - supports phrases and sentences"""
        try:
            if self.vectorizer:
                # Combine texts
                combined_text = " ".join(texts[:config.MAX_POSTS_PER_ACCOUNT])
                
                # Fit TF-IDF with keyword (phrase-aware)
                corpus = [combined_text, keyword]
                tfidf_matrix = self.vectorizer.fit_transform(corpus)
                
                # Calculate cosine similarity
                from sklearn.metrics.pairwise import cosine_similarity
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                
                # Boost score if exact phrase found
                keyword_lower = keyword.lower()
                combined_lower = combined_text.lower()
                if keyword_lower in combined_lower:
                    phrase_bonus = min(0.3, combined_lower.count(keyword_lower) * 0.1)
                    similarity = min(1.0, similarity + phrase_bonus)
                
                return float(max(0, min(1, similarity)))
            else:
                # Enhanced keyword matching for phrases and sentences
                combined_text = " ".join(texts).lower()
                keyword_lower = keyword.lower()
                
                score = 0.0
                
                # 1. Check for exact phrase match (highest weight)
                if keyword_lower in combined_text:
                    count = combined_text.count(keyword_lower)
                    score += min(0.6, count * 0.2)  # Up to 0.6 for exact matches
                
                # 2. Extract and check n-grams from keyword
                words = keyword_lower.split()
                if len(words) >= 2:
                    # Check bigrams
                    bigram_matches = 0
                    for i in range(len(words) - 1):
                        bigram = f"{words[i]} {words[i+1]}"
                        if bigram in combined_text:
                            bigram_matches += 1
                    
                    if bigram_matches > 0:
                        bigram_score = min(0.3, (bigram_matches / (len(words) - 1)) * 0.3)
                        score += bigram_score
                
                # 3. Check individual word matches (lower weight)
                if score < 0.3:  # Only if no phrase matches
                    word_matches = 0
                    significant_words = [w for w in words if len(w) > 3]
                    
                    if significant_words:
                        for word in significant_words:
                            if word in combined_text:
                                word_matches += 1
                        
                        word_score = (word_matches / len(significant_words)) * 0.4
                        score += word_score
                
                # 4. Bonus for word order preservation
                if len(words) >= 3 and score > 0.2:
                    # Check if words appear in similar order
                    positions = []
                    for word in words[:5]:  # Check first 5 words
                        if word in combined_text:
                            positions.append(combined_text.find(word))
                    
                    if len(positions) >= 2:
                        # Check if positions are increasing (same order)
                        is_ordered = all(positions[i] < positions[i+1] for i in range(len(positions)-1))
                        if is_ordered:
                            score += 0.1  # Order bonus
                
                return float(max(0, min(1, score)))
                    
        except Exception as e:
            print(f"Error in mock relevance calculation: {str(e)}")
            return 0.0


# Singleton instance
_analyzer_instance = None


def get_analyzer(use_mock_models: bool = False) -> AIAnalyzer:
    """
    Get atau create singleton instance of AIAnalyzer
    
    Args:
        use_mock_models: Jika True, gunakan mock models
        
    Returns:
        AIAnalyzer: Instance analyzer
    """
    global _analyzer_instance
    
    if _analyzer_instance is None:
        _analyzer_instance = AIAnalyzer(use_mock_models=use_mock_models)
    
    return _analyzer_instance
