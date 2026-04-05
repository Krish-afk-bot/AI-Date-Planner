import google.generativeai as genai
import numpy as np
from config import Config

# Configure Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)

def get_text_model():
    """Get text generation model"""
    return genai.GenerativeModel(
        model_name=Config.GEMINI_TEXT_MODEL,
        generation_config={
            'temperature': Config.PLANNER_TEMPERATURE,
            'max_output_tokens': 8192,
        }
    )

def get_embedding_model():
    """Get embedding model"""
    return genai.GenerativeModel(Config.GEMINI_EMBEDDING_MODEL)

def generate_embedding(text: str) -> list:
    """Generate embeddings for text"""
    try:
        # Use the model name directly without 'models/' prefix
        result = genai.embed_content(
            model=Config.GEMINI_EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise Exception("Failed to generate embedding")

def generate_text(prompt: str, system_instruction: str = None, temperature: float = None) -> str:
    """Generate text with Gemini"""
    try:
        if temperature is None:
            temperature = Config.PLANNER_TEMPERATURE
            
        model = genai.GenerativeModel(
            model_name=Config.GEMINI_TEXT_MODEL,
            system_instruction=system_instruction,
            generation_config={
                'temperature': temperature,
                'max_output_tokens': 8192,
            }
        )
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating text: {e}")
        raise Exception("Failed to generate text")

def cosine_similarity(a: list, b: list) -> float:
    """Calculate cosine similarity between two vectors"""
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    
    a_np = np.array(a)
    b_np = np.array(b)
    
    dot_product = np.dot(a_np, b_np)
    norm_a = np.linalg.norm(a_np)
    norm_b = np.linalg.norm(b_np)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return float(dot_product / (norm_a * norm_b))