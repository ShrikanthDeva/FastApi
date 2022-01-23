import pytest
from app import schemas
from test.conftest import client
def test_get_all_posts(authoraized_client, test_posts):
    res= authoraized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts = map(validate,res.json())
    # print(list(posts))
    assert len(res.json())== len(test_posts)
    assert res.status_code==200

def test_unauthoraised_user_get_all_posts(client, test_posts):
    res= client.get("/posts/")
    assert res.status_code == 401

def test_unauthoraised_user_get_one_posts(client, test_posts):
    res= client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authoraized_client, test_posts):
    res = authoraized_client.get(f"/posts/8888888")
    assert res.status_code == 404

def test_get_one_post(authoraized_client, test_posts):
    res = authoraized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authoraized_client, test_user, test_posts, title, content, published):
    res = authoraized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authoraized_client, test_user, test_posts):
    res = authoraized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "aasdfjasdf"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthoraized_create_posts(client,test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code == 401

def test_unauthoraized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authoraized_client, test_user, test_posts):
    res = authoraized_client.delete(
        f"/posts/{test_posts[0].id}")

    assert res.status_code == 204
    
def test_delete_post_non_exist(authoraized_client, test_user, test_posts):
    res = authoraized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_delete_other_user_post(authoraized_client, test_user, test_posts):
    res = authoraized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authoraized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authoraized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authoraized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authoraized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthoraized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authoraized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authoraized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404