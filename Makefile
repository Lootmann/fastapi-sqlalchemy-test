run:
	python3 -m uvicorn src.main:app --reload

.PHONY: test
test:
	python3 -m pytest -svv

migrate:
	python3 -m src.migrate_db

req:
	pip freeze > requirements.txt

docs:
	google-chrome http://127.0.0.1:8000/docs
