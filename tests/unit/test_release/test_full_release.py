from unittest.mock import patch, mock_open
from auto_readme.cli import cmd_make_all
from argparse import Namespace


def test_all_outputs_regenerated_on_version_change():
    config_content = """
version: "2.0.0"
changelog:
  "2.0.0":
    - Major update
contributors:
  - name: "Test User"
    affiliation: "Test Org"
    email: "test@example.com"
description: "Test description"
title: "Test Project"
tagline: "Test tagline"
published: "2025-01-01"
license: "MIT"
tags: ["test"]
"""
    # Patch open for config.yaml and all output files
    with (
        patch("builtins.open", mock_open(read_data=config_content)),
        patch("auto_readme.cli.write_output") as mock_write,
        patch(
            "auto_readme.generator.load_config",
            return_value={
                "version": "2.0.0",
                "changelog": {"2.0.0": ["Major update"]},
                "contributors": [
                    {
                        "name": "Test User",
                        "affiliation": "Test Org",
                        "email": "test@example.com",
                    }
                ],
                "description": "Test description",
                "title": "Test Project",
                "tagline": "Test tagline",
                "published": "2025-01-01",
                "license": "MIT",
                "tags": ["test"],
            },
        ),
        patch("auto_readme.cli.generate_readme", return_value="# Dummy README\n"),
    ):
        args = Namespace(config="config.yaml")
        cmd_make_all(args)
        written_files = [call.args[0] for call in mock_write.call_args_list]
        assert "README.md" in written_files
        assert "LICENSE" in written_files
        assert "citation.bib" in written_files
        # You can add more assertions for other files as needed
