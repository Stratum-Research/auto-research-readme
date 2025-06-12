"""
Tests for PyPI integration.
"""

from unittest.mock import MagicMock, patch

from auto_readme.integrations.pypi.integration import PyPIIntegration
from tests.fixtures.configs import DATASET_CONFIG, PYTHON_PACKAGE_CONFIG


class TestPyPIIntegration:
    """Test PyPI integration functionality."""

    def test_is_applicable_for_python_package(self):
        """Test that integration is applicable for Python packages."""
        integration = PyPIIntegration()
        assert integration.is_applicable(PYTHON_PACKAGE_CONFIG) is True

    def test_is_not_applicable_for_dataset(self):
        """Test that integration is not applicable for datasets."""
        integration = PyPIIntegration()
        assert integration.is_applicable(DATASET_CONFIG) is False

    def test_setup_creates_workflow_file(self):
        """Test that setup creates the PyPI publishing workflow file."""
        integration = PyPIIntegration()

        mock_template = MagicMock()
        mock_template.render.return_value = "pypi workflow content"

        with (
            patch("pathlib.Path.mkdir") as mock_mkdir,
            patch("pathlib.Path.write_text") as mock_write,
            patch("jinja2.Environment.get_template", return_value=mock_template),
        ):
            result = integration.setup(PYTHON_PACKAGE_CONFIG)

            # Should create .github/workflows directory
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

            # Should write workflow file
            mock_write.assert_called_once_with(
                "pypi workflow content", encoding="utf-8"
            )

            assert "PyPI publishing workflow" in result

    def test_get_requirements_returns_instructions(self):
        """Test that get_requirements returns setup instructions."""
        integration = PyPIIntegration()
        requirements = integration.get_requirements()

        assert isinstance(requirements, list)
        assert len(requirements) > 0
        assert any("PyPI" in req for req in requirements)
