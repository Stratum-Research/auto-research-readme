#!/usr/bin/env python3
"""
Core README generation functionality.

This module provides the main functions for generating README files, citations,
licenses, and handling configuration loading.
"""

import json
from pathlib import Path
from typing import Any, Dict, Union

import yaml
from jinja2 import Environment, FileSystemLoader, PackageLoader

ConfigDict = Dict[str, Any]


def load_config(config_path: str = "config.yaml") -> ConfigDict:
    """
    Load YAML configuration file.

    Args:
        config_path: Path to the configuration file. Defaults to "config.yaml".
                    If default is used, searches in config/config.yaml first.

    Returns:
        Dictionary containing the loaded configuration.

    Raises:
        FileNotFoundError: If the configuration file cannot be found.
        yaml.YAMLError: If the YAML file is malformed.
    """
    # If a specific path is provided, try it first
    if config_path != "config.yaml":
        specific_path = Path(config_path)
        if specific_path.exists():
            with open(specific_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        else:
            raise FileNotFoundError(f"Could not find config file: {config_path}")

    # Default search order for config.yaml
    possible_paths = [
        Path("config") / "config.yaml",
        Path("config.yaml"),
    ]

    for path in possible_paths:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)

    raise FileNotFoundError(
        "Could not find config.yaml in current directory or config/ folder"
    )


def generate_readme(config: ConfigDict) -> str:
    """
    Generate README from template.

    Args:
        config: Configuration dictionary containing project metadata.

    Returns:
        Generated README content as a string.

    Raises:
        jinja2.TemplateNotFound: If the README template cannot be found.
    """
    try:
        # Try to load from package templates first
        env = Environment(loader=PackageLoader("auto_readme", "templates"))
        template = env.get_template("readme.md.j2")
    except Exception:
        # Fallback to local templates folder if package not installed
        env = Environment(loader=FileSystemLoader("templates/"))
        template = env.get_template("readme.md.j2")

    return template.render(**config)


def generate_huggingface_card(config: ConfigDict) -> str:
    """
    Generate Hugging Face dataset card JSON.

    Args:
        config: Configuration dictionary containing project metadata.

    Returns:
        JSON string containing Hugging Face dataset card metadata.
    """
    card_data = {
        "title": config["title"],
        "pretty_name": config["title"].lower(),
        "version": config["version"],
        "language": config.get("language", ["en"]),
        "license": "mit",
        "tags": config.get("tags", []),
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
    }

    return json.dumps(card_data, indent=2)


def generate_zenodo_metadata(config: ConfigDict) -> str:
    """
    Generate Zenodo metadata JSON.

    Args:
        config: Configuration dictionary containing project metadata.

    Returns:
        JSON string containing Zenodo metadata.
    """
    metadata = {
        "upload_type": "dataset",
        "publication_date": config["published"],
        "title": config["title"],
        "creators": [
            {
                "name": f"{c['name'].split()[-1]}, {' '.join(c['name'].split()[:-1])}",
                "affiliation": c["affiliation"],
                "orcid": c["orcid"],
            }
            for c in config.get("contributors", [])
        ],
        "description": config["description"],
        "license": "mit",
        "keywords": config.get("tags", []),
        "version": config["version"],
    }

    return json.dumps(metadata, indent=2)


def generate_citation(config: ConfigDict) -> str:
    """
    Generate BibTeX citation.

    Args:
        config: Configuration dictionary containing project metadata.

    Returns:
        BibTeX citation string.
    """
    # Create citation key from title
    citation_key = config["title"].lower().replace("-", "_").replace(" ", "_")

    # Get authors from contributors
    authors = " and ".join([c["name"] for c in config.get("contributors", [])])

    # Extract year from publication date
    year = config["published"][:4]

    citation = f"""@dataset{{{citation_key}_data,
  title={{{config["title"]}: {config["tagline"]}}},
  author={{{authors}}},
  year={{{year}}},
  version={{{config["version"]}}},
  doi={{{config.get("doi", "")}}},
  url={{{config.get("huggingface_link", "")}}}
}}"""

    return citation


def generate_license(config: ConfigDict) -> str:
    """
    Generate MIT License.

    Args:
        config: Configuration dictionary containing project metadata.

    Returns:
        MIT License text with proper attribution.
    """
    # Extract year and author information
    year = config.get("published", "2025")[:4]
    contributors = config.get("contributors", [])
    author = contributors[0].get("name", "Author") if contributors else "Author"

    license_text = f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

    return license_text


def write_output(
    filename: str, content: str, output_dir: Union[str, Path] = "./"
) -> None:
    """
    Write content to output file.

    Args:
        filename: Name of the file to write.
        content: Content to write to the file.
        output_dir: Directory to write the file to. Defaults to current directory.

    Raises:
        OSError: If the file cannot be written.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    file_path = output_path / filename
    file_path.write_text(content, encoding="utf-8")
    print(f"✓ Generated: {filename}")
