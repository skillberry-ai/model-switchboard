.PHONY: help install install-dev install-all clean build test lint format verify publish coverage

help:
	@echo "Available commands:"
	@echo "  make install          - Install package with default LiteLLM support"
	@echo "  make install-dev      - Install package with development dependencies"
	@echo "  make install-all      - Install package with all provider dependencies"
	@echo "  make test             - Run tests"
	@echo "  make coverage         - Run tests with coverage"
	@echo "  make lint             - Run static checks"
	@echo "  make format           - Format Python code"
	@echo "  make build            - Build distribution packages"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-all:
	pip install -e ".[all,dev]"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean
	python -m build

test:
	pytest

coverage:
	pytest --cov=model_switchboard --cov-report=term-missing

lint:
	black --check .
	isort --check-only .
	flake8 model_switchboard tests

format:
	black .
	isort .

verify: lint coverage build

# Install specific providers
install-openai:
	pip install -e ".[openai]"

install-watsonx:
	pip install -e ".[watsonx]"

install-rits:
	pip install -e ".[rits]"

install-ollama:
	pip install -e ".[ollama]"
