import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def auth_farm():
    client.post("/api/auth/register", json={
        "email": "carbon@example.com",
        "username": "carbonuser",
        "password": "testpass123",
        "full_name": "Carbon Test",
        "role": "farmer",
    })
    login = client.post("/api/auth/login", json={
        "username": "carbonuser",
        "password": "testpass123",
    }).json()
    token = login["access_token"]

    farm = client.post("/api/farms", json={
        "name": "Carbon Farm",
        "country": "Kenya",
        "latitude": -1.2921,
        "longitude": 36.8219,
        "area_hectares": 5.0,
        "crop_types": "maize, beans",
        "sustainability_practices": "cover cropping, agroforestry",
    }, headers={"Authorization": f"Bearer {token}"}).json()

    return token, farm["id"]


def test_estimate_carbon(auth_farm):
    token, farm_id = auth_farm
    response = client.post("/api/carbon/estimate", json={
        "farm_id": farm_id,
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["carbon_offset_tonnes"] > 0
    assert data["sustainability_score"] is not None


def test_get_carbon_scores(auth_farm):
    token, farm_id = auth_farm
    client.post("/api/carbon/estimate", json={"farm_id": farm_id}, headers={"Authorization": f"Bearer {token}"})

    response = client.get(f"/api/carbon/farms/{farm_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_total_carbon(auth_farm):
    token, _ = auth_farm
    response = client.get("/api/carbon/total", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "total_carbon_tonnes" in response.json()
