from groq_client import cosine_similarity
from config import Config
from rag.embed import get_all_kb_documents, embed_query

def retrieve_relevant_docs(query: str, top_k: int = None):
    """Retrieve relevant knowledge base documents for a query"""
    if top_k is None:
        top_k = Config.RAG_TOP_K
    
    # Get query embedding
    query_embedding = embed_query(query)
    
    # Get all KB documents
    kb_docs = get_all_kb_documents()
    
    # Calculate similarity scores
    results = []
    
    for doc in kb_docs:
        if not doc.embedding:
            print(f"Document {doc.id} has no embedding, skipping")
            continue
        
        score = cosine_similarity(query_embedding, doc.embedding)
        
        # Only include if above threshold
        if score >= Config.RAG_SIMILARITY_THRESHOLD:
            # Create snippet
            snippet = doc.content[:500] + "..."
            
            results.append({
                'document': doc,
                'score': score,
                'snippet': snippet
            })
    
    # Sort by score descending and take top K
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

def build_rag_context(results):
    """Build RAG context string from retrieved documents"""
    if len(results) == 0:
        return "No relevant knowledge base documents found."
    
    context = "=== RELEVANT KNOWLEDGE BASE CONTEXT ===\n\n"
    
    for result in results:
        doc = result['document']
        score = result['score']
        context += f"## {doc.title} (Relevance: {score * 100:.1f}%)\n"
        context += f"Tags: {', '.join(doc.tags)}\n\n"
        context += f"{doc.content}\n\n"
        context += "---\n\n"
    
    return context