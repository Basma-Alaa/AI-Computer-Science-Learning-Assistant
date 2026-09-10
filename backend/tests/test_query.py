from fastapi.testclient import TestClient
from app.main import app  # Correct import path to backend/app/main.py

client = TestClient(app)

def test_query_happy_path():
    response = client.post(
        "/query",
        json={"question": "What is machine learning?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data

def test_query_invalid_input():
    response = client.post(
        "/query",
        json={}
    )
    assert response.status_code == 422