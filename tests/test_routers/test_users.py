from fastapi import status
from tests.init_client import test_client as client
from src.schemas import user as user_schema
from tests.util import random_string


def test_create_user(client):
    username = random_string()
    resp = client.post("/users", json={"name": username})
    assert resp.status_code == status.HTTP_200_OK

    resp_obj = resp.json()
    assert "id" in resp_obj
    assert "name" in resp_obj
    assert "posts" not in resp_obj
    assert "comments" not in resp_obj

    user = user_schema.User(**resp_obj)
    assert user.name == username


def test_get_all_users(client):
    for _ in range(10):
        client.post("/users", json={"name": random_string()})

    resp = client.get("/users")
    assert resp.status_code == status.HTTP_200_OK

    resp_obj = resp.json()
    assert len(resp_obj) == 10


class TestUpdate:
    def test_update_user(self, client):
        username = random_string()
        resp = client.post("/users", json={"name": username})
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["name"] == username

        resp = client.put(f"/users/{resp_obj['id']}", json={"name": "updated"})
        assert resp.status_code == status.HTTP_200_OK

        updated_user = user_schema.User(**resp.json())
        assert updated_user.id == resp_obj["id"]
        assert updated_user.name == "updated"
        assert updated_user.name != username

    def test_update_user_which_doesnot_exists(self, client):
        resp = client.put(f"/users/1", json={"name": "updated"})
        assert resp.status_code == status.HTTP_404_NOT_FOUND
