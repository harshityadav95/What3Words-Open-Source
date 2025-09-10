from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_convert_coords():
    response = client.post("/convert-coords", json={"latitude": 51.5074, "longitude": -0.1278})
    assert response.status_code == 200
    data = response.json()
    assert "word1" in data
    assert "word2" in data
    assert "word3" in data

def test_convert_words():
    # First get some words
    response = client.post("/convert-coords", json={"latitude": 51.5074, "longitude": -0.1278})
    words = response.json()
    
    # Then convert back
    response = client.post("/convert-words", json={
        "word1": words["word1"],
        "word2": words["word2"],
        "word3": words["word3"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "latitude" in data
    assert "longitude" in data

def test_invalid_coords():
    response = client.post("/convert-coords", json={"latitude": 100, "longitude": -0.1278})
    assert response.status_code == 400

def test_invalid_words():
    response = client.post("/convert-words", json={"word1": "invalid", "word2": "words", "word3": "here"})
    assert response.status_code == 400