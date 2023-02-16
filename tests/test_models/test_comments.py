from src.models.comment import Comment
from src.models.post import Post
from src.models.user import User
from tests.init_client import test_client as client


def test_user_model():
    user_json = {"id": 1, "name": "James bar"}
    user_model = User(**user_json)

    post_json = {"id": 1, "title": "title", "content": "content", "user_id": 1}
    post_model = Post(**post_json)

    comment_json = {
        "id": 1,
        "comment": "This post is cool",
        "user_id": user_model.id,
        "post_id": post_model.id,
    }
    comment_model = Comment(**comment_json)

    assert (
        str(comment_model)
        == f"<Comment (id,comment,user_id,post_id) = (1,This post is cool,{user_model.id},{post_model.id})>"
    )
