"""
Test Script untuk OpenRouter AI Integration
===========================================
Script untuk memvalidasi bahwa semua komponen AI berfungsi dengan baik
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment
from utils.env_loader import load_env, validate_api_keys

print("=" * 70)
print("SENTIVIZE AI SYSTEM TEST")
print("=" * 70)

# Test 1: Environment Variables
print("\n[TEST 1] Environment Variables")
print("-" * 70)
load_env()
api_status = validate_api_keys()

for service, status in api_status.items():
    configured = "✅ CONFIGURED" if status['configured'] else "❌ NOT CONFIGURED"
    print(f"{service.upper()}: {configured}")
    if status['configured']:
        print(f"  Key preview: {status['key_preview']}")

# Test 2: OpenRouter Engine
print("\n[TEST 2] OpenRouter AI Engine")
print("-" * 70)

try:
    from ai.openrouter_engine import get_openrouter_engine
    
    engine = get_openrouter_engine()
    print("✅ OpenRouter engine initialized successfully")
    
    # Test simple chat
    print("\nTesting simple chat request...")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say 'Hello from Sentivize AI!' in one line."}
    ]
    
    response = engine.chat(messages)
    print(f"Response: {response.content}")
    print(f"Tokens used: {response.tokens_used}")
    
    if "Hello" in response.content or "Sentivize" in response.content:
        print("✅ OpenRouter API working correctly!")
    else:
        print("⚠️ Response might be unexpected")
    
except Exception as e:
    print(f"❌ OpenRouter test failed: {e}")

# Test 3: Job Complexity Detector
print("\n[TEST 3] Job Complexity Detector")
print("-" * 70)

try:
    from ai.job_complexity_detector import JobComplexityDetector
    from ai.advanced_ai_engine import get_ai_engine
    
    ai_engine = get_ai_engine()
    detector = JobComplexityDetector(ai_engine)
    
    # Test low complexity
    job_low = detector.detect_complexity("Admin Staff", "Mengelola administrasi kantor")
    print(f"\nTest LOW complexity job:")
    print(f"  Title: Admin Staff")
    print(f"  Detected: {job_low.complexity.value}")
    print(f"  Fresh Grad Friendly: {job_low.fresh_graduate_friendly}")
    print(f"  ✅ PASS" if job_low.complexity.value == "low" else "❌ FAIL")
    
    # Test high complexity
    job_high = detector.detect_complexity("Senior Software Engineer", "Develop complex systems")
    print(f"\nTest HIGH complexity job:")
    print(f"  Title: Senior Software Engineer")
    print(f"  Detected: {job_high.complexity.value}")
    print(f"  Fresh Grad Friendly: {job_high.fresh_graduate_friendly}")
    print(f"  ✅ PASS" if job_high.complexity.value == "high" else "❌ FAIL")
    
except Exception as e:
    print(f"❌ Job Complexity test failed: {e}")

# Test 4: CV Preview Extractor
print("\n[TEST 4] CV Preview Extractor")
print("-" * 70)

try:
    from ai.cv_preview_extractor import CVPreviewExtractor
    
    extractor = CVPreviewExtractor(use_ai=False)  # Test without AI first
    
    # Test with sample text
    sample_cv_text = """
    John Doe
    john.doe@email.com
    +62 812-3456-7890
    
    EDUCATION
    S1 Computer Science, Universitas Indonesia (2020-2024)
    
    SKILLS
    Python, JavaScript, React, Communication, Teamwork
    
    EXPERIENCE
    Software Engineer Intern at Tech Corp (2023-2024)
    Developed web applications using React and Node.js
    
    PROJECTS
    - E-commerce website
    - Task management app
    """
    
    preview = extractor.extract_from_text(sample_cv_text)
    
    print(f"Name detected: {preview.full_name}")
    print(f"Email detected: {preview.email}")
    print(f"Skills found: {len(preview.hard_skills)} hard skills, {len(preview.soft_skills)} soft skills")
    print(f"Experience: {preview.total_work_experience_months} months")
    print(f"Level: {preview.candidate_level}")
    
    if preview.full_name and preview.email:
        print("✅ CV extraction working!")
    else:
        print("⚠️ Some fields not extracted")
    
except Exception as e:
    print(f"❌ CV Preview test failed: {e}")

# Test 5: Semantic CV Analysis (with OpenRouter)
print("\n[TEST 5] Semantic CV Analysis (OpenRouter)")
print("-" * 70)

try:
    from ai.openrouter_engine import get_openrouter_engine
    
    engine = get_openrouter_engine()
    
    sample_cv = """
    Jane Smith
    Fresh Graduate dari S1 Administrasi Bisnis
    Pengalaman organisasi sebagai Ketua BEM
    Skills: MS Office, komunikasi, event planning, leadership
    """
    
    print("Analyzing sample CV for Admin position...")
    result = engine.analyze_cv_semantic(
        cv_text=sample_cv,
        job_title="Admin Staff",
        job_description="Mengelola administrasi kantor, membuat laporan, komunikasi dengan tim",
        job_complexity="low"
    )
    
    print(f"\nAnalysis Result:")
    print(f"  Suitability Score: {result.get('suitability_score', 'N/A')}/100")
    print(f"  Tier: {result.get('candidate_tier', 'N/A')}")
    print(f"  Recommendation: {result.get('recommendation', 'N/A')}")
    print(f"  Summary: {result.get('overall_assessment', 'N/A')[:150]}...")
    
    if result.get('suitability_score'):
        print("✅ Semantic analysis working!")
    else:
        print("⚠️ Analysis incomplete")
    
except Exception as e:
    print(f"❌ Semantic analysis test failed: {e}")

# Final Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print("""
Jika semua test ✅ PASS:
- Sistem siap digunakan untuk production
- AI reasoning aktif dan berfungsi

Jika ada ❌ FAIL atau ⚠️ WARNING:
- Check error messages di atas
- Review AI_UPGRADE_GUIDE.md untuk troubleshooting
- Sistem tetap bisa jalan dengan fallback mode (tanpa AI reasoning)
""")

print("\n✅ Test completed!")
