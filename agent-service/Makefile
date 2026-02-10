.PHONY: help setup install test lint run clean

help:
	@echo "Agent Service - Available targets:"
	@echo "  make setup      - Create virtual environment and install dependencies"
	@echo "  make install    - Install dependencies in existing environment"
	@echo "  make test       - Run pytest test suite"
	@echo "  make lint       - Run code quality checks"
	@echo "  make run        - Run agent service (placeholder)"
	@echo "  make clean      - Remove build artifacts and cache"

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

install:
	pip install -r requirements.txt

test:
	pytest -v

test-coverage:
	pytest --cov=src --cov-report=html

lint:
	black --check src tests
	mypy src

format:
	black src tests

run:
	python -m src.agent

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	find . -type d -name '.coverage' -delete
	find . -type d -name 'htmlcov' -delete
	find . -type d -name 'build' -delete
	find . -type d -name 'dist' -delete
	find . -type d -name '*.egg-info' -delete
