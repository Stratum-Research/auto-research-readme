"""
Zenodo integration for auto-research-readme.

This integration creates Zenodo metadata files for academic dataset publishing
when Zenodo DOIs or badges are detected in the project configuration.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from ..base import BaseIntegration, ConfigDict


class ZenodoIntegration(BaseIntegration):
    """
    Zenodo metadata integration for academic publishing.

    This integration creates .zenodo.json metadata files that Zenodo uses
    for automatic metadata extraction when depositing research datasets.

    Applicable when Zenodo DOI or Zenodo badge is present in the configuration.
    """

    def is_applicable(self, config: ConfigDict) -> bool:
        """
        Check if Zenodo integration should be enabled.

        Args:
            config: Project configuration dictionary.

        Returns:
            True if DOI contains 'zenodo' or zenodo_link is specified.
        """
        # Check for Zenodo DOI
        doi = config.get("doi", "").lower()
        has_zenodo_doi = "zenodo" in doi

        # Check for Zenodo link
        zenodo_link = config.get("zenodo_link", "").lower()
        has_zenodo_link = "zenodo" in zenodo_link

        return has_zenodo_doi or has_zenodo_link

    def setup(self, config: ConfigDict) -> str:
        """
        Set up Zenodo metadata file.

        Args:
            config: Project configuration dictionary.

        Returns:
            Description of what was set up.

        Raises:
            Exception: If metadata file creation fails.
        """
        try:
            metadata = self._create_zenodo_metadata(config)

            # Write .zenodo.json file
            zenodo_file = Path(".zenodo.json")
            zenodo_file.write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
            )

            return f"Created Zenodo metadata file at {zenodo_file}"

        except Exception as e:
            raise Exception(f"Failed to create Zenodo metadata: {e}")

    def get_requirements(self) -> List[str]:
        """
        Get manual steps for Zenodo integration.

        Returns:
            List of instructions for the user.
        """
        return [
            "Create a Zenodo account at https://zenodo.org/",
            "Upload your dataset to Zenodo",
            "The .zenodo.json file will automatically populate metadata fields",
            "Update the DOI in config.yaml once your dataset is published",
        ]

    def _create_zenodo_metadata(self, config: ConfigDict) -> Dict[str, Any]:
        """
        Create Zenodo metadata dictionary from project config.

        Args:
            config: Project configuration dictionary.

        Returns:
            Dictionary containing Zenodo metadata.
        """
        # Determine upload type based on project type
        project_type = config.get("type", "dataset")
        upload_type_mapping = {
            "dataset": "dataset",
            "python-package": "software",
            "research": "publication",
        }
        upload_type = upload_type_mapping.get(project_type, "dataset")

        # Create creators list from contributors
        creators = []
        for contributor in config.get("contributors", []):
            creator = {
                "name": self._format_author_name(contributor["name"]),
                "affiliation": contributor.get("affiliation", ""),
            }

            # Add ORCID if available
            if contributor.get("orcid"):
                creator["orcid"] = contributor["orcid"]

            creators.append(creator)

        # Extract publication year from date
        publication_date = config.get("published", "2025-01-01")

        metadata = {
            "upload_type": upload_type,
            "publication_date": publication_date,
            "title": config.get("title", ""),
            "creators": creators,
            "description": config.get("description", ""),
            "license": {"id": "MIT"},
            "keywords": config.get("tags", []),
            "version": config.get("version", "1.0.0"),
        }

        # Add DOI if available
        if config.get("doi"):
            metadata["doi"] = config["doi"]

        # Add related identifiers
        related_identifiers = []

        if config.get("github_link"):
            related_identifiers.append(
                {
                    "identifier": config["github_link"],
                    "relation": "isSupplementTo",
                    "resource_type": "software",
                }
            )

        if config.get("huggingface_link"):
            related_identifiers.append(
                {
                    "identifier": config["huggingface_link"],
                    "relation": "isIdenticalTo",
                    "resource_type": "dataset",
                }
            )

        if related_identifiers:
            metadata["related_identifiers"] = related_identifiers

        return metadata

    def _format_author_name(self, name: str) -> str:
        """
        Format author name in 'Last, First' format for Zenodo.

        Args:
            name: Author name in any format.

        Returns:
            Formatted name in 'Last, First' format.
        """
        name_parts = name.strip().split()
        if len(name_parts) == 1:
            return name_parts[0]
        elif len(name_parts) >= 2:
            last_name = name_parts[-1]
            first_names = " ".join(name_parts[:-1])
            return f"{last_name}, {first_names}"
        else:
            return name
