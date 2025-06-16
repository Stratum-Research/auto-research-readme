.PHONY: help install install-dev test test-integration clean lint format format-check type-check pre-commit build publish ci dev-setup release

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in development mode
	pip install -e .

install-dev:  ## Install package with development dependencies
	pip install -e .
	pip install -r requirements-dev.txt

test:  ## Run unit tests
	PYTHONPATH=. pytest tests/ -v

test-integration:  ## Run integration tests with sample configs
	@echo "Running integration tests..."
	PYTHONPATH=. python -m auto_readme.cli init
	PYTHONPATH=. python -m auto_readme.cli make all
	@echo "Integration tests completed successfully!"

test-coverage:  ## Run tests with coverage report
	PYTHONPATH=. pytest tests/ --cov=auto_readme --cov-report=html --cov-report=term

clean:  ## Clean build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:  ## Run linting checks
	flake8 auto_readme/ tests/
	mypy auto_readme/

format:  ## Format code with black and isort
	black auto_readme/ tests/
	isort auto_readme/ tests/

format-check:  ## Check if code needs formatting
	black --check auto_readme/ tests/
	isort --check-only auto_readme/ tests/

type-check:  ## Run type checking
	mypy auto_readme/

pre-commit-install:  ## Install pre-commit hooks
	pre-commit install

pre-commit:  ## Run pre-commit on all files
	pre-commit run --all-files

build:  ## Build package for distribution
	python -m build

publish:  ## Publish package to PyPI (requires setup)
	python -m build
	python -m twine upload dist/*

ci:  ## Run full CI pipeline locally
	make clean
	make lint
	make type-check
	make test
	make format-check
	@echo "✅ All CI checks passed!"

dev-setup:  ## Complete development environment setup
	make install-dev
	make pre-commit-install
	@echo "🎉 Development environment ready!"

release:  ## Create a new release based on config.yaml version
	python auto_readme/integration/release/release.py
