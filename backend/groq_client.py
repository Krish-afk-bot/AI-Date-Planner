from groq import Groq
import numpy as np
from config import Config
from sentence_transformers import SentenceTransformer

# Initialize Groq client
client = Groq(api_key=Config.GROQ_API_KEY)

# Initialize local embedding model (lightweight and fast)
embedding_model = None

def get_embedding_model():
    """Lazy load embedding model"""
    global embedding_model
    if embedding_model is None:
        print(f"Loading embedding model: {Config.EMBEDDING_MODEL}")
        embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
    return embedding_model

def generate_embedding(text: str) -> list:
    """Generate embeddings for text using local model"""
    try:
        model = get_embedding_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    except Exception as e:
        print(f"⚠️ Warning: Embedding failed - {e}")
        print("⚠️ Returning dummy embedding")
        # Return a dummy embedding vector (384 dimensions for all-MiniLM-L6-v2)
        import random
        return [random.random() for _ in range(384)]

def generate_text(prompt: str, system_instruction: str = None, temperature: float = None) -> str:
    """Generate text with Groq"""
    try:
        if temperature is None:
            temperature = Config.PLANNER_TEMPERATURE
        
        messages = []
        if system_instruction:
            messages.append({
                "role": "system",
                "content": system_instruction
            })
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        response = client.chat.completions.create(
            model=Config.GROQ_TEXT_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=8192,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating text: {e}")
        raise Exception(f"Failed to generate text: {str(e)}")

def generate_text_stream(prompt: str, system_instruction: str = None, temperature: float = None):
    """Generate text with Groq (streaming)"""
    try:
        if temperature is None:
            temperature = Config.PLANNER_TEMPERATURE
        
        messages = []
        if system_instruction:
            messages.append({
                "role": "system",
                "content": system_instruction
            })
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        stream = client.chat.completions.create(
            model=Config.GROQ_TEXT_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=8192,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        print(f"Error generating text stream: {e}")
        raise Exception(f"Failed to generate text stream: {str(e)}")

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
