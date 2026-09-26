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

    assert response.status_code == 201


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

def test_pagination(client):
    response = client.get("/scores?page=1&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 2
    assert len(data["items"]) <= 2
def test_pagination_page_2(client):
    response = client.get("/scores?page=2&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["limit"] == 2
def test_min_rating(client):
    client.post(
        "/scores",
        json={
            "name": "LowPlayer",
            "rating": 500
        }
    )

    client.post(
        "/scores",
        json={
            "name": "HighPlayer",
            "rating": 1500
        }
    )

    response = client.get("/scores?min_rating=1000")

    assert response.status_code == 200

    for item in response.json()["items"]:
        assert item["rating"] >= 1000
def test_name_search(client):
    client.post(
        "/scores",
        json={
            "name": "SearchPlayer",
            "rating": 1000
        }
    )

    response = client.get("/scores?name=SearchPlayer")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) >= 1
    assert data["items"][0]["name"] == "SearchPlayer"
def test_sort_rating_desc(client):
    client.post(
        "/scores",
        json={
            "name": "PlayerA",
            "rating": 1000
        }
    )

    client.post(
        "/scores",
        json={
            "name": "PlayerB",
            "rating": 1500
        }
    )

    response = client.get(
        "/scores?sort=rating&order=desc"
    )

    assert response.status_code == 200

    items = response.json()["items"]

    ratings = [item["rating"] for item in items]

    assert ratings == sorted(ratings, reverse=True)
def test_sort_rating_asc(client):
    response = client.get(
        "/scores?sort=rating&order=asc"
    )

    assert response.status_code == 200

    items = response.json()["items"]

    ratings = [item["rating"] for item in items]

    assert ratings == sorted(ratings)