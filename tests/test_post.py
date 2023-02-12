from fastapi import status
from tests.init_client import test_client as client
from src.schemas import post as post_schema
from src.schemas import user as user_schema


class TestCreatePost:
    def test_get_all_posts(self, client):
        # create user
        resp = client.post("/users", json={"name": "hige"})
        user = user_schema.User(**resp.json())

        # get posts by user
        data = {"title": "hello", "content": "world"}
        client.post(f"/users/{user.id}/posts", json=data)
        client.post(f"/users/{user.id}/posts", json=data)
        client.post(f"/users/{user.id}/posts", json=data)

        resp = client.get("/users/1/posts")
        obj = resp.json()
        assert len(obj) == 3

    def test_create_post(self, client):
        # create user
        resp = client.post("/users", json={"name": "hoge"})
        user = user_schema.User(**resp.json())

        # create post
        data = {
            "title": "hello",
            "content": "world",
        }
        resp = client.post(f"/users/{user.id}/posts", json=data)
        assert resp.status_code == status.HTTP_200_OK

        post = post_schema.Post(**resp.json())
        assert post.id == 1
        assert post.title == data["title"]
        assert post.content == data["content"]
        assert post.user_id == user.id

    def test_create_post_no_exists_user_id(self, client):
        # create post
        data = {
            "title": "hello",
            "content": "world",
        }
        resp = client.post(f"/users/{123}/posts", json=data)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestGetpost:
    def test_get_no_posts(self, client):
        # create user
        resp = client.post("/users", json={"name": "hige"})
        user_schema.User(**resp.json())

        resp = client.get("/users/1/posts")
        assert resp.status_code == status.HTTP_200_OK
        obj = resp.json()
        assert len(obj) == 0
        assert obj == []

    def test_get_post_by_user(self, client):
        # create user
        resp = client.post("/users", json={"name": "hige"})
        user = user_schema.User(**resp.json())

        # create post
        data = {
            "title": "hello",
            "content": "world",
        }
        resp = client.post(f"/users/{user.id}/posts", json=data)
        post = post_schema.Post(**resp.json())
        assert resp.status_code == status.HTTP_200_OK

        # get post by user_id and post_id
        resp = client.get(f"/users/{user.id}")
        print(resp.json())

        print(user)
        print(post)
