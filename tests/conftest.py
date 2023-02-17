import pytest

from src.schemas import post as post_schema
from src.schemas import user as user_schema
from tests.init_client import test_client as client
from tests.util import random_string


@pytest.fixture
def user_fixture(client):
    resp = client.post("/users", json={"name": random_string(), "password": random_string()})
    return user_schema.UserCreateResponse(**resp.json())


@pytest.fixture
def post_fixture(client):
    resp = client.post(
        "/users",
        json={
            "name": random_string(),
            "password": random_string(),
        },
    )
    user = user_schema.UserCreateResponse(**resp.json())

    resp = client.post(
        "/posts",
        json={
            "title": random_string(),
            "content": random_string(),
            "user_id": user.id,
        },
    )
    return post_schema.PostCreateResponse(**resp.json())
