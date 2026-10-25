# Foundations brownfield exercise repo — med-claim-lite
# No Docker, no network: Python 3.12 + SQLite only.
DB ?= medclaim.db

.PHONY: help seed test run lint clean

help:
	@echo "make seed   build a fresh SQLite database from seed/data/*.json"
	@echo "make test   run the pytest suite"
	@echo "make run    serve the API at http://localhost:8000"
	@echo "make lint   run ruff on the era-3 code"

seed:
	python seed/build_seed.py $(DB)

test: seed
	pytest

run: seed
	uvicorn medclaim.api:app --reload --port 8000

lint:
	ruff check .

clean:
	rm -f $(DB)
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
