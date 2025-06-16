"""
Tests for integration discovery system.
"""

from unittest.mock import MagicMock, patch

from auto_readme.integration import INTEGRATIONS, setup_all_integrations
from auto_readme.integration.platforms.github.integration import GitHubIntegration
from auto_readme.integration.platforms.pypi.integration import PyPIIntegration
from auto_readme.integration.platforms.zenodo.integration import ZenodoIntegration
from tests.fixtures.configs import DATASET_CONFIG, MINIMAL_CONFIG, PYTHON_PACKAGE_CONFIG


class TestIntegrationDiscovery:
    """Test integration discovery logic."""

    def test_integrations_list_exists(self):
        """Test that INTEGRATIONS list is properly defined."""
        assert isinstance(INTEGRATIONS, list)
        assert len(INTEGRATIONS) == 3
        assert GitHubIntegration in INTEGRATIONS
        assert ZenodoIntegration in INTEGRATIONS
        assert PyPIIntegration in INTEGRATIONS

    def test_github_integration_applicable_for_git_repo(self):
        """Test that GitHub integration is applicable when git repo exists."""
        integration = GitHubIntegration()

        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = True
            assert integration.is_applicable(MINIMAL_CONFIG) is True

    def test_github_integration_applicable_for_github_link(self):
        """Test that GitHub integration is applicable when github_link exists."""
        integration = GitHubIntegration()
        config_with_github = {
            **MINIMAL_CONFIG,
            "github_link": "https://github.com/user/repo",
        }

        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = False
            assert integration.is_applicable(config_with_github) is True

    def test_zenodo_integration_applicable_for_zenodo_doi(self):
        """Test that Zenodo integration is applicable for Zenodo DOI."""
        integration = ZenodoIntegration()
        assert integration.is_applicable(DATASET_CONFIG) is True

    def test_pypi_integration_applicable_for_python_package(self):
        """Test that PyPI integration is applicable for Python packages."""
        integration = PyPIIntegration()
        assert integration.is_applicable(PYTHON_PACKAGE_CONFIG) is True
        assert integration.is_applicable(DATASET_CONFIG) is False


class TestSetupAllIntegrations:
    """Test the setup_all_integrations function."""

    def test_setup_all_integrations_calls_applicable_integrations(self):
        """Test that setup_all_integrations only calls applicable integrations."""
        with patch("builtins.print"):
            # Mock all integrations to be not applicable
            with (
                patch.object(GitHubIntegration, "is_applicable", return_value=False),
                patch.object(ZenodoIntegration, "is_applicable", return_value=False),
                patch.object(PyPIIntegration, "is_applicable", return_value=False),
            ):
                result = setup_all_integrations(MINIMAL_CONFIG)
                assert result == []

    def test_setup_all_integrations_sets_up_applicable_integrations(self):
        """Test that setup_all_integrations sets up applicable integrations."""
        with patch("builtins.print"):
            # Mock GitHub integration as applicable and successful
            with (
                patch.object(GitHubIntegration, "is_applicable", return_value=True),
                patch.object(
                    GitHubIntegration, "setup", return_value="Setup successful"
                ),
                patch.object(GitHubIntegration, "get_requirements", return_value=[]),
                patch.object(ZenodoIntegration, "is_applicable", return_value=False),
                patch.object(PyPIIntegration, "is_applicable", return_value=False),
            ):
                result = setup_all_integrations(MINIMAL_CONFIG)
                assert "GitHub" in result

    def test_setup_all_integrations_handles_exceptions(self):
        """Test that setup_all_integrations handles setup exceptions."""
        with patch("builtins.print"):
            # Mock GitHub integration to fail setup
            with (
                patch.object(GitHubIntegration, "is_applicable", return_value=True),
                patch.object(
                    GitHubIntegration, "setup", side_effect=Exception("Test error")
                ),
                patch.object(ZenodoIntegration, "is_applicable", return_value=False),
                patch.object(PyPIIntegration, "is_applicable", return_value=False),
            ):
                try:
                    setup_all_integrations(MINIMAL_CONFIG)
                    assert False, "Should have raised exception"
                except Exception as e:
                    assert "Test error" in str(e)
