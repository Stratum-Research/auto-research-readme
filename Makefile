.PHONY: help setup run clean test

help:
	@echo "Research Publication Generator"
	@echo ""
	@echo "Available commands:"
	@echo "  setup  - Install dependencies"
	@echo "  run    - Generate all publication files"
	@echo "  clean  - Clean output directory"
	@echo "  test   - Test the generator"

setup:
	pip install -r requirements.txt

run:
	python main.py

clean:
	rm -rf outputs/

test: run
	@echo "Testing file generation..."
	@test -f outputs/dataset_card.json && echo "✓ HuggingFace card generated"
	@test -f outputs/metadata.json && echo "✓ Zenodo metadata generated"
	@test -f outputs/citation.bib && echo "✓ Citation generated"
	@test -f outputs/LICENSE.md && echo "✓ License generated"
	@test -f outputs/README.md && echo "✓ README generated"
	@echo "All files generated successfully!"
