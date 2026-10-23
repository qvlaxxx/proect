from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "bio": "Привіт"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_skill():
    user = client.post("/users/", json={
        "username": "skilluser",
        "email": "skill@example.com"
    }).json()

    response = client.post("/skills/", json={
        "title": "Python",
        "description": "Основи Python програмування",
        "category": "programming",
        "level": "beginner",
        "can_teach": True,
        "want_learn": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Python"