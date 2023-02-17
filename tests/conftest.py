import pytest

from src.schemas import auth as auth_schema
from src.schemas import post as post_schema
from src.schemas import user as user_schema
from tests.init_client import test_client as client
from tests.util import random_string


def login_and_create_token(client, username: str, password: str) -> auth_schema.Token:
    token_resp = client.post(
        "/token",
        data={"username": username, "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = auth_schema.Token(**token_resp.json())
    return {"Authorization": "Bearer {}".format(token.access_token)}


@pytest.fixture
def user_fixture(client) -> tuple:
    username = random_string()
    password = random_string()

    resp = client.post("/users", json={"name": username, "password": password})
    headers = login_and_create_token(client, username, password)

    return (user_schema.UserCreateResponse(**resp.json()), headers)


@pytest.fixture
def post_fixture(client):
    username = random_string()
    password = random_string()

    resp = client.post(
        "/users",
        json={"name": username, "password": password},
    )
    user = user_schema.UserCreateResponse(**resp.json())

    headers = login_and_create_token(client, username, password)
    resp = client.post(
        "/posts",
        json={
            "title": random_string(),
            "content": random_string(),
            "user_id": user.id,
        },
        headers=headers,
    )

    return post_schema.PostCreateResponse(**resp.json()), headers
