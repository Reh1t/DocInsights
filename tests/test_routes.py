import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_root_get():
    response = client.get("/")
    assert response.status_code == 200
    assert "Chatbot API is running" in response.text


def test_upload_without_file():
    response = client.post("/upload/", data={"task": "Test"})
    assert response.status_code == 422  # No files provided

def test_chat_invalid_session():
    response = client.post("/chat/", json={"session_id": "abc", "message": "Hi"})
    assert response.status_code == 200
    assert "Error:" in response.json()["response"]
