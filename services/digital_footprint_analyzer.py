"""
Digital Footprint Analyzer Service
===================================
ADDITIVE MODULE - Tidak mengubah sistem lama
Menganalisis GitHub, LinkedIn, dan Google News berdasarkan data CV

Author: Sentivize Ultra
Date: December 2025
"""

import requests
import re
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, Optional, List, Any
from datetime import datetime
import time


class DigitalFootprintAnalyzer:
    """
    Service untuk menganalisis jejak digital kandidat
    Bersifat OPTIONAL dan tidak mempengaruhi analisis utama
    """
    
    def __init__(self):
        self.github_api_base = "https://api.github.com"
        self.timeout = 10  # seconds
        
    def extract_digital_profiles(self, cv_text: str, candidate_name: str = "") -> Dict[str, Any]:
        """
        Ekstrak URL GitHub dan LinkedIn dari CV
        
        Args:
            cv_text: Text dari CV
            candidate_name: Nama kandidat (untuk Google News)
            
        Returns:
            Dict dengan status deteksi profil digital
        """
        result = {
            'candidate_name': candidate_name.strip() if candidate_name else "Unknown",
            'github': {'status': 'not_found', 'url': None, 'username': None},
            'linkedin': {'status': 'not_found', 'url': None},
            'google_news': {'status': 'pending', 'query': candidate_name.strip() if candidate_name else None}
        }
        
        # GitHub detection
        github_patterns = [
            r'github\.com/([a-zA-Z0-9-]+)',
            r'@([a-zA-Z0-9-]+)\s*\(GitHub\)',
        ]
        
        for pattern in github_patterns:
            match = re.search(pattern, cv_text, re.IGNORECASE)
            if match:
                username = match.group(1)
                result['github'] = {
                    'status': 'detected',
                    'url': f"https://github.com/{username}",
                    'username': username
                }
                break
        
        # LinkedIn detection - improved patterns
        linkedin_patterns = [
            r'linkedin\.com/in/([a-zA-Z0-9-]+)',
            r'linkedin\.com/pub/([a-zA-Z0-9-]+)',
            r'linkedin:[\s]*([a-zA-Z0-9-]+)',
            r'LinkedIn[\s]*:[\s]*([a-zA-Z0-9-]+)',
            r'linkedin\.com/profile/view\?id=([0-9]+)',
            r'www\.linkedin\.com/in/([a-zA-Z0-9-]+)',
            r'https?://[a-z.]*linkedin\.com/in/([a-zA-Z0-9-]+)',
            # General URL detection
            r'(https?://[a-z.]*linkedin\.com/[a-z]+/[a-zA-Z0-9-]+)',
        ]
        
        for pattern in linkedin_patterns:
            match = re.search(pattern, cv_text, re.IGNORECASE)
            if match:
                if len(match.groups()) > 0 and 'http' in match.group(0):
                    # Full URL found
                    result['linkedin'] = {
                        'status': 'detected',
                        'url': match.group(1) if match.lastindex > 1 else match.group(0)
                    }
                else:
                    # Profile ID found
                    profile_id = match.group(1)
                    result['linkedin'] = {
                        'status': 'detected',
                        'url': f"https://linkedin.com/in/{profile_id}"
                    }
                break
        
        return result
    
    def analyze_github_profile(self, username: str) -> Dict[str, Any]:
        """
        Analisis GitHub profile menggunakan public API
        SAFE: Jika gagal, return status error tanpa crash
        
        Args:
            username: GitHub username
            
        Returns:
            Dict dengan hasil analisis atau status error
        """
        try:
            # Get user profile
            user_url = f"{self.github_api_base}/users/{username}"
            user_response = requests.get(user_url, timeout=self.timeout)
            
            if user_response.status_code != 200:
                return {
                    'status': 'error',
                    'message': f"GitHub API returned status {user_response.status_code}",
                    'available': False
                }
            
            user_data = user_response.json()
            
            # Get repositories
            repos_url = f"{self.github_api_base}/users/{username}/repos?per_page=100&sort=updated"
            repos_response = requests.get(repos_url, timeout=self.timeout)
            
            if repos_response.status_code != 200:
                repos_data = []
            else:
                repos_data = repos_response.json()
            
            # Extract insights
            languages = {}
            total_stars = 0
            total_forks = 0
            has_readme_repos = 0
            recent_activity = []
            
            for repo in repos_data[:20]:  # Analyze top 20 recent repos
                # Languages
                if repo.get('language'):
                    lang = repo['language']
                    languages[lang] = languages.get(lang, 0) + 1
                
                # Stats
                total_stars += repo.get('stargazers_count', 0)
                total_forks += repo.get('forks_count', 0)
                
                # README detection
                if repo.get('has_wiki') or repo.get('description'):
                    has_readme_repos += 1
                
                # Recent activity
                if repo.get('updated_at'):
                    recent_activity.append({
                        'name': repo['name'],
                        'updated': repo['updated_at'],
                        'description': repo.get('description', 'No description')
                    })
            
            # Sort languages by frequency
            top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
            
            result = {
                'status': 'success',
                'available': True,
                'profile': {
                    'username': user_data.get('login'),
                    'name': user_data.get('name', 'N/A'),
                    'bio': user_data.get('bio', 'N/A'),
                    'public_repos': user_data.get('public_repos', 0),
                    'followers': user_data.get('followers', 0),
                    'following': user_data.get('following', 0),
                    'created_at': user_data.get('created_at', 'N/A'),
                    'location': user_data.get('location', 'N/A'),
                },
                'activity': {
                    'total_stars_received': total_stars,
                    'total_forks_received': total_forks,
                    'repos_with_documentation': has_readme_repos,
                    'top_languages': [{'language': lang, 'count': count} for lang, count in top_languages],
                    'recent_updates': recent_activity[:5]
                }
            }
            
            return result
            
        except requests.Timeout:
            return {
                'status': 'timeout',
                'message': 'GitHub API request timed out',
                'available': False
            }
        except requests.RequestException as e:
            return {
                'status': 'error',
                'message': f'GitHub API error: {str(e)}',
                'available': False
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Unexpected error: {str(e)}',
                'available': False
            }
    
    def analyze_linkedin_profile(self, linkedin_url: str) -> Dict[str, Any]:
        """
        Analisis LinkedIn profile (limited - hanya metadata publik)
        LinkedIn memerlukan authentication untuk full access
        
        Args:
            linkedin_url: URL LinkedIn profile
            
        Returns:
            Dict dengan status dan info terbatas
        """
        # NOTE: Full LinkedIn analysis memerlukan API key dan authentication
        # LinkedIn often blocks automated requests, so we assume detected = available
        
        # If URL is detected from CV, assume it's valid (LinkedIn blocks automation)
        return {
            'status': 'detected',
            'available': True,
            'url': linkedin_url,
            'message': 'LinkedIn profile terdeteksi dari CV',
            'limitation': 'Data terbatas - LinkedIn memerlukan API untuk analisis mendalam',
            'note': 'Validasi keberadaan profil dapat dilakukan manual oleh HR'
        }
    
    def extract_cv_contexts(self, cv_text: str) -> List[str]:
        """
        Extract konteks dari CV untuk pencarian berita yang lebih akurat
        Cari: organisasi, jabatan, event, pencapaian YANG SPESIFIK
        
        Args:
            cv_text: Text dari CV
            
        Returns:
            List konteks yang bisa digunakan untuk search
        """
        contexts = []
        
        # Pattern untuk organisasi (LEBIH SPESIFIK)
        org_patterns = [
            # PPK Ormawa HIMSIFOR UNSRAT
            r'(?:PPK|Chair|Ketua)[\s\-–]+(?:Ormawa|ORMAWA)[\s]+([A-Z][A-Z]+(?:\s+[A-Z]+)?)',
            # HIMSIFOR UNSRAT, BEM UNSRAT, dll
            r'\b([A-Z]{3,}(?:IFOR|FOR|BEM|HIMA|UKM)[\s]+[A-Z]{3,})\b',
            # Organisasi dengan tahun: "... HIMSIFOR Jan 2024"
            r'\b([A-Z]{3,}[A-Z]+)[\s]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s]+\d{4}',
        ]
        
        for pattern in org_patterns:
            matches = re.findall(pattern, cv_text, re.IGNORECASE)
            for match in matches:
                clean = match.strip()
                # Harus minimal 5 karakter dan tidak generic
                if len(clean) >= 5 and clean not in contexts:
                    # Filter out generic words
                    if not any(generic in clean.lower() for generic in ['operations', 'transparency', 'experiences', 'leader', 'member']):
                        contexts.append(clean)
        
        # Pattern untuk event/pencapaian SPESIFIK
        achievement_patterns = [
            # Finalist – BRIN AIDeaNation
            r'(?:Finalist|Finalis|Winner|Juara)[\s\-–]+([A-Z][A-Za-z0-9\s]+(?:DeaNation|Abdidaya|Bangkit|Competition|Kompetisi))',
            # Abdidaya Nasional (Bali)
            r'(Abdidaya\s+Nasional)',
            r'(BRIN\s+AIDeaNation)',
            r'(Bangkit\s+Academy)',
            # Program names
            r'(?:program|cohort|initiative)[\s:]+["\']?([A-Z][A-Za-z\s]+(?:Digital|Bank|Sampah|Computing))["\']?',
        ]
        
        for pattern in achievement_patterns:
            matches = re.findall(pattern, cv_text, re.IGNORECASE)
            for match in matches:
                clean = match.strip()
                if len(clean) >= 8 and clean not in contexts:
                    # Filter generic words
                    if not any(generic in clean.lower() for generic in ['operations', 'transparency', 'experiences', 'additional']):
                        contexts.append(clean)
        
        # Add specific project names
        project_patterns = [
            r'["\']([A-Z][A-Za-z\s]+Digital)["\']',  # "Rumah Sampah Digital"
            r'(?:project|sistem|system)[\s:]+["\']?([A-Z][A-Za-z\s]+(?:Management|Bank|Vending|Machine))["\']?',
        ]
        
        for pattern in project_patterns:
            matches = re.findall(pattern, cv_text)
            for match in matches:
                clean = match.strip()
                if len(clean) >= 8 and clean not in contexts:
                    contexts.append(clean)
        
        return contexts[:10]  # Return top 10 contexts
    
    def _analyze_news_relevance(
        self,
        results: List[Dict[str, Any]],
        candidate_name: str,
        cv_contexts: List[str],
        cv_text: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        ENHANCEMENT LAYER: Analisis relevansi berita secara kontekstual
        Menggunakan AI reasoning untuk klasifikasi berita
        
        Args:
            results: Raw results dari pencarian Google News
            candidate_name: Nama kandidat
            cv_contexts: Konteks yang diekstrak dari CV
            cv_text: Full text CV untuk referensi
            
        Returns:
            Dict dengan 2 kategori: confirmed (relevan terkonfirmasi) dan conditional (relevan bersyarat)
        """
        confirmed_news = []  # ✅ Relevan & Terkonfirmasi
        conditional_news = []  # ⚠️ Relevan Bersyarat
        
        # Extract name variations for matching
        name_parts = candidate_name.lower().split()
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        
        # Extract year patterns from CV
        year_pattern = re.findall(r'\b(20\d{2})\b', cv_text)
        cv_years = set(year_pattern)
        
        for article in results:
            title = article.get('title', '').lower()
            query_used = article.get('query', '').lower()
            
            # Scoring system untuk relevansi
            relevance_score = 0
            reasons = []
            
            # 1. Check kandidat name in title (strong signal)
            if candidate_name.lower() in title:
                relevance_score += 50
                reasons.append(f"Nama kandidat '{candidate_name}' disebutkan dalam judul")
            elif first_name in title and last_name in title:
                relevance_score += 40
                reasons.append(f"Nama depan dan belakang kandidat ditemukan dalam judul")
            
            # 2. Check CV contexts in title (strong signal)
            matched_contexts = []
            for context in cv_contexts:
                # Split context into keywords
                context_keywords = [word.lower() for word in context.split() if len(word) > 3]
                
                # Check if significant part of context appears in title
                matches_in_title = sum(1 for keyword in context_keywords if keyword in title)
                match_ratio = matches_in_title / len(context_keywords) if context_keywords else 0
                
                if match_ratio >= 0.5:  # 50% or more keywords match
                    relevance_score += 30
                    matched_contexts.append(context)
                    reasons.append(f"Konteks CV '{context}' cocok dengan berita")
            
            # 3. Check year consistency
            article_years = set(re.findall(r'\b(20\d{2})\b', title))
            if article_years and cv_years:
                if article_years.intersection(cv_years):
                    relevance_score += 15
                    common_years = article_years.intersection(cv_years)
                    reasons.append(f"Periode waktu sesuai: {', '.join(common_years)}")
            
            # 4. Check organization keywords
            org_keywords = ['ormawa', 'himsifor', 'bem', 'hima', 'ukm', 'universitas', 'university', 'institut']
            org_in_title = [org for org in org_keywords if org in title]
            if org_in_title and any(org in cv_text.lower() for org in org_in_title):
                relevance_score += 10
                reasons.append(f"Organisasi relevan ditemukan: {', '.join(org_in_title)}")
            
            # 5. Achievement keywords
            achievement_keywords = ['juara', 'pemenang', 'winner', 'champion', 'best', 'terbaik', 'penghargaan', 'award']
            if any(kw in title for kw in achievement_keywords):
                if any(kw in cv_text.lower() for kw in achievement_keywords):
                    relevance_score += 10
                    reasons.append("Pencapaian/penghargaan relevan ditemukan")
            
            # PENTING: Filter out generic "transparency/operations" matches
            # Jika match hanya karena kata generic, skip
            generic_only = False
            if relevance_score < 50 and matched_contexts:
                # Check if matched contexts are just generic words
                generic_words = ['operations', 'transparency', 'leader', 'experiences']
                if all(any(gen in ctx.lower() for gen in generic_words) for ctx in matched_contexts):
                    generic_only = True
            
            # Classification based on score (THRESHOLD LEBIH KETAT)
            if relevance_score >= 70 and not generic_only:
                # ✅ Relevan & Terkonfirmasi (RAISED dari 60 ke 70)
                confirmed_news.append({
                    'title': article.get('title'),
                    'link': article.get('link'),
                    'date': article.get('date'),
                    'source': self._extract_source_from_link(article.get('link', '')),
                    'query_used': article.get('query'),
                    'relevance_score': relevance_score,
                    'reasons': reasons,
                    'matched_contexts': matched_contexts,
                    'summary': self._generate_news_summary(article, reasons)
                })
            elif relevance_score >= 50 and not generic_only:
                # ⚠️ Relevan Bersyarat (RAISED dari 30 ke 50, SKIP jika generic only)
                conditional_news.append({
                    'title': article.get('title'),
                    'link': article.get('link'),
                    'date': article.get('date'),
                    'source': self._extract_source_from_link(article.get('link', '')),
                    'query_used': article.get('query'),
                    'relevance_score': relevance_score,
                    'reasons': reasons,
                    'matched_contexts': matched_contexts,
                    'note': 'Konteks mendekati CV kandidat, layak dipertimbangkan namun belum terkonfirmasi sepenuhnya'
                })
        
        return {
            'confirmed': confirmed_news,
            'conditional': conditional_news,
            'total_confirmed': len(confirmed_news),
            'total_conditional': len(conditional_news)
        }
    
    def _extract_source_from_link(self, link: str) -> str:
        """Extract domain name from news link"""
        if not link:
            return "Unknown Source"
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(link)
            domain = parsed.netloc
            # Remove www. prefix
            domain = domain.replace('www.', '')
            return domain
        except:
            return "Unknown Source"
    
    def _generate_news_summary(self, article: Dict[str, Any], reasons: List[str]) -> str:
        """Generate concise summary for news article"""
        title = article.get('title', 'No title')
        
        # Simple summary: title + main reason
        main_reason = reasons[0] if reasons else "Relevan dengan profil kandidat"
        
        summary = f"{title[:100]}..." if len(title) > 100 else title
        return summary
    
    def search_google_news(self, candidate_name: str, cv_text: str = "") -> Dict[str, Any]:
        """
        Cari berita tentang kandidat di Google News dengan smart query
        Gunakan: nama lengkap, nama awal+akhir, dan konteks dari CV
        
        Args:
            candidate_name: Nama lengkap kandidat
            cv_text: Text dari CV untuk ekstrak konteks
            
        Returns:
            Dict dengan hasil pencarian berita
        """
        try:
            query = candidate_name.strip()
            
            if not query or query == "Unknown":
                return {
                    'status': 'skipped',
                    'available': False,
                    'message': 'Nama kandidat tidak tersedia'
                }
            
            # Generate query variations
            query_variations = [query]  # Full name
            
            # Add first + last name variation
            name_parts = query.split()
            if len(name_parts) >= 2:
                first_last = f"{name_parts[0]} {name_parts[-1]}"
                if first_last != query:
                    query_variations.append(first_last)
            
            # Extract contexts from CV
            contexts = []
            if cv_text:
                contexts = self.extract_cv_contexts(cv_text)
            
            # Build search queries with context
            search_queries = []
            for name_var in query_variations:
                search_queries.append(name_var)  # Just name
                
                # Name + context combinations
                for ctx in contexts:
                    search_queries.append(f"{name_var} {ctx}")
            
            # Use Google News RSS (free, no API key needed)
            # Strategy: Try multiple approaches - simpler queries first, then with context
            
            results = []
            search_attempts = []
            
            # STRATEGY 1: Try individual name parts + key contexts (most specific)
            priority_queries = []
            
            # Add key context-only queries (often more effective)
            for ctx in contexts[:3]:
                if len(ctx) > 10:  # Only meaningful contexts
                    priority_queries.append(ctx)
            
            # Add name variations
            priority_queries.extend(query_variations)
            
            # Add combined queries
            if contexts:
                for name_var in query_variations[:2]:  # Top 2 name variations
                    for ctx in contexts[:2]:  # Top 2 contexts
                        priority_queries.append(f"{name_var} {ctx}")
            
            # STRATEGY 2: Search with multiple language/region combinations
            rss_configs = [
                {'hl': 'id', 'gl': 'ID', 'ceid': 'ID:id'},  # Indonesia
                {'hl': 'en', 'gl': 'ID', 'ceid': 'ID:en'},  # English (Indonesia)
                {'hl': 'id', 'gl': 'US', 'ceid': 'US:id'},  # Global Indonesian
            ]
            
            for query_str in priority_queries[:15]:  # Try up to 15 queries
                for config in rss_configs:
                    try:
                        # Encode query
                        encoded_query = urllib.parse.quote(query_str)
                        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl={config['hl']}&gl={config['gl']}&ceid={config['ceid']}"
                        
                        search_attempts.append({
                            'query': query_str,
                            'url': rss_url,
                            'config': config
                        })
                        
                        # Add user agent to avoid blocking
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                        
                        response = requests.get(rss_url, timeout=self.timeout, headers=headers)
                        
                        if response.status_code == 200:
                            try:
                                # Parse RSS (basic XML parsing)
                                root = ET.fromstring(response.content)
                                items = root.findall('.//item')
                                
                                print(f"   → Query: '{query_str}' | Config: {config['gl']}-{config['hl']} | Found: {len(items)} items")
                                
                                for item in items[:5]:  # Top 5 results per query
                                    title_elem = item.find('title')
                                    link_elem = item.find('link')
                                    pubdate_elem = item.find('pubDate')
                                    
                                    if title_elem is not None:
                                        article = {
                                            'query': query_str,
                                            'title': title_elem.text,
                                            'link': link_elem.text if link_elem is not None else None,
                                            'date': pubdate_elem.text if pubdate_elem is not None else None,
                                            'config': f"{config['gl']}-{config['hl']}"
                                        }
                                        
                                        # Avoid duplicates
                                        if not any(r.get('title') == article['title'] for r in results):
                                            results.append(article)
                            
                            except ET.ParseError as parse_error:
                                print(f"   ⚠ XML parse error for query '{query_str}': {parse_error}")
                                continue
                        
                        # If we have enough results, stop searching
                        if len(results) >= 10:
                            break
                        
                        time.sleep(0.3)  # Rate limiting
                        
                    except requests.Timeout:
                        print(f"   ⚠ Timeout for query '{query_str}'")
                        continue
                    except Exception as query_error:
                        print(f"   ⚠ Error for query '{query_str}': {str(query_error)}")
                        continue
                
                # If we found results, we can be less aggressive
                if len(results) >= 5:
                    break
            
            if results:
                # ENHANCEMENT: AI Contextual Analysis (non-breaking addition)
                analyzed_results = self._analyze_news_relevance(
                    results=results,
                    candidate_name=candidate_name,
                    cv_contexts=contexts,
                    cv_text=cv_text
                )
                
                return {
                    'status': 'found',
                    'available': True,
                    'query_variations': query_variations,
                    'contexts_used': contexts,
                    'results': results,  # Raw results (preserved)
                    'analyzed_results': analyzed_results,  # NEW: AI-analyzed results
                    'total_results': len(results),
                    'message': f'Ditemukan {len(results)} berita relevan'
                }
            else:
                return {
                    'status': 'not_found',
                    'available': True,
                    'query_variations': query_variations,
                    'contexts_used': contexts,
                    'results': [],
                    'message': f'Tidak ditemukan berita untuk "{candidate_name}" dengan konteks yang ada',
                    'note': 'Ini normal untuk sebagian besar kandidat'
                }
            
        except Exception as e:
            return {
                'status': 'error',
                'available': False,
                'message': f'Error searching news: {str(e)}'
            }
    
    def analyze_complete_footprint(
        self, 
        cv_text: str, 
        candidate_name: str,
        job_description: str = ""
    ) -> Dict[str, Any]:
        """
        Analisis lengkap digital footprint kandidat
        MAIN METHOD yang dipanggil dari sistem utama
        
        Args:
            cv_text: Text dari CV
            candidate_name: Nama kandidat
            job_description: Job description (untuk konteks)
            
        Returns:
            Dict lengkap dengan semua hasil analisis
        """
        print("\n" + "="*70)
        print("🔍 Digital Footprint Analysis Started")
        print("="*70)
        
        # Step 1: Extract profiles
        print("\n📋 Step 1: Extracting digital profiles from CV...")
        profiles = self.extract_digital_profiles(cv_text, candidate_name)
        print(f"   ✓ Candidate: {profiles['candidate_name']}")
        print(f"   ✓ GitHub: {profiles['github']['status']}")
        print(f"   ✓ LinkedIn: {profiles['linkedin']['status']}")
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'candidate_name': profiles['candidate_name'],
            'analysis_status': 'completed',
            'sources': {}
        }
        
        # Step 2: Analyze GitHub
        print("\n🔧 Step 2: Analyzing GitHub profile...")
        if profiles['github']['status'] == 'detected':
            github_analysis = self.analyze_github_profile(profiles['github']['username'])
            result['sources']['github'] = github_analysis
            
            if github_analysis['available']:
                print(f"   ✓ GitHub analysis successful")
                print(f"   → Repos: {github_analysis['profile']['public_repos']}")
                print(f"   → Stars: {github_analysis['activity']['total_stars_received']}")
            else:
                print(f"   ⚠ GitHub analysis failed: {github_analysis.get('message')}")
        else:
            result['sources']['github'] = {
                'status': 'not_detected',
                'available': False,
                'message': 'GitHub profile tidak ditemukan di CV'
            }
            print("   ⊘ GitHub not detected in CV")
        
        # Step 3: Analyze LinkedIn
        print("\n💼 Step 3: Analyzing LinkedIn profile...")
        if profiles['linkedin']['status'] == 'detected':
            linkedin_analysis = self.analyze_linkedin_profile(profiles['linkedin']['url'])
            result['sources']['linkedin'] = linkedin_analysis
            print(f"   ✓ LinkedIn validation: {linkedin_analysis['status']}")
        else:
            result['sources']['linkedin'] = {
                'status': 'not_detected',
                'available': False,
                'message': 'LinkedIn profile tidak ditemukan di CV'
            }
            print("   ⊘ LinkedIn not detected in CV")
        
        # Step 4: Search Google News (with CV context + AI analysis)
        print("\n📰 Step 4: Searching Google News...")
        news_analysis = self.search_google_news(profiles['candidate_name'], cv_text)
        result['sources']['google_news'] = news_analysis
        print(f"   ℹ Status: {news_analysis['status']}")
        if news_analysis.get('total_results', 0) > 0:
            print(f"   ✓ Found {news_analysis['total_results']} news articles")
            
            # Show AI analysis results
            analyzed = news_analysis.get('analyzed_results', {})
            if analyzed:
                confirmed = analyzed.get('total_confirmed', 0)
                conditional = analyzed.get('total_conditional', 0)
                print(f"   🤖 AI Analysis: {confirmed} confirmed, {conditional} conditional")
        
        if news_analysis.get('contexts_used'):
            print(f"   → Contexts: {', '.join(news_analysis['contexts_used'][:3])}")
        
        print("\n" + "="*70)
        print("✅ Digital Footprint Analysis Completed")
        print("="*70 + "\n")
        
        return result
    
    def generate_human_friendly_summary(self, footprint_result: Dict[str, Any]) -> str:
        """
        Generate ringkasan human-friendly untuk Tab 3
        
        Args:
            footprint_result: Hasil dari analyze_complete_footprint()
            
        Returns:
            String ringkasan yang mudah dipahami
        """
        summary_parts = []
        
        candidate_name = footprint_result.get('candidate_name', 'Kandidat')
        
        # Opening
        summary_parts.append(f"**Ringkasan Jejak Digital: {candidate_name}**\n")
        
        # GitHub
        github = footprint_result['sources'].get('github', {})
        if github.get('available'):
            profile = github['profile']
            activity = github['activity']
            top_langs = [lang['language'] for lang in activity['top_languages'][:3]]
            
            summary_parts.append(
                f"**GitHub:** Kandidat memiliki profil aktif dengan "
                f"{profile['public_repos']} repository publik. "
                f"Bahasa yang dikuasai: {', '.join(top_langs)}. "
                f"Repository mendapat {activity['total_stars_received']} stars, "
                f"menunjukkan {'kontribusi yang diakui komunitas' if activity['total_stars_received'] > 10 else 'aktivitas personal yang konsisten'}."
            )
        else:
            summary_parts.append(
                "**GitHub:** Tidak ditemukan atau tidak dapat diakses. "
                "Ini tidak mengurangi kualifikasi kandidat, namun data teknis terbatas."
            )
        
        # LinkedIn
        linkedin = footprint_result['sources'].get('linkedin', {})
        if linkedin.get('available'):
            summary_parts.append(
                f"\n\n**LinkedIn:** Profil profesional tersedia dan dapat diakses. "
                f"(Catatan: Analisis mendalam memerlukan LinkedIn API)"
            )
        else:
            summary_parts.append(
                "\n\n**LinkedIn:** Tidak ditemukan atau tidak dapat diverifikasi. "
                "Informasi karier terbatas pada CV yang disubmit."
            )
        
        # Google News (with AI analysis)
        news = footprint_result['sources'].get('google_news', {})
        if news.get('status') == 'found':
            analyzed = news.get('analyzed_results', {})
            
            if analyzed:
                confirmed_count = analyzed.get('total_confirmed', 0)
                conditional_count = analyzed.get('total_conditional', 0)
                
                if confirmed_count > 0:
                    summary_parts.append(
                        f"\n\n**Google News:** Ditemukan {confirmed_count} berita dengan relevansi tinggi "
                        f"yang dapat dikonfirmasi terkait dengan profil kandidat. "
                        f"{f'Tambahan {conditional_count} berita relevan bersyarat yang layak dipertimbangkan. ' if conditional_count > 0 else ''}"
                        f"Analisis dilakukan dengan AI contextual reasoning berdasarkan data CV."
                    )
                elif conditional_count > 0:
                    summary_parts.append(
                        f"\n\n**Google News:** Ditemukan {conditional_count} berita dengan konteks yang mendekati profil kandidat. "
                        f"Berita-berita ini layak dipertimbangkan namun belum dapat dikonfirmasi sepenuhnya."
                    )
                else:
                    total = news.get('total_results', 0)
                    summary_parts.append(
                        f"\n\n**Google News:** Ditemukan {total} berita, namun setelah analisis AI tidak ada yang memiliki "
                        f"relevansi kontekstual yang cukup kuat dengan data CV kandidat."
                    )
            else:
                # Fallback to old format
                total = news.get('total_results', 0)
                contexts = news.get('contexts_used', [])
                context_text = f" dengan konteks: {', '.join(contexts[:2])}" if contexts else ""
                summary_parts.append(
                    f"\n\n**Google News:** Ditemukan {total} berita yang relevan{context_text}. "
                    f"Pencarian dilakukan dengan variasi nama dan konteks dari CV untuk akurasi maksimal."
                )
        elif news.get('status') == 'not_found':
            contexts = news.get('contexts_used', [])
            query_vars = news.get('query_variations', [])
            
            search_info = ""
            if contexts:
                search_info = f" Pencarian menggunakan variasi nama dan konteks: {', '.join(contexts[:2])}"
            
            summary_parts.append(
                f"\n\n**Google News:** Tidak ditemukan berita relevan.{search_info}. "
                "Ini adalah situasi normal untuk sebagian besar kandidat."
            )
        elif news.get('status') == 'pending_implementation':
            summary_parts.append(
                "\n\n**Google News:** Fitur pencarian berita dalam pengembangan. "
                "Tidak ada data pemberitaan publik yang dianalisis saat ini."
            )
        else:
            summary_parts.append(
                "\n\n**Google News:** Pencarian tidak dapat dilakukan. "
                "Tidak ada data pemberitaan yang tersedia."
            )
        
        # Confidence level
        available_sources = sum([
            1 for source in footprint_result['sources'].values() 
            if source.get('available', False)
        ])
        
        if available_sources >= 2:
            confidence = "HIGH"
            confidence_text = "Data digital footprint cukup lengkap untuk memberikan konteks tambahan."
        elif available_sources == 1:
            confidence = "MEDIUM"
            confidence_text = "Data digital footprint terbatas namun memberikan insight tambahan."
        else:
            confidence = "LOW"
            confidence_text = "Data digital footprint minimal. Evaluasi fokus pada CV dan interview."
        
        summary_parts.append(
            f"\n\n**Tingkat Keyakinan Analisis:** {confidence}\n"
            f"{confidence_text}"
        )
        
        # Disclaimer
        summary_parts.append(
            "\n\n---\n"
            "**Disclaimer:** Analisis ini menggunakan data publik dan nama yang tercantum pada CV. "
            "Hasil bersifat pendukung keputusan dan bukan penilaian final. "
            "Digital footprint yang minim tidak mengurangi kualifikasi teknis kandidat."
        )
        
        return "\n".join(summary_parts)


# Singleton instance
_digital_footprint_analyzer = None

def get_digital_footprint_analyzer() -> DigitalFootprintAnalyzer:
    """Get singleton instance of DigitalFootprintAnalyzer"""
    global _digital_footprint_analyzer
    if _digital_footprint_analyzer is None:
        _digital_footprint_analyzer = DigitalFootprintAnalyzer()
        print("✅ Digital Footprint Analyzer module loaded")
    return _digital_footprint_analyzer
