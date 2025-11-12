"""
Services module - Helper functions untuk file handling, column detection, dan web scraping
"""

import pandas as pd
import json
import re
import time
import requests
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
import config


def read_any_file(uploaded_file) -> pd.DataFrame:
    """
    Membaca file yang diupload dengan adaptasi otomatis untuk berbagai struktur data
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        pd.DataFrame: DataFrame dengan kolom yang sudah dinormalisasi
        
    Raises:
        ValueError: Jika format file tidak didukung atau kolom nama tidak ditemukan
    """
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    break
                except:
                    continue
            else:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file)
                
        elif file_extension in ['xlsx', 'xls']:
            # Strategy 1: Try reading all sheets and find the best one
            uploaded_file.seek(0)
            excel_file = pd.ExcelFile(uploaded_file)
            
            best_df = None
            best_score = -1
            
            for sheet_name in excel_file.sheet_names:
                # Try different header rows for each sheet
                for header_row in range(0, min(10, 50)):  # Check up to row 10
                    try:
                        temp_df = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_row)
                        
                        # Skip if empty
                        if temp_df.empty or len(temp_df) == 0:
                            continue
                        
                        # Remove completely empty rows and columns
                        temp_df = temp_df.dropna(how='all', axis=0).dropna(how='all', axis=1)
                        
                        if temp_df.empty or len(temp_df) == 0:
                            continue
                        
                        # Score this dataframe
                        score = 0
                        
                        # Check column names quality
                        valid_cols = 0
                        for col in temp_df.columns:
                            col_str = str(col).lower()
                            # Good column name indicators
                            if not ('unnamed' in col_str or pd.isna(col) or col_str.startswith('column')):
                                valid_cols += 1
                                # Bonus for name-related columns
                                if any(kw in col_str for kw in ['nama', 'name', 'pegawai', 'karyawan', 'nip']):
                                    valid_cols += 3
                        
                        score += valid_cols * 10
                        
                        # Check data quality (non-empty cells)
                        non_empty_ratio = temp_df.notna().sum().sum() / (len(temp_df) * len(temp_df.columns))
                        score += non_empty_ratio * 100
                        
                        # Check if has string data (likely names)
                        string_cols = sum(1 for col in temp_df.columns if temp_df[col].dtype == 'object')
                        score += string_cols * 5
                        
                        # Prefer dataframes with more rows
                        score += min(len(temp_df), 100)
                        
                        if score > best_score:
                            best_score = score
                            best_df = temp_df.copy()
                            
                    except:
                        continue
            
            if best_df is None or len(best_df) == 0:
                raise ValueError("Tidak dapat menemukan data valid dalam file Excel")
            
            df = best_df
            
        elif file_extension == 'json':
            uploaded_file.seek(0)
            df = pd.read_json(uploaded_file)
        else:
            raise ValueError(f"Format file tidak didukung: {file_extension}")
        
        # Clean up dataframe
        # Remove completely empty rows and columns
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1).reset_index(drop=True)
        
        if df.empty or len(df) == 0:
            raise ValueError("File tidak mengandung data yang valid")
        
        # Normalisasi nama kolom: lowercase, strip whitespace, replace spaces
        new_columns = []
        for col in df.columns:
            col_str = str(col).strip().lower()
            col_str = col_str.replace(' ', '_').replace('.', '_').replace('-', '_')
            # Remove special characters
            col_str = ''.join(c if c.isalnum() or c == '_' else '_' for c in col_str)
            # Remove multiple underscores
            while '__' in col_str:
                col_str = col_str.replace('__', '_')
            col_str = col_str.strip('_')
            new_columns.append(col_str if col_str else f'col_{len(new_columns)}')
        
        df.columns = new_columns
        
        # Auto-detect and keep only useful columns (remove mostly empty columns)
        useful_cols = []
        for col in df.columns:
            non_empty_ratio = df[col].notna().sum() / len(df)
            if non_empty_ratio >= 0.1:  # Keep columns with at least 10% data
                useful_cols.append(col)
        
        if useful_cols:
            df = df[useful_cols]
        
        # Validasi: harus ada kolom nama
        name_col = detect_name_column(df)
        if name_col is None:
            # Last resort: use first column with most string data
            for col in df.columns:
                sample = df[col].dropna().head(20)
                if len(sample) > 0:
                    string_count = sum(1 for val in sample if isinstance(val, str) and len(str(val).strip()) > 0)
                    if string_count >= len(sample) * 0.3:
                        print(f"⚠️ Menggunakan kolom '{col}' sebagai kolom nama")
                        name_col = col
                        break
            
            if name_col is None:
                raise ValueError(
                    "Kolom nama tidak ditemukan. Pastikan file memiliki kolom dengan nama karyawan/pegawai.\n"
                    f"Kolom yang ditemukan: {', '.join(df.columns[:15])}"
                )
        
        # Filter out non-name rows (headers, categories, etc)
        df = filter_valid_data_rows(df, name_col)
        
        print(f"✅ File berhasil dibaca: {len(df)} baris, {len(df.columns)} kolom")
        print(f"✅ Kolom nama terdeteksi: '{name_col}'")
        
        return df
        
    except Exception as e:
        raise ValueError(f"Error membaca file: {str(e)}")


def is_non_name_value(value: str) -> bool:
    """
    Deteksi apakah nilai adalah bukan nama (header, kategori, label, etc)
    
    Args:
        value: String value to check
        
    Returns:
        bool: True jika bukan nama sebenarnya
    """
    if not value or not isinstance(value, str):
        return True
    
    value = value.strip()
    if len(value) == 0:
        return True
    
    value_upper = value.upper()
    
    # HANYA skip jika PERSIS SAMA dengan category keywords (bukan contains)
    # Dan semua huruf kapital tanpa campuran
    exact_category_keywords = [
        'KUALIFIKASI PENDIDIKAN', 'PENGALAMAN KERJA', 'RIWAYAT PENDIDIKAN',
        'DATA DIRI', 'INFORMASI PRIBADI', 'PROFILE', 'PROFIL',
        'SKILLS', 'KEMAMPUAN', 'KEAHLIAN'
    ]
    
    # Skip hanya jika nilai PERSIS seperti header/kategori
    if value_upper in exact_category_keywords:
        return True
    
    # Skip jika format seperti "No", "No.", angka saja
    if value_upper in ['NO', 'NO.', 'NOMOR'] or (len(value) <= 3 and value.isdigit()):
        return True
    
    # Skip jika tidak ada huruf sama sekali
    if not any(c.isalpha() for c in value):
        return True
    
    # Skip jika terlalu pendek (< 2 karakter)
    if len(value) < 2:
        return True
    
    # Jangan skip nama yang normal meskipun ada angka atau karakter khusus
    # Nama bisa mengandung gelar (S.Kom, M.Sc), angka (John 2nd), dll
    return False


def filter_valid_data_rows(df: pd.DataFrame, name_col: str) -> pd.DataFrame:
    """
    Filter DataFrame untuk menghapus baris yang bukan data sebenarnya
    (header duplikat, kategori, label, dll)
    
    Args:
        df: DataFrame input
        name_col: Nama kolom yang berisi nama
        
    Returns:
        pd.DataFrame: DataFrame yang sudah difilter
    """
    if name_col not in df.columns:
        return df
    
    # Create mask untuk baris yang valid
    valid_mask = df[name_col].apply(
        lambda x: not is_non_name_value(str(x)) if pd.notna(x) and str(x).strip() else False
    )
    
    # Filter DataFrame
    filtered_df = df[valid_mask].copy()
    
    # Reset index
    filtered_df.reset_index(drop=True, inplace=True)
    
    rows_removed = len(df) - len(filtered_df)
    if rows_removed > 0:
        print(f"🧹 Filtered out {rows_removed} non-data rows (headers/categories)")
    
    return filtered_df


def detect_name_column(df: pd.DataFrame) -> Optional[str]:
    """
    Mendeteksi kolom yang berisi nama karyawan dengan berbagai strategi adaptif
    
    Args:
        df: DataFrame input
        
    Returns:
        str: Nama kolom yang terdeteksi atau None
    """
    # Strategy 1: Exact keyword match
    for col in df.columns:
        col_lower = str(col).lower()
        for keyword in config.NAME_KEYWORDS:
            if keyword in col_lower:
                # Verify it has string data
                sample = df[col].dropna().head(20)
                if len(sample) > 0:
                    string_count = sum(1 for val in sample if isinstance(val, str) and len(str(val).strip()) > 0)
                    if string_count >= len(sample) * 0.3:
                        return col
    
    # Strategy 2: Analyze column content for name-like patterns
    best_col = None
    best_score = 0
    
    for i, col in enumerate(df.columns[:min(10, len(df.columns))]):
        if 'unnamed' in str(col).lower():
            continue
            
        if df[col].dtype != 'object':
            continue
        
        sample = df[col].dropna().head(50)
        if len(sample) < 3:
            continue
        
        score = 0
        
        # Check string values and filter out non-name entries
        string_values = []
        for val in sample:
            if not isinstance(val, str):
                continue
            val_str = str(val).strip()
            if len(val_str) == 0:
                continue
            
            # Skip if it looks like a category/header/label
            if is_non_name_value(val_str):
                continue
                
            string_values.append(val_str)
        
        if len(string_values) < len(sample) * 0.5:
            continue
        
        # Score based on name characteristics
        has_spaces = sum(1 for val in string_values if ' ' in val)
        has_capitals = sum(1 for val in string_values if any(c.isupper() for c in val))
        avg_length = sum(len(val) for val in string_values) / len(string_values) if string_values else 0
        unique_ratio = len(set(string_values)) / len(string_values) if string_values else 0
        
        # Names usually have spaces (first + last name)
        score += (has_spaces / len(string_values)) * 30
        
        # Names usually have capitals
        score += (has_capitals / len(string_values)) * 20
        
        # Names are typically 5-50 characters
        if 5 <= avg_length <= 50:
            score += 20
        
        # Names should be mostly unique
        if unique_ratio > 0.7:
            score += 20
        
        # Prefer earlier columns
        score += (10 - i) * 2
        
        # Check if values look like names (not numbers, URLs, emails)
        non_name_patterns = 0
        for val in string_values[:20]:
            val_lower = val.lower()
            if any(pattern in val_lower for pattern in ['@', 'http', 'www', '.com', '.id', '://']):
                non_name_patterns += 1
            digits = sum(c.isdigit() for c in val)
            if digits > len(val) * 0.5:
                non_name_patterns += 1
        
        if non_name_patterns > len(string_values) * 0.3:
            score *= 0.3
        
        if score > best_score:
            best_score = score
            best_col = col
    
    if best_col and best_score > 20:
        return best_col
    
    # Strategy 3: Check columns with string values
    for col in df.columns:
        if 'unnamed' not in str(col).lower():
            sample = df[col].dropna().head(10)
            if len(sample) > 0:
                string_count = sum(1 for val in sample if isinstance(val, str) and 3 < len(str(val)) < 100)
                if string_count >= len(sample) * 0.5:
                    return col
    
    # Strategy 4: Use first column with data (even unnamed)
    for col in df.columns:
        if df[col].notna().sum() > 0:
            sample = df[col].dropna().head(10)
            string_count = sum(1 for val in sample if isinstance(val, str) and len(str(val).strip()) > 2)
            if string_count >= len(sample) * 0.5:
                return col
    
    return None


def detect_columns(df: pd.DataFrame) -> Dict[str, Optional[str]]:
    """
    Mengidentifikasi kolom-kolom penting dalam DataFrame
    
    Args:
        df: DataFrame input
        
    Returns:
        Dict dengan keys: name_col, social_col, text_col, position_col, unit_col
    """
    result = {
        'name_col': None,
        'social_col': None,
        'text_col': None,
        'position_col': None,
        'unit_col': None
    }
    
    # Detect name column using smart detection
    result['name_col'] = detect_name_column(df)
    
    # Detect social media column
    for col in df.columns:
        col_lower = str(col).lower()
        for keyword in config.SOCIAL_KEYWORDS:
            if keyword in col_lower and result['social_col'] is None:
                result['social_col'] = col
                break
    
    # Detect text/bio column
    for col in df.columns:
        col_lower = str(col).lower()
        for keyword in config.TEXT_KEYWORDS:
            if keyword in col_lower and result['text_col'] is None:
                result['text_col'] = col
                break
    
    # Detect position column
    for col in df.columns:
        col_lower = str(col).lower()
        for keyword in config.POSITION_KEYWORDS:
            if keyword in col_lower and result['position_col'] is None:
                result['position_col'] = col
                break
    
    # Detect unit/department column
    for col in df.columns:
        col_lower = str(col).lower()
        for keyword in config.UNIT_KEYWORDS:
            if keyword in col_lower and result['unit_col'] is None:
                result['unit_col'] = col
                break
    
    # Auto-detect by content if keywords didn't work
    if result['position_col'] is None:
        for col in df.columns:
            if col == result['name_col']:
                continue
            if df[col].dtype == 'object':
                sample = df[col].dropna().head(20)
                if len(sample) > 0:
                    position_indicators = ['kepala', 'ketua', 'direktur', 'manajer', 'manager', 
                                          'staff', 'anggota', 'koordinator', 'supervisor']
                    sample_str = ' '.join([str(val).lower() for val in sample])
                    if any(ind in sample_str for ind in position_indicators):
                        result['position_col'] = col
                        break
    
    # Use longest text column as text_col if not found
    if result['text_col'] is None:
        longest_col = None
        max_avg_length = 0
        for col in df.columns:
            if col in [result['name_col'], result['social_col'], result['position_col'], result['unit_col']]:
                continue
            if df[col].dtype == 'object':
                sample = df[col].dropna().head(30)
                if len(sample) > 0:
                    avg_len = sum(len(str(val)) for val in sample) / len(sample)
                    if avg_len > max_avg_length and avg_len > 20:
                        max_avg_length = avg_len
                        longest_col = col
        result['text_col'] = longest_col
    
    return result


def find_social_media_links(name: str, max_results: int = 3) -> List[str]:
    """
    Mencari profil sosial media berdasarkan nama menggunakan web search
    
    Args:
        name: Nama karyawan
        max_results: Jumlah maksimal hasil pencarian
        
    Returns:
        List[str]: List URL profil sosial media yang ditemukan
    """
    links = []
    
    try:
        # Coba menggunakan DuckDuckGo search (lebih stabil, tidak perlu API key)
        from duckduckgo_search import DDGS
        
        search_queries = [
            f"{name} linkedin",
            f"{name} instagram",
            f"{name} facebook"
        ]
        
        for query in search_queries:
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=2))
                    for result in results:
                        url = result.get('href', result.get('link', ''))
                        if url and any(platform in url.lower() for platform in config.SOCIAL_PLATFORMS):
                            if url not in links:
                                links.append(url)
                                if len(links) >= max_results:
                                    return links
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"Error searching with query '{query}': {str(e)}")
                continue
        
    except ImportError:
        # Fallback ke googlesearch jika duckduckgo tidak tersedia
        try:
            from googlesearch import search
            
            for query in [f"{name} site:linkedin.com", f"{name} site:instagram.com"]:
                try:
                    for url in search(query, num_results=2, sleep_interval=2):
                        if url not in links:
                            links.append(url)
                            if len(links) >= max_results:
                                return links
                except Exception as e:
                    print(f"Error with Google search: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error importing search libraries: {str(e)}")
    
    except Exception as e:
        print(f"Error in find_social_media_links: {str(e)}")
    
    return links


def fetch_public_posts_from_url(url: str, limit: int = 5) -> List[str]:
    """
    Mengekstrak teks publik dari URL (bio/posts)
    CATATAN: Implementasi sederhana - untuk production perlu library khusus per platform
    
    Args:
        url: URL profil sosial media
        limit: Limit jumlah post/text yang diambil
        
    Returns:
        List[str]: List teks yang berhasil diekstrak
    """
    texts = []
    
    try:
        # Set user agent untuk menghindari blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title sebagai bio
        title = soup.find('title')
        if title and title.string:
            texts.append(title.string.strip())
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            texts.append(meta_desc.get('content').strip())
        
        # Extract paragraphs (sederhana, mungkin termasuk noise)
        paragraphs = soup.find_all('p')
        for p in paragraphs[:limit]:
            text = p.get_text().strip()
            if len(text) > 20:  # Filter text pendek
                texts.append(text)
                if len(texts) >= limit:
                    break
        
    except Exception as e:
        print(f"Error fetching from {url}: {str(e)}")
    
    return texts[:limit]


def create_fallback_text(name: str, position: Optional[str] = None, 
                        unit: Optional[str] = None) -> str:
    """
    Membuat teks fallback untuk analisis jika scraping tidak berhasil
    
    Args:
        name: Nama karyawan
        position: Jabatan (opsional)
        unit: Unit kerja (opsional)
        
    Returns:
        str: Teks fallback untuk analisis
    """
    parts = [f"{name}"]
    
    if position:
        parts.append(f"bekerja sebagai {position}")
    
    if unit:
        parts.append(f"di unit {unit}")
    
    parts.append("memiliki minat dan kompetensi di bidang profesional")
    
    return " ".join(parts)


def extract_social_links_from_text(text: str) -> List[str]:
    """
    Ekstrak URL sosial media dari teks
    
    Args:
        text: Teks yang mungkin mengandung URL
        
    Returns:
        List[str]: List URL yang ditemukan
    """
    if pd.isna(text) or not isinstance(text, str):
        return []
    
    links = []
    # Pattern untuk mendeteksi URL
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    found_urls = re.findall(url_pattern, text)
    
    for url in found_urls:
        if any(platform in url.lower() for platform in config.SOCIAL_PLATFORMS):
            links.append(url)
    
    return links


def clean_text(text: str, max_length: int = None) -> str:
    """
    Membersihkan dan memotong teks untuk analisis
    
    Args:
        text: Teks input
        max_length: Panjang maksimal karakter
        
    Returns:
        str: Teks yang sudah dibersihkan
    """
    if not text or pd.isna(text):
        return ""
    
    # Convert to string
    text = str(text)
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text
