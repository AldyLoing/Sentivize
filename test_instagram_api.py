"""
Quick test script untuk Instagram Statistics API
Test dengan username aldy_loing
"""

import requests
import json
import os

# Direct API key (temporary for testing)
RAPIDAPI_KEY = "e4979f2d52mshccd7e28c65d60e2p1ecbe1jsnf369efc1f96e"

def test_instagram_search(username):
    """Test Instagram API dengan username spesifik"""
    
    print(f"\n{'='*70}")
    print(f"Testing Instagram API for: @{username}")
    print(f"{'='*70}\n")
    
    # API endpoint
    api_url = "https://instagram-statistics-api.p.rapidapi.com/community"
    instagram_url = f"https://www.instagram.com/{username}/"
    
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': 'instagram-statistics-api.p.rapidapi.com'
    }
    
    params = {
        'url': instagram_url
    }
    
    print(f"🔗 URL: {instagram_url}")
    print(f"🔑 API Key: {RAPIDAPI_KEY[:20]}...")
    print(f"\n📤 Making request...\n")
    
    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=15)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"\n📥 Response Headers:")
        for key, value in response.headers.items():
            if key.lower() in ['content-type', 'x-ratelimit-requests-remaining', 'x-ratelimit-requests-limit']:
                print(f"  {key}: {value}")
        
        print(f"\n📄 Response Body:")
        
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2))
            
            # Analyze structure
            print(f"\n🔍 Analysis:")
            print(f"  - Type: {type(data)}")
            print(f"  - Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            if isinstance(data, dict):
                for key, value in data.items():
                    print(f"  - {key}: {type(value).__name__}")
                    if isinstance(value, dict):
                        print(f"    → Sub-keys: {list(value.keys())[:10]}")
        else:
            print(f"  {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test dengan username yang diketahui ada
    print("\n" + "="*70)
    print("INSTAGRAM API RESPONSE FORMAT TEST")
    print("="*70)
    
    # Test 1: Username yang pasti ada (therock)
    print("\n\n🧪 TEST 1: Known username (therock)")
    test_instagram_search("therock")
    
    # Test 2: Username kandidat (aldy_loing)
    print("\n\n🧪 TEST 2: Candidate username (aldy_loing)")
    test_instagram_search("aldy_loing")
    
    # Test 3: Username yang tidak ada
    print("\n\n🧪 TEST 3: Non-existent username (thisuserdoesnotexist12345)")
    test_instagram_search("thisuserdoesnotexist12345")
    
    print("\n" + "="*70)
    print("TEST COMPLETED")
    print("="*70 + "\n")
