import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user():
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User",
        "role": "farmer",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "password" not in data


def test_register_duplicate_email():
    client.post("/api/auth/register", json={
        "email": "dupe@example.com",
        "username": "dupe1",
        "password": "testpass123",
        "full_name": "Duplicate",
    })
    response = client.post("/api/auth/register", json={
        "email": "dupe@example.com",
        "username": "dupe2",
        "password": "testpass123",
        "full_name": "Duplicate",
    })
    assert response.status_code == 400


def test_login_success():
    client.post("/api/auth/register", json={
        "email": "login@example.com",
        "username": "loginuser",
        "password": "testpass123",
        "full_name": "Login Test",
    })
    response = client.post("/api/auth/login", json={
        "username": "loginuser",
        "password": "testpass123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid():
    response = client.post("/api/auth/login", json={
        "username": "nonexistent",
        "password": "wrongpass",
    })
    assert response.status_code == 401


def test_get_profile():
    client.post("/api/auth/register", json={
        "email": "profile@example.com",
        "username": "profileuser",
        "password": "testpass123",
        "full_name": "Profile Test",
    })
    login_resp = client.post("/api/auth/login", json={
        "username": "profileuser",
        "password": "testpass123",
    })
    token = login_resp.json()["access_token"]

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "profileuser"


def test_refresh_token():
    client.post("/api/auth/register", json={
        "email": "refresh@example.com",
        "username": "refreshuser",
        "password": "testpass123",
        "full_name": "Refresh Test",
    })
    login = client.post("/api/auth/login", json={
        "username": "refreshuser",
        "password": "testpass123",
    }).json()

    response = client.post("/api/auth/refresh", json={
        "refresh_token": login["refresh_token"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
