from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import logging

from app.models.embeddings import EmbeddingModel
from app.models.llm import LLMModel
from app.utils.scraper import WebScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="Veritus.ai RAG Chatbot")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
embedding_model = EmbeddingModel()
llm_model = LLMModel()

class Query(BaseModel):
    text: str

class Response(BaseModel):
    answer: str
    sources: List[str]

@app.on_event("startup")
async def startup_event():
    """Initialize the knowledge base on startup"""
    try:
        # Check if we already have an index
        if not os.path.exists("app/data/index.faiss"):
            logger.info("Building knowledge base...")
            scraper = WebScraper()
            documents = scraper.crawl_website()
            
            if documents:
                texts = [doc["text"] for doc in documents]
                metadata = [{"text": doc["text"], "source": doc["source"]} for doc in documents]
                embedding_model.add_documents(texts, metadata)
                embedding_model.save_index("app/data")
                logger.info(f"Knowledge base built with {len(documents)} documents")
            else:
                logger.warning("No documents were scraped from the website")
        else:
            logger.info("Loading existing knowledge base...")
            embedding_model.load_index("app/data")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to Veritus.ai RAG Chatbot API"}

@app.post("/query", response_model=Response)
async def process_query(query: Query):
    try:
        # Search for relevant documents
        results = embedding_model.search(query.text)
        
        if not results:
            return Response(
                answer="I don't have enough information to answer that question.",
                sources=[]
            )
        
        # Extract context from top results
        context = [result[1] for result in results[:3]]  # Use top 3 results
        
        # Generate response using LLM
        answer = llm_model.generate_response(query.text, context)
        
        # Extract unique sources
        sources = list(set(doc["source"] for doc in context))
        
        return Response(
            answer=answer,
            sources=sources
        )
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 