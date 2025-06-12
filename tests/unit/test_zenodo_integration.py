"""
Tests for Zenodo integration.
"""

from unittest.mock import MagicMock, patch

from auto_readme.integrations.zenodo.integration import ZenodoIntegration
from tests.fixtures.configs import DATASET_CONFIG, MINIMAL_CONFIG


class TestZenodoIntegration:
    """Test Zenodo integration functionality."""

    def test_is_applicable_with_zenodo_doi(self):
        """Test that integration is applicable with Zenodo DOI."""
        integration = ZenodoIntegration()
        assert integration.is_applicable(DATASET_CONFIG) is True

    def test_is_applicable_with_zenodo_link(self):
        """Test that integration is applicable with zenodo_link."""
        integration = ZenodoIntegration()
        config_with_link = {
            **MINIMAL_CONFIG,
            "zenodo_link": "https://zenodo.org/record/123456",
        }
        assert integration.is_applicable(config_with_link) is True

    def test_is_not_applicable_without_zenodo_references(self):
        """Test that integration is not applicable without Zenodo references."""
        integration = ZenodoIntegration()
        assert integration.is_applicable(MINIMAL_CONFIG) is False

    def test_setup_creates_metadata_file(self):
        """Test that setup creates the .zenodo.json metadata file."""
        integration = ZenodoIntegration()

        with (
            patch("pathlib.Path.write_text") as mock_write,
            patch("json.dumps", return_value='{"test": "metadata"}'),
        ):
            result = integration.setup(DATASET_CONFIG)

            # Should write metadata file
            mock_write.assert_called_once()

            assert "Zenodo metadata file" in result

    def test_get_requirements_returns_instructions(self):
        """Test that get_requirements returns setup instructions."""
        integration = ZenodoIntegration()
        requirements = integration.get_requirements()

        assert isinstance(requirements, list)
        assert len(requirements) > 0
        assert any("Zenodo" in req for req in requirements)
