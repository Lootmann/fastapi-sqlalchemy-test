import pytest
from fastapi import status
from tests.init_client import test_client as client
from src.schemas import user as user_schema
from src.schemas import post as post_schema
from src.schemas import comment as comment_schema
from tests.util import random_string


class TestGetComment:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        self.username = random_string()
        resp = client.post("/users", json={"name": self.username})
        self.user_id = resp.json()["id"]

        self.title = random_string()
        self.content = random_string()
        post_data = {"title": self.title, "content": self.content, "user_id": self.user_id}
        resp = client.post("/posts", json=post_data)
        self.post_id = resp.json()["id"]

    def test_get_all_comments(self, client):
        resp = client.get("/comments")
        assert resp.status_code == status.HTTP_200_OK

        assert len(resp.json()) == 0

        comment_data = {
            "comment": "new comment",
            "user_id": self.user_id,
            "post_id": self.post_id,
        }
        resp = client.post(f"/comments/", json=comment_data)

        resp = client.get("/comments")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

    def test_get_one_comment(self, client):
        resp = client.get("/comments/12")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestPostComment:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        # create user
        self.username = random_string()
        resp = client.post("/users", json={"name": self.username})
        self.user_id = resp.json()["id"]

        # create post
        self.title = random_string()
        self.content = random_string()
        post_data = {"title": self.title, "content": self.content, "user_id": self.user_id}
        resp = client.post("/posts", json=post_data)
        self.post_id = resp.json()["id"]

    def test_create_post(self, client):
        # get comments
        resp = client.get("/comments")
        assert len(resp.json()) == 0

        # create comment
        comment_data = {
            "comment": "this is a comment",
            "user_id": self.user_id,
            "post_id": self.post_id,
        }
        resp = client.post("/comments", json=comment_data)
        assert resp.status_code == status.HTTP_201_CREATED

        created_comment = resp.json()
        assert created_comment["comment"] == "this is a comment"
        assert created_comment["user_id"] == self.user_id
        assert created_comment["post_id"] == self.post_id

        # get comments
        resp = client.get("/comments")
        assert len(resp.json()) == 1

        resp = client.get(f"/posts/{self.post_id}")
        post = post_schema.Post(**resp.json())
        assert post.id == self.post_id
        assert len(post.comments) == 1

        assert created_comment["comment"] == post.comments[0].comment
        assert created_comment["user_id"] == post.comments[0].user_id
        assert created_comment["post_id"] == post.comments[0].post_id
