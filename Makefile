# ---------- CONFIG ----------
CONFIG=config.yaml

# ---------- METADATA GENERATION ----------
all:
	python3 src/main.py --config $(CONFIG)

# hf:
# 	python3 src/main.py --config $(CONFIG) --target hf

# zenodo:
# 	python3 src/main.py --config $(CONFIG) --target zenodo

# readme:
# 	python3 src/main.py --config $(CONFIG) --target readme

# citation:
# 	python3 src/main.py --config $(CONFIG) --target citation

# ---------- UTILITIES ----------
clean:
	rm -f outputs/dataset_card.json outputs/metadata.json outputs/README.md outputs/citation.bib outputs/LICENSE.md

# Run all and stage files for commit
build-and-stage:
	make all
	git add dataset_card.json metadata.json README.md citation.bib LICENSE.md

.PHONY: all hf zenodo readme citation license clean build-and-stage
