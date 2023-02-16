from fastapi import status

from tests.init_client import test_client as client


class TestCreatePost:
    def test_root(self, client):
        resp = client.get("/ping")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["ping"] == "pong :^)"
