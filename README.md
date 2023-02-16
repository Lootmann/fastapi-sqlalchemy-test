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

  - [x] `GET   /users`
  - [x] `POST  /users`
  - [x] `GET   /users/:id`
  - [x] `PATCH /users/:id`
  - [x] `DEL   /users/:id`
  - [x] `GET   /users/:id/posts`
  - [x] `GET   /users/:id/posts/:id`
  - [x] `GET   /users/:id/comments`
  - [x] `GET   /users/:id/comments/:id`

- posts (Required: user_id)

  - [x] `GET   /posts`
  - [x] `POST  /posts`
  - [x] `GET   /posts/:id`
  - [x] `PATCH /posts/:id`
  - [x] `DEL   /posts/:id`
  - [x] `GET   /posts/:id/comments`
  - ~~[x] `GET    /posts/:id/comments/:id`~`

- comments (Required: user_id, and post_id)

  - [x] `GET   /comments`
  - [x] `POST  /comments`
  - [x] `GET   /comments/:id`
  - [x] `PATCH /comments/:id`
  - [x] `DEL   /comments/:id`

## Thinking 🤔

### API1

```
GET /users/:id/posts
GET /users/:id/posts/:id
GET /users/:id/comments
GET /users/:id/comments/:id
```

when I get the response of /user/:id,
I can get all posts and comments, so I wonder if this is really necessary.
Maybe, nothing.

### API2

```
GET /posts/:id/comments/:id
```

これは本当に不要 comment_id だけの指定で十分な気が

## Todo

- Authentication
  - Authentication -> sign_up/login -> get_current_user
