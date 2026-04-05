import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_TEXT_MODEL = 'gemini-2.5-flash'
    GEMINI_EMBEDDING_MODEL = 'gemini-embedding-001'
    
    # Google Places API
    GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', '')
    GOOGLE_PLACES_BASE_URL = 'https://maps.googleapis.com/maps/api/place'
    
    # Firebase
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', '')
    
    # RAG Configuration
    RAG_TOP_K = 3
    RAG_SIMILARITY_THRESHOLD = 0.5
    
    # Planner Configuration
    PLANNER_MAX_RETRIES = 2
    PLANNER_TEMPERATURE = 0.7
    
    # Server Configuration
    PORT = 5001
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

def validate_config():
    """Validate required configuration"""
    if not Config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is required")
    if not Config.GOOGLE_PLACES_API_KEY:
        raise ValueError("GOOGLE_PLACES_API_KEY is required")
    if not Config.FIREBASE_PROJECT_ID:
        raise ValueError("FIREBASE_PROJECT_ID is required")
    print("✅ Configuration validated")