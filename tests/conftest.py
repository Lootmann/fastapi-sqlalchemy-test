import pytest

from src.schemas import auth as auth_schema
from src.schemas import post as post_schema
from src.schemas import user as user_schema
from tests.init_client import test_client as client
from tests.util import random_string


@pytest.fixture
def user_fixture(client):
    username = random_string()
    password = random_string()
    resp = client.post("/users", json={"name": username, "password": password})

    token_resp = client.post(
        "/token",
        data={"username": username, "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token_json = token_resp.json()
    token = auth_schema.Token(**token_json)

    return user_schema.UserCreateResponse(**resp.json())


@pytest.fixture
def post_fixture(client):
    username = random_string()
    password = random_string()
    resp = client.post(
        "/users",
        json={"name": username, "password": password},
    )
    user = user_schema.UserCreateResponse(**resp.json())

    login_resp = client.post(
        "/token",
        data={"username": username, "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    resp = client.post(
        "/posts",
        json={
            "title": random_string(),
            "content": random_string(),
            "user_id": user.id,
        },
    )
    return post_schema.PostCreateResponse(**resp.json())
