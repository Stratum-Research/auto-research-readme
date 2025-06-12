#!/usr/bin/env python3
"""
Command-line interface for auto-research-readme.

This module provides the main CLI commands for the auto-research-readme package,
including initialization, README generation, and automation setup.
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict

from .generator import (
    generate_citation,
    generate_license,
    generate_readme,
    load_config,
    write_output,
)

ConfigDict = Dict[str, Any]


def cmd_make_readme(args: argparse.Namespace) -> None:
    """
    Generate README.md and LICENSE in the top level directory.

    Args:
        args: Command line arguments containing config path.

    Raises:
        SystemExit: If generation fails.
    """
    try:
        config = load_config(args.config)

        # Generate README.md in current directory
        readme_content = generate_readme(config)
        write_output("README.md", readme_content)

        # Generate LICENSE in current directory
        license_content = generate_license(config)
        write_output("LICENSE", license_content)

        print("✓ Generated README.md")
        print("✓ Generated LICENSE")
        print("🎉 Repository files generated successfully!")

    except Exception as e:
        print(f"❌ Error generating files: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_make_all(args: argparse.Namespace) -> None:
    """
    Generate all repository files from config.

    Args:
        args: Command line arguments containing config path.

    Raises:
        SystemExit: If generation fails.
    """
    try:
        config = load_config(args.config)

        generators = {
            "README.md": generate_readme,
            "LICENSE": generate_license,
            "citation.bib": generate_citation,
        }

        generated_files = []
        for filename, generator in generators.items():
            try:
                content = generator(config)
                write_output(filename, content)
                generated_files.append(filename)
            except Exception as e:
                print(f"❌ Error generating {filename}: {e}", file=sys.stderr)

        if generated_files:
            for filename in generated_files:
                print(f"✓ Generated {filename}")
            print("🎉 All repository files generated successfully!")
        else:
            print("❌ No files were generated successfully")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_init(args: argparse.Namespace) -> None:
    """
    Initialize a new project with sample config.

    Args:
        args: Command line arguments (unused for init).
    """
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)

    assets_dir = config_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    sample_config = """title: "My-Dataset"
version: "1.0"
published: "2025-01-01"
tagline: "A sample dataset for demonstration"
description: "This is a sample dataset description. Replace with your actual description."
doi: "10.5281/zenodo.123456"

# Metadata for HuggingFace/README
language:
  - "en"
tags:
  - "machine-learning"
  - "dataset"
  - "sample"
size_categories:
  - "1K<n<10K"

logo_path: "config/assets/logo.png"
banner_path: "config/assets/banner.png"

# Links
github_link: "https://github.com/yourusername/your-repo"
huggingface_link: "https://huggingface.co/datasets/yourusername/your-dataset"
zenodo_link: "https://zenodo.org/record/123456"

# Author info
maintainer: "your.email@example.com"
contributors:
  - name: "Your Name"
    orcid: "0000-0000-0000-0000"
    email: "your.email@example.com"
    affiliation: "Your Organization"
    role: "creator"
"""

    config_file = config_dir / "config.yaml"
    if config_file.exists():
        print("⚠️  config/config.yaml already exists. Skipping...")
    else:
        config_file.write_text(sample_config)
        print("✓ Created config/config.yaml")

    # Create placeholder asset files
    readme_assets = """# Assets Folder

Place your project assets here:
- `logo.png` - Your project logo (recommended: 150px height)
- `banner.png` - Banner image for README (recommended: 800px width)

These will be referenced in your README.md automatically.
"""

    (assets_dir / "README.md").write_text(readme_assets)
    print("✓ Created config/assets/ folder")
    print("\n🎉 Project initialized! Next steps:")
    print("1. Edit config/config.yaml with your project details")
    print("2. Add logo.png and banner.png to config/assets/")
    print("3. Run 'auto-research-readme make readme' to generate README.md and LICENSE")


def cmd_automate(args: argparse.Namespace) -> None:
    """
    Set up automation integrations.

    Args:
        args: Command line arguments containing config path.

    Raises:
        SystemExit: If automation setup fails.
    """
    try:
        from .integrations import setup_all_integrations

        config = load_config(args.config)
        setup_all_integrations(config)

    except Exception as e:
        print(f"❌ Error setting up automation: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate consistent, professional READMEs from YAML config",
        prog="auto-research-readme",
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Make subcommand
    make_parser = subparsers.add_parser("make", help="Generate files from config")
    make_subparsers = make_parser.add_subparsers(
        dest="make_what", help="What to generate"
    )

    # Make readme
    readme_parser = make_subparsers.add_parser(
        "readme", help="Generate README.md and LICENSE"
    )
    readme_parser.add_argument(
        "--config", default="config.yaml", help="Config file path"
    )
    readme_parser.set_defaults(func=cmd_make_readme)

    # Make all
    all_parser = make_subparsers.add_parser("all", help="Generate all repository files")
    all_parser.add_argument("--config", default="config.yaml", help="Config file path")
    all_parser.set_defaults(func=cmd_make_all)

    # Init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize new project with sample config"
    )
    init_parser.set_defaults(func=cmd_init)

    # Automate command
    automate_parser = subparsers.add_parser(
        "automate", help="Set up automation integrations"
    )
    automate_parser.add_argument(
        "--config", default="config.yaml", help="Config file path"
    )
    automate_parser.set_defaults(func=cmd_automate)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
