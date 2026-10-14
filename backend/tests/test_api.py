from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_generate_requires_question():
    response = client.post("/generate", json={"question": ""})
    assert response.status_code == 422
