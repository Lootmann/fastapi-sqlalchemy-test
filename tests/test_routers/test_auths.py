from fastapi import status

from src.schemas import user as user_schema
from tests.init_client import test_client as client
from tests.util import random_string


def test_login(client):
    # create user
    username = random_string()
    password = random_string()

    resp = client.post("/users", json={"name": username, "password": password})
    user = user_schema.UserCreateResponse(**resp.json())

    # login
    login_resp = client.post(
        "/token",
        data={"username": username, "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert login_resp.status_code == status.HTTP_200_OK

    resp_json = login_resp.json()

    assert "access_token" in resp_json
    assert "token_type" in resp_json
    assert resp_json["token_type"] == "bearer"

    # POST /posts required login
    resp = client.post(
        "/posts",
        json={"title": "hoge", "content": "hage", "user_id": user.id},
        headers={"Authorization": "Bearer {}".format(resp_json["access_token"])},
    )
    assert resp.status_code == status.HTTP_201_CREATED

    # test get post
    resp = client.get(f"/users/{user.id}")
    assert resp.status_code == status.HTTP_200_OK

    user = user_schema.User(**resp.json())
    assert user.name == username
    assert len(user.posts) == 1
    assert user.posts[0].title == "hoge"
    assert user.posts[0].content == "hage"
