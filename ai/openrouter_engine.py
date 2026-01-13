"""
OpenRouter AI Engine
====================
Engine AI untuk semantic reasoning menggunakan OpenRouter API
dengan model free seperti deepseek-chat
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import time


@dataclass
class AIResponse:
    """Response dari AI dengan metadata"""
    content: str
    model: str
    tokens_used: int = 0
    reasoning_steps: List[str] = None
    confidence: float = 0.0
    
    def __post_init__(self):
        if self.reasoning_steps is None:
            self.reasoning_steps = []


class OpenRouterEngine:
    """
    AI Engine menggunakan OpenRouter untuk reasoning tingkat tinggi
    dengan model free yang powerful seperti deepseek-chat
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        model: str = "deepseek/deepseek-chat",
        temperature: float = 0.3,
        max_tokens: int = 2000
    ):
        """
        Initialize OpenRouter Engine
        
        Args:
            api_key: OpenRouter API key (jika None, ambil dari environment)
            model: Model name (default: deepseek/deepseek-chat - FREE)
            temperature: Temperature untuk response (0.0-1.0, rendah = stabil)
            max_tokens: Max token untuk response
        """
        # Get API key dari environment atau parameter
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key tidak ditemukan! "
                "Set environment variable OPENROUTER_API_KEY atau pass via parameter."
            )
        
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Request headers
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://sentivize.app",  # Optional
            "X-Title": "Sentivize HR Analytics"  # Optional
        }
        
        print(f"✅ OpenRouter Engine initialized with model: {self.model}")
    
    def chat(
        self, 
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> AIResponse:
        """
        Send chat request ke OpenRouter
        
        Args:
            messages: List of message dicts [{"role": "user/system", "content": "..."}]
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            json_mode: Force JSON output
            
        Returns:
            AIResponse object
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract content
            content = result['choices'][0]['message']['content']
            tokens_used = result.get('usage', {}).get('total_tokens', 0)
            
            return AIResponse(
                content=content,
                model=self.model,
                tokens_used=tokens_used
            )
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ OpenRouter API Error: {e}")
            print(f"ℹ️ Menggunakan fallback scoring (sistem tetap berjalan)")
            return AIResponse(
                content=f"Fallback mode: API Error",
                model=self.model,
                tokens_used=0
            )
    
    def analyze_cv_semantic(
        self, 
        cv_text: str,
        job_title: str,
        job_description: str,
        job_complexity: str = "mid"
    ) -> Dict[str, Any]:
        """
        Analisis CV dengan semantic reasoning mendalam
        
        Args:
            cv_text: Full text dari CV
            job_title: Judul posisi yang dilamar
            job_description: Deskripsi pekerjaan
            job_complexity: low/mid/high
            
        Returns:
            Dict dengan analisis lengkap
        """
        
        # Build prompt yang powerful
        system_prompt = """Anda adalah HR Expert AI dengan kemampuan reasoning mendalam.
        
Tugas Anda: Analisis CV kandidat dengan pemahaman KONTEKSTUAL, bukan keyword matching kaku.

PRINSIP PENTING:
1. Untuk job LOW complexity (admin, kasir, staff entry): jangan menggugurkan fresh graduate
2. Fokus pada POTENTIAL, bukan hanya pengalaman eksplisit
3. Identifikasi TRANSFERABLE SKILLS (skill dari konteks lain yang bisa diaplikasikan)
4. Pahami PROGRESSION dan GROWTH INDICATORS
5. Berikan reasoning yang TRANSPARAN dan HUMAN-FRIENDLY

Output HARUS dalam format JSON dengan struktur:
{
  "overall_assessment": "ringkasan 3-5 kalimat dalam bahasa natural",
  "suitability_score": 0-100,
  "confidence": 0-100,
  "candidate_tier": "EXCELLENT/STRONG/MEDIUM/LOW",
  "key_strengths": ["strength 1", "strength 2", ...],
  "key_weaknesses": ["weakness 1", "weakness 2", ...],
  "matching_aspects": ["aspek yang cocok"],
  "missing_aspects": ["aspek yang kurang"],
  "transferable_skills": ["skill yang bisa ditransfer"],
  "growth_potential": "HIGH/MEDIUM/LOW",
  "reasoning": "penjelasan detail mengapa score tersebut",
  "recommendation": "STRONGLY RECOMMEND / RECOMMEND / CONSIDER / NOT SUITABLE",
  "position_alternatives": ["posisi alternatif yang cocok"],
  "interview_focus": ["area yang perlu digali saat interview"]
}"""

        user_prompt = f"""ANALISIS CV INI:

JOB CONTEXT:
- Posisi: {job_title}
- Kompleksitas: {job_complexity.upper()}
- Deskripsi: {job_description}

CV KANDIDAT:
{cv_text[:3000]}  

INSTRUKSI KHUSUS:
{"- Job ini adalah entry-level, jangan terlalu strict dengan experience. Fokus pada attitude, education, dan learning capability." if job_complexity == "low" else ""}
{"- Job ini memerlukan expertise, evaluasi pengalaman dan skill teknis dengan lebih ketat." if job_complexity == "high" else ""}

Berikan analisis dalam JSON format sesuai struktur yang diminta."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.chat(messages, temperature=0.3, json_mode=True)
        
        try:
            analysis = json.loads(response.content)
            return analysis
        except json.JSONDecodeError:
            # Fallback jika parsing gagal
            return {
                "overall_assessment": response.content[:500],
                "suitability_score": 50,
                "confidence": 30,
                "candidate_tier": "MEDIUM",
                "key_strengths": ["Data tidak dapat diparsing dengan baik"],
                "key_weaknesses": [],
                "reasoning": "Error dalam parsing JSON response",
                "recommendation": "CONSIDER"
            }
    
    def analyze_employee_batch(
        self,
        employees_data: List[Dict[str, Any]],
        job_criteria: str,
        target_position: str,
        job_complexity: str = "mid"
    ) -> List[Dict[str, Any]]:
        """
        Analisis batch karyawan untuk posisi tertentu
        
        Args:
            employees_data: List of employee data dicts
            job_criteria: Kriteria pekerjaan
            target_position: Posisi target
            job_complexity: low/mid/high
            
        Returns:
            List of analysis results
        """
        results = []
        
        for emp in employees_data:
            result = self.analyze_single_employee(
                employee_data=emp,
                job_criteria=job_criteria,
                target_position=target_position,
                job_complexity=job_complexity
            )
            results.append(result)
            
            # Rate limiting
            time.sleep(0.5)
        
        return results
    
    def analyze_single_employee(
        self,
        employee_data: Dict[str, Any],
        job_criteria: str,
        target_position: str,
        job_complexity: str = "mid"
    ) -> Dict[str, Any]:
        """
        Analisis single employee untuk posisi
        
        Args:
            employee_data: Data karyawan
            job_criteria: Kriteria pekerjaan
            target_position: Posisi target
            job_complexity: low/mid/high
            
        Returns:
            Analysis result dict
        """
        
        system_prompt = """Anda adalah HR Expert AI yang menganalisis kesesuaian karyawan untuk posisi tertentu.

PRINSIP:
1. Evaluasi berdasarkan POTENTIAL dan TRANSFERABLE SKILLS
2. Untuk low-complexity jobs: lebih fleksibel, fokus attitude & learning ability
3. Untuk high-complexity jobs: lebih strict pada skill teknis & pengalaman
4. Berikan reasoning yang jelas dan actionable

Output dalam JSON:
{
  "overall_assessment": "ringkasan natural",
  "suitability_score": 0-100,
  "recommendation": "STRONGLY RECOMMEND/RECOMMEND/CONSIDER/NOT SUITABLE",
  "key_strengths": [],
  "key_concerns": [],
  "transferable_skills": [],
  "development_areas": [],
  "position_fit_explanation": "penjelasan mengapa cocok/tidak",
  "alternative_positions": [],
  "confidence": 0-100
}"""

        # Build employee summary
        emp_summary = f"""Nama: {employee_data.get('name', 'Unknown')}
Posisi Sekarang: {employee_data.get('position', 'Unknown')}
Background: {employee_data.get('background', employee_data.get('text', 'No data'))}
"""

        user_prompt = f"""EVALUASI KARYAWAN INI:

{emp_summary}

POSISI TARGET:
- Judul: {target_position}
- Kompleksitas: {job_complexity.upper()}
- Kriteria: {job_criteria}

Berikan analisis dalam JSON sesuai format."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.chat(messages, temperature=0.3, json_mode=True)
        
        try:
            analysis = json.loads(response.content)
            analysis['employee_name'] = employee_data.get('name', 'Unknown')
            return analysis
        except json.JSONDecodeError:
            return {
                "employee_name": employee_data.get('name', 'Unknown'),
                "overall_assessment": "Error parsing response",
                "suitability_score": 50,
                "recommendation": "CONSIDER",
                "confidence": 30
            }
    
    def generate_career_summary(
        self,
        cv_text: str,
        max_sentences: int = 7
    ) -> str:
        """
        Generate human-style career summary dari CV
        
        Args:
            cv_text: Full CV text
            max_sentences: Max kalimat untuk summary
            
        Returns:
            Career summary string
        """
        
        prompt = f"""Buat ringkasan karier kandidat ini dalam {max_sentences} kalimat dengan gaya NATURAL dan HUMAN-FRIENDLY.

CV:
{cv_text[:2000]}

Fokus pada:
1. Latar belakang pendidikan
2. Pengalaman kerja atau organisasi
3. Keahlian utama
4. Kekuatan dan potensi
5. Tipe pekerjaan yang cocok

Tulis dalam bahasa Indonesia yang mudah dipahami HR/Admin non-IT."""

        messages = [
            {"role": "system", "content": "Anda adalah HR writer yang menulis ringkasan karier dengan bahasa natural."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.chat(messages, temperature=0.4, max_tokens=500)
        return response.content.strip()
    
    def extract_skills_intelligent(
        self,
        text: str
    ) -> Dict[str, List[str]]:
        """
        Ekstraksi skill dengan AI reasoning (bukan keyword matching)
        
        Args:
            text: Text untuk dianalisis
            
        Returns:
            Dict dengan hard_skills, soft_skills, technical_skills
        """
        
        prompt = f"""Ekstrak SEMUA SKILL dari text berikut, termasuk skill yang IMPLICIT (tidak ditulis langsung).

Text:
{text[:2000]}

Kategorikan ke:
1. Hard Skills (teknis, measurable)
2. Soft Skills (interpersonal, attitude)
3. Technical Tools (software, platform, tools)

Output JSON:
{{
  "hard_skills": [],
  "soft_skills": [],
  "technical_tools": [],
  "implicit_skills": []  // skill yang tersirat dari pengalaman
}}"""

        messages = [
            {"role": "system", "content": "Anda adalah skill extraction AI yang cerdas."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.chat(messages, temperature=0.2, json_mode=True)
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "hard_skills": [],
                "soft_skills": [],
                "technical_tools": [],
                "implicit_skills": []
            }


# Singleton instance
_openrouter_engine = None


def get_openrouter_engine(
    api_key: Optional[str] = None,
    model: str = "deepseek/deepseek-chat"
) -> OpenRouterEngine:
    """
    Get or create OpenRouter engine instance (singleton)
    
    Args:
        api_key: OpenRouter API key
        model: Model name
        
    Returns:
        OpenRouterEngine instance
    """
    global _openrouter_engine
    
    if _openrouter_engine is None:
        _openrouter_engine = OpenRouterEngine(api_key=api_key, model=model)
    
    return _openrouter_engine
