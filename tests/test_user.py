from fastapi import status
from tests.init_client import test_client as client
from src.schemas.user import User as user_schema


def test_create(client):
    data = {"name": "testmann"}
    resp = client.post("/users", json=data)
    assert resp.status_code == status.HTTP_200_OK

    obj = resp.json()
    assert obj["id"] == 1
    assert obj["name"] == "testmann"


def test_get_all_users(client):
    data = [
        {"id": 1, "name": "hoge", "posts": []},
        {"id": 2, "name": "hage", "posts": []},
        {"id": 3, "name": "hige", "posts": []},
    ]
    client.post("/users", json=data[0])
    client.post("/users", json=data[1])
    client.post("/users", json=data[2])

    resp = client.get("/users")
    assert resp.status_code == status.HTTP_200_OK

    obj = resp.json()
    assert len(obj) == 3
    assert data[0] in obj
    assert data[1] in obj
    assert data[2] in obj
    assert {"name": "moge", "id": 123} not in obj


def test_get_one_user(client):
    data = {"name": "testmann"}
    resp = client.post("/users", json=data)
    assert resp.status_code == status.HTTP_200_OK

    user = user_schema(**resp.json())

    resp = client.get(f"/users/{user.id}")
    assert resp.status_code == status.HTTP_200_OK

    obj = resp.json()
    assert obj["id"] == user.id
    assert obj["name"] == user.name


def test_fail_to_get_user(client):
    resp = client.get("/users")
    assert len(resp.json()) == 0

    resp = client.get("/users/12345")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
