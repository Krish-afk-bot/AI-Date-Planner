import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Groq AI
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GROQ_TEXT_MODEL = 'llama-3.3-70b-versatile'
    GROQ_BASE_URL = 'https://api.groq.com/openai/v1'

    # Embedding (local sentence-transformers)
    EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

    # Google Places API
    GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', '')
    GOOGLE_PLACES_BASE_URL = 'https://maps.googleapis.com/maps/api/place'

    # Firebase
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', '')

    # RAG
    RAG_TOP_K = 3
    RAG_SIMILARITY_THRESHOLD = 0.5

    # Planner
    PLANNER_MAX_RETRIES = 2
    PLANNER_TEMPERATURE = 0.7

    # Server
    PORT = 5001
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

def validate_config():
    """Validate required configuration"""
    if not Config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is required")
    if not Config.GOOGLE_PLACES_API_KEY:
        raise ValueError("GOOGLE_PLACES_API_KEY is required")
    key = Config.GROQ_API_KEY
    print(f"[OK] Config validated. Groq key: {key[:8]}...{key[-8:]} ({len(key)} chars)")