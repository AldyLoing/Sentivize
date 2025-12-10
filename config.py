"""
Configuration file untuk aplikasi analisis karyawan
Berisi konstanta, model names, dan settings
"""

import os

# ============================================================
# AI ENGINE CONFIGURATION
# ============================================================

# OpenRouter API Configuration (NEW - untuk semantic reasoning)
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_MODEL = "deepseek/deepseek-chat"  # Free model
OPENROUTER_TEMPERATURE = 0.3  # Low temperature untuk hasil stabil
OPENROUTER_MAX_TOKENS = 2000

# Fallback: Legacy Transformers Models
# Model Configuration
SENTIMENT_MODEL = "indobenchmark/indobert-base-p1"  # Model untuk Bahasa Indonesia
SENTIMENT_MODEL_FALLBACK = "nlptown/bert-base-multilingual-uncased-sentiment"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# Processing Limits
MAX_TEXT_LENGTH = 512  # Maximum characters untuk input model
MAX_POSTS_PER_ACCOUNT = 5  # Limit jumlah post yang dianalisis
MAX_SEARCH_RESULTS = 3  # Jumlah link sosial media yang dicari

# Column Detection Keywords
NAME_KEYWORDS = ['name', 'nama', 'nama lengkap', 'full name', 'employee name', 'pegawai', 
                 'karyawan', 'nip', 'no', 'nomor', 'staff']
SOCIAL_KEYWORDS = ['social', 'sosial', 'instagram', 'linkedin', 'twitter', 'facebook', 
                   'ig', 'link', 'profile', 'profil', 'media sosial', 'social media']
TEXT_KEYWORDS = ['text', 'bio', 'description', 'deskripsi', 'keterangan', 'about', 
                 'tentang', 'info', 'informasi']
POSITION_KEYWORDS = ['position', 'jabatan', 'posisi', 'role', 'title', 'job']
UNIT_KEYWORDS = ['unit', 'department', 'departemen', 'divisi', 'division', 'team']

# Social Media Platforms
SOCIAL_PLATFORMS = [
    'linkedin.com',
    'instagram.com',
    'facebook.com',
    'twitter.com',
    'x.com',
    'tiktok.com'
]

# Sentiment Labels
SENTIMENT_POSITIVE = "POSITIVE"
SENTIMENT_NEGATIVE = "NEGATIVE"
SENTIMENT_NEUTRAL = "NEUTRAL"

# File Settings
OUTPUT_FILENAME = "hasil_analisis.xlsx"
SUPPORTED_FILE_TYPES = ["csv", "xlsx", "xls", "json"]

# UI Settings
PROGRESS_UPDATE_INTERVAL = 1  # Update progress bar setiap N kandidat
