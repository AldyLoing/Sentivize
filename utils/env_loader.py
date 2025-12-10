"""
Environment loader utility
Load environment variables dari .env file
"""

import os
from pathlib import Path


def load_env():
    """
    Load environment variables dari .env file
    Manual implementation (tanpa python-dotenv dependency)
    """
    env_path = Path(__file__).parent.parent / '.env'
    
    if not env_path.exists():
        print("⚠️ File .env tidak ditemukan. Copy .env.example menjadi .env")
        return False
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments dan empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Set environment variable jika belum ada
                    if key and not os.getenv(key):
                        os.environ[key] = value
        
        print("✅ Environment variables loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error loading .env file: {e}")
        return False


def get_openrouter_api_key() -> str:
    """
    Get OpenRouter API key dari environment
    
    Returns:
        API key string atau empty string jika tidak ada
    """
    return os.getenv('OPENROUTER_API_KEY', '')


def validate_api_keys() -> dict:
    """
    Validate semua API keys yang diperlukan
    
    Returns:
        Dict dengan status validasi
    """
    status = {}
    
    # OpenRouter
    openrouter_key = get_openrouter_api_key()
    status['openrouter'] = {
        'configured': bool(openrouter_key),
        'key_preview': f"{openrouter_key[:15]}..." if openrouter_key else "Not set"
    }
    
    return status


# Auto-load saat module di-import
load_env()
