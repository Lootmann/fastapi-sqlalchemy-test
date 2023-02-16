# FastAPI + SQLAlchemy

Relation のテスト

## Relation

```
- User
    - Post
        - Comment
        - Comment
    - Post
        - Comment
        - Comment
        - Comment
```

## URL

REST な感じで

1. Router を設定
2. API を設定
3. 中身見ながら Schema をいじくる
4. Test して

- users

  - [x] `GET  /users`
  - [x] `POST /users`
  - [x] `GET  /users/:id`
  - [x] `PUT  /users/:id`
  - [x] `DEL  /users/:id`
  - [x] `GET  /users/:id/posts`
  - [x] `GET  /users/:id/posts/:id`
  - [x] `GET  /users/:id/comments`
  - [ ] `GET  /users/:id/comments/:id`

- posts (Required: user_id)

  - [x] `GET    /posts`
  - [x] `POST   /posts`
  - [x] `GET    /posts/:id`
  - [x] `PATCH  /posts/:id`
  - [x] `DEL    /posts/:id`
  - [ ] `GET    /posts/:id/comments`
  - [ ] `GET    /posts/:id/comments/:id`

- comments (Required: user_id, and post_id)

  - [x] `GET  /comments`
  - [x] `POST /comments`
  - [x] `GET  /comments/:id`
  - [x] `PUT  /comments/:id`
  - [x] `DEL  /comments/:id`

## Thinking 🤔

```
GET  /users/:id/posts
GET  /users/:id/posts/:id
GET  /users/:id/comments
GET  /users/:id/comments/:id
```

when I get the response of /user/:id,
I can get all posts and comments, so I wonder if this is really necessary.
Maybe, nothing.
