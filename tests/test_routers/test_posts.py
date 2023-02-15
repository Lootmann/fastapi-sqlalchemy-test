import pytest
from fastapi import status
from tests.init_client import test_client as client
from src.schemas import post as post_schema
from src.schemas import user as user_schema
from tests.util import random_string


@pytest.fixture(autouse=True, scope="function")
def initial(client):
    """
    create user and post and return these params
    """
    username = random_string()
    resp = client.post("/users", json={"name": username})
    resp_obj = resp.json()
    user_id = resp_obj["id"]

    return {
        "username": username,
        "user_id": user_id,
        "user": resp_obj,
    }


class TestGetPost:
    def test_get_all_posts(self, client):
        resp = client.get("/posts")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 0

    def test_get_one_post(self, client, initial):
        post_data = {"title": "new post", "content": "nah", "user_id": initial["user_id"]}
        resp = client.post("/posts", json=post_data)
        assert resp.status_code == status.HTTP_201_CREATED

        post_resp = post_schema.PostCreateResponse(**resp.json())
        resp = client.get(f"/posts/{post_resp.id}")
        assert resp.status_code == status.HTTP_200_OK

        post = post_schema.Post(**resp.json())
        assert post.id == post_resp.id
        assert post.title == post_resp.title
        assert post.content == post_resp.content
        assert post.comments == []

    def test_get_one_post_raise_error(self, client, initial):
        post_data = {"title": "new post", "content": "nah", "user_id": initial["user_id"]}
        resp = client.post("/posts", json=post_data)
        post = post_schema.PostCreateResponse(**resp.json())

        # does not exit post id
        resp = client.get(f"/posts/{post.id + 1}")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        # wrong post id type
        resp = client.get(f"/posts/hoge")
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestPostPost:
    def test_create_post(self, client, initial):
        resp = client.post(
            "/posts", json={"user_id": initial["user_id"], "title": "hoge", "content": "hage"}
        )
        assert resp.status_code == status.HTTP_201_CREATED

        post = post_schema.PostCreateResponse(**resp.json())
        assert post.title == "hoge"
        assert post.content == "hage"

        resp = client.get(f"/users/{initial['user_id']}")
        user = user_schema.User(**resp.json())
        assert user.posts != []

        assert user.posts[0].title == post.title
        assert user.posts[0].content == post.content

    def test_create_post_without_userid(self, client, initial):
        resp = client.post("/posts", json={"title": "hoge", "content": "hage"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_post_raise_user_not_found(self, client, initial):
        resp = client.post("/posts", json={"user_id": 1234, "title": "hoge", "content": "hage"})
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_create_post_without_field(self, client, initial):
        resp = client.post("/posts", json={"user_id": initial["user_id"], "title": "hoge"})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.post("/posts", json={"user_id": initial["user_id"], "content": "hoge"})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.post("/posts", json={"user_id": initial["user_id"]})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.get("/posts")
        resp_json = resp.json()
        assert len(resp_json) == 3


class TestPatchPost:
    @pytest.fixture(autouse=True)
    def initial(self, client):
        self.username = random_string()
        resp = client.post("/users", json={"name": self.username})
        self.user = user_schema.User(**resp.json())

        self.title = random_string()
        self.content = random_string()

        post_data = {"user_id": self.user.id, "title": self.title, "content": self.content}
        resp = client.post("/posts", json=post_data)

        self.post = post_schema.PostCreateResponse(**resp.json())

    def test_udpate_post(self, client):
        update_data = {
            "title": "updated :^)",
            "content": "updated :^)",
            "user_id": self.user.id,
        }

        resp = client.patch(f"/posts/{self.post.id}", json=update_data)
        assert resp.status_code == status.HTTP_200_OK

        updated_post = post_schema.PostCreateResponse(**resp.json())
        assert updated_post.id == self.post.id
        assert updated_post.title != self.post.title
        assert updated_post.title == update_data["title"]
        assert updated_post.content != self.post.content
        assert updated_post.content == update_data["content"]

    def test_update_post_with_invalid_user_id(self, client):
        update_data = {
            "title": "updated :^)",
            "content": "updated :^)",
            "user_id": self.user.id + 100,
        }

        resp = client.patch(f"/posts/{self.post.id}", json=update_data)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_when_post_doesnt_exit_raise_error(self, client):
        update_data = {
            "title": "new!",
            "content": "new!",
            "user_id": self.user.id,
        }

        resp = client.patch(f"/posts/{self.post.id + 1}", json=update_data)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_try_update_post_by_different_post_owner(self, client):
        resp = client.post("/users", json={"name": "malicious-user001"})
        bot = user_schema.User(**resp.json())

        attack_data = {
            "title": "Dream Comes True",
            "conetnet": "Here is The List",
            "user_id": bot.id,
        }
        resp = client.patch(f"/posts/{self.post.id}", json=attack_data)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeletePost:
    def test_delete_post(self, client, initial):
        post_data = {"title": "deleted", "content": "hoge", "user_id": initial["user_id"]}
        resp = client.post("/posts", json=post_data)
        assert resp.status_code == status.HTTP_201_CREATED

        post_id = resp.json()["id"]

        resp = client.get("/posts")
        assert len(resp.json()) == 1

        resp = client.delete(f"/posts/{post_id}")
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        resp = client.get("/posts")
        assert len(resp.json()) == 0

    def test_delete_post_which_wrong_post_id(self, client, initial):
        post_data = {"title": "deleted", "content": "hoge", "user_id": initial["user_id"]}
        resp = client.post("/posts", json=post_data)
        assert resp.status_code == status.HTTP_201_CREATED

        post_id = resp.json()["id"]
        resp = client.delete(f"/posts/{post_id + 10}")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
