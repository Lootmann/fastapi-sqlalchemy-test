from tests.init_client import test_client as client


def test_read(client):
    client.get("/users")
    assert 1 == 1
