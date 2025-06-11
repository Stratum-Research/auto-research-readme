#!/usr/bin/env python3
"""
Research Publication Generator
A minimal tool to generate publication files from a single config.
"""

import json
import yaml
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from huggingface_hub import create_repo
from huggingface_hub import HfApi, HfFolder, Repository


def load_config(path="config.yaml"):
    """Load YAML configuration file."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def generate_huggingface_card(config):
    """Generate Hugging Face dataset card JSON."""
    return json.dumps(
        {
            "title": config["title"],
            "pretty_name": config["tagline"],
            "version": config["version"],
            "language": config["language"],
            "license": "mit",
            "tags": config.get("hugging_face", {}).get("tags", []),
            "description": config["description"],
            "authors": [
                {
                    "name": c["name"],
                    "email": c["email"],
                    "affiliation": c["affiliation"],
                    "orcid": c["orcid"],
                }
                for c in config.get("contributors", [])
            ],
        },
        indent=2,
    )


def generate_zenodo_metadata(config):
    """Generate Zenodo metadata JSON."""
    return json.dumps(
        {
            "upload_type": "dataset",
            "publication_date": config["published"],
            "title": config["title"],
            "creators": [
                {
                    "name": f"{c['name'].split()[1]}, {c['name'].split()[0]}",
                    "affiliation": c["affiliation"],
                    "orcid": c["orcid"],
                }
                for c in config.get("contributors", [])
            ],
            "description": config["description"],
            "license": "mit",
            "keywords": config.get("hugging_face", {}).get("tags", []),
            "version": config["version"],
        },
        indent=2,
    )


def generate_citation(config):
    """Generate BibTeX citation."""
    return f"""@misc{{{config["title"].lower().replace("-", "_")},
  title={{{config["title"]}}},
  author={{{" and ".join([c["name"] for c in config.get("contributors", [])])}}},
  year={{{config["published"][:4]}}},
  version={{{config["version"]}}},
  doi={{{config.get("doi", "")}}},
  url={{{config.get("huggingface_link", "")}}}
}}"""


def generate_license(config):
    """Generate MIT License."""
    env = Environment(loader=FileSystemLoader("templates/"))
    template = env.get_template("License.md.j2")
    return template.render(**config)


def generate_readme(config):
    """Generate README from template."""
    env = Environment(loader=FileSystemLoader("templates/"))
    template = env.get_template("readme.md.j2")
    return template.render(**config)


def write_output(filename, content):
    """Write content to output file."""
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    (output_dir / filename).write_text(content)
    print(f"Generated: {filename}")


def push_to_huggingface(config):
    """Push to Hugging Face."""
    repo_url = create_repo(name=config.title)
    artifact_dir = f"./{config.title}"
    repo = Repository(
        local_dir=artifact_dir,
        clone_from=f"stratum-research/{config.title}",
    )
    repo.git_add()
    repo.git_commit("Commit using Auto-Open-Research package")
    repo.git_push()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate research publication files")
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    args = parser.parse_args()

    config = load_config(args.config)

    # Generate all files
    generators = {
        "dataset_card.json": generate_huggingface_card,
        "metadata.json": generate_zenodo_metadata,
        "citation.bib": generate_citation,
        "LICENSE.md": generate_license,
        "README.md": generate_readme,
    }

    for filename, generator in generators.items():
        try:
            content = generator(config)
            write_output(filename, content)
        except Exception as e:
            print(f"Error generating {filename}: {e}")


if __name__ == "__main__":
    main()
