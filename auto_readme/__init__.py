"""
Auto Research README - Professional README Generator for Research Projects.

A Python package that generates professional README files, citations, licenses,
and automation workflows from simple YAML configuration files.

Key Features:
- Professional README generation with badges and formatting
- Academic citation generation (BibTeX)
- MIT license generation
- GitHub Actions workflow automation
- Zenodo metadata integration
- PyPI publishing automation

Example:
    >>> from auto_readme.generator import generate_readme, load_config
    >>> config = load_config("config.yaml")
    >>> readme_content = generate_readme(config)
"""

__version__ = "1.0.0"
__author__ = "Abdullah Ridwan"
__email__ = "abdullah.ridwan@stratumresearch.com"

# Public API
from .generator import (
    generate_citation,
    generate_license,
    generate_readme,
    load_config,
    write_output,
)

__all__ = [
    "generate_citation",
    "generate_license",
    "generate_readme",
    "load_config",
    "write_output",
    "__version__",
]
