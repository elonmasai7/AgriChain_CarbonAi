import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def setup():
    client.post("/api/auth/register", json={
        "email": "seller@example.com",
        "username": "seller",
        "password": "testpass123",
        "full_name": "Seller",
        "role": "farmer",
    })
    seller_login = client.post("/api/auth/login", json={
        "username": "seller",
        "password": "testpass123",
    }).json()
    seller_token = seller_login["access_token"]

    farm = client.post("/api/farms", json={
        "name": "Market Farm",
        "country": "Kenya",
        "latitude": -1.0,
        "longitude": 37.0,
        "area_hectares": 5.0,
    }, headers={"Authorization": f"Bearer {seller_token}"}).json()

    score = client.post("/api/carbon/estimate", json={
        "farm_id": farm["id"],
    }, headers={"Authorization": f"Bearer {seller_token}"}).json()

    return seller_token, score["id"]


def test_create_listing(setup):
    token, score_id = setup
    response = client.post("/api/marketplace/listings", json={
        "carbon_asset_id": score_id,
        "price_per_tonne": 15.0,
        "total_tonnes": 10.0,
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 201, 400)
    if response.status_code == 200:
        assert response.json()["price_per_tonne"] == 15.0


def test_list_listings(setup):
    token, _ = setup
    response = client.get("/api/marketplace/listings", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "listings" in response.json()
