import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_summarize_empty_text():
    response = client.post("/api/summarize", json={"text": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Text cannot be empty."}

def test_summarize_whitespace_text():
    response = client.post("/api/summarize", json={"text": "   "})
    assert response.status_code == 400
    assert response.json() == {"detail": "Text cannot be empty."}

@patch("app.main.client")
def test_summarize_success(mock_client):
    # Mock the Gemini response
    mock_response = MagicMock()
    mock_response.text = "This is a mocked summary."
    mock_client.models.generate_content.return_value = mock_response
    
    response = client.post("/api/summarize", json={"text": "This is a long text to be summarized."})
    assert response.status_code == 200
    assert response.json() == {"summary": "This is a mocked summary."}

@patch("app.main.client", None)
def test_summarize_missing_api_key():
    # Ensure it fails correctly if client is None
    response = client.post("/api/summarize", json={"text": "Some text"})
    assert response.status_code == 500
    assert "Gemini API key is not configured" in response.json()["detail"]
