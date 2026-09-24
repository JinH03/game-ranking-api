from fastapi.testclient import TestClient
from main import app


def test_get_score(client):
    response = client.get("/scores")

    assert response.status_code == 200
    assert "items" in response.json()

def test_create_score(client):
    response = client.post(
        "/scores",
        json={
            "name": "TestPlayer",
            "rating": 1000
        }
    )

    assert response.status_code == 200


def test_update_score(client):
    client.post(
        "/scores",
        json={
            "name": "TestPlayer",
            "rating": 1000
        }
    )

    response = client.put(
        "/scores/TestPlayer",
        json={
            "rating": 1200
        }
    )

    assert response.status_code == 200
    assert response.json()["rating"] == 1200


def test_delete_score(client):
    client.post(
        "/scores",
        json={
            "name": "TestPlayer",
            "rating": 1000
        }
    )

    response = client.delete("/scores/TestPlayer")

    assert response.status_code == 200

def test_update_not_found(client):
    response = client.put(
        "/scores/NoSuchPlayer",
        json={
            "rating": 1200
        }
    )

    assert response.status_code == 404

def test_delete_not_found(client):
    response = client.delete("/scores/NoSuchPlayer")

    assert response.status_code == 404

def test_create_duplicate(client):
    client.post(
        "/scores",
        json={
            "name": "DuplicatePlayer",
            "rating": 1000
        }
    )

    response = client.post(
        "/scores",
        json={
            "name": "DuplicatePlayer",
            "rating": 1000
        }
    )

    assert response.status_code == 409

def test_create_invalid_rating(client):
    response = client.post(
        "/scores",
        json={
            "name": "InvalidPlayer",
            "rating": -1
        }
    )

    assert response.status_code == 422

def test_invalid_limit(client):
    response = client.get("/scores?limit=10")

    assert response.status_code == 422