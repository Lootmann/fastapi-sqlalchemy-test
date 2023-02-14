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
  - [x] `GET  /users/:id`
  - [x] `POST /users`
  - [x] `PUT  /users/:id`
  - [ ] `GET  /users/:id/posts`
  - [ ] `GET  /users/:id/posts/:id`
  - [ ] `GET  /users/:id/comments`
  - [ ] `GET  /users/:id/comments/:id`

- posts (Required: user_id)

  - [ ] `GET  /posts`
  - [ ] `GET  /posts/:id`
  - [ ] `GET  /posts/:id/comments`
  - [ ] `GET  /posts/:id/comments/:id`
  - [ ] `POST /posts`

- comments (Required: user_id, and post_id)

  - [ ] `GET  /comments`
  - [ ] `GET  /comments/:id`
  - [ ] `POST /comments`
