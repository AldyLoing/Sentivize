"""
Configuration untuk Groq AI Integration
"""

import os
from typing import Optional


class GroqConfig:
    """Configuration untuk Groq AI"""
    
    # Groq API Configuration
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama3-8b-8192"  # Default model
    GROQ_TEMPERATURE: float = 0.7
    GROQ_MAX_TOKENS: int = 2048
    
    # Available models
    AVAILABLE_MODELS = {
        "llama3-8b-8192": {
            "name": "Llama 3 8B",
            "description": "Fast, balanced performance",
            "tokens": 8192
        },
        "llama3-70b-8192": {
            "name": "Llama 3 70B",
            "description": "Highest quality, slower",
            "tokens": 8192
        },
        "mixtral-8x7b-32768": {
            "name": "Mixtral 8x7B",
            "description": "Great for complex reasoning",
            "tokens": 32768
        },
        "gemma-7b-it": {
            "name": "Gemma 7B",
            "description": "Google's model, good for instructions",
            "tokens": 8192
        }
    }
    
    @classmethod
    def load_from_env(cls):
        """Load configuration dari environment variables"""
        cls.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        
        # Optional: Load other configs
        model = os.getenv("GROQ_MODEL")
        if model and model in cls.AVAILABLE_MODELS:
            cls.GROQ_MODEL = model
        
        temp = os.getenv("GROQ_TEMPERATURE")
        if temp:
            try:
                cls.GROQ_TEMPERATURE = float(temp)
            except:
                pass
    
    @classmethod
    def is_groq_available(cls) -> bool:
        """Check if Groq API is configured"""
        if not cls.GROQ_API_KEY:
            cls.load_from_env()
        return cls.GROQ_API_KEY is not None and len(cls.GROQ_API_KEY) > 0
    
    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """Get Groq API key"""
        if not cls.GROQ_API_KEY:
            cls.load_from_env()
        return cls.GROQ_API_KEY
    
    @classmethod
    def set_api_key(cls, api_key: str):
        """Set Groq API key"""
        cls.GROQ_API_KEY = api_key


# Analysis configuration
class AnalysisConfig:
    """Configuration untuk analysis settings"""
    
    # Default analysis modes
    USE_GROQ_AI: bool = True
    USE_MOCK_MODELS: bool = True  # For traditional NLP
    
    # Employee analysis settings
    ENABLE_SOCIAL_SCRAPING: bool = False
    ENABLE_BEHAVIORAL_ANALYSIS: bool = True
    ENABLE_CLUSTERING: bool = True
    
    # CV analysis settings
    ENABLE_DEEP_PARSING: bool = True
    ENABLE_PERSONALITY_ASSESSMENT: bool = True
    ENABLE_CULTURAL_FIT: bool = True
    
    # Performance settings
    MAX_SOCIAL_POSTS: int = 20  # Limit posts untuk API call
    CV_TEXT_LIMIT: int = 4000  # Limit CV text untuk Groq API
    BATCH_SIZE: int = 5  # Batch size untuk batch analysis


# Initialize from environment
GroqConfig.load_from_env()


def get_groq_status() -> dict:
    """Get current Groq configuration status"""
    return {
        "available": GroqConfig.is_groq_available(),
        "api_key_set": GroqConfig.GROQ_API_KEY is not None,
        "model": GroqConfig.GROQ_MODEL,
        "temperature": GroqConfig.GROQ_TEMPERATURE,
        "max_tokens": GroqConfig.GROQ_MAX_TOKENS
    }


def display_groq_info() -> str:
    """Display Groq configuration info untuk UI"""
    if GroqConfig.is_groq_available():
        model_info = GroqConfig.AVAILABLE_MODELS.get(
            GroqConfig.GROQ_MODEL,
            {"name": GroqConfig.GROQ_MODEL}
        )
        return f"""
✅ **Groq AI Status:** Active
📦 **Model:** {model_info['name']}
🎯 **Mode:** Deep Reasoning
"""
    else:
        return """
⚠️ **Groq AI Status:** Not configured
💡 **Note:** Using traditional NLP analysis
🔧 **Setup:** Set GROQ_API_KEY environment variable
"""


if __name__ == "__main__":
    print("🔧 Groq Configuration")
    print("=" * 60)
    
    status = get_groq_status()
    print(f"Groq Available: {status['available']}")
    print(f"API Key Set: {status['api_key_set']}")
    print(f"Model: {status['model']}")
    print(f"Temperature: {status['temperature']}")
    
    print("\n" + display_groq_info())
