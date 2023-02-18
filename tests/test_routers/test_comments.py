from fastapi import status

from src.schemas import comment as comment_schema
from src.schemas import post as post_schema
from tests.init_client import test_client as client


class TestGetComment:
    def test_get_all_comments(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        resp = client.get("/comments", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

        comment_data = {
            "comment": "new comment",
            "post_id": post.id,
        }
        resp = client.post(f"/comments", json=comment_data, headers=headers)

        resp = client.get("/comments", headers=headers)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

    def test_get_one_comment_with_wrong_comment_id(self, client, post_fixture):
        headers = post_fixture[1]
        resp = client.get("/comments/12", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_get_one_comment(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        # create commnt
        comment_data = {
            "comment": "new comment",
            "post_id": post.id,
        }
        resp = client.post(f"/comments", json=comment_data, headers=headers)
        comment_id = resp.json()["id"]

        # get comment by comment_id
        resp = client.get(f"/comments/{comment_id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        comment = comment_schema.Comment(**resp.json())
        assert comment.id == comment_id
        assert comment.comment == "new comment"
        assert comment.post_id == post.id


class TestPostComment:
    def test_create_post(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        # get comments
        resp = client.get("/comments", headers=headers)
        assert len(resp.json()) == 0

        # create comment
        comment_data = {"comment": "this is a comment", "user_id": post.user_id, "post_id": post.id}
        resp = client.post("/comments", json=comment_data, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        created_comment = resp.json()
        assert created_comment["comment"] == "this is a comment"
        assert created_comment["user_id"] == post.user_id
        assert created_comment["post_id"] == post.id

        # get comments
        resp = client.get("/comments", headers=headers)
        assert len(resp.json()) == 1

        resp = client.get(f"/posts/{post.id}", headers=headers)
        post = post_schema.Post(**resp.json())
        assert post.id == post.id
        assert len(post.comments) == 1

        assert created_comment["comment"] == post.comments[0].comment
        assert created_comment["user_id"] == post.comments[0].user_id
        assert created_comment["post_id"] == post.comments[0].post_id

    def test_create_post_which_wrong_comment_id(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        # create comment
        comment_data = {
            "comment": "this is a comment",
            "user_id": post.user_id,
            "post_id": post.id + 1,
        }
        resp = client.post("/comments", json=comment_data, headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateComment:
    def test_udpate_comment(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        comment_data = {
            "comment": "old comment",
            "post_id": post.id,
        }
        resp = client.post("/comments", json=comment_data, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        comment = comment_schema.CommentCreateResponse(**resp.json())

        resp = client.get(f"/comments/{comment.id}", headers=headers)
        comment_json = resp.json()
        assert comment_json["comment"] == "old comment"

        # update
        new_comment_data = {
            "comment": "updated :^)",
            "post_id": post.id,
        }
        resp = client.patch(f"/comments/{comment.id}", json=new_comment_data, headers=headers)
        assert resp.status_code == status.HTTP_200_OK

    def test_update_comment_which_take_wrong_post_id(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        comment_data = {
            "comment": "old comment",
            "post_id": post.id,
        }
        resp = client.post("/comments", json=comment_data, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        comment_id = resp.json()["id"]
        comment_data["post_id"] += 12
        resp = client.patch(f"/comments/{comment_id}", json=comment_data, headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_update_comment_which_has_wrong_comment_id(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        comment_data = {
            "comment": "old comment",
            "post_id": post.id,
        }
        resp = client.post("/comments", json=comment_data, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.patch("/comments/123", json=comment_data, headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteComment:
    def test_delete_comment(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        # create comment
        comment_data = {
            "comment": "this is a comment",
            "post_id": post.id,
        }
        resp = client.post("/comments", json=comment_data, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        comment_id = resp.json()["id"]

        # get all comments
        resp = client.get("/comments", headers=headers)
        assert len(resp.json()) == 1

        # delete comment
        resp = client.delete(f"/comments/{comment_id}", headers=headers)
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        resp = client.get("/comments", headers=headers)
        assert len(resp.json()) == 0

    def test_delete_comment_which_wrong_comment_id(self, client, post_fixture):
        post: post_schema.PostCreateResponse = post_fixture[0]
        headers = post_fixture[1]

        # create comment
        comment_data = {
            "comment": "this is a comment",
            "post_id": post.id,
        }
        resp = client.post("/comments", json=comment_data, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        comment_id = resp.json()["id"]
        resp = client.delete(f"/comments/{comment_id + 1}", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
