import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def auth_token():
    client.post("/api/auth/register", json={
        "email": "farm@example.com",
        "username": "farmuser",
        "password": "testpass123",
        "full_name": "Farm Test",
        "role": "farmer",
    })
    resp = client.post("/api/auth/login", json={
        "username": "farmuser",
        "password": "testpass123",
    })
    return resp.json()["access_token"]


def test_create_farm(auth_token):
    response = client.post("/api/farms", json={
        "name": "Test Farm",
        "country": "Kenya",
        "latitude": -1.2921,
        "longitude": 36.8219,
        "area_hectares": 5.0,
        "crop_types": "maize, beans",
        "irrigation_type": "drip",
        "fertilizer_usage": "organic",
        "soil_type": "loam",
        "sustainability_practices": "cover cropping, crop rotation",
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Farm"
    assert data["country"] == "Kenya"


def test_get_farms(auth_token):
    response = client.get("/api/farms", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = response.json()
    assert "farms" in data or isinstance(data, list)


def test_get_farm_by_id(auth_token):
    create = client.post("/api/farms", json={
        "name": "Specific Farm",
        "country": "Kenya",
        "latitude": -1.0,
        "longitude": 37.0,
        "area_hectares": 3.0,
    }, headers={"Authorization": f"Bearer {auth_token}"})
    farm_id = create.json()["id"]

    response = client.get(f"/api/farms/{farm_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Specific Farm"


def test_update_farm(auth_token):
    create = client.post("/api/farms", json={
        "name": "Update Test",
        "country": "Kenya",
        "latitude": -1.0,
        "longitude": 37.0,
        "area_hectares": 4.0,
    }, headers={"Authorization": f"Bearer {auth_token}"})
    farm_id = create.json()["id"]

    response = client.patch(f"/api/farms/{farm_id}", json={
        "name": "Updated Farm Name",
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Farm Name"
