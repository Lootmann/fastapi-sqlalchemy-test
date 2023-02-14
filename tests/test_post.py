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

        post = post_schema.PostCreateResponse(**resp.json())
        assert post.id == 1
        assert post.title == "hello"
        assert post.content == "world"

    def test_create_post_no_exists_user_id(self, client):
        # create post
        data = {
            "title": "hello",
            "content": "world",
        }
        resp = client.post(f"/users/{123}/posts", json=data)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestGetPost:
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
            "title": "this is a title",
            "content": "what is content :^)",
        }
        resp = client.post(f"/users/{user.id}/posts", json=data)
        post_json = resp.json()

        assert post_json["id"] == 1
        assert post_json["title"] == "this is a title"
        assert post_json["content"] == "what is content :^)"

        # test user has a post
        resp = client.get(f"/users/{user.id}")
        user_obj = user_schema.User(**resp.json())

        assert user_obj.posts[0].id == post_json["id"]
        assert user_obj.posts[0].title == post_json["title"]
        assert user_obj.posts[0].content == post_json["content"]

    def test_get_post_by_post_id(self, client):
        # create user
        resp = client.post("/users", json={"name": "hage"})
        user = user_schema.User(**resp.json())

        # create post
        data = {
            "title": "tt",
            "content": "cc",
        }
        resp = client.post(f"/users/{user.id}/posts", json=data)
        post_json = resp.json()

        # get post by post_id
        resp = client.get(f"/posts/{post_json['id']}")
        assert resp.status_code == status.HTTP_200_OK

        post_obj = post_schema.Post(**resp.json())
        assert post_obj.user_id == user.id
        assert post_obj.title == data["title"]
        assert post_obj.content == post_json["content"]
