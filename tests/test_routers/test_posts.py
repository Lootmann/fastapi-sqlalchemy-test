from fastapi import status

from src.schemas import auth as auth_schema
from src.schemas import post as post_schema
from src.schemas import user as user_schema
from tests.init_client import test_client as client
from tests.util import login_and_create_token, random_string


class TestGetPost:
    def test_get_all_posts(self, client, user_fixture):
        headers = user_fixture[1]

        resp = client.get("/posts", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 0

    def test_get_one_post(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        post_data = {"title": "new post", "content": "nah"}
        resp = client.post("/posts", json=post_data, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        post_resp = post_schema.PostCreateResponse(**resp.json())
        resp = client.get(f"/posts/{post_resp.id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        post = post_schema.Post(**resp.json())
        assert post.user_id == user.id
        assert post.id == post_resp.id
        assert post.title == post_resp.title
        assert post.content == post_resp.content
        assert post.comments == []

    def test_get_one_post_raise_error(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        post_data = {
            "title": "new post",
            "content": "nah",
        }
        resp = client.post("/posts", json=post_data, headers=headers)
        post = post_schema.PostCreateResponse(**resp.json())

        # does not exit post id
        resp = client.get(f"/posts/{post.id + 1}", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        # wrong post id type
        resp = client.get(f"/posts/hoge", headers=headers)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetCommentsByPost:
    def test_comments_by_post_id(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        # create post
        post_data = {
            "title": "new post",
            "content": "nah",
        }
        resp = client.post("/posts", json=post_data, headers=headers)
        post_id = resp.json()["id"]

        # create comment
        comment_data = {
            "comment": random_string(),
            "user_id": user.id,
            "post_id": post_id,
        }
        resp = client.post("/comments", json=comment_data, headers=headers)

        comment_data = {
            "comment": random_string(),
            "user_id": user.id,
            "post_id": post_id,
        }
        client.post("/comments", json=comment_data, headers=headers)

        # get comment by post_id
        resp = client.get(f"/posts/{post_id}/comments", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 2

    def test_comments_by_post_id_which_does_not_exist(self, client, user_fixture):
        headers = user_fixture[1]
        resp = client.get("/posts/123345/comments", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestPostPost:
    def test_create_post(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        resp = client.post(
            "/posts",
            json={
                "title": "hoge",
                "content": "hage",
            },
            headers=headers,
        )
        assert resp.status_code == status.HTTP_201_CREATED

        post = post_schema.PostCreateResponse(**resp.json())
        assert post.title == "hoge"
        assert post.content == "hage"

        resp = client.get(f"/users/{user.id}", headers=headers)
        user = user_schema.User(**resp.json())
        assert user.posts != []

        assert user.posts[0].title == post.title
        assert user.posts[0].content == post.content

    def test_create_post_without_field(self, client, user_fixture):
        user: user_schema.UserCreateResponse = user_fixture[0]
        headers = user_fixture[1]

        resp = client.post("/posts", json={"title": "hoge"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.post("/posts", json={"content": "hoge"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.post("/posts", json={}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.get("/posts", headers=headers)
        resp_json = resp.json()
        assert len(resp_json) == 3


class TestPatchPost:
    def test_udpate_post(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        update_data = {
            "title": "updated :^)",
            "content": "updated :^)",
            "user_id": post.user_id,
        }

        resp = client.patch(f"/posts/{post.id}", json=update_data, headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        updated_post = post_schema.PostCreateResponse(**resp.json())
        assert updated_post.id == post.id
        assert updated_post.title != post.title
        assert updated_post.title == update_data["title"]
        assert updated_post.content != post.content
        assert updated_post.content == update_data["content"]

    def test_when_post_doesnt_exit_raise_error(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        update_data = {
            "title": "new!",
            "content": "new!",
            "user_id": post.user_id,
        }

        resp = client.patch(f"/posts/{post.id + 1}", json=update_data, headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_try_update_post_by_different_post_owner(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]

        # create bot account
        resp = client.post(
            "/users",
            json={
                "name": "malicious-user001",
                "password": "iL0V3Earth",
            },
        )
        bot = user_schema.User(**resp.json())

        # get access_token
        token_resp = client.post(
            "/token",
            data={"username": bot.name, "password": "iL0V3Earth"},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        token = auth_schema.Token(**token_resp.json())
        headers = {"Authorization": "Bearer {}".format(token.access_token)}

        # try to update other owner's post
        attack_data = {
            "title": "Dream Comes True",
            "conetnet": "Here is The List",
        }
        resp = client.patch(f"/posts/{post.id}", json=attack_data, headers=headers)

        # this bot has no right to edit no-ownership post
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


class TestDeletePost:
    def test_delete_post(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        resp = client.delete(f"/posts/{post.id}", headers=headers)
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        resp = client.get("/posts", headers=headers)
        assert len(resp.json()) == 0

    def test_delete_post_which_wrong_post_id(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        resp = client.delete(f"/posts/{post.id+ 10}", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_post_which_wrong_login_user(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]

        username, password = random_string(), random_string()
        resp = client.post("/users", json={"name": username, "password": password})
        different_header = login_and_create_token(client, username, password)

        resp = client.delete(f"/posts/{post.id}", headers=different_header)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
