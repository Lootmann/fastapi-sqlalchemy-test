run:
	PYTHONDONTWRITEBYTECODE=1 python3 -m uvicorn src.main:app --reload --port 8000

.PHONY: test
test:
	python3 -m pytest -svv

.PHONY: migrate
migrate:
	python3 -m src.migrate_db

.PHONY: req
req:
	pip freeze > requirements.txt

.PHONY: docs
docs:
	google-chrome http://127.0.0.1:8000/docs
