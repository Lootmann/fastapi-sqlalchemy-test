from random import randint, sample
from string import ascii_letters, digits, punctuation

from src.schemas import auth as auth_schema
from src.schemas import user as user_schema
from tests.init_client import test_client as client


def random_string(min_: int = 5, max_: int = 20) -> str:
    """random_string
    generate complete a meaningless random string

    Args:
        min_(int): min length
        max_(int): max length
    """
    s = ascii_letters + digits + punctuation
    return "".join(sample(s, randint(min_, max_)))


def login_and_create_token(client, username: str, password: str) -> auth_schema.Token:
    token_resp = client.post(
        "/token",
        data={"username": username, "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = auth_schema.Token(**token_resp.json())
    return {"Authorization": "Bearer {}".format(token.access_token)}
