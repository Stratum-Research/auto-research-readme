.PHONY: help setup install test clean dev-install publish

help:
	@echo "Auto Research README - Pip Package"
	@echo ""
	@echo "Available commands:"
	@echo "  setup        - Install package dependencies"
	@echo "  install      - Install package globally"
	@echo "  dev-install  - Install package in development mode"
	@echo "  test         - Test the package"
	@echo "  clean        - Clean build artifacts"
	@echo "  publish      - Build and publish to PyPI"

setup:
	pip install -r requirements.txt

install:
	pip install .

dev-install:
	pip install -e .

test: dev-install
	@echo "Testing package installation..."
	@auto-research-readme --version && echo "Package installed successfully"
	@echo "Testing init command..."
	@mkdir -p test-tmp && cd test-tmp && auto-research-readme init && echo "Init command works"
	@echo "Testing readme generation..."
	@cd test-tmp && auto-research-readme make readme && echo "README generation works"
	@rm -rf test-tmp
	@echo "All tests passed!"

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

publish: clean
	python -m build
	python -m twine upload dist/*
