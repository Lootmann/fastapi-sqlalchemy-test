import pytest

from src.schemas import auth as auth_schema
from src.schemas import post as post_schema
from src.schemas import user as user_schema
from tests.init_client import test_client as client
from tests.util import login_and_create_token, random_string


@pytest.fixture
def user_fixture(client) -> tuple:
    username = random_string()
    password = random_string()

    resp = client.post("/users", json={"name": username, "password": password})
    headers = login_and_create_token(client, username, password)

    # FIXME: HOW beautify is
    return (user_schema.UserCreateResponse(**resp.json()), headers)


@pytest.fixture
def post_fixture(client):
    # create user
    username, password = random_string(), random_string()

    client.post(
        "/users",
        json={"name": username, "password": password},
    )

    # create token
    headers = login_and_create_token(client, username, password)
    resp = client.post(
        "/posts",
        json={
            "title": random_string(),
            "content": random_string(),
        },
        headers=headers,
    )

    # FIXME: HOW beautify is
    return post_schema.PostCreateResponse(**resp.json()), headers
