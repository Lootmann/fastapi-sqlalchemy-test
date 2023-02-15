from tests.init_client import test_client as client

from src.models.user import User
from src.models.post import Post


def test_user_model():
    user_json = {"id": 1, "name": "James bar"}
    user_model = User(**user_json)

    post_json = {"id": 1, "title": "title", "content": "content", "user_id": 1}
    post_model = Post(**post_json)
    user_model.posts.append(post_model)

    assert (
        str(user_model)
        == "<User (id, name, posts) 1,James bar,[<Post (id,title,content,user_id,comments) = (1,title,content,1,[])>]>"
    )
