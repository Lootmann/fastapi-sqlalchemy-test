run:
	python3 -m uvicorn src.main:app --reload

migrate:
	python3 -m src.migrate_db

req:
	pip freeze > requirements.txt
