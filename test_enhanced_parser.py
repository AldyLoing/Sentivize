"""
Quick Test - Enhanced CV Parser
Test ekstraksi dengan CV_Aldy.pdf
"""

import sys
sys.path.insert(0, '.')

from enhanced_cv_parser import EnhancedCVParser
from cv_parser import CVParser

def test_enhanced_parser():
    """Test enhanced parser dengan CV Aldy"""
    
    print("="*70)
    print("🧪 TESTING ENHANCED CV PARSER")
    print("="*70)
    
    # Load CV
    cv_path = r"e:\Aldy\Berkas\CV_Aldy.pdf"
    
    try:
        # Parse PDF
        parser = CVParser()
        result = parser.parse(cv_path)
        
        if not result['success']:
            print(f"❌ Failed to parse PDF: {result['error']}")
            return
        
        text = result['text']
        print(f"✅ PDF parsed successfully")
        print(f"📄 Text length: {len(text)} characters")
        print(f"📝 Word count: {result['metadata']['word_count']} words")
        print()
        
        # Test Enhanced Parser
        enhanced = EnhancedCVParser()
        extracted = enhanced.extract_all_info(text)
        
        # Display results
        print("="*70)
        print("📊 EXTRACTION RESULTS:")
        print("="*70)
        
        print(f"\n👤 Name: {extracted['name']}")
        if extracted['name'] != 'Unknown':
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n📧 Email: {extracted['email']}")
        if extracted['email']:
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n📞 Phone: {extracted['phone']}")
        if extracted['phone']:
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n🔗 LinkedIn: {extracted['linkedin']}")
        if extracted['linkedin']:
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n💻 GitHub: {extracted['github']}")
        if extracted['github']:
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n📍 Location: {extracted['location']}")
        if extracted['location']:
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n💼 Work Experiences: {len(extracted['experiences'])} entries")
        for i, exp in enumerate(extracted['experiences'], 1):
            print(f"   {i}. {exp['position']} at {exp['company']}")
            print(f"      Duration: {exp['duration']} ({exp['years']} years)")
            print(f"      Technologies: {', '.join(exp['technologies'][:5])}")
            if extracted['experiences']:
                print("   ✅ DETECTED")
            else:
                print("   ⚠️  NOT DETECTED")
        
        print(f"\n🎓 Education: {len(extracted['education'])} entries")
        for i, edu in enumerate(extracted['education'], 1):
            print(f"   {i}. {edu['degree']} - {edu['institution']}")
            if edu['year']:
                print(f"      Year: {edu['year']}")
            if edu['gpa']:
                print(f"      GPA: {edu['gpa']}")
            if extracted['education']:
                print("   ✅ DETECTED")
            else:
                print("   ⚠️  NOT DETECTED")
        
        print(f"\n💻 Technical Skills: {len(extracted['skills']['technical'])} skills")
        if extracted['skills']['technical']:
            print(f"   {', '.join(extracted['skills']['technical'][:15])}")
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n🤝 Soft Skills: {len(extracted['skills']['soft'])} skills")
        if extracted['skills']['soft']:
            print(f"   {', '.join(extracted['skills']['soft'][:10])}")
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n📜 Certifications: {len(extracted['certifications'])} items")
        for cert in extracted['certifications'][:5]:
            print(f"   - {cert}")
        if extracted['certifications']:
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n🚀 Projects: {len(extracted['projects'])} items")
        for proj in extracted['projects'][:3]:
            print(f"   - {proj['name']}")
        if extracted['projects']:
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n🏆 Awards: {len(extracted['awards'])} items")
        for award in extracted['awards'][:5]:
            print(f"   - {award}")
        if extracted['awards']:
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        print(f"\n🌍 Languages: {len(extracted['languages'])} items")
        for lang in extracted['languages']:
            print(f"   - {lang['language']}: {lang['proficiency']}")
        if extracted['languages']:
            print("   ✅ DETECTED")
        else:
            print("   ⚠️  NOT DETECTED")
        
        # Summary
        print("\n" + "="*70)
        print("📈 DETECTION SUMMARY:")
        print("="*70)
        
        detections = []
        detections.append(('Name', extracted['name'] != 'Unknown'))
        detections.append(('Email', bool(extracted['email'])))
        detections.append(('Phone', bool(extracted['phone'])))
        detections.append(('LinkedIn', bool(extracted['linkedin'])))
        detections.append(('GitHub', bool(extracted['github'])))
        detections.append(('Location', bool(extracted['location'])))
        detections.append(('Experience', bool(extracted['experiences'])))
        detections.append(('Education', bool(extracted['education'])))
        detections.append(('Technical Skills', bool(extracted['skills']['technical'])))
        detections.append(('Soft Skills', bool(extracted['skills']['soft'])))
        detections.append(('Certifications', bool(extracted['certifications'])))
        detections.append(('Projects', bool(extracted['projects'])))
        detections.append(('Awards', bool(extracted['awards'])))
        detections.append(('Languages', bool(extracted['languages'])))
        
        detected = sum(1 for _, status in detections if status)
        total = len(detections)
        percentage = (detected / total) * 100
        
        for field, status in detections:
            emoji = "✅" if status else "⚠️ "
            print(f"{emoji} {field}")
        
        print(f"\n🎯 Detection Rate: {detected}/{total} ({percentage:.1f}%)")
        
        if percentage >= 90:
            print("🌟 EXCELLENT - Enhanced parser working perfectly!")
        elif percentage >= 70:
            print("✅ GOOD - Most fields detected successfully")
        elif percentage >= 50:
            print("⚠️  FAIR - Some fields need improvement")
        else:
            print("❌ POOR - Parser needs attention")
        
        print("\n" + "="*70)
        print("✅ TEST COMPLETED")
        print("="*70)
        
    except FileNotFoundError:
        print(f"❌ File not found: {cv_path}")
        print("Please ensure CV_Aldy.pdf exists at the specified path")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_enhanced_parser()
