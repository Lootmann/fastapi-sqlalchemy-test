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

- users

  - [ ] `GET  /users`
  - [ ] `GET  /users/:id`
  - [ ] `POST /users`
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
