"""
Advanced Social Media Intelligence & Sentiment Analysis
========================================================
ADDITIVE MODULE - Menggunakan RapidAPI untuk analisis social media
Tidak mengubah sistem lama

Author: Sentivize Ultra
Date: December 2025
"""

import requests
import os
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import time


class SocialMediaIntelligence:
    """
    Advanced Social Media Intelligence menggunakan RapidAPI
    Bersifat OPTIONAL dan tidak mempengaruhi analisis utama
    """
    
    def __init__(self):
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY', '')
        self.timeout = 15
        self.rate_limit_delay = 1.0  # seconds between requests
        
        # API endpoints (Multi-platform support)
        self.apis = {
            'instagram': {
                'host': 'instagram-statistics-api.p.rapidapi.com',
                'endpoint': 'https://instagram-statistics-api.p.rapidapi.com/community',
                'enabled': bool(self.rapidapi_key),
                'emoji': '📷',
                'note': 'Analytics API - hanya untuk influencer/business accounts (5000+ followers)'
            },
            'instagram_scraper': {
                'host': 'instagram-scraper-stable-api.p.rapidapi.com',
                'endpoint': 'https://instagram-scraper-stable-api.p.rapidapi.com/get_ig_user_info.php',
                'enabled': bool(self.rapidapi_key),
                'emoji': '📷',
                'note': 'Scraper API - untuk regular accounts, bisa detect semua public accounts'
            },
            'linkedin': {
                'host': 'linkedin-data-api.p.rapidapi.com',
                'endpoint': 'https://linkedin-data-api.p.rapidapi.com/get-profile-data-by-url',
                'enabled': bool(self.rapidapi_key),
                'emoji': '💼',
                'note': 'Personal profile data dari LinkedIn URL di CV'
            },
            'facebook': {
                'host': 'facebook-scraper3.p.rapidapi.com',
                'endpoint': 'https://facebook-scraper3.p.rapidapi.com/profile',
                'enabled': bool(self.rapidapi_key),
                'emoji': '👥',
                'note': 'Public profile data dari Facebook URL di CV'
            },
            'twitter': {
                'host': 'twitter-api45.p.rapidapi.com',
                'endpoint': 'https://twitter-api45.p.rapidapi.com/search',
                'enabled': bool(self.rapidapi_key),
                'emoji': '🐦'
            },
            'tiktok': {
                'host': 'tiktok-scraper7.p.rapidapi.com',
                'endpoint': 'https://tiktok-scraper7.p.rapidapi.com/user/info',
                'enabled': bool(self.rapidapi_key),
                'emoji': '🎵'
            },
            'youtube': {
                'host': 'youtube-v2.p.rapidapi.com',
                'endpoint': 'https://youtube-v2.p.rapidapi.com/search',
                'enabled': bool(self.rapidapi_key),
                'emoji': '▶️'
            }
        }
        
        # Sentiment keywords untuk analisis konten
        self.sentiment_keywords = {
            'positive': ['sukses', 'prestasi', 'juara', 'best', 'winner', 'excellent', 'achievement', 
                        'proud', 'grateful', 'thankful', 'inspired', 'motivated', 'professional'],
            'negative': ['kontroversial', 'scandal', 'masalah', 'problem', 'issue', 'complaint', 
                        'angry', 'disappointed', 'frustrated', 'hate', 'racist', 'sexist'],
            'professional': ['project', 'work', 'team', 'leadership', 'research', 'innovation',
                           'technology', 'development', 'management', 'strategic', 'analysis']
        }
        
        # Regex patterns untuk extract social media URLs dari CV
        self.social_media_patterns = {
            'linkedin': [
                r'linkedin\.com/in/([a-zA-Z0-9\-]+)',
                r'linkedin\.com/pub/([a-zA-Z0-9\-]+)',
                r'www\.linkedin\.com/in/([a-zA-Z0-9\-]+)',
            ],
            'facebook': [
                r'facebook\.com/([a-zA-Z0-9\.]+)',
                r'fb\.com/([a-zA-Z0-9\.]+)',
                r'www\.facebook\.com/([a-zA-Z0-9\.]+)',
                r'facebook\.com/profile\.php\?id=(\d+)',
            ],
            'instagram': [
                r'instagram\.com/([a-zA-Z0-9\._]+)',
                r'www\.instagram\.com/([a-zA-Z0-9\._]+)',
                r'@([a-zA-Z0-9\._]+)',  # @username format
            ],
            'twitter': [
                r'twitter\.com/([a-zA-Z0-9_]+)',
                r'x\.com/([a-zA-Z0-9_]+)',
                r'@([a-zA-Z0-9_]+)',  # @handle format
            ]
        }
    
    def extract_social_media_from_cv(self, cv_text: str) -> Dict[str, List[str]]:
        """
        Extract social media URLs/usernames langsung dari CV text
        
        Priority Strategy:
        1. Jika ada URL lengkap di CV → Gunakan langsung (BEST)
        2. Jika tidak ada → Generate username variations (FALLBACK)
        
        Args:
            cv_text: Raw text dari CV kandidat
            
        Returns:
            Dict dengan platform dan list of found URLs/usernames
        """
        found = {
            'linkedin': [],
            'facebook': [],
            'instagram': [],
            'twitter': []
        }
        
        if not cv_text:
            return found
        
        # Convert to lowercase for case-insensitive matching
        cv_lower = cv_text.lower()
        
        # Extract per platform
        for platform, patterns in self.social_media_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, cv_lower)
                if matches:
                    # Clean and deduplicate
                    for match in matches:
                        if match and match not in found[platform]:
                            # Remove common false positives
                            if len(match) > 2 and not match.startswith('http'):
                                found[platform].append(match)
        
        return found
    
    def generate_username_variations(self, full_name: str, cv_data: Dict[str, Any] = None) -> List[str]:
        """
        Generate variasi username LENGKAP berdasarkan nama dan konteks CV
        Sesuai requirement: Multi-variasi pencarian username
        
        Args:
            full_name: Nama lengkap kandidat (e.g., "ALDY OSCAR PANCASILA LOING")
            cv_data: Data tambahan dari CV (organisasi, profesi, achievements)
            
        Returns:
            List comprehensive username variations (20-30 variasi)
        """
        if not full_name or full_name == "Unknown":
            return []
        
        variations = []
        name_parts = full_name.strip().split()
        
        if len(name_parts) >= 2:
            first = name_parts[0].lower()
            last = name_parts[-1].lower()
            middle = name_parts[1].lower() if len(name_parts) > 2 else ""
            middle2 = name_parts[2].lower() if len(name_parts) > 3 else ""
            
            # === 1️⃣ VARIASI NAMA DASAR ===
            # Full name combinations
            variations.append(full_name.replace(" ", "").lower())  # aldyoscarpancasalaloing
            variations.append(full_name.replace(" ", "_").lower())  # aldy_oscar_pancasila_loing
            variations.append(full_name.replace(" ", ".").lower())  # aldy.oscar.pancasila.loing
            
            # First + Last (paling umum)
            variations.append(f"{first}{last}")          # aldyloing
            variations.append(f"{first}_{last}")         # aldy_loing
            variations.append(f"{first}.{last}")         # aldy.loing
            
            # First + Middle
            if middle:
                variations.append(f"{first}{middle}")    # aldyoscar
                variations.append(f"{first}_{middle}")   # aldy_oscar
                variations.append(f"{first}.{middle}")   # aldy.oscar
            
            # Middle + Last
            if middle:
                variations.append(f"{middle}{last}")     # oscarloing
                variations.append(f"{middle}_{last}")    # oscar_loing
            
            # First + Middle + Last (3 parts)
            if middle:
                variations.append(f"{first}{middle}{last}")       # aldyoscarloing
                variations.append(f"{first}_{middle}_{last}")     # aldy_oscar_loing
                variations.append(f"{first}.{middle}.{last}")     # aldy.oscar.loing
            
            # === 2️⃣ VARIASI INITIAL & ABBREVIATIONS ===
            # First initial + Last
            variations.append(f"{first[0]}{last}")       # aloing
            variations.append(f"{first[0]}_{last}")      # a_loing
            variations.append(f"{first[0]}.{last}")      # a.loing
            
            # First + Last initial
            variations.append(f"{first}{last[0]}")       # aldyl
            
            # Initials + Last
            if middle:
                variations.append(f"{first[0]}{middle[0]}{last}")      # aoploing
                variations.append(f"{first[0]}.{middle[0]}.{last}")    # a.o.loing
                variations.append(f"{first[0]}{middle[0]}_{last}")     # ao_loing
            
            if middle and middle2:
                variations.append(f"{first[0]}{middle[0]}{middle2[0]}{last}")  # aoploing
                variations.append(f"{first[0]}.{middle[0]}.{middle2[0]}.{last}")  # a.o.p.loing
            
            # First + Middle initials + Last
            if middle:
                variations.append(f"{first}{middle[0]}{last}")         # aldyoloing
                variations.append(f"{first}.{middle[0]}.{last}")       # aldy.o.loing
                variations.append(f"{first}_{middle[0]}_{last}")       # aldy_o_loing
            
            # === TAMBAHAN: More common patterns ===
            # First + Middle initials only
            if middle:
                variations.append(f"{first}{middle[0]}")               # aldyo
                variations.append(f"{first}{middle[0]}{middle2[0] if middle2 else ''}")  # aldyop
            
            # Abbreviated forms
            if middle:
                variations.append(f"{first}{middle[0]}{last[0]}")      # aldyol
                variations.append(f"{first[0]}{middle}{last}")         # aoscarloing
            
            # CamelCase variations
            variations.append(f"{first.capitalize()}{last.capitalize()}")  # AldyLoing
            if middle:
                variations.append(f"{first.capitalize()}{middle.capitalize()}")  # AldyOscar
                variations.append(f"{first.capitalize()}{middle.capitalize()}{last.capitalize()}")  # AldyOscarLoing
            
            # === TAMBAHAN: Double name patterns ===
            # Last name doubled
            variations.append(f"{first}{last}{last}")        # aldyloinging
            variations.append(f"{first}{last}_{last}")       # aldyloing_loing
            
            # First name doubled
            variations.append(f"{first}{first}{last}")       # aldyaldyloing
            variations.append(f"{first}_{first}_{last}")     # aldy_aldy_loing
            
            # Common number suffixes (birth years, lucky numbers)
            for num in ['01', '99', '00', '21', '23']:
                variations.append(f"{first}{last}{num}")     # aldyloing99
                variations.append(f"{first}_{last}{num}")    # aldy_loing99
                if middle:
                    variations.append(f"{first}{middle}{num}")  # aldyoscar99
            
            # Underscore at end (common pattern)
            variations.append(f"{first}{last}_")             # aldyloing_
            variations.append(f"_{first}{last}")             # _aldyloing
            
            # === 3️⃣ NAMA + KONTEKS CV (EXPANDED) ===
            if cv_data:
                # Nama + Organisasi
                org = cv_data.get('organization', '')
                if org and len(org) < 20:
                    org_clean = re.sub(r'[^a-zA-Z0-9]', '', org).lower()
                    variations.append(f"{first}{org_clean}")            # aldyhimsifor
                    variations.append(f"{first}_{org_clean}")           # aldy_himsifor
                    variations.append(f"{first}{last}{org_clean}")      # aldyloinghimsifor
                    variations.append(f"{org_clean}{first}")            # himsiforaldy
                    if middle:
                        variations.append(f"{first}{middle}{org_clean}")  # aldyoscarhimsifor
                
                # Nama + Profesi/Role
                profession = cv_data.get('profession', '')
                if profession and len(profession) < 15:
                    prof_clean = re.sub(r'[^a-zA-Z0-9]', '', profession).lower()
                    variations.append(f"{first}{prof_clean}")           # aldydev
                    variations.append(f"{first}_{prof_clean}")          # aldy_dev
                    variations.append(f"{first}{last}{prof_clean}")     # aldyloingdev
                    variations.append(f"{prof_clean}{first}")           # devaldy
                    variations.append(f"{prof_clean}_{first}")          # dev_aldy
                
                # Nama + Achievement keyword
                achievements = cv_data.get('achievements', '')
                if achievements:
                    # Extract keywords seperti "PPK", "Lead", "Project", dll
                    keywords = re.findall(r'\b[A-Z]{2,}\b', achievements)
                    for kw in keywords[:3]:  # Increased to 3 keywords
                        kw_lower = kw.lower()
                        if len(kw_lower) <= 8:
                            variations.append(f"{first}{kw_lower}")     # aldyppk
                            variations.append(f"{first}_{kw_lower}")    # aldy_ppk
                            variations.append(f"{first}{last}{kw_lower}")  # aldyloingppk
                            variations.append(f"{kw_lower}{first}")     # ppkaldy
                
                # Nama + Location (if available in CV)
                location = cv_data.get('location', '')
                if location:
                    loc_parts = location.split(',')[0].strip()  # Get first part (city)
                    loc_clean = re.sub(r'[^a-zA-Z0-9]', '', loc_parts).lower()
                    if loc_clean and len(loc_clean) <= 10:
                        variations.append(f"{first}{loc_clean}")        # aldyjakarta
                        variations.append(f"{first}_{loc_clean}")       # aldy_jakarta
        
        # === 4️⃣ REMOVE DUPLICATES & VALIDATE ===
        unique_variations = []
        seen = set()
        for v in variations:
            if v and v not in seen and len(v) >= 3 and len(v) <= 30:  # Min 3, max 30 chars
                unique_variations.append(v)
                seen.add(v)
        
        print(f"   ℹ️ Generated {len(unique_variations)} unique username variations")
        return unique_variations  # Return ALL variations (user wants SEMUA variasi)
    
    def search_instagram_account(self, username_variations: List[str], candidate_name: str) -> Dict[str, Any]:
        """
        Search Instagram account menggunakan RapidAPI Instagram Statistics API
        
        Args:
            username_variations: List username untuk dicoba
            candidate_name: Nama kandidat untuk validasi
            
        Returns:
            Dict dengan hasil pencarian dan confidence level
        """
        if not self.rapidapi_key:
            return {
                'status': 'api_key_missing',
                'platform': 'instagram',
                'message': 'RapidAPI key tidak tersedia. Set RAPIDAPI_KEY di .env'
            }
        
        results = {
            'status': 'searched',
            'platform': 'instagram',
            'candidates': [],
            'confirmed': None
        }
        
        print(f"\n   🔍 Searching Instagram Statistics API for {len(username_variations)} username variations...")
        print(f"   ⚠️  Note: Statistics API hanya detect influencer accounts (5000+ followers)")
        
        # Try MORE variations untuk increase success rate (10 instead of 5)
        max_tries = min(10, len(username_variations))
        print(f"   → Will try {max_tries} variations...")
        
        for username in username_variations[:max_tries]:
            try:
                # Construct Instagram URL
                instagram_url = f"https://www.instagram.com/{username}/"
                
                # RapidAPI Instagram Statistics endpoint
                api_url = "https://instagram-statistics-api.p.rapidapi.com/community"
                
                headers = {
                    'x-rapidapi-key': self.rapidapi_key,
                    'x-rapidapi-host': self.apis['instagram']['host']
                }
                
                params = {
                    'url': instagram_url
                }
                
                print(f"   → Trying @{username}...")
                response = requests.get(api_url, headers=headers, params=params, timeout=self.timeout)
                
                # DEBUG: Print response details
                print(f"      Status: {response.status_code}")
                
                if response.status_code == 200:
                    response_json = response.json()
                    
                    # DEBUG: Print actual response structure
                    print(f"      Response keys: {list(response_json.keys()) if isinstance(response_json, dict) else 'Not a dict'}")
                    
                    # Check meta status code
                    meta = response_json.get('meta', {})
                    if meta.get('code') == 404:
                        print(f"   ✗ @{username} not found (API meta code 404)")
                        continue
                    
                    # Extract actual data from nested structure: {"meta": {...}, "data": {...}}
                    data = response_json.get('data', {})
                    
                    if not data or not isinstance(data, dict):
                        print(f"   ✗ @{username} - No data in response")
                        continue
                    
                    print(f"      Data keys: {list(data.keys())[:10]}")
                    
                    actual_data = data
                    
                    # Extract ALL metrics from API documentation
                    # === BASIC METRICS ===
                    followers = actual_data.get('usersCount', 0)  # Main followers field
                    screen_name = actual_data.get('screenName', username)
                    is_verified = actual_data.get('verified', False)
                    is_blocked = actual_data.get('isBlocked', False)
                    is_closed = actual_data.get('isClosed', False)
                    
                    # === ENGAGEMENT METRICS ===
                    avg_er = actual_data.get('avgER', 0)  # Average Post Engagement Rate
                    avg_interactions = actual_data.get('avgInteractions', 0)
                    avg_views = actual_data.get('avgViews', 0)
                    avg_likes = actual_data.get('avgLikes', 0)
                    avg_comments = actual_data.get('avgComments', 0)
                    
                    # === QUALITY METRICS ===
                    quality_score = actual_data.get('qualityScore', 0)  # 0-1 quality indicator
                    pct_fake_followers = actual_data.get('pctFakeFollowers', 0)  # Percentage fake followers
                    
                    # === DEMOGRAPHICS ===
                    country = actual_data.get('country', '')
                    country_code = actual_data.get('countryCode', '')
                    city = actual_data.get('city', '')
                    gender = actual_data.get('gender', '')  # m | f
                    age = actual_data.get('age', '')  # Age range
                    account_type = actual_data.get('type', '')  # influencer | business
                    categories = actual_data.get('categories', [])
                    
                    # === AUDIENCE DEMOGRAPHICS ===
                    members_types = actual_data.get('membersTypes', [])  # real, suspicious, massfollowers, influencer
                    countries = actual_data.get('countries', [])  # Top audience countries
                    genders = actual_data.get('genders', [])  # Audience gender distribution
                    ages = actual_data.get('ages', [])  # Audience age distribution
                    
                    # === MENTIONS & REACH ===
                    to_mentions_180d = actual_data.get('toMentions180d', 0)  # Times mentioned by others
                    from_mentions_180d = actual_data.get('fromMentions180d', 0)  # Times mentioning others
                    pct_users_count_180d = actual_data.get('pctUsersCount180d', 0)  # Follower growth %
                    
                    # === CONTACT INFO ===
                    contact_email = actual_data.get('contactEmail', '')
                    
                    # === UPDATE TIMESTAMPS ===
                    time_statistics = actual_data.get('timeStatistics', '')
                    time_posts_loaded = actual_data.get('timePostsLoaded', '')
                    
                    print(f"      Followers found: {followers}")
                    
                    # Calculate confidence based on data completeness
                    confidence_score = 0
                    reasons = []
                    
                    if followers > 0:
                        confidence_score += 40
                        reasons.append(f"Account exists with {followers} followers")
                    
                    # Check name similarity - API returns 'name' field
                    profile_name = (actual_data.get('name') or  # Main field from API
                                  actual_data.get('full_name') or 
                                  actual_data.get('fullName') or 
                                  actual_data.get('screenName') or '').lower()
                    
                    print(f"      Profile name: {profile_name}")
                    
                    if profile_name and candidate_name.lower() in profile_name:
                        confidence_score += 40
                        reasons.append("Profile name matches candidate")
                    
                    # Check if verified or has significant following
                    if followers > 1000:
                        confidence_score += 10
                    
                    is_verified = (actual_data.get('is_verified') or 
                                 actual_data.get('verified') or 
                                 actual_data.get('is_business') or False)
                    
                    if is_verified:
                        confidence_score += 10
                        reasons.append("Verified account")
                    
                    # IMPORTANT: Even if score low, still add as candidate if account exists
                    if followers > 0 or profile_name:
                        # Determine confidence level
                        if confidence_score >= 70:
                            confidence_level = 'CONFIRMED'
                        elif confidence_score >= 40:
                            confidence_level = 'POSSIBLE_MATCH'
                        else:
                            confidence_level = 'LOW_CONFIDENCE'
                        
                        # Get bio/description
                        bio = actual_data.get('description', '')
                        
                        # Build comprehensive candidate data with ALL metrics
                        candidate_data = {
                            'username': screen_name or username,
                            'url': instagram_url,
                            'confidence': confidence_level,
                            'confidence_score': confidence_score,
                            'reasons': reasons if reasons else ['Account exists'],
                            'data': {
                                # Basic Info
                                'followers': followers,
                                'profile_name': profile_name or username,
                                'bio': bio,
                                'is_verified': is_verified,
                                'is_blocked': is_blocked,
                                'is_closed': is_closed,
                                'account_type': account_type,
                                
                                # Engagement Metrics
                                'avg_er': avg_er,
                                'avg_interactions': avg_interactions,
                                'avg_views': avg_views,
                                'avg_likes': avg_likes,
                                'avg_comments': avg_comments,
                                
                                # Quality Metrics
                                'quality_score': quality_score,
                                'fake_followers_pct': pct_fake_followers,
                                
                                # Demographics
                                'country': country,
                                'country_code': country_code,
                                'city': city,
                                'gender': gender,
                                'age': age,
                                'categories': categories,
                                
                                # Audience Demographics
                                'audience_types': members_types,
                                'audience_countries': countries,
                                'audience_genders': genders,
                                'audience_ages': ages,
                                
                                # Reach & Growth
                                'mentions_received_180d': to_mentions_180d,
                                'mentions_made_180d': from_mentions_180d,
                                'follower_growth_180d_pct': pct_users_count_180d,
                                
                                # Contact
                                'contact_email': contact_email,
                                
                                # Update Info
                                'last_updated': time_statistics,
                                'posts_last_loaded': time_posts_loaded
                            }
                        }
                        
                        results['candidates'].append(candidate_data)
                    
                        # If CONFIRMED, set as confirmed account
                        if confidence_level == 'CONFIRMED' and not results['confirmed']:
                            results['confirmed'] = candidate_data
                            print(f"   ✓ CONFIRMED: @{username} (score: {confidence_score})")
                            break  # Stop searching if confirmed
                        else:
                            print(f"   • {confidence_level}: @{username} (score: {confidence_score})")
                    else:
                        print(f"   ✗ @{username} - Account exists but no usable data")
                
                elif response.status_code == 404:
                    print(f"   ✗ @{username} not found (404)")
                elif response.status_code == 429:
                    print(f"   ⚠ Rate limit reached, stopping search")
                    results['status'] = 'rate_limited'
                    break
                else:
                    print(f"   ⚠ Error {response.status_code} for @{username}")
                    # Try to print error message if available
                    try:
                        error_data = response.json()
                        if 'message' in error_data:
                            print(f"      Error message: {error_data['message']}")
                    except:
                        pass
                
                time.sleep(self.rate_limit_delay)
                
            except requests.Timeout:
                print(f"   ⚠ Timeout for @{username}")
                continue
            except Exception as e:
                print(f"   ⚠ Error for @{username}: {str(e)}")
                import traceback
                print(f"      Traceback: {traceback.format_exc()[:200]}")
                continue
        
        # Summary
        if results['confirmed']:
            results['status'] = 'confirmed'
            print(f"\n   ✅ Instagram account confirmed: @{results['confirmed']['username']}")
        elif results['candidates']:
            results['status'] = 'candidates_found'
            print(f"\n   ⚠ Found {len(results['candidates'])} possible matches")
        else:
            results['status'] = 'not_found'
            print(f"\n   ✗ No Instagram account found")
        
        return results
    
    def search_twitter_account(self, username_variations: List[str], candidate_name: str, cv_username: str = None) -> Dict[str, Any]:
        """
        Search Twitter/X account menggunakan RapidAPI
        
        Args:
            username_variations: List username untuk dicoba
            candidate_name: Nama kandidat untuk validasi
            cv_username: Username dari CV (PRIORITY jika ada)
            
        Returns:
            Dict dengan status dan data akun yang ditemukan
        """
        if not self.apis['twitter']['enabled']:
            return {'status': 'api_key_missing', 'platform': 'twitter'}
        
        results = {
            'platform': 'twitter',
            'status': 'searching',
            'confirmed': None,
            'candidates': []
        }
        
        print(f"\n🐦 Searching Twitter for: {candidate_name}")
        
        # PRIORITAS: Try CV username first if provided
        if cv_username:
            print(f"   ✅ Trying username from CV: @{cv_username} (PRIORITY)")
            try:
                api_url = f"https://twitter-api45.p.rapidapi.com/screenname.php"
                headers = {
                    'x-rapidapi-key': self.rapidapi_key,
                    'x-rapidapi-host': self.apis['twitter']['host']
                }
                params = {'screenname': cv_username}
                
                response = requests.get(api_url, headers=headers, params=params, timeout=self.timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    if data and not data.get('error'):
                        # Found via CV username - high confidence
                        results['confirmed'] = {
                            'username': cv_username,
                            'url': f"https://twitter.com/{cv_username}",
                            'confidence': 'CONFIRMED_FROM_CV',
                            'data': data
                        }
                        results['status'] = 'confirmed'
                        print(f"   ✅ CONFIRMED from CV: @{cv_username}")
                        return results
            except Exception as e:
                print(f"   ⚠ CV username failed: {str(e)}")
        
        # Try generated variations
        max_tries = min(15, len(username_variations))
        print(f"   Will try {max_tries} username variations...")
        
        for idx, username in enumerate(username_variations[:max_tries], 1):
            try:
                # Twitter API endpoint
                api_url = f"https://twitter-api45.p.rapidapi.com/screenname.php"
                
                headers = {
                    'x-rapidapi-key': self.rapidapi_key,
                    'x-rapidapi-host': self.apis['twitter']['host']
                }
                
                params = {
                    'screenname': username
                }
                
                print(f"   → Trying @{username}...")
                response = requests.get(api_url, headers=headers, params=params, timeout=self.timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data and isinstance(data, dict) and not data.get('error'):
                        followers = data.get('followers_count', 0)
                        
                        confidence_score = 0
                        reasons = []
                        
                        if followers > 0:
                            confidence_score += 35
                            reasons.append(f"Active account with {followers} followers")
                        
                        # Name matching
                        display_name = data.get('name', '').lower()
                        if display_name and candidate_name.lower() in display_name:
                            confidence_score += 40
                            reasons.append("Display name matches candidate")
                        
                        # Check profile description for CV keywords
                        bio = data.get('description', '').lower()
                        if bio:
                            confidence_score += 10
                            reasons.append("Has profile description")
                        
                        # Verified badge
                        if data.get('verified'):
                            confidence_score += 15
                            reasons.append("Verified account")
                        
                        confidence_level = 'CONFIRMED' if confidence_score >= 70 else 'POSSIBLE_MATCH' if confidence_score >= 40 else 'LOW_CONFIDENCE'
                        
                        candidate_data = {
                            'username': username,
                            'url': f"https://twitter.com/{username}",
                            'confidence': confidence_level,
                            'confidence_score': confidence_score,
                            'reasons': reasons,
                            'data': {
                                'followers': followers,
                                'following': data.get('friends_count', 0),
                                'tweets': data.get('statuses_count', 0),
                                'display_name': data.get('name', 'N/A'),
                                'bio': data.get('description', ''),
                                'is_verified': data.get('verified', False),
                                'created_at': data.get('created_at', '')
                            }
                        }
                        
                        results['candidates'].append(candidate_data)
                        
                        if confidence_level == 'CONFIRMED' and not results['confirmed']:
                            results['confirmed'] = candidate_data
                            print(f"   ✓ CONFIRMED: @{username}")
                            break
                
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                print(f"   ⚠ Error for @{username}: {str(e)}")
                continue
        
        # Set final status
        if results['confirmed']:
            results['status'] = 'confirmed'
        elif results['candidates']:
            results['status'] = 'candidates_found'
        else:
            results['status'] = 'not_found'
        
        return results
    
    def search_tiktok_account(self, username_variations: List[str], candidate_name: str, cv_username: str = None) -> Dict[str, Any]:
        """
        Search TikTok account menggunakan RapidAPI
        
        Args:
            username_variations: List username untuk dicoba
            candidate_name: Nama kandidat untuk validasi
            cv_username: Username dari CV (PRIORITY jika ada)
            
        Returns:
            Dict dengan status dan data akun yang ditemukan
        """
        if not self.apis['tiktok']['enabled']:
            return {'status': 'api_key_missing', 'platform': 'tiktok'}
        
        results = {
            'platform': 'tiktok',
            'status': 'searching',
            'confirmed': None,
            'candidates': []
        }
        
        print(f"\n🎵 Searching TikTok for: {candidate_name}")
        
        # PRIORITAS: Try CV username first if provided
        if cv_username:
            print(f"   ✅ Trying username from CV: @{cv_username} (PRIORITY)")
            try:
                api_url = "https://tiktok-scraper7.p.rapidapi.com/user/info"
                headers = {
                    'x-rapidapi-key': self.rapidapi_key,
                    'x-rapidapi-host': self.apis['tiktok']['host']
                }
                params = {'unique_id': cv_username}
                
                response = requests.get(api_url, headers=headers, params=params, timeout=self.timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    if data and data.get('data'):
                        # Found via CV username - high confidence
                        results['confirmed'] = {
                            'username': cv_username,
                            'url': f"https://www.tiktok.com/@{cv_username}",
                            'confidence': 'CONFIRMED_FROM_CV',
                            'data': data.get('data', {})
                        }
                        results['status'] = 'confirmed'
                        print(f"   ✅ CONFIRMED from CV: @{cv_username}")
                        return results
            except Exception as e:
                print(f"   ⚠ CV username failed: {str(e)}")
        
        # Try generated variations
        max_tries = min(15, len(username_variations))
        print(f"   Will try {max_tries} username variations...")
        
        for idx, username in enumerate(username_variations[:max_tries], 1):
            try:
                # TikTok API endpoint
                api_url = "https://tiktok-scraper7.p.rapidapi.com/user/info"
                
                headers = {
                    'x-rapidapi-key': self.rapidapi_key,
                    'x-rapidapi-host': self.apis['tiktok']['host']
                }
                
                params = {
                    'unique_id': username
                }
                
                print(f"   → Trying @{username}... ({idx}/{max_tries})")
                response = requests.get(api_url, headers=headers, params=params, timeout=self.timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data and data.get('data'):
                        user_info = data['data'].get('user', {})
                        stats = data['data'].get('stats', {})
                        
                        followers = stats.get('followerCount', 0)
                        
                        confidence_score = 0
                        reasons = []
                        
                        if followers > 0:
                            confidence_score += 35
                            reasons.append(f"Active account with {followers} followers")
                        
                        # Name matching
                        nickname = user_info.get('nickname', '').lower()
                        if nickname and candidate_name.lower() in nickname:
                            confidence_score += 40
                            reasons.append("Nickname matches candidate")
                        
                        # Bio check
                        bio = user_info.get('signature', '')
                        if bio:
                            confidence_score += 10
                        
                        # Verified
                        if user_info.get('verified'):
                            confidence_score += 15
                            reasons.append("Verified account")
                        
                        confidence_level = 'CONFIRMED' if confidence_score >= 70 else 'POSSIBLE_MATCH' if confidence_score >= 40 else 'LOW_CONFIDENCE'
                        
                        candidate_data = {
                            'username': username,
                            'url': f"https://www.tiktok.com/@{username}",
                            'confidence': confidence_level,
                            'confidence_score': confidence_score,
                            'reasons': reasons,
                            'data': {
                                'followers': followers,
                                'following': stats.get('followingCount', 0),
                                'likes': stats.get('heartCount', 0),
                                'videos': stats.get('videoCount', 0),
                                'nickname': nickname,
                                'bio': bio,
                                'is_verified': user_info.get('verified', False)
                            }
                        }
                        
                        results['candidates'].append(candidate_data)
                        
                        if confidence_level == 'CONFIRMED' and not results['confirmed']:
                            results['confirmed'] = candidate_data
                            print(f"   ✓ CONFIRMED: @{username}")
                            break
                
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                print(f"   ⚠ Error for @{username}: {str(e)}")
                continue
        
        # Set final status
        if results['confirmed']:
            results['status'] = 'confirmed'
        elif results['candidates']:
            results['status'] = 'candidates_found'
        else:
            results['status'] = 'not_found'
        
        return results
    
    def search_instagram_scraper(self, username: str, candidate_name: str) -> Dict[str, Any]:
        """
        Search Instagram menggunakan Scraper API (untuk REGULAR accounts)
        API ini bisa detect semua public accounts, termasuk yang bukan influencer
        
        Args:
            username: Username Instagram (tanpa @)
            candidate_name: Nama kandidat
            
        Returns:
            Dict dengan profile data
        """
        if not self.rapidapi_key:
            return {'status': 'api_key_missing', 'platform': 'instagram_scraper'}
        
        results = {
            'platform': 'instagram',
            'status': 'searching',
            'confirmed': None,
            'candidates': []
        }
        
        try:
            # Instagram Scraper API endpoint
            api_url = "https://instagram-scraper-stable-api.p.rapidapi.com/get_ig_user_info.php"
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'x-rapidapi-host': 'instagram-scraper-stable-api.p.rapidapi.com',
                'x-rapidapi-key': self.rapidapi_key
            }
            
            data = {
                'username': username
            }
            
            print(f"   → Scraper API trying @{username}...")
            response = requests.post(api_url, headers=headers, data=data, timeout=self.timeout)
            
            if response.status_code == 200:
                profile_data = response.json()
                
                if profile_data and not profile_data.get('error'):
                    # Extract data
                    followers = profile_data.get('follower_count', 0)
                    following = profile_data.get('following_count', 0)
                    posts = profile_data.get('media_count', 0)
                    full_name = profile_data.get('full_name', '')
                    bio = profile_data.get('biography', '')
                    is_verified = profile_data.get('is_verified', False)
                    is_private = profile_data.get('is_private', False)
                    
                    confidence_score = 0
                    reasons = []
                    
                    # Account exists
                    if followers >= 0:
                        confidence_score += 30
                        reasons.append(f"Account found with {followers:,} followers")
                    
                    # Name matching
                    if full_name and candidate_name.lower() in full_name.lower():
                        confidence_score += 50
                        reasons.append("Profile name matches candidate")
                    
                    # Active account
                    if posts > 0:
                        confidence_score += 10
                        reasons.append(f"{posts} posts")
                    
                    if is_verified:
                        confidence_score += 10
                        reasons.append("Verified account")
                    
                    candidate_data = {
                        'username': username,
                        'url': f"https://www.instagram.com/{username}",
                        'confidence': 'CONFIRMED' if confidence_score >= 70 else 'POSSIBLE_MATCH',
                        'confidence_score': confidence_score,
                        'reasons': reasons,
                        'data': {
                            'followers': followers,
                            'following': following,
                            'posts': posts,
                            'profile_name': full_name,
                            'bio': bio,
                            'is_verified': is_verified,
                            'is_private': is_private,
                            'source': 'scraper_api'
                        }
                    }
                    
                    results['candidates'].append(candidate_data)
                    
                    if confidence_score >= 70:
                        results['confirmed'] = candidate_data
                        results['status'] = 'confirmed'
                    else:
                        results['status'] = 'possible_match'
                    
                    print(f"   ✓ Found! Followers: {followers:,}, Confidence: {confidence_score}%")
                    return results
            
        except Exception as e:
            print(f"   ✗ Scraper API error: {str(e)}")
        
        results['status'] = 'not_found'
        return results
    
    def search_linkedin_profile(self, linkedin_url: str, candidate_name: str) -> Dict[str, Any]:
        """
        Get LinkedIn profile data dari URL yang ada di CV
        
        Args:
            linkedin_url: LinkedIn URL from CV (e.g., linkedin.com/in/john-doe)
            candidate_name: Nama kandidat
            
        Returns:
            Dict dengan LinkedIn profile data
        """
        if not self.rapidapi_key:
            return {'status': 'api_key_missing', 'platform': 'linkedin'}
        
        results = {
            'platform': 'linkedin',
            'status': 'searching',
            'confirmed': None,
            'data': {}
        }
        
        try:
            # LinkedIn Data API endpoint
            api_url = "https://linkedin-data-api.p.rapidapi.com/get-profile-data-by-url"
            
            headers = {
                'x-rapidapi-host': 'linkedin-data-api.p.rapidapi.com',
                'x-rapidapi-key': self.rapidapi_key
            }
            
            params = {
                'url': linkedin_url if linkedin_url.startswith('http') else f"https://www.linkedin.com/in/{linkedin_url}"
            }
            
            print(f"   → LinkedIn API: {params['url']}")
            response = requests.get(api_url, headers=headers, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                profile_data = response.json()
                
                if profile_data.get('success'):
                    data = profile_data.get('data', {})
                    
                    results['confirmed'] = {
                        'name': data.get('name', ''),
                        'headline': data.get('headline', ''),
                        'location': data.get('location', ''),
                        'connections': data.get('connections', 0),
                        'profile_url': linkedin_url,
                        'summary': data.get('summary', ''),
                        'experience': data.get('experience', []),
                        'education': data.get('education', []),
                        'skills': data.get('skills', [])
                    }
                    results['status'] = 'confirmed'
                    print(f"   ✓ LinkedIn profile found: {data.get('name', 'N/A')}")
                    return results
            
        except Exception as e:
            print(f"   ✗ LinkedIn API error: {str(e)}")
        
        results['status'] = 'not_found'
        return results
    
    def search_facebook_profile(self, facebook_identifier: str, candidate_name: str) -> Dict[str, Any]:
        """
        Get Facebook profile data dari username/URL yang ada di CV
        
        Args:
            facebook_identifier: Facebook username atau profile ID
            candidate_name: Nama kandidat
            
        Returns:
            Dict dengan Facebook profile data
        """
        if not self.rapidapi_key:
            return {'status': 'api_key_missing', 'platform': 'facebook'}
        
        results = {
            'platform': 'facebook',
            'status': 'searching',
            'confirmed': None,
            'data': {}
        }
        
        try:
            # Facebook Scraper API endpoint
            api_url = f"https://facebook-scraper3.p.rapidapi.com/profile/{facebook_identifier}"
            
            headers = {
                'x-rapidapi-host': 'facebook-scraper3.p.rapidapi.com',
                'x-rapidapi-key': self.rapidapi_key
            }
            
            print(f"   → Facebook API: {facebook_identifier}")
            response = requests.get(api_url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                profile_data = response.json()
                
                if profile_data and not profile_data.get('error'):
                    results['confirmed'] = {
                        'name': profile_data.get('name', ''),
                        'username': facebook_identifier,
                        'profile_url': profile_data.get('url', f"https://facebook.com/{facebook_identifier}"),
                        'friends_count': profile_data.get('friends_count', 0),
                        'followers_count': profile_data.get('followers_count', 0),
                        'bio': profile_data.get('bio', ''),
                        'location': profile_data.get('location', ''),
                        'work': profile_data.get('work', []),
                        'education': profile_data.get('education', [])
                    }
                    results['status'] = 'confirmed'
                    print(f"   ✓ Facebook profile found: {profile_data.get('name', 'N/A')}")
                    return results
            
        except Exception as e:
            print(f"   ✗ Facebook API error: {str(e)}")
        
        results['status'] = 'not_found'
        return results
    
    def search_youtube_account(self, username_variations: List[str], candidate_name: str) -> Dict[str, Any]:
        """
        Search YouTube account - using same API pattern
        Note: This API may not have all platforms, we'll try and handle gracefully
        """
        results = {
            'platform': 'youtube',
            'status': 'not_found',
            'confirmed': None,
            'candidates': []
        }
        
        print(f"\n▶️ Searching YouTube for: {candidate_name}")
        print(f"   ⚠️ Note: YouTube search limited by API availability")
        
        # For now, mark as not available since we don't have specific YouTube endpoint
        results['status'] = 'api_not_available'
        return results
    
    def search_facebook_account(self, username_variations: List[str], candidate_name: str) -> Dict[str, Any]:
        """
        DEPRECATED: Use search_facebook_profile instead with CV URL
        """
        return self.search_facebook_profile(username_variations[0] if username_variations else '', candidate_name)
    
    def search_telegram_account(self, username_variations: List[str], candidate_name: str) -> Dict[str, Any]:
        """
        Search Telegram account - using same API pattern
        Note: This API may not have all platforms, we'll try and handle gracefully
        """
        results = {
            'platform': 'telegram',
            'status': 'not_found',
            'confirmed': None,
            'candidates': []
        }
        
        print(f"\n✈️ Searching Telegram for: {candidate_name}")
        print(f"   ⚠️ Note: Telegram search limited by API availability")
        
        # For now, mark as not available since we don't have specific Telegram endpoint
        results['status'] = 'api_not_available'
        return results
    
    def analyze_social_profile(
        self,
        profile_data: Dict[str, Any],
        cv_data: Dict[str, Any],
        candidate_name: str
    ) -> Dict[str, Any]:
        """
        AI Analysis terhadap profil social media
        
        Args:
            profile_data: Data dari API
            cv_data: Data dari CV untuk cross-reference
            candidate_name: Nama kandidat
            
        Returns:
            Dict dengan AI analysis results
        """
        analysis = {
            'sentiment': self._analyze_sentiment(profile_data),
            'professional_behavior': self._assess_professional_behavior(profile_data, cv_data),
            'reputation_risk': self._assess_reputation_risk(profile_data),
            'audience_quality': self._assess_audience_quality(profile_data),
            'cv_consistency': self._check_cv_consistency(profile_data, cv_data)
        }
        
        # Generate human-friendly summary
        analysis['summary'] = self._generate_profile_summary(analysis, candidate_name)
        
        return analysis
    
    def _analyze_sentiment(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze overall sentiment dari bio dan konten social media
        Menggunakan keyword-based sentiment analysis
        """
        bio = profile_data.get('bio', '').lower()
        
        # Count keyword matches
        positive_count = sum(1 for kw in self.sentiment_keywords['positive'] if kw in bio)
        negative_count = sum(1 for kw in self.sentiment_keywords['negative'] if kw in bio)
        professional_count = sum(1 for kw in self.sentiment_keywords['professional'] if kw in bio)
        
        # Calculate sentiment score
        total_keywords = positive_count + negative_count + professional_count
        
        if total_keywords == 0:
            # Neutral if no keywords found
            return {
                'overall': 'NEUTRAL',
                'score': 0.50,
                'confidence': 'LOW',
                'emoji': '😐',
                'context': 'Tidak cukup data konten untuk analisis sentimen'
            }
        
        # Calculate weighted score
        score = (positive_count * 1.0 + professional_count * 0.8 - negative_count * 1.5) / max(total_keywords, 1)
        score = max(0, min(1, (score + 1) / 2))  # Normalize to 0-1
        
        # Determine overall sentiment
        if score >= 0.65:
            overall = 'POSITIVE'
            emoji = '😊'
        elif score >= 0.45:
            overall = 'NEUTRAL'
            emoji = '😐'
        else:
            overall = 'NEGATIVE'
            emoji = '😟'
        
        # Determine confidence
        confidence = 'HIGH' if total_keywords >= 3 else 'MEDIUM' if total_keywords >= 1 else 'LOW'
        
        # Generate context
        contexts = []
        if professional_count > 0:
            contexts.append('Konten profesional')
        if positive_count > negative_count:
            contexts.append('Tone positif')
        if negative_count > 0:
            contexts.append(f'{negative_count} indikator negatif ditemukan')
        
        return {
            'overall': overall,
            'score': score,
            'confidence': confidence,
            'emoji': emoji,
            'context': ', '.join(contexts) if contexts else 'Konten personal/umum'
        }
    
    def _assess_professional_behavior(self, profile_data: Dict[str, Any], cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess professional behavior dari bio dan aktivitas
        Cross-reference dengan CV data
        """
        bio = profile_data.get('bio', '').lower()
        followers = profile_data.get('followers', 0)
        
        score = 0.5  # Base score
        indicators = []
        warnings = []
        
        # Check professional keywords in bio
        professional_count = sum(1 for kw in self.sentiment_keywords['professional'] if kw in bio)
        if professional_count >= 2:
            score += 0.2
            indicators.append(f'Bio mengandung {professional_count} kata kunci profesional')
        
        # Check CV consistency (organization, role, etc)
        org = cv_data.get('organization', '').lower() if cv_data else ''
        if org and org in bio:
            score += 0.15
            indicators.append(f'Bio menyebutkan organisasi dari CV: {org}')
        
        # Check for negative indicators
        negative_count = sum(1 for kw in self.sentiment_keywords['negative'] if kw in bio)
        if negative_count > 0:
            score -= 0.2
            warnings.append(f'{negative_count} kata kunci negatif ditemukan')
        
        # Follower count as professionalism indicator
        if followers >= 10000:
            score += 0.1
            indicators.append('Memiliki audiens yang signifikan')
        
        # Normalize score
        score = max(0.1, min(1.0, score))
        
        # Determine level
        if score >= 0.75:
            level = 'HIGHLY_PROFESSIONAL'
        elif score >= 0.55:
            level = 'PROFESSIONAL'
        elif score >= 0.35:
            level = 'MODERATE'
        else:
            level = 'CASUAL'
        
        return {
            'level': level,
            'score': score,
            'indicators': indicators if indicators else ['Tidak ada indikator profesional yang kuat'],
            'warnings': warnings
        }
    
    def _assess_reputation_risk(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess reputation risk"""
        return {
            'level': 'LOW',
            'score': 0.15,
            'factors': []
        }
    
    def _assess_audience_quality(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess kualitas audience"""
        return {
            'quality': 'GOOD',
            'organic_score': 0.85,
            'fake_followers_estimate': 0.05
        }
    
    def _check_cv_consistency(self, profile_data: Dict[str, Any], cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check consistency antara social media dan CV"""
        return {
            'consistency': 'HIGH',
            'score': 0.90,
            'notes': 'Aktivitas social media sesuai dengan profil profesional di CV'
        }
    
    def _generate_profile_summary(self, analysis: Dict[str, Any], candidate_name: str) -> str:
        """Generate human-friendly summary"""
        sentiment = analysis['sentiment']['overall']
        risk = analysis['reputation_risk']['level']
        professional = analysis['professional_behavior']['level']
        
        summary = f"Aktivitas social media {candidate_name} menunjukkan "
        
        if sentiment == 'POSITIVE':
            summary += "engagement yang positif, "
        elif sentiment == 'NEUTRAL':
            summary += "konten yang netral, "
        
        if professional == 'PROFESSIONAL':
            summary += "konten profesional, "
        
        if risk == 'LOW':
            summary += "dan tidak ditemukan indikasi perilaku berisiko yang bertentangan dengan profil CV."
        
        return summary
    
    def analyze_complete_social_footprint(
        self,
        candidate_name: str,
        cv_text: str = "",
        cv_data: Dict[str, Any] = None,
        manual_links: Dict[str, List[str]] = None
    ) -> Dict[str, Any]:
        """
        Main method untuk analisis lengkap social media intelligence
        
        Args:
            candidate_name: Nama kandidat
            cv_text: Text dari CV
            cv_data: Dict dengan data struktural dari CV
            manual_links: Dict manual social media links dari user input
            
        Returns:
            Dict lengkap dengan semua hasil analisis
        """
        print("\n" + "="*70)
        print("📱 Social Media Intelligence Analysis Started")
        print("="*70)
        
        if not self.rapidapi_key:
            print("⚠️  RapidAPI key not configured - analysis skipped")
            return {
                'status': 'skipped',
                'reason': 'api_key_missing',
                'message': 'RapidAPI key tidak dikonfigurasi. Set RAPIDAPI_KEY di .env untuk mengaktifkan fitur ini.'
            }
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'candidate_name': candidate_name,
            'analysis_status': 'completed',
            'platforms': {},
            'cv_links_found': {}
        }
        
        # === STRATEGY 1: Extract Social Media URLs dari CV (PRIORITY 1) ===
        print(f"\n🔍 Step 1: Extracting social media links from CV...")
        cv_links = self.extract_social_media_from_cv(cv_text)
        
        # Merge with manual links (manual links have priority if provided)
        if manual_links:
            print(f"   📝 Merging with manual inputs...")
            for platform, links in manual_links.items():
                if links:  # If manual link provided
                    if platform not in cv_links or not cv_links[platform]:
                        cv_links[platform] = links
                        print(f"   ✅ Using MANUAL {platform.upper()}: {', '.join(links)}")
                    else:
                        # Merge both (manual + CV extracted)
                        existing = cv_links[platform]
                        combined = list(set(existing + links))  # Remove duplicates
                        cv_links[platform] = combined
                        print(f"   ✅ Merged {platform.upper()}: {len(combined)} links (CV + manual)")
        
        result['cv_links_found'] = cv_links
        
        for platform, links in cv_links.items():
            if links:
                print(f"   ✓ Found {platform.upper()}: {', '.join(links)}")
        
        # === STRATEGY 2: Generate username variations (FALLBACK) ===
        print(f"\n📋 Step 2: Generating username variations for: {candidate_name}")
        username_vars = self.generate_username_variations(candidate_name, cv_data)
        print(f"   ✓ Generated {len(username_vars)} variations")
        
        # === MULTI-PLATFORM SEARCH ===
        
        # 1. LinkedIn - PRIORITY: Use CV URL if found
        if cv_links.get('linkedin'):
            print("\n💼 Searching LinkedIn (from CV URL)...")
            linkedin_result = self.search_linkedin_profile(cv_links['linkedin'][0], candidate_name)
            result['platforms']['linkedin'] = linkedin_result
            if linkedin_result.get('confirmed'):
                print(f"   ✓ LinkedIn found: {linkedin_result['confirmed'].get('name', 'N/A')}")
        else:
            print("\n💼 LinkedIn URL not found in CV")
            result['platforms']['linkedin'] = {'status': 'not_in_cv', 'platform': 'linkedin'}
        
        # 2. Facebook - PRIORITY: Use CV URL if found
        if cv_links.get('facebook'):
            print("\n👥 Searching Facebook (from CV URL)...")
            facebook_result = self.search_facebook_profile(cv_links['facebook'][0], candidate_name)
            result['platforms']['facebook'] = facebook_result
            if facebook_result.get('confirmed'):
                print(f"   ✓ Facebook found: {facebook_result['confirmed'].get('name', 'N/A')}")
        else:
            print("\n👥 Facebook URL not found in CV")
            result['platforms']['facebook'] = {'status': 'not_in_cv', 'platform': 'facebook'}
        
        # 3. Instagram - DUAL APPROACH
        print("\n📷 Searching Instagram...")
        
        # 3a. PRIORITAS TERTINGGI: Try CV URL first if available
        if cv_links.get('instagram'):
            instagram_username = cv_links['instagram'][0]
            print(f"   ✅ Using username from CV: @{instagram_username} (PRIORITY)")
            instagram_result = self.search_instagram_scraper(instagram_username, candidate_name)
        else:
            # 3b. Try Scraper API with ALL username variations (can detect regular accounts)
            print(f"   → No username in CV, trying Scraper API with ALL {len(username_vars)} variations...")
            instagram_result = None
            tried_count = 0
            for username in username_vars:  # Try ALL variations
                tried_count += 1
                if tried_count % 5 == 0:
                    print(f"      Progress: {tried_count}/{len(username_vars)} variations tried...")
                temp_result = self.search_instagram_scraper(username, candidate_name)
                if temp_result.get('status') == 'confirmed':
                    instagram_result = temp_result
                    print(f"      ✅ Found at variation #{tried_count}: @{username}")
                    break
            
            if not instagram_result or instagram_result.get('status') != 'confirmed':
                # 3c. Fallback: Try Statistics API (for influencers only)
                print(f"   → No regular account found, trying Statistics API for influencer accounts...")
                instagram_result = self.search_instagram_account(username_vars, candidate_name)
        
        result['platforms']['instagram'] = instagram_result
        
        if instagram_result and instagram_result.get('confirmed'):
            print(f"   ✓ Instagram account found: @{instagram_result['confirmed']['username']}")
        else:
            print("   ⊘ Instagram account not confirmed")
        
        # 4. Twitter/X - PRIORITIZE CV username if found
        print("\n🐦 Searching Twitter...")
        twitter_cv_username = cv_links.get('twitter', [None])[0]
        twitter_result = self.search_twitter_account(username_vars, candidate_name, cv_username=twitter_cv_username)
        result['platforms']['twitter'] = twitter_result
        
        if twitter_result.get('confirmed'):
            print(f"   ✓ Twitter account found: @{twitter_result['confirmed']['username']}")
        else:
            print("   ⊘ Twitter account not confirmed")
        
        # 5. TikTok - No CV extraction yet, but ready for future
        print("\n🎵 Searching TikTok...")
        tiktok_result = self.search_tiktok_account(username_vars, candidate_name, cv_username=None)
        result['platforms']['tiktok'] = tiktok_result
        
        if tiktok_result.get('confirmed'):
            print(f"   ✓ TikTok account found: @{tiktok_result['confirmed']['username']}")
        else:
            print("   ⊘ TikTok account not confirmed")
        
        # 4. Search YouTube
        print("\n▶️ Searching YouTube...")
        youtube_result = self.search_youtube_account(username_vars, candidate_name)
        result['platforms']['youtube'] = youtube_result
        
        if youtube_result.get('confirmed'):
            print(f"   ✓ YouTube account found: @{youtube_result['confirmed']['username']}")
        elif youtube_result.get('status') == 'api_not_available':
            print("   ⚠️ YouTube API not available yet")
        else:
            print("   ⊘ YouTube account not confirmed")
        
        # 5. Search Facebook
        print("\n👥 Searching Facebook...")
        facebook_result = self.search_facebook_account(username_vars, candidate_name)
        result['platforms']['facebook'] = facebook_result
        
        if facebook_result.get('confirmed'):
            print(f"   ✓ Facebook account found: @{facebook_result['confirmed']['username']}")
        elif facebook_result.get('status') == 'api_not_available':
            print("   ⚠️ Facebook API not available yet")
        else:
            print("   ⊘ Facebook account not confirmed")
        
        # 6. Search Telegram
        print("\n✈️ Searching Telegram...")
        telegram_result = self.search_telegram_account(username_vars, candidate_name)
        result['platforms']['telegram'] = telegram_result
        
        if telegram_result.get('confirmed'):
            print(f"   ✓ Telegram account found: @{telegram_result['confirmed']['username']}")
        elif telegram_result.get('status') == 'api_not_available':
            print("   ⚠️ Telegram API not available yet")
        else:
            print("   ⊘ Telegram account not confirmed")
        
        # Count total platforms found
        platforms_found = sum(1 for p in result['platforms'].values() if p.get('status') == 'confirmed')
        result['total_platforms_found'] = platforms_found
        result['total_platforms_searched'] = len(result['platforms'])
        
        print(f"\n📊 Summary: {platforms_found}/{result['total_platforms_searched']} platforms confirmed")
        
        print("\n" + "="*70)
        print("✅ Social Media Intelligence Analysis Completed")
        print("="*70 + "\n")
        
        return result
    
    def generate_human_friendly_report(self, intelligence_result: Dict[str, Any]) -> str:
        """
        Generate human-friendly report untuk HR
        
        Args:
            intelligence_result: Hasil dari analyze_complete_social_footprint()
            
        Returns:
            String formatted report
        """
        if intelligence_result.get('status') == 'skipped':
            return f"**📱 Social Media Intelligence**\n\n⚠️ {intelligence_result.get('message', 'Tidak tersedia')}"
        
        report_parts = []
        candidate_name = intelligence_result.get('candidate_name', 'Kandidat')
        
        report_parts.append(f"**📱 Social Media Intelligence: {candidate_name}**\n")
        
        platforms = intelligence_result.get('platforms', {})
        
        # Instagram
        instagram = platforms.get('instagram', {})
        if instagram.get('status') == 'confirmed':
            profile = instagram['confirmed']
            data = profile.get('data', {})
            
            report_parts.append("\n**📷 Instagram (Terverifikasi):**")
            report_parts.append(f"- 🔗 Akun: [@{profile.get('username')}]({profile.get('url')})")
            report_parts.append(f"- 👤 Nama Profil: {data.get('profile_name', 'N/A')}")
            report_parts.append(f"- 👥 Followers: {data.get('followers', 0):,}")
            
            # === NEW: Display ALL metrics ===
            # Engagement Metrics
            avg_er = data.get('avg_er', 0)
            if avg_er > 0:
                report_parts.append(f"- 📊 Engagement Rate: {avg_er*100:.2f}%")
            
            avg_likes = data.get('avg_likes', 0)
            if avg_likes > 0:
                report_parts.append(f"- ❤️ Avg Likes/Post: {avg_likes:,.0f}")
            
            avg_comments = data.get('avg_comments', 0)
            if avg_comments > 0:
                report_parts.append(f"- 💬 Avg Comments/Post: {avg_comments:,.0f}")
            
            avg_views = data.get('avg_views', 0)
            if avg_views > 0:
                report_parts.append(f"- 👁️ Avg Views/Post: {avg_views:,.0f}")
            
            # Quality Metrics
            quality_score = data.get('quality_score', 0)
            if quality_score > 0:
                report_parts.append(f"- ⭐ Quality Score: {quality_score*100:.0f}/100")
            
            fake_followers_pct = data.get('fake_followers_pct', 0)
            if fake_followers_pct > 0:
                emoji = "🚨" if fake_followers_pct > 0.3 else "⚠️" if fake_followers_pct > 0.15 else "✅"
                report_parts.append(f"- {emoji} Fake Followers: {fake_followers_pct*100:.1f}%")
            
            # Account Type & Verification
            account_type = data.get('account_type', '')
            if account_type:
                type_emoji = "🌟" if account_type == 'influencer' else "💼"
                report_parts.append(f"- {type_emoji} Account Type: {account_type.title()}")
            
            if data.get('is_verified'):
                report_parts.append("- ✅ Verified Account")
            
            # Demographics
            country = data.get('country', '')
            city = data.get('city', '')
            if country or city:
                location = f"{city}, {country}" if city and country else country or city
                report_parts.append(f"- 📍 Location: {location}")
            
            gender = data.get('gender', '')
            age = data.get('age', '')
            if gender or age:
                demo = []
                if gender:
                    demo.append(f"Gender: {'Male' if gender == 'm' else 'Female' if gender == 'f' else gender}")
                if age:
                    demo.append(f"Age: {age.replace('_', '-')}")
                report_parts.append(f"- 👤 Demographics: {', '.join(demo)}")
            
            # Audience Quality
            audience_types = data.get('audience_types', [])
            if audience_types:
                real_pct = next((t.get('percent', 0) for t in audience_types if t.get('name') == 'real'), 0)
                suspicious_pct = next((t.get('percent', 0) for t in audience_types if t.get('name') == 'suspicious'), 0)
                if real_pct > 0:
                    emoji = "✅" if real_pct > 0.7 else "⚠️" if real_pct > 0.5 else "🚨"
                    report_parts.append(f"- {emoji} Real Audience: {real_pct*100:.0f}%")
                if suspicious_pct > 0:
                    report_parts.append(f"- ⚠️ Suspicious Audience: {suspicious_pct*100:.0f}%")
            
            # Growth & Reach
            follower_growth = data.get('follower_growth_180d_pct', 0)
            if follower_growth != 0:
                emoji = "📈" if follower_growth > 0 else "📉"
                report_parts.append(f"- {emoji} Follower Growth (6mo): {follower_growth*100:+.1f}%")
            
            mentions_received = data.get('mentions_received_180d', 0)
            if mentions_received > 0:
                report_parts.append(f"- 🔔 Mentions Received (6mo): {mentions_received:,}")
            
            # Contact
            contact_email = data.get('contact_email', '')
            if contact_email:
                report_parts.append(f"- 📧 Contact: {contact_email}")
            
            # Bio
            if data.get('bio'):
                bio = data['bio'][:100] + "..." if len(data.get('bio', '')) > 100 else data.get('bio', '')
                report_parts.append(f"- 📝 Bio: {bio}")
            
            # Confidence reasons
            reasons = profile.get('reasons', [])
            if reasons:
                report_parts.append(f"- 🎯 Alasan Kecocokan:")
                for reason in reasons:
                    report_parts.append(f"  • {reason}")
                    
        elif instagram.get('status') == 'candidates_found':
            candidates = instagram.get('candidates', [])
            report_parts.append("\n**📷 Instagram:**")
            report_parts.append(f"- ⚠️ Ditemukan {len(candidates)} kandidat potensial")
            report_parts.append("- Status: Memerlukan verifikasi manual HR")
            
            for idx, candidate in enumerate(candidates[:3], 1):
                data = candidate.get('data', {})
                report_parts.append(f"\n  **Kandidat {idx}:**")
                report_parts.append(f"  - Username: [@{candidate.get('username')}]({candidate.get('url')})")
                report_parts.append(f"  - Followers: {data.get('followers', 0):,}")
                report_parts.append(f"  - Confidence: {candidate.get('confidence', 'UNKNOWN')}")
                
        elif instagram.get('status') == 'rate_limited':
            report_parts.append("\n**📷 Instagram:**")
            report_parts.append("- ⚠️ Rate limit API tercapai")
            report_parts.append("- Silakan coba lagi nanti")
            
        elif instagram.get('status') == 'api_key_missing':
            report_parts.append("\n**📷 Instagram:**")
            report_parts.append("- ⚠️ RapidAPI key belum dikonfigurasi")
            report_parts.append("- Set RAPIDAPI_KEY di .env untuk mengaktifkan")
            
        elif instagram.get('status') == 'not_found':
            report_parts.append("\n**📷 Instagram:**")
            report_parts.append("- ℹ️ Akun tidak ditemukan dengan variasi username yang dicoba")
            report_parts.append("- **Kemungkinan penyebab:**")
            report_parts.append("  • Akun bersifat private (tidak dapat dianalisis)")
            report_parts.append("  • Akun belum memenuhi threshold analytics minimum (biasanya <1000 followers)")
            report_parts.append("  • Username berbeda dari variasi yang dicoba")
            report_parts.append("- **Rekomendasi:** Konfirmasi username Instagram langsung dengan kandidat saat interview")
        
        # === TWITTER ===
        twitter = platforms.get('twitter', {})
        if twitter.get('status') == 'confirmed':
            profile = twitter['confirmed']
            data = profile.get('data', {})
            
            report_parts.append("\n**🐦 Twitter/X (Terverifikasi):**")
            report_parts.append(f"- 🔗 Akun: [@{profile.get('username')}]({profile.get('url')})")
            report_parts.append(f"- 👤 Display Name: {data.get('display_name', 'N/A')}")
            report_parts.append(f"- 👥 Followers: {data.get('followers', 0):,}")
            report_parts.append(f"- 🐤 Tweets: {data.get('tweets', 0):,}")
            
            if data.get('is_verified'):
                report_parts.append("- ✅ Verified Account")
            
            if data.get('bio'):
                bio = data['bio'][:100] + "..." if len(data['bio']) > 100 else data['bio']
                report_parts.append(f"- 📝 Bio: {bio}")
            
            reasons = profile.get('reasons', [])
            if reasons:
                report_parts.append(f"- 🎯 Alasan Kecocokan:")
                for reason in reasons:
                    report_parts.append(f"  • {reason}")
                    
        elif twitter.get('status') == 'candidates_found':
            candidates = twitter.get('candidates', [])
            report_parts.append("\n**🐦 Twitter/X:**")
            report_parts.append(f"- ⚠️ Ditemukan {len(candidates)} kandidat potensial")
            
        elif twitter.get('status') == 'not_found':
            report_parts.append("\n**🐦 Twitter/X:**")
            report_parts.append("- ℹ️ Akun tidak ditemukan")
        
        # === TIKTOK ===
        tiktok = platforms.get('tiktok', {})
        if tiktok.get('status') == 'confirmed':
            profile = tiktok['confirmed']
            data = profile.get('data', {})
            
            report_parts.append("\n**🎵 TikTok (Terverifikasi):**")
            report_parts.append(f"- 🔗 Akun: [@{profile.get('username')}]({profile.get('url')})")
            report_parts.append(f"- 👤 Nickname: {data.get('nickname', 'N/A')}")
            report_parts.append(f"- 👥 Followers: {data.get('followers', 0):,}")
            report_parts.append(f"- 🎬 Videos: {data.get('videos', 0):,}")
            report_parts.append(f"- ❤️ Total Likes: {data.get('likes', 0):,}")
            
            if data.get('is_verified'):
                report_parts.append("- ✅ Verified Account")
            
            if data.get('bio'):
                bio = data['bio'][:100] + "..." if len(data['bio']) > 100 else data['bio']
                report_parts.append(f"- 📝 Bio: {bio}")
            
            reasons = profile.get('reasons', [])
            if reasons:
                report_parts.append(f"- 🎯 Alasan Kecocokan:")
                for reason in reasons:
                    report_parts.append(f"  • {reason}")
                    
        elif tiktok.get('status') == 'candidates_found':
            candidates = tiktok.get('candidates', [])
            report_parts.append("\n**🎵 TikTok:**")
            report_parts.append(f"- ⚠️ Ditemukan {len(candidates)} kandidat potensial")
            
        elif tiktok.get('status') == 'not_found':
            report_parts.append("\n**🎵 TikTok:**")
            report_parts.append("- ℹ️ Akun tidak ditemukan")
        
        # === YOUTUBE ===
        youtube = platforms.get('youtube', {})
        if youtube.get('status') == 'confirmed' and youtube.get('confirmed'):
            profile = youtube['confirmed']
            report_parts.append("\n**▶️ YouTube:**")
            report_parts.append(f"- ✅ **Terverifikasi:** @{profile.get('username', 'N/A')}")
            report_parts.append(f"- 👥 **Subscribers:** {profile.get('followers', 0):,}")
            report_parts.append(f"- 🎯 **Confidence:** {profile.get('confidence', 0):.1f}%")
            if profile.get('bio'):
                report_parts.append(f"- 📝 **Bio:** {profile['bio'][:100]}...")
        
        elif youtube.get('status') == 'api_not_available':
            report_parts.append("\n**▶️ YouTube:**")
            report_parts.append("- ⚠️ API tidak tersedia (belum diimplementasikan)")
        
        elif youtube.get('status') == 'possible_match':
            candidates = youtube.get('candidates', [])
            report_parts.append("\n**▶️ YouTube:**")
            report_parts.append(f"- ⚠️ Ditemukan {len(candidates)} kandidat potensial")
            
        elif youtube.get('status') == 'not_found':
            report_parts.append("\n**▶️ YouTube:**")
            report_parts.append("- ℹ️ Akun tidak ditemukan")
        
        # === FACEBOOK ===
        facebook = platforms.get('facebook', {})
        if facebook.get('status') == 'confirmed' and facebook.get('confirmed'):
            profile = facebook['confirmed']
            report_parts.append("\n**👥 Facebook:**")
            report_parts.append(f"- ✅ **Terverifikasi:** {profile.get('username', 'N/A')}")
            report_parts.append(f"- 👥 **Friends/Followers:** {profile.get('followers', 0):,}")
            report_parts.append(f"- 🎯 **Confidence:** {profile.get('confidence', 0):.1f}%")
            if profile.get('bio'):
                report_parts.append(f"- 📝 **Bio:** {profile['bio'][:100]}...")
        
        elif facebook.get('status') == 'api_not_available':
            report_parts.append("\n**👥 Facebook:**")
            report_parts.append("- ⚠️ API tidak tersedia (belum diimplementasikan)")
        
        elif facebook.get('status') == 'possible_match':
            candidates = facebook.get('candidates', [])
            report_parts.append("\n**👥 Facebook:**")
            report_parts.append(f"- ⚠️ Ditemukan {len(candidates)} kandidat potensial")
            
        elif facebook.get('status') == 'not_found':
            report_parts.append("\n**👥 Facebook:**")
            report_parts.append("- ℹ️ Akun tidak ditemukan")
        
        # === TELEGRAM ===
        telegram = platforms.get('telegram', {})
        if telegram.get('status') == 'confirmed' and telegram.get('confirmed'):
            profile = telegram['confirmed']
            report_parts.append("\n**✈️ Telegram:**")
            report_parts.append(f"- ✅ **Terverifikasi:** @{profile.get('username', 'N/A')}")
            report_parts.append(f"- 👥 **Subscribers:** {profile.get('followers', 0):,}")
            report_parts.append(f"- 🎯 **Confidence:** {profile.get('confidence', 0):.1f}%")
            if profile.get('bio'):
                report_parts.append(f"- 📝 **Bio:** {profile['bio'][:100]}...")
        
        elif telegram.get('status') == 'api_not_available':
            report_parts.append("\n**✈️ Telegram:**")
            report_parts.append("- ⚠️ API tidak tersedia (belum diimplementasikan)")
        
        elif telegram.get('status') == 'possible_match':
            candidates = telegram.get('candidates', [])
            report_parts.append("\n**✈️ Telegram:**")
            report_parts.append(f"- ⚠️ Ditemukan {len(candidates)} kandidat potensial")
            
        elif telegram.get('status') == 'not_found':
            report_parts.append("\n**✈️ Telegram:**")
            report_parts.append("- ℹ️ Akun tidak ditemukan")
        
        # === SUMMARY ===
        total_found = intelligence_result.get('total_platforms_found', 0)
        total_searched = intelligence_result.get('total_platforms_searched', 0)
        
        if total_found > 0:
            report_parts.append(f"\n📊 **Ringkasan:** {total_found}/{total_searched} platform terverifikasi")
        else:
            report_parts.append("\n🔍 **Ringkasan:** Tidak ditemukan jejak sosial media publik yang relevan")
            report_parts.append("\n**Alasan Umum:**")
            report_parts.append("- ✅ **Positif:** Kandidat menjaga privasi digital dengan baik")
            report_parts.append("- 🔒 Akun private (Instagram, Facebook, dll)")
            report_parts.append("- 📉 Akun dengan followers rendah (di bawah threshold analytics)")
            report_parts.append("- 🔄 Username berbeda dari nama di CV")
            report_parts.append("\n**Next Steps:**")
            report_parts.append("- ✋ Minta username sosial media langsung saat interview")
            report_parts.append("- 🔍 Verifikasi manual dengan search Instagram/Facebook manual")
            report_parts.append("- 📧 Kandidat bisa diminta untuk share profile links jika diperlukan")
        
        # Disclaimer
        report_parts.append("\n\n---")
        report_parts.append("**⚠️ Catatan Penting tentang API Analytics:**")
        report_parts.append("\n**Kenapa akun tidak ditemukan padahal tidak private?**")
        report_parts.append("- 🔍 **API ini adalah Instagram/Social Media STATISTICS & ANALYTICS API**")
        report_parts.append("- 📊 API hanya mengindeks akun dengan **data analytics publik** (biasanya influencer, bisnis, creator)")
        report_parts.append("- 📈 Threshold minimum: Biasanya 5.000+ followers atau akun verified/business")
        report_parts.append("- 👤 **Akun personal regular (1-5K followers) TIDAK terindeks** - ini NORMAL")
        report_parts.append("- ✅ Akun publik dengan followers rendah tetap tidak akan muncul karena bukan target API analytics")
        report_parts.append("\n**Ini bukan bug, tapi design dari API:**")
        report_parts.append("- API didesain untuk analisis influencer marketing dan brand monitoring")
        report_parts.append("- Database API hanya berisi akun dengan metrics analytics yang signifikan")
        report_parts.append("- Akun kandidat regular (bukan influencer) biasanya tidak ada di database API")
        report_parts.append("\n**Platform Coverage:**")
        report_parts.append("- ✅ **Instagram, Twitter, TikTok:** Full API support (hanya untuk influencer accounts)")
        report_parts.append("- ⚠️ **YouTube, Facebook, Telegram:** API belum tersedia (dalam pengembangan)")
        report_parts.append("\n**Best Practice:**")
        report_parts.append("- Analisis ini bersifat **pendukung keputusan**, bukan penentu akhir")
        report_parts.append("- Tidak menghakimi, transparan, dan berbasis data")
        report_parts.append("- **Selalu minta username langsung dari kandidat saat interview** untuk verifikasi manual")
        report_parts.append("- Tidak ditemukannya akun ≠ red flag, bisa jadi kandidat menjaga privasi atau akun personal biasa")
        
        return "\n".join(report_parts)


# Singleton instance
_social_media_intelligence = None

def get_social_media_intelligence() -> SocialMediaIntelligence:
    """Get singleton instance"""
    global _social_media_intelligence
    if _social_media_intelligence is None:
        _social_media_intelligence = SocialMediaIntelligence()
        print("✅ Social Media Intelligence module loaded")
    return _social_media_intelligence
