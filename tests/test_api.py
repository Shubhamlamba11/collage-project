import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.memory import memory_store

client = TestClient(app)

def setup_function():
    memory_store.clear()

def test_system_status_endpoint():
    response = client.get("/api/system/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "system_info" in data

def test_chat_endpoint_fallback():
    response = client.post("/api/chat", json={"message": "What is the time?"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Current date and time:" in data["response"]
    assert "latency_ms" in data

def test_math_endpoint():
    response = client.post("/api/math", json={"expression": "10 + 25"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Result: 35" in data["result"]

def test_history_endpoints():
    client.post("/api/chat", json={"message": "Hello"})

    # Get history
    hist_resp = client.get("/api/history")
    assert hist_resp.status_code == 200
    history = hist_resp.json()["history"]
    assert len(history) >= 2

    # Clear history
    del_resp = client.delete("/api/history")
    assert del_resp.status_code == 200

    hist_resp_empty = client.get("/api/history")
    assert len(hist_resp_empty.json()["history"]) == 0

def test_config_endpoint():
    response = client.post("/api/config", json={"gemini_api_key": "test_key_123"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
