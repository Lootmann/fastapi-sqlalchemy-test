from fastapi import status
from tests.init_client import test_client as client
from src.schemas import post as post_schema
from src.schemas import user as user_schema


class TestGetPost:
    def test_get_all_posts(self, client):
        resp = client.get("/posts")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 0


class TestPostPost:
    def test_create_post(self, client):
        resp = client.post("/users", json={"name": "foobar"})
        user = user_schema.User(**resp.json())
        resp = client.post("/posts", json={"user_id": user.id, "title": "hoge", "content": "hage"})
        assert resp.status_code == status.HTTP_201_CREATED

        post = post_schema.PostCreateResponse(**resp.json())
        assert post.title == "hoge"
        assert post.content == "hage"

        resp = client.get(f"/users/{user.id}")
        user = user_schema.User(**resp.json())
        assert user.posts != []

        assert user.posts[0].title == post.title
        assert user.posts[0].content == post.content

    def test_create_post_without_userid(self, client):
        resp = client.post("/posts", json={"title": "hoge", "content": "hage"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_post_raise_user_not_found(self, client):
        resp = client.post("/posts", json={"user_id": 1234, "title": "hoge", "content": "hage"})
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_create_post_without_field(self, client):
        resp = client.post("/users", json={"name": "James Foo"})
        user = user_schema.User(**resp.json())

        resp = client.post("/posts", json={"user_id": user.id, "title": "hoge"})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.post("/posts", json={"user_id": user.id, "content": "hoge"})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.post("/posts", json={"user_id": user.id})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.get("/posts")
        resp_json = resp.json()
        assert len(resp_json) == 3
