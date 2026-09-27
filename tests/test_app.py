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

@patch("app.main.genai.GenerativeModel.generate_content")
def test_summarize_success(mock_generate):
    # Mock the Gemini response
    mock_response = MagicMock()
    mock_response.text = "This is a mocked summary."
    mock_generate.return_value = mock_response
    
    # Needs to pretend we have an API key for this test to pass the internal check
    with patch("app.main.GEMINI_API_KEY", "dummy_key"):
        response = client.post("/api/summarize", json={"text": "This is a long text to be summarized."})
        assert response.status_code == 200
        assert response.json() == {"summary": "This is a mocked summary."}

@patch("app.main.genai.GenerativeModel.generate_content")
def test_summarize_missing_api_key(mock_generate):
    # Ensure it fails correctly if no API key is present
    with patch("app.main.GEMINI_API_KEY", None):
        response = client.post("/api/summarize", json={"text": "Some text"})
        assert response.status_code == 500
        assert "Gemini API key is not configured" in response.json()["detail"]
