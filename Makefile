OPTION = PYTHONDONTWRITEBYTECODE=1

run:
	$(OPTION) python3 -m uvicorn src.main:app --reload --port 8000

.PHONY: test
test:
	#$(OPTION) python3 -m pytest ./tests/test_routers/test_comments.py -svv
	$(OPTION) python3 -m pytest -svv

.PHONY: cov
cov:
	$(OPTION) python3 -m pytest --cov --cov-report=html

.PHONY: profile
profile:
	$(OPTION) python3 -m pytest --profile-svg

.PHONY: measure
measure:
	$(OPTION) python3 -m pytest --durations=0 -vv > ./tmp/pytest-durations.log

.PHONY: migrate
migrate:
	$(OPTION) python3 -m src.migrate_db

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
