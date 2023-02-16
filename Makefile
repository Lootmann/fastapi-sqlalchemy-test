run:
	PYTHONDONTWRITEBYTECODE=1 python3 -m uvicorn src.main:app --reload --port 8000

.PHONY: test
test:
	PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -svv

.PHONY: cov
cov:
	PYTHONDONTWRITEBYTECODE=1 python3 -m pytest --cov --cov-report=html

.PHONY: migrate
migrate:
	PYTHONDONTWRITEBYTECODE=1 python3 -m src.migrate_db

.PHONY: req
req:
	pip freeze > requirements.txt

.PHONY: docs
docs:
	google-chrome http://127.0.0.1:8000/docs

# git behavior
.PHONY: pre
pre:
	pre-commit run --all-files
