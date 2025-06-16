"""
Test fixture configurations for different project types.
"""

# Dataset config
DATASET_CONFIG = {
    "title": "Test Dataset",
    "description": "A test dataset for unit testing",
    "tagline": "A comprehensive test dataset",
    "version": "1.0.0",
    "type": "dataset",
    "published": "2025-01-15",
    "authors": [
        {
            "name": "Dr. Test Author",
            "orcid": "0000-0000-0000-0000",
            "affiliation": "Test University",
            "email": "test@university.edu",
        }
    ],
    "contributors": [  # For README template compatibility
        {
            "name": "Dr. Test Author",
            "orcid": "0000-0000-0000-0000",
            "affiliation": "Test University",
            "email": "test@university.edu",
        }
    ],
    "doi": "10.5281/zenodo.123456",
    "tags": ["test", "dataset", "machine-learning"],
    "keywords": ["test data", "machine learning"],
    "repository": "https://github.com/test/dataset",
    "badges": ["zenodo", "license", "github"],
}

# Python package config
PYTHON_PACKAGE_CONFIG = {
    "title": "Test Python Package",
    "description": "A test Python package for unit testing",
    "version": "2.0.0",
    "type": "python-package",
    "published": "2025-01-15",
    "authors": [
        {
            "name": "Dr. Package Author",
            "orcid": "0000-0001-0000-0001",
            "affiliation": "Dev University",
            "email": "dev@university.edu",
        }
    ],
    "contributors": [  # For README template compatibility
        {
            "name": "Dr. Package Author",
            "orcid": "0000-0001-0000-0001",
            "affiliation": "Dev University",
            "email": "dev@university.edu",
        }
    ],
    "repository": "https://github.com/test/python-package",
    "badges": ["license", "github", "pypi"],
}

# Research project config (no specific DOI or package type)
RESEARCH_PROJECT_CONFIG = {
    "title": "Test Research Project",
    "description": "A general research project for testing",
    "version": "1.5.0",
    "type": "research-project",
    "published": "2025-01-15",
    "authors": [
        {
            "name": "Dr. Research Author",
            "orcid": "0000-0002-0000-0002",
            "affiliation": "Research Institute",
            "email": "research@institute.edu",
        }
    ],
    "contributors": [  # For README template compatibility
        {
            "name": "Dr. Research Author",
            "orcid": "0000-0002-0000-0002",
            "affiliation": "Research Institute",
            "email": "research@institute.edu",
        }
    ],
    "repository": "https://github.com/test/research-project",
    "badges": ["license", "github"],
}

# Zenodo-specific config (has zenodo badge)
ZENODO_CONFIG = {
    "title": "Test Zenodo Project",
    "description": "A project with Zenodo integration",
    "version": "1.0.0",
    "type": "dataset",
    "published": "2025-01-15",
    "authors": [{"name": "Dr. Zenodo Author", "affiliation": "Archive University"}],
    "badges": ["zenodo", "license"],
    "repository": "https://github.com/test/zenodo-project",
}

# Minimal config (just required fields)
MINIMAL_CONFIG = {
    "title": "Minimal Test Project",
    "description": "Minimal configuration for testing",
    "version": "1.0.0",
    "contributors": [{"name": "Minimal Author", "affiliation": "Minimal University"}],
}
