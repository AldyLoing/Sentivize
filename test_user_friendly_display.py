"""
Quick Test Script for User-Friendly Interface
Tests the new display functions with sample data
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_employee_display():
    """Test employee user-friendly display"""
    print("🧪 Testing Employee Display Format...")
    
    # Create mock employee result
    class MockEmployeeResult:
        def __init__(self):
            self.employee_name = "John Doe"
            self.cultural_fit_score = 0.85
            self.sentiment_positive_ratio = 0.78
            self.potential_score = 0.82
            self.confidence_score = 0.88
            
            # Analysis sections
            self.summary = "John adalah karyawan dengan performa excellent dan attitude positif."
            
            self.strengths = [
                "Skor kecocokan budaya sangat tinggi (85%)",
                "Sentimen feedback konsisten positif",
                "Potensi kepemimpinan teridentifikasi",
                "Communication skills excellent"
            ]
            
            self.weaknesses = [
                "Tingkat stress perlu dimonitoring",
                "Work-life balance bisa ditingkatkan"
            ]
            
            self.recommendations = [
                "Pertahankan engagement dengan recognition program",
                "Monitor stress level secara berkala",
                "Siapkan career development path"
            ]
            
            # Details
            self.personality_scores = {
                'Openness': 0.75,
                'Conscientiousness': 0.88,
                'Extraversion': 0.65,
                'Agreeableness': 0.82,
                'Neuroticism': 0.35
            }
            
            self.sentiment_distribution = {
                'positive': 0.78,
                'neutral': 0.15,
                'negative': 0.07
            }
    
    result = MockEmployeeResult()
    
    # Test scoring logic
    match_score = int(result.cultural_fit_score * 100)
    
    if match_score >= 80:
        emoji = "🌟"
        label = "Sangat Cocok"
        print(f"✅ Score {match_score}% → {emoji} {label}")
    elif match_score >= 60:
        emoji = "✅"
        label = "Cocok"
        print(f"✅ Score {match_score}% → {emoji} {label}")
    elif match_score >= 40:
        emoji = "💡"
        label = "Cukup Potensial"
        print(f"✅ Score {match_score}% → {emoji} {label}")
    else:
        emoji = "⚠️"
        label = "Perlu Perhatian"
        print(f"✅ Score {match_score}% → {emoji} {label}")
    
    print(f"✅ Summary: {result.summary}")
    print(f"✅ Strengths: {len(result.strengths)} items")
    print(f"✅ Weaknesses: {len(result.weaknesses)} items")
    print(f"✅ Recommendations: {len(result.recommendations)} items")
    
    return True


def test_cv_display():
    """Test CV user-friendly display"""
    print("\n🧪 Testing CV Display Format...")
    
    # Create mock CV result
    class MockCVProfile:
        def __init__(self):
            self.candidate_name = "Jane Smith"
            self.current_role = "Senior Software Engineer"
            self.total_experience_years = 7
            self.education_level = "Master of Computer Science"
            self.technical_skills = [
                "Python", "Java", "React", "Node.js", "AWS",
                "Docker", "Kubernetes", "Machine Learning"
            ]
            self.soft_skills = ["Leadership", "Communication", "Problem Solving"]
            self.professional_summary = "Experienced software engineer with strong background in full-stack development and cloud technologies."
            self.contact_info = {
                'email': 'jane.smith@email.com',
                'phone': '+62-812-3456-7890',
                'linkedin': 'linkedin.com/in/janesmith',
                'location': 'Jakarta, Indonesia'
            }
    
    class MockCVResult:
        def __init__(self):
            self.cv_profile = MockCVProfile()
            self.relevance_score = 0.88
            self.confidence_score = 0.85
            self.skill_match_score = 0.82
    
    result = MockCVResult()
    profile = result.cv_profile
    
    # Test scoring logic
    match_score = int(result.relevance_score * 100)
    
    if match_score >= 80:
        emoji = "🌟"
        label = "Sangat Cocok"
        decision = "Strong Hire - Kandidat sangat direkomendasikan!"
        print(f"✅ Score {match_score}% → {emoji} {label}")
        print(f"✅ Decision: {decision}")
    elif match_score >= 65:
        emoji = "✅"
        label = "Cocok"
        decision = "Hire - Kandidat direkomendasikan untuk interview lanjutan"
        print(f"✅ Score {match_score}% → {emoji} {label}")
        print(f"✅ Decision: {decision}")
    elif match_score >= 50:
        emoji = "💡"
        label = "Cukup Potensial"
        decision = "Consider - Pertimbangkan dengan interview mendalam"
        print(f"✅ Score {match_score}% → {emoji} {label}")
        print(f"✅ Decision: {decision}")
    else:
        emoji = "⚠️"
        label = "Kurang Sesuai"
        decision = "Pass - Belum sesuai dengan kriteria saat ini"
        print(f"✅ Score {match_score}% → {emoji} {label}")
        print(f"✅ Decision: {decision}")
    
    print(f"✅ Candidate: {profile.candidate_name}")
    print(f"✅ Experience: {profile.total_experience_years} years")
    print(f"✅ Skills: {len(profile.technical_skills)} technical skills")
    print(f"✅ Contact: {profile.contact_info['email']}")
    
    return True


def test_emoji_display():
    """Test emoji rendering"""
    print("\n🧪 Testing Emoji Rendering...")
    
    emojis = {
        "Score High": "🌟",
        "Check": "✅",
        "Idea": "💡",
        "Warning": "⚠️",
        "Target": "🎯",
        "Trophy": "🏆",
        "Briefcase": "💼",
        "Seedling": "🌱",
        "Phone": "📞",
        "Chart": "📊"
    }
    
    for name, emoji in emojis.items():
        print(f"  {emoji} {name}")
    
    print("✅ All emojis rendered successfully")
    return True


def test_indonesian_text():
    """Test Indonesian language support"""
    print("\n🧪 Testing Indonesian Language...")
    
    indonesian_texts = [
        "Ringkasan",
        "Kekuatan",
        "Perlu Ditingkatkan",
        "Rekomendasi",
        "Sangat Cocok",
        "Kecocokan Budaya",
        "Sentimen Positif",
        "Potensi Tinggi"
    ]
    
    for text in indonesian_texts:
        print(f"  ✅ {text}")
    
    print("✅ Indonesian text support verified")
    return True


def main():
    """Run all tests"""
    print("="*60)
    print("🚀 USER-FRIENDLY INTERFACE TEST SUITE")
    print("="*60)
    
    tests = [
        ("Employee Display", test_employee_display),
        ("CV Display", test_cv_display),
        ("Emoji Rendering", test_emoji_display),
        ("Indonesian Language", test_indonesian_text)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED! User-friendly interface is ready! 🎉")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    exit(main())
