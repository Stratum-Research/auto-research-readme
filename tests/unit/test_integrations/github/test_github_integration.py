"""
Tests for GitHub integration.
"""

from unittest.mock import MagicMock, patch

from auto_readme.integration.platforms.github.integration import GitHubIntegration
from tests.fixtures.configs import DATASET_CONFIG, MINIMAL_CONFIG


class TestGitHubIntegration:
    """Test GitHub integration functionality."""

    def test_is_applicable_with_git_directory(self):
        """Test that integration is applicable when .git directory exists."""
        integration = GitHubIntegration()

        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = True
            assert integration.is_applicable(MINIMAL_CONFIG) is True

    def test_is_applicable_with_github_link(self):
        """Test that integration is applicable when github_link is provided."""
        integration = GitHubIntegration()
        config_with_link = {
            **MINIMAL_CONFIG,
            "github_link": "https://github.com/user/repo",
        }

        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = False
            assert integration.is_applicable(config_with_link) is True

    def test_is_not_applicable_without_git_or_link(self):
        """Test that integration is not applicable without git or github_link."""
        integration = GitHubIntegration()

        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = False
            assert integration.is_applicable(MINIMAL_CONFIG) is False

    def test_setup_creates_workflow_file(self):
        """Test that setup creates the GitHub Actions workflow file."""
        integration = GitHubIntegration()

        mock_template = MagicMock()
        mock_template.render.return_value = "workflow content"

        with (
            patch("pathlib.Path.mkdir") as mock_mkdir,
            patch("pathlib.Path.write_text") as mock_write,
            patch("jinja2.Environment.get_template", return_value=mock_template),
        ):
            result = integration.setup(DATASET_CONFIG)

            # Should create .github/workflows directory
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

            # Should write workflow file
            mock_write.assert_called_once_with("workflow content", encoding="utf-8")

            assert "GitHub Actions workflow" in result

    def test_get_requirements_returns_instructions(self):
        """Test that get_requirements returns setup instructions."""
        integration = GitHubIntegration()
        requirements = integration.get_requirements()

        assert isinstance(requirements, list)
        assert len(requirements) > 0
        assert any("GitHub" in req for req in requirements)
