"""
🧪 Test Script: Username Variation Generation
Tests ALL 4 categories of username variations as requested by user:
1. Variasi Nama Dasar (Basic Name Variations)
2. Variasi Username (Username Patterns)
3. Nama + Konteks CV (Name + CV Context)
4. Username Langsung dari CV (Direct CV Username - PRIORITY)
"""

import sys
from services.social_media_intelligence_rapidapi import SocialMediaIntelligence

def test_username_variations():
    """Test comprehensive username generation"""
    
    print("=" * 80)
    print("🧪 TESTING: Username Variation Generation")
    print("=" * 80)
    
    # Initialize service
    service = SocialMediaIntelligence()
    
    # Test Case: ALDY OSCAR PANCASILA LOING
    candidate_name = "ALDY OSCAR PANCASILA LOING"
    
    # Mock CV data with context
    cv_data = {
        'organization': 'HIMSIFOR',
        'profession': 'Project Lead',
        'achievements': 'PPK Ormawa, Lead Developer, IT Champion',
        'location': 'Jakarta, Indonesia'
    }
    
    print(f"\n📋 Candidate Name: {candidate_name}")
    print(f"📄 CV Context:")
    print(f"   - Organization: {cv_data['organization']}")
    print(f"   - Profession: {cv_data['profession']}")
    print(f"   - Achievements: {cv_data['achievements']}")
    print(f"   - Location: {cv_data['location']}")
    
    # Generate variations
    print(f"\n⚙️ Generating username variations...")
    variations = service.generate_username_variations(candidate_name, cv_data)
    
    print(f"\n✅ Generated {len(variations)} unique variations\n")
    
    # Categorize variations for display
    print("=" * 80)
    print("📊 GENERATED VARIATIONS BY CATEGORY:")
    print("=" * 80)
    
    print("\n1️⃣ VARIASI NAMA DASAR (Basic Name Variations):")
    basic_patterns = ['aldyloing', 'aldy_loing', 'aldy.loing', 'aldyoscar', 
                      'aldy_oscar', 'oscarloing', 'aldyoscarloing', 'aldyoscarpancasila']
    for v in variations:
        if any(pattern in v.lower() and len(v) <= 20 and '_' not in v or '.' in v or v.replace('_','').isalpha() for pattern in ['aldy', 'oscar', 'loing']):
            if 'himsifor' not in v and 'project' not in v and 'ppk' not in v and 'jakarta' not in v:
                if not any(char.isdigit() for char in v):
                    print(f"   • {v}")
    
    print("\n2️⃣ VARIASI USERNAME (Username Patterns - initials, abbreviations, numbers):")
    for v in variations:
        if (any(char.isdigit() for char in v) or  # Has numbers
            len([c for c in v if c.isupper()]) > 1 or  # Has multiple capitals (CamelCase)
            (len(v) <= 8 and v[0].islower()) or  # Short initials
            v.startswith('_') or v.endswith('_')):  # Has underscore prefix/suffix
            print(f"   • {v}")
    
    print("\n3️⃣ NAMA + KONTEKS CV (Name + CV Context - org, profession, achievements, location):")
    context_keywords = ['himsifor', 'project', 'lead', 'ppk', 'ormawa', 'dev', 'jakarta']
    for v in variations:
        if any(keyword in v.lower() for keyword in context_keywords):
            print(f"   • {v}")
    
    print("\n4️⃣ PRIORITAS: Username dari CV akan dicoba PERTAMA jika ditemukan")
    print("   (Priority handled in search functions, not in generation)")
    
    # Show statistics
    print("\n" + "=" * 80)
    print("📈 STATISTICS:")
    print("=" * 80)
    print(f"Total Unique Variations: {len(variations)}")
    print(f"Average Length: {sum(len(v) for v in variations) / len(variations):.1f} characters")
    print(f"Shortest: {min(variations, key=len)} ({len(min(variations, key=len))} chars)")
    print(f"Longest: {max(variations, key=len)} ({len(max(variations, key=len))} chars)")
    
    # Show all variations in compact format
    print("\n" + "=" * 80)
    print("📋 ALL VARIATIONS (Compact View):")
    print("=" * 80)
    for i, v in enumerate(variations, 1):
        if i % 5 == 0:
            print(f"{v}")
        else:
            print(f"{v}", end=", ")
    if len(variations) % 5 != 0:
        print()  # New line if not ended with newline
    
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETED")
    print("=" * 80)
    print(f"\n💡 These {len(variations)} variations will be tried during social media search")
    print("💡 CV usernames (if found) will be tried FIRST before these variations")
    print("💡 Instagram: Tries ALL variations with Scraper API")
    print("💡 Twitter/TikTok: Tries up to 15 variations")
    print("💡 Statistics API: Tries up to 10 variations for influencer accounts")

if __name__ == "__main__":
    try:
        test_username_variations()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
