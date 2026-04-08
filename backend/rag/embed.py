from gemini_client import generate_embedding
from rag.kb_docs import KNOWLEDGE_BASE_DOCUMENTS
from models import KBDocument
from datetime import datetime
import json
import os

# In-memory cache for local development
cached_kb_documents = []
is_initialized = False

def load_city_guides():
    """Load city guides from JSON file"""
    city_guides_path = os.path.join(os.path.dirname(__file__), 'city_guides.json')
    try:
        with open(city_guides_path, 'r') as f:
            city_guides = json.load(f)
            # Convert to KB document format
            return [
                {
                    'id': guide['id'],
                    'title': f"{guide['city']} - {guide['occasion'][0] if guide['occasion'] else 'general'}",
                    'content': guide['tip_text'],
                    'tags': [guide['city'], guide['budget_tier']] + guide['personality_tags'] + guide['occasion']
                }
                for guide in city_guides
            ]
    except Exception as e:
        print(f"Error loading city guides: {e}")
        return []

def initialize_knowledge_base():
    """Initialize knowledge base by embedding all documents"""
    global cached_kb_documents, is_initialized
    
    if is_initialized and len(cached_kb_documents) > 0:
        print("Knowledge base already initialized")
        return
    
    print("Initializing knowledge base...")
    cached_kb_documents = []
    
    # Load both original KB docs and city guides
    all_documents = KNOWLEDGE_BASE_DOCUMENTS + load_city_guides()
    
    for doc in all_documents:
        try:
            # Generate embedding
            embedding = generate_embedding(doc['content'])
            
            kb_doc = KBDocument(
                id=doc['id'],
                title=doc['title'],
                content=doc['content'],
                tags=doc['tags'],
                embedding=embedding,
                createdAt=datetime.now()
            )
            
            cached_kb_documents.append(kb_doc)
            print(f"Embedded: {doc['title']}")
        except Exception as e:
            print(f"Error embedding document {doc['id']}: {e}")
    
    is_initialized = True
    print(f"Knowledge base initialized with {len(cached_kb_documents)} documents")

def get_all_kb_documents():
    """Get all KB documents with embeddings"""
    if len(cached_kb_documents) == 0:
        print("KB not initialized, initializing now...")
        initialize_knowledge_base()
    return cached_kb_documents

def embed_query(query: str):
    """Embed a query for RAG retrieval"""
    return generate_embedding(query)