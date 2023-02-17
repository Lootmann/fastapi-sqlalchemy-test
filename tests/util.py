from random import randint, sample
from string import ascii_letters, digits, punctuation

from src.schemas import user as user_schema


def random_string(min_: int = 5, max_: int = 20) -> str:
    """random_string
    generate complete a meaningless random string

    Args:
        min_(int): min length
        max_(int): max length
    """
    s = ascii_letters + digits + punctuation
    return "".join(sample(s, randint(min_, max_)))


def random_user_json() -> dict:
    return {"name": random_string(), "password": random_string()}
