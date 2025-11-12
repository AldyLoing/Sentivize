"""
Groq-Enhanced CV Analyzer
Deep CV analysis dengan Groq AI reasoning engine
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import os

from groq_ai_reasoner import GroqAIReasoner, get_groq_reasoner
from cv_parser import CVParser, parse_cv
from sentiment_analyzer import SentimentAnalyzer
from advanced_cv_analyzer import AdvancedCVAnalyzer


@dataclass
class CVAnalysisResult:
    """Comprehensive CV analysis result"""
    candidate_name: str
    overall_score: float
    recommendation: str
    confidence: float
    
    # Detailed scores
    technical_score: float
    experience_score: float
    education_score: float
    achievements_score: float
    relevance_score: float
    
    # Extracted info
    summary: Dict[str, Any]
    skills: Dict[str, Any]
    experience: List[Dict]
    education: List[Dict]
    
    # AI insights
    strengths: List[str]
    weaknesses: List[str]
    key_insights: List[str]
    
    # Recommendations
    hiring_decision: str
    next_steps: List[str]
    
    # Metadata
    metadata: Dict[str, Any]


class GroqCVAnalyzer:
    """
    CV Analyzer enhanced dengan Groq AI
    
    Features:
    - Deep semantic understanding of CV content
    - Context-aware skill assessment
    - Experience quality evaluation
    - Achievement impact analysis
    - Job relevance matching with reasoning
    """
    
    def __init__(
        self,
        groq_api_key: Optional[str] = None,
        use_mock_models: bool = False,
        enable_groq: bool = True
    ):
        """
        Initialize Groq CV Analyzer
        
        Args:
            groq_api_key: Groq API key
            use_mock_models: Use mock NLP models (fast mode)
            enable_groq: Enable Groq AI reasoning
        """
        self.enable_groq = enable_groq
        self.use_mock = use_mock_models
        
        # Initialize Groq reasoner
        self.groq_reasoner = None
        if enable_groq:
            try:
                self.groq_reasoner = get_groq_reasoner(api_key=groq_api_key)
                print("✅ Groq AI CV Reasoner initialized")
            except Exception as e:
                print(f"⚠️ Groq AI not available: {e}")
                print("   Falling back to traditional CV analysis...")
                self.enable_groq = False
        
        # Initialize CV parser
        self.cv_parser = CVParser()
        
        # Initialize sentiment analyzer
        self.sentiment_analyzer = SentimentAnalyzer(use_transformers=not use_mock_models)
        
        # Initialize traditional analyzer (fallback)
        self.traditional_analyzer = AdvancedCVAnalyzer(use_mock_models=use_mock_models)
    
    def analyze_cv(
        self,
        cv_file_or_text,
        filename: Optional[str] = None,
        job_description: Optional[str] = None,
        required_skills: Optional[List[str]] = None,
        company_values: Optional[List[str]] = None
    ) -> CVAnalysisResult:
        """
        Comprehensive CV analysis dengan Groq AI
        
        Args:
            cv_file_or_text: CV file path/bytes atau text langsung
            filename: Filename (jika input adalah bytes)
            job_description: Job description untuk relevance matching
            required_skills: Required skills list
            company_values: Company values untuk cultural fit
        
        Returns:
            CVAnalysisResult
        """
        
        # 1. Parse CV
        if isinstance(cv_file_or_text, str) and len(cv_file_or_text) > 500:
            # Assume it's CV text directly
            cv_text = cv_file_or_text
            parsed_cv = {
                "success": True,
                "text": cv_text,
                "sections": {},
                "metadata": {"source": "direct_text"}
            }
        else:
            # Parse from file
            parsed_cv = self.cv_parser.parse(cv_file_or_text, filename)
            
            if not parsed_cv['success']:
                return self._error_result(
                    error=parsed_cv.get('error', 'Failed to parse CV')
                )
            
            cv_text = parsed_cv['text']
        
        if not cv_text or len(cv_text) < 50:
            return self._error_result(error="CV text too short or empty")
        
        # 2. Extract contact info and basic structure
        contact_info = self.cv_parser.extract_contact_info(cv_text)
        keywords = self.cv_parser.extract_keywords(cv_text, top_n=30)
        
        # 3. Groq AI Deep Analysis
        groq_analysis = None
        
        if self.enable_groq and self.groq_reasoner:
            try:
                groq_analysis = self.groq_reasoner.analyze_cv(
                    cv_text=cv_text[:4000],  # Limit untuk API
                    job_description=job_description,
                    required_skills=required_skills
                )
                
                print("✅ Groq AI analysis completed")
                
            except Exception as e:
                print(f"⚠️ Groq analysis error: {e}")
                groq_analysis = None
        
        # 4. Traditional NLP Analysis (for supplementary data)
        traditional_result = self.traditional_analyzer.analyze_cv_with_context(
            cv_text=cv_text,
            job_description=job_description or "",
            required_skills=required_skills or []
        )
        
        # 5. Sentiment Analysis (personality indicators)
        sentiment_result = self.sentiment_analyzer.analyze(cv_text, engine="vader")
        tone_analysis = self.sentiment_analyzer.analyze_tone(cv_text)
        
        # 6. Build comprehensive result
        result = self._build_comprehensive_result(
            cv_text=cv_text,
            parsed_cv=parsed_cv,
            contact_info=contact_info,
            keywords=keywords,
            groq_analysis=groq_analysis,
            traditional_result=traditional_result,
            sentiment=sentiment_result,
            tone=tone_analysis,
            job_description=job_description,
            required_skills=required_skills
        )
        
        return result
    
    def analyze_cv_batch(
        self,
        cv_files: List[Tuple[Any, str]],
        job_description: Optional[str] = None,
        required_skills: Optional[List[str]] = None
    ) -> List[CVAnalysisResult]:
        """
        Batch CV analysis
        
        Args:
            cv_files: List of (file_data, filename) tuples
            job_description: Job description
            required_skills: Required skills
        
        Returns:
            List of CVAnalysisResult
        """
        results = []
        
        for file_data, filename in cv_files:
            try:
                result = self.analyze_cv(
                    cv_file_or_text=file_data,
                    filename=filename,
                    job_description=job_description,
                    required_skills=required_skills
                )
                results.append(result)
            except Exception as e:
                print(f"❌ Error analyzing {filename}: {e}")
                results.append(self._error_result(
                    error=str(e),
                    filename=filename
                ))
        
        return results
    
    def rank_candidates(
        self,
        results: List[CVAnalysisResult],
        ranking_criteria: Optional[Dict[str, float]] = None
    ) -> List[Tuple[CVAnalysisResult, float]]:
        """
        Rank candidates berdasarkan CV analysis
        
        Args:
            results: List of CV analysis results
            ranking_criteria: Weights untuk scoring criteria
        
        Returns:
            List of (result, rank_score) tuples, sorted by score
        """
        if not ranking_criteria:
            # Default weights
            ranking_criteria = {
                'overall_score': 0.40,
                'technical_score': 0.25,
                'experience_score': 0.20,
                'relevance_score': 0.15
            }
        
        ranked = []
        
        for result in results:
            if hasattr(result, 'overall_score'):
                rank_score = (
                    result.overall_score * ranking_criteria.get('overall_score', 0.4) +
                    result.technical_score * ranking_criteria.get('technical_score', 0.25) +
                    result.experience_score * ranking_criteria.get('experience_score', 0.2) +
                    result.relevance_score * ranking_criteria.get('relevance_score', 0.15)
                )
                ranked.append((result, rank_score))
        
        # Sort by rank score (descending)
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        return ranked
    
    def _build_comprehensive_result(
        self,
        cv_text: str,
        parsed_cv: Dict,
        contact_info: Dict,
        keywords: List[str],
        groq_analysis: Any,
        traditional_result: Any,
        sentiment: Any,
        tone: Dict,
        job_description: Optional[str],
        required_skills: Optional[List[str]]
    ) -> CVAnalysisResult:
        """Build comprehensive CV analysis result"""
        
        # Extract candidate name (from Groq or traditional)
        candidate_name = "Unknown"
        if groq_analysis and groq_analysis.metadata.get('parsed_result'):
            parsed = groq_analysis.metadata['parsed_result']
            candidate_name = parsed.get('candidate_summary', {}).get('name', candidate_name)
        elif contact_info.get('email'):
            # Try to extract from email
            candidate_name = contact_info['email'].split('@')[0].replace('.', ' ').title()
        
        # Scores
        if groq_analysis and groq_analysis.metadata.get('parsed_result'):
            parsed = groq_analysis.metadata['parsed_result']
            assessment = parsed.get('assessment_scores', {})
            
            technical_score = assessment.get('technical_skills', 70)
            experience_score = assessment.get('experience_quality', 70)
            education_score = assessment.get('education_fit', 70)
            achievements_score = assessment.get('achievements_impact', 70)
            relevance_score = assessment.get('overall_relevance', 70)
            
            overall_score = (
                technical_score * 0.30 +
                experience_score * 0.30 +
                education_score * 0.15 +
                achievements_score * 0.10 +
                relevance_score * 0.15
            )
            
            strengths = parsed.get('strengths', [])
            weaknesses = parsed.get('areas_of_concern', [])
            key_insights = parsed.get('key_insights', [])
            
            recommendation_data = parsed.get('recommendation', {})
            hiring_decision = recommendation_data.get('decision', 'Consider')
            next_steps = recommendation_data.get('next_steps', [])
            confidence = recommendation_data.get('confidence', 70)
            
        else:
            # Use traditional analyzer scores
            technical_score = traditional_result.technical_match_score
            experience_score = traditional_result.experience_quality_score
            education_score = 70.0  # Default
            achievements_score = 70.0  # Default
            relevance_score = traditional_result.overall_relevance_score
            
            overall_score = traditional_result.overall_score
            
            strengths = [f"Keyword match: {kw}" for kw in keywords[:3]]
            weaknesses = ["Analysis dilakukan tanpa Groq AI - insights terbatas"]
            key_insights = traditional_result.key_insights[:3]
            
            hiring_decision = traditional_result.recommendation
            next_steps = ["Review manual diperlukan", "Verify key qualifications"]
            confidence = traditional_result.confidence
        
        # Build summary
        summary = {
            "name": candidate_name,
            "contact": contact_info,
            "keywords": keywords[:15],
            "sentiment": sentiment.label,
            "tone": tone.get('primary_tone', 'professional'),
            "cv_length": len(cv_text),
            "word_count": len(cv_text.split())
        }
        
        # Skills (from keywords and Groq)
        skills = {
            "extracted_skills": keywords[:20],
            "matched_skills": [],
            "missing_skills": []
        }
        
        if groq_analysis and groq_analysis.metadata.get('parsed_result'):
            parsed = groq_analysis.metadata['parsed_result']
            skill_match = parsed.get('skill_match', {})
            skills['matched_skills'] = skill_match.get('matched_skills', [])
            skills['missing_skills'] = skill_match.get('missing_skills', [])
        
        # Build result
        return CVAnalysisResult(
            candidate_name=candidate_name,
            overall_score=round(overall_score, 2),
            recommendation=hiring_decision,
            confidence=round(confidence, 2),
            
            technical_score=round(technical_score, 2),
            experience_score=round(experience_score, 2),
            education_score=round(education_score, 2),
            achievements_score=round(achievements_score, 2),
            relevance_score=round(relevance_score, 2),
            
            summary=summary,
            skills=skills,
            experience=[],  # TODO: Parse experience sections
            education=[],   # TODO: Parse education sections
            
            strengths=strengths,
            weaknesses=weaknesses,
            key_insights=key_insights,
            
            hiring_decision=hiring_decision,
            next_steps=next_steps,
            
            metadata={
                "groq_enabled": self.enable_groq,
                "groq_analysis": groq_analysis is not None,
                "job_description_provided": job_description is not None,
                "required_skills_count": len(required_skills) if required_skills else 0,
                "cv_source": parsed_cv.get('metadata', {}).get('file_type', 'text')
            }
        )
    
    def _error_result(
        self,
        error: str,
        filename: Optional[str] = None
    ) -> CVAnalysisResult:
        """Return error result"""
        return CVAnalysisResult(
            candidate_name="Error",
            overall_score=0,
            recommendation="Error",
            confidence=0,
            
            technical_score=0,
            experience_score=0,
            education_score=0,
            achievements_score=0,
            relevance_score=0,
            
            summary={"error": error, "filename": filename},
            skills={},
            experience=[],
            education=[],
            
            strengths=[],
            weaknesses=[error],
            key_insights=[],
            
            hiring_decision="Error",
            next_steps=["Fix the error and try again"],
            
            metadata={"error": error}
        )


# Helper functions
def get_groq_cv_analyzer(
    groq_api_key: Optional[str] = None,
    use_mock_models: bool = True,
    enable_groq: bool = True
) -> GroqCVAnalyzer:
    """Get configured Groq CV Analyzer"""
    return GroqCVAnalyzer(
        groq_api_key=groq_api_key,
        use_mock_models=use_mock_models,
        enable_groq=enable_groq
    )


def quick_cv_score(
    cv_text: str,
    groq_api_key: Optional[str] = None
) -> float:
    """Quick CV scoring"""
    analyzer = get_groq_cv_analyzer(
        groq_api_key=groq_api_key,
        use_mock_models=True,
        enable_groq=groq_api_key is not None
    )
    
    result = analyzer.analyze_cv(cv_text)
    return result.overall_score


if __name__ == "__main__":
    print("📄 Groq CV Analyzer - Testing")
    print("=" * 60)
    
    # Sample CV text
    sample_cv = """
    JOHN DOE
    Senior Software Engineer
    john.doe@email.com | +1-555-0123 | linkedin.com/in/johndoe
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 8+ years in full-stack development,
    specializing in Python, React, and cloud infrastructure. Proven track
    record of leading technical projects and mentoring teams.
    
    EXPERIENCE
    Senior Software Engineer | Tech Corp | 2020-Present
    - Architected and implemented microservices platform serving 10M+ users
    - Led team of 5 engineers in delivering critical product features
    - Reduced deployment time by 60% through CI/CD automation
    
    Software Engineer | StartupXYZ | 2017-2020
    - Developed REST APIs and frontend applications
    - Implemented authentication and authorization systems
    - Collaborated with product team on feature specifications
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology | 2015-2017
    
    SKILLS
    Languages: Python, JavaScript, TypeScript, Java
    Frameworks: React, Django, FastAPI, Node.js
    Cloud: AWS, Docker, Kubernetes, Terraform
    Databases: PostgreSQL, MongoDB, Redis
    """
    
    # Test without Groq
    analyzer = get_groq_cv_analyzer(
        use_mock_models=True,
        enable_groq=False
    )
    
    result = analyzer.analyze_cv(
        cv_file_or_text=sample_cv,
        job_description="Senior Software Engineer with Python and React experience",
        required_skills=["Python", "React", "AWS", "Microservices"]
    )
    
    print(f"\n✅ Analysis completed!")
    print(f"Candidate: {result.candidate_name}")
    print(f"Overall Score: {result.overall_score}/100")
    print(f"Recommendation: {result.hiring_decision}")
    print(f"Confidence: {result.confidence}%")
    
    print(f"\n📊 Detailed Scores:")
    print(f"  Technical: {result.technical_score}")
    print(f"  Experience: {result.experience_score}")
    print(f"  Education: {result.education_score}")
    print(f"  Relevance: {result.relevance_score}")
    
    print(f"\n💪 Strengths:")
    for strength in result.strengths[:3]:
        print(f"  - {strength}")
    
    print(f"\n🔍 Key Insights:")
    for insight in result.key_insights[:3]:
        print(f"  - {insight}")
    
    print(f"\n📝 Next Steps:")
    for step in result.next_steps:
        print(f"  - {step}")
