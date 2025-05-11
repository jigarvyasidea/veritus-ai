# Veritus.ai RAG Chatbot

A RAG-based chatbot for Veritus.ai using free Hugging Face models.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Features

- Document embedding using sentence-transformers/all-MiniLM-L6-v2
- Vector storage using FAISS
- Text generation using Mistral-7B-Instruct
- Web scraping for knowledge base
- FastAPI backend
- React frontend with Tailwind CSS

## Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/              # ML models and embeddings
│   ├── utils/               # Utility functions
│   └── data/                # Data storage
├── frontend/                # React frontend
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configuration

Create a `.env` file in the root directory with the following variables:
```
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## Usage

1. Start the backend server
2. Navigate to the frontend interface
3. Ask questions about Veritus.ai
4. View responses with source attribution "# veritus-ai" 
