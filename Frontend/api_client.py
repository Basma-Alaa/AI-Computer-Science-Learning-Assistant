import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def query_rag_backend(question: str) -> dict:
    """Sends a user question to the FastAPI backend and returns the JSON response."""
    url = f"{API_BASE_URL}/query"
    payload = {"question": question}
    
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()  # Raises HTTPError if status code is not 200
    return response.json()