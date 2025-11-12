"""
Groq AI Reasoner - Core reasoning engine menggunakan Groq API
Fast, powerful, and contextual AI analysis untuk HR analytics
"""

import os
from typing import Dict, List, Optional, Any
import json
from dataclasses import dataclass, asdict
from groq import Groq


@dataclass
class AIResponse:
    """Struktur response dari AI"""
    content: str
    reasoning: str
    confidence: float
    insights: List[str]
    metadata: Dict[str, Any]


class GroqAIReasoner:
    """
    Groq AI Reasoner untuk analisis HR yang cerdas dan kontekstual
    
    Features:
    - Deep contextual understanding (Indonesian & English)
    - Behavioral profiling
    - Professional assessment
    - Cultural fit analysis
    - Multi-dimensional reasoning
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        model: str = "llama3-8b-8192",
        temperature: float = 0.7
    ):
        """
        Initialize Groq AI Reasoner
        
        Args:
            api_key: Groq API key (default: dari environment variable GROQ_API_KEY)
            model: Model yang digunakan (llama3-8b-8192, gemma-7b-it, mixtral-8x7b-32768)
            temperature: Kreativitas response (0-1, default 0.7)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "❌ Groq API key tidak ditemukan!\n"
                "Set environment variable: GROQ_API_KEY=your_api_key\n"
                "Atau passing api_key saat inisialisasi."
            )
        
        self.client = Groq(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        
        # System prompts untuk berbagai jenis analisis
        self.system_prompts = {
            "employee": """Kamu adalah AI HR Profesional dengan keahlian dalam psikologi kerja, 
            analisis perilaku, dan people analytics. Kamu memahami konteks sosial, 
            budaya kerja Indonesia, dan dapat mengidentifikasi nilai-nilai personal, 
            kepribadian, dan potensi profesional seseorang dari aktivitas digital mereka.
            
            Analisis kamu harus:
            - Mendalam dan kontekstual
            - Objektif namun empatis
            - Berbasis evidence yang jelas
            - Memberikan insight actionable
            - Mempertimbangkan budaya Indonesia dan global
            
            Berikan analisis dalam Bahasa Indonesia yang profesional namun mudah dipahami.""",
            
            "cv": """Kamu adalah AI CV Reviewer ahli dengan pengalaman dalam talent acquisition, 
            technical recruitment, dan professional development. Kamu dapat menganalisis CV/resume 
            dengan mendalam untuk menilai:
            - Kesesuaian dengan job requirements
            - Kualitas pengalaman dan pencapaian
            - Technical dan soft skills
            - Potensi dan trajectory karir
            - Red flags dan areas of concern
            
            Analisis kamu harus:
            - Komprehensif dan detail
            - Fair dan objektif
            - Memberikan scoring yang jelas
            - Menyertakan rekomendasi konkret
            - Bilingual (Indonesia & English)
            
            Berikan analisis profesional yang actionable untuk HR decision making.""",
            
            "personality": """Kamu adalah AI Personality Psychologist yang memahami trait psychology,
            behavioral patterns, dan professional personality assessment. Kamu dapat mengidentifikasi:
            - Big Five personality traits
            - Work style preferences
            - Leadership potential
            - Team dynamics fit
            - Communication patterns
            - Motivational drivers
            
            Analisis kamu scientific-based namun praktis untuk workplace context.""",
            
            "cultural_fit": """Kamu adalah AI Organizational Psychologist yang ahli dalam 
            cultural assessment, values alignment, dan organizational behavior. 
            Kamu dapat mengevaluasi cultural fit berdasarkan:
            - Core values alignment
            - Work culture preferences
            - Collaboration style
            - Adaptability indicators
            - Long-term compatibility
            
            Berikan analisis yang membantu hiring decision dengan pertimbangan cultural context."""
        }
    
    def analyze_employee(
        self,
        employee_data: Dict[str, Any],
        focus_areas: Optional[List[str]] = None
    ) -> AIResponse:
        """
        Analisis karyawan/kandidat secara mendalam
        
        Args:
            employee_data: Data karyawan (nama, jabatan, bio, social posts, etc)
            focus_areas: Area fokus analisis (personality, values, behavior, fit)
        
        Returns:
            AIResponse dengan analisis komprehensif
        """
        # Default focus areas
        if not focus_areas:
            focus_areas = ["personality", "values", "behavior", "professional_fit"]
        
        # Build context dari employee data
        context = self._build_employee_context(employee_data)
        
        # Create user prompt
        user_prompt = f"""
Analisis kandidat berikut secara mendalam:

**DATA KANDIDAT:**
{context}

**AREA ANALISIS:**
{', '.join(focus_areas)}

**TASKS:**
1. Identifikasi personality traits dan behavioral patterns
2. Ekstrak core values dan motivasi personal
3. Assess profesionalitas dan work ethics
4. Evaluasi communication style dan social presence
5. Berikan overall profiling dengan confidence score

**OUTPUT FORMAT (JSON):**
{{
    "personality_traits": {{
        "trait_name": score (0-100),
        ...
    }},
    "core_values": ["value1", "value2", ...],
    "behavioral_patterns": ["pattern1", "pattern2", ...],
    "professional_assessment": {{
        "work_ethics": score,
        "communication": score,
        "leadership_potential": score,
        "team_fit": score
    }},
    "key_insights": ["insight1", "insight2", ...],
    "overall_score": score (0-100),
    "confidence": score (0-100),
    "reasoning": "detailed explanation"
}}

Berikan analisis yang objektif, evidence-based, dan actionable.
"""
        
        # Call Groq API
        response = self._call_groq_api(
            system_prompt=self.system_prompts["employee"],
            user_prompt=user_prompt
        )
        
        # Parse dan struktur response
        return self._parse_employee_response(response, employee_data)
    
    def analyze_cv(
        self,
        cv_text: str,
        job_description: Optional[str] = None,
        required_skills: Optional[List[str]] = None
    ) -> AIResponse:
        """
        Analisis CV/Resume dengan scoring dan recommendations
        
        Args:
            cv_text: Full text dari CV
            job_description: Job description untuk relevance matching
            required_skills: List required skills untuk assessment
        
        Returns:
            AIResponse dengan detailed CV analysis
        """
        # Build context
        context = f"**CV TEXT:**\n{cv_text}\n\n"
        
        if job_description:
            context += f"**JOB DESCRIPTION:**\n{job_description}\n\n"
        
        if required_skills:
            context += f"**REQUIRED SKILLS:**\n{', '.join(required_skills)}\n\n"
        
        # Create prompt
        user_prompt = f"""
Analisis CV/Resume berikut dengan standar professional recruitment:

{context}

**ANALYSIS TASKS:**
1. Extract key information (education, experience, skills, achievements)
2. Assess technical competency dan skill match
3. Evaluate professional experience quality
4. Identify strengths dan development areas
5. Calculate relevance score (jika job description tersedia)
6. Provide hiring recommendation

**OUTPUT FORMAT (JSON):**
{{
    "candidate_summary": {{
        "name": "extracted name",
        "current_role": "current/last position",
        "total_experience_years": number,
        "education_level": "highest degree",
        "key_skills": ["skill1", "skill2", ...]
    }},
    "assessment_scores": {{
        "technical_skills": score (0-100),
        "experience_quality": score (0-100),
        "education_fit": score (0-100),
        "achievements_impact": score (0-100),
        "overall_relevance": score (0-100)
    }},
    "strengths": ["strength1", "strength2", ...],
    "areas_of_concern": ["concern1", "concern2", ...],
    "skill_match": {{
        "matched_skills": ["skill1", "skill2"],
        "missing_skills": ["skill1", "skill2"],
        "match_percentage": score
    }},
    "recommendation": {{
        "decision": "Strong Hire|Hire|Consider|Pass",
        "confidence": score (0-100),
        "reasoning": "detailed explanation",
        "next_steps": ["action1", "action2"]
    }},
    "key_insights": ["insight1", "insight2", ...]
}}

Berikan analisis yang thorough, fair, dan data-driven.
"""
        
        # Call Groq API
        response = self._call_groq_api(
            system_prompt=self.system_prompts["cv"],
            user_prompt=user_prompt
        )
        
        # Parse response
        return self._parse_cv_response(response)
    
    def assess_personality(
        self,
        text_data: str,
        context: str = "professional"
    ) -> Dict[str, Any]:
        """
        Personality assessment dari text data
        
        Args:
            text_data: Text untuk dianalisis (posts, bio, writing samples)
            context: Context analysis (professional, casual, mixed)
        
        Returns:
            Dict dengan personality assessment
        """
        user_prompt = f"""
Lakukan personality assessment berdasarkan text berikut:

**TEXT DATA:**
{text_data}

**CONTEXT:** {context}

**ASSESSMENT FRAMEWORK:**
Gunakan Big Five personality traits dan professional work style indicators.

**OUTPUT FORMAT (JSON):**
{{
    "big_five_traits": {{
        "openness": score (0-100),
        "conscientiousness": score (0-100),
        "extraversion": score (0-100),
        "agreeableness": score (0-100),
        "neuroticism": score (0-100)
    }},
    "work_style": {{
        "analytical_thinking": score,
        "creativity": score,
        "leadership": score,
        "collaboration": score,
        "detail_orientation": score
    }},
    "communication_style": "description",
    "key_characteristics": ["char1", "char2", ...],
    "confidence": score (0-100)
}}

Berikan assessment yang scientific-based dan objective.
"""
        
        response = self._call_groq_api(
            system_prompt=self.system_prompts["personality"],
            user_prompt=user_prompt
        )
        
        return self._parse_json_response(response)
    
    def evaluate_cultural_fit(
        self,
        candidate_profile: Dict[str, Any],
        company_values: List[str],
        team_culture: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluasi cultural fit kandidat dengan company/team
        
        Args:
            candidate_profile: Profile kandidat (dari employee analysis)
            company_values: Core values perusahaan
            team_culture: Deskripsi budaya tim (optional)
        
        Returns:
            Dict dengan cultural fit assessment
        """
        context = f"""
**CANDIDATE PROFILE:**
{json.dumps(candidate_profile, indent=2, ensure_ascii=False)}

**COMPANY VALUES:**
{', '.join(company_values)}
"""
        
        if team_culture:
            context += f"\n**TEAM CULTURE:**\n{team_culture}"
        
        user_prompt = f"""
Evaluasi cultural fit kandidat dengan organization:

{context}

**EVALUATION CRITERIA:**
1. Values alignment dengan company values
2. Work style compatibility dengan team culture
3. Long-term retention potential
4. Integration ease
5. Cultural contribution potential

**OUTPUT FORMAT (JSON):**
{{
    "cultural_fit_score": score (0-100),
    "values_alignment": {{
        "value1": {{"match": score, "evidence": "explanation"}},
        "value2": {{"match": score, "evidence": "explanation"}}
    }},
    "compatibility_assessment": {{
        "team_dynamics": score,
        "communication_fit": score,
        "work_style_match": score,
        "adaptability": score
    }},
    "strengths": ["what makes them a good fit"],
    "potential_challenges": ["areas to watch"],
    "recommendation": {{
        "fit_level": "Excellent|Good|Moderate|Poor",
        "confidence": score,
        "reasoning": "detailed explanation"
    }},
    "onboarding_tips": ["tip1", "tip2"]
}}

Berikan evaluasi yang comprehensive dan actionable.
"""
        
        response = self._call_groq_api(
            system_prompt=self.system_prompts["cultural_fit"],
            user_prompt=user_prompt
        )
        
        return self._parse_json_response(response)
    
    def _call_groq_api(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None
    ) -> str:
        """Call Groq API dengan error handling"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature or self.temperature,
                max_tokens=2048,
                top_p=0.95,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise RuntimeError(f"❌ Groq API call failed: {str(e)}")
    
    def _build_employee_context(self, employee_data: Dict[str, Any]) -> str:
        """Build context string dari employee data"""
        context_parts = []
        
        if "name" in employee_data or "nama" in employee_data:
            name = employee_data.get("name") or employee_data.get("nama")
            context_parts.append(f"Nama: {name}")
        
        if "position" in employee_data or "jabatan" in employee_data:
            position = employee_data.get("position") or employee_data.get("jabatan")
            context_parts.append(f"Jabatan: {position}")
        
        if "bio" in employee_data:
            context_parts.append(f"Bio:\n{employee_data['bio']}")
        
        if "social_posts" in employee_data:
            posts = employee_data["social_posts"]
            if isinstance(posts, list):
                posts_text = "\n".join([f"- {p}" for p in posts[:10]])  # Max 10 posts
            else:
                posts_text = str(posts)
            context_parts.append(f"Social Media Posts:\n{posts_text}")
        
        if "additional_info" in employee_data:
            context_parts.append(f"Info Tambahan:\n{employee_data['additional_info']}")
        
        return "\n\n".join(context_parts)
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON dari AI response"""
        try:
            # Try direct JSON parse
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # Fallback: return structured error
            return {
                "error": "Failed to parse JSON",
                "raw_response": response,
                "parsed": False
            }
    
    def _parse_employee_response(
        self, 
        response: str, 
        original_data: Dict[str, Any]
    ) -> AIResponse:
        """Parse employee analysis response"""
        parsed = self._parse_json_response(response)
        
        return AIResponse(
            content=response,
            reasoning=parsed.get("reasoning", ""),
            confidence=parsed.get("confidence", 75.0),
            insights=parsed.get("key_insights", []),
            metadata={
                "analysis_type": "employee",
                "original_data": original_data,
                "parsed_result": parsed
            }
        )
    
    def _parse_cv_response(self, response: str) -> AIResponse:
        """Parse CV analysis response"""
        parsed = self._parse_json_response(response)
        
        recommendation = parsed.get("recommendation", {})
        
        return AIResponse(
            content=response,
            reasoning=recommendation.get("reasoning", ""),
            confidence=recommendation.get("confidence", 75.0),
            insights=parsed.get("key_insights", []),
            metadata={
                "analysis_type": "cv",
                "parsed_result": parsed,
                "recommendation": recommendation.get("decision", "Consider")
            }
        )


# Helper functions untuk quick access
def get_groq_reasoner(
    api_key: Optional[str] = None,
    model: str = "llama3-8b-8192"
) -> GroqAIReasoner:
    """Get configured Groq AI Reasoner instance"""
    return GroqAIReasoner(api_key=api_key, model=model)


def quick_analyze_text(
    text: str,
    analysis_type: str = "general",
    api_key: Optional[str] = None
) -> str:
    """
    Quick text analysis
    
    Args:
        text: Text to analyze
        analysis_type: Type of analysis (general, sentiment, personality)
        api_key: Groq API key
    
    Returns:
        Analysis result as string
    """
    reasoner = get_groq_reasoner(api_key=api_key)
    
    system_prompt = "Kamu adalah AI analyst yang memahami konteks dan makna teks dengan mendalam."
    
    if analysis_type == "sentiment":
        user_prompt = f"Analisis sentimen teks berikut:\n\n{text}\n\nBerikan: sentiment (positive/negative/neutral), confidence score, dan reasoning."
    elif analysis_type == "personality":
        user_prompt = f"Identifikasi personality traits dari teks berikut:\n\n{text}\n\nBerikan traits dan evidence."
    else:
        user_prompt = f"Analisis teks berikut dan berikan insights:\n\n{text}"
    
    return reasoner._call_groq_api(system_prompt, user_prompt)


if __name__ == "__main__":
    # Example usage
    print("🚀 Groq AI Reasoner - Testing")
    print("=" * 60)
    
    try:
        reasoner = get_groq_reasoner()
        print("✅ Groq AI Reasoner initialized successfully!")
        print(f"📦 Model: {reasoner.model}")
        
        # Test quick analysis
        test_text = "Saya sangat antusias dengan teknologi AI dan selalu ingin belajar hal baru. Saya percaya bahwa kolaborasi tim adalah kunci kesuksesan."
        
        print("\n🧪 Testing quick analysis...")
        result = quick_analyze_text(test_text, analysis_type="personality")
        print("\n📊 Result:")
        print(result[:500] + "..." if len(result) > 500 else result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Pastikan environment variable GROQ_API_KEY sudah di-set!")
