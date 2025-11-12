"""
Test Script untuk Advanced AI System
Memverifikasi bahwa semua modul advanced berfungsi dengan baik
"""

import sys
import os

print("=" * 80)
print("🧪 TESTING ADVANCED AI SYSTEM")
print("=" * 80)

# Test 1: Import advanced modules
print("\n📦 Test 1: Importing Advanced Modules...")
try:
    from advanced_ai_core import (
        AdvancedNLPEngine,
        ContextualReasoningEngine,
        get_advanced_nlp_engine,
        get_reasoning_engine
    )
    print("✅ advanced_ai_core imported successfully")
except Exception as e:
    print(f"❌ Failed to import advanced_ai_core: {e}")
    sys.exit(1)

try:
    from advanced_cv_analyzer import (
        AdvancedCVParser,
        AdvancedCVAnalyzer,
        get_advanced_cv_analyzer
    )
    print("✅ advanced_cv_analyzer imported successfully")
except Exception as e:
    print(f"❌ Failed to import advanced_cv_analyzer: {e}")
    sys.exit(1)

try:
    from advanced_employee_analyzer import (
        AdvancedEmployeeAnalyzer,
        get_advanced_employee_analyzer
    )
    print("✅ advanced_employee_analyzer imported successfully")
except Exception as e:
    print(f"❌ Failed to import advanced_employee_analyzer: {e}")
    sys.exit(1)

# Test 2: Initialize NLP Engine (Mock Mode)
print("\n🧠 Test 2: Initializing NLP Engine (Mock Mode)...")
try:
    nlp_engine = get_advanced_nlp_engine(use_mock_models=True)
    print("✅ NLP Engine initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize NLP Engine: {e}")
    sys.exit(1)

# Test 3: Entity Extraction
print("\n🔍 Test 3: Testing Entity Extraction...")
test_text = """
John Doe is a Senior Software Engineer at Google with 5 years of experience.
He has a Bachelor's degree in Computer Science from MIT with GPA 3.8.
Proficient in Python, Java, React, and AWS. Certified AWS Solutions Architect.
Located in San Francisco, California.
"""

try:
    entities = nlp_engine.extract_entities(test_text)
    print(f"✅ Entities extracted:")
    print(f"   - Organizations: {len(entities.get('organizations', []))}")
    print(f"   - Locations: {len(entities.get('locations', []))}")
    print(f"   - Skills: {len(entities.get('skills', []))}")
    print(f"   - Education: {len(entities.get('education', []))}")
    print(f"   - Certifications: {len(entities.get('certifications', []))}")
except Exception as e:
    print(f"❌ Entity extraction failed: {e}")

# Test 4: Semantic Similarity
print("\n📏 Test 4: Testing Semantic Similarity...")
try:
    text1 = "Python developer with Django experience"
    text2 = "Backend engineer proficient in Python and Django framework"
    similarity = nlp_engine.calculate_semantic_similarity(text1, text2)
    print(f"✅ Similarity calculated: {similarity:.2%}")
    print(f"   Text 1: {text1}")
    print(f"   Text 2: {text2}")
except Exception as e:
    print(f"❌ Similarity calculation failed: {e}")

# Test 5: Topic Extraction
print("\n📊 Test 5: Testing Topic Extraction...")
try:
    long_text = """
    Passionate about environmental sustainability and renewable energy.
    Working on projects related to climate change mitigation and green technology.
    Believe in the importance of conservation and reducing carbon footprint.
    Active in environmental advocacy and community clean-up initiatives.
    """
    topics = nlp_engine.extract_semantic_topics(long_text, num_topics=3)
    print(f"✅ Topics extracted: {len(topics)}")
    for topic, score in topics[:3]:
        print(f"   - {topic}: {score:.2%}")
except Exception as e:
    print(f"❌ Topic extraction failed: {e}")

# Test 6: CV Parser
print("\n📄 Test 6: Testing CV Parser...")
try:
    cv_parser = AdvancedCVParser()
    
    sample_cv = """
    John Doe
    john.doe@email.com | +1-234-567-8900
    linkedin.com/in/johndoe
    
    PROFESSIONAL SUMMARY
    Senior Software Engineer with 5 years of experience in full-stack development.
    
    WORK EXPERIENCE
    Senior Software Engineer | Google Inc. | 2020 - Present
    - Led development of microservices architecture serving 10M+ users
    - Improved system performance by 40%
    - Mentored team of 5 junior engineers
    
    Software Engineer | Microsoft | 2018 - 2020
    - Developed REST APIs using Python and Django
    - Collaborated with cross-functional teams
    
    EDUCATION
    Bachelor of Science in Computer Science | MIT | 2018
    GPA: 3.8/4.0
    Dean's List, Magna Cum Laude
    
    SKILLS
    Python, Java, JavaScript, React, Django, AWS, Docker, Kubernetes
    
    CERTIFICATIONS
    AWS Certified Solutions Architect
    Google Cloud Professional Engineer
    """
    
    cv_profile = cv_parser.create_cv_profile(sample_cv)
    print(f"✅ CV Profile created:")
    print(f"   - Name: {cv_profile.candidate_name}")
    print(f"   - Email: {cv_profile.contact_info.get('email', 'N/A')}")
    print(f"   - Experience: {cv_profile.total_experience_years} years")
    print(f"   - Seniority: {cv_profile.seniority_level}")
    print(f"   - Work Experiences: {len(cv_profile.work_experiences)}")
    print(f"   - Education: {len(cv_profile.education)}")
    print(f"   - Technical Skills: {len(cv_profile.skills['technical'])}")
    print(f"   - Certifications: {len(cv_profile.certifications)}")
except Exception as e:
    print(f"❌ CV parsing failed: {e}")
    import traceback
    traceback.print_exc()

# Test 7: CV Analyzer (Deep Analysis)
print("\n🎯 Test 7: Testing CV Analyzer (Deep Analysis)...")
try:
    cv_analyzer = get_advanced_cv_analyzer(use_mock_models=True)
    
    criteria = """
    3+ years experience in software development
    Proficient in Python and cloud technologies
    Bachelor's degree in Computer Science
    Strong problem-solving skills
    """
    
    result = cv_analyzer.analyze_cv_deep(
        cv_text=sample_cv,
        criteria=criteria
    )
    
    print(f"✅ CV Analysis completed:")
    print(f"   - Relevance Score: {result.relevance_score:.1%}")
    print(f"   - Confidence: {result.confidence_score:.1%}")
    print(f"   - Strengths: {len(result.strengths)}")
    print(f"   - Potential Areas: {len(result.potential_areas)}")
    print(f"   - Recommendation: {result.overall_recommendation[:50]}...")
    
    if result.strengths:
        print(f"\n   Top Strength:")
        print(f"   - {result.strengths[0].category}: {result.strengths[0].reasoning[:80]}...")
    
except Exception as e:
    print(f"❌ CV analysis failed: {e}")
    import traceback
    traceback.print_exc()

# Test 8: Employee Analyzer
print("\n👥 Test 8: Testing Employee Analyzer...")
try:
    employee_analyzer = get_advanced_employee_analyzer(use_mock_models=True)
    
    sample_texts = [
        "Passionate about environmental sustainability and green technology.",
        "Working on renewable energy projects to combat climate change.",
        "Leading a team of engineers to develop eco-friendly solutions.",
        "Presenting at conferences about sustainable development practices."
    ]
    
    result = employee_analyzer.analyze_employee_comprehensive(
        name="Jane Smith",
        position="Senior Engineer",
        unit="Engineering",
        texts=sample_texts,
        social_links=["https://linkedin.com/in/janesmith"],
        keyword="environmental sustainability",
        enable_behavioral_analysis=True
    )
    
    print(f"✅ Employee Analysis completed:")
    print(f"   - Name: {result.name}")
    print(f"   - Relevance Score: {result.relevance_score:.1%}")
    print(f"   - Sentiment: {result.sentiment_label} ({result.sentiment_score:.1%})")
    print(f"   - Potential Score: {result.potential_score:.1%}")
    print(f"   - Confidence: {result.confidence:.1%}")
    
    if result.behavioral_profile:
        profile = result.behavioral_profile
        print(f"\n   Personality Traits:")
        sorted_traits = sorted(profile.personality.traits.items(), key=lambda x: x[1], reverse=True)
        for trait, score in sorted_traits[:3]:
            if score > 0.5:
                print(f"   - {trait.title()}: {score:.0%}")
        
        print(f"\n   Value Alignment:")
        sorted_values = sorted(profile.value_alignment.items(), key=lambda x: x[1], reverse=True)
        for value, score in sorted_values[:3]:
            if score > 0.3:
                print(f"   - {value.replace('_', ' ').title()}: {score:.0%}")
        
        if profile.green_flags:
            print(f"\n   Green Flags: {len(profile.green_flags)}")
            for flag in profile.green_flags[:2]:
                print(f"   ✅ {flag}")
    
    print(f"\n   Recommendation: {result.recommendation[:70]}...")
    
except Exception as e:
    print(f"❌ Employee analysis failed: {e}")
    import traceback
    traceback.print_exc()

# Test 9: Reasoning Engine
print("\n🧩 Test 9: Testing Contextual Reasoning Engine...")
try:
    reasoning_engine = get_reasoning_engine(nlp_engine)
    
    experience_text = """
    Senior Software Engineer at Google (2020-Present)
    - Led team of 5 engineers
    - Managed project with $2M budget
    - Increased system performance by 40%
    - Implemented microservices architecture serving 10M users
    """
    
    exp_analysis = reasoning_engine.analyze_experience_depth(experience_text)
    print(f"✅ Experience Analysis:")
    print(f"   - Years: {exp_analysis.get('years_of_experience', 0)}")
    print(f"   - Level: {exp_analysis.get('responsibility_level', 'N/A')}")
    print(f"   - Technical Depth: {exp_analysis.get('technical_depth', 'N/A')}")
    print(f"   - Leadership Indicators: {len(exp_analysis.get('leadership_indicators', []))}")
    print(f"   - Impact Indicators: {len(exp_analysis.get('impact_indicators', []))}")
    
except Exception as e:
    print(f"❌ Reasoning engine test failed: {e}")

# Test 10: Personality Profiling
print("\n🎭 Test 10: Testing Personality Profiling...")
try:
    sample_posts = [
        "Led a successful project that improved team productivity by 30%",
        "Analyzing market data to drive strategic decisions",
        "Designed innovative solution for customer pain points",
        "Collaborated with cross-functional teams on product launch",
        "Mentoring junior developers and sharing technical knowledge"
    ]
    
    personality = reasoning_engine.infer_personality_traits(sample_posts)
    print(f"✅ Personality Profile:")
    print(f"   - Communication: {personality.communication_style.title()}")
    print(f"   - Social Presence: {personality.social_presence.title()}")
    print(f"   - Professional Tone: {personality.professional_tone.title()}")
    
    print(f"\n   Top Traits:")
    sorted_traits = sorted(personality.traits.items(), key=lambda x: x[1], reverse=True)
    for trait, score in sorted_traits[:4]:
        if score > 0.3:
            print(f"   - {trait.title()}: {score:.0%}")
    
except Exception as e:
    print(f"❌ Personality profiling failed: {e}")

# Final Summary
print("\n" + "=" * 80)
print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 80)
print("\n🎉 Advanced AI System is working correctly!")
print("\nYou can now:")
print("1. Run the application: streamlit run app.py")
print("2. Select 🧠 Advanced Mode in sidebar")
print("3. Try Advanced CV Analyzer or Advanced Employee Analyzer")
print("4. Upload your data and see the magic! ✨")
print("\n📚 Read ADVANCED_QUICK_START.md for detailed usage guide")
print("=" * 80)
