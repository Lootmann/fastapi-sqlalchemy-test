from tests.init_client import test_client as client

from src.models import user as user_model


def test_user_model():
    user_json = {"id": 1, "name": "James bar"}
    model = user_model.User(**user_json)
    assert str(model) == "<User (id, name, posts) 1,James bar,[]>"
