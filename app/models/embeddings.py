import google.generativeai as genai
import numpy as np
from typing import List, Tuple
import logging

# Configure Google AI
GOOGLE_API_KEY = "AIzaSyDpSKlHmJilM9Mjv4lUFw-78eXfepkiGCY"
genai.configure(api_key=GOOGLE_API_KEY)

logger = logging.getLogger(__name__)

class EmbeddingModel:
    def __init__(self):
        self.model = genai.GenerativeModel('embedding-001')
        self.embeddings = []
        self.metadata = []

    def add_documents(self, texts: List[str], metadata: List[dict] = None):
        """Add documents to the vector store"""
        try:
            # Get embeddings from Google AI
            for text in texts:
                embedding = self.model.embed_content(text)['embedding']
                self.embeddings.append(embedding)
            
            # Store metadata if provided
            if metadata:
                self.metadata.extend(metadata)
            else:
                self.metadata.extend([{"text": text} for text in texts])
        except Exception as e:
            logger.error(f"Error in add_documents: {str(e)}")

    def search(self, query: str, k: int = 5) -> List[Tuple[float, dict]]:
        """Search for similar documents"""
        try:
            if not self.embeddings:
                return []

            # Get query embedding
            query_embedding = np.array(self.model.embed_content(query)['embedding'])
            
            # Calculate cosine similarity
            similarities = []
            for embedding in self.embeddings:
                similarity = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
                similarities.append(similarity)
            
            # Get top k results
            top_k_indices = np.argsort(similarities)[-k:][::-1]
            results = [(float(similarities[i]), self.metadata[i]) for i in top_k_indices]
            
            return results
        except Exception as e:
            logger.error(f"Error in search: {str(e)}")
            return [] 