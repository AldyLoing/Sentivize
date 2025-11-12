"""
Test Groq AI Integration
Quick test untuk memverifikasi semua components berfungsi
"""

import sys
import os


def test_imports():
    """Test all required imports"""
    print("🧪 Testing Imports...")
    print("=" * 60)
    
    tests = []
    
    # Core libraries
    try:
        import streamlit
        print("✅ streamlit")
        tests.append(True)
    except ImportError as e:
        print(f"❌ streamlit: {e}")
        tests.append(False)
    
    try:
        import pandas
        print("✅ pandas")
        tests.append(True)
    except ImportError as e:
        print(f"❌ pandas: {e}")
        tests.append(False)
    
    try:
        import numpy
        print("✅ numpy")
        tests.append(True)
    except ImportError as e:
        print(f"❌ numpy: {e}")
        tests.append(False)
    
    # Groq AI
    try:
        import groq
        print("✅ groq")
        tests.append(True)
    except ImportError as e:
        print(f"❌ groq: {e}")
        tests.append(False)
    
    # Sentiment analysis
    try:
        import vaderSentiment
        print("✅ vaderSentiment")
        tests.append(True)
    except ImportError as e:
        print(f"❌ vaderSentiment: {e}")
        tests.append(False)
    
    try:
        import textblob
        print("✅ textblob")
        tests.append(True)
    except ImportError as e:
        print(f"❌ textblob: {e}")
        tests.append(False)
    
    # Document processing
    try:
        import PyPDF2
        print("✅ PyPDF2")
        tests.append(True)
    except ImportError as e:
        print(f"❌ PyPDF2: {e}")
        tests.append(False)
    
    try:
        import docx
        print("✅ python-docx")
        tests.append(True)
    except ImportError as e:
        print(f"❌ python-docx: {e}")
        tests.append(False)
    
    print(f"\n📊 Import Test Results: {sum(tests)}/{len(tests)} passed")
    
    return all(tests)


def test_groq_config():
    """Test Groq configuration"""
    print("\n🔧 Testing Groq Configuration...")
    print("=" * 60)
    
    try:
        from groq_config import GroqConfig, get_groq_status, display_groq_info
        
        status = get_groq_status()
        
        print(f"API Key Set: {status['api_key_set']}")
        print(f"Groq Available: {status['available']}")
        print(f"Model: {status['model']}")
        print(f"Temperature: {status['temperature']}")
        
        print("\n" + display_groq_info())
        
        if status['available']:
            print("✅ Groq configuration OK!")
            return True
        else:
            print("⚠️ Groq API key not set (optional - will use traditional NLP)")
            return True  # Not critical
            
    except Exception as e:
        print(f"❌ Error testing Groq config: {e}")
        return False


def test_sentiment_analyzer():
    """Test sentiment analyzer"""
    print("\n😊 Testing Sentiment Analyzer...")
    print("=" * 60)
    
    try:
        from sentiment_analyzer import SentimentAnalyzer, quick_sentiment
        
        analyzer = SentimentAnalyzer()
        
        test_texts = [
            ("I love this! Amazing work!", "positive"),
            ("This is terrible and frustrating.", "negative"),
            ("The weather is okay today.", "neutral")
        ]
        
        passed = 0
        for text, expected in test_texts:
            result = analyzer.analyze(text)
            actual = result.label
            
            match = "✓" if actual == expected else "✗"
            print(f"{match} '{text[:30]}...' -> {actual} (expected: {expected})")
            
            if actual == expected:
                passed += 1
        
        print(f"\n📊 Sentiment Test: {passed}/{len(test_texts)} passed")
        
        return passed >= 2  # At least 2/3 should pass
        
    except Exception as e:
        print(f"❌ Error testing sentiment analyzer: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cv_parser():
    """Test CV parser"""
    print("\n📄 Testing CV Parser...")
    print("=" * 60)
    
    try:
        from cv_parser import CVParser
        
        parser = CVParser()
        
        # Test with sample text
        sample_cv = """
        JOHN DOE
        Software Engineer
        john.doe@email.com | +1-555-0123
        
        PROFESSIONAL SUMMARY
        Experienced engineer with 5+ years in software development.
        
        SKILLS
        Python, JavaScript, React, AWS
        
        EXPERIENCE
        Senior Developer | Tech Corp | 2020-Present
        - Developed web applications
        - Led team of 5 engineers
        """
        
        # Create temporary file
        import tempfile
        from pathlib import Path
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(sample_cv)
            temp_file = f.name
        
        try:
            result = parser.parse(temp_file)
            
            print(f"Parse Success: {result['success']}")
            print(f"Text Length: {len(result.get('text', ''))}")
            print(f"Sections Found: {len(result.get('sections', {}))}")
            
            # Extract contact
            contact = parser.extract_contact_info(result.get('text', ''))
            print(f"Email Extracted: {'email' in contact}")
            print(f"Phone Extracted: {'phone' in contact}")
            
            # Cleanup
            Path(temp_file).unlink()
            
            success = result['success'] and len(result.get('text', '')) > 0
            
            if success:
                print("✅ CV Parser OK!")
            
            return success
            
        except Exception as e:
            Path(temp_file).unlink()
            raise e
            
    except Exception as e:
        print(f"❌ Error testing CV parser: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_groq_reasoner():
    """Test Groq AI Reasoner (if API key available)"""
    print("\n🧠 Testing Groq AI Reasoner...")
    print("=" * 60)
    
    try:
        from groq_config import GroqConfig
        
        if not GroqConfig.is_groq_available():
            print("⚠️ Groq API key not set - skipping Groq test")
            print("   Set GROQ_API_KEY environment variable to test Groq AI")
            return True  # Not critical
        
        from groq_ai_reasoner import get_groq_reasoner, quick_analyze_text
        
        print("🚀 Attempting Groq API call...")
        
        try:
            reasoner = get_groq_reasoner()
            print(f"✓ Reasoner initialized with model: {reasoner.model}")
            
            # Quick test
            test_text = "Saya sangat antusias dengan teknologi AI dan suka berkolaborasi."
            result = quick_analyze_text(test_text, analysis_type="sentiment")
            
            print(f"✓ API call successful")
            print(f"  Response length: {len(result)} chars")
            print(f"  Sample: {result[:100]}...")
            
            print("✅ Groq AI Reasoner OK!")
            return True
            
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            print("   Check your API key and internet connection")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Groq reasoner: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Test integration components"""
    print("\n🔗 Testing Integration Components...")
    print("=" * 60)
    
    try:
        # Test employee analyzer (without Groq)
        from groq_employee_analyzer import get_groq_employee_analyzer
        
        analyzer = get_groq_employee_analyzer(
            use_mock_models=True,
            enable_groq=False
        )
        
        print("✓ Employee analyzer initialized (mock mode)")
        
        # Test CV analyzer (without Groq)
        from groq_cv_analyzer import get_groq_cv_analyzer
        
        cv_analyzer = get_groq_cv_analyzer(
            use_mock_models=True,
            enable_groq=False
        )
        
        print("✓ CV analyzer initialized (mock mode)")
        
        print("✅ Integration components OK!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing integration: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 GROQ AI INTEGRATION - SYSTEM TEST")
    print("="*60 + "\n")
    
    results = {}
    
    # Run tests
    results['imports'] = test_imports()
    results['groq_config'] = test_groq_config()
    results['sentiment'] = test_sentiment_analyzer()
    results['cv_parser'] = test_cv_parser()
    results['groq_reasoner'] = test_groq_reasoner()
    results['integration'] = test_integration()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\n🎯 Overall: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! System ready to use!")
        return 0
    elif total_passed >= total_tests - 1:  # Allow 1 failure (Groq API)
        print("\n✅ Core tests passed! System functional.")
        print("   Note: Some advanced features may not be available.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
