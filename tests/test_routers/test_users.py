import pytest
from fastapi import status

from src.schemas import post as post_schema
from src.schemas import user as user_schema
from tests.init_client import test_client as client
from tests.util import random_string


def test_create_user(client):
    username = random_string()
    resp = client.post("/users", json={"name": username})
    assert resp.status_code == status.HTTP_200_OK

    resp_obj = resp.json()
    assert "id" in resp_obj
    assert "name" in resp_obj
    assert "posts" not in resp_obj
    assert "comments" not in resp_obj

    user = user_schema.User(**resp_obj)
    assert user.name == username


class TestGetUser:
    def test_get_all_users(self, client):
        for _ in range(10):
            client.post("/users", json={"name": random_string()})

        resp = client.get("/users")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 10

    def test_get_user(self, client):
        username = random_string()
        resp = client.post("/users", json={"name": username})
        assert resp.status_code == status.HTTP_200_OK

        user_data = user_schema.User(**resp.json())
        resp = client.get(f"/users/{user_data.id}")
        assert resp.status_code == status.HTTP_200_OK

        user = user_schema.User(**resp.json())
        assert user.name == username
        assert user.posts == []
        assert user.comments == []

    def test_get_user_which_doesnt_exist(self, client):
        resp = client.get(f"/users/123")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestGetPostByUser:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        self.username = random_string()
        resp = client.post("/users", json={"name": self.username})
        self.user = user_schema.UserCreateResponse(**resp.json())

    def test_get_all_posts_by_user_id(self, client):
        # create post
        post_data = {"title": random_string(), "content": random_string(), "user_id": self.user.id}
        client.post("/posts", json=post_data)
        client.post("/posts", json=post_data)
        client.post("/posts", json=post_data)

        # get user, user has posts
        resp = client.get(f"/users/{self.user.id}/posts")
        posts = resp.json()
        assert len(posts) == 3

        # this resp is same as above ...
        resp = client.get(f"/users/{self.user.id}")
        posts = resp.json()["posts"]
        assert len(posts) == 3

    def test_get_post_by_user_id_and_post_id(self, client):
        post_data = {"title": random_string(), "content": random_string(), "user_id": self.user.id}
        resp = client.post("/posts", json=post_data)
        post_id = resp.json()["id"]

        resp = client.get(f"/users/{self.user.id}/posts/{post_id}")
        assert resp.status_code == status.HTTP_200_OK

        # wrong post_id
        resp = client.get(f"/users/{self.user.id}/posts/{post_id + 1}")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        # wrong user_id
        resp = client.get(f"/users/{self.user.id+ 1}/posts/{post_id}")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestGetCommentByUser:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        self.username = random_string()
        resp = client.post("/users", json={"name": self.username})
        self.user = user_schema.UserCreateResponse(**resp.json())

    def test_get_comments_by_user_id(self, client):
        resp = client.get(f"/users/{self.user.id}/comments")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 0

        post_data = {"title": random_string(), "content": random_string(), "user_id": self.user.id}
        resp = client.post("/posts", json=post_data)
        post_id = resp.json()["id"]

        comment_data = {"comment": random_string(), "user_id": self.user.id, "post_id": post_id}
        client.post("/comments", json=comment_data)
        comment_data = {"comment": random_string(), "user_id": self.user.id, "post_id": post_id}
        client.post("/comments", json=comment_data)
        comment_data = {"comment": random_string(), "user_id": self.user.id, "post_id": post_id}
        client.post("/comments", json=comment_data)

        resp = client.get(f"/users/{self.user.id}/comments")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 3

    def test_get_comments_which_doesnt_exist_user(self, client):
        resp = client.get("/users/123/comments")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_get_comment_by_user_id(self, client):
        post_data = {"title": random_string(), "content": random_string(), "user_id": self.user.id}
        resp = client.post("/posts", json=post_data)
        post_id = resp.json()["id"]

        comment_data = {"comment": "now testing...", "user_id": self.user.id, "post_id": post_id}
        resp = client.post("/comments", json=comment_data)
        comment_id = resp.json()["id"]

        resp = client.get(f"/users/{self.user.id}/comments/{comment_id}")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["comment"] == "now testing..."

        # wrong comment_id
        resp = client.get(f"/users/{self.user.id}/comments/{comment_id + 1}")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        # wrong user_id
        resp = client.get(f"/users/{self.user.id + 1}/comments/{comment_id}")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateUser:
    def test_update_user(self, client):
        username = random_string()
        resp = client.post("/users", json={"name": username})
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert resp_obj["name"] == username

        resp = client.put(f"/users/{resp_obj['id']}", json={"name": "updated"})
        assert resp.status_code == status.HTTP_201_CREATED

        updated_user = user_schema.User(**resp.json())
        assert updated_user.id == resp_obj["id"]
        assert updated_user.name == "updated"
        assert updated_user.name != username

    def test_update_user_which_doesnt_exists(self, client):
        resp = client.put(f"/users/1", json={"name": "updated"})
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteUser:
    def test_delete(self, client):
        create_resp = client.post("/users", json={"name": random_string()})
        assert create_resp.status_code == status.HTTP_200_OK

        resp = client.get("/users")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        user = user_schema.User(**create_resp.json())
        resp = client.delete(f"/users/{user.id}")
        assert resp.status_code == status.HTTP_200_OK

        resp = client.get("/users")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

    def test_delete_which_user_doesnt_exist(self, client):
        resp = client.delete("/users/1")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
