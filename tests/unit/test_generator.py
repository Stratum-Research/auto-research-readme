"""
Tests for the generator module.
"""

from pathlib import Path
from unittest.mock import mock_open, patch

from auto_readme.generator import (
    generate_citation,
    generate_license,
    load_config,
)
from tests.fixtures.configs import DATASET_CONFIG


class TestLoadConfig:
    """Test configuration loading functionality."""

    def test_load_config_from_specific_path(self):
        """Test loading config from a specific path."""
        mock_config = {"title": "Test Project"}

        with patch("builtins.open", mock_open(read_data="title: Test Project")):
            with patch("yaml.safe_load", return_value=mock_config):
                with patch("pathlib.Path.exists", return_value=True):
                    result = load_config("custom_config.yaml")
                    assert result == mock_config

    def test_load_config_searches_default_locations(self):
        """Test that load_config searches in config/ then current directory."""
        mock_config = {"title": "Test Project"}

        with patch("builtins.open", mock_open(read_data="title: Test Project")):
            with patch("yaml.safe_load", return_value=mock_config):
                with patch("pathlib.Path.exists") as mock_exists:
                    # First call for config/config.yaml returns True
                    mock_exists.side_effect = [True]
                    result = load_config()
                    assert result == mock_config


class TestGenerateCitation:
    """Test citation generation functionality."""

    def test_generate_citation_creates_bibtex(self):
        """Test that generate_citation creates proper BibTeX format."""
        result = generate_citation(DATASET_CONFIG)

        assert "@dataset{" in result
        assert "title={" in result
        assert "author={" in result
        assert "year={" in result


class TestGenerateLicense:
    """Test license generation functionality."""

    def test_generate_license_creates_mit_license(self):
        """Test that generate_license creates MIT license."""
        result = generate_license(DATASET_CONFIG)

        assert "MIT License" in result
        assert "Copyright (c)" in result
        assert "Permission is hereby granted" in result
