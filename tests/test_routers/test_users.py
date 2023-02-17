from fastapi import status

from src.schemas import user as user_schema
from tests.init_client import test_client as client
from tests.util import random_string


class TestPostUser:
    def test_create_user(self, client):
        username = random_string()
        password = random_string()

        resp = client.post("/users", json={"name": username, "password": password})
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
            client.post("/users", json={"name": random_string(), "password": random_string()})

        resp = client.get("/users")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 10

    def test_get_user(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers: dict = user_fixture[1]

        resp = client.get(f"/users/{user.id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = user_schema.User(**resp.json())
        assert resp_obj.name == user.name
        assert resp_obj.posts == []
        assert resp_obj.comments == []

    def test_get_user_which_doesnt_exist(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        resp = client.get(f"/users/{user.id + 10000}", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestGetPostByUser:
    def test_get_all_posts_by_user_id(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        # create post
        post_data = {"title": random_string(), "content": random_string(), "user_id": user.id}
        client.post("/posts", json=post_data, headers=headers)
        client.post("/posts", json=post_data, headers=headers)
        client.post("/posts", json=post_data, headers=headers)

        # get user, user has posts
        resp = client.get(f"/users/{user.id}/posts", headers=headers)
        posts = resp.json()
        assert len(posts) == 3

        # this resp is same as above ...
        resp = client.get(f"/users/{user.id}", headers=headers)
        posts = resp.json()["posts"]
        assert len(posts) == 3

    def test_get_post_by_user_id_and_post_id(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        post_data = {"title": random_string(), "content": random_string(), "user_id": user.id}
        resp = client.post("/posts", json=post_data, headers=headers)
        post_id = resp.json()["id"]

        resp = client.get(f"/users/{user.id}/posts/{post_id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        # wrong post_id
        resp = client.get(f"/users/{user.id}/posts/{post_id + 1}", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        # wrong user_id
        resp = client.get(f"/users/{user.id+ 1}/posts/{post_id}", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestGetCommentByUser:
    def test_get_comments_by_user_id(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        resp = client.get(f"/users/{user.id}/comments", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 0

        post_data = {"title": random_string(), "content": random_string(), "user_id": user.id}
        resp = client.post("/posts", json=post_data, headers=headers)
        post_id = resp.json()["id"]

        comment_data = {"comment": random_string(), "user_id": user.id, "post_id": post_id}
        client.post("/comments", json=comment_data, headers=headers)

        comment_data = {"comment": random_string(), "user_id": user.id, "post_id": post_id}
        client.post("/comments", json=comment_data, headers=headers)

        comment_data = {"comment": random_string(), "user_id": user.id, "post_id": post_id}
        client.post("/comments", json=comment_data, headers=headers)

        resp = client.get(f"/users/{user.id}/comments", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 3

    def test_get_comments_which_doesnt_exist_user(self, client, user_fixture):
        headers = user_fixture[1]
        resp = client.get("/users/123/comments", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_get_comment_by_user_id(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        post_data = {"title": random_string(), "content": random_string(), "user_id": user.id}
        resp = client.post("/posts", json=post_data, headers=headers)
        post_id = resp.json()["id"]

        comment_data = {"comment": "now testing...", "user_id": user.id, "post_id": post_id}
        resp = client.post("/comments", json=comment_data, headers=headers)
        comment_id = resp.json()["id"]

        resp = client.get(f"/users/{user.id}/comments/{comment_id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["comment"] == "now testing..."

        # wrong comment_id
        resp = client.get(f"/users/{user.id}/comments/{comment_id + 1}", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        # wrong user_id
        resp = client.get(f"/users/{user.id + 1}/comments/{comment_id}", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateUser:
    def test_update_user(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        resp = client.patch(f"/users/{user.id}", json={"name": "updated"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        updated_user = user_schema.User(**resp.json())
        assert updated_user.id == user.id
        assert updated_user.name == "updated"
        assert updated_user.name != user.name

    def test_update_user_which_doesnt_exists(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        resp = client.patch(f"/users/{user.id + 100}", json={"name": "updated"}, headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteUser:
    def test_delete(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        resp = client.get("/users", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        resp = client.delete(f"/users/{user.id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        resp = client.get("/users", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

    def test_delete_which_user_doesnt_exist(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        resp = client.delete(f"/users/{user.id + 100}", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
