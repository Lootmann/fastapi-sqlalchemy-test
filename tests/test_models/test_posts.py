from src.models.post import Post
from tests.init_client import test_client as client


def test_user_model():
    post_json = {"id": 1, "title": "title", "content": "content", "user_id": 1}
    post_model = Post(**post_json)

    assert str(post_model) == "<Post (id,title,content,user_id,comments) = (1,title,content,1,[])>"
